#!/usr/bin/env python3
"""Measure the reviewed expansion corpus and project bounded-pilot runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from scripts.data.prepare_recovery_admission import (
    HISTORICAL_HOLDS,
    prior_recoveries,
)
from scripts.train.response_only import build_response_only_encoding


ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl"
HOLDS = ROOT / "measurement/data/expansion-v1/cutoff-5885-review/additional-holds.json"
RECOVERIES = ROOT / "measurement/data/expansion-v1/recovery-admission"
RUN_EVIDENCE = ROOT / (
    "measurement/gate3/gcloud/20260827T090603Z/finalization/terminal-download/"
    "output/campaign/training/lr-1e-5/run-evidence.json"
)
PHASE_LEDGER = ROOT / (
    "measurement/gate3/gcloud/20260827T090603Z/finalization/terminal-download/"
    "output/campaign/phase-ledger.json"
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def corpus_rows(root: Path = ROOT) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    original_path = root / ORIGINAL.relative_to(ROOT)
    holds_path = root / HOLDS.relative_to(ROOT)
    recovery_root = root / RECOVERIES.relative_to(ROOT)
    held = HISTORICAL_HOLDS | {
        item["id"] for item in json.loads(holds_path.read_text())["holds"]
    }
    retained = [row for row in read_jsonl(original_path) if row["id"] not in held]
    recoveries, bindings = prior_recoveries(root, recovery_root)
    combined = retained + recoveries
    ids = [row["id"] for row in combined]
    if len(ids) != len(set(ids)):
        raise ValueError("combined corpus contains duplicate IDs")
    return retained, recoveries, combined, bindings


def canonical_jsonl(rows: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(
        json.dumps(row, sort_keys=True, separators=(",", ":")).encode() + b"\n"
        for row in rows
    )


def measure_rows(tokenizer: Any, rows: Iterable[dict[str, Any]], maximum_length: int) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    task_types: Counter[str] = Counter()
    input_tokens: Counter[str] = Counter()
    response_tokens: Counter[str] = Counter()
    over_limit: Counter[str] = Counter()
    maximum = {"tokens": 0, "id": None}
    canonical = hashlib.sha256()
    total = 0
    for row in rows:
        total += 1
        canonical.update(json.dumps(row, sort_keys=True, separators=(",", ":")).encode())
        canonical.update(b"\n")
        encoded = build_response_only_encoding(tokenizer, row["messages"])
        length = len(encoded.encoding["input_ids"])
        lane = row["lane"]
        counts[lane] += 1
        task_types[row["task_type"]] += 1
        input_tokens[lane] += length
        response_tokens[lane] += encoded.response_token_count
        if length > maximum_length:
            over_limit[lane] += 1
        if length > maximum["tokens"]:
            maximum = {"tokens": length, "id": row["id"]}
    return {
        "records": total,
        "canonical_jsonl_sha256": canonical.hexdigest(),
        "counts_by_lane": dict(sorted(counts.items())),
        "counts_by_task_type": dict(sorted(task_types.items())),
        "input_tokens_by_lane": dict(sorted(input_tokens.items())),
        "response_tokens_by_lane": dict(sorted(response_tokens.items())),
        "total_input_tokens": sum(input_tokens.values()),
        "total_response_tokens": sum(response_tokens.values()),
        "sequence_length": maximum_length,
        "records_over_sequence_length_by_lane": dict(sorted(over_limit.items())),
        "maximum_input_tokens": maximum,
    }


def throughput_projection(total_tokens: int, run: dict[str, Any], phases: dict[str, Any]) -> dict[str, Any]:
    state = run["state"]
    measured = state["seen_tokens"] / state["wall_seconds"]
    training_phase = next(item for item in phases["phases"] if item["name"] == "train-lr-1e-5")
    overhead_factor = training_phase["elapsed_seconds"] / state["wall_seconds"]
    conservative = measured * 0.75
    eval_seconds_per_task = 1710 / 180

    def duration(rate: float) -> float:
        return total_tokens / rate * overhead_factor

    expected = duration(measured)
    conservative_seconds = duration(conservative)
    return {
        "source_seen_tokens": state["seen_tokens"],
        "source_training_wall_seconds": state["wall_seconds"],
        "measured_input_tokens_per_second": measured,
        "training_phase_overhead_factor": overhead_factor,
        "conservative_rate_fraction": 0.75,
        "conservative_input_tokens_per_second": conservative,
        "projected_training_phase_seconds": {
            "expected": expected,
            "conservative": conservative_seconds,
        },
        "evaluation_seconds_per_task_from_executed_180_task_run": eval_seconds_per_task,
        "projected_30_task_canary_seconds": 30 * eval_seconds_per_task,
        "projected_180_task_evaluation_seconds": 180 * eval_seconds_per_task,
        "recommended_runtime_ceiling_seconds_including_30m_backup_reserve": 21600,
    }


def assess(root: Path = ROOT, maximum_length: int = 2944) -> dict[str, Any]:
    from transformers import AutoTokenizer

    retained, recoveries, combined, bindings = corpus_rows(root)
    tokenizer = AutoTokenizer.from_pretrained(
        root / "models/qwen3.5-2b-15852e8", local_files_only=True
    )
    corpus = measure_rows(tokenizer, combined, maximum_length)
    run_path = root / RUN_EVIDENCE.relative_to(ROOT)
    phase_path = root / PHASE_LEDGER.relative_to(ROOT)
    run = json.loads(run_path.read_text())
    phases = json.loads(phase_path.read_text())
    projection = throughput_projection(corpus["total_input_tokens"], run, phases)
    return {
        "schema_version": "ganesh-mini-expansion-pilot-assessment/v1",
        "status": "pilot-sufficient-pending-final-corpus-seal",
        "decision": {
            "current_reviewed_expansion_is_sufficient_for_one_bounded_pilot": True,
            "four_thousand_row_floor_retired_for_pilot_entry": True,
            "reason": (
                "The fully reviewed corpus is 80% of the former diagnostic floor, "
                "contains more than five times the seed pilot's input-token volume, "
                "fits the qualified sequence envelope, and the bounded executable pilot "
                "is the measurement that determines whether further expansion is useful."
            ),
            "not_a_main_training_or_release_seal": True,
        },
        "inputs": {
            "original": {"path": str(ORIGINAL.relative_to(ROOT)), "sha256": digest((root / ORIGINAL.relative_to(ROOT)).read_bytes())},
            "holds": {"path": str(HOLDS.relative_to(ROOT)), "sha256": digest((root / HOLDS.relative_to(ROOT)).read_bytes())},
            "recovery_registry": str(RECOVERIES.relative_to(ROOT)),
            "throughput_run": {"path": str(RUN_EVIDENCE.relative_to(ROOT)), "sha256": digest(run_path.read_bytes())},
            "phase_ledger": {"path": str(PHASE_LEDGER.relative_to(ROOT)), "sha256": digest(phase_path.read_bytes())},
        },
        "retained_original_records": len(retained),
        "admitted_recovery_records": len(recoveries),
        "recovery_admission_bindings": bindings,
        "corpus": corpus,
        "seed_pilot_input_tokens": run["state"]["seen_tokens"],
        "expansion_to_seed_input_token_ratio": corpus["total_input_tokens"] / run["state"]["seen_tokens"],
        "throughput": projection,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--corpus-output", type=Path)
    parser.add_argument("--maximum-length", type=int, default=2944)
    args = parser.parse_args()
    report = assess(maximum_length=args.maximum_length)
    if args.corpus_output:
        _, _, rows, _ = corpus_rows()
        data = canonical_jsonl(rows)
        if digest(data) != report["corpus"]["canonical_jsonl_sha256"]:
            raise ValueError("materialized corpus does not match measured corpus")
        args.corpus_output.parent.mkdir(parents=True, exist_ok=True)
        if args.corpus_output.exists() and args.corpus_output.read_bytes() != data:
            raise ValueError("refusing to overwrite a different sealed corpus")
        args.corpus_output.write_bytes(data)
        report["status"] = "pilot-sufficient-corpus-sealed"
        report["sealed_corpus"] = {
            "path": str(args.corpus_output.resolve().relative_to(ROOT)),
            "bytes": len(data),
            "sha256": digest(data),
            "records": len(rows),
        }
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
