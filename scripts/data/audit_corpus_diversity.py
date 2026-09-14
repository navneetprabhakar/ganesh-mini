#!/usr/bin/env python3
"""Audit observable task diversity without reading any evaluation surface."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
TASK_TYPES = ("generation", "repair")
TAG_PATTERNS = {
    "aliasing_or_mutation": r"\b(alias|aliasing|mutat(?:e|ion)|in[- ]place|copy of|must not modify)\b",
    "boundary_or_overflow": r"\b(boundar(?:y|ies)|overflow|underflow|clamp|minimum|maximum|out of range)\b",
    "callbacks_or_events": r"\b(callback|event|listener|handler|emit|subscription)\b",
    "concurrency_or_atomicity": r"\b(concurren|thread[- ]safe|atomic|race|lock|mutex|semaphore)\b",
    "dedup_or_grouping": r"\b(deduplicat|duplicate|distinct|unique|group(?:ed|ing)?|bucket)\b",
    "errors_or_malformed": r"\b(error|exception|invalid|malformed|reject|failure)\b",
    "graph_or_tree": r"\b(graph|tree|node|edge|ancestor|descendant|path|cycle)\b",
    "numeric_aggregation": r"\b(sum|total|average|mean|median|count|prefix|accumulat|aggregate)\b",
    "ordering_or_sorting": r"\b(sort(?:ed|ing)?|order(?:ed|ing)?|stable|lexicograph|priority|rank)\b",
    "parsing_or_encoding": r"\b(parse|parser|decode|encode|escape|tokeni[sz]|format|delimiter|seriali[sz])\b",
    "sequence_transform": r"\b(sequence|subsequence|slice|window|run|segment|rotate|reverse|partition)\b",
    "stateful_workflow": r"\b(state|workflow|catalog|registry|session|transaction|queue|stack|cache)\b",
    "string_or_unicode": r"\b(string|text|character|unicode|rune|whitespace|case[- ]insensitive)\b",
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def message(row: dict[str, Any], role: str) -> str:
    values = [item.get("content", "") for item in row.get("messages", []) if item.get("role") == role]
    if len(values) != 1 or not isinstance(values[0], str):
        raise ValueError(f"{row.get('id')}: expected exactly one {role} message")
    return values[0]


def prompt_tags(prompt: str) -> list[str]:
    lowered = prompt.lower()
    return [name for name, pattern in TAG_PATTERNS.items() if re.search(pattern, lowered)]


def scaffold_fingerprint(prompt: str) -> str:
    value = re.sub(r"```.*?```", " <code> ", prompt, flags=re.DOTALL)
    value = re.sub(r"`[^`]+`", " <symbol> ", value)
    value = re.sub(r'"(?:\\.|[^"\\])*"', " <literal> ", value)
    value = re.sub(r"\b\d+(?:\.\d+)?\b", " <number> ", value)
    value = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\b", lambda match: match.group(0).lower(), value)
    value = re.sub(r"\s+", " ", value).strip()
    return hashlib.sha256(value.encode()).hexdigest()


def percentile(values: Iterable[int], fraction: float) -> int:
    ordered = sorted(values)
    if not ordered:
        return 0
    return ordered[round((len(ordered) - 1) * fraction)]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    lane_counts = Counter(row["lane"] for row in rows)
    type_counts = Counter(row["task_type"] for row in rows)
    joint_counts = Counter(f"{row['lane']}/{row['task_type']}" for row in rows)
    tags = {row["id"]: prompt_tags(message(row, "user")) for row in rows}
    tag_counts = Counter(tag for values in tags.values() for tag in values)
    tag_lanes = {
        tag: dict(sorted(Counter(row["lane"] for row in rows if tag in tags[row["id"]]).items()))
        for tag in TAG_PATTERNS
    }
    prompts = [message(row, "user") for row in rows]
    responses = [message(row, "assistant") for row in rows]
    scaffolds = Counter(scaffold_fingerprint(prompt) for prompt in prompts)
    source_records = [row.get("source", {}).get("record_id") for row in rows]
    return {
        "records": len(rows),
        "records_by_lane": dict(sorted(lane_counts.items())),
        "records_by_task_type": dict(sorted(type_counts.items())),
        "records_by_lane_and_task_type": dict(sorted(joint_counts.items())),
        "unique_source_records": len(set(source_records)),
        "missing_source_record_ids": sum(value is None for value in source_records),
        "prompt_characters": {
            "median": percentile(map(len, prompts), 0.5),
            "p90": percentile(map(len, prompts), 0.9),
            "maximum": max(map(len, prompts), default=0),
        },
        "response_characters": {
            "median": percentile(map(len, responses), 0.5),
            "p90": percentile(map(len, responses), 0.9),
            "maximum": max(map(len, responses), default=0),
        },
        "observable_contract_tags": {
            "counts": dict(sorted(tag_counts.items())),
            "counts_by_lane": tag_lanes,
            "untagged_records": sum(not values for values in tags.values()),
        },
        "normalized_scaffolds": {
            "unique": len(scaffolds),
            "unique_ratio": len(scaffolds) / len(rows) if rows else 0.0,
            "largest_cluster": max(scaffolds.values(), default=0),
            "clusters_with_multiple_records": sum(count > 1 for count in scaffolds.values()),
        },
    }


def build(corpus_path: Path, selected_path: Path) -> dict[str, Any]:
    corpus = read_jsonl(corpus_path)
    selected_prepared = read_jsonl(selected_path)
    ids = [row.get("id") for row in corpus]
    selected_ids = [row.get("source_id") for row in selected_prepared]
    if len(ids) != len(set(ids)):
        raise ValueError("corpus IDs are not unique")
    by_id = {row["id"]: row for row in corpus}
    missing = sorted(set(selected_ids) - set(by_id))
    if missing:
        raise ValueError(f"selected IDs missing from corpus: {missing[:3]}")
    selected = [by_id[value] for value in selected_ids]
    for row in corpus:
        if row.get("lane") not in LANES or row.get("task_type") not in TASK_TYPES:
            raise ValueError(f"{row.get('id')}: unsupported lane or task type")
    corpus_summary = summarize(corpus)
    selected_summary = summarize(selected)
    full_tags = corpus_summary["observable_contract_tags"]["counts"]
    selected_tags = selected_summary["observable_contract_tags"]["counts"]
    representation = {
        tag: {
            "corpus": full_tags.get(tag, 0),
            "selected": selected_tags.get(tag, 0),
            "selected_share": selected_tags.get(tag, 0) / full_tags[tag] if full_tags.get(tag) else None,
        }
        for tag in TAG_PATTERNS
    }
    report = {
        "schema_version": "ganesh-mini-training-corpus-diversity-audit/v1",
        "status": "complete-non-evaluation-audit",
        "scope": {
            "evaluation_surfaces_read": 0,
            "corpus_path": str(corpus_path),
            "corpus_file_sha256": hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
            "selected_path": str(selected_path),
            "selected_file_sha256": hashlib.sha256(selected_path.read_bytes()).hexdigest(),
        },
        "corpus": corpus_summary,
        "selected_probe": selected_summary,
        "tag_representation": representation,
    }
    report["report_sha256"] = hashlib.sha256(canonical_bytes(report)).hexdigest()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--selected", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = build(args.corpus, args.selected)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
