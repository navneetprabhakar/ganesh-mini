#!/usr/bin/env python3
"""Build exact canary and full-development configs for a verified Gate 4 adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    claimed = value.pop(field, None)
    if claimed != canonical_digest(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def relative(root: Path, path: Path) -> str:
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("evaluation input escapes workspace root")
    return str(resolved.relative_to(root.resolve()))


def config(*, run_id: str, task_glob: str, count: int, output_dir: str, adapter_dir: str, run_evidence: str, served_model_id: str = "ganesh-mini-1.0-expansion-pilot-v1") -> dict[str, Any]:
    return {
        "schema_version": "ganesh-mini-production-inference/v1",
        "run_id": run_id,
        "classification": "private_candidate_development",
        "task_globs": [task_glob],
        "allowed_surface": "development",
        "expected_task_count": count,
        "model_contract": "configs/model/qwen3_5_2b.contract.json",
        "model_inventory": "configs/model/qwen3_5_2b.inventory.json",
        "model_dir": "models/qwen3.5-2b-15852e8",
        "auto_model_class": "image-text-to-text",
        "runtimes": "configs/eval/runtimes.json",
        "output_dir": output_dir,
        "serving": {"modality": "text-only", "enable_thinking": False, "context_length": 8192, "add_generation_prompt": True},
        "generation": {"do_sample": False, "max_new_tokens": 4096, "use_cache": True},
        "execution": {"batch_size": 4, "verifier_workers": 12, "length_bucket_width": 256, "required_device": "cuda"},
        "extractor_id": "ganesh-code-fence-v1",
        "adapter": {"dir": adapter_dir, "run_evidence": run_evidence, "served_model_id": served_model_id},
    }


def build(root: Path, card_path: Path, terminal_path: Path, run_path: Path, adapter_dir: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    card = load_sealed(card_path, "card_sha256")
    terminal = load_sealed(terminal_path, "report_sha256")
    run = load_sealed(run_path, "evidence_sha256")
    if card.get("status") != "ready" or terminal.get("status") != "passed" or terminal.get("card_sha256") != card.get("card_sha256"):
        raise ValueError("evaluation configs require a matching passed training terminal report")
    if terminal.get("run_evidence_sha256") != run.get("evidence_sha256") or run.get("status") != "complete":
        raise ValueError("terminal report does not bind the complete training run")
    observed = {str(path.relative_to(adapter_dir)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(adapter_dir.rglob("*")) if path.is_file()}
    if not observed or observed != terminal.get("adapter_files") or observed != run.get("adapter_files"):
        raise ValueError("adapter files do not match training and terminal evidence")
    adapter_relative, run_relative = relative(root, adapter_dir), relative(root, run_path)
    recipe_id = card.get("selected_recipe", {}).get("recipe_id", "ganesh-mini-1.0-expansion-pilot-v1")
    canary = config(run_id=f"{recipe_id}-canary", task_glob="eval/private/development/tranche1/*.task.json", count=30, output_dir=f"measurement/inference/development/{recipe_id}-canary", adapter_dir=adapter_relative, run_evidence=run_relative, served_model_id=recipe_id)
    full = config(run_id=f"{recipe_id}-full", task_glob="eval/private/development/**/*.task.json", count=180, output_dir=f"measurement/inference/development/{recipe_id}-full", adapter_dir=adapter_relative, run_evidence=run_relative, served_model_id=recipe_id)
    capacity_probe = card.get("schema_version") in {"ganesh-mini-expansion-pilot-card/v2", "ganesh-mini-expansion-pilot-card/v3", "ganesh-mini-expansion-pilot-card/v4"}
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-expansion-evaluation-configs/v1",
        "status": "canary-ready-full-blocked",
        "card_sha256": card["card_sha256"],
        "terminal_report_sha256": terminal["report_sha256"],
        "training_run_evidence_sha256": run["evidence_sha256"],
        "adapter_files": observed,
        "canary_config_sha256": canonical_digest(canary),
        "full_config_sha256": canonical_digest(full),
        "full_release_condition": "prohibited-for-capacity-probe" if capacity_probe else "sealed_canary-adjudication-status-promote-to-full-development",
    }
    manifest["manifest_sha256"] = canonical_digest(manifest)
    return canary, full, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--card", type=Path, required=True)
    parser.add_argument("--terminal", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--adapter-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    canary, full, manifest = build(args.root, args.card, args.terminal, args.run, args.adapter_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, value in (("canary.json", canary), ("full.json", full), ("manifest.json", manifest)):
        (args.output_dir / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": manifest["status"], "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
