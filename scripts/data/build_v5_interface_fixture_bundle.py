#!/usr/bin/env python3
"""Build generated-shape fixtures for the V5 witness/runtime interface."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v4_tooling_fixture_bundle import build_fixture_bundle
from scripts.data.repair_delta_v5_preflight import CONTRACT_ID, PLAN_SHA256
from scripts.eval.contracts import sha256_text


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "ganesh-mini-v5-interface-fixture-bundle/v1"
LANES = ("go", "java", "javascript", "rust")


def _reseal(value: dict[str, Any]) -> None:
    value.pop("evidence_sha256", None)
    value["evidence_sha256"] = canonical_sha256(value)


def build_v5_interface_fixture_bundle() -> dict[str, Any]:
    v4 = build_fixture_bundle()
    fixtures = []
    marker = "GANESH_V4_KNOWN_BAD_CROSS_WITNESS_PASS"
    for lane in LANES:
        source = next(
            row for row in v4["fixtures"]
            if row.get("expected") == "admitted"
            and row["envelope"]["candidate"]["lane"] == lane
        )
        envelope = copy.deepcopy(source["envelope"])
        candidate = envelope["candidate"]
        candidate["verification_task"]["files"] = [
            row for row in candidate["verification_task"]["files"]
            if row["role"] == "support"
        ]
        proof = envelope["evidence"]["teacher_proof"]
        witness = proof["known_bad_cross_witness"]
        if lane == "javascript":
            content = f'''"use strict";
const assert = require("assert");
const reference = require("./reference.js");
const knownBad = require("./known_bad.js");
assert.throws(() => reference.computeTotal([]), TypeError);
assert.throws(() => knownBad.computeTotal([]), TypeError);
console.log("{marker}");
'''
            witness["content"] = content
            witness["content_sha256"] = sha256_text(content)
        elif lane == "rust":
            content = f'''mod solution;
fn main() {{
    assert!(solution::compute_total(&[]).is_err());
    println!("{marker}");
}}
'''
            witness["content"] = content
            witness["content_sha256"] = sha256_text(content)
        _reseal(proof)
        assignment = copy.deepcopy(envelope["assignment"])
        assignment["contract_id"] = CONTRACT_ID
        fixtures.append({
            "fixture_id": f"v5-interface-{lane}", "lane": lane,
            "candidate": candidate, "assignment": assignment, "teacher_proof": proof,
        })
    bundle = {
        "schema_version": SCHEMA, "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256, "fixtures": fixtures,
        "negative_contracts": {
            "go_timeout_not_120": "reject-before-execution",
            "javascript_missing_dual_artifact": "reject-before-execution",
            "rust_test_harness_command": "reject-config",
        },
    }
    bundle["bundle_sha256"] = canonical_sha256(bundle)
    return bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    bundle = build_v5_interface_fixture_bundle()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"fixtures": len(bundle["fixtures"]), "bundle_sha256": bundle["bundle_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
