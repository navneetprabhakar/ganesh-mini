#!/usr/bin/env python3
"""Versioned post-teacher/pre-review evidence contract for repair-delta v4.

This module does not execute generated code.  It seals and validates results
from an executor that used the frozen commands in the v4 preflight config.
V3 envelopes and evidence schemas are intentionally not accepted here.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Callable

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import (
    SANDBOX_CONTRACT, infrastructure_failure, load_runtime, verify_commands,
)


PLAN_SHA256 = "79849d2f8b70ba69572b4c3fa1761bdb413562c6f6d9a12537d93a1724812ef6"
CONTRACT_ID = "capability-stratified-v4-repair-delta/v1"
CONFIG_SCHEMA = "ganesh-mini-repair-delta-v4-preflight-config/v1"
EVIDENCE_SCHEMA = "ganesh-mini-repair-delta-v4-post-teacher-preflight/v1"
OUTCOME_SCHEMA = "ganesh-mini-repair-delta-v4-post-teacher-preflight-outcome/v1"
RETRY_SCHEMA = "ganesh-mini-repair-delta-v4-preflight-retry-ledger/v1"
WITNESS_SCHEMA = "ganesh-mini-repair-delta-v4-known-bad-cross-witness/v1"
PROOF_SCHEMA = "ganesh-mini-repair-delta-v4-proof/v1"
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
PROOF_STRING_FIELDS = {
    "capability_operation", "defective_intermediate_or_decision",
    "valid_domain_counterexample", "minimal_capability_specific_patch",
    "scheduled_dimension_obligation",
}
PROOF_BOOLEAN_FIELDS = {
    "known_bad_already_satisfies_scheduled_dimension",
    "cross_dimension_only_patch_cannot_solve",
    "capability_remains_substantive_without_cross_clause",
}
RESULT_KEYS = {
    "runtime_id", "image", "image_id", "commands", "exit_codes", "timed_out",
    "stdout", "stdout_sha256", "stderr", "stderr_sha256", "duration_ms",
    "sandbox_contract_sha256",
}
VISIBILITY = {
    "boundary": "post-teacher-pre-semantic-review-pre-test-author",
    "compile_feedback_visible_to_semantic_reviewer": False,
    "compile_feedback_visible_to_test_author": False,
    "known_bad_cross_witness_visible_to_semantic_reviewer": False,
    "known_bad_cross_witness_visible_to_test_author": False,
    "witness_results_visible_to_test_author": False,
    "evaluation_artifacts_read": 0,
}


class V4PreflightFailure(ValueError):
    """Fail-closed v4 preflight contract violation."""

    def __init__(
        self, message: str, *, evidence: dict[str, Any] | None = None,
        status: str = "terminal-rejected",
    ) -> None:
        super().__init__(message)
        self.evidence = evidence
        self.status = status


CommandExecutor = Callable[[dict[str, Any], str, Path, list[list[str]]], dict[str, Any]]


def _exact(value: Any, keys: set[str], where: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise V4PreflightFailure(f"{where}: keys differ from the v4 contract")
    return value


def _nonempty(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V4PreflightFailure(f"{where}: expected non-empty string")
    return value


def _sha(value: Any, where: str) -> str:
    if (
        not isinstance(value, str) or len(value) != 64
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise V4PreflightFailure(f"{where}: expected lowercase SHA-256")
    return value


def _commands(value: Any, where: str) -> list[list[str]]:
    if not isinstance(value, list) or not value or any(
        not isinstance(command, list) or not command
        or any(not isinstance(part, str) or not part for part in command)
        for command in value
    ):
        raise V4PreflightFailure(f"{where}: expected non-empty argv arrays")
    return value


def load_preflight_config(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _exact(
        value,
        {"schema_version", "contract_id", "plan_sha256", "success_marker", "lanes", "config_sha256"},
        "preflight config",
    )
    body = dict(value)
    claimed = body.pop("config_sha256")
    if (
        value["schema_version"] != CONFIG_SCHEMA
        or value["contract_id"] != CONTRACT_ID
        or value["plan_sha256"] != PLAN_SHA256
        or claimed != canonical_sha256(body)
        or not isinstance(value["lanes"], dict)
        or set(value["lanes"]) != set(LANES)
    ):
        raise V4PreflightFailure("preflight config identity or seal mismatch")
    marker = _nonempty(value["success_marker"], "preflight config success_marker")
    for lane, raw in value["lanes"].items():
        item = _exact(raw, {"compile_commands", "witness_path", "witness_commands"}, f"config lane {lane}")
        _commands(item["compile_commands"], f"config lane {lane} compile commands")
        _commands(item["witness_commands"], f"config lane {lane} witness commands")
        path_value = PurePosixPath(_nonempty(item["witness_path"], f"config lane {lane} witness path"))
        if path_value.is_absolute() or ".." in path_value.parts:
            raise V4PreflightFailure(f"config lane {lane}: unsafe witness path")
    if any(marker in json.dumps(item["compile_commands"]) for item in value["lanes"].values()):
        raise V4PreflightFailure("success marker must not occur in compile commands")
    return value


def test_author_projection_v4(candidate: dict[str, Any], assignment: dict[str, Any]) -> dict[str, Any]:
    """Return the complete V4 test-author view; preflight evidence is not an input."""
    validation = candidate["verification_task"]["validation"]
    return {
        "id": candidate["id"],
        "specification": candidate["messages"][0]["content"],
        "lane": candidate["lane"],
        "embedded_known_bad": validation["known_bad"][0]["code"],
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        "primary_capability_definition": assignment["primary_capability_definition"],
    }


def _validate_candidate_assignment(candidate: dict[str, Any], assignment: dict[str, Any]) -> None:
    lane = candidate.get("lane")
    task = candidate.get("verification_task")
    validation = task.get("validation") if isinstance(task, dict) else None
    known_bad = validation.get("known_bad") if isinstance(validation, dict) else None
    if (
        lane not in LANES
        or not isinstance(task, dict)
        or task.get("language") != lane
        or not isinstance(validation, dict)
        or not isinstance(known_bad, list) or len(known_bad) != 1
        or assignment.get("contract_id") != CONTRACT_ID
        or assignment.get("id") != candidate.get("id")
        or assignment.get("cell_id") != f"{assignment.get('primary_capability')}/{lane}/repair"
        or not isinstance(assignment.get("primary_capability"), str)
        or not assignment["primary_capability"]
        or not isinstance(assignment.get("primary_capability_definition"), str)
        or not assignment["primary_capability_definition"]
        or not isinstance(assignment.get("assigned_cross_cutting_dimension"), str)
        or not assignment["assigned_cross_cutting_dimension"]
    ):
        raise V4PreflightFailure("candidate and assignment do not bind the V4 repair cell")
    for name, implementation in (
        ("reference", validation.get("reference")), ("known_bad", known_bad[0]),
    ):
        if (
            not isinstance(implementation, dict)
            or not isinstance(implementation.get("code"), str)
            or _sha(implementation.get("sha256"), f"{name}.sha256")
            != sha256_text(implementation["code"])
        ):
            raise V4PreflightFailure(f"{name}: code hash mismatch")


def validate_teacher_proof_v4(
    candidate: dict[str, Any], assignment: dict[str, Any], proof: Any,
) -> dict[str, Any]:
    expected = {
        "schema_version", "candidate_id", "teacher_candidate_sha256",
        "queue_record_sha256", "primary_capability",
        "assigned_cross_cutting_dimension", *PROOF_STRING_FIELDS,
        *PROOF_BOOLEAN_FIELDS, "known_bad_cross_witness",
        "teacher_run_evidence_sha256", "visibility", "evidence_sha256",
    }
    value = _exact(proof, expected, "V4 teacher proof")
    body = dict(value)
    claimed = body.pop("evidence_sha256")
    if (
        value["schema_version"] != PROOF_SCHEMA
        or value["candidate_id"] != candidate["id"]
        or value["teacher_candidate_sha256"] != canonical_sha256(candidate)
        or value["primary_capability"] != assignment["primary_capability"]
        or value["assigned_cross_cutting_dimension"]
        != assignment["assigned_cross_cutting_dimension"]
        or any(not isinstance(value[field], str) or not value[field].strip() for field in PROOF_STRING_FIELDS)
        or any(value[field] is not True for field in PROOF_BOOLEAN_FIELDS)
        or _sha(value["queue_record_sha256"], "teacher proof queue_record_sha256")
        != value["queue_record_sha256"]
        or _sha(value["teacher_run_evidence_sha256"], "teacher proof run evidence")
        != value["teacher_run_evidence_sha256"]
        or value["visibility"] != {
            "source_affinity_card": True,
            "source_lineage": True,
            "runtime_contract": True,
            "evaluation_artifacts_read": 0,
        }
        or claimed != canonical_sha256(body)
    ):
        raise V4PreflightFailure("V4 teacher proof is unsealed or unbound")
    return value


def validate_witness(value: Any, lane_config: dict[str, Any], marker: str) -> dict[str, Any]:
    witness = _exact(
        value,
        {
            "schema_version", "valid_domain_input", "scheduled_dimension_assertion",
            "path", "content", "content_sha256", "valid_domain",
            "scheduled_dimension_only",
        },
        "known_bad_cross_witness",
    )
    if (
        witness["schema_version"] != WITNESS_SCHEMA
        or witness["path"] != lane_config["witness_path"]
        or witness["valid_domain"] is not True
        or witness["scheduled_dimension_only"] is not True
        or _sha(witness["content_sha256"], "known_bad_cross_witness.content_sha256")
        != sha256_text(_nonempty(witness["content"], "known_bad_cross_witness.content"))
        or witness["content"].count(marker) != 1
    ):
        raise V4PreflightFailure("known_bad_cross_witness is unbound or not isolated")
    _nonempty(witness["valid_domain_input"], "known_bad_cross_witness.valid_domain_input")
    _nonempty(
        witness["scheduled_dimension_assertion"],
        "known_bad_cross_witness.scheduled_dimension_assertion",
    )
    return witness


def _runtime_binding(
    candidate: dict[str, Any], runtime_path: Path, runtime: dict[str, Any],
) -> dict[str, Any]:
    return {
        "runtime_config_sha256": hashlib.sha256(runtime_path.read_bytes()).hexdigest(),
        "runtime_id": candidate["verification_task"]["runtime_id"],
        "language": candidate["lane"],
        "candidate_path": candidate["verification_task"]["candidate_path"],
        "image": runtime["image"],
        "image_id": runtime["image_id"],
        "manifest_digest": runtime["manifest_digest"],
        "rootfs_layers_sha256": canonical_sha256(runtime["rootfs_layers"]),
        "platform": runtime["platform"],
    }


def _support_files(candidate: dict[str, Any]) -> list[dict[str, str]]:
    files = candidate["verification_task"]["files"]
    if not isinstance(files, list) or any(item.get("role") != "support" for item in files):
        raise V4PreflightFailure("post-teacher preflight candidate must contain no test files")
    return [{"path": item["path"], "sha256": item["sha256"]} for item in files]


def _execution_sha256(
    candidate: dict[str, Any], phase: str, implementation: str,
    commands: list[list[str]], staged_files: list[dict[str, str]],
) -> str:
    return canonical_sha256({
        "contract_id": CONTRACT_ID,
        "candidate_id": candidate["id"],
        "candidate_sha256": canonical_sha256(candidate),
        "phase": phase,
        "implementation": implementation,
        "implementation_sha256": candidate["verification_task"]["validation"][implementation]["sha256"]
        if implementation == "reference" else candidate["verification_task"]["validation"]["known_bad"][0]["sha256"],
        "lane": candidate["lane"],
        "runtime_id": candidate["verification_task"]["runtime_id"],
        "candidate_path": candidate["verification_task"]["candidate_path"],
        "commands": commands,
        "staged_files": staged_files,
    })


def _implementation_sha(candidate: dict[str, Any], implementation: str) -> str:
    validation = candidate["verification_task"]["validation"]
    return validation["reference"]["sha256"] if implementation == "reference" else validation["known_bad"][0]["sha256"]


def _bind_result(
    candidate: dict[str, Any], phase: str, implementation: str,
    commands: list[list[str]], staged_files: list[dict[str, str]], result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "implementation_sha256": _implementation_sha(candidate, implementation),
        "execution_sha256": _execution_sha256(
            candidate, phase, implementation, commands, staged_files,
        ),
        "result": copy.deepcopy(result),
    }


def _attempt_input_binding(
    candidate: dict[str, Any], phase: str, implementation: str,
    commands: list[list[str]], staged_files: list[dict[str, str]],
    runtime_path: Path, runtime: dict[str, Any],
) -> dict[str, Any]:
    return {
        "execution_sha256": _execution_sha256(
            candidate, phase, implementation, commands, staged_files,
        ),
        "candidate_sha256": canonical_sha256(candidate),
        "implementation_sha256": _implementation_sha(candidate, implementation),
        "staged_files": copy.deepcopy(staged_files),
        "runtime_binding": _runtime_binding(candidate, runtime_path, runtime),
        "limits_sha256": canonical_sha256(candidate["verification_task"]["limits"]),
        "commands": copy.deepcopy(commands),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
    }


def _retry_ledger(
    candidate: dict[str, Any], rows: list[dict[str, Any]], status: str,
) -> dict[str, Any]:
    value = {
        "schema_version": RETRY_SCHEMA,
        "candidate_sha256": canonical_sha256(candidate),
        "maximum_attempts": 2,
        "status": status,
        "executions": copy.deepcopy(rows),
        "evaluation_artifacts_read": 0,
    }
    value["ledger_sha256"] = canonical_sha256(value)
    return value


def validate_preflight_retry_ledger(
    value: Any, candidate: dict[str, Any], expected_status: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise V4PreflightFailure("preflight retry ledger is missing")
    body = dict(value)
    claimed = body.pop("ledger_sha256", None)
    rows = value.get("executions")
    if (
        claimed != canonical_sha256(body)
        or value.get("schema_version") != RETRY_SCHEMA
        or value.get("candidate_sha256") != canonical_sha256(candidate)
        or value.get("maximum_attempts") != 2
        or value.get("status") != expected_status
        or value.get("evaluation_artifacts_read") != 0
        or not isinstance(rows, list) or not rows
    ):
        raise V4PreflightFailure("preflight retry ledger is unsealed or unbound")
    for row in rows:
        attempts = row.get("attempts") if isinstance(row, dict) else None
        if (
            not isinstance(row, dict)
            or set(row) != {"phase", "implementation", "input_binding", "attempts"}
            or row.get("phase") not in {"compile_syntax", "known_bad_cross_witness"}
            or row.get("implementation") not in {"reference", "known_bad"}
            or not isinstance(row.get("input_binding"), dict)
            or not isinstance(attempts, list) or not 1 <= len(attempts) <= 2
        ):
            raise V4PreflightFailure("preflight retry ledger execution row is malformed")
        for ordinal, attempt in enumerate(attempts, 1):
            result = attempt.get("result") if isinstance(attempt, dict) else None
            classification = attempt.get("classification") if isinstance(attempt, dict) else None
            expected_classification = (
                "timeout" if isinstance(result, dict) and result.get("timed_out") is True
                else infrastructure_failure(result) if isinstance(result, dict) else "malformed-result"
            )
            if (
                not isinstance(attempt, dict)
                or set(attempt) != {"attempt", "classification", "result"}
                or attempt.get("attempt") != ordinal
                or not isinstance(result, dict)
                or classification != expected_classification
            ):
                raise V4PreflightFailure("preflight retry attempt is malformed or misclassified")
        if attempts[0]["classification"] is None and len(attempts) != 1:
            raise V4PreflightFailure("preflight replay occurred without infrastructure failure")
        if attempts[0]["classification"] is not None and len(attempts) != 2:
            raise V4PreflightFailure("preflight infrastructure failure lacks its one replay")
    return value


def _terminal_outcome(
    candidate: dict[str, Any], assignment: dict[str, Any], runtime_path: Path,
    config: dict[str, Any], runtime: dict[str, Any], status: str,
    phase: str, implementation: str, reason: str, rows: list[dict[str, Any]],
) -> dict[str, Any]:
    value = {
        "schema_version": OUTCOME_SCHEMA, "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256, "status": status,
        "candidate_id": candidate["id"], "candidate_sha256": canonical_sha256(candidate),
        "assignment_sha256": canonical_sha256(assignment),
        "preflight_config_sha256": config["config_sha256"],
        "runtime_binding": _runtime_binding(candidate, runtime_path, runtime),
        "failed_phase": phase, "failed_implementation": implementation,
        "reason": reason, "retry_ledger": _retry_ledger(candidate, rows, status),
        "visibility": dict(VISIBILITY),
    }
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def validate_preflight_outcome_evidence(value: Any) -> dict[str, Any]:
    expected = {
        "schema_version", "contract_id", "plan_sha256", "status", "candidate_id",
        "candidate_sha256", "assignment_sha256", "preflight_config_sha256",
        "runtime_binding", "failed_phase", "failed_implementation", "reason",
        "retry_ledger", "visibility", "evidence_sha256",
    }
    outcome = _exact(value, expected, "post-teacher preflight outcome")
    body = dict(outcome)
    claimed = body.pop("evidence_sha256")
    if (
        outcome["schema_version"] != OUTCOME_SCHEMA
        or outcome["contract_id"] != CONTRACT_ID
        or outcome["plan_sha256"] != PLAN_SHA256
        or outcome["status"] not in {"terminal-rejected", "unresolved"}
        or outcome["failed_phase"] not in {"compile_syntax", "known_bad_cross_witness"}
        or outcome["failed_implementation"] not in {"reference", "known_bad"}
        or not isinstance(outcome["reason"], str) or not outcome["reason"]
        or outcome["visibility"] != VISIBILITY
        or claimed != canonical_sha256(body)
    ):
        raise V4PreflightFailure("post-teacher preflight outcome is unsealed or malformed")
    # The ledger's candidate binding is also fixed by the enclosing sealed outcome.
    ledger = outcome["retry_ledger"]
    ledger_body = dict(ledger) if isinstance(ledger, dict) else {}
    ledger_claimed = ledger_body.pop("ledger_sha256", None)
    if (
        ledger_claimed != canonical_sha256(ledger_body)
        or ledger.get("schema_version") != RETRY_SCHEMA
        or ledger.get("candidate_sha256") != outcome["candidate_sha256"]
        or ledger.get("status") != outcome["status"]
        or ledger.get("maximum_attempts") != 2
        or ledger.get("evaluation_artifacts_read") != 0
    ):
        raise V4PreflightFailure("post-teacher preflight outcome retry ledger mismatch")
    rows = ledger.get("executions")
    if not isinstance(rows, list) or not rows:
        raise V4PreflightFailure("post-teacher preflight outcome has no execution attempts")
    for row in rows:
        attempts = row.get("attempts") if isinstance(row, dict) else None
        if (
            not isinstance(row, dict)
            or set(row) != {"phase", "implementation", "input_binding", "attempts"}
            or not isinstance(row.get("input_binding"), dict)
            or not isinstance(attempts, list) or not 1 <= len(attempts) <= 2
        ):
            raise V4PreflightFailure("post-teacher preflight outcome attempt row is malformed")
        for ordinal, attempt in enumerate(attempts, 1):
            result = attempt.get("result") if isinstance(attempt, dict) else None
            classification = (
                "timeout" if isinstance(result, dict) and result.get("timed_out") is True
                else infrastructure_failure(result) if isinstance(result, dict) else "malformed-result"
            )
            if (
                not isinstance(attempt, dict) or attempt.get("attempt") != ordinal
                or attempt.get("classification") != classification
            ):
                raise V4PreflightFailure("post-teacher preflight outcome attempt classification mismatch")
        if attempts[0]["classification"] is not None and len(attempts) != 2:
            raise V4PreflightFailure("post-teacher preflight outcome omitted its one replay")
    final_attempts = rows[-1]["attempts"]
    if (outcome["status"] == "unresolved") is not (final_attempts[-1]["classification"] is not None):
        raise V4PreflightFailure("post-teacher preflight outcome status is inconsistent")
    return outcome


def build_post_teacher_preflight_evidence(
    candidate: dict[str, Any], assignment: dict[str, Any], teacher_proof: dict[str, Any],
    compile_results: dict[str, dict[str, Any]], witness_results: dict[str, dict[str, Any]],
    runtime_path: Path, config_path: Path, retry_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = load_preflight_config(config_path)
    _validate_candidate_assignment(candidate, assignment)
    teacher_proof = validate_teacher_proof_v4(candidate, assignment, teacher_proof)
    lane = candidate.get("lane")
    task = candidate["verification_task"]
    runtime = load_runtime(runtime_path, task["runtime_id"], lane, task["candidate_path"])
    lane_config = config["lanes"][lane]
    witness = teacher_proof["known_bad_cross_witness"]
    witness = validate_witness(witness, lane_config, config["success_marker"])
    support = _support_files(candidate)
    witness_files = [*support, {"path": witness["path"], "sha256": witness["content_sha256"]}]
    _exact(compile_results, {"reference", "known_bad"}, "compile results")
    _exact(witness_results, {"reference", "known_bad"}, "witness results")
    compile_commands = lane_config["compile_commands"]
    witness_commands = lane_config["witness_commands"]
    if retry_ledger is None:
        rows = []
        for phase, commands, files, source in (
            ("compile_syntax", compile_commands, support, compile_results),
            ("known_bad_cross_witness", witness_commands, witness_files, witness_results),
        ):
            for implementation in ("reference", "known_bad"):
                rows.append({
                    "phase": phase, "implementation": implementation,
                    "input_binding": _attempt_input_binding(
                        candidate, phase, implementation, commands, files,
                        runtime_path, runtime,
                    ),
                    "attempts": [{
                        "attempt": 1, "classification": None,
                        "result": copy.deepcopy(source[implementation]),
                    }],
                })
        retry_ledger = _retry_ledger(candidate, rows, "passed")
    validate_preflight_retry_ledger(retry_ledger, candidate, "passed")
    evidence: dict[str, Any] = {
        "schema_version": EVIDENCE_SCHEMA,
        "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256,
        "candidate_id": candidate["id"],
        "candidate_sha256": canonical_sha256(candidate),
        "assignment_sha256": canonical_sha256(assignment),
        "teacher_proof_evidence_sha256": teacher_proof["evidence_sha256"],
        "preflight_config_sha256": config["config_sha256"],
        "runtime_binding": _runtime_binding(candidate, runtime_path, runtime),
        "retry_ledger": copy.deepcopy(retry_ledger),
        "compile": {
            implementation: _bind_result(
                candidate, "compile_syntax", implementation, compile_commands, support,
                compile_results[implementation],
            )
            for implementation in ("reference", "known_bad")
        },
        "known_bad_cross_witness": {
            "witness": copy.deepcopy(witness),
            "witness_sha256": canonical_sha256(witness),
            "results": {
                implementation: _bind_result(
                    candidate, "known_bad_cross_witness", implementation,
                    witness_commands, witness_files, witness_results[implementation],
                )
                for implementation in ("reference", "known_bad")
            },
        },
        "visibility": dict(VISIBILITY),
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return validate_post_teacher_preflight_evidence(
        candidate, assignment, teacher_proof, evidence, runtime_path, config_path,
    )


def execute_post_teacher_preflight(
    candidate: dict[str, Any], assignment: dict[str, Any], teacher_proof: dict[str, Any],
    runtime_path: Path, config_path: Path,
    executor: CommandExecutor = verify_commands,
) -> dict[str, Any]:
    """Execute and seal the mandatory V4 compile and cross-witness preflight.

    The witness is staged only for its isolated phase and the resulting
    evidence is never passed to semantic review or independent test authorship.
    """
    config = load_preflight_config(config_path)
    _validate_candidate_assignment(candidate, assignment)
    proof = validate_teacher_proof_v4(candidate, assignment, teacher_proof)
    lane_config = config["lanes"][candidate["lane"]]
    witness = validate_witness(
        proof["known_bad_cross_witness"], lane_config, config["success_marker"],
    )
    base_task = copy.deepcopy(candidate["verification_task"])
    base_task["surface"] = "synthetic_harness"
    support = copy.deepcopy(base_task["files"])
    witness_file = {
        "path": witness["path"], "role": "test",
        "content": witness["content"], "sha256": witness["content_sha256"],
    }
    validation = base_task["validation"]
    implementations = {
        "reference": validation["reference"]["code"],
        "known_bad": validation["known_bad"][0]["code"],
    }
    runtime = load_runtime(
        runtime_path, base_task["runtime_id"], candidate["lane"], base_task["candidate_path"],
    )
    compile_results: dict[str, dict[str, Any]] = {}
    witness_results: dict[str, dict[str, Any]] = {}
    retry_rows: list[dict[str, Any]] = []
    steps = (
        ("compile_syntax", lane_config["compile_commands"], support, compile_results, None),
        (
            "known_bad_cross_witness", lane_config["witness_commands"],
            [*support, witness_file], witness_results, config["success_marker"],
        ),
    )
    for phase, commands, files, destination, marker in steps:
        for implementation, code in implementations.items():
            task = copy.deepcopy(base_task)
            task["files"] = copy.deepcopy(files)
            attempts: list[dict[str, Any]] = []
            final_result: dict[str, Any] | None = None
            for attempt in (1, 2):
                result = executor(task, code, runtime_path, commands)
                classification = (
                    "timeout" if result.get("timed_out") is True
                    else infrastructure_failure(result)
                )
                attempts.append({
                    "attempt": attempt, "classification": classification,
                    "result": copy.deepcopy(result),
                })
                final_result = result
                if classification is None:
                    break
            row = {
                "phase": phase, "implementation": implementation,
                "input_binding": _attempt_input_binding(
                    candidate, phase, implementation, commands,
                    [{"path": item["path"], "sha256": item["sha256"]} for item in files],
                    runtime_path, runtime,
                ),
                "attempts": attempts,
            }
            retry_rows.append(row)
            if attempts[-1]["classification"] is not None:
                reason = f"{phase}.{implementation}: unresolved infrastructure after one identical replay"
                evidence = _terminal_outcome(
                    candidate, assignment, runtime_path, config, runtime, "unresolved",
                    phase, implementation, reason, retry_rows,
                )
                raise V4PreflightFailure(reason, evidence=evidence, status="unresolved")
            assert final_result is not None
            try:
                _validate_result(
                    final_result, commands, {**runtime, "runtime_id": base_task["runtime_id"]},
                    marker, f"{phase}.{implementation}",
                )
            except V4PreflightFailure as exc:
                evidence = _terminal_outcome(
                    candidate, assignment, runtime_path, config, runtime,
                    "terminal-rejected", phase, implementation, str(exc), retry_rows,
                )
                raise V4PreflightFailure(str(exc), evidence=evidence) from exc
            destination[implementation] = final_result
    retry_ledger = _retry_ledger(candidate, retry_rows, "passed")
    return build_post_teacher_preflight_evidence(
        candidate, assignment, proof, compile_results, witness_results,
        runtime_path, config_path, retry_ledger,
    )


def _validate_result(
    value: Any, expected_commands: list[list[str]], runtime: dict[str, Any],
    marker: str | None, where: str,
) -> None:
    result = _exact(value, RESULT_KEYS, where)
    if (
        result["runtime_id"] != runtime["runtime_id"]
        or result["image"] != f"{runtime['image'].rsplit(':', 1)[0]}@{runtime['manifest_digest']}"
        or result["image_id"] != runtime["image_id"]
        or result["commands"] != expected_commands
        or result["exit_codes"] != [0] * len(expected_commands)
        or result["timed_out"] is not False
        or result["sandbox_contract_sha256"] != sha256_object(SANDBOX_CONTRACT)
        or not isinstance(result["stdout"], str)
        or result["stdout_sha256"] != sha256_text(result["stdout"])
        or not isinstance(result["stderr"], str)
        or result["stderr_sha256"] != sha256_text(result["stderr"])
        or type(result["duration_ms"]) is not int or result["duration_ms"] < 0
        or infrastructure_failure(result) is not None
        or marker is not None and result["stdout"].count(marker) != 1
    ):
        raise V4PreflightFailure(f"{where}: execution did not pass the frozen contract")


def validate_post_teacher_preflight_evidence(
    candidate: dict[str, Any], assignment: dict[str, Any], teacher_proof: dict[str, Any], evidence: Any,
    runtime_path: Path, config_path: Path,
) -> dict[str, Any]:
    config = load_preflight_config(config_path)
    _validate_candidate_assignment(candidate, assignment)
    teacher_proof = validate_teacher_proof_v4(candidate, assignment, teacher_proof)
    value = _exact(
        evidence,
        {
            "schema_version", "contract_id", "plan_sha256", "candidate_id",
            "candidate_sha256", "assignment_sha256", "teacher_proof_evidence_sha256",
            "preflight_config_sha256",
            "runtime_binding", "compile", "known_bad_cross_witness", "visibility",
            "retry_ledger", "evidence_sha256",
        },
        "post-teacher preflight evidence",
    )
    body = dict(value)
    claimed = body.pop("evidence_sha256")
    if (
        value["schema_version"] != EVIDENCE_SCHEMA
        or value["contract_id"] != CONTRACT_ID
        or value["plan_sha256"] != PLAN_SHA256
        or assignment.get("contract_id") != CONTRACT_ID
        or value["candidate_id"] != candidate.get("id")
        or value["candidate_sha256"] != canonical_sha256(candidate)
        or value["assignment_sha256"] != canonical_sha256(assignment)
        or value["teacher_proof_evidence_sha256"] != teacher_proof["evidence_sha256"]
        or value["preflight_config_sha256"] != config["config_sha256"]
        or value["visibility"] != VISIBILITY
        or claimed != canonical_sha256(body)
    ):
        raise V4PreflightFailure("post-teacher preflight identity, visibility, or seal mismatch")
    lane = candidate["lane"]
    task = candidate["verification_task"]
    runtime_raw = load_runtime(runtime_path, task["runtime_id"], lane, task["candidate_path"])
    runtime = {**runtime_raw, "runtime_id": task["runtime_id"]}
    if value["runtime_binding"] != _runtime_binding(candidate, runtime_path, runtime_raw):
        raise V4PreflightFailure("runtime binding differs from the pinned admission runtime")
    validate_preflight_retry_ledger(value["retry_ledger"], candidate, "passed")
    support = _support_files(candidate)
    lane_config = config["lanes"][lane]
    compile_commands = lane_config["compile_commands"]
    compile_evidence = _exact(value["compile"], {"reference", "known_bad"}, "compile evidence")
    witness_evidence = _exact(
        value["known_bad_cross_witness"], {"witness", "witness_sha256", "results"},
        "known_bad_cross_witness evidence",
    )
    witness = validate_witness(
        witness_evidence["witness"], lane_config, config["success_marker"],
    )
    if (
        witness != teacher_proof["known_bad_cross_witness"]
        or witness_evidence["witness_sha256"] != canonical_sha256(witness)
    ):
        raise V4PreflightFailure("known_bad_cross_witness seal mismatch")
    witness_files = [*support, {"path": witness["path"], "sha256": witness["content_sha256"]}]
    results = _exact(witness_evidence["results"], {"reference", "known_bad"}, "witness results")
    retry_rows = {
        (row["phase"], row["implementation"]): row
        for row in value["retry_ledger"]["executions"]
    }
    if len(retry_rows) != 4:
        raise V4PreflightFailure("preflight retry ledger does not cover all four executions")
    for implementation in ("reference", "known_bad"):
        for phase, binding, commands, files, marker in (
            ("compile_syntax", compile_evidence[implementation], compile_commands, support, None),
            (
                "known_bad_cross_witness", results[implementation],
                lane_config["witness_commands"], witness_files, config["success_marker"],
            ),
        ):
            bound = _exact(
                binding, {"implementation_sha256", "execution_sha256", "result"},
                f"{phase}.{implementation}",
            )
            if (
                bound["implementation_sha256"] != _implementation_sha(candidate, implementation)
                or bound["execution_sha256"] != _execution_sha256(
                    candidate, phase, implementation, commands, files,
                )
            ):
                raise V4PreflightFailure(f"{phase}.{implementation}: input binding mismatch")
            _validate_result(
                bound["result"], commands, runtime, marker,
                f"{phase}.{implementation}",
            )
            retry_row = retry_rows.get((phase, implementation))
            if (
                retry_row is None
                or retry_row["input_binding"] != _attempt_input_binding(
                    candidate, phase, implementation, commands, files,
                    runtime_path, runtime_raw,
                )
                or retry_row["attempts"][-1]["result"] != bound["result"]
                or retry_row["attempts"][-1]["classification"] is not None
            ):
                raise V4PreflightFailure(f"{phase}.{implementation}: retry binding mismatch")
    return value
