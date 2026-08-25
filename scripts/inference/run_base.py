#!/usr/bin/env python3
"""Run the pinned Qwen base through frozen tasks and retain exact evidence.

The checked-in configuration is intentionally restricted to the six synthetic
harness fixtures.  It is control-plane evidence, never a model-quality score.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import resource
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from scripts.eval.contracts import (
    canonical_json,
    load_json,
    sha256_bytes,
    sha256_object,
    sha256_text,
    validate_result,
    validate_task,
)
from scripts.eval.run_task import build_result
from scripts.inference.extract import EXTRACTOR_ID, extract_code
from scripts.verify.sandbox import infrastructure_failure, verify


ROOT = Path(__file__).resolve().parents[2]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).encode() + b"\n")
    os.replace(temporary, path)


def seal(value: dict[str, Any], field: str) -> dict[str, Any]:
    sealed = dict(value)
    sealed[field] = sha256_object(sealed)
    return sealed


def peak_rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def implementation_identity() -> dict[str, str]:
    paths = {
        "runner": ROOT / "scripts/inference/run_base.py",
        "extractor": ROOT / "scripts/inference/extract.py",
        "eval_result_builder": ROOT / "scripts/eval/run_task.py",
        "sandbox_verifier": ROOT / "scripts/verify/sandbox.py",
    }
    return {name + "_sha256": sha256_file(path) for name, path in paths.items()}


def directory_artifact_sha256(model_dir: Path, inventory: dict[str, Any]) -> str:
    entries = []
    for item in inventory["files"]:
        path = model_dir / item["path"]
        if path.is_file():
            actual_sha = sha256_file(path)
            if "sha256" in item and actual_sha != item["sha256"]:
                raise ValueError(f"pinned model hash mismatch: {item['path']}")
            if path.stat().st_size != item["size"]:
                raise ValueError(f"pinned model size mismatch: {item['path']}")
            entries.append({"path": item["path"], "size": path.stat().st_size, "sha256": actual_sha})
    required = {item["path"] for item in inventory["files"]}
    observed = {item["path"] for item in entries}
    if required != observed:
        raise FileNotFoundError(f"model inventory mismatch: missing={sorted(required - observed)}")
    return sha256_object(entries)


def runtime_identity() -> dict[str, Any]:
    try:
        import torch
        import transformers
        return {
            "python": platform.python_version(), "platform": platform.platform(),
            "torch": torch.__version__, "transformers": transformers.__version__,
            "device": "mps" if torch.backends.mps.is_available() else "cpu",
        }
    except ImportError:
        return {"python": platform.python_version(), "platform": platform.platform()}


class Backend(Protocol):
    load_ms: int
    identity: dict[str, Any]
    eos_token_id: int

    def render(self, prompt: str) -> tuple[str, list[int]]: ...
    def generate(self, input_ids: list[int], max_new_tokens: int, use_cache: bool) -> tuple[list[int], str, int]: ...


class TransformersBackend:
    def __init__(self, model_dir: Path) -> None:
        import torch
        from transformers import AutoModelForImageTextToText, AutoTokenizer

        started = time.perf_counter()
        self.torch = torch
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.dtype = torch.bfloat16 if self.device == "mps" else torch.float32
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_dir, local_files_only=True, dtype=self.dtype, attn_implementation="eager"
        ).to(self.device)
        self.model.eval()
        self.eos_token_id = int(self.tokenizer.eos_token_id)
        self.load_ms = round((time.perf_counter() - started) * 1000)
        self.identity = {**runtime_identity(), "dtype": str(next(self.model.parameters()).dtype)}

    def render(self, prompt: str) -> tuple[str, list[int]]:
        rendered = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False,
            add_generation_prompt=True, enable_thinking=False,
        )
        ids = self.tokenizer(rendered, add_special_tokens=False).input_ids
        return rendered, ids

    def generate(self, input_ids: list[int], max_new_tokens: int, use_cache: bool) -> tuple[list[int], str, int]:
        torch = self.torch
        encoded = torch.tensor([input_ids], dtype=torch.long, device=self.device)
        started = time.perf_counter()
        with torch.inference_mode():
            generated = self.model.generate(
                input_ids=encoded, attention_mask=torch.ones_like(encoded), do_sample=False,
                max_new_tokens=max_new_tokens, use_cache=use_cache,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        generation_ms = round((time.perf_counter() - started) * 1000)
        output_ids = generated[0, len(input_ids):].detach().cpu().tolist()
        return output_ids, self.tokenizer.decode(output_ids, skip_special_tokens=False), generation_ms


def validate_config(config: dict[str, Any]) -> None:
    if config.get("schema_version") != "1.0":
        raise ValueError("unsupported config schema_version")
    if config.get("classification") != "synthetic_harness_non_benchmark":
        raise ValueError("this runner configuration must be synthetic/non-benchmark")
    if config.get("allowed_surface") != "synthetic_harness":
        raise ValueError("checked-in base runner is restricted to synthetic_harness")
    serving = config["serving"]
    generation = config["generation"]
    if serving != {
        "modality": "text-only", "enable_thinking": False,
        "context_length": 8192, "add_generation_prompt": True,
    }:
        raise ValueError("serving contract must be exact text-only/non-thinking/8192")
    if generation.get("do_sample") is not False or not 1 <= generation.get("max_new_tokens", 0) <= 4096:
        raise ValueError("generation must be bounded greedy decoding")
    if config.get("extractor_id") != EXTRACTOR_ID:
        raise ValueError("unknown extractor_id")


def model_identity(config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = load_json(ROOT / config["model_contract"])
    inventory = load_json(ROOT / config["model_inventory"])
    if contract["revision"] != inventory["revision"]:
        raise ValueError("model contract and inventory revisions differ")
    artifact = directory_artifact_sha256(ROOT / config["model_dir"], inventory)
    return contract, {
        "model_id": contract["model_id"], "revision": contract["revision"],
        "artifact_sha256": artifact,
        "serving_contract_sha256": sha256_object(contract["serving_contract"]),
        "inventory_sha256": sha256_object(inventory),
    }


def completed_evidence(path: Path, task_sha256: str, config_sha256: str) -> dict[str, Any] | None:
    if not path.exists():
        return None
    evidence = load_json(path)
    supplied = evidence.get("evidence_sha256")
    unhashed = dict(evidence)
    unhashed.pop("evidence_sha256", None)
    if supplied != sha256_object(unhashed):
        raise ValueError(f"resume evidence hash mismatch: {path}")
    if evidence.get("task", {}).get("task_sha256") != task_sha256:
        raise ValueError(f"resume task hash mismatch: {path}")
    if evidence.get("task", {}).get("config_sha256") != config_sha256:
        raise ValueError(f"resume config hash mismatch: {path}")
    if evidence.get("runtime", {}).get("implementation") != implementation_identity():
        raise ValueError(f"resume implementation hash mismatch: {path}")
    validate_result(evidence["verification"]["result"])
    return evidence


def run_task(
    *, task_path: Path, task: dict[str, Any], config: dict[str, Any], config_sha256: str,
    model: dict[str, Any], backend: Backend, runtimes: Path,
) -> dict[str, Any]:
    task_hash = sha256_object(task)
    started_at = utc_now()
    task_started = time.perf_counter()
    rendered, input_ids = backend.render(task["prompt"]["text"])
    max_new = config["generation"]["max_new_tokens"]
    if len(input_ids) + max_new > config["serving"]["context_length"]:
        raise ValueError(f"{task['task_id']}: prompt plus generation exceeds context")
    output_ids, raw_output, generation_ms = backend.generate(
        input_ids, max_new, config["generation"]["use_cache"]
    )
    extraction_started = time.perf_counter()
    code, extraction = extract_code(raw_output, task["language"])
    extraction_ms = round((time.perf_counter() - extraction_started) * 1000)
    verifier_started = time.perf_counter()
    # Synthetic fixtures intentionally carry a model-agnostic placeholder in
    # rendered_prompt.  Project the exact model rendering into the result task
    # so the verifier result never claims the placeholder was served.
    inference_task = dict(task)
    inference_task["rendered_prompt"] = {"text": rendered, "sha256": sha256_text(rendered)}
    validate_task(inference_task)
    verifier = verify(inference_task, code, runtimes)
    verifier_failure = infrastructure_failure(verifier)
    if verifier_failure is not None:
        raise RuntimeError(f"{task['task_id']}: {verifier_failure}")
    verifier_ms = round((time.perf_counter() - verifier_started) * 1000)
    completed_at = utc_now()
    inference = {
        "parameters": {
            **config["serving"], **config["generation"],
            "input_tokens": len(input_ids), "output_tokens": len(output_ids),
        },
        "started_at": started_at,
        "completed_at": completed_at,
    }
    result = build_result(inference_task, raw_output, code, EXTRACTOR_ID, {
        key: model[key] for key in ("model_id", "revision", "artifact_sha256", "serving_contract_sha256")
    }, inference, verifier)
    evidence = {
        "schema_version": "1.0", "classification": config["classification"],
        "run_id": config["run_id"],
        "task": {
            "task_id": task["task_id"], "task_path": str(task_path.relative_to(ROOT)),
            "surface": task["surface"], "language": task["language"],
            "task_sha256": task_hash, "config_sha256": config_sha256,
            "fixture_rendered_prompt_sha256": task["rendered_prompt"]["sha256"],
            "inference_task_sha256": sha256_object(inference_task),
        },
        "model": model, "runtime": {**backend.identity, "implementation": implementation_identity()},
        "prompt": {
            "messages": [{"role": "user", "content": task["prompt"]["text"]}],
            "messages_sha256": sha256_object([{"role": "user", "content": task["prompt"]["text"]}]),
            "rendered": rendered, "rendered_sha256": sha256_text(rendered),
            "input_token_ids": input_ids, "input_token_ids_sha256": sha256_bytes(canonical_json(input_ids)),
        },
        "generation": {
            "raw_output": raw_output, "raw_output_sha256": sha256_text(raw_output),
            "output_token_ids": output_ids, "output_token_ids_sha256": sha256_bytes(canonical_json(output_ids)),
            "stopped_at_eos": bool(output_ids and output_ids[-1] == backend.eos_token_id),
        },
        "extraction": {
            **extraction, "extracted_code": code, "extracted_code_sha256": sha256_text(code),
        },
        "verification": {"result": result, "result_sha256": result["result_sha256"]},
        "timings_ms": {
            "model_load_once": backend.load_ms, "generation": generation_ms,
            "extraction": extraction_ms, "verifier": verifier_ms,
            "task_total": round((time.perf_counter() - task_started) * 1000),
        },
        "memory": {"process_peak_rss_bytes": peak_rss_bytes()},
        "recorded_at": completed_at,
    }
    return seal(evidence, "evidence_sha256")


def build_manifest(
    config: dict[str, Any], config_sha256: str, model: dict[str, Any], runtime: dict[str, Any],
    tasks: list[dict[str, Any]], started_at: str,
) -> dict[str, Any]:
    complete = [item for item in tasks if item["status"] == "complete"]
    passed = sum(item["passed"] is True for item in complete)
    failed = sum(item["passed"] is False for item in complete)
    pending = len(tasks) - len(complete)
    manifest = {
        "schema_version": "1.0", "run_id": config["run_id"],
        "classification": config["classification"],
        "status": "complete" if pending == 0 else "incomplete",
        "config_sha256": config_sha256, "model": model, "runtime": runtime,
        "task_accounting": {
            "expected": len(tasks), "completed": len(complete), "passed": passed,
            "failed": failed, "pending": pending,
        },
        "tasks": tasks, "started_at": started_at,
        "completed_at": utc_now() if pending == 0 else None,
    }
    return seal(manifest, "run_sha256")


def execute(config_path: Path, backend: Backend | None = None) -> dict[str, Any]:
    config = load_json(config_path)
    validate_config(config)
    config_sha = sha256_object(config)
    contract, model = model_identity(config)
    if contract["serving_contract"] != {
        "modality": "text-only", "thinking": False, "context_length": 8192,
        "chat_template_source": "chat_template.jinja",
    }:
        raise ValueError("pinned upstream serving contract changed")
    task_paths = sorted(ROOT.glob(config["task_glob"]))
    if len(task_paths) != 6:
        raise ValueError(f"synthetic proof requires exactly six tasks, found {len(task_paths)}")
    tasks = [(path, validate_task(load_json(path))) for path in task_paths]
    if any(task["surface"] != config["allowed_surface"] for _, task in tasks):
        raise ValueError("non-synthetic task rejected by checked-in configuration")
    backend = backend or TransformersBackend(ROOT / config["model_dir"])
    output_dir = ROOT / config["output_dir"]
    started_at = utc_now()
    rows: list[dict[str, Any]] = []
    for task_path, task in tasks:
        path = output_dir / "tasks" / f"{task['task_id']}.json"
        previous = completed_evidence(path, sha256_object(task), config_sha)
        if previous is None:
            evidence = run_task(
                task_path=task_path, task=task, config=config, config_sha256=config_sha,
                model=model, backend=backend, runtimes=ROOT / config["runtimes"],
            )
            atomic_json(path, evidence)
        else:
            evidence = previous
        rows.append({
            "task_id": task["task_id"], "status": "complete",
            "passed": evidence["verification"]["result"]["passed"],
            "evidence_path": str(path.relative_to(ROOT)),
            "evidence_sha256": evidence["evidence_sha256"],
        })
        atomic_json(output_dir / "run.json", build_manifest(
            config, config_sha, model,
            {**backend.identity, "implementation": implementation_identity()}, rows + [
            {"task_id": pending[1]["task_id"], "status": "pending", "passed": None,
             "evidence_path": None, "evidence_sha256": None}
            for pending in tasks[len(rows):]
        ], started_at))
    return load_json(output_dir / "run.json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/inference/qwen_base_synthetic.json")
    args = parser.parse_args()
    manifest = execute(args.config.resolve())
    accounting = manifest["task_accounting"]
    print(json.dumps({
        "classification": manifest["classification"], "status": manifest["status"],
        "completed": accounting["completed"], "passed": accounting["passed"],
        "failed": accounting["failed"], "run_sha256": manifest["run_sha256"],
    }, sort_keys=True))
    return 0 if manifest["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
