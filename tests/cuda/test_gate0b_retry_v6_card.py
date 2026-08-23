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


def test_retry_v6_card_is_sealed_and_binds_historical_swift_repair() -> None:
    card = json.loads(CARD.read_text())
    claimed = card.pop("card_sha256")
    assert digest(card) == claimed
    assert card["status"] == "approved-awaiting-generation-pinned-upload"
    assert card["authorization"]["status"] == "approved-for-v6"
    assert Decimal(str(card["cost"]["incremental_upper_usd"])) < Decimal(
        str(card["cost"]["requested_incremental_ceiling_usd"])
    )
    source = card["source"]
    assert source["commit"] == "2423f4e7e9c37590b77128318dc3b7416111cb00"
    assert source["qualifier_sha256"] == "778a5b2fabcc6aaa146b43767197c451f85f6177382df265fdf291ca6ed749a5"
    assert source["qualification_runner_sha256"] == "4c2fa94b46e2f7377b7dbf6d7a261ef39dde79143fea8f900bb25548b5115b7c"
    assert source["startup_controller_sha256"] == "7f509d2cd7cfb91696e88942770f2207847862905f1337ace15edba2abaca7ea"
    assert source["metadata_wrapper_sha256"] == "070e41dd232823fac1d11f43d02c2811a5e063b5bc17738440fd73c89681932c"
    assert card["repair"]["dependency_lock_sha256"] == "ef71c0477c214d01c5fade799c1832a05014f89f643ee92fea8f0399988f85ba"
    assert card["model"]["revision"] == "15852e8c16360a2fea060d615a32b45270f8a8fc"
