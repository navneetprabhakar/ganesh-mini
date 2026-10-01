#!/usr/bin/env python3
"""Prebind one fresh Gate 3 source after the sealed duplicate-reserve stop."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256
from scripts.data.build_capability_scale_queue import read_jsonl, source_key


PLAN_SHA256 = "81ba26cbe4b6557bc693ac63e261e6c6d787f08c669b6b42f1415a4649f8d3ad"
ORIGINAL_MANIFEST_SHA256 = "f3e3e312625ec85f067c0089f40b16ed4591fe320745445e34f23825a3dc6d55"
ORIGINAL_QUEUE_SHA256 = "a8d9eb96cdbdb8ccd4ec126b512c71ae832856beff9dd46a799c99571eefba51"
CELL = "associative_aggregation/python/repair"
DUPLICATE_ID = "cap-scale-associative_aggregation-python-repair-reserve-06"
NEW_ID = "cap-scale-associative_aggregation-python-repair-prospective-01"
COUNTED_DRAFTS = 1058
GLOBAL_CAP = 1200


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hash(row: dict[str, Any]) -> str:
    value = row.get("source", {}).get("source_record_sha256")
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(f"{row.get('id')}: missing source-record hash")
    return value


def sealed_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    body = dict(manifest)
    claimed = body.pop("manifest_sha256", None)
    if claimed != ORIGINAL_MANIFEST_SHA256 or claimed != canonical_sha256(body):
        raise ValueError("original scale queue manifest differs from its seal")
    return manifest


def checked_rows(binding: dict[str, Any]) -> list[dict[str, Any]]:
    path = Path(binding["path"])
    if file_sha256(path) != binding["sha256"]:
        raise ValueError(f"{path}: source input hash drift")
    rows = read_jsonl(path)
    if len(rows) != binding["records"]:
        raise ValueError(f"{path}: source input count drift")
    return rows


def pick_source(
    pool: list[dict[str, Any]], original: list[dict[str, Any]],
    prior: list[dict[str, Any]], historical: list[dict[str, Any]],
    lineage: list[dict[str, Any]],
) -> tuple[dict[str, Any], int]:
    if len(original) != 711 or len({row["id"] for row in original}) != 711:
        raise ValueError("original scale queue has changed")
    if len(historical) != 547 or len(prior) != 3225 or len(lineage) != 174:
        raise ValueError("historical source exclusion inventory changed")
    if not any(row["id"] == DUPLICATE_ID and row["cell_id"] == CELL for row in original):
        raise ValueError("duplicate source is absent from the frozen queue")
    historical_sources = [row["candidate"] for row in historical if isinstance(row.get("candidate"), dict)]
    if len(historical_sources) != 547:
        raise ValueError("historical candidate source evidence is incomplete")
    excluded_keys = {source_key(row) for row in [*original, *prior, *historical_sources]}
    excluded_keys |= {row["source_identity"].replace("|", "\0") for row in lineage}
    excluded_hashes = {source_hash(row) for row in original}
    pool_keys = Counter(source_key(row) for row in pool)
    pool_hashes = Counter(source_hash(row) for row in pool)
    eligible = [
        row for row in pool
        if row.get("lane") == "python" and row.get("task_type") == "repair"
        and row.get("source", {}).get("license") == "MIT"
        and source_key(row) not in excluded_keys
        and source_hash(row) not in excluded_hashes
        and pool_keys[source_key(row)] == 1 and pool_hashes[source_hash(row)] == 1
    ]
    if not eligible:
        raise ValueError("no uniquely eligible Python repair source")
    def rank(row: dict[str, Any]) -> str:
        material = f"{PLAN_SHA256}\0{CELL}\0{row['id']}\0{source_key(row)}"
        return hashlib.sha256(material.encode()).hexdigest()
    eligible.sort(key=lambda row: (rank(row), row["id"]))
    return eligible[0], len(eligible)


def prepare(
    plan_path: Path, queue_path: Path, manifest_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if file_sha256(plan_path) != PLAN_SHA256:
        raise ValueError("prospective replacement plan hash drift")
    manifest = sealed_manifest(manifest_path)
    if file_sha256(queue_path) != ORIGINAL_QUEUE_SHA256 or manifest.get("queue_sha256") != ORIGINAL_QUEUE_SHA256:
        raise ValueError("original scale queue bytes drift")
    original = read_jsonl(queue_path)
    inputs = manifest["inputs"]
    pool = checked_rows(inputs["source_queue"])
    prior = checked_rows(inputs["prior_corpus"])
    lineage = checked_rows(inputs["qualified_lineage"])
    historical: list[dict[str, Any]] = []
    for binding in inputs["historical_candidate_files"]:
        rows = checked_rows(binding)
        if "candidate" in rows[0]:
            historical.extend(rows)
    source, eligible_count = pick_source(pool, original, prior, historical, lineage)
    request: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-request/v1",
        "id": NEW_ID,
        "cell_id": CELL,
        "cohort": "prospective_replacement",
        "primary_capability": "associative_aggregation",
        "primary_capability_definition": CAPABILITIES["associative_aggregation"],
        "assigned_cross_cutting_dimension": next(row["assigned_cross_cutting_dimension"] for row in original if row["id"] == DUPLICATE_ID),
        "lane": "python", "task_type": "repair",
        "source_queue_id": source["id"], "source": source["source"],
        "stimulus": source["stimulus"], "evaluation_artifacts_read": 0,
    }
    request["request_sha256"] = canonical_sha256(request)
    if COUNTED_DRAFTS + 1 > GLOBAL_CAP:
        raise ValueError("global teacher-draft cap would be exceeded")
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-prospective-replacement-manifest/v1",
        "status": "source-prebound-not-generated",
        "plan_sha256": PLAN_SHA256,
        "original_queue_manifest_sha256": ORIGINAL_MANIFEST_SHA256,
        "original_queue_sha256": ORIGINAL_QUEUE_SHA256,
        "input_sha256s": {key: binding["sha256"] for key, binding in inputs.items() if isinstance(binding, dict) and "sha256" in binding},
        "historical_file_sha256s": [binding["sha256"] for binding in inputs["historical_candidate_files"]],
        "eligible_source_count": eligible_count,
        "selected_source_queue_id": source["id"],
        "selected_source_identity": source_key(source).replace("\0", "|"),
        "selected_source_record_sha256": source_hash(source),
        "request_sha256": request["request_sha256"],
        "teacher_drafts_before": COUNTED_DRAFTS,
        "maximum_teacher_drafts_after": COUNTED_DRAFTS + 1,
        "global_teacher_draft_cap": GLOBAL_CAP,
        "evaluation_artifacts_read": 0, "gcloud_actions": 0,
    }
    report["manifest_sha256"] = canonical_sha256(report)
    return [request], report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--output-queue", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    args = parser.parse_args()
    if args.output_queue.exists() or args.output_manifest.exists():
        raise ValueError("prospective replacement outputs already exist")
    rows, manifest = prepare(args.plan, args.queue, args.queue_manifest)
    args.output_queue.parent.mkdir(parents=True, exist_ok=True)
    args.output_queue.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")
    args.output_manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "source_queue_id": manifest["selected_source_queue_id"], "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
