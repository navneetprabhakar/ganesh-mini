#!/usr/bin/env python3
"""Seal the local, non-executable Gate 4 gradient-conflict mechanism plan."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
LANES = ("go", "java", "javascript", "typescript", "python", "rust")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_sealed(path: Path, key: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(key, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {key}: {path}")
    value[key] = claimed
    return value


def build(trajectory_path: Path) -> dict[str, Any]:
    trajectory = load_sealed(trajectory_path, "report_sha256")
    summary = trajectory["trajectory_summary"]
    if (
        trajectory.get("schema_version") != "ganesh-mini-lane-stratified-checkpoint-trajectory/v1"
        or trajectory.get("status") != "complete-do-not-promote"
        or summary.get("stable_fail_tasks") != 21
        or summary.get("status_changing_tasks") != 8
        or trajectory.get("conclusion", {}).get("any_checkpoint_passed_continuation_rule") is not False
    ):
        raise ValueError("trajectory evidence does not support this mechanism plan")

    plan: dict[str, Any] = {
        "schema_version": "ganesh-mini-gradient-conflict-mechanism-plan/v1",
        "status": "local-design-only-not-executable",
        "gate": 4,
        "source_evidence": {
            "trajectory_path": str(trajectory_path.relative_to(ROOT)),
            "trajectory_report_sha256": trajectory["report_sha256"],
            "stable_fail_tasks": 21,
            "status_changing_tasks": 8,
            "dominant_changing_archetype": "collapse-runs",
            "dominant_changing_archetype_count": 5,
        },
        "hypothesis": {
            "claim": "Exact lane objective mass did not prevent opposing LoRA update directions between lanes.",
            "uncertainty": "The executable trajectory alone does not prove gradient conflict; weak task-pattern coverage remains a competing explanation.",
        },
        "stage_1_gradient_audit": {
            "optimizer_steps": 0,
            "training_rows": 0,
            "source_rows_used_for_backward_only_measurement": 80,
            "optimizer_groups": 8,
            "group_selection": "fixed evenly spaced groups from the sealed v3 64-group dataset",
            "lanes": list(LANES),
            "pair_count_per_group": 15,
            "gradient_scope": "trainable LoRA parameters only",
            "lane_gradient": "response-token-weighted mean within lane before applying lane objective mass",
            "recorded_metrics": [
                "per-lane gradient norm",
                "all 15 pairwise cosine similarities per group",
                "negative-pair count and lane participation",
            ],
            "conflict_threshold": {
                "negative_cosine_threshold": -0.05,
                "minimum_groups_with_any_negative_pair": 4,
                "minimum_javascript_or_typescript_negative_participation_groups": 4,
            },
            "continuation": "run stage 2 only when every conflict threshold is met; otherwise stop and return to corpus/task-diversity work",
        },
        "stage_2_conditional_probe": {
            "mechanism": "deterministic PCGrad over six unweighted lane-mean LoRA gradients, followed by 20/20/10/10/20/20 weighted aggregation",
            "data": "same 640 unique training rows and same 60 disjoint retention rows as v3",
            "capacity": "same rank-16 target scope as v3",
            "learning_rate": "same 1e-5 as v3",
            "maximum_seen_tokens": 466614,
            "projection_order": "seeded deterministic rotation recorded for every optimizer group",
            "evaluation": "same frozen 30-task continuation screen only after retention and save/reload pass",
            "continuation_rule": {
                "minimum_improved_product_families": 2,
                "minimum_net_pass_gain": 2,
                "maximum_pass_regression_per_lane": 0,
            },
        },
        "hard_stops": [
            "stage-1 conflict threshold not met",
            "non-finite gradient or loss",
            "retention guard failure",
            "save/reload mismatch",
            "cost or wall-time bound",
            "frozen continuation rule failure",
        ],
        "forbidden": [
            "evaluation records entering training",
            "full development evaluation",
            "decision-set opening",
            "checkpoint promotion",
            "merge or quantization",
            "publication",
            "any GCloud action without a separately sealed and explicitly approved execution proposal",
        ],
        "gcloud_authority": "none",
        "promotion_authority": "none",
    }
    plan["plan_sha256"] = canonical_sha256(plan)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trajectory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = build(args.trajectory.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": plan["status"], "plan_sha256": plan["plan_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
