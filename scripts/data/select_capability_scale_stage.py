#!/usr/bin/env python3
"""Fail-closed selection from a sealed, terminal capability-scale stage."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sealed(value: Any, field: str, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected object")
    body = copy.deepcopy(value)
    claimed = body.pop(field, None)
    if not isinstance(claimed, str) or claimed != canonical_sha256(body):
        raise ValueError(f"{label}: invalid {field}")
    return value


def select_stage(
    rows_path: Path,
    report_path: Path,
    statuses: set[str],
    *,
    stage: str,
    rows_hash_field: str,
    row_seal_field: str = "artifact_sha256",
    id_field: str = "candidate_id",
    status_field: str = "status",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not stage or not statuses:
        raise ValueError("stage and at least one selected status are required")
    rows = read_jsonl(rows_path)
    report = sealed(json.loads(report_path.read_text(encoding="utf-8")), "report_sha256", str(report_path))
    if not rows or report.get("evaluation_artifacts_read", 0) != 0:
        raise ValueError("stage is empty or reports evaluation-artifact reads")
    if report.get(rows_hash_field) != canonical_sha256(rows):
        raise ValueError("parent report does not bind all terminal rows")
    reported_count = report.get("requested", report.get("records", report.get("terminal")))
    if reported_count is not None and reported_count != len(rows):
        raise ValueError("parent report terminal count differs from rows")

    ids: set[str] = set()
    artifact_hashes: list[str] = []
    for row in rows:
        identifier = row.get(id_field)
        if not isinstance(identifier, str) or not identifier or identifier in ids:
            raise ValueError("terminal rows contain a missing or duplicate identity")
        ids.add(identifier)
        sealed(row, row_seal_field, f"{stage}/{identifier}")
        if row.get("evaluation_artifacts_read", 0) != 0:
            raise ValueError(f"{stage}/{identifier}: evaluation-artifact read count is nonzero")
        artifact_hashes.append(row[row_seal_field])
    reported_hashes = report.get("terminal_artifact_sha256s")
    if reported_hashes is not None and reported_hashes != artifact_hashes:
        raise ValueError("parent report ordered terminal artifact hashes differ")

    if any(not isinstance(row.get(status_field), str) for row in rows):
        raise ValueError(f"terminal rows do not all contain string field {status_field}")
    selected = [row for row in rows if row.get(status_field) in statuses]
    output: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-stage-selection/v1",
        "stage": stage,
        "id_field": id_field,
        "status_field": status_field,
        "row_seal_field": row_seal_field,
        "selected_statuses": sorted(statuses),
        "parent_report_sha256": report["report_sha256"],
        "parent_terminal_rows_sha256": canonical_sha256(rows),
        "parent_terminal_ids": [row[id_field] for row in rows],
        "parent_terminal_artifact_sha256s": artifact_hashes,
        "selected": len(selected),
        "selected_ids": [row[id_field] for row in selected],
        "selected_artifact_sha256s": [row[row_seal_field] for row in selected],
        "selected_rows_sha256": canonical_sha256(selected),
        "evaluation_artifacts_read": 0,
    }
    output["report_sha256"] = canonical_sha256(output)
    return selected, output


def _atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=Path, required=True)
    parser.add_argument("--parent-report", type=Path, required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--status", action="append", required=True)
    parser.add_argument("--rows-hash-field", required=True)
    parser.add_argument("--row-seal-field", default="artifact_sha256")
    parser.add_argument("--id-field", default="candidate_id")
    parser.add_argument("--status-field", default="status")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    rows, report = select_stage(
        args.rows, args.parent_report, set(args.status), stage=args.stage,
        rows_hash_field=args.rows_hash_field, row_seal_field=args.row_seal_field,
        id_field=args.id_field, status_field=args.status_field,
    )
    _atomic(args.output, "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    _atomic(args.report, json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"selected": len(rows), "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
