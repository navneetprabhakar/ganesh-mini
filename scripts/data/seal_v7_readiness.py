#!/usr/bin/env python3
"""Build the remaining V7 readiness components and terminal composite seal."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v6_readiness import run_offline_v5_raw_regression
from scripts.data.repair_delta_v7_readiness import (
    CANONICAL_LANE_INTERFACES, CONTRACT_ID, inject_controller_paths,
    parse_response_json, response_schema, validate_lane_interface, validate_response,
)
from scripts.data.run_repair_delta_evidence import _response_schema


ROLES = ["primary_discrimination", "cross_cutting"]


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_report(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop("report_sha256", None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: report seal mismatch")
    if value.get("status") != "passed" or value.get("evaluation_artifacts_read") != 0:
        raise ValueError(f"{path}: readiness component did not pass cleanly")
    return value


def _write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--v5-raw-dir", type=Path, required=True)
    parser.add_argument("--v5-terminal-artifacts", type=Path, required=True)
    parser.add_argument("--v6-live-run", type=Path, required=True)
    parser.add_argument("--v6-failure", type=Path, required=True)
    parser.add_argument("--carry", type=Path, required=True)
    parser.add_argument("--cohort", type=Path, required=True)
    parser.add_argument("--staging", type=Path, required=True)
    parser.add_argument("--live-smoke", type=Path, required=True)
    parser.add_argument("--canaries", type=Path, required=True)
    parser.add_argument("--readiness-dir", type=Path, required=True)
    args = parser.parse_args()
    plan_sha = _file_sha(args.plan)

    historical = run_offline_v5_raw_regression(
        sorted(args.v5_raw_dir.glob("*.test_author.json")), args.v5_terminal_artifacts,
    )
    offline = {
        "schema_version": "ganesh-mini-gate2-v7-offline-v5-regression/v1",
        "contract_id": CONTRACT_ID,
        "status": "passed",
        "historical_v6_diagnostic_report_sha256": historical["report_sha256"],
        "coverage": historical["coverage"],
        "evaluation_artifacts_read": 0,
    }
    offline["report_sha256"] = canonical_sha256(offline)
    _write(args.readiness_dir / "offline-v5-regression.json", offline)

    v6_run = json.loads(args.v6_live_run.read_text(encoding="utf-8"))
    response = v6_run["response"]
    validate_response(response)
    injection = inject_controller_paths("javascript", response)
    for malformed in (
        {"primary_discrimination": response["primary_discrimination"]},
        {**response, "extra": {}},
    ):
        try:
            validate_response(malformed)
        except ValueError:
            pass
        else:
            raise ValueError("V7 exact-key negative regression unexpectedly passed")
    duplicate_text = json.dumps(response)[:-1] + ',"cross_cutting":{"content":"x","case_ids":["x"]}}'
    try:
        parse_response_json(duplicate_text)
    except ValueError:
        pass
    else:
        raise ValueError("V7 duplicate serialized-key regression unexpectedly passed")
    order = {
        "schema_version": "ganesh-mini-gate2-v7-v6-order-regression/v1",
        "contract_id": CONTRACT_ID,
        "status": "passed",
        "v6_live_run_file_sha256": _file_sha(args.v6_live_run),
        "v6_live_run_artifact_sha256": v6_run["artifact_sha256"],
        "provider_member_order": list(response),
        "controller_role_order": [row["role"] for row in injection["roles"]],
        "exact_key_set": sorted(response),
        "missing_additional_duplicate_negatives_rejected": True,
        "evaluation_artifacts_read": 0,
    }
    if order["provider_member_order"] != ["cross_cutting", "primary_discrimination"] or order["controller_role_order"] != ROLES:
        raise ValueError("V6 order regression did not prove the corrected contract")
    order["report_sha256"] = canonical_sha256(order)
    _write(args.readiness_dir / "v6-order-regression.json", order)

    valid = {
        "primary_discrimination": {"content": "p", "case_ids": ["p1", "p2"]},
        "cross_cutting": {"content": "c", "case_ids": ["c1"]},
    }
    lane_orders = {lane: [row["role"] for row in inject_controller_paths(lane, valid)["roles"]] for lane in CANONICAL_LANE_INTERFACES}
    negative_shapes = {
        "javascript-parent": ("javascript", "require('../solution.js')"),
        "javascript-dynamic": ("javascript", "require(process.env.TARGET_MODULE)"),
        "typescript-node": ("typescript", 'import test from "node:test"; import {x} from "./solution";'),
        "typescript-strict-null": ("typescript", 'import {x} from "./solution"; let cb: (() => void) | undefined; cb();'),
        "rust-cargo": ("rust", 'include!(concat!(env!("CARGO_MANIFEST_DIR"), "/solution.rs"));'),
    }
    negatives = {name: [row["code"] for row in validate_lane_interface(lane, content)] for name, (lane, content) in negative_shapes.items()}
    if any(not codes for codes in negatives.values()) or any(order != ROLES for order in lane_orders.values()):
        raise ValueError("V7 unit fixture closure failed")
    unit = {
        "schema_version": "ganesh-mini-gate2-v7-unit-fixtures/v1",
        "contract_id": CONTRACT_ID,
        "status": "passed",
        "provider_schema_sha256": canonical_sha256(response_schema()),
        "provider_schema_has_unique_items": "uniqueItems" in repr(response_schema()),
        "lane_controller_orders": lane_orders,
        "negative_static_findings": negatives,
        "implementation_sha256": _file_sha(Path(__file__).with_name("repair_delta_v7_readiness.py")),
        "evaluation_artifacts_read": 0,
    }
    if unit["provider_schema_has_unique_items"]:
        raise ValueError("provider schema contains unsupported uniqueItems")
    unit["report_sha256"] = canonical_sha256(unit)
    _write(args.readiness_dir / "unit-fixtures.json", unit)

    delta_schema = _response_schema("delta_audit", "v7")
    delta = {
        "schema_version": "ganesh-mini-gate2-v7-delta-schema-readiness/v1",
        "contract_id": CONTRACT_ID,
        "status": "passed",
        "response_schema_sha256": canonical_sha256(delta_schema),
        "required": delta_schema["required"],
        "additional_properties": delta_schema["additionalProperties"],
        "evaluation_artifacts_read": 0,
    }
    delta["report_sha256"] = canonical_sha256(delta)
    _write(args.readiness_dir / "delta-schema-readiness.json", delta)

    components = {
        "offline_v5_raw_regression": offline,
        "v6_order_regression": order,
        "unit_fixtures": unit,
        "canonical_staging_closure": _load_report(args.staging),
        "live_provider_schema_smoke": _load_report(args.live_smoke),
        "delta_schema_readiness": delta,
        "training_only_canaries": _load_report(args.canaries),
    }
    carry = json.loads(args.carry.read_text(encoding="utf-8"))
    cohort = json.loads(args.cohort.read_text(encoding="utf-8"))
    v6_failure = json.loads(args.v6_failure.read_text(encoding="utf-8"))
    component_rows = [
        {"name": name, "status": value["status"], "report_sha256": value["report_sha256"]}
        for name, value in components.items()
    ]
    composite = {
        "schema_version": "ganesh-mini-gate2-v7-readiness-composite/v1",
        "contract_id": CONTRACT_ID,
        "plan_sha256": plan_sha,
        "status": "passed",
        "components": component_rows,
        "components_sha256": canonical_sha256(component_rows),
        "v7_carry_manifest_sha256": carry["manifest_sha256"],
        "v7_cohort_manifest_sha256": cohort["manifest_sha256"],
        "v6_readiness_failure_report_sha256": v6_failure["report_sha256"],
        "implementation_hashes": {
            path.name: _file_sha(path) for path in (
                Path(__file__), Path(__file__).with_name("repair_delta_v7_readiness.py"),
                Path(__file__).with_name("run_repair_delta_evidence.py"),
                Path(__file__).with_name("run_v7_canonical_staging_closure.py"),
                Path(__file__).with_name("run_v7_training_only_canaries.py"),
            )
        },
        "evaluation_artifacts_read": 0,
    }
    composite["report_sha256"] = canonical_sha256(composite)
    _write(args.readiness_dir / "readiness-composite.json", composite)
    print(json.dumps({"status": "passed", "report_sha256": composite["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
