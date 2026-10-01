#!/usr/bin/env python3
"""Select byte-preserved broad replay after the 720-row Gate 3 capability seal."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import CAPABILITIES, LANES, TASK_TYPES, canonical_sha256
from scripts.data.build_capability_scale_queue import PRIOR_CORPUS_SHA256, PLAN_SHA256, source_key


RIGHTS = ("prompt", "answer", "tests", "redistribution", "model_training")
SOURCE_FIELDS = ("dataset", "revision", "record_id", "source_record_sha256", "license", "uri")
PAIRS = {(lane, task_type) for lane in LANES for task_type in TASK_TYPES}
CELLS = {f"{capability}/{lane}/{task_type}" for capability in CAPABILITIES for lane, task_type in PAIRS}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _lines(data: bytes, label: str) -> list[tuple[dict[str, Any], bytes]]:
    if not data or not data.endswith(b"\n"):
        raise ValueError(f"{label}: expected nonempty newline-terminated JSONL")
    rows = []
    for raw in data.splitlines(keepends=True):
        if not raw.strip():
            raise ValueError(f"{label}: blank JSONL row")
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError(f"{label}: JSONL row is not an object")
        rows.append((value, raw))
    return rows


def _identity(row: dict[str, Any], label: str) -> str:
    sources = [value for value in (row.get("source"), row.get("lineage")) if value is not None]
    if not sources:
        raise ValueError(f"{label}: incomplete source rights or lineage")
    for source in sources:
        if not isinstance(source, dict) or any(not isinstance(source.get(k), str) or not source[k] for k in SOURCE_FIELDS):
            raise ValueError(f"{label}: incomplete source rights or lineage")
        if len(source["source_record_sha256"]) != 64 or any(c not in "0123456789abcdef" for c in source["source_record_sha256"]):
            raise ValueError(f"{label}: malformed source record hash")
    if any(tuple(source[k] for k in SOURCE_FIELDS[:4]) !=
           tuple(sources[0][k] for k in SOURCE_FIELDS[:4]) for source in sources[1:]):
        raise ValueError(f"{label}: conflicting source and lineage identities")
    source = sources[0]
    identity = source_key(row)
    assignment = row.get("qualification_assignment")
    if assignment is not None and (
        not isinstance(assignment, dict)
        or assignment.get("source_identity") != {key: source[key] for key in ("dataset", "revision", "record_id")}
        or assignment.get("source_record_sha256") != source["source_record_sha256"]
    ):
        raise ValueError(f"{label}: qualification source identity differs from lineage")
    return identity


def _rights(row: dict[str, Any], label: str) -> None:
    rights = row.get("rights")
    if not isinstance(rights, dict) or any(rights.get(key) is not True for key in RIGHTS):
        raise ValueError(f"{label}: incomplete approved rights")


def _capability_rows(data: bytes, manifest: dict[str, Any]) -> tuple[set[str], set[str]]:
    body = dict(manifest)
    claimed = body.pop("manifest_sha256", None)
    if (
        claimed != canonical_sha256(body)
        or manifest.get("schema_version") != "ganesh-mini-gate3-capability-720-seal/v1"
        or manifest.get("status") != "passed"
        or manifest.get("plan_sha256") != PLAN_SHA256
        or manifest.get("records") != 720
        or manifest.get("capability_rows_sha256") != _sha256(data)
        or manifest.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("capability input is not a valid sealed 720-row admission")
    rows = _lines(data, "capability input")
    if len(rows) != 720:
        raise ValueError("capability input must contain exactly 720 rows")
    ids: set[str] = set()
    sources: set[str] = set()
    counts: Counter[str] = Counter()
    for row, _ in rows:
        identifier = row.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in ids:
            raise ValueError("capability input has missing or duplicate record ID")
        ids.add(identifier)
        _rights(row, identifier)
        identity = _identity(row, identifier)
        if identity in sources:
            raise ValueError("capability input reuses a source")
        sources.add(identity)
        cell = row.get("cell_id") or row.get("qualification_assignment", {}).get("cell_id")
        if cell not in CELLS or cell.split("/")[1:] != [row.get("lane"), row.get("task_type")]:
            raise ValueError(f"{identifier}: invalid capability cell")
        if row.get("evaluation_artifacts_read", 0) != 0:
            raise ValueError(f"{identifier}: evaluation read count is nonzero")
        counts[cell] += 1
    if set(counts) != CELLS or any(count != 6 for count in counts.values()):
        raise ValueError("capability input does not contain six admissions per cell")
    return ids, sources


def select(prior_bytes: bytes, capability_bytes: bytes, capability_manifest: dict[str, Any]) -> tuple[bytes, dict[str, Any]]:
    """Return exact prior JSONL lines and a sealed selection manifest; write nothing."""
    if _sha256(prior_bytes) != PRIOR_CORPUS_SHA256:
        raise ValueError("frozen prior corpus hash differs")
    capability_ids, capability_sources = _capability_rows(capability_bytes, capability_manifest)
    rows = _lines(prior_bytes, "prior corpus")
    if len(rows) != 3225:
        raise ValueError("frozen prior corpus row count differs")
    buckets: dict[tuple[str, str], list[tuple[str, dict[str, Any], bytes]]] = {pair: [] for pair in PAIRS}
    prior_ids: set[str] = set()
    for row, raw in rows:
        identifier = row.get("id")
        pair = (row.get("lane"), row.get("task_type"))
        if not isinstance(identifier, str) or not identifier or identifier in prior_ids or pair not in PAIRS:
            raise ValueError("prior corpus has invalid ID or lane/task type")
        prior_ids.add(identifier)
        _rights(row, identifier)
        identity = _identity(row, identifier)
        if identity in capability_sources or identifier in capability_ids:
            continue
        if not isinstance(row.get("messages"), list) or not (row.get("verification_task") or row.get("verification")):
            raise ValueError(f"{identifier}: missing training or verification record")
        rank = _sha256(f"{PLAN_SHA256}\0{pair[0]}\0{pair[1]}\0{identifier}\0{identity}".encode())
        buckets[pair].append((rank, row, raw))
    chosen: list[tuple[dict[str, Any], bytes]] = []
    selected_sources: set[str] = set()
    for pair in sorted(PAIRS):
        bucket = sorted(buckets[pair], key=lambda item: (item[0], item[1]["id"]))
        pair_count = 0
        for _, row, raw in bucket:
            identity = _identity(row, row["id"])
            if identity not in selected_sources:
                chosen.append((row, raw))
                selected_sources.add(identity)
                pair_count += 1
            if pair_count == 15:
                break
        if pair_count != 15:
            raise ValueError(f"{pair}: fewer than 15 source-unique replay rows")
    selected_ids = [row["id"] for row, _ in chosen]
    if len(chosen) != 180 or len(set(selected_ids)) != 180 or len(selected_sources) != 180:
        raise ValueError("broad replay IDs or sources are not globally unique")
    output = b"".join(raw for _, raw in chosen)
    manifest = {
        "schema_version": "ganesh-mini-gate3-broad-replay-selection/v1",
        "status": "selected-pending-final-corpus-gates",
        "plan_sha256": PLAN_SHA256,
        "prior_corpus_sha256": PRIOR_CORPUS_SHA256,
        "capability_manifest_sha256": capability_manifest["manifest_sha256"],
        "capability_rows_sha256": _sha256(capability_bytes),
        "records": 180,
        "per_lane_task_type": 15,
        "unique_record_ids": 180,
        "unique_source_identities": 180,
        "selected_record_ids": selected_ids,
        "replay_jsonl_sha256": _sha256(output),
        "evaluation_artifacts_read": 0,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    return output, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--capability-records", type=Path, required=True)
    parser.add_argument("--capability-manifest", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    args = parser.parse_args()
    if args.output_jsonl.exists() or args.output_manifest.exists():
        raise ValueError("replay outputs already exist")
    selected, manifest = select(
        args.prior_corpus.read_bytes(), args.capability_records.read_bytes(),
        json.loads(args.capability_manifest.read_text(encoding="utf-8")),
    )
    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.output_jsonl.open("xb") as handle:
        handle.write(selected)
    with args.output_manifest.open("x", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"records": 180, "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
