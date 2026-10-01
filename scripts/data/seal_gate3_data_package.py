#!/usr/bin/env python3
"""Seal a validated Gate 3 data package without claiming a pilot result."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.validate_gate3_final_package import validate


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal(manifest_path: Path) -> dict:
    result = validate(manifest_path)
    if result.get("status") != "validated-not-sealed" or result.get("records") != 900:
        raise ValueError("package validator did not pass all 900 records")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    training_binding = manifest.get("canonical_training_jsonl")
    if not isinstance(training_binding, dict):
        raise ValueError("canonical training file binding missing")
    train_path = manifest_path.parent / training_binding["path"]
    if file_sha(train_path) != training_binding.get("sha256"):
        raise ValueError("canonical training file hash mismatch")
    train_rows = [json.loads(line) for line in train_path.read_text(encoding="utf-8").splitlines()]
    if len(train_rows) != 900 or canonical_sha256(train_rows) != result["package_rows_sha256"]:
        raise ValueError("canonical training file differs from validated rows")
    record = {
        "schema_version": "ganesh-mini-gate3-data-package-admission/v1",
        "status": "data-package-passed-pilot-pending",
        "records": 900,
        "capability_records": 720,
        "replay_records": 180,
        "package_manifest_sha256": manifest["manifest_sha256"],
        "package_manifest_file_sha256": file_sha(manifest_path),
        "canonical_training_jsonl_sha256": file_sha(train_path),
        "package_rows_sha256": result["package_rows_sha256"],
        "maximum_scaffold_cluster": result["maximum_scaffold_cluster"],
        "manual_review_disclosure": "two blind independent AI reviews per primary capability; no human sign-off claimed",
        "training_executed": False,
        "pilot_passed": False,
        "release_eligible": False,
        "evaluation_artifacts_read_by_construction": 0,
        "gcloud_actions": 0,
    }
    record["report_sha256"] = canonical_sha256(record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("data-package seal already exists")
    record = seal(args.manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": record["status"], "records": 900, "report_sha256": record["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
