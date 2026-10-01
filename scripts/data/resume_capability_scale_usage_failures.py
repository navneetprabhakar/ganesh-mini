#!/usr/bin/env python3
"""Replay only usage-limited scale teacher calls and merge their sealed results."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import ARCHITECT_SCHEMA, verify_codex_version
from scripts.data.run_capability_scale_teacher import (
    PROMPT_CONTRACT_V2, QUEUE_SEAL, _jsonl, _sealed, _write_atomic,
    _write_atomic_text, load_queue, run_one, scale_architect_prompt,
    select_remaining_first_pass,
)


def expected_input_sha(row: dict[str, Any], config: dict[str, Any], cli_identity: str) -> str:
    return canonical_sha256({
        "request": row,
        "prompt": scale_architect_prompt(row, PROMPT_CONTRACT_V2),
        "schema_path": str(ARCHITECT_SCHEMA),
        "schema_sha256": hashlib.sha256(ARCHITECT_SCHEMA.read_bytes()).hexdigest(),
        "config": config,
        "cli_identity": cli_identity,
        "prompt_contract": PROMPT_CONTRACT_V2,
    })


def is_usage_limit_without_draft(artifact: dict[str, Any]) -> bool:
    if artifact.get("status") != "invocation-failed":
        return False
    failure = artifact.get("failure")
    if not isinstance(failure, dict):
        return False
    events = failure.get("events")
    if not isinstance(events, list):
        return False
    failed = [item for item in events if item.get("type") == "turn.failed"]
    return (
        len(failed) == 1
        and "You've hit your usage limit" in str(failed[0].get("error", {}).get("message", ""))
        and failure.get("final_output") == ""
        and failure.get("usage") is None
        and not any(item.get("type") == "turn.completed" for item in events)
    )


def load_original(
    queue: Path, manifest: Path, canary_report: Path,
    original_report_path: Path, original_candidates_path: Path,
    original_run_dir: Path, config: dict[str, Any], cli_identity: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    rows = select_remaining_first_pass(load_queue(queue, manifest), canary_report)
    report = _sealed(original_report_path, "report_sha256")
    candidates = _jsonl(original_candidates_path)
    artifacts = [_sealed(original_run_dir / f"{row['id']}.teacher.json", "artifact_sha256") for row in rows]
    statuses = Counter(item["status"] for item in artifacts)
    generated = [item["candidate"] for item in artifacts if item["status"] == "generated"]
    if (
        report.get("schema_version") != "ganesh-mini-capability-scale-teacher-report/v1"
        or report.get("status") != "failed"
        or report.get("mode") != "remaining-first-pass"
        or report.get("prompt_contract") != PROMPT_CONTRACT_V2
        or report.get("queue_manifest_sha256") != QUEUE_SEAL
        or report.get("requested") != 534
        or report.get("selected_request_sha256s") != [row["request_sha256"] for row in rows]
        or report.get("terminal_artifact_sha256s") != [item["artifact_sha256"] for item in artifacts]
        or report.get("counts") != dict(sorted(statuses.items()))
        or report.get("candidates_sha256") != canonical_sha256(generated)
        or candidates != generated
        or report.get("cli_identity") != cli_identity
        or report.get("config_sha256") != canonical_sha256(config)
        or report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("original teacher campaign differs from its sealed evidence")
    if statuses != {"generated": 381, "invocation-failed": 153}:
        raise ValueError("original teacher failure census differs from the frozen 381/153 result")
    for row, artifact in zip(rows, artifacts, strict=True):
        if (
            artifact.get("candidate_id") != row["id"]
            or artifact.get("cell_id") != row["cell_id"]
            or artifact.get("request_sha256") != row["request_sha256"]
            or artifact.get("input_sha256") != expected_input_sha(row, config, cli_identity)
            or artifact.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError(f"{row['id']}: original teacher artifact input drift")
        if artifact["status"] == "generated":
            if artifact.get("candidate_sha256") != canonical_sha256(artifact.get("candidate")):
                raise ValueError(f"{row['id']}: generated candidate hash drift")
        elif not is_usage_limit_without_draft(artifact):
            raise ValueError(f"{row['id']}: failure is not a no-draft usage-limit failure")
    return rows, artifacts, report


def run(args: argparse.Namespace) -> dict[str, Any]:
    config = json.loads(args.teacher_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    rows, original, parent = load_original(
        args.queue, args.queue_manifest, args.canary_teacher_report,
        args.original_teacher_report, args.original_candidates,
        args.original_run_dir, config, cli_identity,
    )
    failed_indices = [index for index, item in enumerate(original) if item["status"] == "invocation-failed"]
    selected = failed_indices[:args.limit] if args.limit is not None else failed_indices
    args.retry_run_dir.mkdir(parents=True, exist_ok=True)

    def invoke(index: int) -> tuple[int, dict[str, Any]]:
        return index, run_one(rows[index], config, args.codex_bin, cli_identity,
                              args.retry_run_dir, PROMPT_CONTRACT_V2)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(invoke, selected))

    retried: dict[int, dict[str, Any]] = {}
    for index in failed_indices:
        path = args.retry_run_dir / f"{rows[index]['id']}.teacher.json"
        if path.exists():
            item = _sealed(path, "artifact_sha256")
            if (
                item.get("candidate_id") != rows[index]["id"]
                or item.get("request_sha256") != rows[index]["request_sha256"]
                or item.get("input_sha256") != expected_input_sha(rows[index], config, cli_identity)
            ):
                raise ValueError(f"{rows[index]['id']}: replay artifact input drift")
            retried[index] = item
    counts = dict(sorted(Counter(item["status"] for item in retried.values()).items()))
    retry_report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-usage-retry-report/v1",
        "status": "passed" if counts == {"generated": len(failed_indices)} else "incomplete",
        "parent_report_sha256": parent["report_sha256"],
        "retry_eligible": len(failed_indices),
        "retry_completed": len(retried),
        "counts": counts,
        "retry_request_sha256s": [rows[index]["request_sha256"] for index in failed_indices],
        "retry_artifact_sha256s": [retried[index]["artifact_sha256"] for index in failed_indices if index in retried],
        "evaluation_artifacts_read": 0,
    }
    retry_report["report_sha256"] = canonical_sha256(retry_report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_atomic(args.output_dir / "usage-retry-report.json", retry_report)
    if retry_report["status"] != "passed":
        return retry_report

    merged = [retried.get(index, original[index]) for index in range(len(rows))]
    if any(item["status"] != "generated" for item in merged):
        raise ValueError("teacher merge contains a non-generated request")
    candidates = [item["candidate"] for item in merged]
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-teacher-report/v1",
        "status": "passed", "mode": "remaining-first-pass",
        "requested": 534, "counts": {"generated": 534},
        "prompt_contract": PROMPT_CONTRACT_V2,
        "queue_manifest_sha256": QUEUE_SEAL,
        "selected_request_sha256s": [row["request_sha256"] for row in rows],
        "terminal_artifact_sha256s": [item["artifact_sha256"] for item in merged],
        "candidates_sha256": canonical_sha256(candidates),
        "cli_identity": cli_identity, "config_sha256": canonical_sha256(config),
        "parent_report_sha256": parent["report_sha256"],
        "usage_retry_report_sha256": retry_report["report_sha256"],
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    _write_atomic_text(args.output_dir / "candidates.jsonl", "".join(
        json.dumps(item, sort_keys=True) + "\n" for item in candidates
    ))
    _write_atomic(args.output_dir / "teacher-report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--canary-teacher-report", type=Path, required=True)
    parser.add_argument("--original-teacher-report", type=Path, required=True)
    parser.add_argument("--original-candidates", type=Path, required=True)
    parser.add_argument("--original-run-dir", type=Path, required=True)
    parser.add_argument("--retry-run-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--teacher-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if not 1 <= args.workers <= 12 or args.limit is not None and args.limit < 1:
        raise ValueError("workers must be 1..12 and limit positive")
    report = run(args)
    print(json.dumps({"status": report["status"], "counts": report["counts"],
                      "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
