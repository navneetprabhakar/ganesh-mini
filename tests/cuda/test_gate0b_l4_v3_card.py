from __future__ import annotations

import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_L4_V3_CARD.json"


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def commit_file_sha(commit: str, path: str) -> str:
    return hashlib.sha256(subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)).hexdigest()


def test_l4_v3_card_is_sealed_unapproved_and_binds_memory_repair() -> None:
    card = json.loads(CARD.read_text())
    claimed = card.pop("card_sha256")
    assert digest(card) == claimed
    assert card["status"] == "prepared-awaiting-explicit-gcloud-approval"
    assert card["authorization"]["status"] == "not-approved-for-v3"
    assert card["authorization"]["gcloud_actions_before_approval"] is False
    assert card["repair"]["vision_cpu_offload_required"] is True
    assert card["repair"]["measured_cuda_release_required"] is True
    assert card["resource"]["provisioning_model"] == "STANDARD"
    assert card["resource"]["maximum_run_seconds"] == 2400
    assert card["resource"]["controller_budget_seconds"] + card["resource"]["backup_reserve_seconds"] == 2400
    assert Decimal(str(card["cost"]["incremental_upper_usd"])) < Decimal(str(card["cost"]["requested_incremental_ceiling_usd"]))
    commit = card["source"]["commit"]
    assert card["source"]["qualifier_sha256"] == commit_file_sha(commit, "scripts/cuda/qualify.py")
    assert card["source"]["qwen_runtime_sha256"] == commit_file_sha(commit, "scripts/train/qwen_runtime.py")
    assert card["source"]["production_sft_sha256"] == commit_file_sha(commit, "scripts/train/run_sft.py")
