#!/usr/bin/env python3
"""Create a sealed inventory for a pinned McEval-Instruct source snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TARGETS = {"go", "java", "javascript", "typescript", "python", "rust"}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def audit(path: Path, revision: str) -> dict[str, Any]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("source payload must be a JSON array")
    counts: Counter[str] = Counter()
    missing = Counter()
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"instruction", "output", "language", "source"}:
            raise ValueError(f"row {index}: unexpected schema")
        if not all(isinstance(row[key], str) and row[key] for key in row):
            raise ValueError(f"row {index}: empty or non-string field")
        lane = row["language"].casefold()
        counts[lane] += 1
        if lane in TARGETS:
            missing["target_without_tests"] += 1
    report = {
        "schema_version": "ganesh-mini-expansion-source-inventory/v1",
        "source": "Multilingual-Multimodal-NLP/McEval-Instruct",
        "revision": revision,
        "source_file": path.name,
        "source_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "total_records": len(rows),
        "counts_by_language": dict(sorted(counts.items())),
        "target_language_records": {lane: counts[lane] for lane in sorted(TARGETS)},
        "target_records_with_independent_behavioral_tests": 0,
        "admission_status": "candidate-queue-only",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.input, args.revision)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["admission_status"], "target_records": report["target_language_records"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
