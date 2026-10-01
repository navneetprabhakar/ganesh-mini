#!/usr/bin/env python3
"""Bind the approved one-cell Gate 3 token-length reserve without drafting."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_scale_queue import source_key


PLAN_SHA256 = "1844d190adcdc47496fc18fa9ec94babaeb469931985b384ac0c575726d4b13c"
QUEUE_MANIFEST_SHA256 = "f3e3e312625ec85f067c0089f40b16ed4591fe320745445e34f23825a3dc6d55"
FAILED_REPORT_SHA256 = "4e44bd293e5a7d5404ed44600c7534cf0fcf12bb46da60d835281e8449456927"
FAILED_ID = "cap-scale-binary_and_bitwise-typescript-repair-first_pass-01"
RESERVE_ID = "cap-scale-binary_and_bitwise-typescript-repair-reserve-06"
CELL = "binary_and_bitwise/typescript/repair"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sealed(path: Path, key: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    if body.pop(key, None) != canonical_sha256(body):
        raise ValueError(f"invalid seal: {path}")
    return value


def rows(path: Path) -> list[dict[str, Any]]:
    data = path.read_bytes()
    if not data or not data.endswith(b"\n"):
        raise ValueError(f"incomplete JSONL: {path}")
    return [json.loads(line) for line in data.splitlines()]


def prepare(plan: Path, queue: Path, queue_manifest: Path, failed_report: Path,
            capability: Path, replay: Path, prior: Path) -> tuple[list[dict], dict]:
    if file_sha(plan) != PLAN_SHA256:
        raise ValueError("approved proposal hash drift")
    manifest = sealed(queue_manifest, "manifest_sha256")
    if manifest["manifest_sha256"] != QUEUE_MANIFEST_SHA256 or manifest.get("queue_sha256") != file_sha(queue):
        raise ValueError("frozen queue binding differs")
    failed = sealed(failed_report, "report_sha256")
    if failed["report_sha256"] != FAILED_REPORT_SHA256 or failed.get("status") != "failed" or len(failed.get("failures", [])) != 1:
        raise ValueError("failed tokenization report differs")
    failure = failed["failures"][0]
    if failure.get("id") != FAILED_ID or "3032 tokens" not in failure.get("reason", "") or "max_length=2944" not in failure.get("reason", ""):
        raise ValueError("token-length trigger differs")
    queue_rows = rows(queue)
    if len(queue_rows) != 711:
        raise ValueError("frozen queue count differs")
    reserves = [row for row in queue_rows if row.get("id") == RESERVE_ID]
    if len(reserves) != 1 or reserves[0].get("cell_id") != CELL or reserves[0].get("cohort") != "reserve":
        raise ValueError("exact prebound reserve absent")
    reserve = reserves[0]
    if reserve.get("request_sha256") != canonical_sha256({k: v for k, v in reserve.items() if k != "request_sha256"}):
        raise ValueError("reserve request seal differs")
    if reserve.get("source", {}).get("record_id") != "row-33299" or reserve.get("source", {}).get("source_record_sha256") != "ccb28e294fc38b7e156cf48c4cb97f9a7402e48c0ac05064f046c92d74862ac5":
        raise ValueError("reserve source differs from approved plan")
    if sum(row.get("id") == RESERVE_ID for row in queue_rows) != 1:
        raise ValueError("duplicate reserve ID")
    original = [row for row in queue_rows if row.get("id") == FAILED_ID]
    if len(original) != 1 or original[0].get("cell_id") != CELL:
        raise ValueError("failed request differs from queue")
    cohort = rows(capability)
    if len(cohort) != 720 or sum(row.get("id") == FAILED_ID for row in cohort) != 1:
        raise ValueError("failed row absent from exact 720 cohort")
    if len(rows(replay)) != 180 or len(rows(prior)) != 3225:
        raise ValueError("historical corpus counts differ")
    reserve_source = source_key(reserve)
    if reserve_source in {source_key(row) for row in [*cohort, *rows(replay), *rows(prior)]}:
        raise ValueError("reserve source identity already in training")
    activation = {
        "schema_version": "ganesh-mini-capability-scale-token-length-reserve-activation/v1",
        "failed_candidate_id": FAILED_ID,
        "failed_stage": "final-package-tokenization",
        "failure_status": "rejected-overlength",
        "failure_artifact_sha256": FAILED_REPORT_SHA256,
        "queue_manifest_sha256": QUEUE_MANIFEST_SHA256,
        "reserve_candidate_id": RESERVE_ID,
        "reserve_request_sha256": reserve["request_sha256"],
        "reserve_source_queue_id": reserve["source_queue_id"],
        "cell_id": CELL,
        "approved_plan_sha256": PLAN_SHA256,
        "evaluation_artifacts_read": 0,
    }
    activation["activation_sha256"] = canonical_sha256(activation)
    report = {
        "schema_version": "ganesh-mini-gate3-token-length-activation-report/v1",
        "status": "activated",
        "approved_plan_sha256": PLAN_SHA256,
        "queue_manifest_sha256": QUEUE_MANIFEST_SHA256,
        "failed_tokenization_report_sha256": FAILED_REPORT_SHA256,
        "activation_rows_sha256": canonical_sha256([activation]),
        "activated": 1,
        "teacher_drafts_before": 1059,
        "maximum_teacher_drafts_after": 1060,
        "global_teacher_draft_cap": 1200,
        "evaluation_artifacts_read": 0,
        "gcloud_actions": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return [activation], report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("plan", "queue", "queue_manifest", "failed_report", "capability", "replay", "prior", "output_activation", "output_report"):
        parser.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    args = parser.parse_args()
    if args.output_activation.exists() or args.output_report.exists():
        raise ValueError("activation output already exists")
    activation, report = prepare(args.plan, args.queue, args.queue_manifest, args.failed_report,
                                 args.capability, args.replay, args.prior)
    args.output_activation.parent.mkdir(parents=True, exist_ok=True)
    with args.output_activation.open("x", encoding="utf-8") as handle:
        handle.write("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in activation))
    with args.output_report.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": "activated", "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
