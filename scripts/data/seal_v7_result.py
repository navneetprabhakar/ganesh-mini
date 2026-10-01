#!/usr/bin/env python3
"""Seal the terminal V7 qualification result without reinterpreting outcomes."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v7_readiness import CONTRACT_ID


def _sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--readiness", type=Path, required=True)
    parser.add_argument("--first-pass", type=Path, required=True)
    parser.add_argument("--delta", type=Path, required=True)
    parser.add_argument("--separation", type=Path, required=True)
    parser.add_argument("--admission", type=Path, required=True)
    parser.add_argument("--terminal", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    readiness = _sealed(args.readiness, "report_sha256")
    first = _sealed(args.first_pass, "report_sha256")
    delta = _sealed(args.delta, "report_sha256")
    separation = _sealed(args.separation, "report_sha256")
    admission = _sealed(args.admission, "report_sha256")
    rows = [json.loads(line) for line in args.terminal.read_text(encoding="utf-8").splitlines() if line]
    if len(rows) != 60 or [row["ordinal"] for row in rows] != list(range(60)):
        raise ValueError("V7 terminal artifacts are not exact ordered 60")
    rejected = [row for row in rows if row["status"] != "admitted"]
    expected = {
        "cap-v4-associative_aggregation-rust-repair-primary": {
            "reference.primary_discrimination": "fail",
            "known_bad.primary_discrimination": "fail",
            "reference.cross_cutting": "pass",
            "known_bad.cross_cutting": "pass",
        },
        "cap-v4-binary_and_bitwise-python-repair-primary": {
            "reference.primary_discrimination": "pass",
            "known_bad.primary_discrimination": "fail",
            "reference.cross_cutting": "pass",
            "known_bad.cross_cutting": "fail",
        },
    }
    if {row["candidate_id"]: row["outcomes"] for row in rejected} != expected:
        raise ValueError("V7 rejection identities or matrices differ")
    admitted = [row for row in rows if row["status"] == "admitted"]
    report = {
        "schema_version": "ganesh-mini-gate2-v7-qualification-summary/v1",
        "contract_id": CONTRACT_ID,
        "status": "qualification-failed",
        "reason": "final-all-60-gate-failed",
        "plan_sha256": hashlib.sha256(args.plan.read_bytes()).hexdigest(),
        "readiness_report_sha256": readiness["report_sha256"],
        "first_pass_report_sha256": first["report_sha256"],
        "delta_report_sha256": delta["report_sha256"],
        "separation_report_sha256": separation["report_sha256"],
        "admission_report_sha256": admission["report_sha256"],
        "generated": 60, "admitted": 58, "rejected": 2, "unresolved": 0,
        "admitted_by_lane": dict(sorted(Counter(row["lane"] for row in admitted).items())),
        "admitted_by_capability": dict(sorted(Counter(row["primary_capability"] for row in admitted).items())),
        "admitted_by_dimension": dict(sorted(Counter(row["assigned_cross_cutting_dimension"] for row in admitted).items())),
        "rejections": [
            {
                "candidate_id": row["candidate_id"], "cell_id": row["cell_id"],
                "lane": row["lane"], "outcomes": row["outcomes"],
                "classification": (
                    "primary-test-overconstrains-unspecified-internal-key"
                    if row["lane"] == "rust" else
                    "cross-test-reasserts-primary-digest-dataflow"
                ),
                "bad_reference_demonstrated": False,
            }
            for row in rejected
        ],
        "v2_generation_equivalence": {
            "status": "passed", "generation_cells": 60,
            "qualification_report_sha256": "293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139",
            "admission_report_sha256": "c576ef4f5b0f137edac829703eae6d7c4a63cae513544d36471f7ffcf81b7cb7",
            "envelopes_file_sha256": "4b9427262b2c9645bf2a0edbddba5772340298d6d4554bd4b2f7bce1641d44bf",
        },
        "combined_coverage": {"covered": 118, "required": 120, "status": "failed"},
        "evaluation_artifacts_read_outside_content_free_boundary": 0,
        "training_authorized": False,
    }
    report["report_sha256"] = canonical_sha256(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
