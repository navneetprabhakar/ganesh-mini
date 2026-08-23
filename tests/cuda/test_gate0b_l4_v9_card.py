from __future__ import annotations

import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CARD_PATH = ROOT / "measurement/cuda/gcloud/GATE0B_L4_V9_CARD.json"


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def commit_file_sha(commit: str, relative: str) -> str:
    data = subprocess.run(["git", "show", f"{commit}:{relative}"], cwd=ROOT, check=True, capture_output=True).stdout
    return hashlib.sha256(data).hexdigest()


def test_v6_allocator_retry_card_is_bounded_and_source_pinned() -> None:
    card = json.loads(CARD_PATH.read_text())
    claimed = card.pop("card_sha256")
    assert canonical_sha256(card) == claimed
    assert card["status"] == "approval-required"
    assert card["authorization"]["status"] == "not-approved"
    assert card["authorization"]["maximum_seconds"] == 1800
    assert Decimal(str(card["price"]["incremental_upper_usd"])) < Decimal(str(card["authorization"]["maximum_incremental_usd"]))
    change = card["measured_change"]
    assert change["sequence_length"] == 2944
    assert change["maximum_prepared_record_tokens"] <= change["sequence_length"]
    assert change["previous_nf4_reserved_unallocated_bytes"] > change["previous_nf4_shortfall_bytes"]
    assert change["cuda_allocator_config"] == "expandable_segments:True"
    assert change["allocator_contract_shared_by_qualification_and_production_sft"] is True
    assert change["recipe_parameters_other_than_allocator_changed"] is False
    source = card["source"]
    for key, relative in {
        "qualification_config_sha256": "configs/cuda/qwen3_5_2b_gate0.json",
        "training_config_sha256": "configs/train/seed_pilot.json",
        "qualifier_sha256": "scripts/cuda/qualify.py",
        "qualification_runner_sha256": "scripts/cuda/run_qualification.sh",
        "qwen_runtime_sha256": "scripts/train/qwen_runtime.py",
        "production_sft_sha256": "scripts/train/run_sft.py",
    }.items():
        assert source[key] == commit_file_sha(source["commit"], relative)
    assert card["prelaunch_requirements"]["no_gcloud_inspection_or_mutation_before_explicit_approval"] is True
