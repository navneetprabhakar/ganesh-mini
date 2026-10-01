#!/usr/bin/env python3
"""Execute and seal V7's six-lane, exact 24-suite staging closure."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v7_readiness import CONTRACT_ID, validate_lane_interface
from scripts.data.run_repair_delta_evidence import _executable_evidence
from scripts.eval.contracts import sha256_text
from scripts.verify.sandbox import verify


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
EXPECTED = {
    "reference.primary_discrimination": "pass",
    "reference.cross_cutting": "pass",
    "known_bad.primary_discrimination": "fail",
    "known_bad.cross_cutting": "pass",
}


def _canonicalize_binding(lane: str, content: str) -> str:
    if lane == "javascript":
        content = content.replace('require("./solution")', 'require("./solution.js")')
        content = content.replace("require('./solution')", "require('./solution.js')")
    if lane == "rust" and '#[path = "solution.rs"] mod solution;' not in content:
        content = content.replace("mod solution;", '#[path = "solution.rs"] mod solution;')
    return content


def _prepare(candidate: dict[str, Any], evidence: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = copy.deepcopy(candidate)
    evidence = copy.deepcopy(evidence)
    lane = candidate["lane"]
    roles = {row["path"]: row for row in evidence["test_roles"]}
    for file in candidate["verification_task"]["files"]:
        if file.get("role") != "test":
            continue
        file["content"] = _canonicalize_binding(lane, file["content"])
        file["sha256"] = sha256_text(file["content"])
        roles[file["path"]]["file_sha256"] = file["sha256"]
        findings = validate_lane_interface(lane, file["content"])
        if findings:
            raise ValueError(f"{lane}/{file['path']}: canonical fixture rejected: {findings}")
    return candidate, evidence


def _outcomes(executable: dict[str, Any]) -> dict[str, str]:
    outcomes = {}
    for implementation in ("reference", "known_bad"):
        for role in ("primary_discrimination", "cross_cutting"):
            result = executable["results"][implementation][role]
            outcomes[f"{implementation}.{role}"] = (
                "pass" if result.get("exit_codes") and all(code == 0 for code in result["exit_codes"]) else "fail"
            )
    return outcomes


def build_report(bundle: dict[str, Any], runtime_path: Path, bundle_file_sha256: str) -> dict[str, Any]:
    positives = [row for row in bundle["fixtures"] if row.get("expected") == "admitted"]
    if len(positives) != 6 or {row["envelope"]["candidate"]["lane"] for row in positives} != set(LANES):
        raise ValueError("staging fixture input lacks exact six-lane coverage")
    rows = []
    executions = 0
    for fixture in sorted(positives, key=lambda row: LANES.index(row["envelope"]["candidate"]["lane"])):
        envelope = fixture["envelope"]
        candidate, test_evidence = _prepare(envelope["candidate"], envelope["evidence"]["test_author"])
        executable, retry = _executable_evidence(candidate, test_evidence, runtime_path, verify)
        attempt_count = sum(len(row["attempts"]) for row in retry["attempts"])
        executions += attempt_count
        outcomes = _outcomes(executable)
        if retry["unresolved"] or attempt_count != 4 or outcomes != EXPECTED:
            raise ValueError(f"{candidate['lane']}: exact staging matrix failed: {outcomes}")
        rows.append({
            "lane": candidate["lane"],
            "fixture_id": fixture["fixture_id"],
            "candidate_sha256": canonical_sha256(candidate),
            "test_author_projection_sha256": canonical_sha256(test_evidence),
            "executable_evidence_sha256": executable["evidence_sha256"],
            "retry_ledger_sha256": retry["ledger_sha256"],
            "sandbox_suite_executions": attempt_count,
            "outcomes": outcomes,
        })
    negative_fixtures = {
        "js-parent": ("javascript", "require('../solution.js')"),
        "js-index": ("javascript", "require('./index.js')"),
        "js-dynamic": ("javascript", "require(process.env.TARGET_MODULE || process.argv[2])"),
        "ts-parent": ("typescript", 'import { x } from "../solution";'),
        "ts-node": ("typescript", 'import test from "node:test"; import { x } from "./solution";'),
        "ts-strict-null": ("typescript", 'import { x } from "./solution"; let release: (() => void) | undefined; release();'),
        "rust-parent": ("rust", '#[path = "../solution.rs"] mod solution;'),
        "rust-cargo": ("rust", 'include!(concat!(env!("CARGO_MANIFEST_DIR"), "/solution.rs"));'),
    }
    negatives = []
    for identifier, (lane, content) in negative_fixtures.items():
        findings = validate_lane_interface(lane, content)
        if not findings:
            raise ValueError(f"negative fixture unexpectedly passed: {identifier}")
        negatives.append({"id": identifier, "lane": lane, "finding_codes": [row["code"] for row in findings]})
    report = {
        "schema_version": "ganesh-mini-gate2-v7-canonical-staging-closure/v1",
        "contract_id": CONTRACT_ID,
        "status": "passed",
        "coverage": {"lanes": list(LANES), "sandbox_suite_executions": executions, "matrix": EXPECTED},
        "rows": rows,
        "rows_sha256": canonical_sha256(rows),
        "negative_fixtures": negatives,
        "negative_fixtures_sha256": canonical_sha256(negatives),
        "input_bundle_file_sha256": bundle_file_sha256,
        "runtime_config_sha256": hashlib.sha256(runtime_path.read_bytes()).hexdigest(),
        "evaluation_artifacts_read": 0,
    }
    if executions != 24:
        raise ValueError(f"expected exactly 24 sandbox executions, observed {executions}")
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--runtimes", type=Path, default=Path("configs/eval/runtimes.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.fixtures.read_bytes()
    report = build_report(json.loads(raw), args.runtimes, hashlib.sha256(raw).hexdigest())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
