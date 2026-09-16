#!/usr/bin/env python3
"""Validate and seal combined evidence from repair-source ontology waves."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import CAPABILITIES, LANES, canonical_sha256  # noqa: E402
from scripts.data.build_repair_delta_queue import (  # noqa: E402
    AFFINITY_FIELDS, PLAN_SHA256, canonical_json, ontology_affinity_prompt, read_jsonl, source_key,
)
from scripts.data.run_repair_source_ontology import (  # noqa: E402
    CAMPAIGN_SCHEMA, SCHEMA_VERSION, validate_payload,
)


AGGREGATE_SCHEMA = "ganesh-mini-repair-source-ontology-aggregate/v1"
MINIMUM_SOURCES_PER_CELL = 2


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _load_summary(path: Path, evidence_path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop("summary_sha256", None)
    evidence_bytes = evidence_path.read_bytes()
    if (
        claimed != canonical_sha256(body)
        or value.get("schema_version") != CAMPAIGN_SCHEMA
        or value.get("plan_sha256") != PLAN_SHA256
        or value.get("output_sha256") != sha256_bytes(evidence_bytes)
        or value.get("evaluation_artifacts_read") != 0
        or value.get("status") not in {"complete", "failed"}
        or type(value.get("selected")) is not int
        or type(value.get("completed")) is not int
        or value["selected"] < value["completed"]
        or not isinstance(value.get("failures"), list)
        or not isinstance(value.get("coverage"), dict)
        or not isinstance(value.get("separation_attestation_sha256"), str)
    ):
        raise ValueError(f"ontology campaign summary is invalid: {path}")
    return value


def _validate_evidence_row(
    row: dict[str, Any], sources: dict[str, dict[str, Any]], separation_sha256: str,
) -> tuple[dict[str, Any], tuple[str, str, str]]:
    body = dict(row)
    claimed = body.pop("evidence_sha256", None)
    source = sources.get(row.get("source_queue_id"))
    batch_ids = row.get("batch_source_queue_ids")
    batch_sources = [sources.get(identifier) for identifier in batch_ids] if isinstance(batch_ids, list) else []
    raw_prompt = row.get("raw_prompt")
    raw_output = row.get("raw_output")
    run = row.get("run_evidence")
    runtime = row.get("runtime_parameters")
    run_body = dict(run) if isinstance(run, dict) else {}
    run_claimed = run_body.pop("run_evidence_sha256", None)
    if (
        claimed != canonical_sha256(body)
        or row.get("schema_version") != SCHEMA_VERSION
        or row.get("plan_sha256") != PLAN_SHA256
        or row.get("separation_attestation_sha256") != separation_sha256
        or row.get("evaluation_artifacts_read") != 0
        or source is None or source.get("lane") != row.get("lane")
        or source.get("task_type") != "repair"
        or row.get("source_record_sha256") != source.get("source", {}).get("source_record_sha256")
        or row.get("source_identity") != {
            key: source.get("source", {}).get(key) for key in ("dataset", "revision", "record_id")
        }
        or row.get("stimulus_sha256") != hashlib.sha256(source.get("stimulus", "").encode()).hexdigest()
        or not isinstance(batch_ids, list) or not batch_ids or len(batch_ids) != len(set(batch_ids))
        or row.get("source_queue_id") not in batch_ids
        or any(item is None for item in batch_sources)
        or any(item.get("lane") not in LANES or item.get("task_type") != "repair" for item in batch_sources)
        or len({source_key(item) for item in batch_sources}) != len(batch_sources)
        or row.get("batch_source_records_sha256") != canonical_sha256(batch_sources)
        or not isinstance(raw_prompt, str) or raw_prompt != ontology_affinity_prompt(batch_sources)
        or row.get("prompt_sha256") != hashlib.sha256(raw_prompt.encode()).hexdigest()
        or not isinstance(raw_output, str)
        or row.get("output_sha256") != hashlib.sha256(raw_output.encode()).hexdigest()
        or not isinstance(runtime, dict) or not isinstance(run, dict)
        or run.get("final_output") != raw_output
        or run_claimed != canonical_sha256(run_body)
        or runtime.get("run_evidence_sha256") != run_claimed
        or type(row.get("selection_rank")) is not int or row["selection_rank"] < 0
    ):
        raise ValueError(f"source-ontology evidence is incomplete or unsealed: {row.get('source_queue_id')}")
    try:
        items = validate_payload(json.loads(raw_output), batch_ids)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"source-ontology raw output is invalid: {row.get('source_queue_id')}") from exc
    item = items[batch_ids.index(row["source_queue_id"])]
    expected_verdicts = sorted(item["verdicts"], key=lambda value: value["primary_capability"])
    if row.get("verdicts") != expected_verdicts:
        raise ValueError(f"source-ontology verdicts differ from raw output: {row['source_queue_id']}")
    return source, source_key(source)


def aggregate(
    source_queue_path: Path,
    waves: list[tuple[Path, Path]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not waves:
        raise ValueError("at least one ontology wave is required")
    source_rows = read_jsonl(source_queue_path)
    sources: dict[str, dict[str, Any]] = {}
    for source in source_rows:
        identifier = source.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in sources:
            raise ValueError("source queue contains a malformed or duplicate ID")
        sources[identifier] = source

    combined: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_lineage: set[tuple[str, str, str]] = set()
    separation_sha256: str | None = None
    wave_manifests: list[dict[str, Any]] = []
    for index, (evidence_path, summary_path) in enumerate(waves):
        summary = _load_summary(summary_path, evidence_path)
        current_separation = summary["separation_attestation_sha256"]
        if separation_sha256 is None:
            separation_sha256 = current_separation
        elif current_separation != separation_sha256:
            raise ValueError("ontology waves use different separation attestations")
        rows = read_jsonl(evidence_path)
        if len(rows) != summary["completed"]:
            raise ValueError(f"ontology campaign completed count differs from evidence: {summary_path}")
        wave_ids: set[str] = set()
        wave_coverage = {lane: {capability: 0 for capability in CAPABILITIES} for lane in LANES}
        batch_members: dict[tuple[str, ...], set[str]] = defaultdict(set)
        for row in rows:
            source, lineage = _validate_evidence_row(row, sources, current_separation)
            identifier = row["source_queue_id"]
            if identifier in wave_ids or identifier in seen_ids:
                raise ValueError(f"duplicate source queue ID across ontology waves: {identifier}")
            if lineage in seen_lineage:
                raise ValueError(f"duplicate source lineage across ontology waves: {lineage}")
            wave_ids.add(identifier); seen_ids.add(identifier); seen_lineage.add(lineage)
            batch_members[tuple(row["batch_source_queue_ids"])].add(identifier)
            for verdict in row["verdicts"]:
                if verdict["decision"] == "accept":
                    wave_coverage[source["lane"]][verdict["primary_capability"]] += 1
            combined.append(row)
        for batch_ids, observed_ids in batch_members.items():
            if observed_ids != set(batch_ids):
                raise ValueError(f"ontology wave contains a partial successful batch: {batch_ids}")
        if summary["coverage"] != wave_coverage:
            raise ValueError(f"ontology campaign coverage differs from evidence: {summary_path}")
        wave_manifests.append({
            "wave_index": index,
            "evidence_sha256": sha256_bytes(evidence_path.read_bytes()),
            "summary_file_sha256": sha256_bytes(summary_path.read_bytes()),
            "campaign_manifest": summary,
        })

    lane_index = {lane: index for index, lane in enumerate(LANES)}
    combined.sort(key=lambda row: (lane_index[row["lane"]], row["selection_rank"], row["source_queue_id"]))
    cell_sources: dict[str, list[str]] = {}
    nested = {lane: {capability: [] for capability in CAPABILITIES} for lane in LANES}
    for row in combined:
        for verdict in row["verdicts"]:
            if verdict["decision"] == "accept":
                nested[row["lane"]][verdict["primary_capability"]].append(row["source_queue_id"])
    cells: dict[str, dict[str, Any]] = {}
    for lane in LANES:
        for capability in CAPABILITIES:
            identifiers = sorted(set(nested[lane][capability]))
            cell_id = f"{capability}/{lane}/repair"
            cell_sources[cell_id] = identifiers
            cells[cell_id] = {
                "accepted_unique_sources": len(identifiers),
                "source_queue_ids": identifiers,
                "meets_minimum": len(identifiers) >= MINIMUM_SOURCES_PER_CELL,
            }
    by_lane = {
        lane: {
            "accepted_source_edges": sum(cells[f"{capability}/{lane}/repair"]["accepted_unique_sources"] for capability in CAPABILITIES),
            "cells_meeting_minimum": sum(cells[f"{capability}/{lane}/repair"]["meets_minimum"] for capability in CAPABILITIES),
            "cells_total": len(CAPABILITIES),
        }
        for lane in LANES
    }
    by_capability = {
        capability: {
            "accepted_source_edges": sum(cells[f"{capability}/{lane}/repair"]["accepted_unique_sources"] for lane in LANES),
            "cells_meeting_minimum": sum(cells[f"{capability}/{lane}/repair"]["meets_minimum"] for lane in LANES),
            "cells_total": len(LANES),
        }
        for capability in CAPABILITIES
    }
    all_cells = all(value["meets_minimum"] for value in cells.values())
    evidence_payload = b"".join(canonical_json(row) + b"\n" for row in combined)
    report: dict[str, Any] = {
        "schema_version": AGGREGATE_SCHEMA,
        "plan_sha256": PLAN_SHA256,
        "status": "coverage-complete" if all_cells else "insufficient-coverage",
        "source_queue_sha256": sha256_bytes(source_queue_path.read_bytes()),
        "separation_attestation_sha256": separation_sha256,
        "waves": wave_manifests,
        "wave_count": len(wave_manifests),
        "failed_wave_count": sum(item["campaign_manifest"]["status"] == "failed" for item in wave_manifests),
        "unique_sources": len(combined),
        "unique_lineages": len(seen_lineage),
        "minimum_sources_per_cell": MINIMUM_SOURCES_PER_CELL,
        "coverage": {
            "cells": cells,
            "by_lane": by_lane,
            "by_capability": by_capability,
            "cells_meeting_minimum": sum(value["meets_minimum"] for value in cells.values()),
            "cells_total": len(cells),
            "all_cells_meet_minimum": all_cells,
        },
        "combined_evidence_sha256": sha256_bytes(evidence_payload),
        "evaluation_artifacts_read": 0,
    }
    report["aggregate_sha256"] = canonical_sha256(report)
    return combined, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-queue", type=Path, required=True)
    parser.add_argument(
        "--wave", type=Path, nargs=2, action="append", required=True,
        metavar=("EVIDENCE_JSONL", "SUMMARY_JSON"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    rows, summary = aggregate(args.source_queue, [(wave[0], wave[1]) for wave in args.wave])
    payload = b"".join(canonical_json(row) + b"\n" for row in rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": summary["status"], "waves": summary["wave_count"],
        "unique_sources": summary["unique_sources"],
        "cells_meeting_minimum": summary["coverage"]["cells_meeting_minimum"],
    }, sort_keys=True))
    return 0 if summary["coverage"]["all_cells_meet_minimum"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
