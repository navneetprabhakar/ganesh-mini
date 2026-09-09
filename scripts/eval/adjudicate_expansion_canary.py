#!/usr/bin/env python3
"""Apply the frozen Gate 4 canary promotion rule to executed task evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
FAMILY = {"go": "go", "java": "java", "javascript": "javascript-typescript", "typescript": "javascript-typescript", "python": "python", "rust": "rust"}


def canonical_digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    claimed = value.pop(field, None)
    if claimed != canonical_digest(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def task_rows(directory: Path, task_ids: set[str] | None = None) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    paths = (
        [directory / f"{task_id}.json" for task_id in sorted(task_ids)]
        if task_ids is not None
        else sorted(directory.glob("*.json"))
    )
    for path in paths:
        if not path.is_file():
            raise ValueError(f"missing task evidence: {path}")
        evidence = load_sealed(path, "evidence_sha256")
        task = evidence.get("task", {})
        task_id, lane = task.get("task_id"), task.get("language")
        if not isinstance(task_id, str) or lane not in LANES or task_id in rows:
            raise ValueError(f"invalid or duplicate task evidence: {path}")
        generation = evidence.get("generation", {})
        parameters = evidence.get("parameters") or generation.get("parameters") or {}
        output_tokens = parameters.get("output_tokens", 0)
        maximum = parameters.get("max_new_tokens", 4096)
        rows[task_id] = {
            "lane": lane,
            "family": FAMILY[lane],
            "passed": evidence.get("verification", {}).get("result", {}).get("passed") is True,
            "non_code": not bool(evidence.get("extraction", {}).get("extracted_code", "").strip()),
            "truncated": generation.get("stopped_at_eos") is False and output_tokens >= maximum,
            "evidence_sha256": evidence["evidence_sha256"],
        }
    return rows


def adjudicate(card_path: Path, terminal_path: Path, base_dir: Path, candidate_dir: Path) -> dict[str, Any]:
    card = load_sealed(card_path, "card_sha256")
    terminal = load_sealed(terminal_path, "report_sha256")
    if card.get("status") != "ready" or terminal.get("status") != "passed" or terminal.get("card_sha256") != card.get("card_sha256"):
        raise ValueError("canary adjudication requires the matching passed terminal training report")
    candidate = task_rows(candidate_dir)
    base = task_rows(base_dir, set(candidate))
    if len(candidate) != card.get("evaluation", {}).get("canary_tasks") or set(candidate) != set(base):
        raise ValueError("candidate canary does not exactly map to baseline evidence")
    lane_base = Counter({lane: 0 for lane in LANES}); lane_candidate = Counter({lane: 0 for lane in LANES})
    family_base: Counter[str] = Counter(); family_candidate: Counter[str] = Counter()
    for task_id, row in candidate.items():
        baseline = base[task_id]
        if baseline["lane"] != row["lane"]:
            raise ValueError("candidate and baseline lane bindings differ")
        lane_base[row["lane"]] += int(baseline["passed"]); lane_candidate[row["lane"]] += int(row["passed"])
        family_base[row["family"]] += int(baseline["passed"]); family_candidate[row["family"]] += int(row["passed"])
    rule = card["evaluation"]["promotion_rule"]
    improved_families = sum(family_candidate[name] > family_base[name] for name in set(FAMILY.values()))
    net_gain = sum(lane_candidate.values()) - sum(lane_base.values())
    maximum_lane_regression = max(lane_base[lane] - lane_candidate[lane] for lane in LANES)
    base_non_code = sum(row["non_code"] for row in base.values()); candidate_non_code = sum(row["non_code"] for row in candidate.values())
    base_truncated = sum(row["truncated"] for row in base.values()); candidate_truncated = sum(row["truncated"] for row in candidate.values())
    checks = [
        {"name": "improved_product_families", "passed": improved_families >= rule["minimum_improved_product_families"], "observed": improved_families},
        {"name": "net_pass_gain", "passed": net_gain >= rule["minimum_net_pass_gain"], "observed": net_gain},
        {"name": "lane_regression", "passed": maximum_lane_regression <= rule["maximum_pass_regression_per_lane"], "observed": maximum_lane_regression},
        {"name": "non_code_outputs", "passed": candidate_non_code - base_non_code <= rule["maximum_increase_in_non_code_outputs"], "observed_increase": candidate_non_code - base_non_code},
        {"name": "truncated_outputs", "passed": candidate_truncated - base_truncated <= rule["maximum_increase_in_truncated_outputs"], "observed_increase": candidate_truncated - base_truncated},
    ]
    failed = [check["name"] for check in checks if not check["passed"]]
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-expansion-canary-adjudication/v1",
        "status": "promote-to-full-development" if not failed else "do-not-promote",
        "card_sha256": card["card_sha256"],
        "terminal_report_sha256": terminal["report_sha256"],
        "rule": rule,
        "task_count": len(candidate),
        "base_passes_by_lane": dict(lane_base),
        "candidate_passes_by_lane": dict(lane_candidate),
        "base_passes_by_family": dict(family_base),
        "candidate_passes_by_family": dict(family_candidate),
        "checks": checks,
        "failed_checks": failed,
        "candidate_task_evidence": {task_id: row["evidence_sha256"] for task_id, row in sorted(candidate.items())},
    }
    report["report_sha256"] = canonical_digest(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--card", type=Path, required=True)
    parser.add_argument("--terminal", type=Path, required=True)
    parser.add_argument("--base-tasks", type=Path, required=True)
    parser.add_argument("--candidate-tasks", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = adjudicate(args.card, args.terminal, args.base_tasks, args.candidate_tasks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "failed_checks": report["failed_checks"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "promote-to-full-development" else 2


if __name__ == "__main__":
    raise SystemExit(main())
