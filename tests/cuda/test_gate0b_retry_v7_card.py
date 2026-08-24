from __future__ import annotations

import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_RETRY_V7_CARD.json"


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def file_sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def commit_file_sha(commit: str, path: str) -> str:
    return hashlib.sha256(subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)).hexdigest()


def test_retry_v7_card_is_sealed_unapproved_and_superseded_by_deep_dive_repairs() -> None:
    card = json.loads(CARD.read_text())
    claimed = card.pop("card_sha256")
    assert digest(card) == claimed
    assert card["status"] == "awaiting-explicit-gcloud-approval"
    assert card["authorization"]["status"] == "not-approved-for-v7"
    assert Decimal(str(card["cost"]["incremental_upper_usd"])) < Decimal(
        str(card["cost"]["requested_incremental_ceiling_usd"])
    )
    source = card["source"]
    assert source["commit"] == "2c509c77b07f6cc4b8dfe93ddd21d743ca51d93d"
    assert source["qualifier_sha256"] != file_sha("scripts/cuda/qualify.py")
    assert source["qualification_runner_sha256"] == commit_file_sha(source["commit"],"scripts/cuda/run_qualification.sh")
    assert source["startup_controller_sha256"] == commit_file_sha(source["commit"],"scripts/cuda/gcloud_startup_gate0b.sh")
    assert source["metadata_wrapper_sha256"] == commit_file_sha(source["commit"],"scripts/cuda/gcloud_startup_metadata_wrapper.sh")
    assert card["repair"]["dependency_lock_sha256"] == "ef71c0477c214d01c5fade799c1832a05014f89f643ee92fea8f0399988f85ba"
    assert card["repair"]["dependency_lock_sha256"] != file_sha("uv.lock")
    assert card["model"]["revision"] == "15852e8c16360a2fea060d615a32b45270f8a8fc"
