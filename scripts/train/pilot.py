#!/usr/bin/env python3
"""Fail-closed controller for the Ganesh Mini seed pilot.

This controller validates and materializes an immutable execution card. It does
not import a training framework or start a training process. A later runner may
consume a `ready` card, but must preserve all identities and stop conditions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.train.response_only import ResponseOnlyError, build_response_only_encoding


SHA256 = re.compile(r"^[0-9a-f]{64}$")
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
REQUIRED_GATE0_CHECKS = {
    "model_identity",
    "local_inventory",
    "architecture",
    "chat_template",
    "dependency_matrix",
    "exact_dependency_lock",
    "lora_targets_and_gradients",
    "text_only_inference_smoke",
    "train_save_reload_merge_smoke",
    "base_gguf_f16_q8_smoke",
    "cuda_fused_loss_qualification",
}
REQUIRED_STOP_CONDITIONS = {
    "non_finite_loss",
    "three_consecutive_loss_spikes",
    "token_budget_reached",
    "wall_time_reached",
    "cost_ceiling_reached",
    "checkpoint_write_failure",
    "evidence_write_failure",
}
FALLBACK_REASONS = {
    "primary_cuda_oom",
    "primary_peak_vram_exceeded",
}


class PreflightError(ValueError):
    """A training input failed a closed prerequisite."""


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def sealed(value: dict[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result[field] = canonical_sha256(result)
    return result


def resolve(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def add(checks: list[dict[str, Any]], name: str, passed: bool, detail: str, **evidence: Any) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail, "evidence": evidence})


def verify_file(root: Path, path_value: str, expected_hash: str) -> tuple[bool, dict[str, Any]]:
    path = resolve(root, path_value)
    observed = file_sha256(path) if path.is_file() else None
    return observed == expected_hash and bool(SHA256.fullmatch(expected_hash)), {
        "path": str(path),
        "expected_sha256": expected_hash,
        "observed_sha256": observed,
    }


def count_jsonl(path: Path) -> tuple[int, Counter[str]]:
    count = 0
    lanes: Counter[str] = Counter()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                raise PreflightError(f"blank JSONL row at {path}:{line_number}")
            value = json.loads(line)
            lane = value.get("lane")
            if lane not in LANES:
                raise PreflightError(f"invalid lane at {path}:{line_number}: {lane!r}")
            count += 1
            lanes[lane] += 1
    return count, lanes


def render_response_only(tokenizer: Any, record: dict[str, Any]) -> dict[str, Any]:
    """Render one row with a tokenizer-proven terminal response boundary."""
    messages = record.get("messages")
    if not isinstance(messages, list) or not messages:
        raise PreflightError("non-empty text-only messages are required")
    if any(not isinstance(message, dict) or message.get("role") not in {"system", "user", "assistant"} or not isinstance(message.get("content"), str) for message in messages):
        raise PreflightError("text-only role/content messages are required")
    if messages[-1].get("role") != "assistant":
        raise PreflightError("record must end with one assistant response")
    try:
        response = build_response_only_encoding(tokenizer, messages)
    except ResponseOnlyError as exc:
        raise PreflightError(str(exc)) from exc
    return {
        "id": record.get("id"),
        "lane": record.get("lane"),
        "input_ids": response.encoding["input_ids"],
        "labels": response.encoding["labels"],
        "prompt_token_count": response.prompt_token_count,
        "response_token_count": response.response_token_count,
        "rendered_prompt_sha256": hashlib.sha256(response.rendered.encode()).hexdigest(),
    }


def verify_gate_report(
    checks: list[dict[str, Any]], name: str, path: Path, gate: int, model: dict[str, Any], expected: dict[str, Any] | None = None
) -> dict[str, Any] | None:
    if not path.is_file():
        add(checks, name, False, f"Gate {gate} readiness evidence is absent.", path=str(path))
        return None
    try:
        report = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        add(checks, name, False, "Readiness evidence is unreadable.", path=str(path), error=str(exc))
        return None
    identity_ok = report.get("model_id") == model["model_id"] and report.get("revision") == model["revision"]
    digest_field = "report_sha256" if "report_sha256" in report else "evidence_sha256"
    claimed = report.get(digest_field)
    unsigned = dict(report)
    unsigned.pop(digest_field, None)
    digest_ok = bool(SHA256.fullmatch(str(claimed or ""))) and canonical_sha256(unsigned) == claimed
    expected_ok = all(report.get(key) == value for key, value in (expected or {}).items())
    passed = report.get("gate") == gate and report.get("status") == "ready" and identity_ok and digest_ok and expected_ok
    if gate == 0:
        observed = {item.get("name") for item in report.get("checks", []) if item.get("passed") is True}
        passed = passed and REQUIRED_GATE0_CHECKS <= observed and not report.get("failed_checks")
    add(checks, name, passed, "Readiness report must be sealed, ready, and bound to the exact model.", path=str(path), claimed_sha256=claimed)
    return report


def audit_prepared_records(path: Path) -> tuple[int, Counter[str], int]:
    records = 0
    input_tokens = 0
    response_tokens: Counter[str] = Counter()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            value = json.loads(line)
            lane = value.get("lane")
            input_ids, labels = value.get("input_ids"), value.get("labels")
            prompt_tokens = value.get("prompt_token_count")
            valid = (
                lane in LANES
                and isinstance(input_ids, list)
                and isinstance(labels, list)
                and len(input_ids) == len(labels)
                and isinstance(prompt_tokens, int)
                and 0 < prompt_tokens < len(labels)
                and all(label == -100 for label in labels[:prompt_tokens])
                and labels[prompt_tokens:] == input_ids[prompt_tokens:]
                and bool(SHA256.fullmatch(str(value.get("rendered_prompt_sha256", ""))))
            )
            if not valid:
                raise PreflightError(f"invalid response-only prepared row at {path}:{line_number}")
            records += 1
            input_tokens += len(input_ids)
            response_tokens[lane] += len(labels) - prompt_tokens
    return records, response_tokens, input_tokens


def verify_prepared_manifest(
    checks: list[dict[str, Any]], path: Path, config: dict[str, Any], model_contract: dict[str, Any], gate0: dict[str, Any] | None
) -> dict[str, Any] | None:
    if not path.is_file():
        add(checks, "prepared_dataset", False, "Tokenized/rendered dataset evidence is absent.", path=str(path))
        return None
    manifest = load_json(path)
    claimed = manifest.get("manifest_sha256")
    unsigned = dict(manifest)
    unsigned.pop("manifest_sha256", None)
    digest_ok = bool(SHA256.fullmatch(str(claimed or ""))) and canonical_sha256(unsigned) == claimed
    rendering = manifest.get("rendering", {})
    gate0_template_hash = None
    if gate0:
        for item in gate0.get("checks", []):
            if item.get("name") == "chat_template" and item.get("passed") is True:
                gate0_template_hash = item.get("evidence", {}).get("sha256")
    # Prepared paths in the manifest are repository-relative. Derive the root
    # from the configured manifest location (`<root>/artifacts/train/...`).
    root = path
    while root.name != "artifacts" and root != root.parent:
        root = root.parent
    root = root.parent if root.name == "artifacts" else Path.cwd()
    prepared_path = resolve(root, manifest.get("prepared_train_path", ""))
    prepared_hash_ok = prepared_path.is_file() and file_sha256(prepared_path) == manifest.get("prepared_train_sha256")
    try:
        prepared_records, audited_tokens, audited_input_tokens = audit_prepared_records(prepared_path) if prepared_hash_ok else (0, Counter(), 0)
    except (OSError, json.JSONDecodeError, PreflightError):
        prepared_records, audited_tokens, audited_input_tokens = 0, Counter(), 0
    validation_path = resolve(root, manifest.get("prepared_validation_path", ""))
    validation_hash_ok = validation_path.is_file() and file_sha256(validation_path) == manifest.get("prepared_validation_sha256")
    try:
        validation_records, _, _ = audit_prepared_records(validation_path) if validation_hash_ok else (0, Counter(), 0)
    except (OSError, json.JSONDecodeError, PreflightError):
        validation_records = 0
    bound = (
        manifest.get("passed") is True
        and manifest.get("model_id") == config["model"]["model_id"]
        and manifest.get("revision") == config["model"]["revision"]
        and manifest.get("train_sha256") == config["data"]["train_sha256"]
        and manifest.get("validation_sha256") == config["data"]["validation_sha256"]
        and rendering.get("chat_template_source") == model_contract["serving_contract"]["chat_template_source"]
        and bool(SHA256.fullmatch(str(rendering.get("chat_template_sha256", ""))))
        and rendering.get("chat_template_sha256") == gate0_template_hash
        and rendering.get("upstream_tokenizer_applied") is True
        and rendering.get("add_generation_prompt") is False
        and rendering.get("response_only_labels_verified") is True
        and rendering.get("prompt_label_id") == -100
        and rendering.get("vision_token_count") == 0
    )
    token_counts = manifest.get("sampled_response_tokens_by_lane", {})
    records_ok = (
        prepared_hash_ok
        and prepared_records == manifest.get("prepared_train_records")
        and audited_input_tokens == manifest.get("prepared_train_input_tokens")
        and validation_hash_ok
        and validation_records == manifest.get("prepared_validation_records") == config["data"]["validation_records"]
        and dict(audited_tokens) == token_counts
    )
    total = sum(token_counts.get(lane, 0) for lane in LANES) if all(isinstance(token_counts.get(lane), int) and token_counts[lane] > 0 for lane in LANES) else 0
    tolerance = config["data"]["maximum_absolute_share_error"]
    shares_ok = total > 0 and all(abs(token_counts[lane] / total - target) <= tolerance for lane, target in config["data"]["family_token_targets"].items())
    epochs = manifest.get("effective_epochs_by_lane", {})
    epochs_ok = set(epochs) == set(LANES) and all(
        isinstance(epochs[lane], (int, float)) and 0 < epochs[lane] <= config["recipes"]["primary"]["maximum_effective_epochs"]
        for lane in LANES
    )
    passed = digest_ok and bound and records_ok and shares_ok and epochs_ok
    add(checks, "prepared_dataset", passed, "Prepared data must prove upstream chat rendering, response-only masks, no vision tokens, balanced response tokens, and capped lane epochs.", path=str(path), prepared_records=prepared_records, total_response_tokens=total, records_ok=records_ok, shares_ok=shares_ok, epochs_ok=epochs_ok, claimed_sha256=claimed)
    return manifest


def common_recipe_ok(recipe: dict[str, Any], system: str) -> bool:
    return (
        system == "Linux" == recipe.get("host_os")
        and recipe.get("accelerator") == "CUDA"
        and recipe.get("backend") == "transformers-peft"
        and recipe.get("adapter") == "lora"
        and recipe.get("compute_dtype") == "bfloat16"
        and recipe.get("gradient_checkpointing") is True
        and recipe.get("cuda_allocator_config") == "expandable_segments:True"
        and recipe.get("fused_linear_cross_entropy") == {
            "provider":"liger-kernel",
            "version":"0.8.2",
            "materialize_training_logits":False,
        }
        and recipe.get("micro_batch_size") == 1
        and recipe.get("vision_frozen") is True
        and recipe.get("sequence_length") == 2944
        and recipe.get("packing") is False
        and (recipe.get("lora_rank"), recipe.get("lora_alpha"), recipe.get("lora_dropout")) == (32, 64, 0.05)
        and recipe.get("learning_rate_candidates") == [0.0001, 0.0002]
        and recipe.get("random_seed") == 3502
        and recipe.get("gradient_accumulation_steps") == 8
        and recipe.get("effective_batch_size") == recipe.get("micro_batch_size") * recipe.get("gradient_accumulation_steps")
        and recipe.get("optimizer") == "adamw_torch"
        and recipe.get("optimizer_betas") == [0.9, 0.95]
        and recipe.get("optimizer_epsilon") == 1e-8
        and recipe.get("weight_decay") == 0.01
        and recipe.get("max_gradient_norm") == 1.0
        and recipe.get("dataloader_workers") == 8
        and recipe.get("dataloader_pin_memory") is True
        and recipe.get("dataloader_prefetch_factor") == 4
        and recipe.get("precision") == "bf16"
        and recipe.get("lr_selection_budget_seen_tokens_per_candidate") == 400000
        and recipe.get("lr_selection_rule") == "select_0.0002_only_if_development_macro_improves_by_at_least_one_task_equivalent_with_no_lane_regression_else_0.0001"
        and recipe.get("scheduler") == "cosine"
        and recipe.get("warmup_ratio") == 0.03
        and isinstance(recipe.get("maximum_effective_epochs"), (int, float))
        and 0 < recipe["maximum_effective_epochs"] <= 3
        and recipe.get("checkpoint_every_effective_epochs") == 0.5
    )


def validate_fallback_qualification(
    checks: list[dict[str, Any]], config: dict[str, Any], root: Path
) -> dict[str, Any] | None:
    strategy = config["strategy"]
    primary, fallback = config["recipes"]["primary"], config["recipes"]["fallback"]
    if strategy["selected_recipe_id"] == primary["recipe_id"]:
        clean = strategy["fallback_reason"] is None and strategy["fallback_qualification_path"] is None
        add(checks, "primary_recipe_selected", clean, "The primary BF16 LoRA recipe needs no fallback claim or evidence.")
        return None
    path_value = strategy.get("fallback_qualification_path")
    if strategy["selected_recipe_id"] != fallback["recipe_id"] or strategy.get("fallback_reason") not in FALLBACK_REASONS or not isinstance(path_value, str):
        add(checks, "fallback_qualified", False, "Fallback selection requires an allowed reason and evidence path.")
        return None
    path = resolve(root, path_value)
    if not path.is_file():
        add(checks, "fallback_qualified", False, "Fallback qualification evidence is absent.", path=str(path))
        return None
    evidence = load_json(path)
    claimed = evidence.get("evidence_sha256")
    unsigned = dict(evidence)
    unsigned.pop("evidence_sha256", None)
    sealed_ok = bool(SHA256.fullmatch(str(claimed or ""))) and canonical_sha256(unsigned) == claimed
    model = config["model"]
    bound = (
        evidence.get("schema_version") == "ganesh-mini-fallback-qualification/v1"
        and evidence.get("passed") is True
        and evidence.get("model_id") == model["model_id"]
        and evidence.get("revision") == model["revision"]
        and evidence.get("primary_recipe_id") == primary["recipe_id"]
        and evidence.get("primary_recipe_sha256") == canonical_sha256(primary)
        and evidence.get("fallback_recipe_id") == fallback["recipe_id"]
        and evidence.get("fallback_recipe_sha256") == canonical_sha256(fallback)
        and evidence.get("reason") == strategy["fallback_reason"]
    )
    measurements = evidence.get("measurements", {})
    attempt = evidence.get("primary_attempt", {})
    reason = strategy["fallback_reason"]
    expected_source = {
        "primary_cuda_oom": "cuda_runtime",
        "primary_peak_vram_exceeded": "gpu_telemetry",
    }[reason]
    attempt_ok = (
        isinstance(attempt.get("attempt_id"), str)
        and bool(attempt["attempt_id"])
        and isinstance(attempt.get("observed_at"), str)
        and bool(attempt["observed_at"])
        and attempt.get("measurement_source") == expected_source
        and bool(SHA256.fullmatch(str(attempt.get("measurement_sha256", ""))))
    )
    measured = (
        (reason == "primary_cuda_oom" and measurements.get("cuda_oom_observed") is True)
        or (reason == "primary_peak_vram_exceeded" and isinstance(measurements.get("peak_vram_gb"), (int, float)) and measurements["peak_vram_gb"] > primary["maximum_peak_vram_gb"])
    )
    passed = sealed_ok and bound and attempt_ok and measured
    add(checks, "fallback_qualified", passed, "NF4 QLoRA requires sealed measured BF16 LoRA OOM, VRAM, or cost evidence.", path=str(path), reason=reason, measurements=measurements)
    return evidence


def validate_static(config: dict[str, Any], root: Path, system: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    required_top = {"schema_version", "run_id", "output_model_name", "model", "data", "prerequisites", "rendering", "strategy", "recipes", "control", "outputs"}
    add(checks, "config_shape", set(config) == required_top and config.get("schema_version") == "ganesh-mini-train-config/v4", "Config must contain exactly the versioned controller sections.")

    model = config["model"]
    contract_ok, contract_evidence = verify_file(root, model["contract_path"], model["contract_file_sha256"])
    contract = load_json(resolve(root, model["contract_path"]))
    model_ok = contract_ok and model["model_id"] == contract.get("model_id") and model["revision"] == contract.get("revision") and re.fullmatch(r"[0-9a-f]{40}", model["revision"]) is not None
    add(checks, "model_pin", model_ok, "Raw contract hash, model ID, and immutable revision must all match.", **contract_evidence)

    data = config["data"]
    for prefix in ("source_manifest", "train", "validation"):
        ok, evidence = verify_file(root, data[f"{prefix}_path"], data[f"{prefix}_sha256"])
        add(checks, f"{prefix}_identity", ok, "Input bytes must match the configured SHA-256.", **evidence)
    train_count, train_lanes = count_jsonl(resolve(root, data["train_path"]))
    validation_count, validation_lanes = count_jsonl(resolve(root, data["validation_path"]))
    counts_ok = train_count == data["train_records"] == 1399 and validation_count == data["validation_records"] == 50 and set(train_lanes) == set(LANES) and set(validation_lanes) == set(LANES)
    add(checks, "seed_inventory", counts_ok, "The authorized full seed inventory and all six lanes must be present.", train_records=train_count, validation_records=validation_count, train_lanes=dict(train_lanes), validation_lanes=dict(validation_lanes))

    targets = data["family_token_targets"]
    target_ok = set(targets) == set(LANES) and math.isclose(sum(targets.values()), 1.0, abs_tol=1e-12) and targets == {"go": 0.2, "java": 0.2, "javascript": 0.1, "typescript": 0.1, "python": 0.2, "rust": 0.2}
    add(checks, "five_family_balance", target_ok, "Five families must receive 20% each; JavaScript and TypeScript split one family equally.", targets=targets)

    rendering = config["rendering"]
    render_ok = rendering == {"chat_template_source": contract["serving_contract"]["chat_template_source"], "use_upstream_tokenizer": True, "add_generation_prompt": False, "response_only_loss": True, "prompt_label_id": -100, "vision_tokens_allowed": False}
    add(checks, "rendering_contract", render_ok, "Training must use the upstream Qwen template with response-only labels and no vision tokens.")

    primary, fallback = config["recipes"]["primary"], config["recipes"]["fallback"]
    primary_ok = (
        primary.get("recipe_id") == "bf16-lora-primary-v1"
        and common_recipe_ok(primary, system)
        and primary.get("minimum_gpu_vram_gb") == 24
        and primary.get("maximum_peak_vram_gb") == 23
        and primary.get("base_loading") == "bfloat16"
        and not any(key in primary for key in ("quantization_bits", "quantization_type", "quantization_double"))
    )
    add(checks, "primary_bf16_lora_recipe", primary_ok, "Primary pilot must be BF16 LoRA on Linux CUDA with at least 24 GB VRAM, microbatch 1, and gradient checkpointing.", observed_system=system)
    fallback_ok = (
        fallback.get("recipe_id") == "nf4-qlora-fallback-v1"
        and common_recipe_ok(fallback, system)
        and fallback.get("base_loading") == "qlora"
        and fallback.get("quantization_bits") == 4
        and fallback.get("quantization_type") == "nf4"
        and fallback.get("quantization_double") is True
    )
    add(checks, "fallback_nf4_qlora_recipe", fallback_ok, "The only predeclared fallback is Linux CUDA NF4 QLoRA with the same bounded adapter recipe.", observed_system=system)

    control = config["control"]
    prepared_manifest_path = resolve(root, data["prepared_manifest_path"])
    prepared_budget = load_json(prepared_manifest_path).get("prepared_train_input_tokens") if prepared_manifest_path.is_file() else None
    controls_ok = (
        all(isinstance(control[key], int) and control[key] > 0 for key in ("maximum_seen_tokens", "maximum_wall_seconds", "checkpoint_every_tokens"))
        and control["maximum_seen_tokens"] == prepared_budget
        and isinstance(control["maximum_cost_usd"], (int, float)) and control["maximum_cost_usd"] > 0
        and control["resume_requires_checkpoint_manifest"] is True
        and control["resume_requires_hash_match"] is True
        and REQUIRED_STOP_CONDITIONS <= set(control["stop_conditions"])
    )
    add(checks, "budgets_resume_and_stops", controls_ok, "Finite token/time/cost ceilings, hash-bound resume, checkpoints, and mandatory stop conditions are required.")
    validate_fallback_qualification(checks, config, root)
    return checks, contract


def build_execution_card(config_path: Path, root: Path, system: str | None = None) -> dict[str, Any]:
    config = load_json(config_path)
    checks, contract = validate_static(config, root, system or platform.system())
    model = config["model"]
    prereq = config["prerequisites"]
    reports = {
        "gate0": verify_gate_report(checks, "gate0_ready", resolve(root, prereq["gate0_report_path"]), 0, model),
        "gate1": verify_gate_report(checks, "gate1_ready", resolve(root, prereq["gate1_report_path"]), 1, model, {"evaluation_contract_frozen": True, "base_baseline_complete": True, "decision_prompts_exposed": False}),
        "gate2": verify_gate_report(checks, "gate2_ready", resolve(root, prereq["gate2_report_path"]), 2, model, {"seed_manifest_sha256": config["data"]["source_manifest_sha256"], "train_sha256": config["data"]["train_sha256"], "validation_sha256": config["data"]["validation_sha256"], "compatibility_passed": True, "evaluation_overlap_passed": True}),
    }
    prepared = verify_prepared_manifest(checks, resolve(root, config["data"]["prepared_manifest_path"]), config, contract, reports["gate0"])
    ready = all(item["passed"] for item in checks)
    recipes_by_id = {recipe.get("recipe_id"): recipe for recipe in config["recipes"].values()}
    selected_recipe = recipes_by_id.get(config["strategy"].get("selected_recipe_id"), {})
    card = {
        "schema_version": "ganesh-mini-training-execution-card/v1",
        "status": "ready" if ready else "not_ready",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run_id": config["run_id"],
        "output_model_name": config["output_model_name"],
        "model": {"model_id": model["model_id"], "revision": model["revision"], "contract_file_sha256": model["contract_file_sha256"]},
        "inputs": {
            "config_path": str(config_path),
            "config_sha256": file_sha256(config_path),
            "seed_manifest_sha256": config["data"]["source_manifest_sha256"],
            "train_sha256": config["data"]["train_sha256"],
            "validation_sha256": config["data"]["validation_sha256"],
            "prepared_manifest_sha256": prepared.get("manifest_sha256") if prepared else None,
        },
        "strategy": config["strategy"],
        "selected_recipe": selected_recipe,
        "recipe_identities": {name: {"recipe_id": recipe["recipe_id"], "recipe_sha256": canonical_sha256(recipe)} for name, recipe in config["recipes"].items()},
        "budgets": config["control"],
        "outputs": config["outputs"],
        "prerequisite_evidence": {
            name: (report.get("report_sha256") or report.get("evidence_sha256")) if report else None
            for name, report in reports.items()
        },
        "checks": checks,
        "failed_checks": [item["name"] for item in checks if not item["passed"]],
    }
    return sealed(card, "card_sha256")


def validate_resume(checkpoint: dict[str, Any], card: dict[str, Any]) -> None:
    if checkpoint.get("schema_version") != "ganesh-mini-training-checkpoint/v1" or checkpoint.get("run_id") != card.get("run_id"):
        raise PreflightError("checkpoint identity does not match the execution card")
    unsigned = dict(checkpoint)
    claimed = unsigned.pop("evidence_sha256", None)
    if not SHA256.fullmatch(str(claimed or "")) or canonical_sha256(unsigned) != claimed:
        raise PreflightError("checkpoint evidence hash is invalid")
    if checkpoint.get("config_sha256") != card["inputs"]["config_sha256"] or checkpoint.get("dataset_manifest_sha256") != card["inputs"]["prepared_manifest_sha256"]:
        raise PreflightError("checkpoint inputs do not match the execution card")
    if checkpoint.get("selected_recipe_id") != card["selected_recipe"].get("recipe_id") or checkpoint.get("selected_recipe_sha256") != canonical_sha256(card["selected_recipe"]):
        raise PreflightError("checkpoint recipe does not match the execution card")
    if not isinstance(checkpoint.get("step"), int) or checkpoint["step"] <= 0 or not isinstance(checkpoint.get("seen_tokens"), int) or not 0 < checkpoint["seen_tokens"] <= card["budgets"]["maximum_seen_tokens"]:
        raise PreflightError("checkpoint step or token budget is invalid")
    if not SHA256.fullmatch(str(checkpoint.get("checkpoint_sha256", ""))):
        raise PreflightError("checkpoint artifact hash is invalid")
    epochs = checkpoint.get("effective_epochs_by_lane", {})
    if set(epochs) != set(LANES) or any(not isinstance(value, (int, float)) or value < 0 or value > card["selected_recipe"]["maximum_effective_epochs"] for value in epochs.values()):
        raise PreflightError("checkpoint effective epochs are invalid")


def command_preflight(args: argparse.Namespace) -> int:
    card = build_execution_card(args.config, args.root, args.system)
    rendered = json.dumps(card, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if card["status"] == "ready" else 2


def command_resume(args: argparse.Namespace) -> int:
    card = load_json(args.card)
    if card.get("status") != "ready":
        raise PreflightError("resume requires a ready execution card")
    validate_resume(load_json(args.checkpoint), card)
    return 0


def parser() -> argparse.ArgumentParser:
    root = Path(__file__).resolve().parents[2]
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest="command", required=True)
    preflight = commands.add_parser("preflight", help="validate inputs and materialize a sealed execution card")
    preflight.add_argument("--root", type=Path, default=root)
    preflight.add_argument("--config", type=Path, default=root / "configs/train/seed_pilot.json")
    preflight.add_argument("--system", help=argparse.SUPPRESS)
    preflight.add_argument("--output", type=Path)
    preflight.set_defaults(func=command_preflight)
    resume = commands.add_parser("validate-resume", help="fail closed unless a checkpoint matches a ready card")
    resume.add_argument("--card", type=Path, required=True)
    resume.add_argument("--checkpoint", type=Path, required=True)
    resume.set_defaults(func=command_resume)
    return cli


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"ganesh-seed-pilot: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
