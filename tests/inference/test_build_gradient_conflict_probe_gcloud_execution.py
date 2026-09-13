import json
from pathlib import Path

from scripts.inference.build_gradient_conflict_probe_gcloud_execution import build_execution, build_training, canonical_sha256, load_sealed


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "measurement/gate4/gradient-conflict-probe-20260911"


def test_approved_v4_cards_are_reproducible() -> None:
    proposal = load_sealed(BASE / "gcloud-execution-proposal.json", "proposal_sha256")
    approval = load_sealed(BASE / "attempts/20260911T020000Z/approval.json", "approval_sha256")
    training_path = BASE / "attempts/20260911T020000Z/training-execution-card.json"
    training = build_training(proposal, approval, ROOT / "artifacts/train/gradient-conflict-probe-v4/local-execution-card.json")
    assert training == json.loads(training_path.read_text())
    assert training["status"] == "ready"
    assert training["provider_execution"]["cost_ceiling_usd"] == 2.25
    fake_uri = "gs://bucket/training-execution-card.json#123"
    execution = build_execution(proposal, approval, training_path, fake_uri)
    assert execution["execution"]["maximum_vm_lifetime_seconds"] == 7200
    assert execution["execution"]["controller_budget_seconds"] == 6000
    assert execution["execution"]["backup_reserve_seconds"] == 1200
    claimed = execution.pop("execution_sha256")
    assert claimed == canonical_sha256(execution)
