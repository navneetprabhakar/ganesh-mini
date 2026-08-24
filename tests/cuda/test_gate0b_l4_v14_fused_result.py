from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "measurement/cuda/gcloud/20260824T180957Z"


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_sealed(name: str) -> dict:
    value = json.loads((RUN / name).read_text())
    claimed = value.pop("evidence_sha256")
    assert canonical_sha256(value) == claimed
    value["evidence_sha256"] = claimed
    return value


def test_fused_loss_gate0b_passed_and_artifacts_are_double_verified() -> None:
    result = load_sealed("run-result.json")
    backup = load_sealed("backup-verification.json")
    inventory = load_sealed("inventory-verification.json")
    teardown = load_sealed("teardown-proof.json")

    assert result["status"] == "passed"
    qualification = result["qualification"]
    assert qualification["status"] == "passed"
    assert qualification["records_completed"] == 16
    assert qualification["optimizer_steps"] == 16
    assert qualification["observed_peak_vram_bytes"] < qualification["maximum_peak_vram_bytes"]
    assert qualification["fused_training_loss"]["materialize_training_logits"] is False
    assert qualification["fused_training_loss"]["other_liger_kernels_enabled"] is False
    assert qualification["serialization_equivalence"]["passed"] is True

    assert backup["status"] == "verified" and backup["object_count"] == 41
    assert all(row["local_sha256"] == row["downloaded_sha256"] == row["verified_download_sha256"] for row in backup["objects"])
    assert inventory["inventory_entries"] == 40
    assert inventory["missing_entries"] == inventory["hash_mismatches"] == 0
    assert result["cost"]["incremental_upper_usd"] < result["cost"]["approved_ceiling_usd"]
    assert all(teardown["absence"].values())


def test_state_documents_bind_fused_loss_result_seals() -> None:
    values = [
        load_sealed("run-result.json")["evidence_sha256"],
        load_sealed("backup-verification.json")["evidence_sha256"],
        load_sealed("teardown-proof.json")["evidence_sha256"],
    ]
    for relative in ("docs/process/DECISIONS.md", "docs/process/PROJECT_STATE.md"):
        text = (ROOT / relative).read_text()
        assert all(value in text for value in values)
