#!/usr/bin/env python3
"""Seal the terminal V6 pre-campaign readiness failure."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v6_readiness import CONTRACT_ID, validate_response


REPORT_SCHEMA = "ganesh-mini-gate2-v6-readiness-failure/v1"
EXPECTED_PLAN_SHA256 = "4fe6a1374c01a0a682bf256c91a141b36b26680bdb5279049070f4f143418ec1"
EXPECTED_CARRY_SEAL = "f95270299363fe003e0f8b747f60071eb813d36b09c9c132198588625a2be8af"
EXPECTED_COHORT_SEAL = "188d3b5b3e95f71556321dc1262251375d641d8e23b3961c713985b81eb7e9de"
EXPECTED_SMOKE_FILE_SHA256 = "24a0749d8de8d16907c2fb7814169ef64048d76d03b3d248a8cdf92d8e9d305e"
EXPECTED_SMOKE_ARTIFACT_SEAL = "2582bfa6b9e1dd98ec7994e31ab129ee4b400fb2947bc1facfc85394b5f54730"
EXPECTED_RESPONSE_SCHEMA_SHA256 = "7faee5a48a1750563d1c47aaea77a488a97943bcba1bf1fac489274343a52822"
FAILURE_REASON = "json-object-order-validator-impossible-contract"
VALIDATOR_ERROR = "V6 response must contain the two ordered role objects exactly"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_sealed(path: Path, seal_field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    body = dict(value)
    claimed = body.pop(seal_field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {seal_field}")
    return value


def build_report(
    plan: Path, carry_path: Path, cohort_path: Path, smoke_path: Path,
) -> dict[str, Any]:
    plan_hash = file_sha256(plan)
    carry = load_sealed(carry_path, "manifest_sha256")
    cohort = load_sealed(cohort_path, "manifest_sha256")
    smoke = load_sealed(smoke_path, "artifact_sha256")
    smoke_file_hash = file_sha256(smoke_path)

    if plan_hash != EXPECTED_PLAN_SHA256:
        raise ValueError("V6 plan hash differs from the frozen canonical plan")
    if (
        carry.get("contract_id") != CONTRACT_ID
        or carry.get("plan_sha256") != plan_hash
        or carry.get("manifest_sha256") != EXPECTED_CARRY_SEAL
        or carry.get("records") != 60
    ):
        raise ValueError("V6 carry manifest differs from the frozen 60-record carry")
    if (
        cohort.get("contract_id") != CONTRACT_ID
        or cohort.get("plan_sha256") != plan_hash
        or cohort.get("manifest_sha256") != EXPECTED_COHORT_SEAL
        or cohort.get("records") != 60
    ):
        raise ValueError("V6 cohort manifest differs from the frozen ordered cohort")
    if (
        smoke_file_hash != EXPECTED_SMOKE_FILE_SHA256
        or smoke.get("artifact_sha256") != EXPECTED_SMOKE_ARTIFACT_SEAL
        or smoke.get("contract_version") != "v6"
        or smoke.get("response_schema_sha256") != EXPECTED_RESPONSE_SCHEMA_SHA256
        or smoke.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("V6 live schema smoke differs from the preserved raw artifact")
    attempts = smoke.get("invocation_attempts")
    if (
        not isinstance(attempts, list)
        or len(attempts) != 1
        or attempts[0].get("outcome") != "structured-response"
        or smoke.get("run", {}).get("returncode") != 0
        or not isinstance(smoke.get("response"), dict)
    ):
        raise ValueError("V6 live schema smoke does not prove one terminal structured response")

    try:
        validate_response(smoke["response"])
    except ValueError as exc:
        validator_error = str(exc)
        exception_type = type(exc).__name__
    else:
        raise ValueError("V6 live response no longer reproduces the frozen readiness failure")
    if validator_error != VALIDATOR_ERROR:
        raise ValueError("V6 live response produced a different local validator failure")

    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA,
        "contract_id": CONTRACT_ID,
        "status": "readiness-failed",
        "reason": FAILURE_REASON,
        "failed_readiness_step": "content-free-live-provider-schema-admission-smoke",
        "frozen_inputs": {
            "plan": {"path": str(plan), "sha256": plan_hash},
            "carry_manifest": {
                "path": str(carry_path),
                "file_sha256": file_sha256(carry_path),
                "manifest_sha256": carry["manifest_sha256"],
            },
            "cohort_manifest": {
                "path": str(cohort_path),
                "file_sha256": file_sha256(cohort_path),
                "manifest_sha256": cohort["manifest_sha256"],
            },
        },
        "live_schema_smoke": {
            "raw_artifact": {
                "path": str(smoke_path),
                "file_sha256": smoke_file_hash,
                "artifact_sha256": smoke["artifact_sha256"],
            },
            "response_schema_sha256": smoke["response_schema_sha256"],
            "provider_schema_admitted": True,
            "structured_response_observed": True,
            "invocation_attempts": 1,
            "response_key_order": list(smoke["response"]),
            "local_validation": {
                "status": "failed",
                "exception_type": exception_type,
                "error": validator_error,
            },
        },
        "campaign_accounting": {
            "candidate_test_author_calls": 0,
            "blind_delta_audit_calls": 0,
            "structural_reauthor_calls": 0,
            "candidate_suite_executions": 0,
            "candidate_dispositions": 0,
            "qualification_metrics_emitted": False,
            "evaluation_artifacts_read": 0,
        },
        "boundary": {
            "failure_phase": "pre-campaign-readiness",
            "candidate_campaign_started": False,
            "v6_candidate_outputs_created": 0,
            "v6_tests_admitted": 0,
            "v6_terminal": True,
        },
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def validate_report(report: dict[str, Any]) -> dict[str, Any]:
    body = dict(report)
    claimed = body.pop("report_sha256", None)
    if claimed != canonical_sha256(body):
        raise ValueError("invalid V6 readiness-failure report seal")
    if (
        report.get("schema_version") != REPORT_SCHEMA
        or report.get("contract_id") != CONTRACT_ID
        or report.get("status") != "readiness-failed"
        or report.get("reason") != FAILURE_REASON
        or report.get("campaign_accounting") != {
            "candidate_test_author_calls": 0,
            "blind_delta_audit_calls": 0,
            "structural_reauthor_calls": 0,
            "candidate_suite_executions": 0,
            "candidate_dispositions": 0,
            "qualification_metrics_emitted": False,
            "evaluation_artifacts_read": 0,
        }
    ):
        raise ValueError("invalid V6 readiness-failure accounting")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--carry-manifest", type=Path, required=True)
    parser.add_argument("--cohort-manifest", type=Path, required=True)
    parser.add_argument("--live-smoke", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(args.plan, args.carry_manifest, args.cohort_manifest, args.live_smoke)
    validate_report(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
