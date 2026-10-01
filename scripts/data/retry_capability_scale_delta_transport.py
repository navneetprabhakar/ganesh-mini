#!/usr/bin/env python3
"""Retry sealed delta audits affected only by the CLI HTTPS-fallback classification."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import parse_events
from scripts.data.run_capability_scale_delta_audits import (
    _jsonl, _sealed, _write_json_atomic, _write_jsonl_atomic, run as run_delta,
)


def transport_only_failure(row: dict[str, Any]) -> bool:
    if row.get("status") != "invocation-failed":
        return False
    failure = row.get("failure")
    if not isinstance(failure, dict) or row.get("failure_sha256") != canonical_sha256(failure):
        return False
    if (
        failure.get("returncode") != 0
        or failure.get("timed_out") is not False
        or failure.get("event_parse_error") is not None
        or failure.get("disallowed_tool_item_types") != ["error"]
        or not isinstance(failure.get("usage"), dict)
        or not isinstance(failure.get("final_output"), str)
        or not failure["final_output"]
    ):
        return False
    try:
        events, usage, disallowed = parse_events(failure["stdout_jsonl"])
        payload = json.loads(failure["final_output"])
    except (KeyError, TypeError, ValueError):
        return False
    return (
        isinstance(payload, dict)
        and usage == failure["usage"]
        and not disallowed
        and events == failure["events"]
        and any(event.get("type") == "turn.completed" for event in events)
        and any(
            event.get("type") == "item.completed"
            and isinstance(event.get("item"), dict)
            and event["item"].get("type") == "error"
            and str(event["item"].get("message", "")).startswith(
                "Falling back from WebSockets to HTTPS transport."
            )
            for event in events
        )
    )


def load_parent(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], list[int]]:
    candidates = _jsonl(args.candidates)
    tests = _jsonl(args.test_author_artifacts)
    deltas = _jsonl(args.original_delta_artifacts)
    attached = _jsonl(args.original_attached_candidates)
    report = _sealed(json.loads(args.original_delta_report.read_text(encoding="utf-8")),
                     "report_sha256", "original delta report")
    test_report = _sealed(json.loads(args.test_author_report.read_text(encoding="utf-8")),
                          "report_sha256", "test author report")
    ids = [row.get("id") for row in candidates]
    if (
        len(candidates) != 534 or len(set(ids)) != 534
        or [row.get("candidate_id") for row in tests] != ids
        or [row.get("candidate_id") for row in deltas] != ids
        or [row.get("id") for row in attached] != ids
        or report.get("status") != "failed"
        or report.get("requested") != 534
        or report.get("rows_sha256") != canonical_sha256(deltas)
        or report.get("attached_candidates_sha256") != canonical_sha256(attached)
        or report.get("candidate_sha256s") != [canonical_sha256(row) for row in candidates]
        or report.get("test_author_artifact_sha256s") != [row.get("artifact_sha256") for row in tests]
        or report.get("terminal_artifact_sha256s") != [row.get("artifact_sha256") for row in deltas]
        or report.get("counts") != {"invocation-failed": 127, "passed": 407}
        or report.get("evaluation_artifacts_read") != 0
        or test_report.get("status") != "passed"
        or test_report.get("terminal_artifact_sha256s") != [row.get("artifact_sha256") for row in tests]
        or report.get("upstream_report_binding", {}).get("test_author_report_sha256") != test_report["report_sha256"]
    ):
        raise ValueError("parent delta campaign differs from its sealed 407/127 census")
    for candidate, test, delta in zip(candidates, tests, deltas, strict=True):
        _sealed(test, "artifact_sha256", f"{candidate['id']}/test-author")
        _sealed(delta, "artifact_sha256", f"{candidate['id']}/delta")
        if test.get("evaluation_artifacts_read") != 0 or delta.get("evaluation_artifacts_read") != 0:
            raise ValueError("evaluation artifacts were read")
    failed = [index for index, row in enumerate(deltas) if row["status"] == "invocation-failed"]
    if len(failed) != 127 or any(not transport_only_failure(deltas[index]) for index in failed):
        raise ValueError("non-transport failure cannot enter this retry")
    return candidates, tests, deltas, attached, report, failed


def run(args: argparse.Namespace) -> dict[str, Any]:
    candidates, tests, original, attached, parent, failed = load_parent(args)
    args.retry_output_dir.mkdir(parents=True, exist_ok=True)
    subset_candidates_path = args.retry_output_dir / "retry-candidates.jsonl"
    subset_tests_path = args.retry_output_dir / "retry-test-author-artifacts.jsonl"
    _write_jsonl_atomic(subset_candidates_path, [candidates[index] for index in failed])
    _write_jsonl_atomic(subset_tests_path, [tests[index] for index in failed])
    retry_args = argparse.Namespace(
        candidates=subset_candidates_path,
        test_author_artifacts=subset_tests_path,
        test_author_report=None,
        test_author_selection_report=None,
        codex_config=args.codex_config,
        codex_bin=args.codex_bin,
        workers=args.workers,
        run_dir=args.retry_run_dir,
        output_dir=args.retry_output_dir,
    )
    retry_report = run_delta(retry_args)
    if retry_report["status"] != "passed":
        return retry_report
    retried = _jsonl(args.retry_output_dir / "delta-terminal-artifacts.jsonl")
    retry_attached = _jsonl(args.retry_output_dir / "attached-candidates.jsonl")
    if (
        len(retried) != len(failed)
        or len(retry_attached) != len(failed)
        or retry_report.get("candidate_sha256s") != [canonical_sha256(candidates[index]) for index in failed]
        or retry_report.get("test_author_artifact_sha256s") != [tests[index]["artifact_sha256"] for index in failed]
        or retry_report.get("rows_sha256") != canonical_sha256(retried)
    ):
        raise ValueError("retry report does not bind the exact failed subset")
    for index, new, new_attached in zip(failed, retried, retry_attached, strict=True):
        old = original[index]
        _sealed(new, "artifact_sha256", f"{candidates[index]['id']}/retry")
        if (
            new.get("status") != "passed"
            or new.get("candidate_id") != old.get("candidate_id")
            or new.get("input_sha256") != old.get("input_sha256")
            or new.get("lineage") != old.get("lineage")
            or new.get("test_attachment") != old.get("test_attachment")
            or new_attached != attached[index]
        ):
            raise ValueError(f"{candidates[index]['id']}: retry input or attachment drift")
    merged = list(original)
    for index, new in zip(failed, retried, strict=True):
        merged[index] = new
    counts = dict(sorted(Counter(row["status"] for row in merged).items()))
    if counts != {"passed": 534}:
        raise ValueError("merged delta cohort did not pass")
    report = dict(parent)
    report.pop("report_sha256")
    report.update({
        "status": "passed", "counts": counts,
        "new_calls": parent["new_calls"] + retry_report["new_calls"],
        "resumed": parent["resumed"] + retry_report["resumed"],
        "terminal_artifact_sha256s": [row["artifact_sha256"] for row in merged],
        "lineage_bindings": [row["lineage"] for row in merged],
        "lineage_bindings_sha256": canonical_sha256([row["lineage"] for row in merged]),
        "rows_sha256": canonical_sha256(merged),
        "parent_report_sha256": parent["report_sha256"],
        "transport_retry_report_sha256": retry_report["report_sha256"],
        "transport_retry_candidate_ids": [candidates[index]["id"] for index in failed],
    })
    report["report_sha256"] = canonical_sha256(report)
    args.merged_output_dir.mkdir(parents=True, exist_ok=True)
    _write_jsonl_atomic(args.merged_output_dir / "attached-candidates.jsonl", attached)
    _write_jsonl_atomic(args.merged_output_dir / "delta-terminal-artifacts.jsonl", merged)
    _write_json_atomic(args.merged_output_dir / "delta-audit-report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--test-author-artifacts", type=Path, required=True)
    parser.add_argument("--test-author-report", type=Path, required=True)
    parser.add_argument("--original-delta-artifacts", type=Path, required=True)
    parser.add_argument("--original-delta-report", type=Path, required=True)
    parser.add_argument("--original-attached-candidates", type=Path, required=True)
    parser.add_argument("--retry-run-dir", type=Path, required=True)
    parser.add_argument("--retry-output-dir", type=Path, required=True)
    parser.add_argument("--merged-output-dir", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.workers <= 12:
        raise ValueError("workers must be 1..12")
    report = run(args)
    print(json.dumps({"status": report["status"], "counts": report["counts"],
                      "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
