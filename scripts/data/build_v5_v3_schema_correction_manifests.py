#!/usr/bin/env python3
"""Build and validate V5 V3 schema-correction, carry, and attempt manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from typing import Any

from scripts.data.account_v5_interrupted_attempt import CONTRACT_ID, PLAN_SHA256, validate_completed_semantic
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v5_resilience_manifests import EXPECTED_CARRY_IDS as V1_CARRY_IDS
from scripts.data.run_repair_delta_evidence import _response_schema, _semantic_evidence
from scripts.data.run_repair_delta_two_phase import load_v5_semantic_dispatch
from scripts.data.run_v5_live_schema_admission_smoke import validate_v5_live_schema_admission_smoke_report


ROOT = Path(__file__).resolve().parents[2]
ATTEMPT_ID = "primary-two-phase-v3"
CORRECTION_PLAN_SHA256 = "cda98c216d473513e312c41463bdc2a67457c506761d7339444668686be4b36f"
V2_ACCOUNTING_SEAL = "4d739a334ce3df4cc9feca6fbbbe291d93f53a1d896fb457f8caba93720d5c69"
LIVE_SMOKE_SEAL = "5fbb4f0551f42742b31b99ddf19a5e07dce2df69d7cf405c1d3daa8a7b0f230d"
SCHEMA_SHA256 = "e099481a27e5d40923778098eb3c02126ca40e0116565bcd8a224396baf077cc"
CORRECTION_SCHEMA = "ganesh-mini-gate2-v5-schema-correction-manifest/v1"
CARRY_SCHEMA = "ganesh-mini-gate2-v5-v2-semantic-carry-manifest/v1"
ATTEMPT_SCHEMA = "ganesh-mini-gate2-v5-v3-attempt-manifest/v1"
FROZEN_ATTEMPT_SEAL = "b8013bcf65b0b520347c682fcf83e933a9bc9d89ee77f8ea5407aa13e885303a"
FROZEN_RUNTIME_BINDINGS_SHA256 = "5b7bf7e36af9df3634295817031ebc06d2bdabb8ec1219adf1add3444a2fb0fc"
EXPECTED_CARRY_IDS = (
    "cap-v4-binary_and_bitwise-javascript-repair-primary",
    "cap-v4-binary_and_bitwise-rust-repair-primary",
)
EXPECTED_ALL_V5_CARRY_IDS = V1_CARRY_IDS + EXPECTED_CARRY_IDS
NEW_RUNTIME_PATHS = (
    "scripts/data/account_v5_interrupted_attempt.py",
    "scripts/data/account_v5_interrupted_v2.py",
    "scripts/data/build_v5_resilience_manifests.py",
    "scripts/data/build_v5_v3_schema_correction_manifests.py",
    "scripts/data/run_v5_live_schema_admission_smoke.py",
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def runtime_bindings(v2_attempt: dict[str, Any]) -> dict[str, Any]:
    base = v2_attempt.get("runtime_bindings", {}).get("current_runtime_code_sha256")
    if not isinstance(base, dict) or not base:
        raise ValueError("V2 attempt runtime bindings are missing")
    current = {relative: file_sha256(ROOT / relative) for relative in base}
    changed = {relative for relative in base if current[relative] != base[relative]}
    allowed = {
        "scripts/data/run_repair_delta_evidence.py",
        "scripts/data/run_repair_delta_two_phase.py",
    }
    if not changed or not changed <= allowed or "scripts/data/run_repair_delta_evidence.py" not in changed:
        raise ValueError("V3 runtime drift is not the narrow schema correction/controller integration")
    return {
        "v2_runtime_code_sha256": base,
        "current_runtime_code_sha256": current,
        "intended_changed_v2_paths": sorted(changed),
        "unchanged_v2_paths": sorted(set(base) - changed),
        "new_v3_runtime_code_sha256": {relative: file_sha256(ROOT / relative) for relative in NEW_RUNTIME_PATHS},
    }


def validate_frozen_runtime_bindings(attempt: dict[str, Any]) -> None:
    """Validate the terminal V3 runtime record without coupling it to successors.

    V3's exact runtime bytes and their binding map are immutable evidence covered
    by the frozen attempt seal.  Later campaigns legitimately evolve the shared
    adapter, so historical carry revalidation must authenticate that sealed map,
    not require the working-tree adapter to remain byte-identical forever.
    """
    bindings = attempt.get("runtime_bindings")
    if (
        attempt.get("manifest_sha256") != FROZEN_ATTEMPT_SEAL
        or not isinstance(bindings, dict)
        or canonical_sha256(bindings) != FROZEN_RUNTIME_BINDINGS_SHA256
    ):
        raise ValueError("V3 frozen runtime bindings are invalid")


def validate_carry_rows(
    rows: Any, expected_ids: tuple[str, ...], execution: dict[str, Any],
    generated: dict[str, dict[str, Any]], assignments: dict[str, dict[str, Any]],
    config: dict[str, Any], cli_identity: str,
) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list) or [row.get("candidate_id") for row in rows] != list(expected_ids):
        raise ValueError("V3 semantic carry IDs or order differ")
    output: dict[str, dict[str, Any]] = {}
    for row in rows:
        body = dict(row); claimed = body.pop("carry_row_sha256", None)
        identifier = row.get("candidate_id")
        evidence = row.get("semantic_evidence")
        evidence_body = dict(evidence) if isinstance(evidence, dict) else {}
        evidence_claimed = evidence_body.pop("evidence_sha256", None)
        assignment = assignments.get(identifier)
        candidate = generated.get(identifier)
        source = row.get("source_stage_artifact", {})
        source_path = Path(source.get("path", ""))
        checked = (
            validate_completed_semantic(source_path, candidate, assignment, config, cli_identity)
            if source_path.is_file() and isinstance(candidate, dict) and isinstance(assignment, dict)
            else None
        )
        if (
            claimed != canonical_sha256(body)
            or not isinstance(assignment, dict)
            or not isinstance(candidate, dict)
            or identifier in output
            or row.get("cell_id") != assignment.get("cell_id")
            or row.get("ordinal") != execution["ordered_candidate_ids"].index(identifier)
            or not source_path.is_file()
            or source.get("sha256") != file_sha256(source_path)
            or not isinstance(checked, dict)
            or checked.get("stage_artifact") != source
            or checked.get("input_sha256") != row.get("input_sha256")
            or checked.get("prompt_sha256") != row.get("prompt_sha256")
            or checked.get("run_evidence_sha256") != row.get("run_evidence_sha256")
            or evidence_claimed != canonical_sha256(evidence_body)
            or row.get("semantic_evidence_sha256") != evidence_claimed
            or evidence.get("candidate_sha256") != canonical_sha256(candidate)
            or evidence.get("primary_capability") != assignment.get("primary_capability")
            or evidence.get("assigned_cross_cutting_dimension")
            != assignment.get("assigned_cross_cutting_dimension")
            or row.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError("V3 semantic carry row is unsealed or candidate-unbound")
        output[identifier] = evidence
    return output


def build(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if file_sha256(args.correction_plan) != CORRECTION_PLAN_SHA256:
        raise ValueError("V3 schema-correction plan hash differs")
    v2_accounting = sealed(args.v2_accounting, "report_sha256")
    smoke = sealed(args.live_smoke, "report_sha256")
    execution = sealed(args.execution_manifest, "manifest_sha256")
    readiness = sealed(args.composite_readiness, "report_sha256")
    semantic = sealed(args.semantic_equivalence, "manifest_sha256")
    v2_attempt = sealed(args.v2_attempt_manifest, "manifest_sha256")
    v2_carry = sealed(args.v2_semantic_carry, "manifest_sha256")
    config_bytes = args.codex_config.read_bytes()
    config = json.loads(config_bytes)
    cli_identity = f"codex-cli {config.get('codex_cli_version')}"
    validate_v5_live_schema_admission_smoke_report(
        smoke, config, hashlib.sha256(config_bytes).hexdigest(), cli_identity,
    )
    schema = _response_schema("test_author", "v5")
    if (
        v2_accounting.get("report_sha256") != V2_ACCOUNTING_SEAL
        or v2_accounting.get("attempt_id") != "primary-two-phase-v2"
        or v2_accounting.get("carry_proposal", {}).get("total_completed_semantics") != 42
        or v2_accounting.get("carry_proposal", {}).get("remaining_semantic_calls") != 18
        or v2_accounting.get("carry_proposal", {}).get("test_author_carries") != 0
        or smoke.get("report_sha256") != LIVE_SMOKE_SEAL
        or smoke.get("controls", {}).get("response_schema_sha256") != SCHEMA_SHA256
        or canonical_sha256(schema) != SCHEMA_SHA256
        or execution.get("records") != 60
        or execution.get("composite_readiness_report_sha256") != readiness.get("report_sha256")
        or semantic.get("contract_id") != CONTRACT_ID
        or v2_attempt.get("execution_manifest_sha256") != execution.get("manifest_sha256")
        or v2_attempt.get("semantic_carry_manifest_sha256") != v2_carry.get("manifest_sha256")
    ):
        raise ValueError("V3 controlling evidence or 42/18 partition differs")

    generated_rows = read_jsonl(args.candidates)
    assignment_rows = read_jsonl(args.assignments)
    assignments = {row["id"]: row for row in assignment_rows}
    generated = {row["candidate"]["id"]: row["candidate"] for row in generated_rows}
    ordered_ids = execution["ordered_candidate_ids"]
    if [row["candidate"]["id"] for row in generated_rows] != ordered_ids:
        raise ValueError("V3 candidate inputs do not preserve the exact ordered 60")
    v4_carries, required = load_v5_semantic_dispatch(args.semantic_equivalence, generated_rows, assignments)
    prior_three = validate_carry_rows(
        v2_carry.get("rows"), V1_CARRY_IDS, execution, generated, assignments,
        config, cli_identity,
    )
    if len(v4_carries) != 37 or len(required) != 23 or len(prior_three) != 3:
        raise ValueError("V3 inherited semantic partition differs from 37+3")

    accounting_rows = {
        row["candidate_id"]: row
        for row in v2_accounting.get("carry_proposal", {}).get("v2_completed_semantic_rows", [])
    }
    rows: list[dict[str, Any]] = []
    output: dict[str, dict[str, Any]] = {}
    for identifier in EXPECTED_CARRY_IDS:
        if identifier not in required or identifier not in accounting_rows:
            raise ValueError("V3 two-row carry is outside the frozen 23-review partition")
        source = Path(accounting_rows[identifier]["stage_artifact"]["path"])
        checked = validate_completed_semantic(source, generated[identifier], assignments[identifier], config, cli_identity)
        artifact = sealed(source, "artifact_sha256")
        evidence = _semantic_evidence(
            generated[identifier], assignments[identifier], dict(artifact["response"]),
            artifact["run"]["run_evidence_sha256"],
        )
        row: dict[str, Any] = {
            "schema_version": "ganesh-mini-gate2-v5-v2-semantic-carry/v1",
            "candidate_id": identifier,
            "cell_id": assignments[identifier]["cell_id"],
            "ordinal": ordered_ids.index(identifier),
            "source_attempt_id": "primary-two-phase-v2",
            "target_attempt_id": ATTEMPT_ID,
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
        output[identifier] = evidence

    correction: dict[str, Any] = {
        "schema_version": CORRECTION_SCHEMA,
        "status": "passed-live-schema-admission",
        "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256,
        "correction_plan_sha256": CORRECTION_PLAN_SHA256,
        "v2_accounting_report_sha256": V2_ACCOUNTING_SEAL,
        "v2_semantic_carry_manifest_sha256": v2_carry["manifest_sha256"],
        "live_smoke_report_sha256": LIVE_SMOKE_SEAL,
        "test_author_response_schema_sha256": SCHEMA_SHA256,
        "provider_correction": {
            "removed_provider_keyword": "uniqueItems",
            "local_duplicate_case_id_rejection_preserved": True,
            "content_free_live_smoke_calls": 1,
            "candidate_model_calls": 0,
        },
        "execution_manifest_sha256": execution["manifest_sha256"],
        "ordered_candidate_ids_sha256": execution["ordered_candidate_ids_sha256"],
        "evaluation_artifacts_read": 0,
    }
    correction["manifest_sha256"] = canonical_sha256(correction)
    carry: dict[str, Any] = {
        "schema_version": CARRY_SCHEMA,
        "contract_id": CONTRACT_ID,
        "source_attempt_id": "primary-two-phase-v2",
        "target_attempt_id": ATTEMPT_ID,
        "correction_manifest_sha256": correction["manifest_sha256"],
        "v2_accounting_report_sha256": V2_ACCOUNTING_SEAL,
        "execution_manifest_sha256": execution["manifest_sha256"],
        "semantic_equivalence_manifest_sha256": semantic["manifest_sha256"],
        "prior_v4_equivalent_semantics": 37,
        "prior_v1_completed_semantics": 3,
        "records": 2,
        "rows": rows,
        "rows_sha256": canonical_sha256(rows),
        "total_completed_semantics_after_carry": 42,
        "remaining_semantic_calls": 18,
        "test_author_carries": 0,
        "evaluation_artifacts_read": 0,
    }
    carry["manifest_sha256"] = canonical_sha256(carry)
    bindings = runtime_bindings(v2_attempt)
    attempt: dict[str, Any] = {
        "schema_version": ATTEMPT_SCHEMA,
        "status": "sealed-ready-for-runtime-validation",
        "attempt_id": ATTEMPT_ID,
        "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256,
        "correction_plan_sha256": CORRECTION_PLAN_SHA256,
        "correction_manifest_sha256": correction["manifest_sha256"],
        "v2_accounting_report_sha256": V2_ACCOUNTING_SEAL,
        "live_smoke_report_sha256": LIVE_SMOKE_SEAL,
        "execution_manifest_sha256": execution["manifest_sha256"],
        "base_composite_readiness_report_sha256": readiness["report_sha256"],
        "semantic_equivalence_manifest_sha256": semantic["manifest_sha256"],
        "v2_attempt_manifest_sha256": v2_attempt["manifest_sha256"],
        "v2_semantic_carry_manifest_sha256": v2_carry["manifest_sha256"],
        "v3_semantic_carry_manifest_sha256": carry["manifest_sha256"],
        "ordered_candidate_ids_sha256": execution["ordered_candidate_ids_sha256"],
        "records": 60,
        "semantic_accounting": {
            "v4_equivalent": 37,
            "v1_completed": 3,
            "v2_completed": 2,
            "carried_total": 42,
            "remaining_new_calls": 18,
            "total": 60,
        },
        "test_author_accounting": {"carried": 0, "remaining_new_calls": 60, "total": 60},
        "output_root": str(args.output_root.resolve()),
        "runtime_bindings": bindings,
        "required_controller_interface": {
            "validation_before_model_adapter_construction": True,
            "merge_exactly_two_v2_semantics": True,
            "remove_exactly_two_ids_from_v2_remaining_dispatch": True,
            "implicit_prior_attempt_scan_forbidden": True,
        },
        "python": platform.python_version(),
        "evaluation_artifacts_read": 0,
    }
    attempt["manifest_sha256"] = canonical_sha256(attempt)
    return correction, carry, attempt


def load_v5_v3_schema_correction_attempt(
    *, correction_plan_path: Path, correction_manifest_path: Path,
    v2_accounting_path: Path, live_smoke_path: Path,
    v2_semantic_carry_path: Path, v3_semantic_carry_path: Path,
    v3_attempt_manifest_path: Path, v2_attempt_manifest_path: Path,
    execution_manifest_path: Path, composite_readiness_path: Path,
    semantic_equivalence_path: Path, generated_rows: list[dict[str, Any]],
    assignments: dict[str, dict[str, Any]], output_root: Path,
) -> dict[str, dict[str, Any]]:
    """Validate V3 startup and return exactly five completed V5 semantic carries."""
    if file_sha256(correction_plan_path) != CORRECTION_PLAN_SHA256:
        raise ValueError("V3 schema-correction plan hash differs")
    correction = sealed(correction_manifest_path, "manifest_sha256")
    accounting = sealed(v2_accounting_path, "report_sha256")
    smoke = sealed(live_smoke_path, "report_sha256")
    carry = sealed(v3_semantic_carry_path, "manifest_sha256")
    attempt = sealed(v3_attempt_manifest_path, "manifest_sha256")
    v2_attempt = sealed(v2_attempt_manifest_path, "manifest_sha256")
    execution = sealed(execution_manifest_path, "manifest_sha256")
    readiness = sealed(composite_readiness_path, "report_sha256")
    semantic = sealed(semantic_equivalence_path, "manifest_sha256")
    v2_carry = sealed(v2_semantic_carry_path, "manifest_sha256")
    validate_frozen_runtime_bindings(attempt)
    if (
        correction.get("schema_version") != CORRECTION_SCHEMA
        or correction.get("status") != "passed-live-schema-admission"
        or correction.get("live_smoke_report_sha256") != smoke.get("report_sha256")
        or correction.get("test_author_response_schema_sha256") != SCHEMA_SHA256
        or accounting.get("report_sha256") != V2_ACCOUNTING_SEAL
        or smoke.get("report_sha256") != LIVE_SMOKE_SEAL
        or carry.get("schema_version") != CARRY_SCHEMA
        or carry.get("records") != 2
        or carry.get("test_author_carries") != 0
        or carry.get("total_completed_semantics_after_carry") != 42
        or carry.get("remaining_semantic_calls") != 18
        or attempt.get("schema_version") != ATTEMPT_SCHEMA
        or attempt.get("status") != "sealed-ready-for-runtime-validation"
        or attempt.get("attempt_id") != ATTEMPT_ID
        or attempt.get("correction_manifest_sha256") != correction.get("manifest_sha256")
        or attempt.get("v3_semantic_carry_manifest_sha256") != carry.get("manifest_sha256")
        or attempt.get("v2_attempt_manifest_sha256") != v2_attempt.get("manifest_sha256")
        or attempt.get("v2_semantic_carry_manifest_sha256") != v2_carry.get("manifest_sha256")
        or attempt.get("execution_manifest_sha256") != execution.get("manifest_sha256")
        or attempt.get("base_composite_readiness_report_sha256") != readiness.get("report_sha256")
        or attempt.get("semantic_equivalence_manifest_sha256") != semantic.get("manifest_sha256")
        or attempt.get("output_root") != str(output_root.resolve())
        or attempt.get("semantic_accounting") != {
            "v4_equivalent": 37, "v1_completed": 3, "v2_completed": 2,
            "carried_total": 42, "remaining_new_calls": 18, "total": 60,
        }
        or attempt.get("test_author_accounting") != {"carried": 0, "remaining_new_calls": 60, "total": 60}
        or attempt.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("V3 correction, carry, or attempt manifest differs from runtime")
    generated = {row.get("candidate", {}).get("id"): row.get("candidate") for row in generated_rows}
    config_path = ROOT / "configs/data/expansion_teacher.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    cli_identity = f"codex-cli {config.get('codex_cli_version')}"
    prior_output = validate_carry_rows(
        v2_carry.get("rows"), V1_CARRY_IDS, execution, generated, assignments,
        config, cli_identity,
    )
    rows = carry.get("rows")
    if not isinstance(rows, list) or carry.get("rows_sha256") != canonical_sha256(rows):
        raise ValueError("V3 carry rows are invalid")
    new_output = validate_carry_rows(
        rows, EXPECTED_CARRY_IDS, execution, generated, assignments, config, cli_identity,
    )
    output = {**prior_output, **new_output}
    if tuple(output) != EXPECTED_ALL_V5_CARRY_IDS:
        raise ValueError("V3 loader did not return the exact five completed V5 semantic carries")
    return output


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "correction-plan", "v2-accounting", "live-smoke", "execution-manifest",
        "composite-readiness", "semantic-equivalence", "v1-accounting",
        "resilience-addendum", "v2-semantic-carry", "v2-attempt-manifest",
        "candidates", "assignments", "codex-config",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--v2-output-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--correction-output", type=Path, required=True)
    parser.add_argument("--carry-output", type=Path, required=True)
    parser.add_argument("--attempt-output", type=Path, required=True)
    args = parser.parse_args(argv)
    correction, carry, attempt = build(args)
    write_json(args.correction_output, correction)
    write_json(args.carry_output, carry)
    write_json(args.attempt_output, attempt)
    print(json.dumps({
        "correction_manifest_sha256": correction["manifest_sha256"],
        "carry_manifest_sha256": carry["manifest_sha256"],
        "attempt_manifest_sha256": attempt["manifest_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
