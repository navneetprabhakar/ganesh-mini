from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "measurement/cuda/gcloud/20260824T160620Z"


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_sealed(name: str, field: str) -> dict:
    value = json.loads((RUN / name).read_text())
    claimed = value.pop(field)
    assert canonical_sha256(value) == claimed
    value[field] = claimed
    return value


def test_flex_start_rejection_created_no_billable_runtime_and_tore_down() -> None:
    result = load_sealed("run-result.json", "result_sha256")
    backup = load_sealed("backup-verification.json", "verification_sha256")
    teardown = load_sealed("teardown-proof.json", "proof_sha256")
    assert result["status"] == "flex-start-rejected-before-running"
    assert result["provisioning_model"] == "FLEX_START"
    assert result["pending_state_observed"] is True
    assert result["running_state_observed"] is False
    assert result["qualification_started"] is False
    assert result["compute_billable_seconds"] == 0
    assert result["compute_cost_usd"] == 0
    assert result["allocator_hypothesis_tested"] is False
    assert backup["verified"] is True
    assert backup["object_count"] == 6
    assert backup["manifest_a_sha256"] == backup["manifest_b_sha256"]
    assert teardown["pending_request"]["terminal"] is True
    assert teardown["instance"]["absent"] and teardown["disk"]["absent"]
    assert teardown["subnet"]["absent"] and teardown["network"]["absent"]
    assert teardown["matching_routers_absent"] is True
