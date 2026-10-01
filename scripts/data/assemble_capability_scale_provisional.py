#!/usr/bin/env python3
"""Assemble the 546 executable scale candidates without granting admission.

Only independently sealed terminal outcomes can contribute.  This script
neither opens evaluation content nor performs separation or training.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_scale_queue import source_key
from scripts.data.prepare_capability_scale_prospective_replacement import (
    CELL as PROSPECTIVE_CELL,
    DUPLICATE_ID,
    NEW_ID as PROSPECTIVE_ID,
    ORIGINAL_MANIFEST_SHA256,
    PLAN_SHA256 as PROSPECTIVE_PLAN_SHA256,
)
from scripts.data.run_capability_scale_delta_audits import _write_json_atomic, _write_jsonl_atomic
from scripts.data.run_capability_scale_final_matrix import _jsonl, _sealed


def _report(path: Path, label: str) -> dict[str, Any]:
    report = _sealed(json.loads(path.read_text(encoding="utf-8")), "report_sha256", label)
    if report.get("evaluation_artifacts_read") != 0:
        raise ValueError(f"{label}: evaluation artifact exposure")
    return report


def _rows(path: Path, report: dict[str, Any], field: str, label: str) -> list[dict[str, Any]]:
    rows = _jsonl(path)
    if report.get(field) != canonical_sha256(rows):
        raise ValueError(f"{label}: rows differ from sealed report")
    if field == "terminal_rows_sha256" and "terminal_artifact_sha256s" in report:
        if report["terminal_artifact_sha256s"] != [row.get("artifact_sha256") for row in rows]:
            raise ValueError(f"{label}: ordered artifact hashes differ")
        for row in rows:
            _sealed(row, "artifact_sha256", str(row.get("candidate_id")))
            if row.get("evaluation_artifacts_read") != 0:
                raise ValueError(f"{label}: artifact read evaluation data")
    return rows


def _attached(path: Path, report_path: Path, label: str) -> dict[str, dict[str, Any]]:
    report = _report(report_path, label)
    rows = _rows(path, report, "attached_candidates_sha256", label)
    indexed = {row.get("id"): row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError(f"{label}: duplicate candidate identity")
    return indexed


def _matrix(path: Path, report_path: Path, label: str) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    report = _report(report_path, label)
    rows = _rows(path, report, "terminal_rows_sha256", label)
    if report.get("requested") != len(rows):
        raise ValueError(f"{label}: incomplete matrix")
    indexed = {row.get("candidate_id"): row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError(f"{label}: duplicate matrix identity")
    return indexed, report


def _admitted(candidate: dict[str, Any], matrix: dict[str, Any], label: str) -> None:
    assignment = candidate.get("qualification_assignment")
    if (
        matrix.get("status") != "admitted" or matrix.get("candidate_sha256") != canonical_sha256(candidate)
        or not isinstance(assignment, dict) or assignment.get("cell_id") != matrix.get("cell_id")
        or candidate.get("lane") != matrix.get("lane") or candidate.get("task_type") != matrix.get("task_type")
        or candidate.get("teacher_evidence", {}).get("evaluation_artifacts_read") != 0
    ):
        raise ValueError(f"{label}: candidate or matrix admission differs")


def assemble(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    base, go, reserve = args.first_pass_root, args.first_pass_root / "go-single-worker-v1", args.first_pass_root / "go-single-worker-v1/reserve-v1"
    entry = _sealed(json.loads(args.training_entry_manifest.read_text(encoding="utf-8")), "manifest_sha256", "training entry")
    if entry.get("status") != "passed" or entry.get("records") != 174 or entry.get("evaluation_artifacts_read") != 0:
        raise ValueError("training-entry inventory is not the frozen passing 174 rows")
    top_up = entry.get("cell_top_up")
    if not isinstance(top_up, dict) or len(top_up) != 120 or sum(top_up.values()) != 546:
        raise ValueError("training-entry cell top-up differs")

    canary_report = _report(args.canary_dir / "canary-result.json", "scale canary")
    canary = _rows(args.canary_dir / "admitted-candidates.jsonl", canary_report, "admitted_candidates_sha256", "scale canary")
    if canary_report.get("status") != "passed" or len(canary) != 12 or canary_report.get("admitted") != 12:
        raise ValueError("scale canary is not 12/12 passing")

    reconciliation_report = _report(go / "reconciled/reconciliation-report.json", "correction reconciliation")
    reconciliation = _rows(go / "reconciled/terminal-artifacts.jsonl", reconciliation_report, "terminal_rows_sha256", "correction reconciliation")
    if reconciliation_report.get("status") != "passed" or reconciliation_report.get("counts") != {"admitted": 518, "rejected": 16} or len(reconciliation) != 534:
        raise ValueError("first-pass correction reconciliation differs")
    original_matrix, original_report = _matrix(go / "assessment/terminal-artifacts.jsonl", go / "assessment/matrix-report.json", "derived first pass")
    corrected_matrix, corrected_report = _matrix(base / "test-reauthor-v1/matrix/terminal-artifacts.jsonl", base / "test-reauthor-v1/matrix/matrix-report.json", "first-pass correction")
    if reconciliation_report.get("derived_matrix_report_sha256") != original_report["report_sha256"] or reconciliation_report.get("correction_matrix_report_sha256") != corrected_report["report_sha256"]:
        raise ValueError("reconciliation does not bind its matrix inputs")
    original_candidates = _attached(base / "delta-transport-retry-v1/merged/attached-candidates.jsonl", base / "delta-transport-retry-v1/merged/delta-audit-report.json", "first-pass delta")
    corrected_candidates = _attached(base / "test-reauthor-v1/delta/attached-candidates.jsonl", base / "test-reauthor-v1/delta/delta-audit-report.json", "first-pass correction delta")

    selected = list(canary)
    for row in reconciliation:
        if row["status"] != "admitted":
            continue
        identifier = row["candidate_id"]
        correction = row["source_stage"] == "correction-matrix"
        matrix = (corrected_matrix if correction else original_matrix).get(identifier)
        candidate = (corrected_candidates if correction else original_candidates).get(identifier)
        if matrix is None or candidate is None or matrix.get("artifact_sha256") != row.get("source_artifact_sha256"):
            raise ValueError(f"{identifier}: reconciled admission is not bound to its terminal matrix")
        _admitted(candidate, matrix, identifier)
        selected.append(candidate)

    reserve_matrix, reserve_report = _matrix(reserve / "matrix/terminal-artifacts.jsonl", reserve / "matrix/matrix-report.json", "reserve matrix")
    reserve_correction_matrix, reserve_correction_report = _matrix(reserve / "correction-v1/matrix/terminal-artifacts.jsonl", reserve / "correction-v1/matrix/matrix-report.json", "reserve correction matrix")
    if reserve_report.get("counts") != {"admitted": 15, "rejected": 1} or reserve_correction_report.get("counts") != {"admitted": 1}:
        raise ValueError("reserve matrix outcomes differ from the terminal 15+1 correction")
    reserve_candidates = _attached(reserve / "delta/attached-candidates.jsonl", reserve / "delta/delta-audit-report.json", "reserve delta")
    reserve_correction_candidates = _attached(reserve / "correction-v1/delta/attached-candidates.jsonl", reserve / "correction-v1/delta/delta-audit-report.json", "reserve correction delta")
    if set(reserve_correction_matrix) != {identifier for identifier, row in reserve_matrix.items() if row["status"] == "rejected"}:
        raise ValueError("reserve correction is not exactly the sole rejected reserve")
    prospective_paths = [
        getattr(args, "prospective_queue", None),
        getattr(args, "prospective_manifest", None),
        getattr(args, "prospective_dir", None),
    ]
    prospective = all(path is not None for path in prospective_paths)
    if any(path is not None for path in prospective_paths) and not prospective:
        raise ValueError("prospective queue, manifest, and directory must be supplied together")
    for identifier, matrix in reserve_matrix.items():
        corrected = matrix["status"] == "rejected"
        terminal = reserve_correction_matrix[identifier] if corrected else matrix
        candidate = (reserve_correction_candidates if corrected else reserve_candidates).get(identifier)
        if candidate is None:
            raise ValueError(f"{identifier}: reserve attachment missing")
        _admitted(candidate, terminal, identifier)
        if prospective and identifier == DUPLICATE_ID:
            continue  # Canary already owns this exact source identity and candidate ID.
        selected.append(candidate)

    prospective_binding: dict[str, Any] | None = None
    if prospective:
        manifest = _sealed(json.loads(args.prospective_manifest.read_text(encoding="utf-8")), "manifest_sha256", "prospective source manifest")
        queue = _jsonl(args.prospective_queue)
        if (
            manifest.get("status") != "source-prebound-not-generated"
            or manifest.get("plan_sha256") != PROSPECTIVE_PLAN_SHA256
            or manifest.get("original_queue_manifest_sha256") != ORIGINAL_MANIFEST_SHA256
            or manifest.get("maximum_teacher_drafts_after") != 1059
            or manifest.get("evaluation_artifacts_read") != 0
            or len(queue) != 1 or queue[0].get("id") != PROSPECTIVE_ID
            or queue[0].get("cell_id") != PROSPECTIVE_CELL
            or queue[0].get("request_sha256") != manifest.get("request_sha256")
            or source_key(queue[0]).replace("\0", "|") != manifest.get("selected_source_identity")
        ):
            raise ValueError("prospective source binding is not the sealed one-cell exception")
        root = args.prospective_dir
        teacher = _report(root / "teacher/teacher-report.json", "prospective teacher")
        semantic = _report(root / "semantic/semantic-report.json", "prospective semantic")
        test_author = _report(root / "test-author/test-author-report.json", "prospective test author")
        delta = _report(root / "delta/delta-audit-report.json", "prospective delta")
        matrix_rows, matrix_report = _matrix(root / "matrix/terminal-artifacts.jsonl", root / "matrix/matrix-report.json", "prospective matrix")
        candidates = _attached(root / "delta/attached-candidates.jsonl", root / "delta/delta-audit-report.json", "prospective delta")
        if (
            any(report.get("status") not in ("passed", "complete") for report in (teacher, semantic, test_author, delta, matrix_report))
            or teacher.get("requested") != 1 or teacher.get("counts") != {"generated": 1}
            or teacher.get("queue_manifest_sha256") != manifest["manifest_sha256"]
            or semantic.get("counts", {}).get("passed") != 1
            or test_author.get("counts") != {"structurally-valid": 1}
            or delta.get("counts") != {"passed": 1}
            or matrix_report.get("counts") != {"admitted": 1}
            or set(matrix_rows) != {PROSPECTIVE_ID} or set(candidates) != {PROSPECTIVE_ID}
        ):
            raise ValueError("prospective replacement did not pass every construction stage")
        candidate = candidates[PROSPECTIVE_ID]
        terminal = matrix_rows[PROSPECTIVE_ID]
        _admitted(candidate, terminal, PROSPECTIVE_ID)
        if (
            source_key(candidate) != source_key(queue[0])
            or candidate.get("teacher_evidence", {}).get("request_sha256") != queue[0]["request_sha256"]
        ):
            raise ValueError("prospective admission differs from prebound source")
        selected.append(candidate)
        prospective_binding = {
            "manifest_sha256": manifest["manifest_sha256"],
            "teacher_report_sha256": teacher["report_sha256"],
            "semantic_report_sha256": semantic["report_sha256"],
            "test_author_report_sha256": test_author["report_sha256"],
            "delta_report_sha256": delta["report_sha256"],
            "matrix_report_sha256": matrix_report["report_sha256"],
            "excluded_duplicate_candidate_id": DUPLICATE_ID,
        }

    ids = [row.get("id") for row in selected]
    if len(selected) != 546 or len(set(ids)) != 546:
        raise ValueError(f"scale cohort is not 546 candidate-unique rows: rows={len(selected)}, unique={len(set(ids))}")
    sources = [source_key(row) for row in selected]
    if len(set(sources)) != 546:
        raise ValueError("scale cohort reuses a source identity")
    counts = Counter(row.get("qualification_assignment", {}).get("cell_id") for row in selected)
    if dict(counts) != {cell: count for cell, count in top_up.items() if count}:
        raise ValueError("scale cohort does not fill exact frozen per-cell deficits")
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-scale-provisional-assembly/v2" if prospective else "ganesh-mini-gate3-scale-provisional-assembly/v1",
        "status": "provisional-separation-pending", "records": 546,
        "canary": 12, "first_pass": 518, "reserves": 15 if prospective else 16,
        "training_entry_manifest_sha256": entry["manifest_sha256"],
        "canary_report_sha256": canary_report["report_sha256"],
        "reconciliation_report_sha256": reconciliation_report["report_sha256"],
        "reserve_matrix_report_sha256": reserve_report["report_sha256"],
        "reserve_correction_matrix_report_sha256": reserve_correction_report["report_sha256"],
        "candidate_rows_sha256": canonical_sha256(selected),
        "cell_counts": dict(sorted(counts.items())),
        "unique_record_ids": len(set(ids)), "unique_source_identities": len(set(sources)),
        "evaluation_artifacts_read": 0,
    }
    if prospective_binding is not None:
        report["prospective_replacement"] = prospective_binding
        report["prospective_replacements"] = 1
    report["report_sha256"] = canonical_sha256(report)
    return selected, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--training-entry-manifest", type=Path, required=True)
    parser.add_argument("--canary-dir", type=Path, required=True)
    parser.add_argument("--first-pass-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--prospective-queue", type=Path)
    parser.add_argument("--prospective-manifest", type=Path)
    parser.add_argument("--prospective-dir", type=Path)
    args = parser.parse_args()
    rows, report = assemble(args)
    if args.output_dir.exists():
        raise ValueError("provisional scale assembly output already exists")
    _write_jsonl_atomic(args.output_dir / "candidates.jsonl", rows)
    _write_json_atomic(args.output_dir / "report.json", report)
    print(json.dumps({"status": report["status"], "records": 546, "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
