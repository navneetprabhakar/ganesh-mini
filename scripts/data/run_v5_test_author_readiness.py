#!/usr/bin/env python3
"""Execute and validate sealed V5 strict test-author readiness fixtures."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v5_test_author_fixture_bundle import LANES, PLAN_SHA256, SCHEMA
from scripts.data.run_repair_delta_evidence import (
    V5_CONTRACT_ID, V5_TEST_AUTHOR_RESPONSE_SCHEMA_VERSION,
    _response_schema, _stage_prompt, add_tests_for_contract,
)
from scripts.eval.contracts import sha256_text


REPORT_SCHEMA = "ganesh-mini-v5-test-author-readiness-report/v1"


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_bundle(bundle: Any) -> dict[str, Any]:
    if not isinstance(bundle, dict):
        raise ValueError("V5 test-author fixture bundle is missing")
    body = dict(bundle)
    claimed = body.pop("bundle_sha256", None)
    positives = bundle.get("positive_fixtures")
    negatives = bundle.get("negative_fixtures")
    if (
        set(bundle) != {
            "schema_version", "contract_id", "plan_sha256", "lanes",
            "positive_fixtures", "negative_fixtures", "evaluation_artifacts_read",
            "bundle_sha256",
        }
        or claimed != canonical_sha256(body)
        or bundle.get("schema_version") != SCHEMA
        or bundle.get("contract_id") != V5_CONTRACT_ID
        or bundle.get("plan_sha256") != PLAN_SHA256
        or bundle.get("lanes") != list(LANES)
        or bundle.get("evaluation_artifacts_read") != 0
        or not isinstance(positives, list) or len(positives) != len(LANES)
        or [row.get("lane") for row in positives] != list(LANES)
        or not isinstance(negatives, list)
        or [row.get("fixture_id") for row in negatives] != [
            "reject-legacy-three-file-array", "reject-java-entrypoint",
            "reject-typescript-node-test-import", "reject-primary-dependent-cross-test",
        ]
    ):
        raise ValueError("V5 test-author fixture bundle is malformed or unsealed")
    return bundle


def run_v5_test_author_readiness(bundle: dict[str, Any]) -> dict[str, Any]:
    bundle = _validate_bundle(bundle)
    schema = _response_schema("test_author", "v5")
    if (
        schema.get("$id") != V5_TEST_AUTHOR_RESPONSE_SCHEMA_VERSION
        or schema.get("additionalProperties") is not False
        or schema.get("required") != ["primary_discrimination", "cross_cutting"]
        or set(schema.get("properties", {})) != {"primary_discrimination", "cross_cutting"}
    ):
        raise ValueError("production V5 response schema differs from the strict contract")

    positives = []
    for fixture in bundle["positive_fixtures"]:
        lane = fixture["lane"]
        prompt = _stage_prompt("test_author", {"lane": lane}, "v5")
        candidate, evidence = add_tests_for_contract(
            copy.deepcopy(fixture["candidate"]), copy.deepcopy(fixture["assignment"]),
            copy.deepcopy(fixture["response"]), fixture["run_sha256"],
        )
        test_files = [row for row in candidate["verification_task"]["files"] if row["role"] == "test"]
        if (
            len(test_files) != 2 or len(evidence.get("test_roles", [])) != 2
            or [row.get("role") for row in evidence["test_roles"]]
            != ["primary_discrimination", "cross_cutting"]
            or evidence.get("response_schema_version") != V5_TEST_AUTHOR_RESPONSE_SCHEMA_VERSION
        ):
            raise ValueError(f"positive {lane} fixture did not produce the exact two-role contract")
        positives.append({
            "fixture_id": fixture["fixture_id"], "lane": lane, "status": "passed",
            "input_sha256": canonical_sha256({
                "candidate": fixture["candidate"], "assignment": fixture["assignment"],
                "response": fixture["response"], "run_sha256": fixture["run_sha256"],
            }),
            "prompt_sha256": sha256_text(prompt),
            "candidate_sha256": canonical_sha256(candidate),
            "test_author_evidence_sha256": evidence["evidence_sha256"],
            "test_file_sha256s": [row["sha256"] for row in test_files],
        })

    negatives = []
    for fixture in bundle["negative_fixtures"]:
        try:
            add_tests_for_contract(
                copy.deepcopy(fixture["candidate"]), copy.deepcopy(fixture["assignment"]),
                copy.deepcopy(fixture["response"]), fixture["run_sha256"],
            )
        except ValueError as error:
            message = str(error)
            if fixture["expected_error"] not in message:
                raise ValueError(
                    f"{fixture['fixture_id']}: unexpected production rejection: {message}"
                ) from error
            negatives.append({
                "fixture_id": fixture["fixture_id"], "lane": fixture["lane"],
                "status": "rejected-as-required", "exception_type": type(error).__name__,
                "error": message,
                "input_sha256": canonical_sha256({
                    "candidate": fixture["candidate"], "assignment": fixture["assignment"],
                    "response": fixture["response"], "run_sha256": fixture["run_sha256"],
                }),
            })
        else:
            raise ValueError(f"{fixture['fixture_id']}: invalid response was accepted")

    bindings = {
        "fixture_bundle_sha256": bundle["bundle_sha256"],
        "fixture_builder_sha256": _file_sha256(
            ROOT / "scripts/data/build_v5_test_author_fixture_bundle.py"
        ),
        "readiness_runner_sha256": _file_sha256(Path(__file__)),
        "production_contract_implementation_sha256": _file_sha256(
            ROOT / "scripts/data/run_repair_delta_evidence.py"
        ),
        "response_schema_sha256": canonical_sha256(schema),
        "positive_results_sha256": canonical_sha256(positives),
        "negative_results_sha256": canonical_sha256(negatives),
    }
    report = {
        "schema_version": REPORT_SCHEMA, "contract_id": V5_CONTRACT_ID,
        "plan_sha256": PLAN_SHA256, "status": "passed",
        "coverage": {
            "positive_lanes": list(LANES), "positive_count": len(positives),
            "negative_fixture_ids": [row["fixture_id"] for row in negatives],
            "negative_count": len(negatives), "production_dispatcher_exercised": True,
            "strict_named_role_schema": True,
        },
        "bindings": bindings, "positive_results": positives,
        "negative_results": negatives, "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def validate_v5_test_author_readiness_report(
    report: Any, bundle: dict[str, Any],
) -> dict[str, Any]:
    bundle = _validate_bundle(bundle)
    if not isinstance(report, dict):
        raise ValueError("V5 test-author readiness report is missing")
    body = dict(report)
    claimed = body.pop("report_sha256", None)
    positives = report.get("positive_results")
    negatives = report.get("negative_results")
    coverage = report.get("coverage")
    expected_bindings = {
        "fixture_bundle_sha256": bundle["bundle_sha256"],
        "fixture_builder_sha256": _file_sha256(
            ROOT / "scripts/data/build_v5_test_author_fixture_bundle.py"
        ),
        "readiness_runner_sha256": _file_sha256(Path(__file__)),
        "production_contract_implementation_sha256": _file_sha256(
            ROOT / "scripts/data/run_repair_delta_evidence.py"
        ),
        "response_schema_sha256": canonical_sha256(_response_schema("test_author", "v5")),
        "positive_results_sha256": canonical_sha256(positives),
        "negative_results_sha256": canonical_sha256(negatives),
    }
    if (
        set(report) != {
            "schema_version", "contract_id", "plan_sha256", "status", "coverage",
            "bindings", "positive_results", "negative_results",
            "evaluation_artifacts_read", "report_sha256",
        }
        or claimed != canonical_sha256(body)
        or report.get("schema_version") != REPORT_SCHEMA
        or report.get("contract_id") != V5_CONTRACT_ID
        or report.get("plan_sha256") != PLAN_SHA256
        or report.get("status") != "passed"
        or report.get("evaluation_artifacts_read") != 0
        or not isinstance(positives, list) or len(positives) != len(LANES)
        or [row.get("lane") for row in positives] != list(LANES)
        or any(row.get("status") != "passed" for row in positives)
        or not isinstance(negatives, list) or len(negatives) != 4
        or any(row.get("status") != "rejected-as-required" for row in negatives)
        or not isinstance(coverage, dict)
        or coverage != {
            "positive_lanes": list(LANES), "positive_count": len(LANES),
            "negative_fixture_ids": [
                "reject-legacy-three-file-array", "reject-java-entrypoint",
                "reject-typescript-node-test-import", "reject-primary-dependent-cross-test",
            ],
            "negative_count": 4, "production_dispatcher_exercised": True,
            "strict_named_role_schema": True,
        }
        or report.get("bindings") != expected_bindings
    ):
        raise ValueError("V5 test-author readiness report is invalid or unbound")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
    report = run_v5_test_author_readiness(bundle)
    validate_v5_test_author_readiness_report(report, bundle)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"], "report_sha256": report["report_sha256"],
        "positive_count": report["coverage"]["positive_count"],
        "negative_count": report["coverage"]["negative_count"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
