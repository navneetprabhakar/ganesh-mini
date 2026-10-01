#!/usr/bin/env python3
"""Freeze the entire Go slice for uniform single-worker matrix requalification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_capability_scale_delta_audits import _write_json_atomic, _write_jsonl_atomic
from scripts.data.run_capability_scale_final_matrix import _jsonl, _sealed


def load_bound_rows(path: Path, report_path: Path, rows_field: str, count: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = _jsonl(path)
    report = _sealed(json.loads(report_path.read_text(encoding="utf-8")),
                     "report_sha256", str(report_path))
    if (
        len(rows) != count
        or report.get("requested") != count
        or report.get(rows_field) != canonical_sha256(rows)
        or report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError(f"{path}: rows differ from their sealed report")
    return rows, report


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    teachers, teacher_report = load_bound_rows(
        args.teacher_candidates, args.teacher_report, "candidates_sha256", 534,
    )
    tests, test_report = load_bound_rows(
        args.test_artifacts, args.test_report, "terminal_rows_sha256", 534,
    )
    deltas, delta_report = load_bound_rows(
        args.delta_artifacts, args.delta_report, "rows_sha256", 534,
    )
    attached = _jsonl(args.attached_candidates)
    parent, matrix_report = load_bound_rows(
        args.matrix_artifacts, args.matrix_report, "terminal_rows_sha256", 534,
    )
    ids = [row.get("id") for row in teachers]
    if (
        teacher_report.get("status") != "passed"
        or test_report.get("status") != "passed"
        or delta_report.get("status") != "passed"
        or matrix_report.get("status") != "failed"
        or len(set(ids)) != 534
        or [row.get("candidate_id") for row in tests] != ids
        or [row.get("candidate_id") for row in deltas] != ids
        or [row.get("candidate_id") for row in parent] != ids
        or [row.get("id") for row in attached] != ids
        or delta_report.get("attached_candidates_sha256") != canonical_sha256(attached)
        or matrix_report.get("terminal_artifact_sha256s")
        != [row.get("artifact_sha256") for row in parent]
    ):
        raise ValueError("first-pass cohorts or reports are not one-to-one and sealed")
    for row in tests + deltas + parent:
        _sealed(row, "artifact_sha256", str(row.get("candidate_id")))
        if row.get("evaluation_artifacts_read") != 0:
            raise ValueError("evaluation-artifact read in upstream cohort")
    selected = [index for index, row in enumerate(teachers) if row.get("lane") == "go"]
    if len(selected) != 89 or any(
        attached[index].get("lane") != "go" or parent[index].get("lane") != "go"
        for index in selected
    ):
        raise ValueError("Go cohort is not the frozen 89-candidate slice")
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    subsets = {
        "teacher-candidates.jsonl": [teachers[index] for index in selected],
        "test-artifacts.jsonl": [tests[index] for index in selected],
        "delta-artifacts.jsonl": [deltas[index] for index in selected],
        "attached-candidates.jsonl": [attached[index] for index in selected],
    }
    for filename, rows in subsets.items():
        _write_jsonl_atomic(output / filename, rows)
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-go-single-worker-cohort/v1",
        "status": "ready",
        "selected": 89,
        "ordered_candidate_ids": [ids[index] for index in selected],
        "original_input_sha256s": [parent[index]["input_sha256"] for index in selected],
        "original_artifact_sha256s": [parent[index]["artifact_sha256"] for index in selected],
        "original_statuses": [parent[index]["status"] for index in selected],
        "parent_report_sha256s": {
            "teacher": teacher_report["report_sha256"],
            "test_author": test_report["report_sha256"],
            "delta": delta_report["report_sha256"],
            "matrix": matrix_report["report_sha256"],
        },
        "subset_sha256s": {filename: canonical_sha256(rows) for filename, rows in subsets.items()},
        "workers": 1,
        "candidate_or_runtime_mutation": False,
        "evaluation_artifacts_read": 0,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    _write_json_atomic(output / "manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teacher-candidates", type=Path, required=True)
    parser.add_argument("--teacher-report", type=Path, required=True)
    parser.add_argument("--test-artifacts", type=Path, required=True)
    parser.add_argument("--test-report", type=Path, required=True)
    parser.add_argument("--delta-artifacts", type=Path, required=True)
    parser.add_argument("--delta-report", type=Path, required=True)
    parser.add_argument("--attached-candidates", type=Path, required=True)
    parser.add_argument("--matrix-artifacts", type=Path, required=True)
    parser.add_argument("--matrix-report", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    manifest = prepare(args)
    print(json.dumps({"selected": manifest["selected"],
                      "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
