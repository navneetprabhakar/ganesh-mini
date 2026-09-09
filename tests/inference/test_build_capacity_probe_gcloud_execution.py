from pathlib import Path

from scripts.inference.build_capacity_probe_gcloud_execution import build, canonical_sha256, load_sealed


ROOT = Path(__file__).resolve().parents[2]


def test_builds_exact_bounded_execution_card() -> None:
    base = ROOT / "measurement/gate4/capacity-probe-20260909"
    card = build(
        load_sealed(base / "gcloud-execution-proposal.json", "proposal_sha256"),
        load_sealed(base / "attempts/20260909T173721Z/approval.json", "approval_sha256"),
        base / "attempts/20260909T173721Z/training-execution-card.json",
        "gs://bucket/path/training-execution-card.json#1788979356084121",
    )
    claimed = card.pop("execution_sha256")
    assert claimed == canonical_sha256(card)
    assert card["status"] == "authorized-executable"
    assert card["execution"]["maximum_vm_lifetime_seconds"] == 7200
    assert card["execution"]["controller_budget_seconds"] == 6000
    assert card["execution"]["backup_reserve_seconds"] == 1200
    assert card["cost"]["absolute_cost_ceiling_usd"] == 2.25
    assert len(card["inputs"]) == 10
