#!/usr/bin/env python3
"""Execute decision tranche 6 sequentially in bounded Docker sandboxes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.eval.authoring.build_decision_tranche6 import MANIFEST, OVERLAP, ROOT
from scripts.eval.contracts import load_json, sha256_object, validate_task, write_json
from scripts.verify.sandbox import SANDBOX_CONTRACT, verify

DEFAULT_OUTPUT = ROOT / "manifests/evaluation/private/decision-tranche6-directionality.json"
RUNTIME_CONFIG = ROOT / "configs/eval/runtimes.json"
EXPECTED_MANIFEST_SHA256 = "f97eb03d1206cb7135a520f2fb069a44375b9332a4e36ddc9f78cbb0ca6d7c89"
EXPECTED_OVERLAP_SHA256 = "80f4d7f340fc4994f97e8c332e9eea9a339c7eb4837f9d00595775b0ef1ba0ff"


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


def run(output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    manifest = load_json(MANIFEST); claimed = manifest["manifest_sha256"]
    if claimed != EXPECTED_MANIFEST_SHA256 or sha256_object({k: v for k, v in manifest.items() if k != "manifest_sha256"}) != claimed:
        raise RuntimeError("decision tranche6 manifest hash mismatch")
    overlap = load_json(OVERLAP); overlap_claimed = overlap["report_sha256"]
    if overlap_claimed != EXPECTED_OVERLAP_SHA256 or sha256_object({k: v for k, v in overlap.items() if k != "report_sha256"}) != overlap_claimed:
        raise RuntimeError("decision tranche6 overlap seal mismatch")
    if overlap["status"] != "passed" or overlap["evaluation_manifest"] != str(MANIFEST.relative_to(ROOT)) or overlap["evaluation_manifest_sha256"] != claimed:
        raise RuntimeError("decision tranche6 is not bound by the passed overlap seal")
    if SANDBOX_CONTRACT.get("backend") != "docker" or SANDBOX_CONTRACT.get("network") != "none" or SANDBOX_CONTRACT.get("pull") != "never":
        raise RuntimeError("directionality requires the pinned network-none Docker sandbox")
    rows = []
    for entry in manifest["tasks"]:
        rows.append(execute(entry, "reference")); rows.append(execute(entry, "known_bad"))
    failures = [{"task_id": row["task_id"], "artifact": row["artifact"], "expected_pass": row["expected_pass"], "observed_pass": row["observed_pass"], "timed_out": row["verifier"]["timed_out"]} for row in rows if row["expected_pass"] != row["observed_pass"] or row["verifier"]["timed_out"]]
    evidence = {
        "schema_version": "ganesh-mini-directionality-evidence/v1", "evaluation_manifest": str(MANIFEST.relative_to(ROOT)),
        "evaluation_manifest_sha256": claimed, "overlap_report": str(OVERLAP.relative_to(ROOT)),
        "overlap_report_sha256": overlap_claimed, "runtime_config": str(RUNTIME_CONFIG.relative_to(ROOT)),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT), "execution_mode": "sequential",
        "task_count": manifest["task_count"], "execution_count": len(rows),
        "reference_passes": sum(row["artifact"] == "reference" and row["observed_pass"] for row in rows),
        "known_bad_rejections": sum(row["artifact"] == "known_bad" and not row["observed_pass"] for row in rows),
        "failures": failures, "status": "passed" if not failures else "failed", "executions": rows,
    }
    evidence["evidence_sha256"] = sha256_object(evidence); write_json(output, evidence); return evidence


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT); args = parser.parse_args()
    evidence = run(args.output); print(json.dumps({k: evidence[k] for k in ("status", "execution_count", "reference_passes", "known_bad_rejections", "evidence_sha256")}, sort_keys=True)); return int(evidence["status"] != "passed")


if __name__ == "__main__":
    raise SystemExit(main())
