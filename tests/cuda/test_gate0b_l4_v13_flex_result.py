from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "measurement/cuda/gcloud/20260824T161956Z"


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def load_sealed(name: str, field: str) -> dict:
    value=json.loads((RUN/name).read_text()); claimed=value.pop(field)
    assert canonical_sha256(value)==claimed
    value[field]=claimed
    return value


def test_allocator_retry_failed_before_training_and_tore_down() -> None:
    result=load_sealed("run-result.json","result_sha256")
    backup=load_sealed("backup-verification.json","verification_sha256")
    teardown=load_sealed("teardown-proof.json","proof_sha256")
    assert result["status"]=="failed-memory-capacity"
    assert result["cuda_allocator"]["hypothesis_outcome"]=="insufficient-alone"
    assert result["nf4_qlora"]["sequence_envelope_completed"] is False
    assert result["training_records_started"]==0
    assert result["optimizer_steps_completed"]==0
    assert result["billing"]["incremental_upper_usd"]<result["billing"]["approved_incremental_ceiling_usd"]
    assert backup["verified"] is True and backup["object_count"]==32
    assert backup["generation_inventory_pass_a_sha256"]==backup["generation_inventory_pass_b_sha256"]
    assert backup["runtime_inventory_pass_a"] and backup["runtime_inventory_pass_b"]
    assert teardown["instance"]["absent"] and teardown["disk"]["absent"]
    assert teardown["subnet"]["absent"] and teardown["network"]["absent"]


def test_canonical_state_documents_bind_run_backup_and_teardown_seals() -> None:
    result=load_sealed("run-result.json","result_sha256")
    backup=load_sealed("backup-verification.json","verification_sha256")
    teardown=load_sealed("teardown-proof.json","proof_sha256")
    for relative in ("docs/process/DECISIONS.md","docs/process/PROJECT_STATE.md"):
        text=(ROOT/relative).read_text()
        assert result["result_sha256"] in text
        assert backup["verification_sha256"] in text
        assert teardown["proof_sha256"] in text
