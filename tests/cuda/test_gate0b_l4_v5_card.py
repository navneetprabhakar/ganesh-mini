import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_L4_V5_CARD.json"


def test_l4_v5_card_is_sealed_approval_required_and_commit_bound() -> None:
    card = json.loads(CARD.read_text())
    claimed = card.pop("card_sha256")
    assert claimed == hashlib.sha256(
        json.dumps(card, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert card["status"] == "approval-required"
    assert card["authorization"]["status"] == "not-approved"
    assert card["resource"]["provisioning_model"] == "STANDARD"
    assert card["resource"]["maximum_run_seconds"] == 2400
    assert card["price"]["incremental_upper_usd"] < 0.7
    assert card["measured_change"]["records_or_tokens_truncated"] == 0
    assert card["measured_change"]["maximum_prepared_record_tokens"] < 3072

    commit = card["source"]["commit"]
    for key, path in (
        ("qualification_config_sha256", "configs/cuda/qwen3_5_2b_gate0.json"),
        ("training_config_sha256", "configs/train/seed_pilot.json"),
        ("qualifier_sha256", "scripts/cuda/qualify.py"),
    ):
        content = subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)
        assert card["source"][key] == hashlib.sha256(content).hexdigest()
