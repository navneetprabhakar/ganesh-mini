import json
from pathlib import Path

from scripts.inference.build_lane_checkpoint_sweep_gcloud_proposal import build
from scripts.inference.build_lane_checkpoint_sweep_readonly_report import build as build_report


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "measurement/gate4/lane-stratified-probe-checkpoint-sweep-20260910"


def test_report_replays_and_binds_readonly_evidence() -> None:
    report = json.loads((BASE / "gcloud-readonly-inspection-report.json").read_text())

    assert report == build_report(ROOT, report["checked_at"])
    assert report["conclusion"]["prerequisites_passed"] is True
    assert report["conclusion"]["execution_authorized"] is False
    assert len(report["inputs"]) == 12


def test_proposal_is_bounded_diagnostic_only() -> None:
    report = json.loads((BASE / "gcloud-readonly-inspection-report.json").read_text())
    proposal = build(report)

    assert proposal["status"] == "pending-explicit-execution-approval"
    assert proposal["promotion_authority"] == "none"
    assert proposal["checkpoint_selection_authority"] == "none"
    assert proposal["training_allowed"] is False
    assert proposal["full_development_allowed"] is False
    assert proposal["decision_surface_allowed"] is False
    assert proposal["resource"]["maximum_vm_lifetime_seconds"] == 7200
    assert proposal["cost"]["provider_upper_usd"] == "1.762043024"
    assert proposal["cost"]["absolute_cost_ceiling_usd"] == "2.25"
    assert len(proposal["inputs"]) == 10


def test_repository_proposal_matches_builder() -> None:
    report = json.loads((BASE / "gcloud-readonly-inspection-report.json").read_text())
    proposal = json.loads((BASE / "gcloud-execution-proposal.json").read_text())

    assert proposal == build(report)
