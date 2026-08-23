from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_RETRY_V6_CARD.json"


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def file_sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def test_retry_v6_card_is_sealed_and_binds_swift_repair() -> None:
    card = json.loads(CARD.read_text())
    claimed = card.pop("card_sha256")
    assert digest(card) == claimed
    assert card["status"] == "prepared-awaiting-explicit-gcloud-approval"
    assert card["authorization"]["status"] == "not-yet-approved-for-v6"
    assert Decimal(str(card["cost"]["incremental_upper_usd"])) < Decimal(
        str(card["cost"]["requested_incremental_ceiling_usd"])
    )
    source = card["source"]
    assert source["commit"] == "2423f4e7e9c37590b77128318dc3b7416111cb00"
    assert source["qualifier_sha256"] == file_sha("scripts/cuda/qualify.py")
    assert source["qualification_runner_sha256"] == file_sha("scripts/cuda/run_qualification.sh")
    assert source["startup_controller_sha256"] == file_sha("scripts/cuda/gcloud_startup_gate0b.sh")
    assert source["metadata_wrapper_sha256"] == file_sha("scripts/cuda/gcloud_startup_metadata_wrapper.sh")
    assert card["repair"]["dependency_lock_sha256"] == file_sha("uv.lock")
    assert card["model"]["revision"] == "15852e8c16360a2fea060d615a32b45270f8a8fc"
