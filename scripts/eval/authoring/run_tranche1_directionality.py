#!/usr/bin/env python3
"""Execute and preserve tranche-1 reference/bad directionality evidence."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from scripts.eval.authoring.build_tranche1 import MANIFEST, ROOT
from scripts.eval.contracts import load_json, sha256_object, write_json
from scripts.verify.sandbox import verify

DEFAULT_OUTPUT = ROOT / "manifests/evaluation/private/development-tranche1-directionality.json"
RUNTIME_CONFIG = ROOT / "configs/eval/runtimes.json"


def passed(result: dict[str, Any]) -> bool:
    return not result["timed_out"] and bool(result["exit_codes"]) and all(code == 0 for code in result["exit_codes"])


def execute(entry: dict[str, Any], artifact: str) -> dict[str, Any]:
    task = load_json(ROOT / entry["path"])
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
    rows.sort(key=lambda row: (row["task_id"], row["artifact"]))
    failures = [
        {"task_id": row["task_id"], "artifact": row["artifact"], "expected_pass": row["expected_pass"], "observed_pass": row["observed_pass"]}
        for row in rows if row["expected_pass"] != row["observed_pass"]
    ]
    evidence = {
        "schema_version": "ganesh-mini-directionality-evidence/v1",
        "evaluation_manifest": str(MANIFEST.relative_to(ROOT)),
        "evaluation_manifest_sha256": manifest["manifest_sha256"],
        "runtime_config": str(RUNTIME_CONFIG.relative_to(ROOT)),
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


def run(output: Path = DEFAULT_OUTPUT, workers: int = 4, retry_failures: bool = False) -> dict[str, Any]:
    manifest = load_json(MANIFEST)
    if retry_failures:
        prior = load_json(output)
        if prior["evaluation_manifest_sha256"] != manifest["manifest_sha256"]:
            raise RuntimeError("cannot retry evidence for a different manifest")
        rows = prior["executions"]
        replacements = {}
        for row in rows:
            if row["verifier"]["timed_out"] or row["expected_pass"] != row["observed_pass"]:
                replacements[(row["task_id"], row["artifact"])] = execute(
                    next(entry for entry in manifest["tasks"] if entry["task_id"] == row["task_id"]), row["artifact"]
                )
        rows = [replacements.get((row["task_id"], row["artifact"]), row) for row in rows]
        evidence = summarize(manifest, rows)
        write_json(output, evidence)
        return evidence
    rows = []
    futures = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for entry in manifest["tasks"]:
            futures.extend((pool.submit(execute, entry, "reference"), pool.submit(execute, entry, "known_bad")))
        for future in as_completed(futures):
            rows.append(future.result())
    evidence = summarize(manifest, rows)
    write_json(output, evidence)
    return evidence


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=DEFAULT_OUTPUT)
    parser.add_argument("--workers",type=int,default=4)
    parser.add_argument("--retry-failures",action="store_true")
    args=parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error("--workers must be in [1,8]")
    evidence=run(args.output,args.workers,args.retry_failures)
    print(json.dumps({k:evidence[k] for k in ("status","execution_count","reference_passes","known_bad_rejections","evidence_sha256")},sort_keys=True))
    return int(evidence["status"] != "passed")


if __name__ == "__main__":
    raise SystemExit(main())
