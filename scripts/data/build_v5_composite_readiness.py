#!/usr/bin/env python3
"""Build and validate the fail-closed V5 pre-execution readiness seal."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v5_preflight import CONTRACT_ID, PLAN_SHA256
from scripts.data.run_v5_interface_fixtures import validate_v5_interface_readiness_report


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "ganesh-mini-gate2-v5-composite-readiness/v1"
BUDGET_ADDENDUM_SHA256 = "1933b409b656ab90cf4a82e44b0b2b7dc29d4701d3a162add64db179319a4899"
BUDGET_CONTRACT = {
    "ordered_first_pass_candidates": 60,
    "immutable_carries": 58,
    "fresh_teacher_primaries": 2,
    "maximum_generated_reserves": 5,
    "absolute_terminal_candidate_budget": 65,
    "absolute_new_teacher_generation_budget": 7,
}
RUNTIME_CODE_PATHS = (
    "scripts/data/build_v5_composite_readiness.py",
    "scripts/data/generate_v5_typescript_primaries.py",
    "scripts/data/assemble_v5_execution_cohort.py",
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


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path, where: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{where}: unreadable JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{where}: expected one JSON object")
    return value


def _validate_seal(value: dict[str, Any], field: str, where: str) -> None:
    body = dict(value)
    claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{where}: invalid {field}")


def _validate_manifest(
    value: dict[str, Any], seal_field: str, schema: str, where: str,
) -> None:
    _validate_seal(value, seal_field, where)
    if (
        value.get("schema_version") != schema
        or value.get("contract_id") != CONTRACT_ID
        or value.get("plan_sha256") != PLAN_SHA256
        or value.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError(f"{where}: identity or evaluation-separation mismatch")


def build_v5_composite_readiness(
    *, v4_tooling_report_path: Path, v4_tooling_bundle_path: Path,
    admission_config_path: Path, interface_report_path: Path,
    interface_bundle_path: Path, strict_test_author_report_path: Path,
    strict_test_author_bundle_path: Path, plan_path: Path,
    source_addendum_path: Path, budget_addendum_path: Path,
    cohort_manifest_path: Path, source_manifest_path: Path,
    carry_manifest_path: Path, semantic_manifest_path: Path,
    exclusion_ledger_path: Path, runtime_config_path: Path,
    v5_preflight_config_path: Path, v4_preflight_config_path: Path,
) -> dict[str, Any]:
    if _file_sha256(plan_path) != PLAN_SHA256:
        raise ValueError("V5 base plan hash mismatch")
    source_addendum_sha256 = _file_sha256(source_addendum_path)
    if _file_sha256(budget_addendum_path) != BUDGET_ADDENDUM_SHA256:
        raise ValueError("V5 budget clarification addendum hash mismatch")

    cohort = _load(cohort_manifest_path, "cohort manifest")
    source = _load(source_manifest_path, "source manifest")
    carry = _load(carry_manifest_path, "carry manifest")
    semantic = _load(semantic_manifest_path, "semantic equivalence manifest")
    exclusion = _load(exclusion_ledger_path, "exclusion ledger")
    _validate_manifest(
        cohort, "manifest_sha256", "ganesh-mini-gate2-v5-ordered-cohort-manifest/v1",
        "cohort manifest",
    )
    _validate_manifest(
        source, "manifest_sha256", "ganesh-mini-gate2-v5-source-manifest/v1",
        "source manifest",
    )
    _validate_manifest(
        carry, "manifest_sha256", "ganesh-mini-gate2-v5-immutable-carry-manifest/v1",
        "carry manifest",
    )
    _validate_manifest(
        semantic, "manifest_sha256", "ganesh-mini-gate2-v5-semantic-equivalence-manifest/v1",
        "semantic equivalence manifest",
    )
    _validate_manifest(
        exclusion, "ledger_sha256", "ganesh-mini-gate2-v5-exclusion-ledger/v1",
        "exclusion ledger",
    )
    if (
        cohort.get("source_feasibility_addendum_sha256") != source_addendum_sha256
        or source.get("source_feasibility_addendum_sha256") != source_addendum_sha256
        or carry.get("source_feasibility_addendum_sha256") != source_addendum_sha256
        or cohort.get("source_manifest_sha256") != source.get("manifest_sha256")
        or cohort.get("carry_manifest_sha256") != carry.get("manifest_sha256")
        or source.get("exclusion_ledger_sha256") != exclusion.get("ledger_sha256")
        or semantic.get("cohort_manifest_sha256") != cohort.get("manifest_sha256")
        or semantic.get("carry_manifest_sha256") != carry.get("manifest_sha256")
        or cohort.get("records") != 60
        or carry.get("records") != 58
        or cohort.get("immutable_carries") != 58
        or cohort.get("fresh_teacher_primaries") != 2
        or cohort.get("maximum_generated_reserves") != 5
        or cohort.get("absolute_terminal_candidate_budget") != 65
        or cohort.get("absolute_new_teacher_generation_budget") != 7
        or any(
            item.get("budget_clarification_addendum_sha256") != BUDGET_ADDENDUM_SHA256
            for item in (cohort, source, carry, semantic, exclusion)
        )
    ):
        raise ValueError("V5 cohort/source/carry/semantic bindings or budgets mismatch")

    interface_bundle = _load(interface_bundle_path, "V5 interface fixture bundle")
    interface_report = _load(interface_report_path, "V5 interface readiness report")
    validate_v5_interface_readiness_report(
        interface_report, interface_bundle, runtime_config_path,
        v5_preflight_config_path, v4_preflight_config_path,
    )
    strict_bundle = _load(strict_test_author_bundle_path, "V5 strict test-author fixture bundle")
    strict_report = _load(strict_test_author_report_path, "V5 strict test-author report")
    from scripts.data.run_v5_test_author_readiness import (
        validate_v5_test_author_readiness_report,
    )
    validate_v5_test_author_readiness_report(strict_report, strict_bundle)

    v4_report = _load(v4_tooling_report_path, "V4 full tooling report")
    _validate_seal(v4_report, "report_sha256", "V4 full tooling report")
    if (
        v4_report.get("schema_version") != "ganesh-mini-v4-tooling-fixture-report/v1"
        or v4_report.get("status") != "passed"
        or v4_report.get("evaluation_artifacts_read") != 0
        or v4_report.get("bindings", {}).get("fixture_input_sha256")
        != _file_sha256(v4_tooling_bundle_path)
        or v4_report.get("bindings", {}).get("admission_config_sha256")
        != _file_sha256(admission_config_path)
        or v4_report.get("bindings", {}).get("runtime_config_sha256")
        != _file_sha256(runtime_config_path)
        or v4_report.get("bindings", {}).get("preflight_config_sha256")
        != _file_sha256(v4_preflight_config_path)
    ):
        raise ValueError("V4 full tooling report is not sealed or input-bound")

    runtime_hashes = {}
    for relative in RUNTIME_CODE_PATHS:
        path = ROOT / relative
        if not path.is_file():
            raise ValueError(f"missing readiness runtime code: {relative}")
        runtime_hashes[relative] = _file_sha256(path)
    bindings = {
        "v4_full_tooling_report_sha256": _file_sha256(v4_tooling_report_path),
        "v4_full_tooling_report_seal": v4_report["report_sha256"],
        "v4_full_tooling_bundle_sha256": _file_sha256(v4_tooling_bundle_path),
        "admission_config_sha256": _file_sha256(admission_config_path),
        "v5_interface_report_sha256": _file_sha256(interface_report_path),
        "v5_interface_report_seal": interface_report["report_sha256"],
        "v5_interface_bundle_sha256": _file_sha256(interface_bundle_path),
        "strict_test_author_report_sha256": _file_sha256(strict_test_author_report_path),
        "strict_test_author_report_seal": strict_report["report_sha256"],
        "strict_test_author_bundle_sha256": _file_sha256(strict_test_author_bundle_path),
        "plan_sha256": PLAN_SHA256,
        "source_feasibility_addendum_sha256": source_addendum_sha256,
        "budget_clarification_addendum_sha256": BUDGET_ADDENDUM_SHA256,
        "cohort_manifest_sha256": cohort["manifest_sha256"],
        "source_manifest_sha256": source["manifest_sha256"],
        "carry_manifest_sha256": carry["manifest_sha256"],
        "semantic_equivalence_manifest_sha256": semantic["manifest_sha256"],
        "exclusion_ledger_sha256": exclusion["ledger_sha256"],
        "runtime_config_sha256": _file_sha256(runtime_config_path),
        "v5_preflight_config_sha256": _file_sha256(v5_preflight_config_path),
        "v4_preflight_config_sha256": _file_sha256(v4_preflight_config_path),
        "runtime_code_sha256": runtime_hashes,
    }
    report = {
        "schema_version": SCHEMA_VERSION,
        "status": "passed",
        "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256,
        "budgets": dict(BUDGET_CONTRACT),
        "bindings": bindings,
        "model_calls_eligible": True,
        "qualification_executed": False,
        "gcloud_authorized": False,
        "training_authorized": False,
        "qualification_candidates_admitted": 0,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def validate_v5_composite_readiness(report: Any, **paths: Path) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("V5 composite readiness report is missing")
    expected = build_v5_composite_readiness(**paths)
    if report != expected:
        raise ValueError("V5 composite readiness report is stale, tampered, or unbound")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "v4-tooling-report", "v4-tooling-bundle", "admission-config",
        "interface-report", "interface-bundle",
        "strict-test-author-report", "strict-test-author-bundle", "plan",
        "source-addendum", "budget-addendum", "cohort-manifest", "source-manifest",
        "carry-manifest", "semantic-manifest", "exclusion-ledger", "runtime-config",
        "v5-preflight-config", "v4-preflight-config",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    paths = {key: value for key, value in vars(args).items() if key != "output"}
    report = build_v5_composite_readiness(**{f"{key}_path": value for key, value in paths.items()})
    validate_v5_composite_readiness(
        report, **{f"{key}_path": value for key, value in paths.items()},
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
