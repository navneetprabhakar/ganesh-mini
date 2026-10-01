#!/usr/bin/env python3
"""Materialize the exact passing subset of a sealed scale delta cohort."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--test-artifacts", type=Path, required=True)
    parser.add_argument("--attached-candidates", type=Path, required=True)
    parser.add_argument("--delta-artifacts", type=Path, required=True)
    parser.add_argument("--delta-report", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    candidates, tests, attached, deltas = map(
        _rows, (args.candidates, args.test_artifacts, args.attached_candidates, args.delta_artifacts),
    )
    report = json.loads(args.delta_report.read_text(encoding="utf-8"))
    body = dict(report); claimed = body.pop("report_sha256", None)
    if claimed != canonical_sha256(body) or report.get("rows_sha256") != canonical_sha256(deltas):
        raise ValueError("delta report or rows are unsealed")
    passed = {row["candidate_id"] for row in deltas if row.get("status") == "passed"}
    indexed = [
        {row.get("candidate_id", row.get("id")): row for row in values}
        for values in (candidates, tests, attached, deltas)
    ]
    if any(not passed <= set(values) for values in indexed):
        raise ValueError("passing delta subset is absent from an upstream input")
    ordered = [row["id"] for row in candidates if row["id"] in passed]
    outputs = (
        ("candidates.jsonl", indexed[0]), ("test-artifacts.jsonl", indexed[1]),
        ("attached-candidates.jsonl", indexed[2]), ("delta-artifacts.jsonl", indexed[3]),
    )
    for name, values in outputs:
        _atomic(args.output_dir / name, [values[identifier] for identifier in ordered])
    selection: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-delta-pass-selection/v1",
        "delta_report_sha256": report["report_sha256"],
        "selected_candidate_ids": ordered,
        "selected": len(ordered),
        "evaluation_artifacts_read": 0,
    }
    selection["report_sha256"] = canonical_sha256(selection)
    temporary = args.output_dir / "selection-report.json.tmp"
    temporary.write_text(json.dumps(selection, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(args.output_dir / "selection-report.json")
    print(json.dumps({"selected": len(ordered), "report_sha256": selection["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
