import hashlib
import json
from decimal import Decimal
from pathlib import Path


ROOT=Path(__file__).resolve().parents[2]
CARD=ROOT/"measurement/cuda/gcloud/GATE0B_RETRY_V3_CARD.json"


def digest(value: dict) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def file_sha(path: str) -> str:
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def test_retry_v3_card_is_sealed_and_preserves_historical_runtime() -> None:
    card=json.loads(CARD.read_text()); claimed=card.pop("card_sha256")
    assert digest(card)==claimed
    assert card["status"]=="prepared-awaiting-explicit-gcloud-approval"
    assert card["authorization_boundary"]["gcloud_status"]=="not-approved-by-this-card"
    assert card["resource"]["automatic_restart"] is False and card["resource"]["instance_termination_action"]=="STOP"
    assert card["runtime"]["controller_budget_seconds"]+card["runtime"]["backup_reserve_seconds"]==card["resource"]["max_run_duration_seconds"]
    assert Decimal(str(card["cost"]["cumulative_planned_upper_usd"]))<Decimal(str(card["cost"]["absolute_cumulative_ceiling_usd"]))
    source=card["source"]
    assert source["qualifier_sha256"]==file_sha("scripts/cuda/qualify.py")
    assert source["qualification_runner_sha256"]=="043bcaeb2a88f03ca64da8c1d6ae7b6226087a776ec49f838992ddcc6da39b1a"
    assert source["qualification_runner_sha256"]!=file_sha("scripts/cuda/run_qualification.sh")
    assert source["startup_controller_sha256"]==file_sha("scripts/cuda/gcloud_startup_gate0b.sh")
    assert source["metadata_wrapper_sha256"]==file_sha("scripts/cuda/gcloud_startup_metadata_wrapper.sh")
