#!/usr/bin/env python3
"""Build and validate the explicit V5 interrupted-stage carry and attempt manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from typing import Any

from scripts.data.account_v5_interrupted_attempt import (
    CONTRACT_ID, PLAN_SHA256, SCHEMA as INTERRUPTION_SCHEMA,
    validate_completed_semantic,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_repair_delta_evidence import _semantic_evidence
from scripts.data.run_repair_delta_two_phase import load_v5_semantic_dispatch
from scripts.data.build_v5_test_author_fixture_bundle import LANES
from scripts.data.run_v5_test_author_readiness import (
    REPORT_SCHEMA as TEST_AUTHOR_REPORT_SCHEMA,
    _validate_bundle as validate_test_author_bundle,
)


ROOT = Path(__file__).resolve().parents[2]
ADDENDUM_SHA256 = "affd11c63849dade7c7a682d99143578e7b72746291cb7ed0514f3148093c7f9"
CARRY_SCHEMA = "ganesh-mini-gate2-v5-interrupted-semantic-carry-manifest/v1"
ATTEMPT_SCHEMA = "ganesh-mini-gate2-v5-resilient-attempt-manifest/v1"
ATTEMPT_ID = "primary-two-phase-v2"
HISTORICAL_V5_TEST_AUTHOR_SCHEMA_SHA256 = (
    "540c16635f55a452131f9c942924111230fbee1dfc2be4af2bc5b40312ad4fe4"
)
EXPECTED_CARRY_IDS = (
    "cap-v4-associative_aggregation-java-repair-primary",
    "cap-v4-associative_aggregation-javascript-repair-primary",
    "cap-v4-associative_aggregation-rust-repair-primary",
)
BASE_RUNTIME_CODE_PATHS = (
    "scripts/data/generate_v5_typescript_primaries.py",
    "scripts/data/assemble_v5_execution_cohort.py",
    "scripts/data/build_v5_composite_readiness.py",
    "scripts/data/repair_delta_v5_contract.py",
    "scripts/data/summarize_repair_delta_qualification.py",
    "scripts/data/run_repair_delta_two_phase.py",
    "scripts/data/run_repair_delta_evidence.py",
    "scripts/data/repair_delta_v5_preflight.py",
    "scripts/data/run_v5_interface_fixtures.py",
    "scripts/data/run_v5_test_author_readiness.py",
    "scripts/data/admit_repair_delta.py",
    "scripts/verify/sandbox.py",
)
INTENDED_CHANGED_BASE_PATHS = {
    "scripts/data/run_repair_delta_two_phase.py",
    "scripts/data/run_repair_delta_evidence.py",
}
NEW_RESILIENCE_PATHS = (
    "scripts/data/account_v5_interrupted_attempt.py",
    "scripts/data/build_v5_resilience_manifests.py",
)
CONFIG_PATHS = (
    "configs/eval/runtimes.json",
    "configs/data/gate2_v5_interface_preflight.json",
    "configs/data/gate2_v4_post_teacher_preflight.json",
    "configs/data/expansion_v1.json",
    "configs/data/expansion_teacher.json",
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def runtime_bindings(base_readiness: dict[str, Any]) -> dict[str, Any]:
    base_hashes = base_readiness.get("bindings", {}).get("runtime_code_sha256")
    if not isinstance(base_hashes, dict) or set(base_hashes) != set(BASE_RUNTIME_CODE_PATHS):
        raise ValueError("base composite runtime-code inventory differs")
    current = {relative: file_sha256(ROOT / relative) for relative in BASE_RUNTIME_CODE_PATHS}
    changed = {relative for relative in BASE_RUNTIME_CODE_PATHS if current[relative] != base_hashes[relative]}
    if changed != INTENDED_CHANGED_BASE_PATHS:
        raise ValueError("runtime drift exceeds the exact resilience controller/adapter correction")
    return {
        "base_composite_runtime_code_sha256": base_hashes,
        "current_runtime_code_sha256": current,
        "intended_changed_base_paths": sorted(changed),
        "unchanged_base_paths": sorted(set(BASE_RUNTIME_CODE_PATHS) - changed),
        "new_resilience_code_sha256": {
            relative: file_sha256(ROOT / relative) for relative in NEW_RESILIENCE_PATHS
        },
        "config_sha256": {relative: file_sha256(ROOT / relative) for relative in CONFIG_PATHS},
    }


def build(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    if file_sha256(args.addendum) != ADDENDUM_SHA256:
        raise ValueError("V5 resilience addendum hash differs")
    interruption = sealed(args.interruption_report, "report_sha256")
    execution = sealed(args.execution_manifest, "manifest_sha256")
    readiness = sealed(args.composite_readiness, "report_sha256")
    semantic = sealed(args.semantic_equivalence, "manifest_sha256")
    if (
        interruption.get("schema_version") != INTERRUPTION_SCHEMA
        or interruption.get("status") != "interrupted-incomplete-no-candidate-dispositions"
        or interruption.get("contract_id") != CONTRACT_ID
        or interruption.get("plan_sha256") != PLAN_SHA256
        or interruption.get("semantic_review_accounting", {}).get("completed_new_review_artifacts") != 3
        or interruption.get("semantic_review_accounting", {}).get("absent_new_review_artifacts") != 20
        or interruption.get("evaluation_artifacts_read") != 0
        or execution.get("contract_id") != CONTRACT_ID or execution.get("records") != 60
        or execution.get("composite_readiness_report_sha256") != readiness.get("report_sha256")
        or semantic.get("contract_id") != CONTRACT_ID
    ):
        raise ValueError("V5 interruption, execution, or semantic partition differs")
    generated_rows = read_jsonl(args.candidates)
    assignment_rows = read_jsonl(args.assignments)
    assignments = {row.get("id"): row for row in assignment_rows}
    carried_v4, required = load_v5_semantic_dispatch(
        args.semantic_equivalence, generated_rows, assignments,
    )
    generated = {row.get("candidate", {}).get("id"): row.get("candidate") for row in generated_rows}
    if set(EXPECTED_CARRY_IDS) - required or len(carried_v4) != 37 or len(required) != 23:
        raise ValueError("V5 three-artifact carry is outside the frozen 23-review partition")
    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = f"codex-cli {config.get('codex_cli_version')}"
    interruption_rows = {
        row["candidate_id"]: row
        for row in interruption["semantic_review_accounting"]["completed"]
    }
    rows: list[dict[str, Any]] = []
    for identifier in EXPECTED_CARRY_IDS:
        candidate = generated.get(identifier); assignment = assignments.get(identifier)
        if not isinstance(candidate, dict) or not isinstance(assignment, dict):
            raise ValueError("V5 carry candidate or assignment is missing")
        source_path = Path(interruption_rows[identifier]["stage_artifact"]["path"])
        checked = validate_completed_semantic(
            source_path, candidate, assignment, config, cli_identity,
        )
        artifact = sealed(source_path, "artifact_sha256")
        evidence = _semantic_evidence(
            candidate, assignment, dict(artifact["response"]),
            artifact["run"]["run_evidence_sha256"],
        )
        row: dict[str, Any] = {
            "schema_version": "ganesh-mini-gate2-v5-interrupted-semantic-carry/v1",
            "candidate_id": identifier, "cell_id": assignment["cell_id"],
            "ordinal": execution["ordered_candidate_ids"].index(identifier),
            "disposition": "completed-v5-semantic-call-carried-from-interrupted-attempt",
            "source_attempt_id": "primary-two-phase-v1",
            "source_stage_artifact": checked["stage_artifact"],
            "input_sha256": checked["input_sha256"],
            "prompt_sha256": checked["prompt_sha256"],
            "run_evidence_sha256": checked["run_evidence_sha256"],
            "semantic_evidence": evidence,
            "semantic_evidence_sha256": evidence["evidence_sha256"],
            "evaluation_artifacts_read": 0,
        }
        row["carry_row_sha256"] = canonical_sha256(row)
        rows.append(row)
    carry: dict[str, Any] = {
        "schema_version": CARRY_SCHEMA, "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256, "resilience_addendum_sha256": ADDENDUM_SHA256,
        "interruption_report_sha256": interruption["report_sha256"],
        "execution_manifest_sha256": execution["manifest_sha256"],
        "base_composite_readiness_report_sha256": readiness["report_sha256"],
        "semantic_equivalence_manifest_sha256": semantic["manifest_sha256"],
        "source_attempt_id": "primary-two-phase-v1", "target_attempt_id": ATTEMPT_ID,
        "rows": rows, "rows_sha256": canonical_sha256(rows), "records": 3,
        "remaining_new_semantic_calls": 20, "logical_new_semantic_calls_total": 23,
        "evaluation_artifacts_read": 0,
    }
    carry["manifest_sha256"] = canonical_sha256(carry)
    output_root = args.output_root.resolve()
    attempt: dict[str, Any] = {
        "schema_version": ATTEMPT_SCHEMA, "status": "sealed-ready-for-runtime-validation",
        "attempt_id": ATTEMPT_ID, "contract_id": CONTRACT_ID, "plan_sha256": PLAN_SHA256,
        "resilience_addendum_sha256": ADDENDUM_SHA256,
        "interruption_report_sha256": interruption["report_sha256"],
        "semantic_carry_manifest_sha256": carry["manifest_sha256"],
        "execution_manifest_sha256": execution["manifest_sha256"],
        "base_composite_readiness_report_sha256": readiness["report_sha256"],
        "semantic_equivalence_manifest_sha256": semantic["manifest_sha256"],
        "ordered_candidate_ids_sha256": execution["ordered_candidate_ids_sha256"],
        "records": 60, "semantic_accounting": {
            "v4_equivalent": 37, "interrupted_v5_completed": 3,
            "remaining_v5_calls": 20, "total": 60,
        },
        "output_root": str(output_root), "runtime_bindings": runtime_bindings(readiness),
        "readiness_supersession": {
            "base_composite_preserved_as_construction_evidence": True,
            "base_live_runtime_hash_check_superseded_only_for": sorted(INTENDED_CHANGED_BASE_PATHS),
            "unchanged_base_runtime_hashes_required": True,
            "fresh_teacher_evidence_and_execution_cohort_unchanged": True,
        },
        "required_controller_interface": {
            "cli_flags": ["--v5-resilience-addendum", "--v5-semantic-interruption-carry",
                          "--v5-attempt-manifest"],
            "validation_before_model_adapter_construction": True,
            "implicit_old_attempt_directory_scan_forbidden": True,
        },
        "python": platform.python_version(), "evaluation_artifacts_read": 0,
    }
    attempt["manifest_sha256"] = canonical_sha256(attempt)
    return carry, attempt


def load_v5_resilience_attempt(
    *, addendum_path: Path, carry_manifest_path: Path, attempt_manifest_path: Path,
    interruption_report_path: Path, execution_manifest_path: Path,
    composite_readiness_path: Path,
    semantic_equivalence_path: Path, generated_rows: list[dict[str, Any]],
    assignments: dict[str, dict[str, Any]], output_root: Path,
) -> dict[str, dict[str, Any]]:
    """Runtime validator API; return exactly three admission-ready semantic evidence objects."""
    if file_sha256(addendum_path) != ADDENDUM_SHA256:
        raise ValueError("V5 resilience addendum hash differs")
    carry = sealed(carry_manifest_path, "manifest_sha256")
    attempt = sealed(attempt_manifest_path, "manifest_sha256")
    interruption = sealed(interruption_report_path, "report_sha256")
    execution = sealed(execution_manifest_path, "manifest_sha256")
    readiness = sealed(composite_readiness_path, "report_sha256")
    semantic = sealed(semantic_equivalence_path, "manifest_sha256")
    if (
        carry.get("schema_version") != CARRY_SCHEMA or carry.get("records") != 3
        or carry.get("resilience_addendum_sha256") != ADDENDUM_SHA256
        or carry.get("interruption_report_sha256") != interruption.get("report_sha256")
        or carry.get("execution_manifest_sha256") != execution.get("manifest_sha256")
        or carry.get("base_composite_readiness_report_sha256") != readiness.get("report_sha256")
        or carry.get("semantic_equivalence_manifest_sha256") != semantic.get("manifest_sha256")
        or carry.get("target_attempt_id") != ATTEMPT_ID
        or attempt.get("schema_version") != ATTEMPT_SCHEMA
        or attempt.get("status") != "sealed-ready-for-runtime-validation"
        or attempt.get("attempt_id") != ATTEMPT_ID
        or attempt.get("semantic_carry_manifest_sha256") != carry.get("manifest_sha256")
        or attempt.get("execution_manifest_sha256") != execution.get("manifest_sha256")
        or attempt.get("base_composite_readiness_report_sha256") != readiness.get("report_sha256")
        or attempt.get("output_root") != str(output_root.resolve())
        or attempt.get("runtime_bindings") != runtime_bindings(readiness)
        or attempt.get("semantic_accounting") != {
            "v4_equivalent": 37, "interrupted_v5_completed": 3,
            "remaining_v5_calls": 20, "total": 60,
        }
        or attempt.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("V5 resilience carry or attempt manifest differs from runtime")
    generated = {row.get("candidate", {}).get("id"): row.get("candidate") for row in generated_rows}
    _, required = load_v5_semantic_dispatch(
        semantic_equivalence_path, generated_rows, assignments,
    )
    rows = carry.get("rows")
    if (
        not isinstance(rows, list) or len(rows) != 3
        or carry.get("rows_sha256") != canonical_sha256(rows)
        or [row.get("candidate_id") for row in rows] != list(EXPECTED_CARRY_IDS)
    ):
        raise ValueError("V5 semantic carry rows differ from the exact three artifacts")
    output: dict[str, dict[str, Any]] = {}
    for row in rows:
        body = dict(row); claimed = body.pop("carry_row_sha256", None)
        identifier = row.get("candidate_id")
        evidence = row.get("semantic_evidence")
        evidence_body = dict(evidence) if isinstance(evidence, dict) else {}
        evidence_claimed = evidence_body.pop("evidence_sha256", None)
        candidate = generated.get(identifier); assignment = assignments.get(identifier)
        source = row.get("source_stage_artifact", {})
        source_path = Path(source.get("path", ""))
        if (
            claimed != canonical_sha256(body) or identifier not in required
            or not isinstance(candidate, dict) or not isinstance(assignment, dict)
            or row.get("cell_id") != assignment.get("cell_id")
            or row.get("ordinal") != execution["ordered_candidate_ids"].index(identifier)
            or not source_path.is_file() or source.get("sha256") != file_sha256(source_path)
            or evidence_claimed != canonical_sha256(evidence_body)
            or row.get("semantic_evidence_sha256") != evidence_claimed
            or evidence.get("candidate_sha256") != canonical_sha256(candidate)
            or evidence.get("primary_capability") != assignment.get("primary_capability")
            or evidence.get("assigned_cross_cutting_dimension")
            != assignment.get("assigned_cross_cutting_dimension")
            or row.get("evaluation_artifacts_read") != 0 or identifier in output
        ):
            raise ValueError("V5 interrupted semantic carry row is unsealed or candidate-unbound")
        output[identifier] = evidence
    return output


def validate_historical_v5_test_author_readiness_under_resilience(
    report: Any, bundle: dict[str, Any], *, addendum_path: Path,
    carry_manifest_path: Path, attempt_manifest_path: Path,
    interruption_report_path: Path, execution_manifest_path: Path,
    composite_readiness_path: Path, semantic_equivalence_path: Path,
    generated_rows: list[dict[str, Any]], assignments: dict[str, dict[str, Any]],
    output_root: Path,
) -> dict[str, Any]:
    """Validate frozen test-author evidence through the exact V2 drift supersession.

    The historical report remains byte-for-byte construction evidence.  Its
    production-adapter binding is compared with the base hash recorded by the
    sealed resilience attempt, while every other historical binding remains
    current.  The normal resilience loader then proves that the only live base
    runtime drift is the controller and adapter correction allowed by the
    addendum.
    """
    bundle = validate_test_author_bundle(bundle)
    carried = load_v5_resilience_attempt(
        addendum_path=addendum_path,
        carry_manifest_path=carry_manifest_path,
        attempt_manifest_path=attempt_manifest_path,
        interruption_report_path=interruption_report_path,
        execution_manifest_path=execution_manifest_path,
        composite_readiness_path=composite_readiness_path,
        semantic_equivalence_path=semantic_equivalence_path,
        generated_rows=generated_rows,
        assignments=assignments,
        output_root=output_root,
    )
    if tuple(carried) != EXPECTED_CARRY_IDS:
        raise ValueError("V5 resilience validation did not return the exact three semantic carries")
    attempt = sealed(attempt_manifest_path, "manifest_sha256")
    runtime = attempt.get("runtime_bindings", {})
    base_hashes = runtime.get("base_composite_runtime_code_sha256", {})
    current_hashes = runtime.get("current_runtime_code_sha256", {})
    adapter_path = "scripts/data/run_repair_delta_evidence.py"
    runner_path = "scripts/data/run_v5_test_author_readiness.py"
    if not isinstance(report, dict):
        raise ValueError("historical V5 test-author readiness report is missing")
    body = dict(report); claimed = body.pop("report_sha256", None)
    positives = report.get("positive_results")
    negatives = report.get("negative_results")
    coverage = report.get("coverage")
    expected_bindings = {
        "fixture_bundle_sha256": bundle["bundle_sha256"],
        "fixture_builder_sha256": file_sha256(
            ROOT / "scripts/data/build_v5_test_author_fixture_bundle.py"
        ),
        "readiness_runner_sha256": base_hashes.get(runner_path),
        "production_contract_implementation_sha256": base_hashes.get(adapter_path),
        # Historical readiness remains evidence for the schema it actually
        # exercised.  Live V5 invocations separately bind the current schema
        # hash into their input and stage artifact.
        "response_schema_sha256": HISTORICAL_V5_TEST_AUTHOR_SCHEMA_SHA256,
        "positive_results_sha256": canonical_sha256(positives),
        "negative_results_sha256": canonical_sha256(negatives),
    }
    if (
        claimed != canonical_sha256(body)
        or report.get("schema_version") != TEST_AUTHOR_REPORT_SCHEMA
        or report.get("contract_id") != CONTRACT_ID
        or report.get("plan_sha256") != PLAN_SHA256
        or report.get("status") != "passed"
        or report.get("evaluation_artifacts_read") != 0
        or report.get("bindings") != expected_bindings
        or base_hashes.get(runner_path) != current_hashes.get(runner_path)
        or current_hashes.get(runner_path) != file_sha256(ROOT / runner_path)
        or base_hashes.get(adapter_path) == current_hashes.get(adapter_path)
        or current_hashes.get(adapter_path) != file_sha256(ROOT / adapter_path)
        or not isinstance(positives, list) or len(positives) != len(LANES)
        or [row.get("lane") for row in positives] != list(LANES)
        or any(row.get("status") != "passed" for row in positives)
        or not isinstance(negatives, list) or len(negatives) != 4
        or any(row.get("status") != "rejected-as-required" for row in negatives)
        or coverage != {
            "positive_lanes": list(LANES), "positive_count": len(LANES),
            "negative_fixture_ids": [
                "reject-legacy-three-file-array", "reject-java-entrypoint",
                "reject-typescript-node-test-import", "reject-primary-dependent-cross-test",
            ],
            "negative_count": 4, "production_dispatcher_exercised": True,
            "strict_named_role_schema": True,
        }
    ):
        raise ValueError("historical V5 test-author readiness is not covered by resilience")
    return report


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--addendum", type=Path, required=True)
    parser.add_argument("--interruption-report", type=Path, required=True)
    parser.add_argument("--execution-manifest", type=Path, required=True)
    parser.add_argument("--composite-readiness", type=Path, required=True)
    parser.add_argument("--semantic-equivalence", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--assignments", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--carry-output", type=Path, required=True)
    parser.add_argument("--attempt-output", type=Path, required=True)
    args = parser.parse_args(argv)
    carry, attempt = build(args)
    write_json(args.carry_output, carry); write_json(args.attempt_output, attempt)
    print(json.dumps({"carry_manifest_sha256": carry["manifest_sha256"],
                      "attempt_manifest_sha256": attempt["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
