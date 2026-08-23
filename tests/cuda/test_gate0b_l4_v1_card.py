from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_L4_V1_CARD.json"


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def test_l4_v1_card_is_sealed_approved_and_binds_current_runtime() -> None:
    card = json.loads(CARD.read_text())
    claimed = card.pop("card_sha256")
    assert digest(card) == claimed
    assert card["status"] == "approved-awaiting-generation-pinned-upload"
    assert card["authorization"]["status"] == "approved-for-one-l4-v1-attempt"
    assert card["source"]["commit"] == "ce5d4e6ef5f06c6338f06b0c2ecf61fcb9c8c67b"
    assert card["source"]["qualifier_sha256"] == file_sha("scripts/cuda/qualify.py")
    assert card["source"]["qualification_runner_sha256"] == file_sha("scripts/cuda/run_qualification.sh")
    assert card["source"]["startup_controller_sha256"] == file_sha("scripts/cuda/gcloud_startup_gate0b.sh")
    assert card["source"]["metadata_wrapper_sha256"] == file_sha("scripts/cuda/gcloud_startup_metadata_wrapper.sh")
    assert card["source"]["qualification_config_sha256"] == file_sha("configs/cuda/qwen3_5_2b_gate0.json")
    assert card["resource"]["machine_type"] == "g2-standard-8"
    assert card["resource"]["provisioning_model"] == "STANDARD"
    assert card["runtime"]["controller_budget_seconds"] + card["runtime"]["backup_reserve_seconds"] == 3600
    assert Decimal(str(card["cost"]["incremental_upper_usd"])) < Decimal(str(card["cost"]["absolute_incremental_ceiling_usd"]))
    assert card["hardware_admission"]["minimum_cuda_vram_bytes"] == 22 * 1024**3
    assert card["hardware_admission"]["maximum_peak_vram_bytes"] == 21 * 1024**3
