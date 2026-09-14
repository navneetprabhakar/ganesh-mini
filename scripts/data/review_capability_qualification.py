#!/usr/bin/env python3
"""Blind semantic review for capability-qualification candidate specifications."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256, load_sealed
from scripts.data.generate_capability_qualification import LANES, teacher_shards
from scripts.data.generate_expansion_qualification import (
    CodexInvocationFailure,
    canonical_json,
    invoke_codex,
    verify_codex_version,
)
from scripts.eval.contracts import sha256_text


REVIEW_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "id", "verdict", "primary_capability_is_substantive",
                    "generic_edge_case_boilerplate_is_primary", "rationale",
                ],
                "properties": {
                    "id": {"type": "string", "minLength": 1},
                    "verdict": {"type": "string", "enum": ["pass", "reject"]},
                    "primary_capability_is_substantive": {"type": "boolean"},
                    "generic_edge_case_boilerplate_is_primary": {"type": "boolean"},
                    "rationale": {"type": "string", "minLength": 1},
                },
            },
        },
    },
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_candidates(path: Path) -> list[dict[str, Any]]:
    rows = read_jsonl(path)
    if not rows or len({row.get("id") for row in rows}) != len(rows):
        raise ValueError("candidate input must contain unique IDs")
    for row in rows:
        assignment = row.get("qualification_assignment")
        messages = row.get("messages")
        if (
            row.get("lane") not in LANES
            or not isinstance(assignment, dict)
            or assignment.get("cell_id")
            != f"{assignment.get('primary_capability')}/{row.get('lane')}/{row.get('task_type')}"
            or not isinstance(assignment.get("primary_capability_definition"), str)
            or not assignment["primary_capability_definition"].strip()
            or not isinstance(assignment.get("assigned_cross_cutting_dimension"), str)
            or not assignment["assigned_cross_cutting_dimension"].strip()
            or not isinstance(messages, list)
            or len(messages) != 2
            or messages[0].get("role") != "user"
            or not isinstance(messages[0].get("content"), str)
            or not messages[0]["content"].strip()
        ):
            raise ValueError(f"{row.get('id')}: candidate lacks a valid semantic-review binding")
    return rows


def select_batch(rows: list[dict[str, Any]], lane: str, batch_index: int, batch_size: int) -> list[dict[str, Any]]:
    if lane not in LANES or batch_index < 0 or not 1 <= batch_size <= 10:
        raise ValueError("lane, batch-index, or batch-size is invalid")
    lane_rows = [row for row in rows if row["lane"] == lane]
    selected = lane_rows[batch_index * batch_size:(batch_index + 1) * batch_size]
    if not selected:
        raise ValueError(f"empty semantic-review batch {lane}/{batch_index}")
    return selected


def review_prompt(rows: list[dict[str, Any]]) -> str:
    visible = [
        {
            "id": row["id"],
            "specification": row["messages"][0]["content"],
            "assigned_primary_capability": row["qualification_assignment"]["primary_capability"],
            "primary_capability_definition": row["qualification_assignment"]["primary_capability_definition"],
            "scheduled_cross_cutting_dimension": row["qualification_assignment"]["assigned_cross_cutting_dimension"],
        }
        for row in rows
    ]
    return f"""Independently review whether each training-task specification satisfies its assigned ontology labels.
Do not use tools or inspect the filesystem. You may see only candidate IDs, specifications, assigned primary
capabilities and definitions, and scheduled cross-cutting dimensions. You have not seen reference implementations,
known-bad implementations, tests, verifier outputs, teacher context, source stimuli, or evaluation artifacts.

Items: {json.dumps(visible, separators=(",", ":"), ensure_ascii=False)}

Pass only when the assigned primary capability is a substantive behavior required to solve the specification and the
scheduled cross-cutting dimension is concretely specified. Reject when the capability is merely named, incidental, or
replaceable by generic edge-case prose, or when broad empty/malformed/boundary/ordering/aliasing/mutation boilerplate
dominates the task. Set primary_capability_is_substantive and generic_edge_case_boilerplate_is_primary independently,
then make verdict consistent: pass requires true and false respectively. Give a concise specification-only rationale.
Return every exact ID and only the schema-constrained object."""


def seal_run(evidence: dict[str, Any]) -> dict[str, Any]:
    sealed = dict(evidence)
    sealed["run_evidence_sha256"] = sha256_bytes(canonical_json(sealed))
    return sealed


def exact_review_items(payload: dict[str, Any], expected_ids: list[str]) -> list[dict[str, Any]]:
    fields = {
        "id", "verdict", "primary_capability_is_substantive",
        "generic_edge_case_boilerplate_is_primary", "rationale",
    }
    items = payload.get("items")
    if not isinstance(items, list) or len(items) != len(expected_ids):
        raise ValueError("semantic-review item count differs from request")
    by_id: dict[str, dict[str, Any]] = {}
    for item in items:
        if (
            not isinstance(item, dict)
            or set(item) != fields
            or not isinstance(item.get("id"), str)
            or not item["id"].strip()
            or item.get("verdict") not in {"pass", "reject"}
            or type(item.get("primary_capability_is_substantive")) is not bool
            or type(item.get("generic_edge_case_boilerplate_is_primary")) is not bool
            or not isinstance(item.get("rationale"), str)
            or not item["rationale"].strip()
            or item["id"] in by_id
        ):
            raise ValueError("semantic-review item differs from contract")
        by_id[item["id"]] = item
    if set(by_id) != set(expected_ids):
        raise ValueError("semantic-review IDs differ from request")
    return [by_id[record_id] for record_id in expected_ids]


def candidate_sha256(candidate: dict[str, Any]) -> str:
    return canonical_sha256({
        key: value for key, value in candidate.items()
        if key not in {"qualification_assignment", "teacher_evidence"}
    })


def build_semantic_evidence(
    candidate: dict[str, Any], review: dict[str, Any], run_evidence_sha256: str,
) -> dict[str, Any]:
    substantive = review["primary_capability_is_substantive"]
    generic = review["generic_edge_case_boilerplate_is_primary"]
    verdict = review["verdict"]
    if (verdict == "pass") != (substantive is True and generic is False):
        raise ValueError(f"{candidate['id']}: semantic verdict is internally inconsistent")
    assignment = candidate["qualification_assignment"]
    evidence: dict[str, Any] = {
        "candidate_sha256": candidate_sha256(candidate),
        "specification_sha256": sha256_text(candidate["messages"][0]["content"]),
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        "verdict": verdict,
        "primary_capability_is_substantive": substantive,
        "generic_edge_case_boilerplate_is_primary": generic,
        "rationale": review["rationale"],
        "reviewer_run_evidence_sha256": run_evidence_sha256,
        "visibility": {
            "specification_and_assigned_labels_only": True,
            "reference_visible": False,
            "known_bad_visible": False,
            "tests_visible": False,
            "verifier_outputs_visible": False,
            "teacher_context_visible": False,
            "source_stimulus_visible": False,
            "evaluation_artifacts_read": 0,
        },
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return evidence


def review_shard(
    rows: list[dict[str, Any]], config: dict[str, Any], codex_bin: str, schema_path: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str | None]:
    lane = rows[0]["lane"]
    expected_ids = [row["id"] for row in rows]
    runs: list[dict[str, Any]] = []
    try:
        payload, run = invoke_codex(
            codex_bin, config, schema_path, review_prompt(rows), "capability-blind-semantic-review", lane,
        )
        run = seal_run(run)
        runs.append(run)
        items = exact_review_items(payload, expected_ids)
        by_id = {row["id"]: row for row in rows}
        return [build_semantic_evidence(by_id[item["id"]], item, run["run_evidence_sha256"]) for item in items], runs, None
    except CodexInvocationFailure as exc:
        runs.append(seal_run(exc.evidence))
        return [], runs, str(exc)
    except (KeyError, OSError, RuntimeError, TypeError, ValueError) as exc:
        return [], runs, str(exc)


def review_batch(
    rows: list[dict[str, Any]], config: dict[str, Any], codex_bin: str, schema_path: Path,
    workers: int = 1,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]]:
    if not rows or any(row["lane"] != rows[0]["lane"] for row in rows):
        raise ValueError("semantic-review batch must be nonempty and lane-homogeneous")
    if not 1 <= workers <= 4:
        raise ValueError("review workers must be 1..4")
    shards = teacher_shards(rows, workers)
    results: list[tuple[list[dict[str, Any]], list[dict[str, Any]], str | None] | None] = [None] * len(shards)
    with ThreadPoolExecutor(max_workers=len(shards)) as executor:
        futures = {
            executor.submit(review_shard, shard, config, codex_bin, schema_path): index
            for index, shard in enumerate(shards)
        }
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    reviews: list[dict[str, Any]] = []
    runs: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for index, result in enumerate(results):
        if result is None:
            raise RuntimeError(f"semantic-review shard {index} did not return")
        shard_reviews, shard_runs, error = result
        reviews.extend(shard_reviews)
        runs.extend(shard_runs)
        if error is not None:
            failures.append({"lane": rows[0]["lane"], "shard": str(index), "reason": error})
    if failures:
        reviews = []
    return reviews, runs, failures


def campaign_descriptor(candidates_path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    descriptor = {
        "candidate_input_sha256": sha256_bytes(candidates_path.read_bytes()),
        "candidate_count": len(rows),
        "ordered_candidate_ids": [row["id"] for row in rows],
        "evaluation_artifacts_read": 0,
    }
    descriptor["campaign_sha256"] = canonical_sha256(descriptor)
    return descriptor


def verify_completed(
    output: Path, evidence_path: Path, expected_ids: list[str], campaign_sha256: str, batch_sha256: str,
) -> dict[str, Any] | None:
    if not output.exists() and not evidence_path.exists():
        return None
    if not output.is_file() or not evidence_path.is_file():
        raise ValueError("partial semantic-review artifacts exist")
    evidence = load_sealed(evidence_path, "evidence_sha256")
    rows = read_jsonl(output)
    if (
        evidence.get("campaign_sha256") != campaign_sha256
        or evidence.get("batch_sha256") != batch_sha256
        or evidence.get("semantic_output_sha256") != sha256_bytes(output.read_bytes())
        or evidence.get("requested_ids") != expected_ids
        or evidence.get("failures") != []
        or len(rows) != len(expected_ids)
        or any(row.get("candidate_sha256") is None for row in rows)
        or any(load_evidence(row) is None for row in rows)
    ):
        raise ValueError("existing semantic-review batch fails its seal")
    return evidence


def load_evidence(row: dict[str, Any]) -> dict[str, Any] | None:
    try:
        claimed = row["evidence_sha256"]
        body = dict(row)
        body.pop("evidence_sha256")
        return row if claimed == canonical_sha256(body) else None
    except (KeyError, TypeError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teacher-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--lane", choices=LANES, required=True)
    parser.add_argument("--batch-index", type=int, required=True)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.teacher_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    all_rows = load_candidates(args.candidates)
    selected = select_batch(all_rows, args.lane, args.batch_index, args.batch_size)
    campaign = campaign_descriptor(args.candidates, all_rows)
    batch = {
        "campaign_sha256": campaign["campaign_sha256"],
        "lane": args.lane,
        "batch_index": args.batch_index,
        "batch_size": args.batch_size,
        "ordered_candidate_ids": [row["id"] for row in selected],
    }
    batch_sha256 = canonical_sha256(batch)
    completed = verify_completed(
        args.output, args.evidence, batch["ordered_candidate_ids"], campaign["campaign_sha256"], batch_sha256,
    )
    if completed is not None:
        print(json.dumps({"status": "reused", "reviewed": len(selected)}, sort_keys=True))
        return 0

    with tempfile.TemporaryDirectory(prefix="ganesh-semantic-schema-") as temp_name:
        schema_path = Path(temp_name) / "semantic-review.schema.json"
        schema_path.write_text(json.dumps(REVIEW_SCHEMA, sort_keys=True) + "\n", encoding="utf-8")
        reviews, runs, failures = review_batch(selected, config, args.codex_bin, schema_path, args.workers)
    payload = b"".join(canonical_json(review) + b"\n" for review in reviews)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    evidence: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-semantic-review-batch/v1",
        "cli_identity": cli_identity,
        "teacher": config,
        "campaign": campaign,
        "campaign_sha256": campaign["campaign_sha256"],
        "batch": batch,
        "batch_sha256": batch_sha256,
        "requested_ids": batch["ordered_candidate_ids"],
        "reviewed": len(reviews),
        "semantic_output_sha256": sha256_bytes(payload),
        "evaluation_artifacts_read": 0,
        "runs": runs,
        "failures": failures,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "reviewed", "reviewed": len(reviews), "failures": len(failures)}, sort_keys=True))
    return 0 if len(reviews) == len(selected) and not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
