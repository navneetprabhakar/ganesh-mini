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


def _valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str) and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _source_map(path: Path) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    for source in read_jsonl(path):
        identifier = source.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in sources:
            raise ValueError("source queue contains a malformed or duplicate ID")
        sources[identifier] = source
    return sources


def _load_summary(
    path: Path, evidence_path: Path, allowed_plan_sha256s: set[str],
) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop("summary_sha256", None)
    evidence_bytes = evidence_path.read_bytes()
    if (
        claimed != canonical_sha256(body)
        or value.get("schema_version") != CAMPAIGN_SCHEMA
        or value.get("plan_sha256") not in allowed_plan_sha256s
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
    allowed_plan_sha256s: set[str],
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
        or row.get("plan_sha256") not in allowed_plan_sha256s
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


def _coverage(rows: list[dict[str, Any]]) -> dict[str, Any]:
    nested = {lane: {capability: [] for capability in CAPABILITIES} for lane in LANES}
    for row in rows:
        for verdict in row["verdicts"]:
            if verdict["decision"] == "accept":
                nested[row["lane"]][verdict["primary_capability"]].append(row["source_queue_id"])
    cells: dict[str, dict[str, Any]] = {}
    for lane in LANES:
        for capability in CAPABILITIES:
            identifiers = sorted(set(nested[lane][capability]))
            cell_id = f"{capability}/{lane}/repair"
            cells[cell_id] = {
                "accepted_unique_sources": len(identifiers),
                "source_queue_ids": identifiers,
                "meets_minimum": len(identifiers) >= MINIMUM_SOURCES_PER_CELL,
            }
    by_lane = {
        lane: {
            "accepted_source_edges": sum(
                cells[f"{capability}/{lane}/repair"]["accepted_unique_sources"]
                for capability in CAPABILITIES
            ),
            "cells_meeting_minimum": sum(
                cells[f"{capability}/{lane}/repair"]["meets_minimum"]
                for capability in CAPABILITIES
            ),
            "cells_total": len(CAPABILITIES),
        }
        for lane in LANES
    }
    by_capability = {
        capability: {
            "accepted_source_edges": sum(
                cells[f"{capability}/{lane}/repair"]["accepted_unique_sources"] for lane in LANES
            ),
            "cells_meeting_minimum": sum(
                cells[f"{capability}/{lane}/repair"]["meets_minimum"] for lane in LANES
            ),
            "cells_total": len(LANES),
        }
        for capability in CAPABILITIES
    }
    all_cells = all(value["meets_minimum"] for value in cells.values())
    return {
        "cells": cells,
        "by_lane": by_lane,
        "by_capability": by_capability,
        "cells_meeting_minimum": sum(value["meets_minimum"] for value in cells.values()),
        "cells_total": len(cells),
        "all_cells_meet_minimum": all_cells,
    }


def _load_carry_forward_summary(
    summary_path: Path, evidence_path: Path, source_queue_path: Path,
    compatible_plan_sha256s: set[str],
) -> dict[str, Any]:
    value = json.loads(summary_path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop("aggregate_sha256", None)
    waves = value.get("waves")
    if (
        claimed != canonical_sha256(body)
        or value.get("schema_version") != AGGREGATE_SCHEMA
        or value.get("plan_sha256") not in compatible_plan_sha256s
        or value.get("source_queue_sha256") != sha256_bytes(source_queue_path.read_bytes())
        or value.get("combined_evidence_sha256") != sha256_bytes(evidence_path.read_bytes())
        or value.get("evaluation_artifacts_read") != 0
        or type(value.get("unique_sources")) is not int
        or type(value.get("unique_lineages")) is not int
        or not isinstance(value.get("separation_attestation_sha256s"), list)
        or not all(_valid_sha256(item) for item in value["separation_attestation_sha256s"])
        or not isinstance(waves, list) or value.get("wave_count") != len(waves)
    ):
        raise ValueError(f"ontology aggregate carry-forward is invalid: {summary_path}")
    for wave in waves:
        campaign = wave.get("campaign_manifest") if isinstance(wave, dict) else None
        campaign_body = dict(campaign) if isinstance(campaign, dict) else {}
        campaign_claimed = campaign_body.pop("summary_sha256", None)
        if (
            campaign_claimed != canonical_sha256(campaign_body)
            or campaign.get("plan_sha256") != value["plan_sha256"]
            or campaign.get("evaluation_artifacts_read") != 0
            or not _valid_sha256(wave.get("evidence_sha256"))
            or not _valid_sha256(wave.get("summary_file_sha256"))
        ):
            raise ValueError(f"ontology aggregate carry-forward wave is invalid: {summary_path}")
    return value


def aggregate(
    source_queue_path: Path,
    waves: list[tuple[Path, Path]],
    plan_sha256: str = PLAN_SHA256,
    compatible_plan_sha256s: tuple[str, ...] = (),
    carry_forwards: tuple[tuple[Path, Path, Path], ...] = (),
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not waves and not carry_forwards:
        raise ValueError("at least one ontology wave or carry-forward is required")
    allowed_plan_sha256s = {plan_sha256, *compatible_plan_sha256s}
    if any(
        len(value) != 64 or any(character not in "0123456789abcdef" for character in value)
        for value in allowed_plan_sha256s
    ):
        raise ValueError("ontology aggregate plan SHA-256 is malformed")
    sources = _source_map(source_queue_path)

    combined: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_lineage: set[tuple[str, str, str]] = set()
    separation_sha256s: list[str] = []
    wave_manifests: list[dict[str, Any]] = []
    carry_forward_manifests: list[dict[str, Any]] = []
    explicitly_compatible = set(compatible_plan_sha256s)
    for index, (evidence_path, summary_path, predecessor_source_queue_path) in enumerate(carry_forwards):
        summary = _load_carry_forward_summary(
            summary_path, evidence_path, predecessor_source_queue_path, explicitly_compatible,
        )
        predecessor_sources = _source_map(predecessor_source_queue_path)
        rows = read_jsonl(evidence_path)
        if len(rows) != summary["unique_sources"]:
            raise ValueError("carry-forward source count differs from its aggregate summary")
        predecessor_lineages: set[tuple[str, str, str]] = set()
        batch_members: dict[tuple[str, ...], set[str]] = defaultdict(set)
        for row in rows:
            separation_sha256 = row.get("separation_attestation_sha256")
            if separation_sha256 not in summary["separation_attestation_sha256s"]:
                raise ValueError("carry-forward row uses an unbound separation attestation")
            _old_source, old_lineage = _validate_evidence_row(
                row, predecessor_sources, separation_sha256, {summary["plan_sha256"]},
            )
            _new_source, new_lineage = _validate_evidence_row(
                row, sources, separation_sha256, {summary["plan_sha256"]},
            )
            identifier = row["source_queue_id"]
            if old_lineage != new_lineage or identifier in seen_ids or new_lineage in seen_lineage:
                raise ValueError(f"duplicate or changed carry-forward source lineage: {identifier}")
            seen_ids.add(identifier); seen_lineage.add(new_lineage); predecessor_lineages.add(old_lineage)
            batch_members[tuple(row["batch_source_queue_ids"])].add(identifier)
            combined.append(row)
        for batch_ids, observed_ids in batch_members.items():
            if observed_ids != set(batch_ids):
                raise ValueError(f"ontology carry-forward contains a partial successful batch: {batch_ids}")
        if len(predecessor_lineages) != summary["unique_lineages"]:
            raise ValueError("carry-forward lineage count differs from its aggregate summary")
        if _coverage(rows) != summary.get("coverage"):
            raise ValueError("carry-forward coverage differs from its aggregate summary")
        for separation_sha256 in summary["separation_attestation_sha256s"]:
            if separation_sha256 not in separation_sha256s:
                separation_sha256s.append(separation_sha256)
        carry_forward_manifests.append({
            "carry_forward_index": index,
            "plan_sha256": summary["plan_sha256"],
            "evidence_sha256": sha256_bytes(evidence_path.read_bytes()),
            "summary_file_sha256": sha256_bytes(summary_path.read_bytes()),
            "source_queue_sha256": sha256_bytes(predecessor_source_queue_path.read_bytes()),
            "aggregate_sha256": summary["aggregate_sha256"],
            "unique_sources": summary["unique_sources"],
            "unique_lineages": summary["unique_lineages"],
        })
    for index, (evidence_path, summary_path) in enumerate(waves):
        summary = _load_summary(summary_path, evidence_path, allowed_plan_sha256s)
        current_separation = summary["separation_attestation_sha256"]
        if current_separation not in separation_sha256s:
            separation_sha256s.append(current_separation)
        rows = read_jsonl(evidence_path)
        if len(rows) != summary["completed"]:
            raise ValueError(f"ontology campaign completed count differs from evidence: {summary_path}")
        wave_ids: set[str] = set()
        wave_coverage = {lane: {capability: 0 for capability in CAPABILITIES} for lane in LANES}
        batch_members: dict[tuple[str, ...], set[str]] = defaultdict(set)
        for row in rows:
            source, lineage = _validate_evidence_row(
                row, sources, current_separation, allowed_plan_sha256s,
            )
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
    coverage = _coverage(combined)
    all_cells = coverage["all_cells_meet_minimum"]
    evidence_payload = b"".join(canonical_json(row) + b"\n" for row in combined)
    report: dict[str, Any] = {
        "schema_version": AGGREGATE_SCHEMA,
        "plan_sha256": plan_sha256,
        "compatible_plan_sha256s": sorted(allowed_plan_sha256s - {plan_sha256}),
        "status": "coverage-complete" if all_cells else "insufficient-coverage",
        "source_queue_sha256": sha256_bytes(source_queue_path.read_bytes()),
        "separation_attestation_sha256s": separation_sha256s,
        "waves": wave_manifests,
        "wave_count": len(wave_manifests),
        "failed_wave_count": sum(item["campaign_manifest"]["status"] == "failed" for item in wave_manifests),
        "unique_sources": len(combined),
        "unique_lineages": len(seen_lineage),
        "minimum_sources_per_cell": MINIMUM_SOURCES_PER_CELL,
        "coverage": coverage,
        "combined_evidence_sha256": sha256_bytes(evidence_payload),
        "evaluation_artifacts_read": 0,
    }
    if carry_forward_manifests:
        report["carry_forwards"] = carry_forward_manifests
        report["carry_forward_count"] = len(carry_forward_manifests)
    report["aggregate_sha256"] = canonical_sha256(report)
    return combined, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-queue", type=Path, required=True)
    parser.add_argument(
        "--wave", type=Path, nargs=2, action="append", required=True,
        metavar=("EVIDENCE_JSONL", "SUMMARY_JSON"),
    )
    parser.add_argument(
        "--carry-forward", type=Path, nargs=3, action="append", default=[],
        metavar=("AGGREGATE_EVIDENCE_JSONL", "AGGREGATE_SUMMARY_JSON", "SOURCE_QUEUE_JSONL"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--plan-sha256", default=PLAN_SHA256)
    parser.add_argument("--compatible-plan-sha256", action="append", default=[])
    args = parser.parse_args()
    rows, summary = aggregate(
        args.source_queue, [(wave[0], wave[1]) for wave in args.wave],
        args.plan_sha256, tuple(args.compatible_plan_sha256),
        tuple((item[0], item[1], item[2]) for item in args.carry_forward),
    )
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
