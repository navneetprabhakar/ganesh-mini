#!/usr/bin/env python3
"""Seal the upload-only boundary for the lane-stratified checkpoint sweep."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


BUCKET = "ganesh-gate0-model-transfer-1061994342941"
OBJECTS = (
    ("artifacts/eval/workspaces/lane-stratified-v3-checkpoint-sweep.tar.gz", "workspace.tar.gz"),
    ("artifacts/eval/workspaces/lane-stratified-v3-checkpoint-sweep.manifest.json", "workspace.manifest.json"),
    ("artifacts/eval/workspaces/lane-stratified-v3-checkpoint-sweep-startup.sh", "startup.sh"),
    ("artifacts/eval/workspaces/lane-stratified-v3-checkpoint-sweep-startup.manifest.json", "startup.manifest.json"),
    ("artifacts/eval/workspaces/lane-stratified-v3-checkpoint-sweep-recovery.tar.gz", "recovery.tar.gz"),
    ("artifacts/eval/workspaces/lane-stratified-v3-checkpoint-sweep-recovery.manifest.json", "recovery.manifest.json"),
)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
    ).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(root: Path, source_commit: str) -> dict[str, Any]:
    if len(source_commit) != 40 or any(character not in "0123456789abcdef" for character in source_commit):
        raise ValueError("source commit must be a full lowercase Git SHA")
    prefix = f"ganesh-mini-1.0/evaluation/lane-stratified-v3-checkpoint-sweep/input/{source_commit[:8]}"
    objects = []
    for relative, name in OBJECTS:
        path = root / relative
        if not path.is_file():
            raise ValueError(f"checkpoint-sweep upload input is missing: {relative}")
        objects.append({
            "source": relative,
            "destination": f"gs://{BUCKET}/{prefix}/{name}",
            "size_bytes": path.stat().st_size,
            "sha256": file_sha256(path),
        })
    plan: dict[str, Any] = {
        "schema_version": "ganesh-mini-lane-checkpoint-sweep-gcloud-upload-plan/v1",
        "status": "pending-explicit-gcloud-upload-approval",
        "purpose": "obtain immutable GCS generations for the diagnostic-only v3 checkpoint sweep",
        "project": "executespecv1",
        "bucket": BUCKET,
        "source_commit": source_commit,
        "object_count": len(objects),
        "maximum_new_bytes": sum(row["size_bytes"] for row in objects),
        "objects": objects,
        "allowed_operations": [
            "upload the six named immutable objects with create-only preconditions",
            "capture assigned object generations",
            "download each exact generation and compare bytes",
            "write a sealed local upload receipt",
        ],
        "forbidden_operations": [
            "inspect, create, start, stop, mutate, or delete compute and network resources",
            "overwrite or delete any existing GCS object generation",
            "train or open full-development or decision evaluation surfaces",
            "select, promote, merge, quantize, publish, or claim checkpoint improvement",
        ],
    }
    plan["upload_plan_sha256"] = canonical_sha256(plan)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = build(args.root.resolve(), args.source_commit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "maximum_new_bytes": plan["maximum_new_bytes"],
        "status": plan["status"],
        "upload_plan_sha256": plan["upload_plan_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
