from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_RETRY_V8_CARD.json"


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def file_sha(path: str) -> str:
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def test_retry_v8_card_is_sealed_unapproved_and_binds_deep_dive_repairs() -> None:
    card=json.loads(CARD.read_text()); claimed=card.pop("card_sha256")
    assert digest(card)==claimed
    assert card["status"]=="awaiting-explicit-gcloud-approval"
    assert card["authorization"]["status"]=="not-approved-for-v8"
    assert card["predecessor"]["status"]=="superseded-before-gcloud-use"
    assert card["source"]["commit"]=="4873d337e62a57ec20ac43ff625616850a108607"
    assert card["source"]["qualifier_sha256"]==file_sha("scripts/cuda/qualify.py")
    assert card["source"]["qwen_runtime_sha256"]==file_sha("scripts/train/qwen_runtime.py")
    assert card["source"]["workspace_packager_sha256"]==file_sha("scripts/train/package_workspace.py")
    assert card["repair"]["deep_dive_evidence_file_sha256"]==file_sha("measurement/cuda/local_deep_dive_20260823.json")
    assert card["runtime"]["controller_budget_seconds"]+card["runtime"]["backup_reserve_seconds"]==card["resource"]["max_run_duration_seconds"]
    assert Decimal(str(card["cost"]["incremental_upper_usd"]))<Decimal(str(card["cost"]["requested_incremental_ceiling_usd"]))
    assert len(card["source"]["workspace_archive"]["sha256"])==64
    assert all(len(card["reused_generation_pinned_inputs"][name])==64 for name in ("image_sha256","offline_bundle_sha256","model_sha256"))
