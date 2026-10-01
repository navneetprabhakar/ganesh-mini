#!/usr/bin/env python3
"""Export a sealed reserve-chain ledger into the frozen teacher activation schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_capability_scale_delta_audits import _write_json_atomic, _write_jsonl_atomic
from scripts.data.run_capability_scale_final_matrix import _sealed
from scripts.data.run_capability_scale_teacher import QUEUE_SEAL, load_queue


HISTORICAL_DRAFTS = 489
CANARY_DRAFTS = 19
REMAINING_FIRST_PASS_DRAFTS = 534
GLOBAL_DRAFT_CAP = 1200


def export(queue_path: Path, queue_manifest_path: Path, ledger_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    queue = load_queue(queue_path, queue_manifest_path)
    ledger = _sealed(json.loads(ledger_path.read_text(encoding="utf-8")), "ledger_sha256", str(ledger_path))
    activations = ledger.get("activations")
    if (
        ledger.get("status") != "active" or ledger.get("queue_manifest_sha256") != QUEUE_SEAL
        or ledger.get("evaluation_artifacts_read") != 0 or not isinstance(activations, list)
        or ledger.get("activation_count") != len(activations)
        or len(activations) != 16 or len({row.get("replacement_candidate_id") for row in activations}) != 16
        or HISTORICAL_DRAFTS + CANARY_DRAFTS + REMAINING_FIRST_PASS_DRAFTS + len(activations) > GLOBAL_DRAFT_CAP
    ):
        raise ValueError("reserve ledger or teacher-draft ceiling differs from the frozen campaign")
    queue_by_id = {row["id"]: row for row in queue}
    rows: list[dict[str, Any]] = []
    for ordinal, value in enumerate(activations, start=1):
        _sealed(value, "activation_sha256", str(value.get("replacement_candidate_id")))
        replacement = queue_by_id.get(value.get("replacement_candidate_id"))
        if (
            value.get("ordinal") != ordinal or replacement is None or replacement.get("cohort") != "reserve"
            or replacement.get("request_sha256") != value.get("replacement_request_sha256")
            or replacement.get("source_queue_id") != value.get("replacement_source_queue_id")
            or replacement.get("cell_id") != value.get("cell_id")
            or value.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError("reserve activation does not bind its frozen queue row")
        row = {
            "schema_version": "ganesh-mini-capability-scale-reserve-activation/v1",
            "failed_candidate_id": value["failed_candidate_id"],
            "failed_stage": value["failed_stage"],
            "failure_status": value["failure_status"],
            "failure_artifact_sha256": value["failure_artifact_sha256"],
            "cell_id": value["cell_id"],
            "reserve_candidate_id": value["replacement_candidate_id"],
            "reserve_request_sha256": value["replacement_request_sha256"],
            "reserve_source_queue_id": value["replacement_source_queue_id"],
            "queue_manifest_sha256": QUEUE_SEAL,
            "reserve_chain_activation_sha256": value["activation_sha256"],
            "evaluation_artifacts_read": 0,
        }
        row["activation_sha256"] = canonical_sha256(row)
        rows.append(row)
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-reserve-activation-report/v1",
        "status": "activated", "queue_manifest_sha256": QUEUE_SEAL,
        "reserve_ledger_sha256": ledger["ledger_sha256"],
        "terminal_failures": len(rows), "activated": len(rows),
        "activation_rows_sha256": canonical_sha256(rows),
        "teacher_drafts_before": HISTORICAL_DRAFTS + CANARY_DRAFTS + REMAINING_FIRST_PASS_DRAFTS,
        "projected_drafts_after": HISTORICAL_DRAFTS + CANARY_DRAFTS + REMAINING_FIRST_PASS_DRAFTS + len(rows),
        "global_teacher_draft_cap": GLOBAL_DRAFT_CAP,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return rows, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output-rows", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()
    if args.output_rows.exists() or args.output_report.exists():
        raise ValueError("reserve activation outputs already exist")
    rows, report = export(args.queue, args.queue_manifest, args.ledger)
    _write_jsonl_atomic(args.output_rows, rows)
    _write_json_atomic(args.output_report, report)
    print(json.dumps({"activated": report["activated"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
