#!/usr/bin/env python3
"""Build the deterministic Gate 4 v4 gradient-conflict probe configuration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.train.gradient_conflict import evenly_spaced_group_indices


ROOT = Path(__file__).resolve().parents[2]
LANE_WEIGHTS = {"go": 0.2, "java": 0.2, "javascript": 0.1, "typescript": 0.1, "python": 0.2, "rust": 0.2}


def build(source: dict[str, Any]) -> dict[str, Any]:
    if (
        source.get("schema_version") != "ganesh-mini-expansion-pilot-config/v3"
        or source.get("recipe", {}).get("recipe_id") != "bf16-lora-lane-stratified-probe-v3"
        or source.get("data", {}).get("records") != 640
        or source.get("recipe", {}).get("gradient_accumulation_steps") != 10
        or source.get("control", {}).get("maximum_seen_tokens") != 466614
    ):
        raise ValueError("source must be the exact v3 lane-stratified configuration")
    config = json.loads(json.dumps(source))
    config["schema_version"] = "ganesh-mini-expansion-pilot-config/v4"
    config["run_id"] = "ganesh-mini-1.0-gradient-conflict-probe-v4"
    config["recipe"]["recipe_id"] = "bf16-lora-gradient-conflict-pcgrad-v4"
    config["recipe"]["gradient_conflict"] = {
        "stage_1": {
            "optimizer_steps": 0,
            "selected_optimizer_groups": evenly_spaced_group_indices(64, 8),
            "negative_cosine_threshold": -0.05,
            "minimum_groups_with_negative_pair": 4,
            "minimum_javascript_or_typescript_groups": 4,
        },
        "stage_2": {
            "conditional_on_stage_1": True,
            "algorithm": "pcgrad",
            "lane_gradient": "response-token-weighted-mean",
            "lane_weights": LANE_WEIGHTS,
            "projection_order": "seeded-cyclic-rotation",
            "projection_seed": 3502,
        },
    }
    config["evaluation"]["promotion_rule"]["rule_id"] = "gradient-conflict-probe-continuation-v4"
    config["evaluation"]["authority"] = (
        "conditional gradient audit plus continuation-screen-only; retention guard must pass; "
        "no checkpoint promotion, full-development evaluation, decision-set opening, merge, quantization, or publication"
    )
    config["throughput"] = {
        **config["throughput"],
        "expected_training_seconds": 1895,
        "conservative_training_seconds": 2700,
        "stage_1_audit_conservative_seconds": 360,
        "basis": "v3 measured throughput plus eight extra backward-only groups and deterministic LoRA-gradient projection overhead",
    }
    config["hypothesis"] = {
        "observation": "exact six-lane objective mass still produced late cross-lane pass oscillation and no promotable checkpoint",
        "uncertainty": "the checkpoint trajectory does not by itself prove gradient conflict; insufficient task-pattern coverage remains plausible",
        "stage_1": "measure all 15 pairwise LoRA-gradient cosines on fixed optimizer groups 0,9,18,27,36,45,54,63 without optimizer steps",
        "stage_2": "only if the frozen conflict threshold passes, project negative per-lane LoRA gradients with deterministic PCGrad before weighted aggregation",
        "early_stop": "stop without training if stage 1 fails; otherwise stop after the same 640-row probe unless retention and canary rules both pass",
    }
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "configs/train/expansion_lane_stratified_probe_v3.json")
    parser.add_argument("--output", type=Path, default=ROOT / "configs/train/gradient_conflict_probe_v4.json")
    args = parser.parse_args()
    config = build(json.loads(args.source.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "built-local-not-executable", "output": str(args.output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
