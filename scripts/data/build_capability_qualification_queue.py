#!/usr/bin/env python3
"""Build the deterministic training-only 120-cell qualification queue."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256, load_sealed


SEED = 3502


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def source_key(row: dict[str, Any]) -> str:
    source = row.get("source") or row.get("lineage") or {}
    values = (source.get("dataset"), source.get("revision"), source.get("record_id"))
    if not all(isinstance(value, str) and value for value in values):
        raise ValueError(f"{row.get('id')}: incomplete source identity")
    return "\0".join(values)


def selection_key(cell_id: str, row: dict[str, Any]) -> str:
    return hashlib.sha256(f"{SEED}\0{cell_id}\0{row['id']}\0{source_key(row)}".encode()).hexdigest()


def build(plan_path: Path, source_queue_path: Path, prior_corpus_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    plan = load_sealed(plan_path, "plan_sha256")
    if (
        plan.get("schema_version") != "ganesh-mini-capability-stratified-corpus-plan/v1"
        or plan.get("status") != "local-contract-sealed-qualification-implementation-next"
        or plan.get("matrix", {}).get("cells") != 120
        or plan.get("qualification", {}).get("drafts") != 240
    ):
        raise ValueError("capability plan does not authorize this qualification queue")
    source_rows = read_jsonl(source_queue_path)
    prior_rows = read_jsonl(prior_corpus_path)
    prior_sources = {source_key(row) for row in prior_rows}
    eligible = [row for row in source_rows if source_key(row) not in prior_sources]
    if len({row.get("id") for row in eligible}) != len(eligible):
        raise ValueError("eligible source queue IDs are not unique")

    used_sources: set[str] = set()
    output: list[dict[str, Any]] = []
    for cell in plan["matrix"]["cell_contracts"]:
        candidates = [
            row for row in eligible
            if row.get("lane") == cell["lane"]
            and row.get("task_type") == cell["task_type"]
            and source_key(row) not in used_sources
        ]
        candidates.sort(key=lambda row: selection_key(cell["cell_id"], row))
        count = cell["qualification_drafts"]
        if len(candidates) < count:
            raise ValueError(f"{cell['cell_id']}: insufficient unused training sources")
        for ordinal, source_row in enumerate(candidates[:count], start=1):
            key = source_key(source_row)
            used_sources.add(key)
            output.append({
                "schema_version": "ganesh-mini-capability-qualification-draft/v1",
                "id": f"cap-v2-{cell['primary_capability']}-{cell['lane']}-{cell['task_type']}-{ordinal:02d}",
                "cell_id": cell["cell_id"],
                "primary_capability": cell["primary_capability"],
                "primary_capability_definition": plan["ontology"]["primary_capabilities"][cell["primary_capability"]],
                "assigned_cross_cutting_dimension": cell["assigned_cross_cutting_dimension"],
                "lane": cell["lane"],
                "task_type": cell["task_type"],
                "source_queue_id": source_row["id"],
                "source": source_row["source"],
                "stimulus": source_row["stimulus"],
            })

    if len(output) != 240 or len(used_sources) != 240:
        raise ValueError("qualification queue is not exactly 240 source-unique drafts")
    cell_counts = Counter(row["cell_id"] for row in output)
    if set(cell_counts.values()) != {2} or len(cell_counts) != 120:
        raise ValueError("qualification queue does not contain two drafts per cell")
    payload = b"".join(canonical_json(row) + b"\n" for row in output)
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-qualification-queue-manifest/v1",
        "status": "ready-for-isolated-teacher-qualification",
        "plan_sha256": plan["plan_sha256"],
        "seed": SEED,
        "inputs": {
            "source_queue_path": str(source_queue_path),
            "source_queue_sha256": hashlib.sha256(source_queue_path.read_bytes()).hexdigest(),
            "prior_corpus_path": str(prior_corpus_path),
            "prior_corpus_sha256": hashlib.sha256(prior_corpus_path.read_bytes()).hexdigest(),
        },
        "selection": {
            "method": "per-cell seeded SHA-256 order over unused same-lane/task-type training sources",
            "prior_corpus_sources_excluded": len(prior_sources),
            "evaluation_surfaces_read": 0,
        },
        "records": len(output),
        "unique_source_identities": len(used_sources),
        "cells": len(cell_counts),
        "records_per_cell": dict(sorted(cell_counts.items())),
        "queue_sha256": hashlib.sha256(payload).hexdigest(),
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    return output, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--source-queue", type=Path, required=True)
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    rows, manifest = build(args.plan, args.source_queue, args.prior_corpus)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(rows), "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
