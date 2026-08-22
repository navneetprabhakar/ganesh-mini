#!/usr/bin/env python3
"""Execute decision tranche-1 directionality sequentially in bounded sandboxes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.eval.authoring.build_decision_tranche1 import MANIFEST, ROOT
from scripts.eval.contracts import load_json, sha256_object, validate_task, write_json
from scripts.verify.sandbox import verify

DEFAULT_OUTPUT = ROOT / "manifests/evaluation/private/decision-tranche1-directionality.json"
RUNTIME_CONFIG = ROOT / "configs/eval/runtimes.json"
CROSS_TRANCHE_OVERLAP = ROOT / "manifests/evaluation/private/decision-tranches1-2-cross-overlap.json"
EXPECTED_MANIFEST_SHA256 = "4202928ddd2168fed9bb331c027244cce538a1c14f71b3fa7cf842f7698ca110"
EXPECTED_CROSS_TRANCHE_SHA256 = "2c9d3dd4c91b846f95adf437c79ae6d52543e030d5a35a6317b828ba42116cf3"


def passed(result: dict[str, Any]) -> bool:
    return not result["timed_out"] and bool(result["exit_codes"]) and all(code == 0 for code in result["exit_codes"])


def execute(entry: dict[str, Any], artifact: str) -> dict[str, Any]:
    task = validate_task(load_json(ROOT / entry["path"]))
    if sha256_object(task) != entry["sha256"]:
        raise RuntimeError(f"task hash does not match sealed manifest: {task['task_id']}")
    selected = task["validation"]["reference"] if artifact == "reference" else task["validation"]["known_bad"][0]
    verifier = verify(task, selected["code"], RUNTIME_CONFIG)
    return {
        "task_id": task["task_id"],
        "language": task["language"],
        "artifact": artifact,
        "artifact_label": selected["label"],
        "artifact_sha256": selected["sha256"],
        "expected_pass": artifact == "reference",
        "observed_pass": passed(verifier),
        "verifier": verifier,
    }


def summarize(manifest: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    failures = [
        {
            "task_id": row["task_id"],
            "artifact": row["artifact"],
            "expected_pass": row["expected_pass"],
            "observed_pass": row["observed_pass"],
            "timed_out": row["verifier"]["timed_out"],
        }
        for row in rows
        if row["expected_pass"] != row["observed_pass"] or row["verifier"]["timed_out"]
    ]
    evidence = {
        "schema_version": "ganesh-mini-directionality-evidence/v1",
        "evaluation_manifest": str(MANIFEST.relative_to(ROOT)),
        "evaluation_manifest_sha256": manifest["manifest_sha256"],
        "cross_tranche_overlap_report": str(CROSS_TRANCHE_OVERLAP.relative_to(ROOT)),
        "cross_tranche_overlap_report_sha256": EXPECTED_CROSS_TRANCHE_SHA256,
        "runtime_config": str(RUNTIME_CONFIG.relative_to(ROOT)),
        "execution_mode": "sequential",
        "task_count": manifest["task_count"],
        "execution_count": len(rows),
        "reference_passes": sum(row["artifact"] == "reference" and row["observed_pass"] for row in rows),
        "known_bad_rejections": sum(row["artifact"] == "known_bad" and not row["observed_pass"] for row in rows),
        "failures": failures,
        "status": "passed" if not failures else "failed",
        "executions": rows,
    }
    evidence["evidence_sha256"] = sha256_object(evidence)
    return evidence


def run(output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    manifest = load_json(MANIFEST)
    claimed = manifest["manifest_sha256"]
    if claimed != EXPECTED_MANIFEST_SHA256 or sha256_object({key: value for key, value in manifest.items() if key != "manifest_sha256"}) != claimed:
        raise RuntimeError("decision tranche1 manifest hash mismatch")
    cross = load_json(CROSS_TRANCHE_OVERLAP)
    cross_claimed = cross["report_sha256"]
    if cross_claimed != EXPECTED_CROSS_TRANCHE_SHA256 or sha256_object({key: value for key, value in cross.items() if key != "report_sha256"}) != cross_claimed:
        raise RuntimeError("decision cross-tranche overlap seal mismatch")
    expected_binding = {str(MANIFEST.relative_to(ROOT)): EXPECTED_MANIFEST_SHA256}
    observed_binding = {entry["path"]: entry["sha256"] for entry in cross["manifests"]}
    if cross["status"] != "passed" or observed_binding.get(str(MANIFEST.relative_to(ROOT))) != expected_binding[str(MANIFEST.relative_to(ROOT))]:
        raise RuntimeError("decision tranche1 is not bound by the passed cross-tranche seal")
    rows: list[dict[str, Any]] = []
    for entry in manifest["tasks"]:
        rows.append(execute(entry, "reference"))
        rows.append(execute(entry, "known_bad"))
    evidence = summarize(manifest, rows)
    write_json(output, evidence)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    evidence = run(args.output)
    print(json.dumps({key: evidence[key] for key in ("status", "execution_count", "reference_passes", "known_bad_rejections", "evidence_sha256")}, sort_keys=True))
    return int(evidence["status"] != "passed")


if __name__ == "__main__":
    raise SystemExit(main())
