#!/usr/bin/env python3
"""Run v3 repair-delta evidence across the content-free separation boundary.

Phase one performs only blind semantic review, independent split-test
authorship, and delta audit.  It emits the complete post-test candidate cohort
before any candidate code is executed.  The existing global separation
builder then compares that cohort as one immutable batch.  Phase two consumes
only content-free, sealed per-candidate sidecars and may execute the split
suites and assemble admission envelopes.

The orchestration functions accept stage/verifier callables so unit tests do
not invoke Codex, containers, or evaluation data.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, as_completed, wait
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_expansion import canonical_json  # noqa: E402
from scripts.data.admit_repair_delta import (  # noqa: E402
    CONTRACT_ID, ENVELOPE_SCHEMA, PROOF_BOOLEAN_OVERLAP, SEMANTIC_BOOLEANS,
    SEPARATION_PASSES, V4_ASSEMBLY_SCHEMA, V4_CONTRACT_ID, V4_ENVELOPE_SCHEMA,
    V5_ASSEMBLY_SCHEMA, V5_ENVELOPE_SCHEMA,
    load_v4_primary_cohort_binding, teacher_candidate_sha256,
    validate_envelope, validate_v4_terminal_accounting,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.data.build_capability_separation_attestations import (  # noqa: E402
    PASS_FIELDS, SCHEMA_VERSION as SEPARATION_REPORT_SCHEMA, build_report,
)
from scripts.data.generate_expansion_qualification import verify_codex_version  # noqa: E402
from scripts.data.run_repair_delta_evidence import (  # noqa: E402
    ARTIFACT_SCHEMA, IsolatedCodexAdapter, StageFn, StageInvocationFailure, VerifierFn,
    add_tests_for_contract, _delta_evidence, _executable_evidence, _rebind_semantic,
    _semantic_evidence, _terminal, delta_projection, load_campaign_inputs,
    semantic_projection, seal, test_author_projection,
)
from scripts.data.repair_delta_v4_preflight import (  # noqa: E402
    PLAN_SHA256 as V4_PLAN_SHA256, execute_post_teacher_preflight,
    V4PreflightFailure, validate_teacher_proof_v4,
)
from scripts.data.repair_delta_v5_preflight import (  # noqa: E402
    CONTRACT_ID as V5_CONTRACT_ID, V5PreflightFailure,
    execute_v5_interface_preflight,
)
from scripts.verify.sandbox import verify  # noqa: E402


PREPARATION_SCHEMA = "ganesh-mini-repair-delta-pre-separation/v1"
SIDECAR_SCHEMA = "ganesh-mini-repair-delta-separation-sidecar/v1"
CAMPAIGN_SCHEMA = "ganesh-mini-repair-delta-two-phase-campaign/v1"
V4_VERIFIER_SCHEDULER_CONTRACT = {
    "schema_version": "ganesh-mini-repair-delta-v4-verifier-scheduler/v1",
    "scheduler_id": "gate2-v4-lane-aware-verifier/v1",
    "global_candidate_concurrency": 6,
    "lane_candidate_concurrency": {
        "go": 1, "java": 4, "javascript": 4,
        "typescript": 2, "python": 4, "rust": 4,
    },
    "all_lane_limits_explicit": True,
    "scheduling_unit": "candidate",
    "per_candidate_suites_sequential": True,
}
V4_VERIFIER_SCHEDULER_SHA256 = canonical_sha256(V4_VERIFIER_SCHEDULER_CONTRACT)
V5_VERIFIER_SCHEDULER_CONTRACT = {
    **copy.deepcopy(V4_VERIFIER_SCHEDULER_CONTRACT),
    "schema_version": "ganesh-mini-repair-delta-v5-verifier-scheduler/v1",
    "scheduler_id": "gate2-v5-lane-aware-verifier/v1",
    "go_final_suite_attempt_timeout_seconds": 120,
    "go_aggregate_candidate_timeout_seconds": None,
}
V5_VERIFIER_SCHEDULER_SHA256 = canonical_sha256(V5_VERIFIER_SCHEDULER_CONTRACT)
V4_LANES = frozenset({"go", "java", "javascript", "typescript", "python", "rust"})
V5_ASSEMBLY_MANIFEST_SCHEMA = "ganesh-mini-gate2-v5-execution-cohort-manifest/v1"
V5_ASSIGNMENT_SCHEMA = "ganesh-mini-repair-delta-v5-assignment/v1"
V5_READINESS_SCHEMA = "ganesh-mini-gate2-v5-composite-readiness/v1"


def _sealed(value: dict[str, Any], field: str) -> dict[str, Any]:
    body = dict(value)
    claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"unsealed {field} artifact")
    return value


def _as_v4_assembly(value: dict[str, Any]) -> dict[str, Any]:
    output = copy.deepcopy(value)
    output["schema_version"] = V4_ASSEMBLY_SCHEMA
    output.pop("artifact_sha256", None)
    output["artifact_sha256"] = canonical_sha256(output)
    return output


def _as_v5_assembly(value: dict[str, Any]) -> dict[str, Any]:
    output = copy.deepcopy(value)
    output["schema_version"] = V5_ASSEMBLY_SCHEMA
    output.pop("artifact_sha256", None)
    output["artifact_sha256"] = canonical_sha256(output)
    return output


def _stage_contract_failure(
    candidate: dict[str, Any], stage: str, response: Any, exc: Exception,
) -> dict[str, Any]:
    """Seal a candidate-local malformed stage response without exposing it downstream."""
    run_sha256 = response.get("_run_sha256") if isinstance(response, dict) else None
    return seal({
        "schema_version": "ganesh-mini-repair-delta-v4-stage-contract-failure/v1",
        "candidate_id": candidate["id"],
        "candidate_sha256": canonical_sha256(candidate),
        "stage": stage,
        "response_sha256": canonical_sha256(response),
        "run_evidence_sha256": run_sha256,
        "error_type": type(exc).__name__,
        "reason": str(exc),
        "evaluation_artifacts_read": 0,
    })


def _envelope_assignment(
    assignment: dict[str, Any], contract_id: str,
) -> dict[str, Any]:
    if contract_id in {V4_CONTRACT_ID, V5_CONTRACT_ID}:
        return copy.deepcopy(assignment)
    return {
        "contract_id": contract_id, "cell_id": assignment["cell_id"],
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
    }


def _write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    """Atomically publish one candidate-local artifact in its final directory."""
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            handle.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
            temporary_path = Path(handle.name)
        temporary_path.replace(path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def load_v5_assembled_inputs(
    candidates_path: Path, assignments_path: Path, assembly_manifest_path: Path,
    composite_readiness_path: Path, runtime_path: Path, preflight_config_path: Path,
    *, controller_binding_superseded_by_resilience: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    """Load the explicit, canonical 60-row V5 execution-cohort assembly."""
    candidate_bytes = candidates_path.read_bytes()
    assignment_bytes = assignments_path.read_bytes()
    generated = [json.loads(line) for line in candidate_bytes.splitlines() if line.strip()]
    assignment_rows = [json.loads(line) for line in assignment_bytes.splitlines() if line.strip()]
    manifest = json.loads(assembly_manifest_path.read_text(encoding="utf-8"))
    readiness = json.loads(composite_readiness_path.read_text(encoding="utf-8"))
    _sealed(manifest, "manifest_sha256")
    _sealed(readiness, "report_sha256")
    expected_ids = manifest.get("ordered_candidate_ids")
    if (
        manifest.get("schema_version") != V5_ASSEMBLY_MANIFEST_SCHEMA
        or manifest.get("contract_id") != V5_CONTRACT_ID
        or manifest.get("plan_sha256")
        != "132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b"
        or manifest.get("records") != 60
        or manifest.get("immutable_carries") != 58
        or manifest.get("fresh_teacher_primaries") != 2
        or manifest.get("evaluation_artifacts_read") != 0
        or not isinstance(expected_ids, list) or len(expected_ids) != 60
        or manifest.get("ordered_candidate_ids_sha256") != canonical_sha256(expected_ids)
        or manifest.get("candidate_output", {}).get("sha256")
        != hashlib.sha256(candidate_bytes).hexdigest()
        or manifest.get("assignment_output", {}).get("sha256")
        != hashlib.sha256(assignment_bytes).hexdigest()
        or manifest.get("generated_rows_sha256") != canonical_sha256(generated)
        or manifest.get("assignments_sha256") != canonical_sha256(assignment_rows)
        or readiness.get("schema_version") != V5_READINESS_SCHEMA
        or readiness.get("status") != "passed"
        or readiness.get("contract_id") != V5_CONTRACT_ID
        or readiness.get("plan_sha256") != manifest.get("plan_sha256")
        or readiness.get("report_sha256")
        != manifest.get("composite_readiness_report_sha256")
        or readiness.get("bindings", {}).get("runtime_config_sha256")
        != hashlib.sha256(runtime_path.read_bytes()).hexdigest()
        or readiness.get("bindings", {}).get("v5_preflight_config_sha256")
        != hashlib.sha256(preflight_config_path.read_bytes()).hexdigest()
        or (
            not controller_binding_superseded_by_resilience
            and readiness.get("bindings", {}).get("runtime_code_sha256", {}).get(
                "scripts/data/run_repair_delta_two_phase.py"
            ) != hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        )
    ):
        raise ValueError("V5 execution-cohort assembly or composite readiness is invalid")
    if len(generated) != 60 or len(assignment_rows) != 60:
        raise ValueError("V5 assembled inputs must contain exactly 60 rows")
    actual_ids = [row.get("candidate", {}).get("id") for row in generated]
    assignment_ids = [row.get("id") for row in assignment_rows]
    if actual_ids != expected_ids or assignment_ids != expected_ids:
        raise ValueError("V5 assembled candidates and assignments differ from canonical order")
    assignments: dict[str, dict[str, Any]] = {}
    for generated_row, assignment in zip(generated, assignment_rows, strict=True):
        body = dict(assignment); claimed = body.pop("assignment_sha256", None)
        candidate = generated_row.get("candidate")
        if (
            claimed != canonical_sha256(body)
            or assignment.get("schema_version") != V5_ASSIGNMENT_SCHEMA
            or assignment.get("contract_id") != V5_CONTRACT_ID
            or not isinstance(candidate, dict)
            or assignment.get("id") != candidate.get("id")
            or assignment.get("lane") != candidate.get("lane")
            or assignment.get("source") != candidate.get("source")
            or assignment["id"] in assignments
        ):
            raise ValueError("V5 assembled assignment is unsealed or candidate-unbound")
        assignments[assignment["id"]] = assignment
    return generated, assignments, manifest


def _validate_teacher_binding(
    generated: dict[str, Any], assignment: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], str]:
    candidate = copy.deepcopy(generated["candidate"])
    proof = copy.deepcopy(generated["repair_delta_proof"])
    input_sha = canonical_sha256({"generated": generated, "assignment": assignment})
    proof_body = dict(proof)
    proof_claimed = proof_body.pop("evidence_sha256", None)
    if (
        proof_claimed != canonical_sha256(proof_body)
        or proof.get("candidate_id") != candidate.get("id")
        or proof.get("teacher_candidate_sha256") != teacher_candidate_sha256(candidate)
        or assignment.get("id") != candidate.get("id")
        or assignment.get("contract_id") != CONTRACT_ID
    ):
        raise ValueError("teacher proof, pre-test candidate, and sealed assignment do not bind")
    return candidate, proof, input_sha


def prepare_candidate(
    generated: dict[str, Any], assignment: dict[str, Any],
    semantic_fn: StageFn, test_fn: StageFn, delta_fn: StageFn,
) -> dict[str, Any]:
    """Author all pre-execution evidence and return a sealed post-test row."""
    candidate, proof, input_sha = _validate_teacher_binding(generated, assignment)

    semantic_response = semantic_fn(semantic_projection(candidate, assignment))
    semantic_run = semantic_response.pop("_run_sha256")
    semantic = _semantic_evidence(candidate, assignment, semantic_response, semantic_run)
    if any(semantic[field] is not True for field in SEMANTIC_BOOLEANS):
        return _terminal(candidate, assignment, "semantic_review", "blind semantic boolean failed", {
            "teacher_proof": proof, "semantic_review": semantic,
        }, input_sha)
    if any(semantic[field] is not proof[field] for field in PROOF_BOOLEAN_OVERLAP):
        return _terminal(candidate, assignment, "proof_consistency", "teacher proof disagrees with blind review", {
            "teacher_proof": proof, "semantic_review": semantic,
        }, input_sha)

    test_response = test_fn(test_author_projection(candidate, assignment))
    test_run = test_response.pop("_run_sha256")
    candidate, test_evidence = add_tests_for_contract(
        candidate, assignment, test_response, test_run,
    )
    semantic = _rebind_semantic(semantic, candidate)

    delta_response = delta_fn(delta_projection(candidate, assignment))
    delta_run = delta_response.pop("_run_sha256")
    delta = _delta_evidence(candidate, assignment, delta_response, delta_run)
    if (
        delta["independent_semantic_delta_count"] != 1
        or delta["delta_is_capability_specific"] is not True
        or delta["introduces_multiple_independent_fixes"] is not False
    ):
        return _terminal(candidate, assignment, "delta_audit", "delta auditor rejected the repair", {
            "teacher_proof": proof, "semantic_review": semantic,
            "test_author": test_evidence, "delta_audit": delta,
        }, input_sha)

    artifact: dict[str, Any] = {
        "schema_version": PREPARATION_SCHEMA,
        "status": "awaiting-separation",
        "input_sha256": input_sha,
        "candidate_id": candidate["id"],
        "candidate_sha256": canonical_sha256(candidate),
        "cell_id": assignment["cell_id"],
        "candidate": candidate,
        "assignment": copy.deepcopy(assignment),
        "evidence": {
            "teacher_proof": proof, "semantic_review": semantic,
            "test_author": test_evidence, "delta_audit": delta,
        },
        "execution_performed": False,
        "evaluation_artifacts_read": 0,
    }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    return artifact


def prepare_candidate_v4(
    generated: dict[str, Any], assignment: dict[str, Any],
    semantic_fn: StageFn, test_fn: StageFn, delta_fn: StageFn,
    runtime_path: Path, preflight_config_path: Path,
) -> dict[str, Any]:
    """Run mandatory V4 preflight before any blind reviewer or test author."""
    candidate = copy.deepcopy(generated["candidate"])
    proof = copy.deepcopy(generated["repair_delta_proof"])
    input_sha = canonical_sha256({"generated": generated, "assignment": assignment})
    if assignment.get("contract_id") != V4_CONTRACT_ID:
        raise ValueError("V4 preparation requires the exact V4 assignment contract")
    validate_teacher_proof_v4(candidate, assignment, proof)
    try:
        preflight = execute_post_teacher_preflight(
            candidate, assignment, proof, runtime_path, preflight_config_path,
        )
    except V4PreflightFailure as exc:
        if exc.evidence is None:
            raise
        artifact = _as_v4_assembly(_terminal(
            candidate, assignment, "post_teacher_preflight", str(exc),
            {"teacher_proof": proof, "post_teacher_preflight": exc.evidence}, input_sha,
        ))
        if exc.status == "unresolved":
            artifact["status"] = "unresolved"
            artifact.pop("artifact_sha256")
            artifact["artifact_sha256"] = canonical_sha256(artifact)
        return artifact

    semantic_response = semantic_fn(semantic_projection(candidate, assignment))
    semantic_payload = copy.deepcopy(semantic_response)
    try:
        semantic_run = semantic_response.pop("_run_sha256")
        semantic = _semantic_evidence(candidate, assignment, semantic_response, semantic_run)
    except (KeyError, TypeError, ValueError) as exc:
        return _as_v4_assembly(_terminal(
            candidate, assignment, "semantic_review_contract", str(exc), {
                "teacher_proof": proof, "post_teacher_preflight": preflight,
                "stage_contract_failure": _stage_contract_failure(
                    candidate, "semantic_review", semantic_payload, exc,
                ),
            }, input_sha,
        ))
    if any(semantic[field] is not True for field in SEMANTIC_BOOLEANS):
        return _as_v4_assembly(_terminal(candidate, assignment, "semantic_review", "blind semantic boolean failed", {
            "teacher_proof": proof, "post_teacher_preflight": preflight,
            "semantic_review": semantic,
        }, input_sha))
    if any(semantic[field] is not proof[field] for field in PROOF_BOOLEAN_OVERLAP):
        return _as_v4_assembly(_terminal(candidate, assignment, "proof_consistency", "teacher proof disagrees with blind review", {
            "teacher_proof": proof, "post_teacher_preflight": preflight,
            "semantic_review": semantic,
        }, input_sha))

    test_response = test_fn(test_author_projection(candidate, assignment))
    test_payload = copy.deepcopy(test_response)
    try:
        test_run = test_response.pop("_run_sha256")
        candidate, test_evidence = add_tests_for_contract(
            candidate, assignment, test_response, test_run,
        )
    except (KeyError, TypeError, ValueError) as exc:
        return _as_v4_assembly(_terminal(
            candidate, assignment, "test_author_contract", str(exc), {
                "teacher_proof": proof, "post_teacher_preflight": preflight,
                "semantic_review": semantic,
                "stage_contract_failure": _stage_contract_failure(
                    candidate, "test_author", test_payload, exc,
                ),
            }, input_sha,
        ))
    semantic = _rebind_semantic(semantic, candidate)
    delta_response = delta_fn(delta_projection(candidate, assignment))
    delta_payload = copy.deepcopy(delta_response)
    try:
        delta_run = delta_response.pop("_run_sha256")
        delta = _delta_evidence(candidate, assignment, delta_response, delta_run)
    except (KeyError, TypeError, ValueError) as exc:
        return _as_v4_assembly(_terminal(
            candidate, assignment, "delta_audit_contract", str(exc), {
                "teacher_proof": proof, "post_teacher_preflight": preflight,
                "semantic_review": semantic, "test_author": test_evidence,
                "stage_contract_failure": _stage_contract_failure(
                    candidate, "delta_audit", delta_payload, exc,
                ),
            }, input_sha,
        ))
    evidence = {
        "teacher_proof": proof, "post_teacher_preflight": preflight,
        "semantic_review": semantic, "test_author": test_evidence, "delta_audit": delta,
    }
    if (
        delta["independent_semantic_delta_count"] != 1
        or delta["delta_is_capability_specific"] is not True
        or delta["introduces_multiple_independent_fixes"] is not False
    ):
        return _as_v4_assembly(_terminal(
            candidate, assignment, "delta_audit", "delta auditor rejected the repair",
            evidence, input_sha,
        ))
    artifact: dict[str, Any] = {
        "schema_version": PREPARATION_SCHEMA, "status": "awaiting-separation",
        "input_sha256": input_sha, "candidate_id": candidate["id"],
        "candidate_sha256": canonical_sha256(candidate), "cell_id": assignment["cell_id"],
        "candidate": candidate, "assignment": copy.deepcopy(assignment),
        "evidence": evidence, "execution_performed": True,
        "pre_separation_execution_scope": "compile-and-known-bad-cross-witness-only",
        "evaluation_artifacts_read": 0,
    }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    return artifact


def prepare_candidate_v5(
    generated: dict[str, Any], assignment: dict[str, Any],
    semantic_fn: StageFn, test_fn: StageFn, delta_fn: StageFn,
    runtime_path: Path, preflight_config_path: Path, v4_preflight_config_path: Path,
    carried_semantic: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the sealed V5 interface preflight before any downstream V5 stage."""
    candidate = copy.deepcopy(generated["candidate"])
    proof = copy.deepcopy(generated["repair_delta_proof"])
    input_sha = canonical_sha256({"generated": generated, "assignment": assignment})
    if assignment.get("contract_id") != V5_CONTRACT_ID:
        raise ValueError("V5 preparation requires the exact V5 assignment contract")
    def terminal(stage: str, reason: str, evidence: dict[str, Any]) -> dict[str, Any]:
        return _as_v5_assembly(
            _terminal(candidate, assignment, stage, reason, evidence, input_sha)
        )
    def unresolved_invocation(
        stage: str, exc: StageInvocationFailure, evidence: dict[str, Any],
    ) -> dict[str, Any]:
        value = terminal(stage, str(exc), {
            **evidence, "stage_invocation_failure": copy.deepcopy(exc.evidence),
        })
        value["status"] = "unresolved"
        value.pop("artifact_sha256")
        value["artifact_sha256"] = canonical_sha256(value)
        return value
    try:
        preflight = execute_v5_interface_preflight(
            candidate, assignment, proof, runtime_path, preflight_config_path,
            v4_preflight_config_path,
        )
    except V5PreflightFailure as exc:
        if exc.evidence is None:
            raise
        artifact = terminal("interface_preflight", str(exc), {
                "teacher_proof": proof,
                "interface_preflight": copy.deepcopy(exc.evidence),
            })
        if exc.status == "unresolved":
            artifact["status"] = "unresolved"
            artifact.pop("artifact_sha256")
            artifact["artifact_sha256"] = canonical_sha256(artifact)
        return artifact

    if carried_semantic is not None:
        semantic = copy.deepcopy(carried_semantic)
        semantic_body = dict(semantic)
        semantic_claimed = semantic_body.pop("evidence_sha256", None)
        if (
            semantic_claimed != canonical_sha256(semantic_body)
            or semantic.get("candidate_sha256") != canonical_sha256(candidate)
            or semantic.get("primary_capability") != assignment.get("primary_capability")
            or semantic.get("assigned_cross_cutting_dimension")
            != assignment.get("assigned_cross_cutting_dimension")
        ):
            raise ValueError("carried V5 semantic review is unsealed or candidate-unbound")
    else:
        try:
            semantic_response = semantic_fn(semantic_projection(candidate, assignment))
        except StageInvocationFailure as exc:
            return unresolved_invocation("semantic_review_invocation", exc, {
                "teacher_proof": proof, "interface_preflight": preflight,
            })
        semantic_payload = copy.deepcopy(semantic_response)
        try:
            semantic_run = semantic_response.pop("_run_sha256")
            semantic = _semantic_evidence(candidate, assignment, semantic_response, semantic_run)
        except (KeyError, TypeError, ValueError) as exc:
            return terminal("semantic_review_contract", str(exc), {
                "teacher_proof": proof, "interface_preflight": preflight,
                "stage_contract_failure": _stage_contract_failure(
                    candidate, "semantic_review", semantic_payload, exc,
                ),
            })
    if any(semantic[field] is not True for field in SEMANTIC_BOOLEANS):
        return terminal("semantic_review", "blind semantic boolean failed", {
            "teacher_proof": proof, "interface_preflight": preflight,
            "semantic_review": semantic,
        })
    if any(semantic[field] is not proof[field] for field in PROOF_BOOLEAN_OVERLAP):
        return terminal("proof_consistency", "teacher proof disagrees with blind review", {
            "teacher_proof": proof, "interface_preflight": preflight,
            "semantic_review": semantic,
        })

    try:
        test_response = test_fn(test_author_projection(candidate, assignment))
    except StageInvocationFailure as exc:
        return unresolved_invocation("test_author_invocation", exc, {
            "teacher_proof": proof, "interface_preflight": preflight,
            "semantic_review": semantic,
        })
    test_payload = copy.deepcopy(test_response)
    try:
        test_run = test_response.pop("_run_sha256")
        candidate, test_evidence = add_tests_for_contract(
            candidate, assignment, test_response, test_run,
        )
    except (KeyError, TypeError, ValueError) as exc:
        return terminal("test_author_contract", str(exc), {
            "teacher_proof": proof, "interface_preflight": preflight,
            "semantic_review": semantic,
            "stage_contract_failure": _stage_contract_failure(
                candidate, "test_author", test_payload, exc,
            ),
        })
    semantic = _rebind_semantic(semantic, candidate)
    try:
        delta_response = delta_fn(delta_projection(candidate, assignment))
    except StageInvocationFailure as exc:
        return unresolved_invocation("delta_audit_invocation", exc, {
            "teacher_proof": proof, "interface_preflight": preflight,
            "semantic_review": semantic, "test_author": test_evidence,
        })
    delta_payload = copy.deepcopy(delta_response)
    try:
        delta_run = delta_response.pop("_run_sha256")
        delta = _delta_evidence(candidate, assignment, delta_response, delta_run)
    except (KeyError, TypeError, ValueError) as exc:
        return terminal("delta_audit_contract", str(exc), {
            "teacher_proof": proof, "interface_preflight": preflight,
            "semantic_review": semantic, "test_author": test_evidence,
            "stage_contract_failure": _stage_contract_failure(
                candidate, "delta_audit", delta_payload, exc,
            ),
        })
    evidence = {
        "teacher_proof": proof, "interface_preflight": preflight,
        "semantic_review": semantic, "test_author": test_evidence, "delta_audit": delta,
    }
    if (
        delta["independent_semantic_delta_count"] != 1
        or delta["delta_is_capability_specific"] is not True
        or delta["introduces_multiple_independent_fixes"] is not False
    ):
        return terminal("delta_audit", "delta auditor rejected the repair", evidence)
    artifact: dict[str, Any] = {
        "schema_version": PREPARATION_SCHEMA, "status": "awaiting-separation",
        "input_sha256": input_sha, "candidate_id": candidate["id"],
        "candidate_sha256": canonical_sha256(candidate), "cell_id": assignment["cell_id"],
        "candidate": candidate, "assignment": copy.deepcopy(assignment),
        "evidence": evidence, "execution_performed": True,
        "pre_separation_execution_scope": "v5-interface-preflight-only",
        "evaluation_artifacts_read": 0,
    }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    return artifact


def load_v5_semantic_dispatch(
    manifest_path: Path, generated_rows: list[dict[str, Any]],
    assignments: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    """Validate and partition the exact 37 carried and 23 new V5 reviews."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    body = dict(manifest)
    claimed = body.pop("manifest_sha256", None)
    equivalences = manifest.get("equivalences")
    required_rows = manifest.get("review_required")
    if (
        claimed != canonical_sha256(body)
        or manifest.get("schema_version")
        != "ganesh-mini-gate2-v5-semantic-equivalence-manifest/v1"
        or manifest.get("contract_id") != V5_CONTRACT_ID
        or manifest.get("plan_sha256")
        != "132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b"
        or manifest.get("equivalent_reviews") != 37
        or manifest.get("new_reviews_required") != 23
        or manifest.get("evaluation_artifacts_read") != 0
        or not isinstance(equivalences, list) or len(equivalences) != 37
        or not isinstance(required_rows, list) or len(required_rows) != 23
        or manifest.get("equivalences_sha256") != canonical_sha256(equivalences)
        or manifest.get("review_required_sha256") != canonical_sha256(required_rows)
    ):
        raise ValueError("V5 semantic equivalence manifest is invalid or unsealed")
    generated = {
        row.get("candidate", {}).get("id"): row.get("candidate")
        for row in generated_rows if isinstance(row, dict)
    }
    if len(generated) != 60 or any(not isinstance(value, dict) for value in generated.values()):
        raise ValueError("V5 semantic dispatch requires the exact 60-candidate cohort")
    carried: dict[str, dict[str, Any]] = {}
    for row in equivalences:
        if not isinstance(row, dict):
            raise ValueError("V5 semantic equivalence row is malformed")
        identifier = row.get("candidate_id")
        candidate = generated.get(identifier)
        assignment = assignments.get(identifier)
        row_body = dict(row)
        row_claimed = row_body.pop("equivalence_row_sha256", None)
        evidence = row.get("semantic_evidence")
        evidence_body = dict(evidence) if isinstance(evidence, dict) else {}
        evidence_claimed = evidence_body.pop("evidence_sha256", None)
        if (
            row_claimed != canonical_sha256(row_body)
            or not isinstance(candidate, dict) or not isinstance(assignment, dict)
            or assignment.get("contract_id") != V5_CONTRACT_ID
            or row.get("cell_id") != assignment.get("cell_id")
            or row.get("candidate_sha256") != canonical_sha256(candidate)
            or row.get("semantic_projection_sha256")
            != canonical_sha256(semantic_projection(candidate, assignment))
            or row.get("semantic_evidence_sha256") != evidence_claimed
            or evidence_claimed != canonical_sha256(evidence_body)
            or evidence.get("candidate_sha256") != canonical_sha256(candidate)
            or identifier in carried
        ):
            raise ValueError("V5 carried semantic review is not exactly projection-equivalent")
        carried[identifier] = copy.deepcopy(evidence)
    required: set[str] = set()
    for row in required_rows:
        if not isinstance(row, dict) or set(row) != {"ordinal", "candidate_id", "cell_id", "reason"}:
            raise ValueError("V5 new semantic-review row is malformed")
        identifier = row["candidate_id"]
        assignment = assignments.get(identifier)
        expected_reason = (
            "fresh-v5-teacher-primary"
            if isinstance(assignment, dict)
            and assignment.get("mode") == "fresh-v5-teacher-primary"
            else "no-equivalent-v4-review"
        )
        if (
            identifier in required or identifier not in generated
            or not isinstance(assignment, dict)
            or row["cell_id"] != assignment.get("cell_id")
            or row["reason"] != expected_reason
        ):
            raise ValueError("V5 new semantic-review dispatch is duplicated or unbound")
        required.add(identifier)
    if set(generated) != set(assignments) or set(generated) != set(carried) | required or set(carried) & required:
        raise ValueError("V5 semantic carry/new-review partition does not cover exactly 60 candidates")
    return carried, required


def run_preparation_resumable_v4(
    generated_rows: list[dict[str, Any]], assignments: dict[str, dict[str, Any]],
    output_dir: Path, semantic_fn: StageFn, test_fn: StageFn, delta_fn: StageFn,
    runtime_path: Path, preflight_config_path: Path, workers: int = 6,
) -> list[dict[str, Any]]:
    if type(workers) is not int or not 1 <= workers <= 6:
        raise ValueError("V4 preparation workers must be an integer from 1 through 6")
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict[str, Any] | None] = [None] * len(generated_rows)
    pending: list[tuple[int, dict[str, Any], dict[str, Any], Path]] = []
    seen: set[str] = set()
    for index, generated in enumerate(generated_rows):
        identifier = generated.get("candidate", {}).get("id")
        assignment = assignments.get(identifier)
        if not isinstance(identifier, str) or not isinstance(assignment, dict) or identifier in seen:
            raise ValueError("V4 generated candidate lacks one unique exact assignment")
        seen.add(identifier)
        path = output_dir / f"{identifier}.pre-separation.json"
        expected = canonical_sha256({"generated": generated, "assignment": assignment})
        if path.exists():
            artifact = json.loads(path.read_text(encoding="utf-8"))
            _sealed(artifact, "artifact_sha256")
            if artifact.get("input_sha256") != expected:
                raise ValueError(f"{identifier}: prepared artifact binds different input")
            artifacts[index] = artifact
        else:
            pending.append((index, generated, assignment, path))

    def prepare_and_write(generated, assignment, path):
        artifact = prepare_candidate_v4(
            generated, assignment, semantic_fn, test_fn, delta_fn,
            runtime_path, preflight_config_path,
        )
        _write_json_atomic(path, artifact)
        return artifact

    waiting = [
        (index, generated["candidate"]["lane"], generated, assignment, path)
        for index, generated, assignment, path in pending
    ]
    lane_active: Counter[str] = Counter()
    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="repair-delta-v4-prep") as executor:
        futures: dict[Any, tuple[int, str]] = {}
        while waiting or futures:
            cursor = 0
            while cursor < len(waiting) and len(futures) < workers:
                index, lane, generated, assignment, path = waiting[cursor]
                if lane not in V4_LANES:
                    raise ValueError("V4 preparation requires one of the six frozen lanes")
                lane_limit = V4_VERIFIER_SCHEDULER_CONTRACT["lane_candidate_concurrency"][lane]
                if lane_active[lane] >= lane_limit:
                    cursor += 1
                    continue
                waiting.pop(cursor)
                lane_active[lane] += 1
                future = executor.submit(prepare_and_write, generated, assignment, path)
                futures[future] = (index, lane)
            if not futures:
                raise RuntimeError("V4 preparation scheduler could not dispatch a pending lane")
            completed, _ = wait(futures, return_when=FIRST_COMPLETED)
            for future in completed:
                index, lane = futures.pop(future)
                lane_active[lane] -= 1
                artifacts[index] = future.result()
    if any(artifact is None for artifact in artifacts):
        raise RuntimeError("V4 preparation did not produce one artifact per candidate")
    return [artifact for artifact in artifacts if artifact is not None]


def _v5_cached_invocation_replay_eligible(
    artifact: dict[str, Any], identifier: str, adapter: Any,
) -> bool:
    """Reopen only a cached unresolved stage with a sealed eligible correction."""
    return bool(
        artifact.get("status") == "unresolved"
        and artifact.get("terminal_stage") in {
            "semantic_review_invocation", "test_author_invocation", "delta_audit_invocation",
        }
        and adapter is not None
        and callable(getattr(adapter, "has_eligible_correction", None))
        and adapter.has_eligible_correction(identifier)
    )


def merge_v5_resilience_semantics(
    carried_semantics: dict[str, dict[str, Any]], review_required: set[str],
    interrupted_semantics: dict[str, dict[str, Any]], expected_additional: int = 3,
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    """Merge one sealed interruption carry into the frozen 37/23 partition."""
    expected_totals = {3: (40, 20), 5: (42, 18)}
    if expected_additional not in expected_totals:
        raise ValueError("V5 semantic recovery permits exactly three or five additional carries")
    interrupted_ids = set(interrupted_semantics)
    if (
        len(interrupted_semantics) != expected_additional
        or interrupted_ids & set(carried_semantics)
        or not interrupted_ids <= review_required
    ):
        raise ValueError("V5 interrupted semantic carries overlap or differ from the 23-call partition")
    merged = {**carried_semantics, **copy.deepcopy(interrupted_semantics)}
    remaining = review_required - interrupted_ids
    expected_carried, expected_remaining = expected_totals[expected_additional]
    if (
        len(merged) != expected_carried
        or len(remaining) != expected_remaining
        or set(merged) & remaining
    ):
        raise ValueError(
            f"V5 resilience semantic accounting differs from exact "
            f"{expected_carried} carry plus {expected_remaining} new"
        )
    return merged, remaining


def run_preparation_resumable_v5(
    generated_rows: list[dict[str, Any]], assignments: dict[str, dict[str, Any]],
    output_dir: Path, semantic_fn: StageFn, test_fn: StageFn, delta_fn: StageFn,
    runtime_path: Path, preflight_config_path: Path, v4_preflight_config_path: Path,
    semantic_equivalence_manifest_path: Path,
    interrupted_semantics: dict[str, dict[str, Any]] | None = None,
    expected_interrupted_semantics: int = 3,
    workers: int = 6,
) -> list[dict[str, Any]]:
    """Run V5 preparation with the same frozen lane concurrency as V4."""
    if type(workers) is not int or not 1 <= workers <= 6:
        raise ValueError("V5 preparation workers must be an integer from 1 through 6")
    carried_semantics, review_required = load_v5_semantic_dispatch(
        semantic_equivalence_manifest_path, generated_rows, assignments,
    )
    if interrupted_semantics is not None:
        carried_semantics, review_required = merge_v5_resilience_semantics(
            carried_semantics, review_required, interrupted_semantics,
            expected_interrupted_semantics,
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict[str, Any] | None] = [None] * len(generated_rows)
    pending: list[tuple[int, dict[str, Any], dict[str, Any], Path]] = []
    seen: set[str] = set()
    invocation_adapters = {
        "semantic_review_invocation": semantic_fn,
        "test_author_invocation": test_fn,
        "delta_audit_invocation": delta_fn,
    }
    for index, generated in enumerate(generated_rows):
        identifier = generated.get("candidate", {}).get("id")
        assignment = assignments.get(identifier)
        if not isinstance(identifier, str) or not isinstance(assignment, dict) or identifier in seen:
            raise ValueError("V5 generated candidate lacks one unique exact assignment")
        seen.add(identifier)
        path = output_dir / f"{identifier}.pre-separation.json"
        expected = canonical_sha256({"generated": generated, "assignment": assignment})
        if path.exists():
            artifact = json.loads(path.read_text(encoding="utf-8"))
            _sealed(artifact, "artifact_sha256")
            if artifact.get("input_sha256") != expected:
                raise ValueError(f"{identifier}: prepared artifact binds different input")
            adapter = invocation_adapters.get(artifact.get("terminal_stage"))
            eligible = _v5_cached_invocation_replay_eligible(
                artifact, identifier, adapter,
            )
            if eligible:
                pending.append((index, generated, assignment, path))
            else:
                artifacts[index] = artifact
        else:
            pending.append((index, generated, assignment, path))

    def prepare_and_write(generated, assignment, path):
        artifact = prepare_candidate_v5(
            generated, assignment, semantic_fn, test_fn, delta_fn,
            runtime_path, preflight_config_path, v4_preflight_config_path,
            carried_semantics.get(generated["candidate"]["id"]),
        )
        _write_json_atomic(path, artifact)
        return artifact

    waiting = [
        (index, generated["candidate"]["lane"], generated, assignment, path)
        for index, generated, assignment, path in pending
    ]
    lane_active: Counter[str] = Counter()
    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="repair-delta-v5-prep") as executor:
        futures: dict[Any, tuple[int, str]] = {}
        while waiting or futures:
            cursor = 0
            while cursor < len(waiting) and len(futures) < workers:
                index, lane, generated, assignment, path = waiting[cursor]
                if lane not in V4_LANES:
                    raise ValueError("V5 preparation requires one of the six frozen lanes")
                lane_limit = V4_VERIFIER_SCHEDULER_CONTRACT["lane_candidate_concurrency"][lane]
                if lane_active[lane] >= lane_limit:
                    cursor += 1
                    continue
                waiting.pop(cursor)
                lane_active[lane] += 1
                future = executor.submit(prepare_and_write, generated, assignment, path)
                futures[future] = (index, lane)
            if not futures:
                raise RuntimeError("V5 preparation scheduler could not dispatch a pending lane")
            completed, _ = wait(futures, return_when=FIRST_COMPLETED)
            for future in completed:
                index, lane = futures.pop(future)
                lane_active[lane] -= 1
                artifacts[index] = future.result()
    if any(artifact is None for artifact in artifacts):
        raise RuntimeError("V5 preparation did not produce one artifact per candidate")
    if set(carried_semantics) | review_required != seen:
        raise RuntimeError("V5 semantic dispatch did not cover the exact prepared cohort")
    return [artifact for artifact in artifacts if artifact is not None]


def run_preparation_resumable(
    generated_rows: list[dict[str, Any]], assignments: dict[str, dict[str, Any]],
    output_dir: Path, semantic_fn: StageFn, test_fn: StageFn, delta_fn: StageFn,
    workers: int = 12,
) -> list[dict[str, Any]]:
    if type(workers) is not int or not 1 <= workers <= 12:
        raise ValueError("preparation workers must be an integer from 1 through 12")
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict[str, Any] | None] = [None] * len(generated_rows)
    pending: list[tuple[int, dict[str, Any], dict[str, Any], Path]] = []
    identifiers: set[str] = set()
    for index, generated in enumerate(generated_rows):
        identifier = generated.get("candidate", {}).get("id")
        assignment = assignments.get(identifier)
        if not isinstance(identifier, str) or not isinstance(assignment, dict):
            raise ValueError("generated candidate lacks an exact assignment")
        if identifier in identifiers:
            raise ValueError("generated candidate identities are duplicated")
        identifiers.add(identifier)
        path = output_dir / f"{identifier}.pre-separation.json"
        expected = canonical_sha256({"generated": generated, "assignment": assignment})
        if path.exists():
            artifact = json.loads(path.read_text(encoding="utf-8"))
            _sealed(artifact, "artifact_sha256")
            if artifact.get("input_sha256") != expected:
                raise ValueError(f"{identifier}: prepared artifact binds different input")
            artifacts[index] = artifact
        else:
            pending.append((index, generated, assignment, path))

    def prepare_and_write(
        generated: dict[str, Any], assignment: dict[str, Any], path: Path,
    ) -> dict[str, Any]:
        artifact = prepare_candidate(generated, assignment, semantic_fn, test_fn, delta_fn)
        _write_json_atomic(path, artifact)
        return artifact

    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="repair-delta-prep") as executor:
        futures = {
            executor.submit(prepare_and_write, generated, assignment, path): index
            for index, generated, assignment, path in pending
        }
        for future in as_completed(futures):
            artifacts[futures[future]] = future.result()

    if any(artifact is None for artifact in artifacts):
        raise RuntimeError("preparation did not produce one artifact per input candidate")
    return [artifact for artifact in artifacts if artifact is not None]


def write_post_test_candidates(artifacts: list[dict[str, Any]], path: Path) -> list[dict[str, Any]]:
    candidates = [row["candidate"] for row in artifacts if row.get("status") == "awaiting-separation"]
    identifiers = [row["id"] for row in candidates]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("post-test candidate identities are duplicated")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in candidates))
    return candidates


def write_terminal_artifacts(artifacts: list[dict[str, Any]], path: Path) -> None:
    """Write the complete ordered cohort for terminal admission accounting.

    Unlike ``admission-envelopes.jsonl``, this artifact deliberately retains
    pre-execution rejects and unresolved verifier outcomes.  The final
    admission report can therefore disposition every generated candidate and
    the qualification summary cannot mistake a partial ready-only input for a
    complete first pass.
    """
    identifiers: list[str] = []
    for artifact in artifacts:
        _sealed(artifact, "artifact_sha256")
        identifier = artifact.get("candidate_id")
        if (
            artifact.get("schema_version") not in {
                ARTIFACT_SCHEMA, V4_ASSEMBLY_SCHEMA, V5_ASSEMBLY_SCHEMA,
            }
            or artifact.get("status") not in {
                "ready-for-admission", "terminal-rejected", "unresolved",
            }
            or not isinstance(identifier, str) or not identifier
        ):
            raise ValueError("terminal evidence cohort contains a malformed artifact")
        identifiers.append(identifier)
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("terminal evidence cohort contains duplicate candidate IDs")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in artifacts))


def separation_contract_sha256(report: dict[str, Any]) -> str:
    """Hash only the frozen comparator behavior, not observed candidate results."""
    return canonical_sha256({
        "schema_version": SEPARATION_REPORT_SCHEMA,
        "policy": report["comparison_manifest"]["policy"],
        "pass_fields": list(PASS_FIELDS),
        "sidecar_schema": SIDECAR_SCHEMA,
    })


def build_separation_sidecars(
    report: dict[str, Any], candidates: list[dict[str, Any]], output_path: Path,
) -> tuple[list[dict[str, Any]], str]:
    _sealed(report, "report_sha256")
    if (
        report.get("schema_version") != SEPARATION_REPORT_SCHEMA
        or report.get("evaluation_artifacts_read_by_construction") != 0
        or report.get("comparison_manifest_sha256")
        != canonical_sha256(report.get("comparison_manifest"))
    ):
        raise ValueError("global separation report is unsealed or not content-free")
    by_id = {row.get("id"): row for row in report.get("records", []) if isinstance(row, dict)}
    candidate_by_id = {row["id"]: row for row in candidates}
    if set(by_id) != set(candidate_by_id) or len(by_id) != len(report.get("records", [])):
        raise ValueError("global separation report does not cover the exact post-test cohort")
    contract_sha = separation_contract_sha256(report)
    sidecars: list[dict[str, Any]] = []
    for identifier in sorted(candidate_by_id):
        source = by_id[identifier]
        candidate_sha = canonical_sha256(candidate_by_id[identifier])
        if source.get("candidate_sha256") != candidate_sha or any(
            type(source.get(field)) is not bool for field in PASS_FIELDS
        ):
            raise ValueError(f"{identifier}: separation record is malformed or candidate-unbound")
        row = {
            "schema_version": SIDECAR_SCHEMA,
            "candidate_id": identifier,
            "candidate_sha256": candidate_sha,
            "comparison_contract_sha256": contract_sha,
            "comparison_manifest_sha256": report["comparison_manifest_sha256"],
            **{field: source[field] for field in PASS_FIELDS},
            "evaluation_artifacts_read_by_construction": 0,
        }
        row["evidence_sha256"] = canonical_sha256(row)
        sidecars.append(row)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in sidecars))
    return sidecars, contract_sha


def _validate_prepared(artifact: dict[str, Any]) -> None:
    _sealed(artifact, "artifact_sha256")
    candidate = artifact.get("candidate")
    evidence = artifact.get("evidence")
    if (
        artifact.get("schema_version") != PREPARATION_SCHEMA
        or artifact.get("status") != "awaiting-separation"
        or artifact.get("execution_performed") not in {False, True}
        or artifact.get("evaluation_artifacts_read") != 0
        or not isinstance(candidate, dict)
        or artifact.get("candidate_id") != candidate.get("id")
        or artifact.get("candidate_sha256") != canonical_sha256(candidate)
        or not isinstance(evidence, dict)
    ):
        raise ValueError("prepared artifact is malformed or not pre-execution")
    contract_id = artifact.get("assignment", {}).get("contract_id")
    expected = {"teacher_proof", "semantic_review", "test_author", "delta_audit"}
    if contract_id in {V4_CONTRACT_ID, V5_CONTRACT_ID}:
        expected.add(
            "interface_preflight" if contract_id == V5_CONTRACT_ID
            else "post_teacher_preflight"
        )
        expected_scope = (
            "v5-interface-preflight-only"
            if contract_id == V5_CONTRACT_ID
            else "compile-and-known-bad-cross-witness-only"
        )
        if (
            artifact.get("execution_performed") is not True
            or artifact.get("pre_separation_execution_scope") != expected_scope
        ):
            raise ValueError("prepared interface artifact lacks its isolated preflight execution scope")
    elif contract_id == CONTRACT_ID:
        if artifact.get("execution_performed") is not False or "pre_separation_execution_scope" in artifact:
            raise ValueError("prepared V3 artifact unexpectedly contains pre-separation execution")
    else:
        raise ValueError("prepared artifact has an unknown repair-delta contract")
    if set(evidence) != expected:
        raise ValueError("prepared artifact evidence set does not match its contract")
    for value in evidence.values():
        _sealed(value, "evidence_sha256")


def resume_candidate(
    prepared: dict[str, Any], separation: dict[str, Any], runtime_path: Path,
    verifier_fn: VerifierFn = verify,
) -> dict[str, Any]:
    """Consume a content-free sidecar, then and only then execute suites."""
    _validate_prepared(prepared)
    _sealed(separation, "evidence_sha256")
    candidate = copy.deepcopy(prepared["candidate"])
    assignment = copy.deepcopy(prepared["assignment"])
    if (
        separation.get("schema_version") != SIDECAR_SCHEMA
        or separation.get("candidate_id") != candidate["id"]
        or separation.get("candidate_sha256") != canonical_sha256(candidate)
        or separation.get("evaluation_artifacts_read_by_construction") != 0
    ):
        raise ValueError("separation sidecar does not bind the prepared candidate")
    evidence = copy.deepcopy(prepared["evidence"])
    evidence["separation"] = copy.deepcopy(separation)
    phase2_input_sha = canonical_sha256({
        "prepared_artifact_sha256": prepared["artifact_sha256"],
        "separation_evidence_sha256": separation["evidence_sha256"],
        "runtime_config_sha256": hashlib.sha256(runtime_path.read_bytes()).hexdigest(),
    })
    if any(separation.get(field) is not True for field in SEPARATION_PASSES):
        result = _terminal(
            candidate, assignment, "separation", "global content-free separation failed",
            evidence, prepared["input_sha256"],
        )
        result["phase2_input_sha256"] = phase2_input_sha
        result.pop("artifact_sha256")
        result["artifact_sha256"] = canonical_sha256(result)
        if assignment["contract_id"] == V4_CONTRACT_ID:
            return _as_v4_assembly(result)
        return _as_v5_assembly(result) if assignment["contract_id"] == V5_CONTRACT_ID else result

    executable, retry_ledger = _executable_evidence(
        candidate, evidence["test_author"], runtime_path, verifier_fn,
    )
    evidence["executable"] = executable
    if retry_ledger["unresolved"]:
        value = _terminal(
            candidate, assignment, "executable",
            "unresolved infrastructure after one identical replay",
            {**evidence, "retry_ledger": retry_ledger}, prepared["input_sha256"],
        )
        value["status"] = "unresolved"
        value["phase2_input_sha256"] = phase2_input_sha
        value.pop("artifact_sha256")
        value["artifact_sha256"] = canonical_sha256(value)
        if assignment["contract_id"] == V4_CONTRACT_ID:
            return _as_v4_assembly(value)
        return _as_v5_assembly(value) if assignment["contract_id"] == V5_CONTRACT_ID else value

    contract_id = assignment["contract_id"]
    lineage_body = {
        "candidate_sha256": canonical_sha256(candidate), "contract_id": contract_id,
        "cell_id": assignment["cell_id"],
        "source_identity": {key: candidate["source"].get(key) for key in ("dataset", "revision", "record_id")},
        "source_record_sha256": candidate["source"]["source_record_sha256"], "complete": True,
        "teacher_proof_evidence_sha256": evidence["teacher_proof"]["evidence_sha256"],
        "semantic_review_evidence_sha256": evidence["semantic_review"]["evidence_sha256"],
        "test_author_evidence_sha256": evidence["test_author"]["evidence_sha256"],
        "delta_audit_evidence_sha256": evidence["delta_audit"]["evidence_sha256"],
        "separation_evidence_sha256": separation["evidence_sha256"],
        "executable_evidence_sha256": executable["evidence_sha256"],
    }
    if contract_id == V4_CONTRACT_ID:
        lineage_body["post_teacher_preflight_evidence_sha256"] = evidence[
            "post_teacher_preflight"
        ]["evidence_sha256"]
    elif contract_id == V5_CONTRACT_ID:
        lineage_body["interface_preflight_evidence_sha256"] = evidence[
            "interface_preflight"
        ]["evidence_sha256"]
    lineage = seal(lineage_body)
    evidence["lineage"] = lineage
    envelope = {
        "schema_version": {
            V4_CONTRACT_ID: V4_ENVELOPE_SCHEMA,
            V5_CONTRACT_ID: V5_ENVELOPE_SCHEMA,
        }.get(contract_id, ENVELOPE_SCHEMA),
        "candidate": candidate,
        "assignment": _envelope_assignment(assignment, contract_id),
        "evidence": evidence,
    }
    result = {
        "schema_version": {
            V4_CONTRACT_ID: V4_ASSEMBLY_SCHEMA,
            V5_CONTRACT_ID: V5_ASSEMBLY_SCHEMA,
        }.get(contract_id, ARTIFACT_SCHEMA),
        "status": "ready-for-admission",
        "input_sha256": prepared["input_sha256"], "candidate_id": candidate["id"],
        "phase2_input_sha256": phase2_input_sha,
        "envelope": envelope, "retry_ledger": retry_ledger,
        "evaluation_artifacts_read": 0,
    }
    result["artifact_sha256"] = canonical_sha256(result)
    return result


def run_resume_resumable(
    prepared_rows: list[dict[str, Any]], sidecars: list[dict[str, Any]],
    output_dir: Path, runtime_path: Path, verifier_fn: VerifierFn = verify,
    workers: int = 12,
) -> list[dict[str, Any]]:
    if type(workers) is not int or not 1 <= workers <= 12:
        raise ValueError("phase-two workers must be an integer from 1 through 12")
    output_dir.mkdir(parents=True, exist_ok=True)
    by_id = {row.get("candidate_id"): row for row in sidecars}
    prepared_ids = [row.get("candidate_id") for row in prepared_rows]
    if (
        any(not isinstance(identifier, str) or not identifier for identifier in prepared_ids)
        or len(set(prepared_ids)) != len(prepared_ids)
    ):
        raise ValueError("prepared candidate identities are malformed or duplicated")
    awaiting = {row["candidate_id"] for row in prepared_rows if row.get("status") == "awaiting-separation"}
    if set(by_id) != awaiting or len(by_id) != len(sidecars):
        raise ValueError("separation sidecars do not exactly cover prepared post-test candidates")
    runtime_config_sha256 = hashlib.sha256(runtime_path.read_bytes()).hexdigest()
    results: list[dict[str, Any] | None] = [None] * len(prepared_rows)
    pending: list[tuple[int, dict[str, Any], dict[str, Any], Path]] = []
    for index, prepared in enumerate(prepared_rows):
        if prepared.get("status") != "awaiting-separation":
            results[index] = prepared
            continue
        identifier = prepared["candidate_id"]
        path = output_dir / f"{identifier}.evidence.json"
        expected_phase2_input = canonical_sha256({
            "prepared_artifact_sha256": prepared["artifact_sha256"],
            "separation_evidence_sha256": by_id[identifier]["evidence_sha256"],
            "runtime_config_sha256": runtime_config_sha256,
        })
        if path.exists():
            artifact = json.loads(path.read_text(encoding="utf-8"))
            _sealed(artifact, "artifact_sha256")
            if (
                artifact.get("input_sha256") != prepared["input_sha256"]
                or artifact.get("phase2_input_sha256") != expected_phase2_input
            ):
                raise ValueError(f"{identifier}: resumed artifact binds different phase-two input")
            results[index] = artifact
        else:
            pending.append((index, prepared, by_id[identifier], path))

    def resume_and_write(
        prepared: dict[str, Any], sidecar: dict[str, Any], path: Path,
    ) -> dict[str, Any]:
        artifact = resume_candidate(prepared, sidecar, runtime_path, verifier_fn)
        _write_json_atomic(path, artifact)
        return artifact

    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="repair-delta-verify") as executor:
        futures = {
            executor.submit(resume_and_write, prepared, sidecar, path): index
            for index, prepared, sidecar, path in pending
        }
        for future in as_completed(futures):
            results[futures[future]] = future.result()

    if any(result is None for result in results):
        raise RuntimeError("phase two did not produce one artifact per prepared candidate")
    return [result for result in results if result is not None]


def run_resume_resumable_v4(
    prepared_rows: list[dict[str, Any]], sidecars: list[dict[str, Any]],
    output_dir: Path, runtime_path: Path, verifier_fn: VerifierFn = verify,
    *, scheduler_contract: dict[str, Any] = V4_VERIFIER_SCHEDULER_CONTRACT,
    scheduler_sha256: str = V4_VERIFIER_SCHEDULER_SHA256,
    scheduler_label: str = "V4",
) -> list[dict[str, Any]]:
    """Run phase two under an explicit, sealed interface lane scheduler."""
    output_dir.mkdir(parents=True, exist_ok=True)
    by_id = {row.get("candidate_id"): row for row in sidecars}
    prepared_ids = [row.get("candidate_id") for row in prepared_rows]
    if (
        any(not isinstance(identifier, str) or not identifier for identifier in prepared_ids)
        or len(set(prepared_ids)) != len(prepared_ids)
    ):
        raise ValueError("prepared candidate identities are malformed or duplicated")
    awaiting = {row["candidate_id"] for row in prepared_rows if row.get("status") == "awaiting-separation"}
    if set(by_id) != awaiting or len(by_id) != len(sidecars):
        raise ValueError("separation sidecars do not exactly cover prepared post-test candidates")

    runtime_config_sha256 = hashlib.sha256(runtime_path.read_bytes()).hexdigest()
    results: list[dict[str, Any] | None] = [None] * len(prepared_rows)
    pending: list[tuple[int, str, dict[str, Any], dict[str, Any], Path, str]] = []
    for index, prepared in enumerate(prepared_rows):
        if prepared.get("status") != "awaiting-separation":
            results[index] = prepared
            continue
        candidate = prepared.get("candidate")
        lane = candidate.get("lane") if isinstance(candidate, dict) else None
        if lane not in V4_LANES:
            raise ValueError(f"{scheduler_label} verifier scheduler requires one of the six frozen lanes")
        identifier = prepared["candidate_id"]
        path = output_dir / f"{identifier}.evidence.json"
        expected_phase2_input = canonical_sha256({
            "prepared_artifact_sha256": prepared["artifact_sha256"],
            "separation_evidence_sha256": by_id[identifier]["evidence_sha256"],
            "runtime_config_sha256": runtime_config_sha256,
            "verifier_scheduler_contract_sha256": scheduler_sha256,
        })
        if path.exists():
            artifact = json.loads(path.read_text(encoding="utf-8"))
            _sealed(artifact, "artifact_sha256")
            scheduler = artifact.get("verifier_scheduler")
            if (
                artifact.get("input_sha256") != prepared["input_sha256"]
                or artifact.get("phase2_input_sha256") != expected_phase2_input
                or scheduler != {
                    "contract": scheduler_contract,
                    "contract_sha256": scheduler_sha256,
                }
            ):
                raise ValueError(f"{identifier}: resumed artifact binds different {scheduler_label} phase-two input")
            results[index] = artifact
        else:
            pending.append((index, lane, prepared, by_id[identifier], path, expected_phase2_input))

    def resume_and_write(
        prepared: dict[str, Any], sidecar: dict[str, Any], path: Path, phase2_input_sha256: str,
    ) -> dict[str, Any]:
        artifact = resume_candidate(prepared, sidecar, runtime_path, verifier_fn)
        artifact["phase2_input_sha256"] = phase2_input_sha256
        artifact["verifier_scheduler"] = {
            "contract": copy.deepcopy(scheduler_contract),
            "contract_sha256": scheduler_sha256,
        }
        artifact.pop("artifact_sha256")
        artifact["artifact_sha256"] = canonical_sha256(artifact)
        _write_json_atomic(path, artifact)
        return artifact

    waiting = list(pending)
    lane_active: Counter[str] = Counter()
    with ThreadPoolExecutor(
        max_workers=scheduler_contract["global_candidate_concurrency"],
        thread_name_prefix=f"repair-delta-{scheduler_label.lower()}-verify",
    ) as executor:
        futures: dict[Any, tuple[int, str]] = {}
        while waiting or futures:
            cursor = 0
            while (
                cursor < len(waiting)
                and len(futures) < scheduler_contract["global_candidate_concurrency"]
            ):
                index, lane, prepared, sidecar, path, expected = waiting[cursor]
                lane_limit = scheduler_contract["lane_candidate_concurrency"].get(
                    lane, scheduler_contract["global_candidate_concurrency"],
                )
                if lane_active[lane] >= lane_limit:
                    cursor += 1
                    continue
                waiting.pop(cursor)
                lane_active[lane] += 1
                future = executor.submit(resume_and_write, prepared, sidecar, path, expected)
                futures[future] = (index, lane)
            if not futures:
                raise RuntimeError(f"{scheduler_label} verifier scheduler could not dispatch a pending lane")
            completed, _ = wait(futures, return_when=FIRST_COMPLETED)
            for future in completed:
                index, lane = futures.pop(future)
                lane_active[lane] -= 1
                results[index] = future.result()

    if any(result is None for result in results):
        raise RuntimeError(f"{scheduler_label} phase two did not produce one artifact per prepared candidate")
    return [result for result in results if result is not None]


def run_resume_resumable_v5(
    prepared_rows: list[dict[str, Any]], sidecars: list[dict[str, Any]],
    output_dir: Path, runtime_path: Path, verifier_fn: VerifierFn = verify,
) -> list[dict[str, Any]]:
    return run_resume_resumable_v4(
        prepared_rows, sidecars, output_dir, runtime_path, verifier_fn,
        scheduler_contract=V5_VERIFIER_SCHEDULER_CONTRACT,
        scheduler_sha256=V5_VERIFIER_SCHEDULER_SHA256,
        scheduler_label="V5",
    )


def enforce_immediate_v4_final_admission(
    artifacts: list[dict[str, Any]], admission_config: dict[str, Any],
    runtime_path: Path, separation_contract_sha256: str,
    preflight_config_path: Path, cohort_binding: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Replace any controller-ready artifact rejected by the exact final validator."""
    if cohort_binding is not None:
        artifacts = canonicalize_v4_terminal_order(artifacts, cohort_binding)
        validate_v4_terminal_accounting(artifacts, cohort_binding)
    final: list[dict[str, Any]] = []
    for artifact in artifacts:
        if artifact.get("status") != "ready-for-admission":
            final.append(artifact)
            continue
        envelope = artifact["envelope"]
        try:
            admitted = validate_envelope(
                envelope, admission_config, runtime_path, separation_contract_sha256,
                V4_CONTRACT_ID, preflight_config_path,
            )
        except (KeyError, TypeError, ValueError) as exc:
            rejection_evidence = copy.deepcopy(envelope["evidence"])
            rejection_evidence["retry_ledger"] = copy.deepcopy(artifact["retry_ledger"])
            rejected = _as_v4_assembly(_terminal(
                envelope["candidate"], envelope["assignment"], "final_admission",
                str(exc), rejection_evidence, artifact["input_sha256"],
            ))
            rejected["phase2_input_sha256"] = artifact.get("phase2_input_sha256")
            rejected["verifier_scheduler"] = copy.deepcopy(artifact.get("verifier_scheduler"))
            rejected.pop("artifact_sha256")
            rejected["artifact_sha256"] = canonical_sha256(rejected)
            final.append(rejected)
            continue
        accepted = copy.deepcopy(artifact)
        accepted["final_admission_sha256"] = canonical_sha256(admitted)
        accepted.pop("artifact_sha256")
        accepted["artifact_sha256"] = canonical_sha256(accepted)
        final.append(accepted)
    if cohort_binding is not None:
        validate_v4_terminal_accounting(final, cohort_binding)
    return final


def enforce_immediate_v5_final_admission(
    artifacts: list[dict[str, Any]], admission_config: dict[str, Any],
    runtime_path: Path, separation_contract_sha256: str,
    preflight_config_path: Path, ordered_candidate_ids: list[str],
) -> list[dict[str, Any]]:
    """Apply the exact V5 validator and preserve canonical cohort order."""
    by_id = {row.get("candidate_id"): row for row in artifacts}
    if len(by_id) != len(artifacts) or set(by_id) != set(ordered_candidate_ids):
        raise ValueError("V5 terminal artifacts do not cover the exact assembled cohort")
    artifacts = [by_id[identifier] for identifier in ordered_candidate_ids]
    final: list[dict[str, Any]] = []
    for artifact in artifacts:
        if artifact.get("status") != "ready-for-admission":
            final.append(artifact)
            continue
        envelope = artifact["envelope"]
        try:
            admitted = validate_envelope(
                envelope, admission_config, runtime_path, separation_contract_sha256,
                V5_CONTRACT_ID, preflight_config_path,
            )
        except (KeyError, TypeError, ValueError) as exc:
            rejection_evidence = copy.deepcopy(envelope["evidence"])
            rejection_evidence["retry_ledger"] = copy.deepcopy(artifact["retry_ledger"])
            rejected = _as_v5_assembly(_terminal(
                envelope["candidate"], envelope["assignment"], "final_admission",
                str(exc), rejection_evidence, artifact["input_sha256"],
            ))
            rejected["phase2_input_sha256"] = artifact.get("phase2_input_sha256")
            rejected["verifier_scheduler"] = copy.deepcopy(artifact.get("verifier_scheduler"))
            rejected.pop("artifact_sha256")
            rejected["artifact_sha256"] = canonical_sha256(rejected)
            final.append(rejected)
            continue
        accepted = copy.deepcopy(artifact)
        accepted["final_admission_sha256"] = canonical_sha256(admitted)
        accepted.pop("artifact_sha256")
        accepted["artifact_sha256"] = canonical_sha256(accepted)
        final.append(accepted)
    return final


def canonicalize_v4_terminal_order(
    artifacts: list[dict[str, Any]], cohort_binding: dict[str, Any],
) -> list[dict[str, Any]]:
    """Reconstruct the canonical queue order after lane-aware concurrent execution."""
    expected = cohort_binding.get("ordered_primary_candidate_ids")
    if not isinstance(expected, list):
        raise ValueError("V4 cohort binding lacks ordered primary candidate IDs")
    by_id = {
        row.get("candidate_id"): row for row in artifacts if isinstance(row, dict)
    }
    if (
        len(by_id) != len(artifacts)
        or len(artifacts) != len(expected)
        or set(by_id) != set(expected)
    ):
        raise ValueError("V4 artifacts cannot be reconstructed as the exact primary cohort")
    return [by_id[identifier] for identifier in expected]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--queue-manifest", type=Path)
    parser.add_argument("--teacher-candidates", type=Path, action="append")
    parser.add_argument("--teacher-evidence", type=Path, action="append")
    parser.add_argument("--cohort", choices=("primary", "reserve"), required=True)
    parser.add_argument("--reserve-eligibility", type=Path)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--training-corpus", type=Path, action="append", required=True)
    parser.add_argument("--evaluation-root", type=Path, action="append", required=True)
    parser.add_argument("--prompt-simhash-max-hamming", type=int, default=3)
    parser.add_argument("--minimum-fuzzy-tokens", type=int, default=12)
    parser.add_argument("--workers", type=int, choices=range(1, 13), default=12)
    parser.add_argument("--contract-version", choices=("v3", "v4", "v5"), default="v3")
    parser.add_argument(
        "--v4-preflight-config", type=Path,
        default=Path("configs/data/gate2_v4_post_teacher_preflight.json"),
    )
    parser.add_argument(
        "--admission-config", type=Path, default=Path("configs/data/expansion_v1.json"),
    )
    parser.add_argument(
        "--tooling-readiness-report", type=Path,
        help="passed production-tooling fixture report; required by --contract-version v4",
    )
    parser.add_argument(
        "--tooling-fixtures", type=Path,
        help="explicit fixture bundle used by the report; omit for the deterministic default bundle",
    )
    parser.add_argument("--v5-candidates", type=Path)
    parser.add_argument("--v5-assignments", type=Path)
    parser.add_argument("--v5-assembly-manifest", type=Path)
    parser.add_argument("--v5-composite-readiness", type=Path)
    parser.add_argument("--v5-semantic-equivalence", type=Path)
    parser.add_argument("--v5-resilience-addendum", type=Path)
    parser.add_argument("--v5-semantic-interruption-carry", type=Path)
    parser.add_argument("--v5-attempt-manifest", type=Path)
    parser.add_argument("--v5-interruption-report", type=Path)
    parser.add_argument("--v5-schema-correction-plan", type=Path)
    parser.add_argument("--v5-schema-correction-manifest", type=Path)
    parser.add_argument("--v5-v2-accounting", type=Path)
    parser.add_argument("--v5-live-schema-smoke", type=Path)
    parser.add_argument("--v5-v3-semantic-carry", type=Path)
    parser.add_argument("--v5-v3-attempt-manifest", type=Path)
    parser.add_argument(
        "--v5-invocation-correction-contract-dir", type=Path,
        help="optional sealed per-stage correction contracts for eligible no-thread/no-response failures",
    )
    parser.add_argument(
        "--v5-preflight-config", type=Path,
        default=Path("configs/data/gate2_v5_interface_preflight.json"),
    )
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    v5_v3_values = {
        "--v5-schema-correction-plan": args.v5_schema_correction_plan,
        "--v5-schema-correction-manifest": args.v5_schema_correction_manifest,
        "--v5-v2-accounting": args.v5_v2_accounting,
        "--v5-live-schema-smoke": args.v5_live_schema_smoke,
        "--v5-v3-semantic-carry": args.v5_v3_semantic_carry,
        "--v5-v3-attempt-manifest": args.v5_v3_attempt_manifest,
    }
    v5_v3_mode = any(value is not None for value in v5_v3_values.values())
    if v5_v3_mode and args.contract_version != "v5":
        parser.error("V5 V3 correction flags require --contract-version v5")
    if v5_v3_mode and args.v5_invocation_correction_contract_dir is not None:
        parser.error("V5 V3 schema correction does not consume prior invocation correction contracts")
    if v5_v3_mode and (
        args.v5_resilience_addendum is not None or args.v5_interruption_report is not None
    ):
        parser.error("V5 V3 schema correction uses sealed V2 accounting, not V2 startup flags")
    if args.contract_version == "v5":
        required_v5 = {
            "--v5-candidates": args.v5_candidates,
            "--v5-assignments": args.v5_assignments,
            "--v5-assembly-manifest": args.v5_assembly_manifest,
            "--v5-composite-readiness": args.v5_composite_readiness,
            "--v5-semantic-equivalence": args.v5_semantic_equivalence,
            "--v5-semantic-interruption-carry": args.v5_semantic_interruption_carry,
            "--v5-attempt-manifest": args.v5_attempt_manifest,
        }
        if v5_v3_mode:
            required_v5.update(v5_v3_values)
        else:
            required_v5.update({
                "--v5-resilience-addendum": args.v5_resilience_addendum,
                "--v5-interruption-report": args.v5_interruption_report,
            })
        missing = [name for name, value in required_v5.items() if value is None]
        if missing:
            parser.error(f"V5 requires {', '.join(missing)}")
        generated, assignments, manifest = load_v5_assembled_inputs(
            args.v5_candidates, args.v5_assignments, args.v5_assembly_manifest,
            args.v5_composite_readiness, args.runtime_config, args.v5_preflight_config,
            controller_binding_superseded_by_resilience=True,
        )
    else:
        required_legacy = {
            "--queue": args.queue, "--queue-manifest": args.queue_manifest,
            "--teacher-candidates": args.teacher_candidates,
            "--teacher-evidence": args.teacher_evidence,
        }
        missing = [name for name, value in required_legacy.items() if value is None]
        if missing:
            parser.error(f"{args.contract_version.upper()} requires {', '.join(missing)}")
        plan_sha256 = V4_PLAN_SHA256 if args.contract_version == "v4" else None
        generated, assignments, manifest = load_campaign_inputs(
            args.queue, args.queue_manifest, args.teacher_candidates, args.teacher_evidence,
            args.cohort, args.reserve_eligibility,
            **({"plan_sha256": plan_sha256, "contract_version": "v4"}
               if plan_sha256 is not None else {}),
        )
    v4_cohort_binding = None
    tooling_readiness_sha256 = None
    if args.contract_version == "v4":
        from scripts.data.run_v4_tooling_fixtures import validate_tooling_readiness_report
        if args.tooling_readiness_report is None:
            parser.error("--tooling-readiness-report is required by --contract-version v4")
        readiness = json.loads(args.tooling_readiness_report.read_text(encoding="utf-8"))
        validate_tooling_readiness_report(
            readiness, args.admission_config, args.runtime_config,
            args.v4_preflight_config, args.tooling_fixtures,
        )
        tooling_readiness_sha256 = readiness["report_sha256"]
        if (
            manifest.get("inputs", {}).get("tooling_readiness_report_sha256")
            != tooling_readiness_sha256
        ):
            raise ValueError("V4 queue is not bound to the validated tooling-readiness report")
        v4_cohort_binding = load_v4_primary_cohort_binding(
            args.queue, args.queue_manifest, args.cohort,
        )
    interrupted_semantics = None
    expected_interrupted_semantics = 3
    if args.contract_version == "v5":
        if v5_v3_mode:
            # Lazy import avoids the validator's intentional use of this
            # module's frozen semantic-partition loader.
            from scripts.data.build_v5_v3_schema_correction_manifests import (
                load_v5_v3_schema_correction_attempt,
            )
            interrupted_semantics = load_v5_v3_schema_correction_attempt(
                correction_plan_path=args.v5_schema_correction_plan,
                correction_manifest_path=args.v5_schema_correction_manifest,
                v2_accounting_path=args.v5_v2_accounting,
                live_smoke_path=args.v5_live_schema_smoke,
                v2_semantic_carry_path=args.v5_semantic_interruption_carry,
                v3_semantic_carry_path=args.v5_v3_semantic_carry,
                v3_attempt_manifest_path=args.v5_v3_attempt_manifest,
                v2_attempt_manifest_path=args.v5_attempt_manifest,
                execution_manifest_path=args.v5_assembly_manifest,
                composite_readiness_path=args.v5_composite_readiness,
                semantic_equivalence_path=args.v5_semantic_equivalence,
                generated_rows=generated, assignments=assignments,
                output_root=args.output_root,
            )
            expected_interrupted_semantics = 5
            if len(interrupted_semantics) != 5:
                raise ValueError("V5 V3 correction validator did not return exactly five semantic carries")
        else:
            from scripts.data.build_v5_resilience_manifests import load_v5_resilience_attempt
            interrupted_semantics = load_v5_resilience_attempt(
                addendum_path=args.v5_resilience_addendum,
                carry_manifest_path=args.v5_semantic_interruption_carry,
                attempt_manifest_path=args.v5_attempt_manifest,
                interruption_report_path=args.v5_interruption_report,
                execution_manifest_path=args.v5_assembly_manifest,
                composite_readiness_path=args.v5_composite_readiness,
                semantic_equivalence_path=args.v5_semantic_equivalence,
                generated_rows=generated, assignments=assignments,
                output_root=args.output_root,
            )
            if len(interrupted_semantics) != 3:
                raise ValueError("V5 resilience validator did not return exactly three semantic carries")
    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    adapters = {
        stage: IsolatedCodexAdapter(
            stage, config, args.codex_bin, args.output_root / "codex-runs", cli_identity,
            args.contract_version,
            args.v5_invocation_correction_contract_dir if args.contract_version == "v5" else None,
        )
        for stage in ("semantic_review", "test_author", "delta_audit")
    }
    if args.contract_version == "v4":
        prepared = run_preparation_resumable_v4(
            generated, assignments, args.output_root / "pre-separation",
            adapters["semantic_review"], adapters["test_author"], adapters["delta_audit"],
            args.runtime_config, args.v4_preflight_config, min(args.workers, 6),
        )
    elif args.contract_version == "v5":
        prepared = run_preparation_resumable_v5(
            generated, assignments, args.output_root / "pre-separation",
            adapters["semantic_review"], adapters["test_author"], adapters["delta_audit"],
            args.runtime_config, args.v5_preflight_config, args.v4_preflight_config,
            args.v5_semantic_equivalence, interrupted_semantics,
            expected_interrupted_semantics, min(args.workers, 6),
        )
    else:
        prepared = run_preparation_resumable(
            generated, assignments, args.output_root / "pre-separation",
            adapters["semantic_review"], adapters["test_author"], adapters["delta_audit"],
            args.workers,
        )
    candidate_path = args.output_root / "post-test-candidates.jsonl"
    candidates = write_post_test_candidates(prepared, candidate_path)
    if not candidates:
        raise ValueError("no post-test candidates remain for global separation")
    report = build_report(
        candidate_path, args.training_corpus, args.evaluation_root,
        args.prompt_simhash_max_hamming, args.minimum_fuzzy_tokens,
    )
    report_path = args.output_root / "global-separation-report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sidecar_path = args.output_root / "separation-sidecars.jsonl"
    sidecars, contract_sha = build_separation_sidecars(report, candidates, sidecar_path)
    if args.contract_version in {"v4", "v5"}:
        resume_interface = (
            run_resume_resumable_v5
            if args.contract_version == "v5" else run_resume_resumable_v4
        )
        final = resume_interface(
            prepared, sidecars, args.output_root / "candidate-evidence", args.runtime_config,
        )
        admission_config = json.loads(args.admission_config.read_text(encoding="utf-8"))
        if args.contract_version == "v4":
            final = enforce_immediate_v4_final_admission(
                final, admission_config, args.runtime_config, contract_sha,
                args.v4_preflight_config, v4_cohort_binding,
            )
        else:
            final = enforce_immediate_v5_final_admission(
                final, admission_config, args.runtime_config, contract_sha,
                args.v5_preflight_config, manifest["ordered_candidate_ids"],
            )
    else:
        final = run_resume_resumable(
            prepared, sidecars, args.output_root / "candidate-evidence", args.runtime_config,
            workers=args.workers,
        )
    envelope_path = args.output_root / "admission-envelopes.jsonl"
    ready = [row["envelope"] for row in final if row.get("status") == "ready-for-admission"]
    envelope_path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in ready))
    terminal_path = args.output_root / "terminal-artifacts.jsonl"
    write_terminal_artifacts(final, terminal_path)
    inventory = {
        "schema_version": CAMPAIGN_SCHEMA,
        "status": "ready-for-admission" if len(ready) == len(final) else "terminal-or-unresolved",
        "cohort": args.cohort, "queue_manifest_sha256": manifest["manifest_sha256"],
        "generated": len(generated), "post_test": len(candidates), "ready": len(ready),
        "terminal_rejected": sum(row.get("status") == "terminal-rejected" for row in final),
        "unresolved": sum(row.get("status") == "unresolved" for row in final),
        "post_test_candidates_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "separation_report_sha256": report["report_sha256"],
        "separation_contract_sha256": contract_sha,
        "separation_sidecars_sha256": hashlib.sha256(sidecar_path.read_bytes()).hexdigest(),
        "admission_envelopes_sha256": hashlib.sha256(envelope_path.read_bytes()).hexdigest(),
        "terminal_artifacts": {
            "path": str(terminal_path), "bytes": terminal_path.stat().st_size,
            "sha256": hashlib.sha256(terminal_path.read_bytes()).hexdigest(),
            "records": len(final),
        },
        "artifact_sha256s": {row["candidate_id"]: row["artifact_sha256"] for row in final},
        "cli_identity": cli_identity,
        "codex_config_sha256": hashlib.sha256(args.codex_config.read_bytes()).hexdigest(),
        "runtime_config_sha256": hashlib.sha256(args.runtime_config.read_bytes()).hexdigest(),
        "contract_id": {
            "v3": CONTRACT_ID, "v4": V4_CONTRACT_ID, "v5": V5_CONTRACT_ID,
        }[args.contract_version],
        "plan_sha256": V4_PLAN_SHA256 if args.contract_version == "v4" else manifest["plan_sha256"],
        "verifier_scheduler": (
            {"contract": V4_VERIFIER_SCHEDULER_CONTRACT,
             "contract_sha256": V4_VERIFIER_SCHEDULER_SHA256}
            if args.contract_version == "v4" else
            {"contract": V5_VERIFIER_SCHEDULER_CONTRACT,
             "contract_sha256": V5_VERIFIER_SCHEDULER_SHA256}
            if args.contract_version == "v5" else None
        ),
        "v4_preflight_config_sha256": (
            hashlib.sha256(args.v4_preflight_config.read_bytes()).hexdigest()
            if args.contract_version == "v4" else None
        ),
        "v5_preflight_config_sha256": (
            hashlib.sha256(args.v5_preflight_config.read_bytes()).hexdigest()
            if args.contract_version == "v5" else None
        ),
        "admission_config_sha256": (
            hashlib.sha256(args.admission_config.read_bytes()).hexdigest()
            if args.contract_version == "v4" else None
        ),
        "tooling_readiness_report_sha256": tooling_readiness_sha256,
        "v5_composite_readiness_report_sha256": (
            json.loads(args.v5_composite_readiness.read_text(encoding="utf-8"))["report_sha256"]
            if args.contract_version == "v5" else None
        ),
        "evaluation_artifacts_read_outside_separation": 0,
    }
    if args.contract_version == "v4":
        inventory["v4_primary_cohort_binding"] = v4_cohort_binding
    inventory["report_sha256"] = canonical_sha256(inventory)
    inventory_path = args.output_root / "two-phase-inventory.json"
    inventory_path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": inventory["status"], "ready": len(ready),
        "separation_contract_sha256": contract_sha,
        "report_sha256": inventory["report_sha256"],
    }, sort_keys=True))
    return 0 if inventory["status"] == "ready-for-admission" else 2


if __name__ == "__main__":
    raise SystemExit(main())
