#!/usr/bin/env python3
"""Seal one blind test-reauthor correction for executable reference failures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def activate(matrix_artifacts: Path, matrix_report: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = _jsonl(matrix_artifacts)
    report = _sealed(matrix_report, "report_sha256")
    if (
        report.get("terminal_rows_sha256") != canonical_sha256(rows)
        or report.get("requested") != len(rows)
        or report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("matrix report does not bind terminal artifacts")
    activated: list[dict[str, Any]] = []
    for row in rows:
        if row.get("status") != "rejected":
            continue
        body = dict(row); claimed = body.pop("artifact_sha256", None)
        outcomes = row.get("outcomes", {})
        if (
            claimed != canonical_sha256(body)
            or outcomes.get("reference.primary_discrimination") == "pass"
            and outcomes.get("reference.cross_cutting") == "pass"
        ):
            continue
        activation: dict[str, Any] = {
            "schema_version": "ganesh-mini-capability-scale-test-reauthor-activation/v1",
            "candidate_id": row["candidate_id"],
            "cell_id": row["cell_id"],
            "failed_matrix_artifact_sha256": row["artifact_sha256"],
            "correction_count": 1,
            "author_visibility": {
                "specification_and_controller_bindings_only": True,
                "prior_tests_visible": False,
                "verifier_outputs_visible": False,
                "reference_visible": False,
                "evaluation_artifacts_read": 0,
            },
        }
        activation["activation_sha256"] = canonical_sha256(activation)
        activated.append(activation)
    result: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-test-reauthor-activation-report/v1",
        "status": "activated" if activated else "no-eligible-rejections",
        "matrix_report_sha256": report["report_sha256"],
        "activated": len(activated),
        "activation_rows_sha256": canonical_sha256(activated),
        "maximum_correction_count": 1,
        "evaluation_artifacts_read": 0,
    }
    result["report_sha256"] = canonical_sha256(result)
    return activated, result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix-artifacts", type=Path, required=True)
    parser.add_argument("--matrix-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--candidates", type=Path)
    parser.add_argument("--selected-candidates", type=Path)
    args = parser.parse_args()
    rows, report = activate(args.matrix_artifacts, args.matrix_report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.candidates is not None or args.selected_candidates is not None:
        if args.candidates is None or args.selected_candidates is None:
            raise ValueError("candidates and selected-candidates must be supplied together")
        candidates = _jsonl(args.candidates)
        wanted = {row["candidate_id"] for row in rows}
        selected = [row for row in candidates if row.get("id") in wanted]
        if len(selected) != len(wanted):
            raise ValueError("correction candidates differ from activation")
        args.selected_candidates.parent.mkdir(parents=True, exist_ok=True)
        args.selected_candidates.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in selected), encoding="utf-8",
        )
    print(json.dumps({"status": report["status"], "activated": report["activated"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "activated" else 2


if __name__ == "__main__":
    raise SystemExit(main())
