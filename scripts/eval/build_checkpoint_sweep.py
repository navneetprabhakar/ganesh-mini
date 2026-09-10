#!/usr/bin/env python3
"""Build sealed diagnostic canary configs for saved Gate 4 checkpoints."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


def canonical_digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    claimed = value.pop(field, None)
    if claimed != canonical_digest(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


SERVED_MODEL_PREFIX_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*[a-z0-9]$")


def checkpoint_config(name: str, runtime_training_dir: Path, served_model_prefix: str) -> dict[str, Any]:
    served_id = f"{served_model_prefix}-{name}"
    return {
        "schema_version": "ganesh-mini-production-inference/v1",
        "run_id": f"{served_id}-canary-diagnostic",
        "classification": "private_candidate_development",
        "task_globs": ["eval/private/development/tranche1/*.task.json"],
        "allowed_surface": "development",
        "expected_task_count": 30,
        "model_contract": "configs/model/qwen3_5_2b.contract.json",
        "model_inventory": "configs/model/qwen3_5_2b.inventory.json",
        "model_dir": "models/qwen3.5-2b-15852e8",
        "auto_model_class": "image-text-to-text",
        "runtimes": "configs/eval/runtimes.json",
        "output_dir": f"measurement/inference/development/{served_id}-canary-diagnostic",
        "serving": {"modality": "text-only", "enable_thinking": False, "context_length": 8192, "add_generation_prompt": True},
        "generation": {"do_sample": False, "max_new_tokens": 4096, "use_cache": True},
        "execution": {"batch_size": 4, "verifier_workers": 12, "length_bucket_width": 256, "required_device": "cuda"},
        "extractor_id": "ganesh-code-fence-v1",
        "adapter": {
            "dir": str(runtime_training_dir / "checkpoints" / name / "adapter"),
            "run_evidence": str(runtime_training_dir / "run-evidence.json"),
            "checkpoint_manifest": str(runtime_training_dir / "checkpoints" / name / "manifest.json"),
            "served_model_id": served_id,
        },
    }


def build(
    run_path: Path,
    checkpoints_dir: Path,
    runtime_training_dir: Path,
    served_model_prefix: str = "ganesh-mini-1.0-expansion-pilot-v1",
) -> tuple[list[tuple[str, dict[str, Any]]], dict[str, Any]]:
    if not SERVED_MODEL_PREFIX_RE.fullmatch(served_model_prefix):
        raise ValueError("served model prefix must be a lowercase identifier")
    run = load_sealed(run_path, "evidence_sha256")
    if run.get("status") != "complete":
        raise ValueError("checkpoint sweep requires a complete training run")
    checkpoints: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for path in sorted(checkpoints_dir.glob("tokens-*/manifest.json")):
        checkpoint = load_sealed(path, "manifest_sha256")
        if checkpoint.get("status") != "complete" or checkpoint.get("identities") != run.get("identities"):
            raise ValueError(f"checkpoint does not bind the complete training run: {path}")
        checkpoints.append(
            (
                path.parent.name,
                checkpoint_config(path.parent.name, runtime_training_dir, served_model_prefix),
                checkpoint,
            )
        )
    if len(checkpoints) != 6:
        raise ValueError(f"expected six saved checkpoints, found {len(checkpoints)}")
    configs = [(name, config) for name, config, _ in checkpoints[:-1]]
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-checkpoint-sweep/v1",
        "status": "diagnostic-only",
        "training_run_evidence_sha256": run["evidence_sha256"],
        "measured_final_checkpoint": checkpoints[-1][0],
        "unmeasured_checkpoint_count": len(configs),
        "checkpoint_manifest_sha256": {name: checkpoint["manifest_sha256"] for name, _, checkpoint in checkpoints},
        "config_sha256": {name: canonical_digest(config) for name, config in configs},
        "task_surface": "private development tranche 1",
        "task_count_per_checkpoint": 30,
        "promotion_authority": "none",
    }
    manifest["manifest_sha256"] = canonical_digest(manifest)
    return configs, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--checkpoints", type=Path, required=True)
    parser.add_argument("--runtime-training-dir", type=Path, default=Path("/training"))
    parser.add_argument(
        "--served-model-prefix",
        default="ganesh-mini-1.0-expansion-pilot-v1",
        help="identity prefix used by each diagnostic checkpoint config",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    configs, manifest = build(
        args.run,
        args.checkpoints,
        args.runtime_training_dir,
        args.served_model_prefix,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, config in configs:
        (args.output_dir / f"{name}.json").write_text(json.dumps(config, indent=2, sort_keys=True) + "\n")
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": manifest["status"], "checkpoint_count": len(configs), "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
