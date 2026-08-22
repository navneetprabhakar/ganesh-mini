#!/usr/bin/env python3
"""Execute bounded, evidence-preserving Qwen3.5 Gate 0 runtime probes.

Large artifacts stay below ignored ``models/`` and ``outputs/`` paths.  The
small JSON evidence written by this program is safe to commit.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import platform
import resource
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write_evidence(value: dict[str, Any], path: Path) -> None:
    value["evidence_sha256"] = digest(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def runtime_identity() -> dict[str, Any]:
    import peft
    import torch
    import transformers

    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "peft": peft.__version__,
        "mps_available": torch.backends.mps.is_available(),
    }


def load_contract(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_model(model_dir: Path, device: str):
    import torch
    from transformers import AutoModelForImageTextToText, AutoTokenizer

    dtype = torch.bfloat16 if device == "mps" else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    started = time.monotonic()
    model = AutoModelForImageTextToText.from_pretrained(
        model_dir,
        local_files_only=True,
        dtype=dtype,
        attn_implementation="eager",
    )
    model.to(device)
    return tokenizer, model, time.monotonic() - started


def inference(args: argparse.Namespace) -> int:
    import torch

    contract = load_contract(args.contract)
    device = "mps" if torch.backends.mps.is_available() and not args.cpu else "cpu"
    started = time.monotonic()
    try:
        tokenizer, model, load_seconds = load_model(args.model_dir, device)
        model.eval()
        messages = [{"role": "user", "content": args.prompt}]
        rendered = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
        )
        inputs = tokenizer(rendered, return_tensors="pt").to(device)
        with torch.inference_mode():
            generated = model.generate(
                **inputs,
                do_sample=False,
                max_new_tokens=args.max_new_tokens,
                pad_token_id=tokenizer.eos_token_id,
            )
        new_ids = generated[0, inputs.input_ids.shape[1] :]
        raw = tokenizer.decode(new_ids, skip_special_tokens=False)
        clean = tokenizer.decode(new_ids, skip_special_tokens=True)
        passed = bool(clean.strip()) and rendered.endswith("<think>\n\n</think>\n\n")
        evidence = {
            "schema_version": 1,
            "kind": "text_only_non_thinking_inference",
            "passed": passed,
            "model_id": contract["model_id"],
            "revision": contract["revision"],
            "model_dir": str(args.model_dir.resolve()),
            "runtime": runtime_identity(),
            "device": device,
            "dtype": str(next(model.parameters()).dtype),
            "load_seconds": load_seconds,
            "wall_seconds": time.monotonic() - started,
            "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "generation": {"do_sample": False, "max_new_tokens": args.max_new_tokens},
            "messages": messages,
            "rendered_prompt": rendered,
            "rendered_prompt_sha256": hashlib.sha256(rendered.encode()).hexdigest(),
            "input_tokens": int(inputs.input_ids.shape[1]),
            "output_tokens": int(new_ids.shape[0]),
            "raw_output": raw,
            "extracted_output": clean,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # fail-closed evidence is more useful than a traceback-only failure
        evidence = {
            "schema_version": 1,
            "kind": "text_only_non_thinking_inference",
            "passed": False,
            "model_id": contract["model_id"],
            "revision": contract["revision"],
            "runtime": runtime_identity(),
            "error_type": type(exc).__name__,
            "error": str(exc),
            "wall_seconds": time.monotonic() - started,
            "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
    write_evidence(evidence, args.output)
    return 0 if evidence["passed"] else 2


def _select_records(path: Path, tokenizer, count: int, max_length: int) -> list[dict[str, Any]]:
    candidates = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            rendered = tokenizer.apply_chat_template(row["messages"], tokenize=False, add_generation_prompt=False)
            token_count = len(tokenizer(rendered, add_special_tokens=False).input_ids)
            if token_count <= max_length:
                candidates.append((token_count, row, rendered))
    candidates.sort(key=lambda item: (item[0], item[1]["id"]))
    if len(candidates) < count:
        raise ValueError(f"only {len(candidates)} records fit max_length={max_length}")
    return [{"row": row, "rendered": rendered, "tokens": size} for size, row, rendered in candidates[:count]]


def lora_train(args: argparse.Namespace) -> int:
    import torch
    from peft import LoraConfig, PeftModel, get_peft_model

    contract = load_contract(args.contract)
    device = "mps" if torch.backends.mps.is_available() and not args.cpu else "cpu"
    started = time.monotonic()
    evidence: dict[str, Any]
    catalog: dict[str, Any] | None = None
    try:
        tokenizer, base, load_seconds = load_model(args.model_dir, device)
        # Exact suffixes are derived from this runtime object, never copied from
        # another architecture. Conv1d/state parameters are not Linear modules.
        all_linear = [(name, module) for name, module in base.named_modules() if isinstance(module, torch.nn.Linear)]
        language_linear = [
            (name, module)
            for name, module in all_linear
            if name.startswith("model.language_model.") and not name.endswith("lm_head")
        ]
        target_suffixes = sorted({name.rsplit(".", 1)[-1] for name, _ in language_linear})
        config = LoraConfig(
            r=args.rank,
            lora_alpha=args.rank * 2,
            lora_dropout=0.0,
            target_modules=target_suffixes,
            bias="none",
            task_type="CAUSAL_LM",
        )
        model = get_peft_model(base, config)
        records = _select_records(args.records, tokenizer, args.record_count, args.max_length)
        optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=args.learning_rate)
        losses = []
        gradient_names: set[str] = set()
        model.train()
        for item in records:
            encoded = tokenizer(
                item["rendered"], return_tensors="pt", truncation=True, max_length=args.max_length
            ).to(device)
            labels = encoded.input_ids.clone()
            # Gate 0 tests mechanics. The production response-only collator is
            # qualified separately before Gate 3; this probe uses full LM loss.
            optimizer.zero_grad(set_to_none=True)
            output = model(**encoded, labels=labels)
            if not torch.isfinite(output.loss):
                raise RuntimeError(f"non-finite loss at record {item['row']['id']}")
            output.loss.backward()
            for name, parameter in model.named_parameters():
                if parameter.requires_grad and parameter.grad is not None and torch.count_nonzero(parameter.grad).item() > 0:
                    gradient_names.add(name)
            optimizer.step()
            losses.append(float(output.loss.detach().cpu()))

        trainable = [(name, p) for name, p in model.named_parameters() if "lora_" in name]
        modules = []
        for name, module in all_linear:
            suffix = name.rsplit(".", 1)[-1]
            targeted = name.startswith("model.language_model.") and suffix in target_suffixes
            related_grad = any(name in grad_name for grad_name in gradient_names)
            modules.append(
                {
                    "name": name,
                    "type": "torch.nn.Linear",
                    "num_parameters": sum(p.numel() for p in module.parameters(recurse=False)),
                    "lora_targeted": targeted,
                    "adapter_trainable_parameters": sum(
                        p.numel() for grad_name, p in trainable if targeted and name in grad_name
                    ),
                    "adapter_gradient_observed": related_grad if targeted else False,
                }
            )
        catalog = {
            "schema_version": 1,
            "source_kind": "runtime_named_modules",
            "model_id": contract["model_id"],
            "revision": contract["revision"],
            "gradient_probe_passed": bool(gradient_names),
            "target_suffixes": target_suffixes,
            "modules": modules,
        }
        args.catalog_output.parent.mkdir(parents=True, exist_ok=True)
        args.catalog_output.write_text(json.dumps(catalog, indent=2, sort_keys=True) + "\n")

        args.adapter_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(args.adapter_dir, safe_serialization=True)
        tokenizer.save_pretrained(args.adapter_dir)
        adapter_files = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(args.adapter_dir.iterdir())
            if path.is_file()
        }
        # Free the optimizer/MPS graph before reload and merge.
        del optimizer, model, base, all_linear, language_linear, trainable, modules
        gc.collect()
        if device == "mps":
            torch.mps.empty_cache()
        _, reload_base, _ = load_model(args.model_dir, device)
        reloaded = PeftModel.from_pretrained(reload_base, args.adapter_dir, is_trainable=False)
        merged = reloaded.merge_and_unload(safe_merge=True)
        merged.eval()
        probe = tokenizer("def add(a, b):", return_tensors="pt").to(device)
        with torch.inference_mode():
            logits = merged(**probe).logits
        merge_finite = bool(torch.isfinite(logits).all().item())
        passed = len(losses) == args.record_count and all(x > 0 for x in losses) and bool(gradient_names) and merge_finite
        evidence = {
            "schema_version": 1,
            "kind": "train_save_reload_merge_smoke",
            "passed": passed,
            "model_id": contract["model_id"],
            "revision": contract["revision"],
            "runtime": runtime_identity(),
            "device": device,
            "load_seconds": load_seconds,
            "record_ids": [item["row"]["id"] for item in records],
            "record_tokens": [item["tokens"] for item in records],
            "max_length": args.max_length,
            "rank": args.rank,
            "learning_rate": args.learning_rate,
            "target_suffixes": target_suffixes,
            "losses": losses,
            "gradient_parameter_count": len(gradient_names),
            "merge_logits_finite": merge_finite,
            "adapter_file_sha256": adapter_files,
            "catalog_sha256": digest(catalog),
            "wall_seconds": time.monotonic() - started,
            "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "scope_note": "Apple BF16 LoRA mechanics; not CUDA QLoRA qualification",
        }
    except Exception as exc:
        evidence = {
            "schema_version": 1,
            "kind": "train_save_reload_merge_smoke",
            "passed": False,
            "model_id": contract["model_id"],
            "revision": contract["revision"],
            "runtime": runtime_identity(),
            "device": device,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "wall_seconds": time.monotonic() - started,
            "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "scope_note": "Apple BF16 LoRA mechanics; not CUDA QLoRA qualification",
        }
    write_evidence(evidence, args.output)
    return 0 if evidence["passed"] else 2


def parser() -> argparse.ArgumentParser:
    root = Path(__file__).resolve().parents[2]
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--contract", type=Path, default=root / "configs/model/qwen3_5_2b.contract.json")
    common.add_argument("--model-dir", type=Path, required=True)
    common.add_argument("--cpu", action="store_true")
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    infer = sub.add_parser("inference", parents=[common])
    infer.add_argument("--prompt", default="Return only a Python function add(a, b) that returns the sum.")
    infer.add_argument("--max-new-tokens", type=int, default=48)
    infer.add_argument("--output", type=Path, required=True)
    infer.set_defaults(func=inference)
    train = sub.add_parser("lora-train", parents=[common])
    train.add_argument("--records", type=Path, default=root / "data/seed/ganesh_v01/train.jsonl")
    train.add_argument("--record-count", type=int, default=16)
    train.add_argument("--max-length", type=int, default=256)
    train.add_argument("--rank", type=int, default=4)
    train.add_argument("--learning-rate", type=float, default=1e-5)
    train.add_argument("--adapter-dir", type=Path, default=root / "outputs/gate0/adapter")
    train.add_argument("--catalog-output", type=Path, required=True)
    train.add_argument("--output", type=Path, required=True)
    train.set_defaults(func=lora_train)
    return cli


def main() -> int:
    args = parser().parse_args()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
