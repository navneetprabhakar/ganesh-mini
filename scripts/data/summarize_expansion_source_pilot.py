#!/usr/bin/env python3
"""Seal the corrected-lineage source-driven expansion pilot summary."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.admit_expansion import _tokens, canonical_json, normalized_sha256, simhash


BATCHES = (
    ("go", "000"), ("java", "000"), ("javascript", "000"), ("typescript", "000"),
    ("python", "000"), ("rust", "000"), ("typescript", "001"), ("rust", "001"),
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def usage_from(path: Path) -> Counter[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    result: Counter[str] = Counter()
    for run in payload["runs"]:
        usage = run.get("usage") or {}
        result.update({
            "input_tokens": usage.get("input_tokens", 0),
            "cached_input_tokens": usage.get("cached_input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "reasoning_output_tokens": usage.get("reasoning_output_tokens", 0),
            "teacher_runs": 1,
        })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    measurement = args.root / "measurement/data/expansion-v1"
    cache = args.root / "datasets/cache/expansion-v1"
    review_path = measurement / "source-pilot-quality-review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    if review.get("status") != "passed" or not all(item.get("passed") is True for item in review.get("samples", [])):
        raise ValueError("manual quality review is not passed")
    queue_report = json.loads((measurement / "source-pilot-queue-v1-report.json").read_text(encoding="utf-8"))
    queue_sha = queue_report["output"]["sha256"]
    reports: list[dict[str, Any]] = []
    admitted: list[dict[str, Any]] = []
    usage: Counter[str] = Counter()
    batch_seals: dict[str, Any] = {}
    for lane, index in BATCHES:
        name = f"{lane}-{index}"
        report_path = measurement / f"source-pilot-{name}-lineage.admission.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        admitted_path = cache / f"source-pilot-{name}-lineage.admitted.jsonl"
        admitted_bytes = admitted_path.read_bytes()
        if report["output"]["sha256"] != sha256_bytes(admitted_bytes):
            raise ValueError(f"{name}: admission report output hash mismatch")
        lineage = json.loads((measurement / f"source-pilot-{name}-lineage-restoration.json").read_text(encoding="utf-8"))
        teacher = json.loads((cache / f"source-pilot-{name}.teacher-evidence.json").read_text(encoding="utf-8"))
        if teacher["queue"]["sha256"] != queue_sha:
            raise ValueError(f"{name}: teacher evidence queue hash mismatch")
        reports.append(report)
        admitted.extend(read_jsonl(admitted_path))
        usage.update(usage_from(cache / f"source-pilot-{name}.teacher-evidence.json"))
        usage.update(usage_from(cache / f"source-pilot-{name}-repair.teacher-evidence.json"))
        batch_seals[name] = {
            "accepted": report["accepted"], "rejected": len(report["rejected"]),
            "admission_report_sha256": report["report_sha256"],
            "lineage_restoration_sha256": lineage["evidence_sha256"],
        }
    ids: set[str] = set()
    prompts: dict[str, str] = {}
    conversations: set[str] = set()
    fuzzy: list[tuple[int, str, int]] = []
    collisions: list[dict[str, str]] = []
    for row in admitted:
        prompt = row["messages"][0]["content"]
        prompt_hash = normalized_sha256(prompt)
        conversation_hash = row["content_hashes"]["conversation_sha256"]
        if row["id"] in ids:
            collisions.append({"id": row["id"], "reason": "duplicate id"})
        if prompt_hash in prompts:
            collisions.append({"id": row["id"], "reason": f"exact prompt duplicate of {prompts[prompt_hash]}"})
        if conversation_hash in conversations:
            collisions.append({"id": row["id"], "reason": "exact conversation duplicate"})
        token_count = len(_tokens(prompt))
        if token_count >= 12:
            candidate_hash = simhash(prompt)
            for other_hash, other_id, other_tokens in fuzzy:
                if other_tokens >= 12 and (candidate_hash ^ other_hash).bit_count() <= 3:
                    collisions.append({"id": row["id"], "reason": f"fuzzy prompt duplicate of {other_id}"})
            fuzzy.append((candidate_hash, row["id"], token_count))
        ids.add(row["id"]); prompts[prompt_hash] = row["id"]; conversations.add(conversation_hash)
    lanes = Counter(row["lane"] for row in admitted)
    task_types = Counter(row["task_type"] for row in admitted)
    requested = len(BATCHES) * 10
    summary = {
        "schema_version": "ganesh-mini-expansion-source-pilot-summary/v1",
        "queue": {"records": queue_report["records"], "sha256": queue_sha},
        "requested": requested, "accepted": len(admitted), "rejected": requested - len(admitted),
        "yield": len(admitted) / requested,
        "accepted_by_lane": dict(sorted(lanes.items())),
        "accepted_by_task_type": dict(sorted(task_types.items())),
        "aggregate_teacher_usage": dict(usage),
        "cross_batch_collisions": collisions,
        "quality_review_sha256": sha256_bytes(review_path.read_bytes()),
        "batch_seals": batch_seals,
        "decision": (
            "Proceed with adaptive reserve generation and stop each lane/task type when its frozen final quota is met. "
            "Apply at most one targeted correction and reject remaining failures."
        ),
    }
    if collisions or len(admitted) != 71:
        raise ValueError(f"source pilot invariant failed: accepted={len(admitted)}, collisions={len(collisions)}")
    summary["summary_sha256"] = sha256_bytes(canonical_json(summary))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"accepted": len(admitted), "requested": requested, "sha256": summary["summary_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
