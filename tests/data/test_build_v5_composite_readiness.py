from __future__ import annotations

from pathlib import Path

import pytest

from scripts.data import build_v5_composite_readiness as subject


ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"


def _paths() -> dict[str, Path]:
    return {
        "v4_tooling_report_path": V5 / "readiness-v1/v4-tooling-report.json",
        "v4_tooling_bundle_path": V5 / "readiness-v1/v4-tooling-fixture-bundle.json",
        "admission_config_path": ROOT / "configs/data/expansion_v1.json",
        "interface_report_path": V5 / "readiness-v1/interface-report.json",
        "interface_bundle_path": V5 / "readiness-v1/interface-fixture-bundle.json",
        "strict_test_author_report_path": V5 / "cohort-v1/readiness-v1/test-author-readiness-report.json",
        "strict_test_author_bundle_path": V5 / "cohort-v1/readiness-v1/test-author-fixture-bundle.json",
        "plan_path": ROOT / "docs/plans/GATE2_REPAIR_DELTA_V5_INTERFACE_REPLAY_PLAN_20260916.md",
        "source_addendum_path": ROOT / "docs/plans/GATE2_V5_SOURCE_FEASIBILITY_ADDENDUM_20260916.md",
        "budget_addendum_path": ROOT / "docs/plans/GATE2_V5_BUDGET_CLARIFICATION_ADDENDUM_20260916.md",
        "cohort_manifest_path": V5 / "cohort-v1/cohort-manifest.json",
        "source_manifest_path": V5 / "cohort-v1/source-manifest.json",
        "carry_manifest_path": V5 / "cohort-v1/carry-manifest.json",
        "semantic_manifest_path": V5 / "cohort-v1/semantic-equivalence.json",
        "exclusion_ledger_path": V5 / "cohort-v1/exclusion-ledger.json",
        "runtime_config_path": ROOT / "configs/eval/runtimes.json",
        "v5_preflight_config_path": ROOT / "configs/data/gate2_v5_interface_preflight.json",
        "v4_preflight_config_path": ROOT / "configs/data/gate2_v4_post_teacher_preflight.json",
    }


def test_composite_readiness_seals_all_inputs_and_budget_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(subject, "validate_v5_interface_readiness_report", lambda report, *_args: report)
    monkeypatch.setattr(
        "scripts.data.run_v5_test_author_readiness.validate_v5_test_author_readiness_report",
        lambda report, _bundle: report,
    )
    monkeypatch.setattr(
        "scripts.data.run_v4_tooling_fixtures.validate_tooling_readiness_report",
        lambda report, *_args: report,
    )
    paths = _paths()
    report = subject.build_v5_composite_readiness(**paths)
    assert report["status"] == "passed"
    assert report["model_calls_eligible"] is True
    assert report["qualification_executed"] is False
    assert report["gcloud_authorized"] is False
    assert report["budgets"] == {
        "ordered_first_pass_candidates": 60,
        "immutable_carries": 58,
        "fresh_teacher_primaries": 2,
        "maximum_generated_reserves": 5,
        "absolute_terminal_candidate_budget": 65,
        "absolute_new_teacher_generation_budget": 7,
    }
    subject.validate_v5_composite_readiness(report, **paths)
    tampered = dict(report)
    tampered["budgets"] = {**report["budgets"], "maximum_generated_reserves": 6}
    with pytest.raises(ValueError, match="stale, tampered, or unbound"):
        subject.validate_v5_composite_readiness(tampered, **paths)
