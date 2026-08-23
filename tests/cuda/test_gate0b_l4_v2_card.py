from __future__ import annotations

import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/GATE0B_L4_V2_CARD.json"


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def commit_file_sha(commit: str, path: str) -> str:
    return hashlib.sha256(subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)).hexdigest()


def test_l4_v2_card_is_sealed_and_binds_zone_only_retry() -> None:
    card = json.loads(CARD.read_text())
    claimed = card.pop("card_sha256")
    assert digest(card) == claimed
    assert card["authorization"]["status"] == "same-approved-infrastructure-zone-only-retry"
    assert card["predecessor"]["outcome"] == "us-central1-b capacity failure before VM or disk creation"
    assert card["resource"]["zone"] == "us-central1-a"
    assert card["resource"]["machine_type"] == "g2-standard-8"
    assert card["resource"]["provisioning_model"] == "STANDARD"
    assert Decimal(str(card["cost"]["incremental_upper_usd"])) < Decimal(str(card["cost"]["absolute_incremental_ceiling_usd"]))
    commit = card["source"]["commit"]
    assert card["source"]["qualifier_sha256"] == commit_file_sha(commit, "scripts/cuda/qualify.py")
    assert card["source"]["qualification_runner_sha256"] == commit_file_sha(commit, "scripts/cuda/run_qualification.sh")
    assert card["source"]["startup_controller_sha256"] == commit_file_sha(commit, "scripts/cuda/gcloud_startup_gate0b.sh")
    assert card["source"]["metadata_wrapper_sha256"] == commit_file_sha(commit, "scripts/cuda/gcloud_startup_metadata_wrapper.sh")
    assert card["source"]["qualification_config_sha256"] == commit_file_sha(commit, "configs/cuda/qwen3_5_2b_gate0.json")
