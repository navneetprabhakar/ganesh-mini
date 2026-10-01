#!/usr/bin/env python3
"""Build the deterministic 546-first-pass plus 165-reserve scale queue."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256


PLAN_SHA256 = "d0e2b112eaa17eb96d2a0284964c9d107bc94b3fcd8edc6369cf7792026100ee"
ENTRY_SEAL = "fbf45982984c2c669e03abf1c773d768019651184547104271de12c42f79318c"
LINEAGE_SHA256 = "f9daacdd55183ac220f926d8135124e4ffba97ea42acd8bb114326b64e19f73c"
SOURCE_QUEUE_SHA256 = "b76fdf8d14b1bb5513846b426f7927a63e80c46755fc96a1fbcec65bac23252c"
PRIOR_CORPUS_SHA256 = "4254b6f82323421edbbece17fe1a0eb43a622c697059921afbf34aca600b949d"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def source_key(row: dict[str, Any]) -> str:
    source = row.get("source") or row.get("lineage") or {}
    values = (source.get("dataset"), source.get("revision"), source.get("record_id"))
    if not all(isinstance(value, str) and value for value in values):
        raise ValueError(f"{row.get('id')}: incomplete source identity")
    return "\0".join(values)


def candidate_from(value: dict[str, Any]) -> dict[str, Any]:
    candidate = value.get("candidate")
    if not isinstance(candidate, dict):
        raise ValueError("historical teacher output is missing its candidate")
    return candidate


def selection_key(cell_id: str, row: dict[str, Any]) -> str:
    material = f"{PLAN_SHA256}\0{cell_id}\0{row['id']}\0{source_key(row)}"
    return hashlib.sha256(material.encode()).hexdigest()


def build(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    fixed = {
        args.plan: PLAN_SHA256,
        args.lineage: LINEAGE_SHA256,
        args.source_queue: SOURCE_QUEUE_SHA256,
        args.prior_corpus: PRIOR_CORPUS_SHA256,
    }
    for path, digest in fixed.items():
        if file_sha256(path) != digest:
            raise ValueError(f"{path}: frozen input hash differs")
    entry = json.loads(args.entry_manifest.read_text(encoding="utf-8"))
    entry_body = dict(entry); entry_claimed = entry_body.pop("manifest_sha256", None)
    if (
        entry_claimed != ENTRY_SEAL or entry_claimed != canonical_sha256(entry_body)
        or entry.get("status") != "passed" or entry.get("records") != 174
        or sum(entry.get("cell_top_up", {}).values()) != 546
    ):
        raise ValueError("training-entry manifest is invalid")

    lineage = read_jsonl(args.lineage)
    if len(lineage) != 174 or len({row["source_identity"] for row in lineage}) != 174:
        raise ValueError("qualified lineage is incomplete or source-colliding")
    cells: dict[str, dict[str, Any]] = {}
    for row in lineage:
        cells.setdefault(row["cell_id"], row)
    if len(cells) != 120 or set(cells) != set(entry["cell_top_up"]):
        raise ValueError("qualified lineage cells differ from top-up accounting")

    v2 = read_jsonl(args.v2_envelopes)
    v3 = [row for path in args.v3_candidates for row in read_jsonl(path)]
    v4 = [row for path in args.v4_candidates for row in read_jsonl(path)]
    v5 = read_jsonl(args.v5_candidates)
    assignments = read_jsonl(args.v5_assignments)
    fresh_v5_ids = {row["id"] for row in assignments if row.get("mode") == "fresh-v5-teacher-primary"}
    if (len(v2), len(v3), len(v4), len(fresh_v5_ids)) != (247, 60, 180, 2):
        raise ValueError("historical teacher draft accounting differs from 247+60+180+2")
    if len(v5) != 60 or not fresh_v5_ids <= {candidate_from(row)["id"] for row in v5}:
        raise ValueError("V5 fresh teacher replacements are not present")

    historical_candidates = [candidate_from(row) for row in [*v2, *v3, *v4, *v5]]
    historical_sources = {source_key(row) for row in historical_candidates}
    prior_rows = read_jsonl(args.prior_corpus)
    prior_sources = {source_key(row) for row in prior_rows}
    qualified_sources = {row["source_identity"].replace("|", "\0") for row in lineage}
    excluded = historical_sources | prior_sources | qualified_sources

    source_rows = read_jsonl(args.source_queue)
    if len({row["id"] for row in source_rows}) != len(source_rows):
        raise ValueError("source queue IDs are not unique")
    available = [row for row in source_rows if source_key(row) not in excluded]
    used: set[str] = set()
    output: list[dict[str, Any]] = []

    reserve_order = sorted(cells, key=lambda cell: hashlib.sha256(f"{PLAN_SHA256}\0reserve\0{cell}".encode()).hexdigest())
    reserve_counts = {cell: 1 + (index < 45) for index, cell in enumerate(reserve_order)}
    for cell_id in sorted(cells):
        metadata = cells[cell_id]
        first_count = entry["cell_top_up"][cell_id]
        reserve_count = reserve_counts[cell_id]
        candidates = [
            row for row in available
            if row.get("lane") == metadata["lane"]
            and row.get("task_type") == metadata["task_type"]
            and source_key(row) not in used
        ]
        candidates.sort(key=lambda row: selection_key(cell_id, row))
        if len(candidates) < first_count + reserve_count:
            raise ValueError(f"{cell_id}: insufficient source-unique scale inputs")
        for position, source in enumerate(candidates[:first_count + reserve_count], start=1):
            cohort = "first_pass" if position <= first_count else "reserve"
            key = source_key(source); used.add(key)
            row = {
                "schema_version": "ganesh-mini-capability-scale-request/v1",
                "id": f"cap-scale-{metadata['primary_capability']}-{metadata['lane']}-{metadata['task_type']}-{cohort}-{position:02d}",
                "cell_id": cell_id,
                "cohort": cohort,
                "primary_capability": metadata["primary_capability"],
                "primary_capability_definition": CAPABILITIES[metadata["primary_capability"]],
                "assigned_cross_cutting_dimension": metadata["assigned_cross_cutting_dimension"],
                "lane": metadata["lane"],
                "task_type": metadata["task_type"],
                "source_queue_id": source["id"],
                "source": source["source"],
                "stimulus": source["stimulus"],
                "evaluation_artifacts_read": 0,
            }
            row["request_sha256"] = canonical_sha256(row)
            output.append(row)

    cohort_counts = Counter(row["cohort"] for row in output)
    if cohort_counts != {"first_pass": 546, "reserve": 165} or len(used) != 711:
        raise ValueError("scale queue does not reconcile to 546+165 unique requests")
    payload = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in output).encode()
    input_paths = [args.v2_envelopes, *args.v3_candidates, *args.v4_candidates, args.v5_candidates, args.v5_assignments]
    manifest = {
        "schema_version": "ganesh-mini-capability-scale-queue-manifest/v1",
        "status": "ready-for-first-pass-construction",
        "plan_sha256": PLAN_SHA256,
        "training_entry_manifest_sha256": ENTRY_SEAL,
        "historical_draft_accounting": {"v2": 247, "v3": 60, "v4": 180, "v5": 2, "total": 489, "remaining_under_1200": 711},
        "inputs": {
            "source_queue": {"path": str(args.source_queue), "sha256": SOURCE_QUEUE_SHA256, "records": len(source_rows)},
            "prior_corpus": {"path": str(args.prior_corpus), "sha256": PRIOR_CORPUS_SHA256, "records": len(prior_rows)},
            "qualified_lineage": {"path": str(args.lineage), "sha256": LINEAGE_SHA256, "records": len(lineage)},
            "historical_candidate_files": [{"path": str(path), "sha256": file_sha256(path), "records": len(read_jsonl(path))} for path in input_paths],
        },
        "source_exclusion": {"prior_sources": len(prior_sources), "historical_teacher_sources": len(historical_sources), "qualified_sources": len(qualified_sources), "evaluation_surfaces_read": 0},
        "records": 711,
        "first_pass_records": 546,
        "reserve_records": 165,
        "unique_source_identities": 711,
        "cells": 120,
        "queue_sha256": hashlib.sha256(payload).hexdigest(),
        "first_pass_by_task_type": dict(Counter(row["task_type"] for row in output if row["cohort"] == "first_pass")),
        "reserve_allocation": {"one_slot_cells": 75, "two_slot_cells": 45, "maximum_per_cell": 2},
        "gcloud_actions": 0,
        "training_executed": False,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    return output, manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("plan", "entry-manifest", "lineage", "source-queue", "prior-corpus", "v2-envelopes", "v5-candidates", "v5-assignments", "output", "manifest"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--v3-candidates", type=Path, action="append", required=True)
    parser.add_argument("--v4-candidates", type=Path, action="append", required=True)
    args = parser.parse_args(argv)
    rows, manifest = build(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(rows), "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
