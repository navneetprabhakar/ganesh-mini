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
    checks = [
        {"name": "linux_cuda_contract", "passed": (system or platform.system()) == "Linux" and recipe["host_os"] == "Linux" and recipe["accelerator"] == "CUDA"},
        {"name": "model_contract", **checked_file(root, model["contract_path"], model["contract_sha256"])},
        {"name": "prepared_manifest_file", **checked_file(root, data["prepared_manifest_path"], data["prepared_manifest_file_sha256"])},
        {"name": "prepared_train_file", **checked_file(root, data["prepared_train_path"], data["prepared_train_sha256"])},
        {"name": "prepared_validation_file", **checked_file(root, data["prepared_validation_path"], data["prepared_validation_sha256"])},
        {"name": "throughput_evidence", **checked_file(root, config["throughput"]["evidence_path"], config["throughput"]["evidence_sha256"])},
    ]
    manifest = json.loads(resolve(root, data["prepared_manifest_path"]).read_text())
    claimed = manifest.pop("manifest_sha256", None)
    manifest_seal_ok = claimed == canonical_digest(manifest) == data["prepared_manifest_sha256"]
    checks.append({"name": "prepared_manifest_seal", "passed": manifest_seal_ok})
    prepared = manifest.get("prepared_train", {})
    identity_ok = (
        config.get("schema_version") == "ganesh-mini-expansion-pilot-config/v1"
        and prepared.get("records") == data["records"] == 3225
        and prepared.get("input_tokens") == data["input_tokens"] == control["maximum_seen_tokens"] == 2438853
        and manifest.get("revision") == model["revision"]
        and manifest.get("status") == "ready"
    )
    checks.append({"name": "corpus_and_model_identity", "passed": identity_ok})
    recipe_ok = (
        recipe.get("recipe_id") == "bf16-lora-expansion-pilot-v1"
        and recipe.get("learning_rate") == 0.00001
        and recipe.get("base_loading") == "bfloat16"
        and recipe.get("sequence_length") == 2944
        and recipe.get("micro_batch_size") == 1
        and recipe.get("gradient_accumulation_steps") == 8
        and recipe.get("maximum_effective_epochs") == 1.0
        and recipe.get("maximum_peak_vram_gb") == 23
    )
    checks.append({"name": "single_bounded_recipe", "passed": recipe_ok})
    quarter = control.get("checkpoint_tokens")
    bounds_ok = (
        control.get("maximum_wall_seconds") == 21600
        and control.get("finalization_reserve_seconds") == 1800
        and isinstance(quarter, list) and len(quarter) == 4
        and quarter[-1] == control["maximum_seen_tokens"]
        and all(0 < value <= control["maximum_seen_tokens"] for value in quarter)
    )
    checks.append({"name": "runtime_and_checkpoint_bounds", "passed": bounds_ok})
    failed = [item["name"] for item in checks if not item["passed"]]
    card: dict[str, Any] = {
        "schema_version": "ganesh-mini-expansion-pilot-card/v1",
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
