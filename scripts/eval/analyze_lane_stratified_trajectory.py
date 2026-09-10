#!/usr/bin/env python3
"""Build a sealed task-level trajectory audit for the Gate 4 v3 checkpoint sweep."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.campaign.run_checkpoint_sweep_host import verify_result_tasks
from scripts.campaign.run_host import atomic_json, canonical_sha256, load_sealed
from scripts.eval.analyze_checkpoint_trajectory import FAMILIES, counts, load_tasks


def transition(before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    gains = []
    losses = []
    for task_id in sorted(before):
        was_pass = before[task_id]["verification"]["result"]["passed"]
        is_pass = after[task_id]["verification"]["result"]["passed"]
        if not was_pass and is_pass:
            gains.append(task_id)
        elif was_pass and not is_pass:
            losses.append(task_id)
    return {"gains": gains, "losses": losses}


def archetype(task_id: str, language: str) -> str:
    prefix = f"dev-t1-{language}-"
    if not task_id.startswith(prefix):
        raise ValueError(f"unexpected task identity: {task_id}")
    return task_id.removeprefix(prefix)


def candidate_point(
    label: str,
    tasks: dict[str, dict[str, Any]],
    base: dict[str, dict[str, Any]],
    *,
    run_sha256: str,
    seen_tokens: int,
) -> dict[str, Any]:
    lane_passes, family_passes = counts(tasks)
    base_lanes, base_families = counts(base)
    paired = transition(base, tasks)
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
        "gains_vs_base": paired["gains"],
        "losses_vs_base": paired["losses"],
        "changed_extracted_code_vs_base": sum(
            tasks[task_id]["extraction"]["extracted_code_sha256"]
            != base[task_id]["extraction"]["extracted_code_sha256"]
            for task_id in tasks
        ),
        "zero_lane_regression_vs_base": all(lane_passes[lane] >= base_lanes[lane] for lane in base_lanes),
        "run_sha256": run_sha256,
    }


def analyze(
    base_dir: Path,
    checkpoint_root: Path,
    final_dir: Path,
    final_run_path: Path,
    *,
    final_seen_tokens: int,
) -> dict[str, Any]:
    base = load_tasks(base_dir)
    final = load_tasks(final_dir)
    selected_ids = set(final)
    if len(selected_ids) != 30 or not selected_ids <= set(base):
        raise ValueError("base and final evidence must cover the same 30 frozen tasks")
    base = {task_id: base[task_id] for task_id in selected_ids}

    series: list[tuple[str, int, str, dict[str, dict[str, Any]]]] = []
    for directory in sorted(checkpoint_root.glob("tokens-*")):
        run = load_sealed(directory / "run.json", "run_sha256")
        verify_result_tasks(directory, run)
        tasks = load_tasks(directory / "tasks")
        if set(tasks) != selected_ids:
            raise ValueError(f"checkpoint task set mismatch: {directory.name}")
        series.append((directory.name, int(directory.name.removeprefix("tokens-")), run["run_sha256"], tasks))
    if not series:
        raise ValueError("no checkpoint evidence found")

    final_run = load_sealed(final_run_path, "run_sha256")
    verify_result_tasks(final_dir.parent, final_run)
    if final_run.get("task_accounting", {}).get("completed") != 30:
        raise ValueError("final canary is incomplete")
    series.append((f"tokens-{final_seen_tokens:012d}", final_seen_tokens, final_run["run_sha256"], final))

    named_points = [("base", base), *((label, tasks) for label, _, _, tasks in series)]
    adjacent = []
    for (before_label, before), (after_label, after) in zip(named_points, named_points[1:]):
        adjacent.append({"before": before_label, "after": after_label, **transition(before, after)})

    task_rows = []
    for task_id in sorted(selected_ids):
        values = [tasks[task_id] for _, tasks in named_points]
        pattern = "".join("P" if value["verification"]["result"]["passed"] else "F" for value in values)
        language = values[0]["task"]["language"]
        task_rows.append({
            "task_id": task_id,
            "language": language,
            "archetype": archetype(task_id, language),
            "pass_pattern": pattern,
            "unique_extracted_code_count": len({value["extraction"]["extracted_code_sha256"] for value in values}),
        })

    base_lanes, base_families = counts(base)
    candidate_points = [
        candidate_point(label, tasks, base, run_sha256=run_sha256, seen_tokens=seen_tokens)
        for label, seen_tokens, run_sha256, tasks in series
    ]
    for candidate in candidate_points:
        candidate["continuation_rule_passed"] = (
            candidate["passed"] >= sum(base_lanes.values()) + 2
            and len(candidate["improved_families_vs_base"]) >= 2
            and candidate["zero_lane_regression_vs_base"]
        )

    changing = [row for row in task_rows if len(set(row["pass_pattern"])) > 1]
    changing_archetypes = Counter(row["archetype"] for row in changing)
    pattern_counts = Counter(row["pass_pattern"] for row in task_rows)
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-lane-stratified-checkpoint-trajectory/v1",
        "status": "complete-do-not-promote",
        "classification": "private-development-aggregate",
        "task_count": 30,
        "point_labels": [label for label, _ in named_points],
        "base": {"passed": sum(base_lanes.values()), "lane_passes": base_lanes, "family_passes": base_families},
        "candidate_points": candidate_points,
        "adjacent_transitions": adjacent,
        "task_trajectories": task_rows,
        "trajectory_summary": {
            "pass_pattern_counts": dict(sorted(pattern_counts.items())),
            "stable_pass_tasks": sum(set(row["pass_pattern"]) == {"P"} for row in task_rows),
            "stable_fail_tasks": sum(set(row["pass_pattern"]) == {"F"} for row in task_rows),
            "ever_passed_tasks": sum("P" in row["pass_pattern"] for row in task_rows),
            "status_changing_tasks": len(changing),
            "status_changing_archetypes": dict(sorted(changing_archetypes.items())),
        },
        "conclusion": {
            "any_checkpoint_passed_continuation_rule": any(row["continuation_rule_passed"] for row in candidate_points),
            "early_stopping_supported": False,
            "observed_failure_shape": "persistent broad failure plus late cross-lane pass oscillation",
            "next_mechanism_class": "lane-isolated specialist adapters followed by measured delta combination",
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
    parser.add_argument("--final-seen-tokens", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = analyze(
        args.base_tasks,
        args.checkpoint_results,
        args.final_tasks,
        args.final_run,
        final_seen_tokens=args.final_seen_tokens,
    )
    atomic_json(args.output, report)
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
