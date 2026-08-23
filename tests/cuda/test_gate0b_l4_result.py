from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "measurement/cuda/gcloud/20260823T145734Z"


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_sealed(path: Path, field: str) -> dict:
    value = json.loads(path.read_text())
    claimed = value.pop(field)
    assert canonical_sha256(value) == claimed
    value[field] = claimed
    return value


def test_l4_result_is_fail_closed_backed_up_and_torn_down() -> None:
    result = load_sealed(RUN / "run-result.json", "evidence_sha256")
    manifest = load_sealed(RUN / "gcs-backup-manifest.json", "evidence_sha256")
    absence = load_sealed(RUN / "postdelete-absence-proof.json", "evidence_sha256")
    primary = load_sealed(RUN / "runtime-verified/qualification-bf16-lora-primary-v1.json", "evidence_sha256")
    fallback = load_sealed(RUN / "runtime-verified/qualification-nf4-qlora-fallback-v1.json", "evidence_sha256")

    assert result["status"] == "failed-memory-capacity"
    assert result["claims"] == {
        "gate0b_passed": False,
        "optimizer_steps": 0,
        "training_records_started": 0,
        "training_complete": False,
    }
    assert primary["error_type"] == fallback["error_type"] == "OutOfMemoryError"
    assert result["primary"]["evidence_sha256"] == primary["evidence_sha256"]
    assert result["fallback"]["evidence_sha256"] == fallback["evidence_sha256"]
    assert manifest["status"] == "verified" and manifest["object_count"] == 32
    assert result["backup"]["manifest_evidence_sha256"] == manifest["evidence_sha256"]
    assert absence["status"] == "passed" and len(absence["queries"]) == 4
    assert result["teardown"]["absence_proof_sha256"] == absence["evidence_sha256"]
