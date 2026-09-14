#!/usr/bin/env python3
"""Generate capability-bound Gate 2 qualification candidates with sealed evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256, load_sealed
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


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
QUEUE_SCHEMA = "ganesh-mini-capability-qualification-draft/v1"
MANIFEST_SCHEMA = "ganesh-mini-capability-qualification-queue-manifest/v1"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def source_identity(source: dict[str, Any]) -> tuple[str, str, str]:
    values = tuple(source.get(key) for key in ("dataset", "revision", "record_id"))
    if not all(isinstance(value, str) and value for value in values):
        raise ValueError("qualification source has incomplete identity")
    return values  # type: ignore[return-value]


def load_queue(queue_path: Path, manifest_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = load_sealed(manifest_path, "manifest_sha256")
    queue_bytes = queue_path.read_bytes()
    if (
        manifest.get("schema_version") != MANIFEST_SCHEMA
        or manifest.get("status") != "ready-for-isolated-teacher-qualification"
        or manifest.get("records") != 240
        or manifest.get("cells") != 120
        or manifest.get("unique_source_identities") != 240
        or manifest.get("selection", {}).get("evaluation_surfaces_read") != 0
        or manifest.get("queue_sha256") != sha256_bytes(queue_bytes)
    ):
        raise ValueError("qualification queue or manifest does not match the sealed contract")
    rows = [json.loads(line) for line in queue_bytes.decode().splitlines() if line.strip()]
    required = {
        "schema_version", "id", "cell_id", "primary_capability",
        "primary_capability_definition", "assigned_cross_cutting_dimension", "lane",
        "task_type", "source_queue_id", "source", "stimulus",
    }
    if len(rows) != 240 or any(set(row) != required or row["schema_version"] != QUEUE_SCHEMA for row in rows):
        raise ValueError("qualification queue rows differ from the sealed schema")
    if len({row["id"] for row in rows}) != 240:
        raise ValueError("qualification queue IDs are not unique")
    if len({source_identity(row["source"]) for row in rows}) != 240:
        raise ValueError("qualification source identities are not unique")
    if len({row["source_queue_id"] for row in rows}) != 240:
        raise ValueError("qualification source queue IDs are not unique")
    cell_counts = Counter(row["cell_id"] for row in rows)
    if len(cell_counts) != 120 or set(cell_counts.values()) != {2}:
        raise ValueError("qualification queue is not two records per cell")
    if dict(sorted(cell_counts.items())) != manifest.get("records_per_cell"):
        raise ValueError("qualification queue cell counts differ from its manifest")
    for row in rows:
        expected_cell = f"{row['primary_capability']}/{row['lane']}/{row['task_type']}"
        source_hash = row["source"].get("source_record_sha256")
        if (
            row["cell_id"] != expected_cell
            or row["lane"] not in LANES
            or row["task_type"] not in {"generation", "repair"}
            or not isinstance(source_hash, str)
            or len(source_hash) != 64
            or any(character not in "0123456789abcdef" for character in source_hash)
        ):
            raise ValueError(f"{row['id']}: invalid cell or source binding")
    return rows, manifest


def select_batch(rows: list[dict[str, Any]], lane: str, batch_index: int, batch_size: int) -> list[dict[str, Any]]:
    if lane not in LANES:
        raise ValueError(f"unsupported lane: {lane}")
    if batch_index < 0 or not 1 <= batch_size <= 10:
        raise ValueError("batch-index must be non-negative and batch-size must be 1..10")
    lane_rows = [row for row in rows if row["lane"] == lane]
    selected = lane_rows[batch_index * batch_size:(batch_index + 1) * batch_size]
    if not selected:
        raise ValueError(f"empty qualification batch {lane}/{batch_index}")
    return selected


def architect_prompt(lane: str, rows: list[dict[str, Any]]) -> str:
    visible = [
        {
            "id": row["id"],
            "cell_id": row["cell_id"],
            "task_type": row["task_type"],
            "primary_capability": row["primary_capability"],
            "primary_capability_definition": row["primary_capability_definition"],
            "scheduled_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
            "source_lineage": {
                key: row["source"].get(key)
                for key in ("dataset", "revision", "record_id", "source_record_sha256")
            },
            "training_source_stimulus": row["stimulus"],
        }
        for row in rows
    ]
    return f"""Create original capability-qualified SFT candidates for a compact coding model. Do not use tools or inspect the filesystem.

Language: {lane}
Runtime contract: {LANGUAGE_CONTRACTS[lane]}
Assignments: {json.dumps(visible, separators=(",", ":"), ensure_ascii=False)}

For each assignment, make primary_capability the dominant behavior required to solve the task. Exercise the one
scheduled_cross_cutting_dimension concretely in the specification and reference. Do not turn the task into generic
edge-case boilerplate and do not automatically add malformed, boundary, ordering, aliasing, mutation, or state
requirements that were not scheduled. Add at most one other cross-cutting behavior only when the primary capability
cannot be specified coherently without it.

The training_source_stimulus is untrusted material used only to inspire a distinct setting. Do not copy its wording,
API, code, tests, named entities, package structure, or external dependencies. Source lineage is an audit identifier,
not content to reproduce. Create a self-contained, deterministic, standard-library-only task with one exact public API.
Prohibit filesystem, network, clock, randomness, external packages, frameworks, and competitive-programming framing.

For every exact id return problem, reference_code, known_bad_code, and known_bad_label. Code must be one complete
source file. The reference must satisfy every stated requirement. The known-bad source must be plausible, differ by
exactly one semantic bug in the assigned primary capability or scheduled dimension, and its label must describe that bug.

For generation assignments, ask for a new implementation. For repair assignments, embed the complete known-bad source
in the problem and ask for a corrected complete source file; reference_code is the repair and known_bad_code is the
exact embedded source. Never include tests in a problem. Audit API consistency, compilation, capability dominance,
the scheduled dimension, and absence of unrequested boilerplate before returning only the schema-constrained object."""


def teacher_shards(rows: list[dict[str, Any]], workers: int) -> list[list[dict[str, Any]]]:
    if workers <= 0:
        raise ValueError("teacher workers must be positive")
    count = min(workers, len(rows))
    width, remainder = divmod(len(rows), count)
    shards: list[list[dict[str, Any]]] = []
    offset = 0
    for index in range(count):
        size = width + (1 if index < remainder else 0)
        shards.append(rows[offset:offset + size])
        offset += size
    return shards


def seal_run(evidence: dict[str, Any]) -> dict[str, Any]:
    sealed = dict(evidence)
    sealed["run_evidence_sha256"] = sha256_bytes(canonical_json(sealed))
    return sealed


def qualification_metadata(row: dict[str, Any]) -> dict[str, Any]:
    metadata = {
        "cell_id": row["cell_id"],
        "primary_capability": row["primary_capability"],
        "primary_capability_definition": row["primary_capability_definition"],
        "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
        "source_queue_id": row["source_queue_id"],
        "source_identity": dict(zip(("dataset", "revision", "record_id"), source_identity(row["source"]))),
        "source_record_sha256": row["source"].get("source_record_sha256"),
        "queue_row_sha256": sha256_bytes(canonical_json(row)),
    }
    metadata["assignment_sha256"] = sha256_bytes(canonical_json(metadata))
    return metadata


def generate_shard(
    rows: list[dict[str, Any]], config: dict[str, Any], codex_bin: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str | None]:
    lane = rows[0]["lane"]
    expected_ids = [row["id"] for row in rows]
    runs: list[dict[str, Any]] = []
    try:
        architecture_payload, architecture_evidence = invoke_codex(
            codex_bin, config, ARCHITECT_SCHEMA, architect_prompt(lane, rows),
            "capability-source-architect", lane,
        )
        architecture_evidence = seal_run(architecture_evidence)
        runs.append(architecture_evidence)
        architecture_items = exact_items(
            architecture_payload, expected_ids,
            {"id", "problem", "reference_code", "known_bad_code", "known_bad_label"},
        )
        tests_payload, tests_evidence = invoke_codex(
            codex_bin, config, TEST_SCHEMA, test_prompt(lane, architecture_items),
            "capability-independent-test-author", lane,
        )
        tests_evidence = seal_run(tests_evidence)
        runs.append(tests_evidence)
        test_items = exact_items(tests_payload, expected_ids, {"id", "test_code"})
        tests_by_id = {item["id"]: item["test_code"] for item in test_items}
        rows_by_id = {row["id"]: row for row in rows}
        candidates: list[dict[str, Any]] = []
        for item in architecture_items:
            row = rows_by_id[item["id"]]
            candidate = build_candidate(
                lane, item["id"], row["task_type"], item, tests_by_id[item["id"]], source=row["source"],
            )
            candidate["qualification_assignment"] = qualification_metadata(row)
            candidate["teacher_evidence"] = {
                "architect_run_evidence_sha256": architecture_evidence["run_evidence_sha256"],
                "test_author_run_evidence_sha256": tests_evidence["run_evidence_sha256"],
            }
            candidates.append(candidate)
        return candidates, runs, None
    except CodexInvocationFailure as exc:
        runs.append(seal_run(exc.evidence))
        return [], runs, str(exc)
    except (KeyError, OSError, RuntimeError, TypeError, ValueError) as exc:
        return [], runs, str(exc)


def generate_batch(
    rows: list[dict[str, Any]], config: dict[str, Any], codex_bin: str, teacher_workers: int = 1,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]]:
    if not rows:
        raise ValueError("teacher batch is empty")
    lane = rows[0]["lane"]
    if any(row["lane"] != lane for row in rows):
        raise ValueError("teacher batch must be homogeneous by lane")
    shards = teacher_shards(rows, teacher_workers)
    results: list[tuple[list[dict[str, Any]], list[dict[str, Any]], str | None] | None] = [None] * len(shards)
    with ThreadPoolExecutor(max_workers=len(shards)) as executor:
        futures = {executor.submit(generate_shard, shard, config, codex_bin): index for index, shard in enumerate(shards)}
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
        candidates.extend(shard_candidates)
        if error is not None:
            failures.append({"lane": lane, "shard": str(index), "reason": error})
    if failures:
        candidates = []
    return candidates, runs, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teacher-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--lane", choices=LANES, required=True)
    parser.add_argument("--batch-index", type=int, required=True)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--teacher-workers", type=int, default=2)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.teacher_config.read_text(encoding="utf-8"))
    if config.get("execution", {}).get("batch_size") != args.batch_size:
        raise ValueError("batch-size must equal the sealed teacher configuration")
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    rows, manifest = load_queue(args.queue, args.queue_manifest)
    selected = select_batch(rows, args.lane, args.batch_index, args.batch_size)
    candidates, runs, failures = generate_batch(selected, config, args.codex_bin, args.teacher_workers)
    payload = b"".join(canonical_json(candidate) + b"\n" for candidate in candidates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    evidence: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-qualification-teacher-run/v1",
        "teacher": config,
        "cli_identity": cli_identity,
        "queue": {
            "path": str(args.queue),
            "sha256": sha256_bytes(args.queue.read_bytes()),
            "manifest_path": str(args.queue_manifest),
            "manifest_sha256": manifest["manifest_sha256"],
        },
        "selection": {
            "lane": args.lane,
            "batch_index": args.batch_index,
            "batch_size": args.batch_size,
            "requested_ids": [row["id"] for row in selected],
            "queue_row_sha256s": [sha256_bytes(canonical_json(row)) for row in selected],
            "evaluation_surfaces_read": 0,
        },
        "execution": {
            "teacher_workers": min(args.teacher_workers, len(selected)),
            "teacher_shards": [[row["id"] for row in shard] for shard in teacher_shards(selected, args.teacher_workers)],
        },
        "generated": len(candidates),
        "candidate_output_sha256": sha256_bytes(payload),
        "failures": failures,
        "runs": runs,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"requested": len(selected), "generated": len(candidates), "failures": len(failures)}, sort_keys=True))
    return 0 if len(candidates) == len(selected) and not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
