#!/usr/bin/env python3
"""Produce and assemble isolated v3 repair-delta qualification evidence.

The orchestration core accepts stage callables so tests never invoke an LLM or
sandbox.  Production adapters may use ``invoke_codex`` and ``verify``; every
stage receives only its frozen visibility projection.  Per-candidate artifacts
are sealed and safely resumable only when their complete input binding matches.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_repair_delta import (  # noqa: E402
    CONTRACT_ID, ENVELOPE_SCHEMA, PROOF_BOOLEAN_OVERLAP, SEMANTIC_BOOLEANS,
    suite_sha256, teacher_candidate_sha256,
)
from scripts.data.admit_expansion import canonical_json  # noqa: E402
from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.data.build_capability_corpus_plan import load_sealed  # noqa: E402
from scripts.data.build_repair_delta_queue import PLAN_SHA256  # noqa: E402
from scripts.data.generate_expansion_qualification import (  # noqa: E402
    invoke_codex, verify_codex_version,
)
from scripts.data.generate_repair_delta_candidates import load_reserve_eligibility  # noqa: E402
from scripts.eval.contracts import sha256_object, sha256_text  # noqa: E402
from scripts.verify.sandbox import SANDBOX_CONTRACT, infrastructure_failure, verify  # noqa: E402


ARTIFACT_SCHEMA = "ganesh-mini-repair-delta-evidence-assembly/v1"
StageFn = Callable[[dict[str, Any]], dict[str, Any]]
SeparationFn = Callable[[dict[str, Any]], dict[str, Any]]
VerifierFn = Callable[[dict[str, Any], str, Path], dict[str, Any]]


def seal(value: dict[str, Any]) -> dict[str, Any]:
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def semantic_projection(candidate: dict[str, Any], assignment: dict[str, Any]) -> dict[str, Any]:
    validation = candidate["verification_task"]["validation"]
    return {
        "id": candidate["id"], "specification": candidate["messages"][0]["content"],
        "lane": candidate["lane"],
        "embedded_known_bad": validation["known_bad"][0]["code"],
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
    }


def test_author_projection(candidate: dict[str, Any], assignment: dict[str, Any]) -> dict[str, Any]:
    value = semantic_projection(candidate, assignment)
    value["primary_capability_definition"] = assignment["primary_capability_definition"]
    return value


def delta_projection(candidate: dict[str, Any], assignment: dict[str, Any]) -> dict[str, Any]:
    value = semantic_projection(candidate, assignment)
    value["reference"] = candidate["verification_task"]["validation"]["reference"]["code"]
    return value


def _semantic_evidence(
    candidate: dict[str, Any], assignment: dict[str, Any], response: dict[str, Any], run_sha256: str,
) -> dict[str, Any]:
    if set(response) != {*SEMANTIC_BOOLEANS, "rationale"} or any(
        type(response.get(field)) is not bool for field in SEMANTIC_BOOLEANS
    ) or not isinstance(response.get("rationale"), str) or not response["rationale"].strip():
        raise ValueError("semantic reviewer response differs from the frozen boolean contract")
    candidate_sha = canonical_sha256(candidate)
    return seal({
        "candidate_sha256": candidate_sha,
        "specification_sha256": sha256_text(candidate["messages"][0]["content"]),
        "known_bad_sha256": candidate["verification_task"]["validation"]["known_bad"][0]["sha256"],
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        **response, "reviewer_run_evidence_sha256": run_sha256,
        "visibility": {
            "specification_visible": True, "embedded_known_bad_visible": True,
            "assigned_labels_visible": True, "teacher_proof_visible": False,
            "reference_visible": False, "tests_visible": False, "verifier_outputs_visible": False,
            "training_stimulus_visible": False, "source_dataset_visible": False,
            "v2_outcomes_visible": False, "evaluation_artifacts_read": 0,
        },
    })


def _add_tests(
    candidate: dict[str, Any], assignment: dict[str, Any], response: dict[str, Any], run_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = response.get("files")
    if not isinstance(rows, list) or not rows:
        raise ValueError("test author returned no split test files")
    updated = copy.deepcopy(candidate)
    support = [item for item in updated["verification_task"]["files"] if item.get("role") == "support"]
    files: list[dict[str, Any]] = []
    roles: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "content", "role", "case_ids"}:
            raise ValueError("test-author file differs from the frozen split-role contract")
        if row["role"] not in {"primary_discrimination", "cross_cutting"}:
            raise ValueError("test-author emitted an unknown logical role")
        content = row["content"].rstrip() + "\n"
        digest = sha256_text(content)
        files.append({"path": row["path"], "role": "test", "content": content, "sha256": digest})
        roles.append({
            "path": row["path"], "file_sha256": digest, "role": row["role"],
            "case_ids": row["case_ids"],
            "valid_domain_only": row["role"] == "primary_discrimination",
            "scheduled_dimension_only": row["role"] == "cross_cutting",
        })
    updated["verification_task"]["files"] = [*support, *files]
    candidate_sha = canonical_sha256(updated)
    evidence = seal({
        "candidate_sha256": candidate_sha,
        "specification_sha256": sha256_text(updated["messages"][0]["content"]),
        "known_bad_sha256": updated["verification_task"]["validation"]["known_bad"][0]["sha256"],
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        "test_roles": roles, "test_author_run_evidence_sha256": run_sha256,
        "visibility": {
            "specification_visible": True, "embedded_known_bad_visible": True,
            "capability_definition_visible": True, "scheduled_dimension_visible": True,
            "reference_visible": False, "teacher_proof_visible": False,
            "semantic_review_visible": False, "verifier_outputs_visible": False,
            "evaluation_artifacts_read": 0,
        },
    })
    return updated, evidence


def _rebind_semantic(semantic: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Carry blind findings across the test-only mutation without exposing tests."""
    rebound = dict(semantic)
    rebound.pop("evidence_sha256")
    rebound["candidate_sha256"] = canonical_sha256(candidate)
    rebound["pre_test_semantic_evidence_sha256"] = semantic["evidence_sha256"]
    return seal(rebound)


def _delta_evidence(
    candidate: dict[str, Any], assignment: dict[str, Any], response: dict[str, Any], run_sha256: str,
) -> dict[str, Any]:
    expected = {"independent_semantic_delta_count", "delta_is_capability_specific", "introduces_multiple_independent_fixes", "delta_description"}
    if set(response) != expected:
        raise ValueError("delta-auditor response differs from the frozen contract")
    validation = candidate["verification_task"]["validation"]
    return seal({
        "candidate_sha256": canonical_sha256(candidate),
        "specification_sha256": sha256_text(candidate["messages"][0]["content"]),
        "reference_sha256": validation["reference"]["sha256"],
        "known_bad_sha256": validation["known_bad"][0]["sha256"],
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        **response, "delta_auditor_run_evidence_sha256": run_sha256,
        "visibility": {
            "specification_visible": True, "embedded_known_bad_visible": True,
            "reference_visible": True, "assigned_labels_visible": True,
            "tests_visible": False, "verifier_outputs_visible": False,
            "teacher_proof_visible": False, "training_stimulus_visible": False,
            "v2_outcomes_visible": False, "evaluation_artifacts_read": 0,
        },
    })


def _run_with_one_replay(
    verifier: VerifierFn, task: dict[str, Any], code: str, runtime_path: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], bool]:
    attempts: list[dict[str, Any]] = []
    for attempt in (1, 2):
        result = verifier(task, code, runtime_path)
        classification = "timeout" if result.get("timed_out") is True else infrastructure_failure(result)
        attempts.append({"attempt": attempt, "classification": classification, "result": result})
        if classification is None:
            return result, attempts, False
    return attempts[-1]["result"], attempts, True


def _executable_evidence(
    candidate: dict[str, Any], test_evidence: dict[str, Any], runtime_path: Path,
    verifier: VerifierFn,
) -> tuple[dict[str, Any], dict[str, Any]]:
    task = candidate["verification_task"]
    runtime_document = json.loads(runtime_path.read_text(encoding="utf-8"))
    runtime = runtime_document["runtimes"][task["runtime_id"]]
    roles = test_evidence["test_roles"]
    retry_rows: list[dict[str, Any]] = []
    results: dict[str, dict[str, Any]] = {"reference": {}, "known_bad": {}}
    unresolved = False
    implementations = {
        "reference": task["validation"]["reference"]["code"],
        "known_bad": task["validation"]["known_bad"][0]["code"],
    }
    for role in ("primary_discrimination", "cross_cutting"):
        role_rows = [row for row in roles if row["role"] == role]
        role_paths = {row["path"] for row in role_rows}
        suite_task = copy.deepcopy(task)
        suite_task["surface"] = "synthetic_harness"
        suite_task["files"] = [
            item for item in task["files"] if item.get("role") == "support" or item["path"] in role_paths
        ]
        for implementation, code in implementations.items():
            result, attempts, failed = _run_with_one_replay(verifier, suite_task, code, runtime_path)
            retry_rows.append({"implementation": implementation, "role": role, "attempts": attempts})
            unresolved = unresolved or failed
            results[implementation][role] = {
                **result, "suite_sha256": suite_sha256(candidate, role_rows),
                "manifest_digest": runtime["manifest_digest"],
                "limits_sha256": canonical_sha256(task["limits"]),
            }
    retry_ledger = {
        "schema_version": "ganesh-mini-repair-delta-retry-ledger/v1",
        "candidate_sha256": canonical_sha256(candidate), "maximum_attempts": 2,
        "attempts": retry_rows, "unresolved": unresolved, "evaluation_artifacts_read": 0,
    }
    retry_ledger["ledger_sha256"] = canonical_sha256(retry_ledger)
    executable = seal({
        "candidate_sha256": canonical_sha256(candidate),
        "runtime_config_sha256": hashlib.sha256(runtime_path.read_bytes()).hexdigest(),
        "reference_sha256": task["validation"]["reference"]["sha256"],
        "known_bad_sha256": task["validation"]["known_bad"][0]["sha256"],
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        "retry_ledger_sha256": retry_ledger["ledger_sha256"], "results": results,
    })
    return executable, retry_ledger


def _terminal(
    candidate: dict[str, Any], assignment: dict[str, Any], stage: str, reason: str,
    evidence: dict[str, Any], input_sha256: str,
) -> dict[str, Any]:
    value = {
        "schema_version": ARTIFACT_SCHEMA, "status": "terminal-rejected",
        "input_sha256": input_sha256, "candidate_id": candidate["id"],
        "cell_id": assignment["cell_id"], "terminal_stage": stage, "reason": reason,
        "evidence": evidence, "evaluation_artifacts_read": 0,
    }
    value["artifact_sha256"] = canonical_sha256(value)
    return value


def produce_candidate(
    generated: dict[str, Any], assignment: dict[str, Any], runtime_path: Path,
    semantic_fn: StageFn, test_fn: StageFn, delta_fn: StageFn,
    separation_fn: SeparationFn, verifier_fn: VerifierFn = verify,
) -> dict[str, Any]:
    candidate = copy.deepcopy(generated["candidate"])
    proof = copy.deepcopy(generated["repair_delta_proof"])
    input_sha = canonical_sha256({"generated": generated, "assignment": assignment})
    proof_body = dict(proof); proof_claimed = proof_body.pop("evidence_sha256", None)
    if (
        proof_claimed != canonical_sha256(proof_body)
        or proof.get("candidate_id") != candidate.get("id")
        or proof.get("teacher_candidate_sha256") != teacher_candidate_sha256(candidate)
        or assignment.get("id") != candidate.get("id")
        or assignment.get("contract_id") != CONTRACT_ID
    ):
        raise ValueError("teacher proof, pre-test candidate, and sealed assignment do not bind")

    semantic_response = semantic_fn(semantic_projection(candidate, assignment))
    semantic_run = semantic_response.pop("_run_sha256")
    semantic = _semantic_evidence(candidate, assignment, semantic_response, semantic_run)
    if any(semantic[field] is not True for field in SEMANTIC_BOOLEANS):
        return _terminal(candidate, assignment, "semantic_review", "blind semantic boolean failed", {"teacher_proof": proof, "semantic_review": semantic}, input_sha)
    if any(semantic[field] is not proof[field] for field in PROOF_BOOLEAN_OVERLAP):
        return _terminal(candidate, assignment, "proof_consistency", "teacher proof disagrees with blind review", {"teacher_proof": proof, "semantic_review": semantic}, input_sha)

    test_response = test_fn(test_author_projection(candidate, assignment))
    test_run = test_response.pop("_run_sha256")
    candidate, test_evidence = _add_tests(candidate, assignment, test_response, test_run)
    semantic = _rebind_semantic(semantic, candidate)

    delta_response = delta_fn(delta_projection(candidate, assignment))
    delta_run = delta_response.pop("_run_sha256")
    delta = _delta_evidence(candidate, assignment, delta_response, delta_run)
    if (
        delta["independent_semantic_delta_count"] != 1
        or delta["delta_is_capability_specific"] is not True
        or delta["introduces_multiple_independent_fixes"] is not False
    ):
        return _terminal(candidate, assignment, "delta_audit", "delta auditor rejected the repair", {"teacher_proof": proof, "semantic_review": semantic, "test_author": test_evidence, "delta_audit": delta}, input_sha)

    separation = separation_fn(candidate)
    executable, retry_ledger = _executable_evidence(candidate, test_evidence, runtime_path, verifier_fn)
    if retry_ledger["unresolved"]:
        value = _terminal(candidate, assignment, "executable", "unresolved infrastructure after one identical replay", {
            "teacher_proof": proof, "semantic_review": semantic, "test_author": test_evidence,
            "delta_audit": delta, "separation": separation, "executable": executable,
            "retry_ledger": retry_ledger,
        }, input_sha)
        value["status"] = "unresolved"
        value.pop("artifact_sha256"); value["artifact_sha256"] = canonical_sha256(value)
        return value

    candidate_sha = canonical_sha256(candidate)
    lineage = seal({
        "candidate_sha256": candidate_sha, "contract_id": CONTRACT_ID,
        "cell_id": assignment["cell_id"],
        "source_identity": {key: candidate["source"].get(key) for key in ("dataset", "revision", "record_id")},
        "source_record_sha256": candidate["source"]["source_record_sha256"], "complete": True,
        "teacher_proof_evidence_sha256": proof["evidence_sha256"],
        "semantic_review_evidence_sha256": semantic["evidence_sha256"],
        "test_author_evidence_sha256": test_evidence["evidence_sha256"],
        "delta_audit_evidence_sha256": delta["evidence_sha256"],
        "separation_evidence_sha256": separation["evidence_sha256"],
        "executable_evidence_sha256": executable["evidence_sha256"],
    })
    envelope = {
        "schema_version": ENVELOPE_SCHEMA, "candidate": candidate,
        "assignment": {
            "contract_id": CONTRACT_ID, "cell_id": assignment["cell_id"],
            "primary_capability": assignment["primary_capability"],
            "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        },
        "evidence": {
            "teacher_proof": proof, "semantic_review": semantic, "test_author": test_evidence,
            "delta_audit": delta, "separation": separation, "executable": executable,
            "lineage": lineage,
        },
    }
    artifact = {
        "schema_version": ARTIFACT_SCHEMA, "status": "ready-for-admission",
        "input_sha256": input_sha, "candidate_id": candidate["id"], "envelope": envelope,
        "retry_ledger": retry_ledger, "evaluation_artifacts_read": 0,
    }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    return artifact


def run_resumable(
    generated_rows: list[dict[str, Any]], assignments: dict[str, dict[str, Any]],
    output_dir: Path, runtime_path: Path, semantic_fn: StageFn, test_fn: StageFn,
    delta_fn: StageFn, separation_fn: SeparationFn, verifier_fn: VerifierFn = verify,
) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict[str, Any]] = []
    for generated in generated_rows:
        identifier = generated.get("candidate", {}).get("id")
        assignment = assignments.get(identifier)
        if not isinstance(identifier, str) or not isinstance(assignment, dict):
            raise ValueError("generated candidate lacks an exact assignment")
        path = output_dir / f"{identifier}.evidence.json"
        expected_input = canonical_sha256({"generated": generated, "assignment": assignment})
        if path.exists():
            artifact = json.loads(path.read_text(encoding="utf-8"))
            body = dict(artifact); claimed = body.pop("artifact_sha256", None)
            if claimed != canonical_sha256(body) or artifact.get("input_sha256") != expected_input:
                raise ValueError(f"{identifier}: resumable artifact is unsealed or binds different input")
        else:
            artifact = produce_candidate(
                generated, assignment, runtime_path, semantic_fn, test_fn, delta_fn,
                separation_fn, verifier_fn,
            )
            path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        artifacts.append(artifact)
    return artifacts


def _response_schema(stage: str) -> dict[str, Any]:
    boolean = {"type": "boolean"}
    if stage == "semantic_review":
        properties = {field: boolean for field in SEMANTIC_BOOLEANS}
        properties["rationale"] = {"type": "string", "minLength": 1}
    elif stage == "test_author":
        properties = {"files": {
            "type": "array", "minItems": 2,
            "items": {"type": "object", "additionalProperties": False,
                      "required": ["path", "content", "role", "case_ids"],
                      "properties": {
                          "path": {"type": "string", "minLength": 1},
                          "content": {"type": "string", "minLength": 1},
                          "role": {"enum": ["primary_discrimination", "cross_cutting"]},
                          "case_ids": {"type": "array", "minItems": 1,
                                       "items": {"type": "string", "minLength": 1}},
                      }},
        }}
    elif stage == "delta_audit":
        properties = {
            "independent_semantic_delta_count": {"type": "integer", "minimum": 0},
            "delta_is_capability_specific": boolean,
            "introduces_multiple_independent_fixes": boolean,
            "delta_description": {"type": "string", "minLength": 1},
        }
    else:
        raise ValueError(f"unknown Codex evidence stage {stage}")
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object",
        "additionalProperties": False, "required": list(properties), "properties": properties,
    }


def _stage_prompt(stage: str, projection: dict[str, Any]) -> str:
    common = "Do not use tools or inspect the filesystem. Return only the schema-constrained object."
    if stage == "semantic_review":
        instruction = (
            "Blindly assess all six repair-delta booleans from only this specification, embedded known-bad, "
            "and assigned labels. You have not seen the teacher proof, reference, tests, verifier output, "
            "source stimulus, v2 outcomes, or evaluation material."
        )
    elif stage == "test_author":
        instruction = (
            "Author independent deterministic standard-library tests from only this specification, embedded "
            "known-bad, capability definition, and scheduled dimension. Emit distinct hashed-file inputs for "
            "primary_discrimination (at least two valid-domain cases) and cross_cutting (at least one isolated "
            "scheduled-dimension case). You have not seen the reference, proof, semantic result, verifier output, "
            "or evaluation material."
        )
    elif stage == "delta_audit":
        instruction = (
            "Audit the known-bad/reference delta using only the supplied specification, implementations, and "
            "assigned labels. Identify the number of independent semantic fixes and whether the sole delta is "
            "capability-specific. You have not seen tests, proof, verifier output, source stimulus, v2 outcomes, "
            "or evaluation material."
        )
    else:
        raise ValueError(f"unknown Codex evidence stage {stage}")
    return f"{instruction}\nInput: {json.dumps(projection, separators=(',', ':'), ensure_ascii=False)}\n{common}"


class IsolatedCodexAdapter:
    """One-stage adapter with content-addressed, sealed per-candidate resumption."""

    def __init__(
        self, stage: str, config: dict[str, Any], codex_bin: str, run_dir: Path,
        cli_identity: str,
    ) -> None:
        self.stage = stage
        self.config = config
        self.codex_bin = codex_bin
        self.run_dir = run_dir
        self.cli_identity = cli_identity
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def __call__(self, projection: dict[str, Any]) -> dict[str, Any]:
        identifier = projection.get("id")
        if not isinstance(identifier, str) or not identifier or any(
            char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in identifier
        ):
            raise ValueError("stage candidate ID is not a safe artifact name")
        prompt = _stage_prompt(self.stage, projection)
        input_sha = canonical_sha256({"stage": self.stage, "projection": projection, "prompt": prompt})
        path = self.run_dir / f"{identifier}.{self.stage}.json"
        if path.exists():
            artifact = json.loads(path.read_text(encoding="utf-8"))
            body = dict(artifact); claimed = body.pop("artifact_sha256", None)
            if claimed != canonical_sha256(body) or artifact.get("input_sha256") != input_sha:
                raise ValueError(f"{identifier}/{self.stage}: sealed Codex run drift")
            return {**artifact["response"], "_run_sha256": artifact["run"]["run_evidence_sha256"]}
        with tempfile.TemporaryDirectory(prefix=f"ganesh-v3-{self.stage}-") as temp_name:
            schema_path = Path(temp_name) / "schema.json"
            schema_path.write_text(json.dumps(_response_schema(self.stage), sort_keys=True) + "\n", encoding="utf-8")
            response, run = invoke_codex(
                self.codex_bin, self.config, schema_path, prompt,
                f"repair-delta-{self.stage}", projection.get("lane", "unknown"),
            )
        run = dict(run)
        run["run_evidence_sha256"] = canonical_sha256(run)
        artifact = {
            "schema_version": "ganesh-mini-repair-delta-codex-stage/v1",
            "stage": self.stage, "candidate_id": identifier, "input_sha256": input_sha,
            "prompt_sha256": sha256_text(prompt), "cli_identity": self.cli_identity,
            "config_sha256": canonical_sha256(self.config), "response": response, "run": run,
            "evaluation_artifacts_read": 0,
        }
        artifact["artifact_sha256"] = canonical_sha256(artifact)
        path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return {**response, "_run_sha256": run["run_evidence_sha256"]}


def load_campaign_inputs(
    queue_path: Path, manifest_path: Path, candidate_paths: list[Path],
    evidence_paths: list[Path], cohort: str, reserve_eligibility_path: Path | None = None,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    manifest = load_sealed(manifest_path, "manifest_sha256")
    queue_payload = queue_path.read_bytes()
    queue = [json.loads(line) for line in queue_payload.decode().splitlines() if line.strip()]
    if (
        manifest.get("schema_version") != "ganesh-mini-repair-delta-queue-manifest/v1"
        or manifest.get("plan_sha256") != PLAN_SHA256
        or manifest.get("queue_sha256") != hashlib.sha256(queue_payload).hexdigest()
        or manifest.get("assignments") != 120 or len(queue) != 120
        or len({row.get("id") for row in queue}) != 120
        or len(candidate_paths) != len(evidence_paths) or not candidate_paths
        or cohort not in {"primary", "reserve"}
    ):
        raise ValueError("sealed queue, teacher batch pairs, or cohort are invalid")
    queue_by_id = {row["id"]: row for row in queue}
    generated: list[dict[str, Any]] = []
    for candidate_path, evidence_path in zip(candidate_paths, evidence_paths, strict=True):
        evidence = load_sealed(evidence_path, "evidence_sha256")
        payload = candidate_path.read_bytes()
        rows = [json.loads(line) for line in payload.decode().splitlines() if line.strip()]
        ids = [row.get("candidate", {}).get("id") for row in rows]
        if (
            evidence.get("schema_version") != "ganesh-mini-repair-delta-teacher-batch/v1"
            or evidence.get("plan_sha256") != PLAN_SHA256
            or evidence.get("queue_manifest_sha256") != manifest["manifest_sha256"]
            or evidence.get("role") != cohort
            or evidence.get("candidate_output_sha256") != hashlib.sha256(payload).hexdigest()
            or evidence.get("requested_ids") != ids or evidence.get("generated") != len(rows)
            or evidence.get("failures") != [] or evidence.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError(f"{candidate_path}: teacher batch is incomplete or unbound")
        generated.extend(rows)
    ids = [row.get("candidate", {}).get("id") for row in generated]
    selected = [queue_by_id.get(identifier) for identifier in ids]
    if any(not isinstance(row, dict) or row.get("role") != cohort for row in selected) or len(set(ids)) != len(ids):
        raise ValueError("teacher outputs do not map uniquely to the requested queue cohort")
    if cohort == "primary":
        if reserve_eligibility_path is not None or len(generated) != 60 or len({row["cell_id"] for row in selected}) != 60:
            raise ValueError("primary evidence campaign requires exactly all 60 repair cells")
    else:
        if reserve_eligibility_path is None:
            raise ValueError("reserve evidence campaign requires sealed eligibility")
        eligible = load_reserve_eligibility(reserve_eligibility_path, manifest["manifest_sha256"])
        if not 1 <= len(generated) <= 6 or {row["cell_id"] for row in selected} != eligible:
            raise ValueError("reserve teacher outputs differ from sealed eligible cells")
    return generated, {row["id"]: row for row in selected}, manifest


def load_separation_sidecars(path: Path, contract_sha256: str) -> SeparationFn:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        body = dict(row); claimed = body.pop("evidence_sha256", None)
        identifier = row.get("candidate_id")
        if (
            claimed != canonical_sha256(body) or not isinstance(identifier, str)
            or identifier in by_id or row.get("comparison_contract_sha256") != contract_sha256
            or row.get("evaluation_artifacts_read_by_construction") != 0
        ):
            raise ValueError("separation sidecars are unsealed, duplicated, or use another contract")
        by_id[identifier] = row

    def lookup(candidate: dict[str, Any]) -> dict[str, Any]:
        row = by_id.get(candidate["id"])
        if row is None or row.get("candidate_sha256") != canonical_sha256(candidate):
            raise ValueError(f"{candidate['id']}: exact separation sidecar is absent")
        return copy.deepcopy(row)
    return lookup


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--teacher-candidates", type=Path, action="append", required=True)
    parser.add_argument("--teacher-evidence", type=Path, action="append", required=True)
    parser.add_argument("--cohort", choices=("primary", "reserve"), required=True)
    parser.add_argument("--reserve-eligibility", type=Path)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--separation-sidecars", type=Path, required=True)
    parser.add_argument("--separation-contract-sha256", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    generated, assignments, manifest = load_campaign_inputs(
        args.queue, args.queue_manifest, args.teacher_candidates, args.teacher_evidence,
        args.cohort, args.reserve_eligibility,
    )
    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    adapters = {
        stage: IsolatedCodexAdapter(stage, config, args.codex_bin, args.output_root / "codex-runs", cli_identity)
        for stage in ("semantic_review", "test_author", "delta_audit")
    }
    separation = load_separation_sidecars(args.separation_sidecars, args.separation_contract_sha256)
    artifacts = run_resumable(
        generated, assignments, args.output_root / "candidate-evidence", args.runtime_config,
        adapters["semantic_review"], adapters["test_author"], adapters["delta_audit"], separation,
    )
    envelope_path = args.output_root / "admission-envelopes.jsonl"
    ready = [row["envelope"] for row in artifacts if row["status"] == "ready-for-admission"]
    envelope_path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in ready))
    inventory_path = args.output_root / "evidence-inventory.json"
    inventory: dict[str, Any] = {
        "schema_version": "ganesh-mini-repair-delta-evidence-campaign/v1",
        "status": "ready-for-admission" if len(ready) == len(artifacts) else "terminal-or-unresolved",
        "cohort": args.cohort, "queue_manifest_sha256": manifest["manifest_sha256"],
        "generated": len(generated), "ready": len(ready),
        "terminal_rejected": sum(row["status"] == "terminal-rejected" for row in artifacts),
        "unresolved": sum(row["status"] == "unresolved" for row in artifacts),
        "envelopes": {"path": str(envelope_path), "bytes": envelope_path.stat().st_size,
                      "sha256": hashlib.sha256(envelope_path.read_bytes()).hexdigest()},
        "artifact_sha256s": {row["candidate_id"]: row["artifact_sha256"] for row in artifacts},
        "cli_identity": cli_identity, "codex_config_sha256": hashlib.sha256(args.codex_config.read_bytes()).hexdigest(),
        "runtime_config_sha256": hashlib.sha256(args.runtime_config.read_bytes()).hexdigest(),
        "separation_sidecars_sha256": hashlib.sha256(args.separation_sidecars.read_bytes()).hexdigest(),
        "evaluation_artifacts_read": 0,
    }
    inventory["report_sha256"] = canonical_sha256(inventory)
    inventory_path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": inventory["status"], "ready": len(ready), "report_sha256": inventory["report_sha256"]}, sort_keys=True))
    return 0 if inventory["status"] == "ready-for-admission" else 2


if __name__ == "__main__":
    raise SystemExit(main())
