#!/usr/bin/env python3
"""V5 witness/runtime interface preflight for immutable V4 teacher artifacts.

This module is deliberately separate from the sealed V4 preflight.  It adds
the prospectively frozen V5 execution modes without reinterpreting V4 results.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Callable

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v4_preflight import (
    PROOF_SCHEMA as V4_PROOF_SCHEMA,
    validate_teacher_proof_v4, validate_witness,
)
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import (
    SANDBOX_CONTRACT, infrastructure_failure, load_runtime, verify_commands,
)


PLAN_SHA256 = "132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b"
CONTRACT_ID = "capability-stratified-v5-interface-replay/v1"
V4_CONTRACT_ID = "capability-stratified-v4-repair-delta/v1"
CONFIG_SCHEMA = "ganesh-mini-repair-delta-v5-interface-preflight-config/v1"
EVIDENCE_SCHEMA = "ganesh-mini-repair-delta-v5-interface-preflight/v1"
RETRY_SCHEMA = "ganesh-mini-repair-delta-v5-interface-retry-ledger/v1"
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
JAVA_CWD_INFRASTRUCTURE_SIGNATURE = (
    "Properties init: Could not determine current working directory"
)
GO_ATTEMPT_CONTRACT = {
    "candidate_concurrency": 1,
    "preflight_attempt_timeout_seconds": 120,
    "final_suite_attempt_timeout_seconds": 120,
    "final_suites_sequential": True,
    "final_matrix_seconds_without_replay": 480,
    "final_matrix_seconds_with_four_replays": 960,
    "aggregate_candidate_timeout_seconds": None,
}

CommandExecutor = Callable[[dict[str, Any], str, Path, list[list[str]]], dict[str, Any]]


class V5PreflightFailure(ValueError):
    def __init__(self, message: str, *, status: str = "terminal-rejected", evidence: Any = None) -> None:
        super().__init__(message)
        self.status = status
        self.evidence = evidence


def _exact(value: Any, keys: set[str], where: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise V5PreflightFailure(f"{where}: keys differ from V5 contract")
    return value


def load_v5_preflight_config(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _exact(value, {
        "schema_version", "contract_id", "plan_sha256", "success_marker",
        "go_attempt_contract", "lanes", "config_sha256",
    }, "V5 preflight config")
    body = dict(value); claimed = body.pop("config_sha256")
    if (
        value["schema_version"] != CONFIG_SCHEMA
        or value["contract_id"] != CONTRACT_ID
        or value["plan_sha256"] != PLAN_SHA256
        or claimed != canonical_sha256(body)
        or value["go_attempt_contract"] != GO_ATTEMPT_CONTRACT
        or set(value["lanes"]) != set(LANES)
        or not isinstance(value["success_marker"], str)
        or not value["success_marker"]
    ):
        raise V5PreflightFailure("V5 preflight config identity or seal mismatch")
    expected_modes = {
        "javascript": "dual-immutable-artifact",
        "rust": "binary-main-per-implementation",
    }
    for lane, raw in value["lanes"].items():
        required = {"witness_mode", "compile_commands", "witness_path", "witness_commands"}
        if lane == "javascript":
            required |= {"reference_path", "known_bad_path"}
        item = _exact(raw, required, f"V5 lane {lane}")
        if item["witness_mode"] != expected_modes.get(lane, "single-implementation"):
            raise V5PreflightFailure(f"V5 lane {lane}: witness mode mismatch")
        for name in ("compile_commands", "witness_commands"):
            commands = item[name]
            if not isinstance(commands, list) or not commands or any(
                not isinstance(command, list) or not command
                or any(not isinstance(part, str) or not part for part in command)
                for command in commands
            ):
                raise V5PreflightFailure(f"V5 lane {lane}: invalid {name}")
        for name in required & {"witness_path", "reference_path", "known_bad_path"}:
            path_value = PurePosixPath(item[name])
            if not item[name] or path_value.is_absolute() or ".." in path_value.parts:
                raise V5PreflightFailure(f"V5 lane {lane}: unsafe {name}")
    js = value["lanes"]["javascript"]
    if js["reference_path"] != "reference.js" or js["known_bad_path"] != "known_bad.js":
        raise V5PreflightFailure("V5 JavaScript dual-artifact paths drifted")
    rust_commands = value["lanes"]["rust"]["witness_commands"]
    if "--test" in {part for command in rust_commands for part in command}:
        raise V5PreflightFailure("V5 Rust binary witness must not use rustc --test")
    return value


def classify_v5_infrastructure(result: dict[str, Any], lane: str) -> str | None:
    if result.get("timed_out") is True:
        return "timeout"
    if lane == "java" and JAVA_CWD_INFRASTRUCTURE_SIGNATURE in (
        str(result.get("stdout", "")) + "\n" + str(result.get("stderr", ""))
    ):
        return "java-cwd-infrastructure"
    return infrastructure_failure(result)


def _validate_inputs(
    candidate: dict[str, Any], assignment: dict[str, Any], proof: dict[str, Any],
    v4_config_path: Path,
) -> dict[str, Any]:
    lane = candidate.get("lane")
    task = candidate.get("verification_task")
    if (
        lane not in LANES or not isinstance(task, dict)
        or task.get("language") != lane
        or assignment.get("contract_id") != CONTRACT_ID
        or assignment.get("id") != candidate.get("id")
        or assignment.get("cell_id")
        != f"{assignment.get('primary_capability')}/{lane}/repair"
        or proof.get("schema_version") != V4_PROOF_SCHEMA
    ):
        raise V5PreflightFailure("candidate, V5 assignment, and carried proof do not bind")
    files = task.get("files")
    if not isinstance(files, list) or any(item.get("role") != "support" for item in files):
        raise V5PreflightFailure("V5 preflight requires a pre-test candidate")
    if lane == "go" and task.get("limits", {}).get("timeout_seconds") != 120:
        raise V5PreflightFailure("V5 Go preflight attempt limit must be 120 seconds")
    v4_assignment = copy.deepcopy(assignment)
    v4_assignment["contract_id"] = V4_CONTRACT_ID
    del v4_config_path  # V4 proof identity is independent of its execution config.
    return validate_teacher_proof_v4(candidate, v4_assignment, proof)


def _runtime_binding(candidate: dict[str, Any], runtime_path: Path) -> dict[str, Any]:
    task = candidate["verification_task"]
    runtime = load_runtime(runtime_path, task["runtime_id"], candidate["lane"], task["candidate_path"])
    return {
        "runtime_config_sha256": hashlib.sha256(runtime_path.read_bytes()).hexdigest(),
        "runtime_id": task["runtime_id"], "image": runtime["image"],
        "image_id": runtime["image_id"], "manifest_digest": runtime["manifest_digest"],
        "candidate_path": task["candidate_path"], "platform": runtime["platform"],
    }


def _result_passed(
    result: dict[str, Any], commands: list[list[str]], marker: str | None, lane: str,
) -> bool:
    if (
        result.get("commands") != commands or result.get("timed_out") is not False
        or result.get("exit_codes") != [0] * len(commands)
        or result.get("sandbox_contract_sha256") != sha256_object(SANDBOX_CONTRACT)
        or result.get("stdout_sha256") != sha256_text(str(result.get("stdout", "")))
        or result.get("stderr_sha256") != sha256_text(str(result.get("stderr", "")))
        or classify_v5_infrastructure(result, lane) is not None
    ):
        return False
    return marker is None or str(result.get("stdout", "")).splitlines().count(marker) == 1


def _run(
    executor: CommandExecutor, task: dict[str, Any], code: str, runtime_path: Path,
    commands: list[list[str]], lane: str, phase: str, implementation: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    input_binding = {
        "phase": phase, "implementation": implementation,
        "task_sha256": canonical_sha256(task), "code_sha256": sha256_text(code),
        "commands": copy.deepcopy(commands),
        "attempt_timeout_seconds": task["limits"]["timeout_seconds"],
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
    }
    input_binding["binding_sha256"] = canonical_sha256(input_binding)
    attempts = []
    result: dict[str, Any] = {}
    for ordinal in (1, 2):
        result = executor(copy.deepcopy(task), code, runtime_path, copy.deepcopy(commands))
        classification = classify_v5_infrastructure(result, lane)
        attempts.append({
            "attempt": ordinal, "classification": classification,
            "input_binding": copy.deepcopy(input_binding), "result": copy.deepcopy(result),
        })
        if classification is None:
            break
    return result, {
        "phase": phase, "implementation": implementation,
        "input_binding": input_binding, "attempts": attempts,
    }


def execute_v5_interface_preflight(
    candidate: dict[str, Any], assignment: dict[str, Any], proof: dict[str, Any],
    runtime_path: Path, config_path: Path, v4_config_path: Path,
    executor: CommandExecutor = verify_commands,
) -> dict[str, Any]:
    config = load_v5_preflight_config(config_path)
    proof = _validate_inputs(candidate, assignment, proof, v4_config_path)
    lane = candidate["lane"]
    task = copy.deepcopy(candidate["verification_task"])
    task["surface"] = "synthetic_harness"
    lane_config = config["lanes"][lane]
    witness = proof["known_bad_cross_witness"]
    validate_witness(witness, lane_config, config["success_marker"])
    validation = task["validation"]
    implementations = {
        "reference": validation["reference"]["code"],
        "known_bad": validation["known_bad"][0]["code"],
    }
    rows: list[dict[str, Any]] = []
    compile_results: dict[str, Any] = {}
    for implementation, code in implementations.items():
        compile_task = copy.deepcopy(task)
        result, row = _run(
            executor, compile_task, code, runtime_path,
            lane_config["compile_commands"], lane, "compile_syntax", implementation,
        )
        rows.append(row)
        if row["attempts"][-1]["classification"] is not None:
            raise V5PreflightFailure(
                f"compile_syntax.{implementation}: unresolved infrastructure after one identical replay",
                status="unresolved", evidence={"retry_rows": rows},
            )
        if not _result_passed(result, lane_config["compile_commands"], None, lane):
            raise V5PreflightFailure(f"compile_syntax.{implementation}: execution did not pass")
        compile_results[implementation] = result

    marker = config["success_marker"]
    witness_results: dict[str, Any] = {}
    if lane_config["witness_mode"] == "dual-immutable-artifact":
        witness_task = copy.deepcopy(task)
        witness_task["files"] = [
            *copy.deepcopy(task["files"]),
            {"path": lane_config["reference_path"], "role": "support",
             "content": implementations["reference"],
             "sha256": sha256_text(implementations["reference"])},
            {"path": lane_config["known_bad_path"], "role": "support",
             "content": implementations["known_bad"],
             "sha256": sha256_text(implementations["known_bad"])},
            {"path": witness["path"], "role": "test", "content": witness["content"],
             "sha256": witness["content_sha256"]},
        ]
        result, row = _run(
            executor, witness_task, implementations["reference"], runtime_path,
            lane_config["witness_commands"], lane, "known_bad_cross_witness", "reference+known_bad",
        )
        rows.append(row)
        if row["attempts"][-1]["classification"] is not None:
            raise V5PreflightFailure(
                "known_bad_cross_witness.reference+known_bad: unresolved infrastructure after one identical replay",
                status="unresolved", evidence={"retry_rows": rows},
            )
        if not _result_passed(result, lane_config["witness_commands"], marker, lane):
            raise V5PreflightFailure("known_bad_cross_witness.reference+known_bad: execution did not pass")
        witness_results["reference+known_bad"] = result
    else:
        for implementation, code in implementations.items():
            witness_task = copy.deepcopy(task)
            witness_task["files"] = [
                *copy.deepcopy(task["files"]),
                {"path": witness["path"], "role": "test", "content": witness["content"],
                 "sha256": witness["content_sha256"]},
            ]
            result, row = _run(
                executor, witness_task, code, runtime_path,
                lane_config["witness_commands"], lane,
                "known_bad_cross_witness", implementation,
            )
            rows.append(row)
            if row["attempts"][-1]["classification"] is not None:
                raise V5PreflightFailure(
                    f"known_bad_cross_witness.{implementation}: unresolved infrastructure after one identical replay",
                    status="unresolved", evidence={"retry_rows": rows},
                )
            if not _result_passed(result, lane_config["witness_commands"], marker, lane):
                raise V5PreflightFailure(
                    f"known_bad_cross_witness.{implementation}: execution did not pass",
                )
            witness_results[implementation] = result

    retry_ledger = {
        "schema_version": RETRY_SCHEMA, "candidate_sha256": canonical_sha256(candidate),
        "maximum_attempts": 2, "executions": rows, "unresolved": False,
        "evaluation_artifacts_read": 0,
    }
    retry_ledger["ledger_sha256"] = canonical_sha256(retry_ledger)
    evidence = {
        "schema_version": EVIDENCE_SCHEMA, "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256, "candidate_id": candidate["id"],
        "candidate_sha256": canonical_sha256(candidate),
        "assignment_sha256": canonical_sha256(assignment),
        "teacher_proof_evidence_sha256": proof["evidence_sha256"],
        "preflight_config_sha256": config["config_sha256"],
        "runtime_binding": _runtime_binding(candidate, runtime_path),
        "witness_mode": lane_config["witness_mode"],
        "attempt_contract": copy.deepcopy(
            GO_ATTEMPT_CONTRACT if lane == "go" else {
                "attempt_timeout_seconds": task["limits"]["timeout_seconds"],
                "maximum_attempts": 2,
            }
        ),
        "compile": compile_results, "witness": copy.deepcopy(witness),
        "witness_results": witness_results, "retry_ledger": retry_ledger,
        "evaluation_artifacts_read": 0,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return validate_v5_interface_preflight_evidence(evidence, candidate, assignment, config_path)


def validate_v5_interface_preflight_evidence(
    evidence: Any, candidate: dict[str, Any], assignment: dict[str, Any], config_path: Path,
) -> dict[str, Any]:
    config = load_v5_preflight_config(config_path)
    value = _exact(evidence, {
        "schema_version", "contract_id", "plan_sha256", "candidate_id",
        "candidate_sha256", "assignment_sha256", "teacher_proof_evidence_sha256",
        "preflight_config_sha256", "runtime_binding", "witness_mode",
        "attempt_contract", "compile", "witness", "witness_results",
        "retry_ledger", "evaluation_artifacts_read", "evidence_sha256",
    }, "V5 preflight evidence")
    body = dict(value); claimed = body.pop("evidence_sha256")
    lane = candidate["lane"]
    if (
        claimed != canonical_sha256(body)
        or value["schema_version"] != EVIDENCE_SCHEMA
        or value["contract_id"] != CONTRACT_ID or value["plan_sha256"] != PLAN_SHA256
        or value["candidate_id"] != candidate["id"]
        or value["candidate_sha256"] != canonical_sha256(candidate)
        or value["assignment_sha256"] != canonical_sha256(assignment)
        or value["preflight_config_sha256"] != config["config_sha256"]
        or value["witness_mode"] != config["lanes"][lane]["witness_mode"]
        or value["evaluation_artifacts_read"] != 0
        or value["attempt_contract"] != (
            GO_ATTEMPT_CONTRACT if lane == "go" else {
                "attempt_timeout_seconds": candidate["verification_task"]["limits"]["timeout_seconds"],
                "maximum_attempts": 2,
            }
        )
    ):
        raise V5PreflightFailure("V5 preflight evidence identity or seal mismatch")
    rows = value["retry_ledger"].get("executions")
    if not isinstance(rows, list) or len(rows) != (3 if lane == "javascript" else 4):
        raise V5PreflightFailure("V5 retry ledger execution coverage mismatch")
    for row in rows:
        attempts = row.get("attempts")
        if not isinstance(attempts, list) or not 1 <= len(attempts) <= 2:
            raise V5PreflightFailure("V5 retry ledger attempt coverage mismatch")
        if attempts[0]["classification"] is None and len(attempts) != 1:
            raise V5PreflightFailure("V5 replay occurred without infrastructure failure")
        if attempts[0]["classification"] is not None and len(attempts) != 2:
            raise V5PreflightFailure("V5 infrastructure failure lacks one replay")
        if any(attempt["input_binding"] != row["input_binding"] for attempt in attempts):
            raise V5PreflightFailure("V5 infrastructure replay was not byte-identical")
    return value
