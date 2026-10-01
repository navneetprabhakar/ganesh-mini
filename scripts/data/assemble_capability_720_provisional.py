#!/usr/bin/env python3
"""Carry the sealed 174 training-entry rows into a provisional 720-row cohort."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256
from scripts.data.build_capability_scale_queue import source_key
from scripts.data.run_capability_scale_delta_audits import _write_json_atomic, _write_jsonl_atomic
from scripts.data.run_capability_scale_final_matrix import _sealed, _jsonl


ENTRY_SEAL = "fbf45982984c2c669e03abf1c773d768019651184547104271de12c42f79318c"
MATERIALIZED_SCALE_SEAL = "8f27cb55c1b6fedea24b2a2e7d086a78203b327c94022fa18f08a213a0a1023b"
RIGHTS = ("prompt", "answer", "tests", "redistribution", "model_training")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _entry_record(row: dict[str, Any], v2: dict[str, dict[str, Any]], v9: dict[str, dict[str, Any]]) -> dict[str, Any]:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    if claimed != canonical_sha256(body) or row.get("evaluation_artifacts_read") != 0:
        raise ValueError("training-entry lineage row is not sealed")
    identifier = row["record_id"]
    if row["origin"] == "v2-generation":
        wrapper = v2.get(identifier)
        if wrapper is None:
            raise ValueError(f"{identifier}: missing V2 record")
        record = wrapper["record"]
        if wrapper.get("qualification", {}).get("candidate_sha256") != row["upstream_qualification"]["candidate_sha256"]:
            raise ValueError(f"{identifier}: V2 qualification hash mismatch")
    elif row["origin"] == "v9-repair":
        record = v9.get(identifier)
        if record is None:
            raise ValueError(f"{identifier}: missing V9 record")
        if canonical_sha256(record) != row["upstream_qualification"]["candidate_sha256"]:
            raise ValueError(f"{identifier}: V9 candidate hash mismatch")
    else:
        raise ValueError(f"{identifier}: unsupported training-entry origin")
    if canonical_sha256(record) != row["record_sha256"]:
        raise ValueError(f"{identifier}: training-entry record hash mismatch")
    copied = copy.deepcopy(record)
    copied["source"] = copy.deepcopy(row["source"])
    copied["primary_capability"] = row["primary_capability"]
    copied["cell_id"] = row["cell_id"]
    if (
        copied.get("id") != identifier or copied.get("lane") != row["lane"]
        or copied.get("task_type") != row["task_type"]
        or source_key(copied).replace("\0", "|") != row["source_identity"]
        or any(copied.get("rights", {}).get(key) is not True for key in RIGHTS)
    ):
        raise ValueError(f"{identifier}: retained row lineage differs")
    return copied


def assemble(
    entry_manifest_path: Path, lineage_path: Path, v2_path: Path, v9_path: Path,
    scale_path: Path, scale_report_path: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    entry = _sealed(json.loads(entry_manifest_path.read_text(encoding="utf-8")), "manifest_sha256", "training entry")
    scale_report = _sealed(json.loads(scale_report_path.read_text(encoding="utf-8")), "report_sha256", "scale assembly")
    lineage = _jsonl(lineage_path)
    scale = _jsonl(scale_path)
    if (
        entry.get("manifest_sha256") != ENTRY_SEAL or entry.get("status") != "passed"
        or entry.get("records") != 174 or len(lineage) != 174
        or scale_report.get("report_sha256") != MATERIALIZED_SCALE_SEAL
        or scale_report.get("status") != "verified-envelopes-separation-pending"
        or scale_report.get("records") != 546 or len(scale) != 546
        or scale_report.get("materialized_rows_sha256") != canonical_sha256(scale)
        or scale_report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("training-entry or scale assembly input differs from frozen evidence")
    v2_rows = _jsonl(v2_path)
    v9_rows = _jsonl(v9_path)
    v2 = {item["record"]["id"]: item for item in v2_rows}
    v9 = {item["id"]: item for item in v9_rows}
    if len(v2) != len(v2_rows) or len(v9) != len(v9_rows):
        raise ValueError("upstream training-entry source records are duplicated")
    retained = [_entry_record(row, v2, v9) for row in lineage]
    combined = retained + scale
    ids = [row["id"] for row in combined]
    sources = [source_key(row) for row in combined]
    if len(set(ids)) != 720 or len(set(sources)) != 720:
        raise ValueError("720-row provisional cohort reuses ID or source identity")
    counts = Counter(
        row.get("cell_id") or row.get("qualification_assignment", {}).get("cell_id")
        for row in combined
    )
    expected = {f"{capability}/{lane}/{kind}" for capability in CAPABILITIES for lane in ("go", "java", "javascript", "typescript", "python", "rust") for kind in ("generation", "repair")}
    if set(counts) != expected or any(counts[cell] != 6 for cell in expected):
        raise ValueError("720-row provisional cohort is not six per cell")
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-capability-720-provisional/v1",
        "status": "separation-and-quality-pending",
        "records": 720, "retained_training_entry": 174, "new_scale": 546,
        "unique_record_ids": 720, "unique_source_identities": 720,
        "entry_manifest_sha256": ENTRY_SEAL,
        "lineage_file_sha256": file_sha256(lineage_path),
        "v2_admitted_file_sha256": file_sha256(v2_path),
        "v9_complete_file_sha256": file_sha256(v9_path),
        "scale_report_sha256": MATERIALIZED_SCALE_SEAL,
        "scale_file_sha256": file_sha256(scale_path),
        "retained_rows_sha256": canonical_sha256(retained),
        "capability_rows_sha256": canonical_sha256(combined),
        "cell_counts": dict(sorted(counts.items())),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return retained, combined, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entry-manifest", type=Path, required=True)
    parser.add_argument("--entry-lineage", type=Path, required=True)
    parser.add_argument("--v2-admitted", type=Path, required=True)
    parser.add_argument("--v9-complete", type=Path, required=True)
    parser.add_argument("--scale-candidates", type=Path, required=True)
    parser.add_argument("--scale-report", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise ValueError("provisional 720 output already exists")
    retained, combined, report = assemble(
        args.entry_manifest, args.entry_lineage, args.v2_admitted, args.v9_complete,
        args.scale_candidates, args.scale_report,
    )
    _write_jsonl_atomic(args.output_dir / "retained-174.jsonl", retained)
    _write_jsonl_atomic(args.output_dir / "capability-720.jsonl", combined)
    _write_json_atomic(args.output_dir / "report.json", report)
    print(json.dumps({"status": report["status"], "records": 720, "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
