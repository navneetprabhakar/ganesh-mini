#!/usr/bin/env python3
"""Repeat one sealed unresolved matrix input in isolation for diagnosis only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_capability_scale_final_matrix import (
    _execute_one, _evidence, _jsonl, _sealed, _stable_teacher_projection,
    _validate_delta, _validate_test_evidence,
)
from scripts.data.run_repair_delta_evidence import _executable_evidence
from scripts.verify.sandbox import verify


def run(args: argparse.Namespace) -> dict:
    report = _sealed(json.loads(args.parent_report.read_text(encoding="utf-8")),
                     "report_sha256", "parent matrix report")
    terminal = _jsonl(args.parent_artifacts)
    if (
        report.get("requested") != len(terminal)
        or report.get("terminal_rows_sha256") != canonical_sha256(terminal)
        or report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("parent matrix report does not bind terminal rows")
    parent = next((row for row in terminal if row.get("candidate_id") == args.candidate_id), None)
    if parent is None or parent.get("status") != "unresolved":
        raise ValueError("diagnostic target is not a sealed unresolved parent result")
    _sealed(parent, "artifact_sha256", "parent matrix artifact")

    teacher = next((row for row in _jsonl(args.teacher_candidates) if row.get("id") == args.candidate_id), None)
    candidate = next((row for row in _jsonl(args.attached_candidates) if row.get("id") == args.candidate_id), None)
    delta_row = next((row for row in _jsonl(args.delta_artifacts) if row.get("candidate_id") == args.candidate_id), None)
    if teacher is None or candidate is None or delta_row is None:
        raise ValueError("diagnostic target missing from upstream cohort")
    _sealed(delta_row, "artifact_sha256", "delta artifact")
    if (
        candidate.get("lane") != "go"
        or delta_row.get("status") != "passed"
        or canonical_sha256(_stable_teacher_projection(candidate))
        != canonical_sha256(_stable_teacher_projection(teacher))
    ):
        raise ValueError("diagnostic target is not an unchanged passing-delta Go candidate")
    test = _evidence(delta_row, ("test_attachment", "test_author_evidence", "test_evidence"), "test-author")
    delta = _evidence(delta_row, ("delta_evidence", "delta_audit"), "delta")
    _validate_test_evidence(candidate, test)
    _validate_delta(candidate, delta)
    args.run_dir.mkdir(parents=True, exist_ok=True)
    result = _execute_one(candidate, test, delta, args.runtimes, args.run_dir,
                          _executable_evidence, verify)
    if result.get("input_sha256") != parent.get("input_sha256"):
        raise ValueError("diagnostic execution input differs from the parent")
    diagnostic = {
        "schema_version": "ganesh-mini-capability-matrix-single-diagnostic/v1",
        "status": "diagnostic-only",
        "candidate_id": args.candidate_id,
        "parent_report_sha256": report["report_sha256"],
        "parent_artifact_sha256": parent["artifact_sha256"],
        "diagnostic_artifact_sha256": result["artifact_sha256"],
        "parent_status": parent["status"],
        "diagnostic_status": result["status"],
        "same_input_sha256": parent["input_sha256"],
        "workers": 1,
        "admission_credit": 0,
        "evaluation_artifacts_read": 0,
    }
    diagnostic["report_sha256"] = canonical_sha256(diagnostic)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(diagnostic, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return diagnostic


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--parent-report", type=Path, required=True)
    parser.add_argument("--parent-artifacts", type=Path, required=True)
    parser.add_argument("--teacher-candidates", type=Path, required=True)
    parser.add_argument("--attached-candidates", type=Path, required=True)
    parser.add_argument("--delta-artifacts", type=Path, required=True)
    parser.add_argument("--runtimes", type=Path, default=Path("configs/eval/runtimes.json"))
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    print(json.dumps({"diagnostic_status": result["diagnostic_status"],
                      "report_sha256": result["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
