#!/usr/bin/env python3
"""Build a sealed aggregate trajectory report from private canary evidence."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.campaign.run_checkpoint_sweep_host import verify_result_tasks
from scripts.campaign.run_host import atomic_json, canonical_sha256, load_sealed


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
FAMILIES = {
    "go": ("go",),
    "java": ("java",),
    "javascript_typescript": ("javascript", "typescript"),
    "python": ("python",),
    "rust": ("rust",),
}


def load_tasks(directory: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.glob("*.json")):
        value = load_sealed(path, "evidence_sha256")
        task_id = value.get("task", {}).get("task_id")
        if not isinstance(task_id, str) or task_id in result:
            raise ValueError(f"invalid or duplicate task evidence: {path}")
        result[task_id] = value
    return result


def outcome(value: dict[str, Any]) -> str:
    verification = value["verification"]["result"]
    if verification["passed"]:
        return "passed"
    verifier = verification["verifier"]
    if verifier.get("timed_out"):
        return "verifier-timeout"
    exit_codes = verifier.get("exit_codes", [])
    if not exit_codes:
        return "missing-execution"
    if exit_codes[0] != 0:
        return "compile-or-load-failure"
    return "behavioral-test-failure"


def counts(tasks: dict[str, dict[str, Any]]) -> tuple[dict[str, int], dict[str, int]]:
    lanes = {lane: 0 for lane in LANES}
    for value in tasks.values():
        if value["verification"]["result"]["passed"]:
            lanes[value["task"]["language"]] += 1
    families = {
        family: sum(lanes[lane] for lane in family_lanes)
        for family, family_lanes in FAMILIES.items()
    }
    return lanes, families


def point(
    label: str,
    tasks: dict[str, dict[str, Any]],
    base: dict[str, dict[str, Any]],
    *,
    run_sha256: str,
    seen_tokens: int,
) -> dict[str, Any]:
    lane_passes, family_passes = counts(tasks)
    _, base_families = counts(base)
    transitions = Counter()
    categories = Counter()
    changed_code = 0
    for task_id, value in tasks.items():
        before = base[task_id]["verification"]["result"]["passed"]
        after = value["verification"]["result"]["passed"]
        transitions[f"{'pass' if before else 'fail'}_to_{'pass' if after else 'fail'}"] += 1
        categories[outcome(value)] += 1
        if value["extraction"]["extracted_code_sha256"] != base[task_id]["extraction"]["extracted_code_sha256"]:
            changed_code += 1
    return {
        "label": label,
        "seen_tokens": seen_tokens,
        "passed": sum(lane_passes.values()),
        "lane_passes": lane_passes,
        "family_passes": family_passes,
        "improved_families_vs_base": sorted(
            family for family in FAMILIES if family_passes[family] > base_families[family]
        ),
        "regressed_families_vs_base": sorted(
            family for family in FAMILIES if family_passes[family] < base_families[family]
        ),
        "task_transitions_vs_base": dict(sorted(transitions.items())),
        "failure_categories": dict(sorted(categories.items())),
        "changed_extracted_code_vs_base": changed_code,
        "run_sha256": run_sha256,
    }


def analyze(base_dir: Path, checkpoint_root: Path, final_dir: Path, final_run_path: Path) -> dict[str, Any]:
    base = load_tasks(base_dir)
    final = load_tasks(final_dir)
    if len(base) < 30 or set(final) - set(base):
        raise ValueError("base evidence does not cover the final canary")
    selected_ids = set(final)
    base = {task_id: base[task_id] for task_id in selected_ids}
    if len(base) != 30:
        raise ValueError("trajectory requires exactly 30 frozen canary tasks")

    series: list[tuple[str, int, str, dict[str, dict[str, Any]]]] = []
    for directory in sorted(checkpoint_root.glob("tokens-*")):
        run = load_sealed(directory / "run.json", "run_sha256")
        verify_result_tasks(directory, run)
        tasks = load_tasks(directory / "tasks")
        if set(tasks) != selected_ids:
            raise ValueError(f"checkpoint task set mismatch: {directory.name}")
        series.append((directory.name, int(directory.name.removeprefix("tokens-")), run["run_sha256"], tasks))

    final_run = load_sealed(final_run_path, "run_sha256")
    verify_result_tasks(final_dir.parent, final_run)
    if final_run.get("task_accounting", {}).get("completed") != 30:
        raise ValueError("final canary is incomplete")
    series.append(("final", 2_438_853, final_run["run_sha256"], final))

    base_lanes, base_families = counts(base)
    task_rows = []
    for task_id in sorted(selected_ids):
        values = [base[task_id], *(tasks[task_id] for *_, tasks in series)]
        pass_pattern = "".join("P" if value["verification"]["result"]["passed"] else "F" for value in values)
        task_rows.append({
            "task_id": task_id,
            "language": values[0]["task"]["language"],
            "pass_pattern": pass_pattern,
            "outcome_pattern": [outcome(value) for value in values],
            "unique_extracted_code_count": len({value["extraction"]["extracted_code_sha256"] for value in values}),
            "final_code_changed_vs_base": values[-1]["extraction"]["extracted_code_sha256"] != values[0]["extraction"]["extracted_code_sha256"],
        })

    pattern_counts = Counter(row["pass_pattern"] for row in task_rows)
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-checkpoint-trajectory/v1",
        "status": "complete-partial-sweep-analysis",
        "classification": "private-development-aggregate",
        "task_count": 30,
        "base": {
            "passed": sum(base_lanes.values()),
            "lane_passes": base_lanes,
            "family_passes": base_families,
        },
        "candidate_points": [
            point(label, tasks, base, run_sha256=run_sha256, seen_tokens=seen_tokens)
            for label, seen_tokens, run_sha256, tasks in series
        ],
        "task_trajectories": task_rows,
        "trajectory_summary": {
            "pass_pattern_counts": dict(sorted(pattern_counts.items())),
            "stable_pass_tasks": sum(row["pass_pattern"] == "P" * len(row["pass_pattern"]) for row in task_rows),
            "stable_fail_tasks": sum(row["pass_pattern"] == "F" * len(row["pass_pattern"]) for row in task_rows),
            "ever_passed_tasks": sum("P" in row["pass_pattern"] for row in task_rows),
            "status_changing_tasks": sum(len(set(row["pass_pattern"])) > 1 for row in task_rows),
        },
        "incomplete_checkpoint": {
            "label": "tokens-000002036559",
            "included": False,
            "reason": "no task or run evidence; score must not be reconstructed",
        },
        "conclusion": {
            "early_stopping_supported": False,
            "broad_multilingual_transfer_observed": False,
            "next_mechanism": "change adapter capacity or target scope under a separately bounded pilot",
            "promotion_authority": "none",
        },
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-tasks", type=Path, required=True)
    parser.add_argument("--checkpoint-results", type=Path, required=True)
    parser.add_argument("--final-tasks", type=Path, required=True)
    parser.add_argument("--final-run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = analyze(args.base_tasks, args.checkpoint_results, args.final_tasks, args.final_run)
    atomic_json(args.output, report)
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
