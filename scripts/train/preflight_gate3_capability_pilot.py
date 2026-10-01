#!/usr/bin/env python3
"""Static Gate 3 pilot identity check; never creates a runnable execution card."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGETS = {"go": .2, "java": .2, "javascript": .1, "typescript": .1, "python": .2, "rust": .2}
EXPECTED = {
    "model_revision": "15852e8c16360a2fea060d615a32b45270f8a8fc",
    "package_seal": "149b030f11bc0eb054f0a4d511432f33b4123e3b65fab77c2166dca23d1190aa",
    "prepared_manifest": "4bae0de2096ce8ae973d0f7b3ecc9214d8b6ef2e3addfb31cc4afd37446c2d01",
    "prepared_train": "6f43f373c34fd61749b44ef73eb8803f9f0df33ad13b2358ee6efde95fe5fa1f",
    "prepared_validation": "6a9d3aa37b30bc2672517f6d63113011de5f8156aa1049e588fdc70a36b77f46",
}


def canonical_sha(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve(root: Path, value: str) -> Path:
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("configured path escaped repository")
    return path


def sealed(path: Path, field: str) -> dict:
    record = json.loads(path.read_text(encoding="utf-8"))
    claimed = record.pop(field, None)
    if claimed != canonical_sha(record):
        raise ValueError(f"invalid {field}: {path}")
    record[field] = claimed
    return record


def verify_model_inventory(model_dir: Path, inventory_path: Path) -> dict:
    """Stream-check the exact pinned upstream files before any model load."""
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if (inventory.get("model_id") != "Qwen/Qwen3.5-2B" or
        inventory.get("revision") != EXPECTED["model_revision"] or
        not isinstance(inventory.get("files"), list)):
        raise ValueError("model inventory identity differs")
    expected_names = {item["path"] for item in inventory["files"]}
    actual_names = {item.name for item in model_dir.iterdir() if item.is_file()}
    if actual_names != expected_names:
        raise ValueError("model directory file inventory differs")
    for item in inventory["files"]:
        path = model_dir / item["path"]
        if not path.is_file() or path.stat().st_size != item["size"]:
            raise ValueError(f"model file size differs: {item['path']}")
        lfs_content = bool(item.get("sha256"))
        digest = hashlib.sha256() if lfs_content else hashlib.sha1(f"blob {item['size']}\0".encode("ascii"))
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
                digest.update(chunk)
        expected = item["sha256"] if lfs_content else item["git_oid"]
        if digest.hexdigest() != expected:
            raise ValueError(f"model file identity differs: {item['path']}")
    return {"revision": inventory["revision"], "files_verified": len(inventory["files"]),
            "inventory_file_sha256": file_sha(inventory_path)}


def assess(config_path: Path, root: Path = ROOT) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    data, recipe, model = config["data"], config["recipe"], config["model"]
    if (config.get("schema_version") != "ganesh-mini-capability-pilot-config/v1" or
        model.get("model_id") != "Qwen/Qwen3.5-2B" or
        model.get("revision") != EXPECTED["model_revision"] or
        data.get("records") != 900 or data.get("input_tokens") != 651639 or
        data.get("validation_records") != 50 or
        data.get("package_seal_sha256") != EXPECTED["package_seal"] or
        data.get("prepared_manifest_sha256") != EXPECTED["prepared_manifest"] or
        data.get("prepared_train_sha256") != EXPECTED["prepared_train"] or
        data.get("prepared_validation_sha256") != EXPECTED["prepared_validation"]):
        raise ValueError("pilot config differs from frozen input identities")
    if (recipe.get("host_os") != "Linux" or recipe.get("accelerator") != "CUDA" or
        recipe.get("qualified_seed_recipe_file_sha256") != "344b69e81a28fb8203bf178e96629f2f3ed64ae75c227d4931615077e32bd4e6" or
        recipe.get("minimum_gpu_vram_gb") != 24 or
        recipe.get("maximum_peak_vram_gb") != 23 or
        recipe.get("base_loading") != "bfloat16" or
        recipe.get("compute_dtype") != "bfloat16" or
        recipe.get("sequence_length") != 2944 or recipe.get("packing") is not False or
        recipe.get("lora_rank") != 8 or recipe.get("lora_alpha") != 16 or
        recipe.get("lora_dropout") != .05 or
        recipe.get("target_policy") != "last-8-attention-projections" or
        recipe.get("gradient_accumulation_steps") != 8 or
        recipe.get("learning_rate_candidates") != [1e-5, 3e-5] or
        recipe.get("maximum_effective_epochs") != 1.0 or
        recipe.get("fused_linear_cross_entropy") != "liger-kernel-0.8.2" or
        recipe.get("objective_targets") != TARGETS):
        raise ValueError("pilot recipe differs from frozen conservative mechanism")
    evaluation = config["evaluation"]
    if evaluation != {"canary_tasks": 30, "development_tasks": 180,
                      "decision_tasks_opened": 0, "minimum_improved_product_families": 4,
                      "material_lane_regression_allowed": False,
                      "formatting_or_truncation_increase_allowed": False}:
        raise ValueError("pilot evaluation contract differs")
    model_contract = resolve(root, model["contract_path"])
    if file_sha(model_contract) != model["contract_sha256"]:
        raise ValueError("upstream model contract differs")
    if (model.get("inventory_file_sha256") != "4809435a6bc027b96ea8c170a82540f667fa3f5db74117940ab96ffc4133436b" or
        file_sha(resolve(root, model["inventory_path"])) != model["inventory_file_sha256"]):
        raise ValueError("upstream model inventory contract differs")
    seed_recipe_path = resolve(root, recipe["qualified_seed_recipe_path"])
    if file_sha(seed_recipe_path) != recipe["qualified_seed_recipe_file_sha256"]:
        raise ValueError("qualified seed recipe bytes differ")
    control = config["control"]
    if control != {
        "maximum_seen_tokens": 651639,
        "maximum_wall_seconds": 21600,
        "finalization_reserve_seconds": 1800,
        "checkpoint_every_tokens": 162910,
        "stop_conditions": ["non_finite_loss", "robust_optimizer_group_loss_anomaly",
                            "token_budget_reached", "wall_time_reached",
                            "cost_ceiling_reached", "checkpoint_write_failure",
                            "evidence_write_failure"],
    }:
        raise ValueError("pilot runtime bounds differ")
    package = sealed(resolve(root, data["package_seal_path"]), "report_sha256")
    manifest = sealed(resolve(root, data["prepared_manifest_path"]), "manifest_sha256")
    if (package["report_sha256"] != data["package_seal_sha256"] or
        package.get("status") != "data-package-passed-pilot-pending" or
        package.get("training_executed") is not False or
        manifest["manifest_sha256"] != data["prepared_manifest_sha256"] or
        manifest.get("status") != "prepared-not-trained" or
        manifest.get("data_package_report_sha256") != package["report_sha256"] or
        manifest.get("revision") != model["revision"] or
        manifest.get("prepared_validation_sha256") != data["prepared_validation_sha256"]):
        raise ValueError("package or prepared manifest seal differs")
    train_path = resolve(root, data["prepared_train_path"])
    validation_path = resolve(root, data["prepared_validation_path"])
    if (file_sha(train_path) != data["prepared_train_sha256"] or
        file_sha(validation_path) != data["prepared_validation_sha256"]):
        raise ValueError("prepared file bytes differ")
    rows = [json.loads(line) for line in train_path.read_text(encoding="utf-8").splitlines()]
    validation = [json.loads(line) for line in validation_path.read_text(encoding="utf-8").splitlines()]
    ids = {row["source_id"] for row in rows}
    validation_ids = {row["source_id"] for row in validation}
    tokens = sum(len(row["input_ids"]) for row in rows)
    if (len(rows) != 900 or len(ids) != 900 or len(validation) != 50 or
        len(validation_ids) != 50 or ids & validation_ids or tokens != 651639 or
        any(len(row["input_ids"]) != len(row["labels"]) or
            len(row["input_ids"]) > 2944 or
            row["labels"][:row["prompt_token_count"]] != [-100] * row["prompt_token_count"]
            for row in rows + validation)):
        raise ValueError("prepared row integrity or separation differs")
    mass = {lane: 0.0 for lane in TARGETS}
    for row in rows:
        mass[row["lane"]] += row["objective_weight"]
    total_mass = sum(mass.values())
    if any(abs(mass[lane] / total_mass - target) > 1e-9 for lane, target in TARGETS.items()):
        raise ValueError("five-family objective differs")
    try:
        import torch
        cuda_available = torch.cuda.is_available() and torch.cuda.device_count() == 1
    except ImportError:
        cuda_available = False
    host_qualified = platform.system() == "Linux" and cuda_available
    return {
        "schema_version": "ganesh-mini-capability-pilot-static-preflight/v1",
        "status": "static-inputs-passed-host-and-execution-card-pending",
        "config_sha256": file_sha(config_path),
        "prepared_manifest_sha256": manifest["manifest_sha256"],
        "records": len(rows),
        "input_tokens": tokens,
        "validation_records": len(validation),
        "static_inputs_passed": True,
        "host_os": platform.system(),
        "single_cuda_detected": cuda_available,
        "host_os_and_cuda_detected": host_qualified,
        "execution_card_ready": False,
        "training_executed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/train/gate3_capability_pilot_v1.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = assess(args.config)
    report["report_sha256"] = canonical_sha(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, sort_keys=True)
            handle.write("\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
