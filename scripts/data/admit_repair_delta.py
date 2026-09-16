#!/usr/bin/env python3
"""Fail-closed admission for the v3 repair-delta qualification lane.

The program consumes already-authored and already-executed training-only
evidence.  It never reads evaluation artifacts and never executes candidate
code.  Semantic evidence is independently sealed and explicitly proves that
the reviewer could not see the teacher proof or executable evidence.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_expansion import AdmissionFailure, canonical_json, read_jsonl, validate_candidate  # noqa: E402
from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.eval.contracts import sha256_object, sha256_text  # noqa: E402
from scripts.verify.sandbox import SANDBOX_CONTRACT  # noqa: E402


CONTRACT_ID = "capability-stratified-v3-repair-delta/v1"
ENVELOPE_SCHEMA = "ganesh-mini-repair-delta-envelope/v1"
OUTPUT_SCHEMA = "ganesh-mini-repair-delta-admitted/v1"
REPORT_SCHEMA = "ganesh-mini-repair-delta-admission-report/v1"
ASSEMBLY_SCHEMA = "ganesh-mini-repair-delta-evidence-assembly/v1"
EVIDENCE_NAMES = {
    "teacher_proof", "semantic_review", "test_author", "delta_audit",
    "separation", "executable", "lineage",
}
SEMANTIC_BOOLEANS = (
    "repair_delta_requires_primary_capability",
    "scheduled_dimension_is_concrete_and_secondary",
    "known_bad_already_satisfies_scheduled_dimension",
    "cross_dimension_only_patch_cannot_solve",
    "capability_remains_substantive_without_cross_clause",
    "generic_boilerplate_is_not_primary",
)
PROOF_BOOLEAN_OVERLAP = (
    "known_bad_already_satisfies_scheduled_dimension",
    "cross_dimension_only_patch_cannot_solve",
    "capability_remains_substantive_without_cross_clause",
)
SEPARATION_PASSES = (
    "exact_training_passed", "normalized_training_passed", "fuzzy_training_passed",
    "exact_evaluation_passed", "normalized_evaluation_passed", "fuzzy_evaluation_passed",
)


class UnresolvedEvidence(AdmissionFailure):
    """Infrastructure evidence that requires the one allowed identical replay."""


def validate_retry_ledger(value: Any, candidate_sha256: str, unresolved: bool) -> dict[str, Any]:
    """Validate the bounded identical-replay ledger emitted by evidence assembly."""
    if not isinstance(value, dict):
        raise AdmissionFailure("retry ledger is missing")
    body = dict(value)
    claimed = body.pop("ledger_sha256", None)
    attempts = value.get("attempts")
    if (
        claimed != canonical_sha256(body)
        or value.get("schema_version") != "ganesh-mini-repair-delta-retry-ledger/v1"
        or value.get("candidate_sha256") != candidate_sha256
        or value.get("maximum_attempts") != 2
        or value.get("unresolved") is not unresolved
        or value.get("evaluation_artifacts_read") != 0
        or not isinstance(attempts, list) or len(attempts) != 4
    ):
        raise AdmissionFailure("retry ledger is unsealed or unbound")
    expected = {
        (implementation, role)
        for implementation in ("reference", "known_bad")
        for role in ("primary_discrimination", "cross_cutting")
    }
    observed: set[tuple[str, str]] = set()
    unresolved_rows = 0
    for row in attempts:
        if not isinstance(row, dict):
            raise AdmissionFailure("retry ledger attempt row is malformed")
        key = (row.get("implementation"), row.get("role"))
        runs = row.get("attempts")
        if key not in expected or key in observed or not isinstance(runs, list) or not 1 <= len(runs) <= 2:
            raise AdmissionFailure("retry ledger attempt coverage is malformed")
        observed.add(key)
        for index, run in enumerate(runs, 1):
            if (
                not isinstance(run, dict) or run.get("attempt") != index
                or not isinstance(run.get("result"), dict)
                or run.get("classification") is not None
                and not isinstance(run.get("classification"), str)
            ):
                raise AdmissionFailure("retry ledger run is malformed")
        final_unresolved = runs[-1].get("classification") is not None
        if final_unresolved and len(runs) != 2:
            raise AdmissionFailure("unresolved execution lacks its one identical replay")
        unresolved_rows += int(final_unresolved)
    if observed != expected or bool(unresolved_rows) is not unresolved:
        raise AdmissionFailure("retry ledger unresolved state is inconsistent")
    return value


def validate_assembly_artifact(value: Any) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
    """Return disposition, optional envelope, and a content-free disposition row."""
    if not isinstance(value, dict) or value.get("schema_version") != ASSEMBLY_SCHEMA:
        raise AdmissionFailure("unsupported repair-delta evidence assembly artifact")
    body = dict(value)
    claimed = body.pop("artifact_sha256", None)
    status = value.get("status")
    identifier = value.get("candidate_id")
    if (
        claimed != canonical_sha256(body) or status not in {
            "ready-for-admission", "terminal-rejected", "unresolved",
        }
        or not isinstance(identifier, str) or not identifier
        or value.get("evaluation_artifacts_read") != 0
        or _sha(value.get("input_sha256"), "assembly input") != value.get("input_sha256")
    ):
        raise AdmissionFailure("evidence assembly artifact is unsealed or malformed")
    if status == "ready-for-admission":
        envelope = value.get("envelope")
        if not isinstance(envelope, dict) or envelope.get("candidate", {}).get("id") != identifier:
            raise AdmissionFailure("ready artifact does not bind its candidate envelope")
        candidate_sha = canonical_sha256(envelope["candidate"])
        ledger = validate_retry_ledger(value.get("retry_ledger"), candidate_sha, False)
        executable = envelope.get("evidence", {}).get("executable", {})
        if executable.get("retry_ledger_sha256") != ledger["ledger_sha256"]:
            raise AdmissionFailure("executable evidence does not bind the retry ledger")
        return "ready", envelope, {"id": identifier}
    evidence = value.get("evidence")
    cell = value.get("cell_id")
    stage = value.get("terminal_stage")
    reason = value.get("reason")
    if (
        not isinstance(evidence, dict) or not evidence
        or not isinstance(cell, str) or not cell
        or not isinstance(stage, str) or not stage
        or not isinstance(reason, str) or not reason
    ):
        raise AdmissionFailure("terminal artifact lacks its bound disposition evidence")
    for name, item in evidence.items():
        if name != "retry_ledger":
            _sealed(item, name)
    if status == "unresolved":
        executable = evidence.get("executable")
        if not isinstance(executable, dict):
            raise AdmissionFailure("unresolved artifact lacks executable evidence")
        ledger = validate_retry_ledger(evidence.get("retry_ledger"), executable.get("candidate_sha256"), True)
        if executable.get("retry_ledger_sha256") != ledger["ledger_sha256"]:
            raise AdmissionFailure("unresolved executable does not bind the retry ledger")
    elif "retry_ledger" in evidence:
        raise AdmissionFailure("terminal semantic rejection unexpectedly contains a retry ledger")
    return status, None, {"id": identifier, "cell_id": cell, "terminal_stage": stage, "reason": reason}


def _sha(value: Any, where: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise AdmissionFailure(f"{where}: expected lowercase SHA-256")
    return value


def _sealed(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AdmissionFailure(f"{where}: expected sealed object")
    body = dict(value)
    claimed = body.pop("evidence_sha256", None)
    if claimed != canonical_sha256(body):
        raise AdmissionFailure(f"{where}: evidence seal mismatch")
    return value


def _runtime(runtime_path: Path, candidate: dict[str, Any]) -> tuple[dict[str, Any], str]:
    payload = runtime_path.read_bytes()
    document = json.loads(payload)
    task = candidate["verification_task"]
    runtime = document.get("runtimes", {}).get(task["runtime_id"]) if isinstance(document, dict) else None
    if (
        document.get("schema_version") != "3.0"
        or document.get("platform") != "linux/amd64"
        or not isinstance(runtime, dict)
        or runtime.get("language") != candidate["lane"]
        or runtime.get("candidate_path") != task["candidate_path"]
        or runtime.get("platform") != "linux/amd64"
    ):
        raise AdmissionFailure("runtime config does not bind the candidate lane and path")
    return runtime, hashlib.sha256(payload).hexdigest()


def _visibility(evidence: dict[str, Any], expected: dict[str, Any], where: str) -> None:
    visibility = evidence.get("visibility")
    if not isinstance(visibility, dict) or visibility != expected:
        raise AdmissionFailure(f"{where}: visibility contract mismatch")


def _test_roles(candidate: dict[str, Any], evidence: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    rows = evidence.get("test_roles")
    if not isinstance(rows, list):
        raise AdmissionFailure("test_author.test_roles must be an array")
    tests = {
        item["path"]: item for item in candidate["verification_task"]["files"]
        if item.get("role") == "test"
    }
    by_role: dict[str, list[dict[str, Any]]] = {"primary_discrimination": [], "cross_cutting": []}
    seen_paths: set[str] = set()
    seen_cases: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "path", "file_sha256", "role", "case_ids", "valid_domain_only", "scheduled_dimension_only",
        }:
            raise AdmissionFailure("test role entry differs from the frozen contract")
        role = row.get("role")
        path = row.get("path")
        cases = row.get("case_ids")
        if (
            role not in by_role or path not in tests or path in seen_paths
            or row.get("file_sha256") != tests[path]["sha256"]
            or not isinstance(cases, list) or not cases
            or len(set(cases)) != len(cases)
            or any(not isinstance(case, str) or not case or case in seen_cases for case in cases)
        ):
            raise AdmissionFailure("test roles do not bind unique hashed test files and cases")
        if role == "primary_discrimination" and (
            row.get("valid_domain_only") is not True or row.get("scheduled_dimension_only") is not False
        ):
            raise AdmissionFailure("primary-discrimination cases must be valid-domain and capability-specific")
        if role == "cross_cutting" and (
            row.get("valid_domain_only") is not False or row.get("scheduled_dimension_only") is not True
        ):
            raise AdmissionFailure("cross-cutting cases must isolate the scheduled dimension")
        seen_paths.add(path)
        seen_cases.update(cases)
        by_role[role].append(row)
    if seen_paths != set(tests):
        raise AdmissionFailure("every executable test file must have exactly one logical role")
    if sum(len(row["case_ids"]) for row in by_role["primary_discrimination"]) < 2:
        raise AdmissionFailure("at least two primary-discrimination cases are required")
    if sum(len(row["case_ids"]) for row in by_role["cross_cutting"]) < 1:
        raise AdmissionFailure("at least one cross-cutting case is required")
    return by_role


def suite_sha256(candidate: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    task = candidate["verification_task"]
    return canonical_sha256({
        "candidate_id": candidate["id"], "runtime_id": task["runtime_id"],
        "candidate_path": task["candidate_path"], "limits": task["limits"],
        "files": [{"path": row["path"], "sha256": row["file_sha256"]} for row in rows],
    })


def teacher_candidate_sha256(candidate: dict[str, Any]) -> str:
    """Reconstruct the candidate boundary before independent tests were added."""
    pretest = copy.deepcopy(candidate)
    pretest["verification_task"]["files"] = [
        item for item in pretest["verification_task"]["files"] if item.get("role") != "test"
    ]
    return canonical_sha256(pretest)


def _execution_result(
    result: Any, expected_suite_sha256: str, runtime: dict[str, Any], limits_sha256: str,
    expected_runtime_id: str, should_pass: bool, where: str,
) -> None:
    expected_image = f"{str(runtime['image']).rsplit(':', 1)[0]}@{runtime['manifest_digest']}"
    if (
        not isinstance(result, dict)
        or result.get("suite_sha256") != expected_suite_sha256
        or result.get("runtime_id") != expected_runtime_id
        or result.get("image") != expected_image
        or result.get("image_id") != runtime.get("image_id")
        or result.get("manifest_digest") != runtime.get("manifest_digest")
        or result.get("sandbox_contract_sha256") != sha256_object(SANDBOX_CONTRACT)
        or result.get("limits_sha256") != limits_sha256
        or not isinstance(result.get("exit_codes"), list)
    ):
        raise AdmissionFailure(f"{where}: executable evidence binding mismatch or infrastructure failure")
    if result.get("timed_out") is True or not result["exit_codes"]:
        raise UnresolvedEvidence(f"{where}: unresolved verifier infrastructure evidence")
    if result.get("timed_out") is not False:
        raise AdmissionFailure(f"{where}: timed_out must be explicit")
    passed = all(code == 0 for code in result["exit_codes"])
    if passed is not should_pass:
        expectation = "pass" if should_pass else "fail"
        raise AdmissionFailure(f"{where}: suite must {expectation}")


def validate_envelope(
    envelope: Any, admission_config: dict[str, Any], runtime_path: Path,
    separation_contract_sha256: str,
) -> dict[str, Any]:
    if not isinstance(envelope, dict) or envelope.get("schema_version") != ENVELOPE_SCHEMA:
        raise AdmissionFailure("unsupported repair-delta envelope")
    candidate = envelope.get("candidate")
    assignment = envelope.get("assignment")
    if not isinstance(candidate, dict) or not isinstance(assignment, dict):
        raise AdmissionFailure("candidate and assignment are required")
    validate_candidate(candidate, admission_config)
    if candidate["task_type"] != "repair" or candidate["verification_task"]["task_type"] != "repair":
        raise AdmissionFailure("v3 repair-delta lane accepts repair candidates only")
    primary = assignment.get("primary_capability")
    dimension = assignment.get("assigned_cross_cutting_dimension")
    if (
        assignment.get("contract_id") != CONTRACT_ID
        or assignment.get("cell_id") != f"{primary}/{candidate['lane']}/repair"
        or not isinstance(primary, str) or not primary
        or not isinstance(dimension, str) or not dimension
    ):
        raise AdmissionFailure("assignment does not bind the v3 repair cell")
    candidate_sha = canonical_sha256(candidate)
    specification_sha = sha256_text(candidate["messages"][0]["content"])
    validation = candidate["verification_task"]["validation"]
    if len(validation["known_bad"]) != 1:
        raise AdmissionFailure("repair-delta candidate requires exactly one known-bad implementation")
    reference_sha = validation["reference"]["sha256"]
    known_bad_sha = validation["known_bad"][0]["sha256"]
    evidence = envelope.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != EVIDENCE_NAMES:
        raise AdmissionFailure("repair-delta evidence set is incomplete")
    sealed = {name: _sealed(evidence[name], name) for name in EVIDENCE_NAMES}
    for name, item in sealed.items():
        if name == "teacher_proof":
            continue
        if item.get("candidate_sha256") != candidate_sha:
            raise AdmissionFailure(f"{name}: candidate hash mismatch")

    proof = sealed["teacher_proof"]
    if (
        proof.get("candidate_id") != candidate["id"]
        or proof.get("teacher_candidate_sha256") != teacher_candidate_sha256(candidate)
        or proof.get("primary_capability") != primary
        or proof.get("assigned_cross_cutting_dimension") != dimension
    ):
        raise AdmissionFailure("teacher proof does not bind the assigned capability and dimension")
    for field in (
        "capability_operation", "defective_intermediate_or_decision", "valid_domain_counterexample",
        "minimal_capability_specific_patch", "scheduled_dimension_obligation",
    ):
        if not isinstance(proof.get(field), str) or not proof[field].strip():
            raise AdmissionFailure(f"teacher_proof.{field}: non-empty structural proof is required")
    for field in PROOF_BOOLEAN_OVERLAP:
        if type(proof.get(field)) is not bool:
            raise AdmissionFailure(f"teacher_proof.{field}: boolean required")

    semantic = sealed["semantic_review"]
    if (
        semantic.get("specification_sha256") != specification_sha
        or semantic.get("known_bad_sha256") != known_bad_sha
        or semantic.get("primary_capability") != primary
        or semantic.get("assigned_cross_cutting_dimension") != dimension
        or any(semantic.get(field) is not True for field in SEMANTIC_BOOLEANS)
    ):
        raise AdmissionFailure("blind semantic review did not independently pass every measured boolean")
    _visibility(semantic, {
        "specification_visible": True, "embedded_known_bad_visible": True,
        "assigned_labels_visible": True, "teacher_proof_visible": False,
        "reference_visible": False, "tests_visible": False, "verifier_outputs_visible": False,
        "training_stimulus_visible": False, "source_dataset_visible": False,
        "v2_outcomes_visible": False, "evaluation_artifacts_read": 0,
    }, "semantic_review")
    if any(semantic[field] is not proof[field] for field in PROOF_BOOLEAN_OVERLAP):
        raise AdmissionFailure("deterministic proof-consistency check found a semantic/proof disagreement")

    test_author = sealed["test_author"]
    if (
        test_author.get("specification_sha256") != specification_sha
        or test_author.get("known_bad_sha256") != known_bad_sha
        or test_author.get("primary_capability") != primary
        or test_author.get("assigned_cross_cutting_dimension") != dimension
    ):
        raise AdmissionFailure("test-author evidence does not bind specification and embedded known-bad")
    _visibility(test_author, {
        "specification_visible": True, "embedded_known_bad_visible": True,
        "capability_definition_visible": True, "scheduled_dimension_visible": True,
        "reference_visible": False, "teacher_proof_visible": False,
        "semantic_review_visible": False, "verifier_outputs_visible": False,
        "evaluation_artifacts_read": 0,
    }, "test_author")
    roles = _test_roles(candidate, test_author)

    delta = sealed["delta_audit"]
    if (
        delta.get("specification_sha256") != specification_sha
        or delta.get("reference_sha256") != reference_sha
        or delta.get("known_bad_sha256") != known_bad_sha
        or delta.get("primary_capability") != primary
        or delta.get("assigned_cross_cutting_dimension") != dimension
        or delta.get("independent_semantic_delta_count") != 1
        or delta.get("delta_is_capability_specific") is not True
        or delta.get("introduces_multiple_independent_fixes") is not False
        or not isinstance(delta.get("delta_description"), str) or not delta["delta_description"].strip()
    ):
        raise AdmissionFailure("delta auditor did not confirm exactly one capability-specific bug")
    _visibility(delta, {
        "specification_visible": True, "embedded_known_bad_visible": True,
        "reference_visible": True, "assigned_labels_visible": True,
        "tests_visible": False, "verifier_outputs_visible": False,
        "teacher_proof_visible": False, "training_stimulus_visible": False,
        "v2_outcomes_visible": False, "evaluation_artifacts_read": 0,
    }, "delta_audit")

    separation = sealed["separation"]
    _sha(separation_contract_sha256, "separation contract")
    if (
        separation.get("comparison_contract_sha256") != separation_contract_sha256
        or not isinstance(separation.get("comparison_manifest_sha256"), str)
        or len(separation["comparison_manifest_sha256"]) != 64
        or any(char not in "0123456789abcdef" for char in separation["comparison_manifest_sha256"])
        or any(separation.get(field) is not True for field in SEPARATION_PASSES)
        or separation.get("evaluation_artifacts_read_by_construction") != 0
    ):
        raise AdmissionFailure("unchanged content-free separation contract did not pass")

    runtime, runtime_config_sha = _runtime(runtime_path, candidate)
    executable = sealed["executable"]
    task = candidate["verification_task"]
    limits_sha = canonical_sha256(task["limits"])
    if (
        executable.get("runtime_config_sha256") != runtime_config_sha
        or executable.get("reference_sha256") != reference_sha
        or executable.get("known_bad_sha256") != known_bad_sha
        or executable.get("sandbox_contract_sha256") != sha256_object(SANDBOX_CONTRACT)
    ):
        raise AdmissionFailure("executable evidence does not bind the unchanged runtime and sandbox")
    results = executable.get("results")
    if not isinstance(results, dict) or set(results) != {"reference", "known_bad"}:
        raise AdmissionFailure("executable suite results are incomplete")
    for implementation, should_primary_pass, should_cross_pass in (
        ("reference", True, True), ("known_bad", False, True),
    ):
        suites = results.get(implementation)
        if not isinstance(suites, dict) or set(suites) != {"primary_discrimination", "cross_cutting"}:
            raise AdmissionFailure(f"{implementation}: split suite evidence is incomplete")
        _execution_result(
            suites["primary_discrimination"], suite_sha256(candidate, roles["primary_discrimination"]),
            runtime, limits_sha, task["runtime_id"], should_primary_pass, f"{implementation}.primary_discrimination",
        )
        _execution_result(
            suites["cross_cutting"], suite_sha256(candidate, roles["cross_cutting"]),
            runtime, limits_sha, task["runtime_id"], should_cross_pass, f"{implementation}.cross_cutting",
        )

    lineage = sealed["lineage"]
    source = candidate["source"]
    if (
        lineage.get("source_identity") != {key: source.get(key) for key in ("dataset", "revision", "record_id")}
        or lineage.get("contract_id") != CONTRACT_ID
        or lineage.get("cell_id") != assignment["cell_id"]
        or lineage.get("source_record_sha256") != source.get("source_record_sha256")
        or lineage.get("complete") is not True
        or lineage.get("teacher_proof_evidence_sha256") != proof["evidence_sha256"]
        or lineage.get("semantic_review_evidence_sha256") != semantic["evidence_sha256"]
        or lineage.get("test_author_evidence_sha256") != test_author["evidence_sha256"]
        or lineage.get("delta_audit_evidence_sha256") != delta["evidence_sha256"]
        or lineage.get("separation_evidence_sha256") != separation["evidence_sha256"]
        or lineage.get("executable_evidence_sha256") != executable["evidence_sha256"]
    ):
        raise AdmissionFailure("lineage evidence chain is incomplete or mismatched")
    return {
        "schema_version": OUTPUT_SCHEMA, "id": candidate["id"], "cell_id": assignment["cell_id"],
        "lane": candidate["lane"], "primary_capability": primary,
        "assigned_cross_cutting_dimension": dimension, "candidate": candidate,
        "evidence_sha256s": {name: sealed[name]["evidence_sha256"] for name in sorted(sealed)},
        "proof_consistency_sha256": canonical_sha256({
            field: {"teacher": proof[field], "reviewer": semantic[field]}
            for field in PROOF_BOOLEAN_OVERLAP
        }),
    }


def admit(
    envelopes: list[Any], admission_config: dict[str, Any], runtime_path: Path,
    separation_contract_sha256: str, unresolved: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    admitted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line, input_row in enumerate(envelopes, 1):
        identifier = input_row.get("candidate_id", input_row.get("candidate", {}).get("id", f"line-{line}")) if isinstance(input_row, dict) else f"line-{line}"
        try:
            envelope = input_row
            measured: dict[str, Any] | None = None
            if isinstance(input_row, dict) and input_row.get("schema_version") == ASSEMBLY_SCHEMA:
                disposition, envelope, measured = validate_assembly_artifact(input_row)
                if identifier in seen:
                    raise AdmissionFailure("duplicate repair-delta candidate ID")
                seen.add(identifier)
                if disposition == "terminal-rejected":
                    rejected.append({"line": line, **measured})
                    continue
                if disposition == "unresolved":
                    if unresolved is None:
                        raise UnresolvedEvidence(measured["reason"])
                    unresolved.append({"line": line, **measured})
                    continue
                if envelope is None:
                    raise AdmissionFailure("ready evidence assembly artifact lacks an envelope")
            row = validate_envelope(envelope, admission_config, runtime_path, separation_contract_sha256)
            if measured is None and row["id"] in seen:
                raise AdmissionFailure("duplicate repair-delta candidate ID")
            if measured is None:
                seen.add(row["id"])
            admitted.append(row)
        except UnresolvedEvidence as exc:
            if unresolved is None:
                raise
            unresolved.append({"line": line, "id": identifier, "reason": str(exc)})
        except (AdmissionFailure, KeyError, TypeError, ValueError) as exc:
            rejected.append({"line": line, "id": identifier, "reason": str(exc)})
    return admitted, rejected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("configs/data/expansion_v1.json"))
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--separation-contract-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rejected-output", type=Path, required=True)
    parser.add_argument("--unresolved-output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    rows = read_jsonl(args.input)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    unresolved: list[dict[str, Any]] = []
    admitted, rejected = admit(
        rows, config, args.runtime_config, args.separation_contract_sha256, unresolved,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(b"".join(canonical_json(row) + b"\n" for row in admitted))
    args.rejected_output.parent.mkdir(parents=True, exist_ok=True)
    args.rejected_output.write_text(json.dumps(rejected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.unresolved_output.parent.mkdir(parents=True, exist_ok=True)
    args.unresolved_output.write_text(json.dumps(unresolved, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA,
        "status": "admission-complete" if not rejected and not unresolved else "failed",
        "contract_id": CONTRACT_ID,
        "input": {"path": str(args.input), "bytes": args.input.stat().st_size, "sha256": hashlib.sha256(args.input.read_bytes()).hexdigest()},
        "runtime_config_sha256": hashlib.sha256(args.runtime_config.read_bytes()).hexdigest(),
        "admission_config_sha256": hashlib.sha256(args.config.read_bytes()).hexdigest(),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        "separation_contract_sha256": args.separation_contract_sha256,
        "accepted": len(admitted), "rejected": len(rejected), "unresolved": len(unresolved),
        "counts_by_lane": dict(sorted(Counter(row["lane"] for row in admitted).items())),
        "evaluation_artifacts_read": 0,
        "outputs": {
            "admitted": {"path": str(args.output), "bytes": args.output.stat().st_size, "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()},
            "rejected": {"path": str(args.rejected_output), "bytes": args.rejected_output.stat().st_size, "sha256": hashlib.sha256(args.rejected_output.read_bytes()).hexdigest()},
            "unresolved": {"path": str(args.unresolved_output), "bytes": args.unresolved_output.stat().st_size, "sha256": hashlib.sha256(args.unresolved_output.read_bytes()).hexdigest()},
        },
    }
    report["report_sha256"] = canonical_sha256(report)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "accepted": len(admitted), "rejected": len(rejected), "unresolved": len(unresolved)}, sort_keys=True))
    return 0 if not rejected and not unresolved else 1


if __name__ == "__main__":
    raise SystemExit(main())
