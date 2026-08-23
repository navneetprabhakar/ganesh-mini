from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_RETRY_V5_CARD.json"


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def file_sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def test_retry_v5_card_is_sealed_and_binds_import_path_repair() -> None:
    card = json.loads(CARD.read_text())
    claimed = card.pop("card_sha256")
    assert digest(card) == claimed
    assert card["status"] == "approved-awaiting-generation-pinned-upload"
    assert card["authorization"]["status"] == "approved-for-v5"
    assert Decimal(str(card["cost"]["incremental_upper_usd"])) < Decimal(
        str(card["cost"]["requested_incremental_ceiling_usd"])
    )
    source = card["source"]
    assert source["commit"] == "d318f595c1319e32db37ea24f9a9c94515d79fa8"
    assert source["qualifier_sha256"] == file_sha("scripts/cuda/qualify.py")
    assert source["qualification_runner_sha256"] == file_sha("scripts/cuda/run_qualification.sh")
    assert source["startup_controller_sha256"] == file_sha("scripts/cuda/gcloud_startup_gate0b.sh")
    assert source["metadata_wrapper_sha256"] == file_sha("scripts/cuda/gcloud_startup_metadata_wrapper.sh")
    assert card["repair"]["dependency_lock_sha256"] == file_sha("uv.lock")
    assert card["model"]["revision"] == "15852e8c16360a2fea060d615a32b45270f8a8fc"
