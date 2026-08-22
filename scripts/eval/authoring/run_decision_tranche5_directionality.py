#!/usr/bin/env python3
"""Execute decision tranche-5 directionality in bounded sandboxes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.eval.authoring.build_decision_tranche5 import MANIFEST, OVERLAP, ROOT
from scripts.eval.contracts import load_json, sha256_object, validate_task, write_json
from scripts.verify.sandbox import SANDBOX_CONTRACT, verify

DEFAULT_OUTPUT = ROOT / "manifests/evaluation/private/decision-tranche5-directionality.json"
RUNTIME_CONFIG = ROOT / "configs/eval/runtimes.json"
EXPECTED_MANIFEST_SHA256 = "ee52d232e2d44411a398ad680def61ffffd54722d8a8fc400ffdd2143d4240e3"
EXPECTED_OVERLAP_SHA256 = "251cee5751463ffa76159823b3ec939a6edbd66e328336ca65e7169022186de5"


def passed(result: dict[str, Any]) -> bool:
    return not result["timed_out"] and bool(result["exit_codes"]) and all(code == 0 for code in result["exit_codes"])


def execute(entry: dict[str, Any], artifact: str) -> dict[str, Any]:
    task = validate_task(load_json(ROOT / entry["path"]))
    if sha256_object(task) != entry["sha256"]:
        raise RuntimeError(f"task hash does not match sealed manifest: {task['task_id']}")
    selected = task["validation"]["reference"] if artifact == "reference" else task["validation"]["known_bad"][0]
    verifier = verify(task, selected["code"], RUNTIME_CONFIG)
    return {
        "task_id": task["task_id"], "language": task["language"], "artifact": artifact,
        "artifact_label": selected["label"], "artifact_sha256": selected["sha256"],
        "expected_pass": artifact == "reference", "observed_pass": passed(verifier), "verifier": verifier,
    }


def summarize(manifest: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    failures = [
        {"task_id": row["task_id"], "artifact": row["artifact"], "expected_pass": row["expected_pass"],
         "observed_pass": row["observed_pass"], "timed_out": row["verifier"]["timed_out"]}
        for row in rows
        if row["expected_pass"] != row["observed_pass"] or row["verifier"]["timed_out"]
    ]
    evidence = {
        "schema_version": "ganesh-mini-directionality-evidence/v1",
        "evaluation_manifest": str(MANIFEST.relative_to(ROOT)),
        "evaluation_manifest_sha256": manifest["manifest_sha256"],
        "overlap_report": str(OVERLAP.relative_to(ROOT)),
        "overlap_report_sha256": EXPECTED_OVERLAP_SHA256,
        "runtime_config": str(RUNTIME_CONFIG.relative_to(ROOT)),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        "execution_mode": "sequential",
        "task_count": manifest["task_count"], "execution_count": len(rows),
        "reference_passes": sum(row["artifact"] == "reference" and row["observed_pass"] for row in rows),
        "known_bad_rejections": sum(row["artifact"] == "known_bad" and not row["observed_pass"] for row in rows),
        "failures": failures, "status": "passed" if not failures else "failed", "executions": rows,
    }
    evidence["evidence_sha256"] = sha256_object(evidence)
    return evidence


def run(output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    manifest = load_json(MANIFEST); claimed = manifest["manifest_sha256"]
    if claimed != EXPECTED_MANIFEST_SHA256 or sha256_object({key: value for key, value in manifest.items() if key != "manifest_sha256"}) != claimed:
        raise RuntimeError("decision tranche5 manifest hash mismatch")
    overlap = load_json(OVERLAP); overlap_claimed = overlap["report_sha256"]
    if overlap_claimed != EXPECTED_OVERLAP_SHA256 or sha256_object({key: value for key, value in overlap.items() if key != "report_sha256"}) != overlap_claimed:
        raise RuntimeError("decision tranche5 overlap seal mismatch")
    if overlap["status"] != "passed" or overlap["evaluation_manifest"] != str(MANIFEST.relative_to(ROOT)) or overlap["evaluation_manifest_sha256"] != claimed:
        raise RuntimeError("decision tranche5 is not bound by the passed overlap seal")
    if SANDBOX_CONTRACT.get("backend") != "docker" or SANDBOX_CONTRACT.get("network") != "none" or SANDBOX_CONTRACT.get("pull") != "never":
        raise RuntimeError("directionality requires the pinned network-none Docker sandbox")
    rows: list[dict[str, Any]] = []
    for entry in manifest["tasks"]:
        rows.append(execute(entry, "reference")); rows.append(execute(entry, "known_bad"))
    evidence = summarize(manifest, rows); write_json(output, evidence); return evidence


def reference_preflight() -> dict[str, Any]:
    manifest = load_json(MANIFEST)
    claimed = manifest["manifest_sha256"]
    if claimed != EXPECTED_MANIFEST_SHA256 or sha256_object({key: value for key, value in manifest.items() if key != "manifest_sha256"}) != claimed:
        raise RuntimeError("decision tranche5 manifest hash mismatch")
    rows = [execute(entry, "reference") for entry in manifest["tasks"]]
    failures = [row["task_id"] for row in rows if not row["observed_pass"] or row["verifier"]["timed_out"]]
    return {"status": "passed" if not failures else "failed", "execution_count": len(rows), "reference_passes": len(rows) - len(failures), "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT); parser.add_argument("--reference-only", action="store_true"); args = parser.parse_args()
    if args.reference_only:
        preflight = reference_preflight(); print(json.dumps(preflight, sort_keys=True)); return int(preflight["status"] != "passed")
    evidence = run(args.output)
    print(json.dumps({key: evidence[key] for key in ("status", "execution_count", "reference_passes", "known_bad_rejections", "evidence_sha256")}, sort_keys=True))
    return int(evidence["status"] != "passed")


if __name__ == "__main__":
    raise SystemExit(main())
