from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.seal_v6_readiness_failure import (
    FAILURE_REASON, REPORT_SCHEMA, VALIDATOR_ERROR, build_report, validate_report,
)


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "docs/plans/GATE2_REPAIR_DELTA_V6_CANONICAL_TEST_REPLAY_PLAN_20260917.md"
BASE = ROOT / "measurement/gate2/capability-stratified-v6-canonical-test-replay"
CARRY = BASE / "cohort-v1/carry-manifest.json"
COHORT = BASE / "cohort-v1/cohort-manifest.json"
SMOKE = BASE / "readiness-v1/live-schema-runs/v6-live-schema-smoke.test_author.json"


def test_build_report_seals_exact_pre_campaign_failure() -> None:
    report = build_report(PLAN, CARRY, COHORT, SMOKE)
    assert validate_report(report) is report
    assert report["schema_version"] == REPORT_SCHEMA
    assert report["status"] == "readiness-failed"
    assert report["reason"] == FAILURE_REASON
    assert report["live_schema_smoke"]["provider_schema_admitted"] is True
    assert report["live_schema_smoke"]["structured_response_observed"] is True
    assert report["live_schema_smoke"]["response_key_order"] == [
        "cross_cutting", "primary_discrimination",
    ]
    assert report["live_schema_smoke"]["local_validation"] == {
        "status": "failed",
        "exception_type": "ValueError",
        "error": VALIDATOR_ERROR,
    }
    accounting = report["campaign_accounting"]
    assert accounting["candidate_test_author_calls"] == 0
    assert accounting["blind_delta_audit_calls"] == 0
    assert accounting["structural_reauthor_calls"] == 0
    assert accounting["evaluation_artifacts_read"] == 0
    assert report["boundary"]["candidate_campaign_started"] is False


def test_validate_report_rejects_tampering() -> None:
    report = build_report(PLAN, CARRY, COHORT, SMOKE)
    tampered = copy.deepcopy(report)
    tampered["campaign_accounting"]["candidate_test_author_calls"] = 1
    with pytest.raises(ValueError, match="seal"):
        validate_report(tampered)


def test_build_report_rejects_different_smoke(tmp_path: Path) -> None:
    smoke = json.loads(SMOKE.read_text(encoding="utf-8"))
    smoke["response_schema_sha256"] = "0" * 64
    smoke.pop("artifact_sha256")
    smoke["artifact_sha256"] = canonical_sha256(smoke)
    path = tmp_path / "smoke.json"
    path.write_text(json.dumps(smoke, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="preserved raw artifact"):
        build_report(PLAN, CARRY, COHORT, path)
