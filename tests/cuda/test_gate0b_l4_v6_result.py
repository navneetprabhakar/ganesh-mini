from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "measurement/cuda/gcloud/20260823T165923Z"


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_sealed(name: str, seal: str) -> dict:
    value = json.loads((RUN / name).read_text())
    claimed = value.pop(seal)
    assert canonical_sha256(value) == claimed
    value[seal] = claimed
    return value


def test_v4_retry_result_backup_and_teardown_are_fail_closed() -> None:
    result = load_sealed("run-result.json", "result_sha256")
    backup = load_sealed("backup-verification.json", "verification_sha256")
    teardown = load_sealed("teardown-proof.json", "proof_sha256")
    assert result["status"] == "failed-memory-capacity"
    assert result["training_records_started"] == 0
    assert result["optimizer_steps_completed"] == 0
    assert result["bf16_lora"]["error_type"] == "OutOfMemoryError"
    assert result["nf4_qlora"]["error_type"] == "OutOfMemoryError"
    assert result["nf4_qlora"]["shortfall_bytes"] > 0
    assert Decimal(str(result["billing"]["compute_upper_usd"])) < Decimal(str(result["billing"]["approved_incremental_ceiling_usd"]))
    assert backup["verified"] is True
    assert backup["object_count"] == 32
    assert backup["manifest_a_sha256"] == backup["manifest_b_sha256"]
    assert backup["runtime_inventory_pass_a"] is True
    assert backup["runtime_inventory_pass_b"] is True
    assert teardown["checked_after_verified_backup"] is True
    assert all(teardown[key]["absent"] for key in ("instance", "disk", "subnet", "network"))
