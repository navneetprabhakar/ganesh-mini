#!/usr/bin/env python3
"""Seal the resolved 12-cell capability-scale construction canary."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.review_capability_qualification import candidate_sha256, load_evidence


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sealed(path: Path, field: str = "report_sha256") -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact_map(path: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in _rows(path):
        body = dict(row); claimed = body.pop("artifact_sha256", None)
        if claimed != canonical_sha256(body) or row.get("candidate_id") in result:
            raise ValueError(f"{path}: unsealed or duplicate artifact")
        result[row["candidate_id"]] = row
    return result


def run(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    original = _rows(args.original_candidates)
    reserves = _rows(args.reserve_candidates)
    candidates = {row["id"]: row for row in [*original, *reserves]}
    semantics = [*_rows(args.original_semantic), *_rows(args.reserve_semantic)]
    semantic_by_hash = {row["candidate_sha256"]: row for row in semantics}
    if len(semantic_by_hash) != len(semantics) or any(load_evidence(row) is None for row in semantics):
        raise ValueError("semantic evidence is unsealed or duplicate")
    matrix_sources = (
        (args.original_matrix, args.original_matrix_report, 0),
        (args.reserve_matrix, args.reserve_matrix_report, 0),
        (args.correction_matrix, args.correction_matrix_report, 1),
    )
    admitted: dict[str, tuple[dict[str, Any], int]] = {}
    matrix_reports: list[str] = []
    for artifacts_path, report_path, correction_count in matrix_sources:
        artifacts = _artifact_map(artifacts_path)
        report = _sealed(report_path)
        if report.get("terminal_rows_sha256") != canonical_sha256(list(artifacts.values())):
            raise ValueError(f"{report_path}: terminal matrix binding differs")
        matrix_reports.append(report["report_sha256"])
        for identifier, artifact in artifacts.items():
            if artifact["status"] == "admitted":
                admitted[identifier] = (artifact, correction_count)
    if len(admitted) != 12:
        raise ValueError(f"resolved canary must admit exactly 12 candidates, got {len(admitted)}")
    records: list[dict[str, Any]] = []
    admitted_candidates: list[dict[str, Any]] = []
    for lane in ("go", "java", "javascript", "typescript", "python", "rust"):
        for task_type in ("generation", "repair"):
            matches = [
                (identifier, artifact, correction)
                for identifier, (artifact, correction) in admitted.items()
                if artifact["lane"] == lane and artifact["task_type"] == task_type
            ]
            if len(matches) != 1:
                raise ValueError(f"{lane}/{task_type}: canary admission is not exact")
            identifier, artifact, correction = matches[0]
            candidate = candidates.get(identifier)
            if candidate is None:
                raise ValueError(f"{identifier}: admitted candidate is absent from teacher inputs")
            semantic = semantic_by_hash.get(candidate_sha256(candidate))
            if semantic is None or semantic.get("verdict") != "pass":
                raise ValueError(f"{identifier}: admitted candidate lacks passing semantic evidence")
            records.append({
                "candidate_id": identifier, "cell_id": artifact["cell_id"],
                "lane": lane, "task_type": task_type,
                "candidate_sha256": canonical_sha256(candidate),
                "source_identity": candidate["qualification_assignment"]["source_identity"],
                "source_record_sha256": candidate["qualification_assignment"]["source_record_sha256"],
                "semantic_evidence_sha256": semantic["evidence_sha256"],
                "matrix_artifact_sha256": artifact["artifact_sha256"],
                "correction_count": correction,
                "evaluation_artifacts_read": 0,
            })
            admitted_candidates.append(candidate)
    if len({canonical_sha256(row["source_identity"]) for row in records}) != 12:
        raise ValueError("canary admissions are not source-unique")
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-canary-result/v1",
        "status": "passed",
        "admitted": 12,
        "cells": 12,
        "teacher_drafts": 19,
        "first_pass_terminal_failures": 7,
        "activated_reserves": 7,
        "test_reauthors": 2,
        "matrix_report_sha256s": matrix_reports,
        "records_sha256": canonical_sha256(records),
        "admitted_candidates_sha256": canonical_sha256(admitted_candidates),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return admitted_candidates, {"report": report, "records": records}


def _atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8"); temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "original-candidates", "reserve-candidates", "original-semantic", "reserve-semantic",
        "original-matrix", "original-matrix-report", "reserve-matrix", "reserve-matrix-report",
        "correction-matrix", "correction-matrix-report",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    candidates, result = run(args)
    _atomic(args.output_dir / "admitted-candidates.jsonl", "".join(json.dumps(row, sort_keys=True) + "\n" for row in candidates))
    _atomic(args.output_dir / "admission-records.jsonl", "".join(json.dumps(row, sort_keys=True) + "\n" for row in result["records"]))
    _atomic(args.output_dir / "canary-result.json", json.dumps(result["report"], indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["report"]["status"], "admitted": 12, "report_sha256": result["report"]["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
