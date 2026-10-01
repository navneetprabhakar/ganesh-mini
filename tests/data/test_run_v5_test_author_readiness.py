from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v5_test_author_fixture_bundle import (
    LANES, build_v5_test_author_fixture_bundle,
)
from scripts.data.run_v5_test_author_readiness import (
    run_v5_test_author_readiness, validate_v5_test_author_readiness_report,
)
from scripts.data.build_v5_v3_schema_correction_manifests import (
    load_v5_v3_schema_correction_attempt,
)


ROOT = Path(__file__).resolve().parents[2]
READINESS_ROOT = (
    ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"
    / "cohort-v1/readiness-v1"
)


def _reseal_bundle(bundle: dict) -> None:
    bundle.pop("bundle_sha256", None)
    bundle["bundle_sha256"] = canonical_sha256(bundle)


def _reseal_report(report: dict) -> None:
    report.pop("report_sha256", None)
    report["report_sha256"] = canonical_sha256(report)


def test_v5_test_author_readiness_executes_all_positive_and_negative_contracts() -> None:
    bundle = build_v5_test_author_fixture_bundle()
    report = run_v5_test_author_readiness(bundle)

    assert report["status"] == "passed"
    assert report["coverage"]["positive_lanes"] == list(LANES)
    assert [row["lane"] for row in report["positive_results"]] == list(LANES)
    assert all(len(row["test_file_sha256s"]) == 2 for row in report["positive_results"])
    assert [row["fixture_id"] for row in report["negative_results"]] == [
        "reject-legacy-three-file-array", "reject-java-entrypoint",
        "reject-typescript-node-test-import", "reject-primary-dependent-cross-test",
    ]
    assert all(row["exception_type"] == "ValueError" for row in report["negative_results"])
    assert validate_v5_test_author_readiness_report(report, bundle) is report


def test_v5_test_author_readiness_rejects_tampered_bundle_before_execution() -> None:
    bundle = build_v5_test_author_fixture_bundle()
    bundle["positive_fixtures"][0]["response"]["primary_discrimination"]["case_ids"] = ["one"]
    with pytest.raises(ValueError, match="malformed or unsealed"):
        run_v5_test_author_readiness(bundle)


def test_v5_test_author_readiness_fails_if_negative_is_accepted() -> None:
    bundle = build_v5_test_author_fixture_bundle()
    invalid = bundle["negative_fixtures"][0]
    invalid["response"] = copy.deepcopy(bundle["positive_fixtures"][4]["response"])
    _reseal_bundle(bundle)
    with pytest.raises(ValueError, match="invalid response was accepted"):
        run_v5_test_author_readiness(bundle)


def test_v5_test_author_readiness_validator_rejects_resealed_result_drift() -> None:
    bundle = build_v5_test_author_fixture_bundle()
    report = run_v5_test_author_readiness(bundle)
    report["negative_results"][0]["status"] = "passed"
    report["bindings"]["negative_results_sha256"] = canonical_sha256(
        report["negative_results"]
    )
    _reseal_report(report)
    with pytest.raises(ValueError, match="invalid or unbound"):
        validate_v5_test_author_readiness_report(report, bundle)


def test_v5_test_author_readiness_validator_binds_production_implementation() -> None:
    bundle = build_v5_test_author_fixture_bundle()
    report = run_v5_test_author_readiness(bundle)
    report["bindings"]["production_contract_implementation_sha256"] = "0" * 64
    _reseal_report(report)
    with pytest.raises(ValueError, match="invalid or unbound"):
        validate_v5_test_author_readiness_report(report, bundle)


def test_repository_v5_test_author_readiness_is_sealed_and_revalidated_by_v3() -> None:
    bundle = json.loads(
        (READINESS_ROOT / "test-author-fixture-bundle.json").read_text(encoding="utf-8")
    )
    report = json.loads(
        (READINESS_ROOT / "test-author-readiness-report.json").read_text(encoding="utf-8")
    )
    v5_root = READINESS_ROOT.parents[1]
    execution = v5_root / "cohort-v1/execution-v1"
    generated = [
        json.loads(line) for line in (execution / "candidates.jsonl").read_text().splitlines()
        if line
    ]
    assignment_rows = [
        json.loads(line) for line in (execution / "assignments.jsonl").read_text().splitlines()
        if line
    ]
    assignments = {row["id"]: row for row in assignment_rows}
    v2 = v5_root / "primary-two-phase-v2"
    v3 = v5_root / "primary-two-phase-v3"
    carried = load_v5_v3_schema_correction_attempt(
        correction_plan_path=ROOT / "docs/plans/GATE2_V5_SCHEMA_COMPATIBILITY_CORRECTION_20260917.md",
        correction_manifest_path=v3 / "schema-correction-manifest.json",
        v2_accounting_path=v2 / "interruption-accounting.json",
        live_smoke_path=v3 / "readiness-v1/live-schema-admission-smoke.json",
        v2_semantic_carry_path=v2 / "semantic-interruption-carry-manifest.json",
        v3_semantic_carry_path=v3 / "semantic-interruption-carry-manifest.json",
        v3_attempt_manifest_path=v3 / "attempt-manifest.json",
        v2_attempt_manifest_path=v2 / "attempt-manifest.json",
        execution_manifest_path=execution / "manifest.json",
        composite_readiness_path=v5_root / "readiness-v1/composite-report.json",
        semantic_equivalence_path=v5_root / "cohort-v1/semantic-equivalence.json",
        generated_rows=generated, assignments=assignments, output_root=v3,
    )
    assert len(carried) == 5
    report_body = dict(report); report_seal = report_body.pop("report_sha256")
    bundle_body = dict(bundle); bundle_seal = bundle_body.pop("bundle_sha256")
    assert report_seal == canonical_sha256(report_body)
    assert bundle_seal == canonical_sha256(bundle_body)
    assert report["status"] == "passed"
    assert report["bindings"]["response_schema_sha256"] == (
        "540c16635f55a452131f9c942924111230fbee1dfc2be4af2bc5b40312ad4fe4"
    )
    correction = json.loads((v3 / "schema-correction-manifest.json").read_text())
    assert correction["test_author_response_schema_sha256"] == (
        "e099481a27e5d40923778098eb3c02126ca40e0116565bcd8a224396baf077cc"
    )
    assert correction["provider_correction"]["removed_provider_keyword"] == "uniqueItems"
