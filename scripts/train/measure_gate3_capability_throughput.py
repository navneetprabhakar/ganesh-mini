#!/usr/bin/env python3
"""Measure a bounded, training-only Gate 3 optimizer envelope on the actual CUDA host."""

from __future__ import annotations

import argparse
import gc
import json
import math
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from scripts.train.preflight_gate3_capability_pilot import ROOT, assess, canonical_sha, file_sha, resolve, verify_model_inventory
from scripts.train.qwen_runtime import configure_cuda_allocator, configure_fused_training_loss, configure_qwen_training_structure
from scripts.train.run_sft import collate, load_rows, seed_everything, select_lora_targets
from scripts.train.cuda_host_floor import assess_cuda_host


PROBE_ROWS = 16
MAXIMUM_WALL_SECONDS = 1800


def select_probe_rows(rows: list[dict], count: int = PROBE_ROWS) -> list[dict]:
    """Choose the longest source-unique rows, pessimistic for memory and throughput."""
    if len(rows) < count or len({row["source_id"] for row in rows}) != len(rows):
        raise ValueError("probe input is short or source-duplicated")
    return sorted(rows, key=lambda row: (-len(row["input_ids"]), row["source_id"]))[:count]


def measure(config_path: Path, model_dir: Path, instance_id: str, output: Path,
            hourly_cost_usd: Decimal, absolute_incremental_ceiling_usd: Decimal) -> dict:
    if not instance_id.strip() or output.exists():
        raise ValueError("non-empty instance ID and unused output path required")
    if (not hourly_cost_usd.is_finite() or not absolute_incremental_ceiling_usd.is_finite() or
        hourly_cost_usd <= 0 or absolute_incremental_ceiling_usd <= 0):
        raise ValueError("positive finite hourly price and absolute incremental ceiling required")
    cost_bounded_seconds = int(absolute_incremental_ceiling_usd / hourly_cost_usd * Decimal(3600)) - 600
    if cost_bounded_seconds <= 0:
        raise ValueError("cost ceiling leaves no 600-second finalization reserve")
    wall_limit = min(MAXIMUM_WALL_SECONDS, cost_bounded_seconds)
    whole_started = time.monotonic()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    seed_path = resolve(ROOT, config["recipe"]["qualified_seed_recipe_path"])
    recipe = json.loads(seed_path.read_text(encoding="utf-8"))["recipes"]["primary"]
    recipe["lr_selection_budget_seen_tokens_per_candidate"] = 651639
    configure_cuda_allocator(recipe["cuda_allocator_config"])
    static = assess(config_path)
    if not static["host_os_and_cuda_detected"]:
        raise RuntimeError("throughput qualifier requires the actual Linux single-CUDA host")
    inventory_path = resolve(ROOT, config["model"]["inventory_path"])
    verified_model = verify_model_inventory(model_dir, inventory_path)
    rows = load_rows(resolve(ROOT, config["data"]["prepared_train_path"]))
    probe = select_probe_rows(rows)
    if any(len(row["input_ids"]) > recipe["sequence_length"] for row in probe):
        raise RuntimeError("probe row exceeds frozen token envelope")

    import torch
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForImageTextToText, get_cosine_schedule_with_warmup

    hardware = assess_cuda_host(torch, output.with_name('gpu-hardware-preflight.json'))
    properties = torch.cuda.get_device_properties(0)
    seed_everything(recipe["random_seed"])
    torch.cuda.set_device(0)
    torch.cuda.reset_peak_memory_stats(0)
    model = AutoModelForImageTextToText.from_pretrained(model_dir, local_files_only=True,
                                                         dtype=torch.bfloat16, device_map={"": 0})
    structure = configure_qwen_training_structure(model)
    if not structure["vision_moved_to_cpu"]:
        raise RuntimeError("frozen vision offload did not occur")
    gc.collect()
    torch.cuda.empty_cache()
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()
    if not model.is_gradient_checkpointing:
        raise RuntimeError("frozen gradient checkpointing did not activate")
    fused = configure_fused_training_loss(model, recipe["fused_linear_cross_entropy"]["version"])
    targets = select_lora_targets(model.named_modules(), torch.nn.Linear, recipe)
    model = get_peft_model(model, LoraConfig(r=recipe["lora_rank"], lora_alpha=recipe["lora_alpha"],
                                           lora_dropout=recipe["lora_dropout"], target_modules=targets,
                                           bias="none", task_type="CAUSAL_LM"))
    trainable = [parameter for parameter in model.parameters() if parameter.requires_grad]
    if not trainable:
        raise RuntimeError("no trainable adapter parameters")
    optimizer = torch.optim.AdamW(trainable, lr=recipe["learning_rate_candidates"][0],
                                  betas=tuple(recipe["optimizer_betas"]),
                                  eps=recipe["optimizer_epsilon"], weight_decay=recipe["weight_decay"])
    scheduler = get_cosine_schedule_with_warmup(
        optimizer, math.ceil(2 * recipe["warmup_ratio"]), 2)
    model.train()
    optimizer.zero_grad(set_to_none=True)
    torch.cuda.synchronize()
    train_started = time.monotonic()
    seen_tokens = 0
    response_tokens = 0
    raw_losses = []
    accumulation = recipe["gradient_accumulation_steps"]
    for index, row in enumerate(probe, 1):
        batch = collate(row, "cuda:0")
        result = model(**batch, skip_logits=True)
        if result.logits is not None or not torch.isfinite(result.loss):
            raise RuntimeError("qualifier loss was non-finite or materialized logits")
        weight = float(row["objective_weight"])
        if not math.isfinite(weight) or weight <= 0:
            raise RuntimeError("qualifier objective weight is invalid")
        (result.loss * weight).backward()
        raw_losses.append(float(result.loss.detach().cpu()))
        seen_tokens += int(batch["attention_mask"].sum().item())
        response_tokens += int((batch["labels"] != -100).sum().item())
        if index % accumulation == 0:
            torch.nn.utils.clip_grad_norm_(trainable, recipe["max_gradient_norm"])
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad(set_to_none=True)
            if time.monotonic() - whole_started > wall_limit:
                raise RuntimeError("bounded throughput qualifier exceeded wall limit")
    torch.cuda.synchronize()
    training_seconds = time.monotonic() - train_started
    peak = max(torch.cuda.max_memory_allocated(0), torch.cuda.max_memory_reserved(0))
    if peak > int(recipe["maximum_peak_vram_gb"] * 1024**3):
        raise RuntimeError("throughput qualifier exceeded frozen peak-VRAM limit")
    if not training_seconds > 0 or len(raw_losses) != PROBE_ROWS:
        raise RuntimeError("throughput qualifier did not complete exact probe")
    report = {
        "schema_version": "ganesh-mini-capability-pilot-throughput/v1",
        "status": "passed",
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "instance_id": instance_id,
        "model_revision": verified_model["revision"],
        "model_inventory_file_sha256": verified_model["inventory_file_sha256"],
        "recipe_sha256": canonical_sha(recipe),
        "prepared_manifest_sha256": config["data"]["prepared_manifest_sha256"],
        "prepared_train_sha256": file_sha(resolve(ROOT, config["data"]["prepared_train_path"])),
        "selection": "longest-16-source-unique-rows",
        "selected_source_ids": [row["source_id"] for row in probe],
        "probe_records": PROBE_ROWS,
        "optimizer_steps": PROBE_ROWS // accumulation,
        "input_tokens": seen_tokens,
        "response_tokens": response_tokens,
        "training_wall_seconds": training_seconds,
        "whole_process_wall_seconds": time.monotonic() - whole_started,
        "hourly_cost_usd": str(hourly_cost_usd),
        "absolute_incremental_ceiling_usd": str(absolute_incremental_ceiling_usd),
        "cost_bounded_wall_seconds": wall_limit,
        "measured_input_tokens_per_second": seen_tokens / training_seconds,
        "peak_vram_bytes": peak,
        "gpu_name": properties.name,
        "gpu_vram_bytes": properties.total_memory,
        "gpu_hardware_preflight_sha256": hardware["evidence_sha256"],
        "fused_loss": fused,
        "loss_finite": all(math.isfinite(loss) for loss in raw_losses),
        "quality_result": False,
        "adapter_retained": False,
    }
    report["report_sha256"] = canonical_sha(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/train/gate3_capability_pilot_v1.json")
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--hourly-cost-usd", type=Decimal, required=True)
    parser.add_argument("--absolute-incremental-ceiling-usd", type=Decimal, required=True)
    args = parser.parse_args()
    report = measure(args.config, args.model_dir, args.instance_id, args.output,
                     args.hourly_cost_usd, args.absolute_incremental_ceiling_usd)
    print(json.dumps({"status": report["status"],
                      "measured_input_tokens_per_second": report["measured_input_tokens_per_second"],
                      "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
