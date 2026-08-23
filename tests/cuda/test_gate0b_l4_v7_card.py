from __future__ import annotations

import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_L4_V7_CARD.json"


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def commit_file_sha(commit: str, path: str) -> str:
    return hashlib.sha256(subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)).hexdigest()


def test_l4_v7_card_is_sealed_data_preserving_and_approval_gated() -> None:
    card = json.loads(CARD.read_text())
    claimed = card.pop("card_sha256")
    assert canonical_sha256(card) == claimed
    assert card["status"] == "approval-required"
    assert card["authorization"]["status"] == "not-approved"
    assert card["authorization"]["maximum_seconds"] == 2400
    assert card["authorization"]["maximum_gpu_count"] == 1
    assert Decimal(str(card["price"]["incremental_upper_usd"])) < Decimal(str(card["price"]["requested_ceiling_usd"]))
    change = card["measured_change"]
    assert change["new_sequence_length"] == 2944
    assert change["maximum_prepared_record_tokens"] <= change["new_sequence_length"]
    assert change["records_or_tokens_truncated"] == 0
    assert change["qualification_outcome_guaranteed"] is False
    commit = card["source"]["commit"]
    assert card["source"]["qualification_config_sha256"] == commit_file_sha(commit, "configs/cuda/qwen3_5_2b_gate0.json")
    assert card["source"]["training_config_sha256"] == commit_file_sha(commit, "configs/train/seed_pilot.json")
    assert card["source"]["qualifier_sha256"] == commit_file_sha(commit, "scripts/cuda/qualify.py")
