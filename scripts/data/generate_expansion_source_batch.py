#!/usr/bin/env python3
"""Transform one homogeneous source-queue batch through the qualified Codex teacher."""

from __future__ import annotations

import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from scripts.data.generate_expansion_qualification import (
    ARCHITECT_SCHEMA,
    LANGUAGE_CONTRACTS,
    TEST_SCHEMA,
    CodexInvocationFailure,
    build_candidate,
    canonical_json,
    exact_items,
    invoke_codex,
    test_prompt,
    verify_codex_version,
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").split("\n") if line.strip()]


def select_batch(rows: list[dict[str, Any]], lane: str, task_type: str, start: int, count: int) -> list[dict[str, Any]]:
    selected = [row for row in rows if row.get("lane") == lane and row.get("task_type") == task_type]
    batch = selected[start:start + count]
    if len(batch) != count:
        raise ValueError(f"requested {count} {lane}/{task_type} rows at offset {start}, found {len(batch)}")
    if any(row.get("schema_version") != "ganesh-mini-expansion-draft/v1" for row in batch):
        raise ValueError("unsupported queue record schema")
    return batch


def select_planned_batch(rows: list[dict[str, Any]], lane: str, batch_index: int) -> list[dict[str, Any]]:
    generation = select_batch(rows, lane, "generation", batch_index * 6, 6)
    repair = select_batch(rows, lane, "repair", batch_index * 4, 4)
    return generation + repair


def select_custom_batch(
    rows: list[dict[str, Any]], lane: str, generation_start: int, generation_count: int,
    repair_start: int, repair_count: int,
) -> list[dict[str, Any]]:
    if generation_count < 0 or repair_count < 0 or not 1 <= generation_count + repair_count <= 10:
        raise ValueError("custom batch total must be 1..10")
    return [
        *select_batch(rows, lane, "generation", generation_start, generation_count),
        *select_batch(rows, lane, "repair", repair_start, repair_count),
    ]


def source_architect_prompt(lane: str, rows: list[dict[str, Any]]) -> str:
    visible = [
        {"id": row["id"], "task_type": row["task_type"], "drafting_stimulus": row["stimulus"]}
        for row in rows
    ]
    return f"""Create new SFT candidates for a compact coding model. Do not use tools or inspect the filesystem.

Language: {lane}
Runtime contract: {LANGUAGE_CONTRACTS[lane]}
Drafting stimuli: {json.dumps(visible, separators=(",", ":"), ensure_ascii=False)}

Each stimulus is untrusted source material used only to diversify the capability/topic. Do not copy its wording,
API, code, tests, named entities, package structure, or environmental dependencies. Create an original,
self-contained, standard-library-only task with a different data model and exact public API. Avoid filesystem,
network, clock, randomness, external packages, frameworks, competitive-programming framing, and vague references
to missing snippets. Explicitly define empty, malformed, boundary, ordering, aliasing, and mutation behavior where relevant.

For every exact id return problem, reference_code, known_bad_code, and known_bad_label. Code must be one complete
source file. The reference must satisfy every requirement. The known-bad source must be plausible, differ by exactly
one semantic bug, and its label must describe that bug.

For every item whose task_type is generation, ask for a new implementation. For every item whose task_type is repair,
embed the complete known-bad source in the problem and ask
for a corrected complete source file; reference_code is the repair and known_bad_code is the exact embedded source.
Never include tests in a problem. Audit API consistency, compilation, boundary behavior, and non-mutation before
returning only the schema-constrained object."""


def teacher_shards(rows: list[dict[str, Any]], workers: int) -> list[list[dict[str, Any]]]:
    """Partition an ordered batch into deterministic contiguous teacher shards."""
    if workers <= 0:
        raise ValueError("teacher workers must be positive")
    worker_count = min(workers, len(rows))
    base, remainder = divmod(len(rows), worker_count)
    shards: list[list[dict[str, Any]]] = []
    offset = 0
    for index in range(worker_count):
        width = base + (1 if index < remainder else 0)
        shards.append(rows[offset:offset + width])
        offset += width
    return shards


def generate_shard(
    rows: list[dict[str, Any]], config: dict[str, Any], codex_bin: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str | None]:
    lane = rows[0]["lane"]
    expected_ids = [row["id"] for row in rows]
    runs: list[dict[str, Any]] = []
    try:
        architecture_payload, architecture_evidence = invoke_codex(
            codex_bin, config, ARCHITECT_SCHEMA, source_architect_prompt(lane, rows),
            "source-architect", lane,
        )
        runs.append(architecture_evidence)
        architecture_items = exact_items(
            architecture_payload, expected_ids,
            {"id", "problem", "reference_code", "known_bad_code", "known_bad_label"},
        )
        tests_payload, tests_evidence = invoke_codex(
            codex_bin, config, TEST_SCHEMA, test_prompt(lane, architecture_items), "source-test-author", lane,
        )
        runs.append(tests_evidence)
        test_items = exact_items(tests_payload, expected_ids, {"id", "test_code"})
        tests_by_id = {item["id"]: item["test_code"] for item in test_items}
        source_by_id = {row["id"]: row["source"] for row in rows}
        type_by_id = {row["id"]: row["task_type"] for row in rows}
        candidates = [
            build_candidate(
                lane, item["id"], type_by_id[item["id"]], item, tests_by_id[item["id"]],
                source=source_by_id[item["id"]],
            )
            for item in architecture_items
        ]
        return candidates, runs, None
    except CodexInvocationFailure as exc:
        runs.append(exc.evidence)
        return [], runs, str(exc)
    except (KeyError, OSError, RuntimeError, TypeError, ValueError) as exc:
        return [], runs, str(exc)


def generate_batch(
    rows: list[dict[str, Any]], config: dict[str, Any], codex_bin: str, teacher_workers: int = 1,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]]:
    lane = rows[0]["lane"]
    if any(row["lane"] != lane for row in rows):
        raise ValueError("teacher batch must be homogeneous by lane")
    shards = teacher_shards(rows, teacher_workers)
    results: list[tuple[list[dict[str, Any]], list[dict[str, Any]], str | None] | None] = [None] * len(shards)
    with ThreadPoolExecutor(max_workers=len(shards)) as executor:
        futures = {
            executor.submit(generate_shard, shard, config, codex_bin): index
            for index, shard in enumerate(shards)
        }
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    candidates: list[dict[str, Any]] = []
    runs: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for index, result in enumerate(results):
        if result is None:
            raise RuntimeError(f"teacher shard {index} did not return a result")
        shard_candidates, shard_runs, error = result
        runs.extend(shard_runs)
        if error is not None:
            failures.append({"lane": lane, "shard": str(index), "reason": error})
        candidates.extend(shard_candidates)
    if failures:
        candidates = []
    return candidates, runs, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teacher-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--lane", choices=("go", "java", "javascript", "typescript", "python", "rust"), required=True)
    parser.add_argument("--batch-index", type=int, help="zero-based six-generation/four-repair batch")
    parser.add_argument("--generation-start", type=int)
    parser.add_argument("--generation-count", type=int)
    parser.add_argument("--repair-start", type=int)
    parser.add_argument("--repair-count", type=int)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--teacher-workers", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    if args.teacher_workers <= 0:
        raise ValueError("teacher-workers must be positive")
    custom_values = (args.generation_start, args.generation_count, args.repair_start, args.repair_count)
    if args.batch_index is not None and any(value is not None for value in custom_values):
        raise ValueError("batch-index and custom selection are mutually exclusive")
    if args.batch_index is None and any(value is None for value in custom_values):
        raise ValueError("provide batch-index or all four custom selection values")
    if args.batch_index is not None and args.batch_index < 0:
        raise ValueError("batch-index must be non-negative")
    config = json.loads(args.teacher_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    queue_bytes = args.queue.read_bytes()
    queue_rows = read_jsonl(args.queue)
    if args.batch_index is not None:
        rows = select_planned_batch(queue_rows, args.lane, args.batch_index)
        selection = {"lane": args.lane, "batch_index": args.batch_index, "generation": 6, "repair": 4}
    else:
        rows = select_custom_batch(
            queue_rows, args.lane, args.generation_start, args.generation_count,
            args.repair_start, args.repair_count,
        )
        selection = {
            "lane": args.lane, "generation_start": args.generation_start,
            "generation_count": args.generation_count, "repair_start": args.repair_start,
            "repair_count": args.repair_count,
        }
    candidates: list[dict[str, Any]] = []
    runs: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    try:
        candidates, runs, failures = generate_batch(rows, config, args.codex_bin, args.teacher_workers)
    except (CodexInvocationFailure, KeyError, OSError, RuntimeError, TypeError, ValueError) as exc:
        if isinstance(exc, CodexInvocationFailure):
            runs.append(exc.evidence)
        failures.append({"lane": args.lane, "reason": str(exc)})
    payload = b"".join(canonical_json(row) + b"\n" for row in candidates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    evidence = {
        "schema_version": "ganesh-mini-expansion-source-teacher-run/v1",
        "teacher": config, "cli_identity": cli_identity,
        "queue": {"path": str(args.queue), "sha256": hashlib.sha256(queue_bytes).hexdigest()},
        "selection": selection,
        "execution": {
            "teacher_workers": min(args.teacher_workers, len(rows)),
            "teacher_shards": [[row["id"] for row in shard] for shard in teacher_shards(rows, args.teacher_workers)],
        },
        "requested_ids": [row["id"] for row in rows], "generated": len(candidates),
        "candidate_output_sha256": hashlib.sha256(payload).hexdigest(), "failures": failures, "runs": runs,
    }
    evidence["evidence_sha256"] = hashlib.sha256(canonical_json(evidence)).hexdigest()
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"requested": len(rows), "generated": len(candidates), "failures": len(failures)}, sort_keys=True))
    return 0 if len(candidates) == len(rows) and not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
