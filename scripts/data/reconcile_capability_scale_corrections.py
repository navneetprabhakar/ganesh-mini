#!/usr/bin/env python3
"""Seal first-pass dispositions after the one allowed blind test reauthor.

This is a construction-stage reserve selector, not a training admission seal.
Every source matrix and correction artifact remains immutable and separately
addressable.  A corrected candidate uses its entire terminal correction
outcome; a failed correction is never silently restored to the first pass.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_capability_scale_delta_audits import _write_json_atomic, _write_jsonl_atomic
from scripts.data.run_capability_scale_final_matrix import _jsonl, _sealed


EXPECTED_MATRIX = {
    "reference.primary_discrimination": "pass",
    "reference.cross_cutting": "pass",
    "known_bad.primary_discrimination": "fail",
    "known_bad.cross_cutting": "pass",
}


def _stage(rows_path: Path, report_path: Path, hash_field: str, count: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = _jsonl(rows_path)
    report = _sealed(json.loads(report_path.read_text(encoding="utf-8")), "report_sha256", str(report_path))
    if (
        len(rows) != count or report.get("requested") != count
        or report.get(hash_field) != canonical_sha256(rows)
        or report.get("evaluation_artifacts_read") != 0
        or report.get("terminal_artifact_sha256s") != [row.get("artifact_sha256") for row in rows]
    ):
        raise ValueError(f"{rows_path}: unbound stage rows")
    for row in rows:
        _sealed(row, "artifact_sha256", str(row.get("candidate_id")))
        if row.get("evaluation_artifacts_read") != 0:
            raise ValueError("stage artifact read evaluation data")
    return rows, report


def reconcile(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    original, original_report = _stage(args.original_rows, args.original_report, "terminal_rows_sha256", 534)
    first, first_report = _stage(args.derived_rows, args.derived_report, "terminal_rows_sha256", 534)
    if (
        first_report.get("parent_report_sha256") != original_report["report_sha256"]
        or [row["candidate_id"] for row in first] != [row["candidate_id"] for row in original]
        or len({row["candidate_id"] for row in first}) != 534
    ):
        raise ValueError("derived matrix is not the complete original candidate cohort")
    original_by_id = {row["candidate_id"]: row for row in original}
    first_by_id = {row["candidate_id"]: row for row in first}

    activation = _jsonl(args.activation_rows)
    activation_report = _sealed(json.loads(args.activation_report.read_text(encoding="utf-8")),
                                "report_sha256", "correction activation")
    if (
        len(activation) != 18 or activation_report.get("activated") != 18
        or activation_report.get("activation_rows_sha256") != canonical_sha256(activation)
        or activation_report.get("matrix_report_sha256") != original_report["report_sha256"]
        or activation_report.get("maximum_correction_count") != 1
        or activation_report.get("evaluation_artifacts_read") != 0
        or len({row.get("candidate_id") for row in activation}) != 18
    ):
        raise ValueError("correction activations are not bound to the original matrix")
    for row in activation:
        _sealed(row, "activation_sha256", str(row.get("candidate_id")))
        parent = original_by_id.get(row["candidate_id"])
        current = first_by_id.get(row["candidate_id"])
        if (
            parent is None or current is None or parent.get("status") != "rejected"
            or current.get("status") != "rejected"
            or row.get("failed_matrix_artifact_sha256") != parent["artifact_sha256"]
            or row.get("cell_id") != parent.get("cell_id")
            or row.get("correction_count") != 1
        ):
            raise ValueError(f"{row.get('candidate_id')}: correction parent changed or was not rejected")
    activation_by_id = {row["candidate_id"]: row for row in activation}

    author, author_report = _stage(args.author_rows, args.author_report, "terminal_rows_sha256", 18)
    if (
        author_report.get("correction_candidate_ids") != [row["candidate_id"] for row in activation]
        or {row["candidate_id"] for row in author} != set(activation_by_id)
    ):
        raise ValueError("test reauthors do not cover the exact activated cohort")
    author_by_id = {row["candidate_id"]: row for row in author}
    for identifier, row in author_by_id.items():
        parent = first_by_id[identifier]
        if (
            row.get("correction_activation_sha256") != activation_by_id[identifier]["activation_sha256"]
            or row.get("correction_count") != 1
            or (row.get("cell_id"), row.get("lane"), row.get("task_type"))
            != (parent.get("cell_id"), parent.get("lane"), parent.get("task_type"))
        ):
            raise ValueError(f"{identifier}: reauthor candidate or activation drifted")
    valid_ids = {identifier for identifier, row in author_by_id.items() if row["status"] == "structurally-valid"}
    if len(valid_ids) != 17 or any(row["status"] not in {"structurally-valid", "structural-rejected"} for row in author):
        raise ValueError("reauthor terminal statuses differ from the sealed 17/1 cohort")

    delta, delta_report = _stage(args.delta_rows, args.delta_report, "rows_sha256", 17)
    if (
        delta_report.get("status") != "passed"
        or delta_report.get("upstream_report_binding", {}).get("test_author_parent_report_sha256") != author_report["report_sha256"]
        or delta_report.get("test_author_artifact_sha256s") != [author_by_id[row["candidate_id"]]["artifact_sha256"] for row in delta]
        or {row["candidate_id"] for row in delta} != valid_ids
        or any(row["status"] != "passed" for row in delta)
    ):
        raise ValueError("fresh blind delta does not pass the complete valid correction cohort")
    matrix, matrix_report = _stage(args.matrix_rows, args.matrix_report, "terminal_rows_sha256", 17)
    if (
        {row["candidate_id"] for row in matrix} != valid_ids
        or matrix_report.get("delta_report_sha256") != delta_report["report_sha256"]
        or any(row["status"] not in {"admitted", "rejected"} for row in matrix)
    ):
        raise ValueError("correction matrix is incomplete or upstream binding differs")
    matrix_by_id = {row["candidate_id"]: row for row in matrix}
    for identifier, row in matrix_by_id.items():
        parent = first_by_id[identifier]
        if (row.get("cell_id"), row.get("lane"), row.get("task_type")) != (
            parent.get("cell_id"), parent.get("lane"), parent.get("task_type")
        ) or (row["status"] == "admitted" and row.get("outcomes") != EXPECTED_MATRIX):
            raise ValueError(f"{identifier}: correction matrix lineage or outcomes differ")

    terminal: list[dict[str, Any]] = []
    for parent in first:
        identifier = parent["candidate_id"]
        correction = matrix_by_id.get(identifier) or author_by_id.get(identifier)
        disposition = correction or parent
        status = "admitted" if disposition["status"] == "admitted" else "rejected" if correction else parent["status"]
        if status not in {"admitted", "rejected"}:
            raise ValueError(f"{identifier}: unresolved terminal disposition")
        row = {
            "schema_version": "ganesh-mini-gate3-scale-correction-reconciliation-row/v1",
            "candidate_id": identifier, "cell_id": parent["cell_id"], "lane": parent["lane"],
            "task_type": parent["task_type"], "status": status,
            "correction_count": 1 if correction else 0,
            "source_stage": "correction-matrix" if identifier in matrix_by_id else
                            "correction-test-author" if identifier in author_by_id else "first-pass-matrix",
            "source_artifact_sha256": disposition["artifact_sha256"],
            "first_pass_artifact_sha256": parent["artifact_sha256"],
            "evaluation_artifacts_read": 0,
        }
        row["artifact_sha256"] = canonical_sha256(row)
        terminal.append(row)
    counts = dict(sorted(Counter(row["status"] for row in terminal).items()))
    report = {
        "schema_version": "ganesh-mini-gate3-scale-correction-reconciliation/v1",
        "status": "passed" if counts == {"admitted": 518, "rejected": 16} else "failed",
        "requested": 534, "counts": counts,
        "original_matrix_report_sha256": original_report["report_sha256"],
        "derived_matrix_report_sha256": first_report["report_sha256"],
        "activation_report_sha256": activation_report["report_sha256"],
        "author_report_sha256": author_report["report_sha256"],
        "delta_report_sha256": delta_report["report_sha256"],
        "correction_matrix_report_sha256": matrix_report["report_sha256"],
        "ordered_candidate_ids": [row["candidate_id"] for row in terminal],
        "terminal_artifact_sha256s": [row["artifact_sha256"] for row in terminal],
        "terminal_rows_sha256": canonical_sha256(terminal),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return terminal, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("original-rows", "original-report", "derived-rows", "derived-report",
                 "activation-rows", "activation-report", "author-rows", "author-report",
                 "delta-rows", "delta-report", "matrix-rows", "matrix-report",
                 "output-rows", "output-report"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    rows, report = reconcile(args)
    if args.output_rows.exists() or args.output_report.exists():
        raise ValueError("reconciliation outputs already exist")
    _write_jsonl_atomic(args.output_rows, rows)
    _write_json_atomic(args.output_report, report)
    print(json.dumps({"status": report["status"], "counts": report["counts"],
                      "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
