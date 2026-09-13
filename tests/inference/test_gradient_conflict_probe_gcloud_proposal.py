import json
from pathlib import Path

from scripts.inference.build_gradient_conflict_probe_gcloud_proposal import build, canonical_sha256
from scripts.inference.build_gradient_conflict_probe_readonly_report import build as build_report


ROOT = Path(__file__).resolve().parents[2]


def test_repository_readonly_report_and_proposal_are_reproducible() -> None:
    report = build_report(ROOT)
    committed_report = json.loads((ROOT / "measurement/gate4/gradient-conflict-probe-20260911/gcloud-readonly-inspection-report.json").read_text())
    assert report == committed_report
    proposal = build()
    committed_proposal = json.loads((ROOT / "measurement/gate4/gradient-conflict-probe-20260911/gcloud-execution-proposal.json").read_text())
    assert proposal == committed_proposal
    assert proposal["status"] == "pending-explicit-execution-approval"
    assert proposal["cost"]["absolute_cost_ceiling_usd"] == "2.25"
    assert proposal["experiment"]["full_development_tasks"] == 0
    assert proposal["experiment"]["stage_1"]["optimizer_steps"] == 0
    assert proposal["experiment"]["stage_2"]["conditional_on_stage_1"] is True
    claimed = proposal.pop("proposal_sha256")
    assert claimed == canonical_sha256(proposal)
