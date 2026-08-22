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
    """Render one row with the tokenizer-owned chat template and assistant mask.

    Qwen's template is the authority. We deliberately do not infer response
    boundaries from token IDs or hard-coded delimiters.
    """
    messages = record.get("messages")
    if not isinstance(messages, list) or not messages:
        raise PreflightError("non-empty text-only messages are required")
    if any(not isinstance(message, dict) or message.get("role") not in {"system", "user", "assistant"} or not isinstance(message.get("content"), str) for message in messages):
        raise PreflightError("text-only role/content messages are required")
    if messages[-1].get("role") != "assistant":
        raise PreflightError("record must end with one assistant response")
    encoded = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=False,
        return_dict=True,
        return_assistant_tokens_mask=True,
    )
    input_ids = encoded.get("input_ids")
    mask = encoded.get("assistant_masks", encoded.get("assistant_tokens_mask"))
    if input_ids and isinstance(input_ids[0], list):
        if len(input_ids) != 1:
            raise PreflightError("batched chat rendering is not accepted")
        input_ids = input_ids[0]
    if mask and isinstance(mask[0], list):
        mask = mask[0]
    if not isinstance(input_ids, list) or not isinstance(mask, list) or len(input_ids) != len(mask):
        raise PreflightError("tokenizer did not return a valid assistant token mask")
    response_positions = [index for index, active in enumerate(mask) if active == 1]
    if not response_positions or response_positions != list(range(response_positions[0], len(input_ids))):
        raise PreflightError("assistant mask must identify one terminal response")
    labels = [token if active == 1 else -100 for token, active in zip(input_ids, mask)]
    rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    if not isinstance(rendered, str) or not rendered:
        raise PreflightError("tokenizer did not render a non-empty chat string")
    return {
        "id": record.get("id"),
        "lane": record.get("lane"),
        "input_ids": input_ids,
        "labels": labels,
        "prompt_token_count": response_positions[0],
        "rendered_prompt_sha256": hashlib.sha256(rendered.encode()).hexdigest(),
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


def audit_prepared_records(path: Path) -> tuple[int, Counter[str]]:
    records = 0
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
            response_tokens[lane] += len(labels) - prompt_tokens
    return records, response_tokens


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
        prepared_records, audited_tokens = audit_prepared_records(prepared_path) if prepared_hash_ok else (0, Counter())
    except (OSError, json.JSONDecodeError, PreflightError):
        prepared_records, audited_tokens = 0, Counter()
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
    records_ok = prepared_hash_ok and prepared_records == manifest.get("prepared_train_records") and dict(audited_tokens) == token_counts
    total = sum(token_counts.get(lane, 0) for lane in LANES) if all(isinstance(token_counts.get(lane), int) and token_counts[lane] > 0 for lane in LANES) else 0
    tolerance = config["data"]["maximum_absolute_share_error"]
    shares_ok = total > 0 and all(abs(token_counts[lane] / total - target) <= tolerance for lane, target in config["data"]["family_token_targets"].items())
    epochs = manifest.get("effective_epochs_by_lane", {})
    epochs_ok = set(epochs) == set(LANES) and all(
        isinstance(epochs[lane], (int, float)) and 0 < epochs[lane] <= config["recipe"]["maximum_effective_epochs"]
        for lane in LANES
    )
    passed = digest_ok and bound and records_ok and shares_ok and epochs_ok
    add(checks, "prepared_dataset", passed, "Prepared data must prove upstream chat rendering, response-only masks, no vision tokens, balanced response tokens, and capped lane epochs.", path=str(path), prepared_records=prepared_records, total_response_tokens=total, records_ok=records_ok, shares_ok=shares_ok, epochs_ok=epochs_ok, claimed_sha256=claimed)
    return manifest


def validate_static(config: dict[str, Any], root: Path, system: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    required_top = {"schema_version", "run_id", "output_model_name", "model", "data", "prerequisites", "rendering", "recipe", "control", "outputs"}
    add(checks, "config_shape", set(config) == required_top and config.get("schema_version") == "ganesh-mini-train-config/v1", "Config must contain exactly the versioned controller sections.")

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

    recipe = config["recipe"]
    recipe_ok = (
        system == "Linux" == recipe["host_os"]
        and recipe["accelerator"] == "CUDA"
        and recipe["backend"] == "ms-swift-transformers"
        and recipe["base_loading"] == "qlora"
        and recipe["quantization_bits"] == 4
        and recipe["quantization_type"] == "nf4"
        and recipe["quantization_double"] is True
        and recipe["compute_dtype"] == "bfloat16"
        and recipe["vision_frozen"] is True
        and recipe["sequence_length"] == 4096
        and recipe["packing"] is False
        and (recipe["lora_rank"], recipe["lora_alpha"], recipe["lora_dropout"]) == (32, 64, 0.05)
        and recipe["learning_rate_candidates"] == [0.0001, 0.0002]
        and recipe["scheduler"] == "cosine"
        and recipe["warmup_ratio"] == 0.03
        and 0 < recipe["maximum_effective_epochs"] <= 3
        and recipe["checkpoint_every_effective_epochs"] == 0.5
    )
    add(checks, "bounded_cuda_recipe", recipe_ok, "Pilot recipe must remain the predeclared Linux CUDA NF4/BF16 QLoRA recipe.", observed_system=system)

    control = config["control"]
    controls_ok = (
        all(isinstance(control[key], int) and control[key] > 0 for key in ("maximum_seen_tokens", "maximum_wall_seconds", "checkpoint_every_tokens"))
        and isinstance(control["maximum_cost_usd"], (int, float)) and control["maximum_cost_usd"] > 0
        and control["resume_requires_checkpoint_manifest"] is True
        and control["resume_requires_hash_match"] is True
        and REQUIRED_STOP_CONDITIONS <= set(control["stop_conditions"])
    )
    add(checks, "budgets_resume_and_stops", controls_ok, "Finite token/time/cost ceilings, hash-bound resume, checkpoints, and mandatory stop conditions are required.")
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
        "recipe": config["recipe"],
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
    if not isinstance(checkpoint.get("step"), int) or checkpoint["step"] <= 0 or not isinstance(checkpoint.get("seen_tokens"), int) or not 0 < checkpoint["seen_tokens"] <= card["budgets"]["maximum_seen_tokens"]:
        raise PreflightError("checkpoint step or token budget is invalid")
    if not SHA256.fullmatch(str(checkpoint.get("checkpoint_sha256", ""))):
        raise PreflightError("checkpoint artifact hash is invalid")
    epochs = checkpoint.get("effective_epochs_by_lane", {})
    if set(epochs) != set(LANES) or any(not isinstance(value, (int, float)) or value < 0 or value > card["recipe"]["maximum_effective_epochs"] for value in epochs.values()):
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
