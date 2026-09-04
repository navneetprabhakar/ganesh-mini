#!/usr/bin/env python3
"""Build the deterministic, stratified expansion-v1 manual-review sample."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from scripts.data.admit_expansion import canonical_json


SCHEMA_VERSION = "ganesh-mini-expansion-quality-sample/v1"
CRITERIA = (
    "prompt_clarity",
    "api_consistency",
    "test_independence",
    "non_triviality",
    "idiomatic_code",
    "dependency_isolation",
    "realistic_known_bad_failure",
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").split("\n") if line.strip()]


def correction_history(row: dict[str, Any]) -> str:
    transformation = row.get("lineage", {}).get("transformation", "")
    if not isinstance(transformation, str):
        raise ValueError(f"record {row.get('id')}: invalid lineage transformation")
    return "corrected" if "corrected against independent tests" in transformation else "first_pass"


def stratum(row: dict[str, Any]) -> tuple[str, str, str, str]:
    try:
        return row["lane"], row["lineage"]["dataset"], row["task_type"], correction_history(row)
    except (KeyError, TypeError) as exc:
        raise ValueError(f"record {row.get('id')}: missing sampling stratum") from exc


def allocate(populations: dict[tuple[str, str, str, str], int], sample_size: int) -> dict[tuple[str, str, str, str], int]:
    if sample_size <= 0 or sample_size > sum(populations.values()):
        raise ValueError("sample size must be positive and no larger than the population")
    keys = sorted(populations)
    if sample_size < len(keys):
        raise ValueError("sample is too small to cover every non-empty stratum")
    total = sum(populations.values())
    allocated = {key: 1 for key in keys}
    remaining = sample_size - len(keys)
    while remaining:
        eligible = [key for key in keys if allocated[key] < populations[key]]
        if not eligible:
            raise ValueError("unable to allocate the requested sample")
        key = max(
            eligible,
            key=lambda item: (
                populations[item] * sample_size / total - allocated[item],
                populations[item] - allocated[item],
                tuple(reversed(item)),
            ),
        )
        allocated[key] += 1
        remaining -= 1
    return allocated


def build_sample(
    rows: list[dict[str, Any]], corpus_sha256: str, sample_size: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    identifiers = [row.get("id") for row in rows]
    if any(not isinstance(identifier, str) or not identifier for identifier in identifiers):
        raise ValueError("every corpus record must have a non-empty string ID")
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("corpus record IDs are not unique")
    grouped: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[stratum(row)].append(row)
    populations = {key: len(value) for key, value in grouped.items()}
    allocation = allocate(populations, sample_size)
    selected: list[dict[str, Any]] = []
    strata_report: list[dict[str, Any]] = []
    for key in sorted(grouped):
        ranked = sorted(
            grouped[key],
            key=lambda row: (sha256_bytes(f"{corpus_sha256}\0{row['id']}".encode()), row["id"]),
        )
        chosen = ranked[:allocation[key]]
        selected.extend(chosen)
        lane, source, task_type, history = key
        strata_report.append({
            "lane": lane, "source": source, "task_type": task_type,
            "rejection_history": history, "population": len(ranked), "selected": len(chosen),
        })
    selected.sort(key=lambda row: (stratum(row), row["id"]))
    report = {
        "schema_version": SCHEMA_VERSION,
        "corpus_sha256": corpus_sha256,
        "population": len(rows),
        "sample_size": len(selected),
        "selection": "minimum SHA-256 of corpus SHA-256, NUL, and record ID within proportionally allocated strata",
        "stratification": ["lane", "source", "task_type", "rejection_history"],
        "criteria": list(CRITERIA),
        "strata": strata_report,
        "records": [{
            "id": row["id"], "lane": row["lane"], "source": row["lineage"]["dataset"],
            "task_type": row["task_type"], "rejection_history": correction_history(row),
            "review": {criterion: None for criterion in CRITERIA}, "notes": None,
        } for row in selected],
        "systematic_defects": [],
        "status": "pending-manual-review",
    }
    return selected, report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=6000)
    parser.add_argument("--sample-size", type=int, default=300)
    args = parser.parse_args()

    payload = args.input.read_bytes()
    corpus_sha = sha256_bytes(payload)
    rows = read_jsonl(args.input)
    state = json.loads(args.state.read_text(encoding="utf-8"))
    if state.get("status") != "complete":
        raise ValueError("production state is not complete")
    if corpus_sha != state.get("corpus_sha256"):
        raise ValueError("corpus SHA-256 differs from production state")
    if len(rows) != args.expected_count:
        raise ValueError(f"expected {args.expected_count} corpus rows, found {len(rows)}")
    actual = Counter((row["lane"], row["task_type"]) for row in rows)
    expected = {(lane, task): count for lane, tasks in state["targets"].items() for task, count in tasks.items()}
    if dict(actual) != expected or state.get("counts") != state.get("targets"):
        raise ValueError("corpus does not match frozen lane/task quotas")

    selected, report = build_sample(rows, corpus_sha, args.sample_size)
    sample_payload = b"".join(canonical_json(row) + b"\n" for row in selected)
    report["sample_sha256"] = sha256_bytes(sample_payload)
    report_without_seal = canonical_json(report)
    report["report_sha256"] = sha256_bytes(report_without_seal)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(sample_payload)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
