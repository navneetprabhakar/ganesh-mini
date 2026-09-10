#!/usr/bin/env python3
"""Fail-closed local preparation for the one-recipe Gate 4 expansion pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SHA256 = 64


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def resolve(root: Path, value: str) -> Path:
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("configured path escapes repository root")
    return path


def checked_file(root: Path, path: str, expected: str) -> dict[str, Any]:
    target = resolve(root, path)
    observed = digest(target) if target.is_file() else None
    return {"path": path, "expected_sha256": expected, "observed_sha256": observed, "passed": observed == expected}


def build_card(config_path: Path, root: Path = ROOT, system: str | None = None) -> dict[str, Any]:
    config = json.loads(config_path.read_text())
    data, model, recipe, control = config["data"], config["model"], config["recipe"], config["control"]
    schema = config.get("schema_version")
    checks = [
        {"name": "linux_cuda_contract", "passed": (system or platform.system()) == "Linux" and recipe["host_os"] == "Linux" and recipe["accelerator"] == "CUDA"},
        {"name": "model_contract", **checked_file(root, model["contract_path"], model["contract_sha256"])},
        {"name": "prepared_manifest_file", **checked_file(root, data["prepared_manifest_path"], data["prepared_manifest_file_sha256"])},
        {"name": "prepared_train_file", **checked_file(root, data["prepared_train_path"], data["prepared_train_sha256"])},
        {"name": "prepared_validation_file", **checked_file(root, data["prepared_validation_path"], data["prepared_validation_sha256"])},
        {"name": "throughput_evidence", **checked_file(root, config["throughput"]["evidence_path"], config["throughput"]["evidence_sha256"])},
    ]
    if schema in {"ganesh-mini-expansion-pilot-config/v3", "ganesh-mini-expansion-pilot-config/v4"}:
        checks.append({"name": "source_prepared_train_file", **checked_file(root, data["source_prepared_train_path"], data["source_prepared_train_sha256"])})
    manifest = json.loads(resolve(root, data["prepared_manifest_path"]).read_text())
    claimed = manifest.pop("manifest_sha256", None)
    manifest_seal_ok = claimed == canonical_digest(manifest) == data["prepared_manifest_sha256"]
    checks.append({"name": "prepared_manifest_seal", "passed": manifest_seal_ok})
    prepared = manifest.get("prepared_train", {})
    prefix_balance_ok = True
    if schema == "ganesh-mini-expansion-pilot-config/v1":
        identity_ok = prepared.get("records") == data["records"] == 3225 and prepared.get("input_tokens") == data["input_tokens"] == control["maximum_seen_tokens"] == 2438853
    elif schema == "ganesh-mini-expansion-pilot-config/v2":
        rows = [json.loads(line) for line in resolve(root, data["prepared_train_path"]).read_text().splitlines() if line]
        prefix = rows[:data["records"]]
        prefix_tokens = sum(sum(row["attention_mask"]) for row in prefix)
        identity_ok = (
            prepared.get("records") == data["source_records"] == len(rows) == 3225
            and prepared.get("input_tokens") == data["source_input_tokens"] == 2438853
            and len(prefix) == data["records"] == 624
            and prefix_tokens == data["input_tokens"] == control["maximum_seen_tokens"] == 468601
        )
        family_mass = {family: 0.0 for family in ("go", "java", "javascript_typescript", "python", "rust")}
        for row in prefix:
            family = "javascript_typescript" if row["lane"] in {"javascript", "typescript"} else row["lane"]
            family_mass[family] += float(row["objective_weight"])
        total_mass = sum(family_mass.values())
        observed_shares = {family: round(mass / total_mass, 4) for family, mass in family_mass.items()}
        prefix_balance_ok = max(abs(share - 0.2) for share in observed_shares.values()) <= 0.02 and observed_shares == config.get("hypothesis", {}).get("prefix_objective_shares")
    elif schema in {"ganesh-mini-expansion-pilot-config/v3", "ganesh-mini-expansion-pilot-config/v4"}:
        rows = [json.loads(line) for line in resolve(root, data["prepared_train_path"]).read_text().splitlines() if line]
        retention = [json.loads(line) for line in resolve(root, data["prepared_validation_path"]).read_text().splitlines() if line]
        accumulation = recipe["gradient_accumulation_steps"]
        expected_counts = {"go": 2, "java": 2, "javascript": 1, "typescript": 1, "python": 2, "rust": 2}
        expected_mass = {"go": 0.2, "java": 0.2, "javascript": 0.1, "typescript": 0.1, "python": 0.2, "rust": 0.2}
        train_ids = {row["source_id"] for row in rows}
        retention_ids = {row["source_id"] for row in retention}
        groups_ok = len(rows) % accumulation == 0
        for start in range(0, len(rows), accumulation):
            group = rows[start:start + accumulation]
            counts = {lane: sum(row["lane"] == lane for row in group) for lane in expected_counts}
            mass = {lane: sum(float(row["objective_weight"]) for row in group if row["lane"] == lane) for lane in expected_mass}
            groups_ok = groups_ok and counts == expected_counts and all(abs(mass[lane] - expected_mass[lane]) <= 1e-12 for lane in expected_mass)
        identity_ok = (
            manifest.get("schema_version") == "ganesh-mini-lane-stratified-probe-data/v1"
            and manifest.get("source", {}).get("records") == data["source_records"] == 3225
            and manifest.get("source", {}).get("sha256") == data["source_prepared_train_sha256"]
            and prepared.get("records") == data["records"] == len(rows) == 640
            and prepared.get("input_tokens") == data["input_tokens"] == control["maximum_seen_tokens"] == 466614
            and manifest.get("prepared_validation", {}).get("records") == data["retention_records"] == len(retention) == 60
            and manifest.get("prepared_validation", {}).get("disjoint_from_training") is True
            and len(train_ids) == len(rows) and len(retention_ids) == len(retention) and not train_ids & retention_ids
        )
        prefix_balance_ok = groups_ok and all(manifest.get("group_contract", {}).get(key) is True for key in (
            "every_group_contains_all_six_lanes", "every_group_matches_record_target", "every_group_matches_objective_target"
        ))
    else:
        identity_ok = False
    identity_ok = identity_ok and (schema in {"ganesh-mini-expansion-pilot-config/v3", "ganesh-mini-expansion-pilot-config/v4"} or manifest.get("revision") == model["revision"]) and manifest.get("status") == "ready"
    checks.append({"name": "corpus_and_model_identity", "passed": identity_ok})
    checks.append({"name": "prefix_objective_balance", "passed": prefix_balance_ok})
    is_v1 = schema == "ganesh-mini-expansion-pilot-config/v1"
    is_v3 = schema == "ganesh-mini-expansion-pilot-config/v3"
    is_v4 = schema == "ganesh-mini-expansion-pilot-config/v4"
    lane_grouped = is_v3 or is_v4
    expected_recipe = "bf16-lora-expansion-pilot-v1" if is_v1 else "bf16-lora-lane-stratified-probe-v3" if is_v3 else "bf16-lora-gradient-conflict-pcgrad-v4" if is_v4 else "bf16-lora-capacity-probe-v2"
    recipe_ok = (
        recipe.get("recipe_id") == expected_recipe
        and recipe.get("learning_rate") == 0.00001
        and recipe.get("base_loading") == "bfloat16"
        and recipe.get("sequence_length") == 2944
        and recipe.get("micro_batch_size") == 1
        and recipe.get("gradient_accumulation_steps") == (10 if lane_grouped else 8)
        and recipe.get("effective_batch_size") == (10 if lane_grouped else 8)
        and recipe.get("maximum_effective_epochs") == (1.0 if is_v1 else 0.19845 if lane_grouped else 0.193488)
        and recipe.get("maximum_peak_vram_gb") == 23
    )
    if schema in {"ganesh-mini-expansion-pilot-config/v2", "ganesh-mini-expansion-pilot-config/v3", "ganesh-mini-expansion-pilot-config/v4"}:
        recipe_ok = recipe_ok and recipe.get("lora_rank") == 16 and recipe.get("lora_alpha") == 32 and recipe.get("target_policy") == {
            "scope": "all-attention-plus-last-n-mlp",
            "model_layer_count": 24,
            "layer_count": 8,
            "full_attention_projections": ["q_proj", "v_proj"],
            "linear_attention_projections": ["in_proj_qkv", "out_proj"],
            "mlp_projections": ["gate_proj", "up_proj", "down_proj"],
        }
    checks.append({"name": "single_bounded_recipe", "passed": recipe_ok})
    if is_v4:
        recipe_ok = recipe_ok and recipe.get("gradient_conflict") == {
            "stage_1": {
                "optimizer_steps": 0,
                "selected_optimizer_groups": [0, 9, 18, 27, 36, 45, 54, 63],
                "negative_cosine_threshold": -0.05,
                "minimum_groups_with_negative_pair": 4,
                "minimum_javascript_or_typescript_groups": 4,
            },
            "stage_2": {
                "conditional_on_stage_1": True,
                "algorithm": "pcgrad",
                "lane_gradient": "response-token-weighted-mean",
                "lane_weights": {"go": 0.2, "java": 0.2, "javascript": 0.1, "typescript": 0.1, "python": 0.2, "rust": 0.2},
                "projection_order": "seeded-cyclic-rotation",
                "projection_seed": 3502,
            },
        }
    retention_guard_ok = True
    if lane_grouped:
        retention_guard_ok = config.get("evaluation", {}).get("retention_loss_guard") == {
            "surface": "60 disjoint authorized training-corpus holdout rows; 10 per lane",
            "metric": "supervised_token_mean_loss",
            "maximum_relative_loss_increase_per_lane": 0.05,
            "maximum_relative_five_family_macro_loss_increase": 0.0,
        }
    checks.append({"name": "non_evaluation_retention_contract", "passed": retention_guard_ok})
    quarter = control.get("checkpoint_tokens")
    expected_checkpoints = 4 if is_v1 else 6
    bounds_ok = (
        control.get("maximum_wall_seconds") == (21600 if is_v1 else 7200)
        and control.get("finalization_reserve_seconds") == 1800
        and isinstance(quarter, list) and len(quarter) == expected_checkpoints
        and quarter[-1] == control["maximum_seen_tokens"]
        and all(0 < value <= control["maximum_seen_tokens"] for value in quarter)
    )
    checks.append({"name": "runtime_and_checkpoint_bounds", "passed": bounds_ok})
    promotion = config.get("evaluation", {}).get("promotion_rule")
    expected_rule = {
        "rule_id": "expansion-pilot-canary-promotion-v1" if is_v1 else "lane-stratified-probe-continuation-v3" if is_v3 else "gradient-conflict-probe-continuation-v4" if is_v4 else "capacity-probe-continuation-v2",
        "minimum_improved_product_families": 4 if is_v1 else 2,
        "minimum_net_pass_gain": 1 if is_v1 else 2,
        "maximum_pass_regression_per_lane": 0,
        "maximum_increase_in_non_code_outputs": 0,
        "maximum_increase_in_truncated_outputs": 0,
        "save_reload_required": True,
    }
    promotion_ok = promotion == expected_rule
    checks.append({"name": "frozen_canary_promotion_rule", "passed": promotion_ok})
    failed = [item["name"] for item in checks if not item["passed"]]
    card: dict[str, Any] = {
        "schema_version": "ganesh-mini-expansion-pilot-card/v1" if is_v1 else "ganesh-mini-expansion-pilot-card/v3" if is_v3 else "ganesh-mini-expansion-pilot-card/v4" if is_v4 else "ganesh-mini-expansion-pilot-card/v2",
        "status": "prepared-not-executable" if not failed else "not-ready",
        "reason": "provider_price_and_explicit_gcloud_execution_approval_not_bound" if not failed else "local_preflight_failed",
        "run_id": config["run_id"],
        "config": {"path": str(config_path.relative_to(root)), "sha256": digest(config_path)},
        "model": model,
        "inputs": {
            "config_sha256": digest(config_path),
            "prepared_manifest_sha256": data["prepared_manifest_sha256"],
            "prepared_data_sha256": data["prepared_train_sha256"],
            "validation_data_sha256": data["prepared_validation_sha256"],
        },
        "data": data,
        "selected_recipe": recipe,
        "control": control,
        "evaluation": config["evaluation"],
        "throughput": config["throughput"],
        "provider_execution": None,
        "checks": checks,
        "failed_checks": failed,
    }
    card["card_sha256"] = canonical_digest(card)
    return card


def bind_provider(local_card: dict[str, Any], provider: dict[str, Any]) -> dict[str, Any]:
    """Convert a locally sealed card into an executable card after approval."""
    unsigned = dict(local_card)
    claimed = unsigned.pop("card_sha256", None)
    if claimed != canonical_digest(unsigned) or local_card.get("status") != "prepared-not-executable" or local_card.get("failed_checks"):
        raise ValueError("provider binding requires an intact prepared local card")
    required = {"provider", "project", "zone", "machine_type", "accelerator", "hourly_cost_usd", "prior_cost_usd", "cost_ceiling_usd", "price_evidence_sha256", "approval_evidence_sha256"}
    if set(provider) != required:
        raise ValueError("provider binding fields are incomplete or unexpected")
    if provider["provider"] != "gcloud" or provider["accelerator"] != "NVIDIA_L4" or not all(isinstance(provider[key], str) and provider[key] for key in ("project", "zone", "machine_type")):
        raise ValueError("provider identity is invalid")
    if not all(isinstance(provider[key], (int, float)) for key in ("hourly_cost_usd", "prior_cost_usd", "cost_ceiling_usd")):
        raise ValueError("provider cost values must be numeric")
    if not 0 < provider["hourly_cost_usd"] or not 0 <= provider["prior_cost_usd"] < provider["cost_ceiling_usd"]:
        raise ValueError("provider cost envelope is invalid")
    if any(not isinstance(provider[key], str) or len(provider[key]) != SHA256 for key in ("price_evidence_sha256", "approval_evidence_sha256")):
        raise ValueError("provider evidence hashes are invalid")
    card = dict(unsigned)
    card["status"] = "ready"
    card["reason"] = "provider_price_and_explicit_approval_bound"
    card["provider_execution"] = provider
    card["card_sha256"] = canonical_digest(card)
    return card


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/train/expansion_pilot_v1.json")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/train/expansion-pilot-v1/local-execution-card.json")
    parser.add_argument("--system", default=None)
    parser.add_argument("--provider-binding", type=Path)
    args = parser.parse_args()
    card = build_card(args.config.resolve(), ROOT, args.system)
    if args.provider_binding:
        card = bind_provider(card, json.loads(args.provider_binding.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(card, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": card["status"], "failed_checks": card["failed_checks"], "card_sha256": card["card_sha256"]}, sort_keys=True))
    return 0 if not card["failed_checks"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
