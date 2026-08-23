from __future__ import annotations

import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_L4_V8_EXECUTION_CARD.json"
APPROVAL = "Approved: one Standard L4 Gate 0B v5 retry, maximum 40 minutes and USD 0.70 incremental cost, including temporary private networking, verified GCS backup, and complete teardown."


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def commit_file_sha(commit: str, path: str) -> str:
    return hashlib.sha256(subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)).hexdigest()


def test_v8_execution_card_seals_exact_bounded_approval_and_source() -> None:
    card = json.loads(CARD.read_text())
    claimed = card.pop("card_sha256")
    assert canonical_sha256(card) == claimed
    assert card["authorization"]["verbatim"] == APPROVAL
    assert card["authorization"]["maximum_seconds"] == 2400
    assert card["authorization"]["maximum_gpu_count"] == 1
    assert card["resource"]["provisioning_model"] == "STANDARD"
    assert Decimal(str(card["price"]["incremental_upper_usd"])) < Decimal(str(card["price"]["approved_ceiling_usd"]))
    assert card["measured_change"]["new_sequence_length"] == 2944
    assert card["measured_change"]["records_or_tokens_truncated"] == 0
    commit = card["source"]["commit"]
    assert card["source"]["qualification_config_sha256"] == commit_file_sha(commit, "configs/cuda/qwen3_5_2b_gate0.json")
    assert card["source"]["training_config_sha256"] == commit_file_sha(commit, "configs/train/seed_pilot.json")
    assert card["source"]["qualifier_sha256"] == commit_file_sha(commit, "scripts/cuda/qualify.py")
