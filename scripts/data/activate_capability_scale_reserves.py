#!/usr/bin/env python3
"""Activate one source-unique reserve for each terminal scale delta rejection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_capability_scale_teacher import QUEUE_SEAL, load_queue


ELIGIBLE_FAILURES = {"semantic-rejected", "response-contract-rejected"}


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sealed_file(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def _atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def activate(
    queue_path: Path, queue_manifest: Path, delta_artifacts: Path, delta_report_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    queue = load_queue(queue_path, queue_manifest)
    delta = _jsonl(delta_artifacts)
    report = _sealed_file(delta_report_path, "report_sha256")
    if (
        report.get("rows_sha256") != canonical_sha256(delta)
        or report.get("requested") != len(delta)
        or report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("delta report does not bind terminal artifacts")
    failures = [row for row in delta if row.get("status") in ELIGIBLE_FAILURES]
    reserves_by_cell: dict[str, list[dict[str, Any]]] = {}
    for row in queue:
        if row["cohort"] == "reserve":
            reserves_by_cell.setdefault(row["cell_id"], []).append(row)
    activations: list[dict[str, Any]] = []
    used: set[str] = set()
    for failure in failures:
        body = dict(failure); claimed = body.pop("artifact_sha256", None)
        if claimed != canonical_sha256(body) or failure.get("evaluation_artifacts_read") != 0:
            raise ValueError(f"{failure.get('candidate_id')}: failure artifact is unsealed")
        available = [row for row in reserves_by_cell.get(failure["cell_id"], []) if row["id"] not in used]
        if not available:
            raise ValueError(f"{failure['cell_id']}: no source-unique reserve remains")
        reserve = available[0]; used.add(reserve["id"])
        activation: dict[str, Any] = {
            "schema_version": "ganesh-mini-capability-scale-reserve-activation/v1",
            "failed_candidate_id": failure["candidate_id"],
            "failed_stage": "delta_audit",
            "failure_status": failure["status"],
            "failure_artifact_sha256": failure["artifact_sha256"],
            "cell_id": failure["cell_id"],
            "reserve_candidate_id": reserve["id"],
            "reserve_request_sha256": reserve["request_sha256"],
            "reserve_source_queue_id": reserve["source_queue_id"],
            "queue_manifest_sha256": QUEUE_SEAL,
            "evaluation_artifacts_read": 0,
        }
        activation["activation_sha256"] = canonical_sha256(activation)
        activations.append(activation)
    result: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-reserve-activation-report/v1",
        "status": "activated" if len(activations) == len(failures) else "failed",
        "delta_report_sha256": report["report_sha256"],
        "terminal_failures": len(failures),
        "activated": len(activations),
        "activation_rows_sha256": canonical_sha256(activations),
        "queue_manifest_sha256": QUEUE_SEAL,
        "evaluation_artifacts_read": 0,
    }
    result["report_sha256"] = canonical_sha256(result)
    return activations, result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--delta-artifacts", type=Path, required=True)
    parser.add_argument("--delta-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    rows, report = activate(args.queue, args.queue_manifest, args.delta_artifacts, args.delta_report)
    _atomic(args.output, "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    _atomic(args.report, json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "activated": report["activated"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "activated" else 2


if __name__ == "__main__":
    raise SystemExit(main())
