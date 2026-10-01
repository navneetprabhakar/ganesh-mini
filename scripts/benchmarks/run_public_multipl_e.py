#!/usr/bin/env python3
"""Generate reproducible chat completions for pinned public MultiPL-E tasks.

The output layout is accepted by MultiPL-E's network-isolated evaluator.
This script only generates text; it never executes model-produced code.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

from datasets import load_dataset

from scripts.inference.run_gguf_evaluation import LlamaCppServerBackend


ROOT = Path(__file__).resolve().parents[2]
DATASET_ID = "nuprl/MultiPL-E"
DATASET_REVISION = "28441b6024e71d4a1c1c0f6bf171c935cd5a43f2"
LANGUAGES = {"go": "Go", "java": "Java", "js": "JavaScript", "ts": "TypeScript", "rs": "Rust", "py": "Python"}
MULTIPL_E_REPO_REVISION = "3025a531af7450e7df8b96fe0440e9804480bbad"
PROMPT_TEMPLATE = (
    "Complete the following incomplete {language} program. Return the entire "
    "completed program, starting with the provided prefix exactly. Return "
    "only code, with no Markdown, tests, examples, or explanation.\n\n{prefix}"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256_text(json.dumps(value, sort_keys=True, separators=(",", ":")))


def strip_single_fence(raw: str) -> str:
    text = raw.strip()
    for ending in ("<|im_end|>", "<|endoftext|>"):
        if text.endswith(ending):
            text = text[: -len(ending)].rstrip()
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    if len(lines) < 3 or not lines[-1].strip().startswith("```"):
        return text
    return "\n".join(lines[1:-1]).strip()


def postprocess_program(
    raw: str, prefix: str, stop_tokens: list[str], *,
    stop_nonmatching_full_program: bool = False,
) -> tuple[str, bool]:
    program = strip_single_fence(raw)
    if not program.startswith(prefix):
        if stop_nonmatching_full_program:
            stop_positions = [program.find(token) for token in stop_tokens if program.find(token) >= 0]
            if stop_positions:
                program = program[:min(stop_positions)].rstrip() + "\n"
        return program, False
    suffix = program[len(prefix):]
    stop_positions = [suffix.find(token) for token in stop_tokens if suffix.find(token) >= 0]
    if stop_positions:
        suffix = suffix[:min(stop_positions)]
    return prefix + suffix.rstrip() + "\n", True


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_name(path.name + ".pending")
    pending.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(pending, path)


def write_gzip_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_name(path.name + ".pending")
    with gzip.open(pending, "wt", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
    os.replace(pending, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=LANGUAGES, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--device", choices=("mps", "cpu"), default="mps")
    parser.add_argument("--llama-cpp", type=Path, default=ROOT / "models/llama.cpp")
    parser.add_argument("--multipl-e-repo", type=Path,
                        default=ROOT / "artifacts/public-benchmark/MultiPL-E")
    parser.add_argument("--max-new-tokens", type=int, default=768)
    parser.add_argument("--max-tasks", type=int, default=0,
                        help="Deterministic SHA-256 sample of N tasks; 0 means all")
    parser.add_argument("--rust-whole-program-stop", action="store_true",
                        help="Apply published Rust stop token to full-program responses")
    args = parser.parse_args()
    if args.max_new_tokens < 1 or args.max_tasks < 0:
        parser.error("token and task limits must be nonnegative, with positive tokens")
    if args.rust_whole_program_stop and args.language != "rs":
        parser.error("--rust-whole-program-stop is Rust-only")
    model = args.model.resolve(strict=True)
    llama_root = args.llama_cpp.resolve(strict=True)
    server = llama_root / "build/bin/llama-server"
    if not server.is_file():
        raise FileNotFoundError(server)
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=llama_root, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if args.language == "py":
        benchmark_repo = args.multipl_e_repo.resolve(strict=True)
        benchmark_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=benchmark_repo, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        if benchmark_revision != MULTIPL_E_REPO_REVISION:
            raise ValueError("MultiPL-E Python benchmark repository revision changed")
        python_dataset = benchmark_repo / "datasets/HumanEvalPlus-v0.1.8.jsonl"
        dataset = []
        for line in python_dataset.read_text().splitlines():
            source = json.loads(line)
            dataset.append({
                "name": source["task_id"].replace("/", "_"),
                "language": "py",
                "prompt": source["prompt"],
                "tests": source["test"] + f"\ncheck({source['entry_point']})\n",
                "stop_tokens": [],
            })
        dataset_identity = {
            "dataset_id": "nuprl/MultiPL-E:datasets/HumanEvalPlus-v0.1.8.jsonl",
            "dataset_revision": benchmark_revision,
            "dataset_file_sha256": sha256_file(python_dataset),
            "dataset_config": "humanevalplus-py",
        }
    else:
        dataset = list(load_dataset(
            DATASET_ID, f"humaneval-{args.language}", split="test",
            revision=DATASET_REVISION,
        ))
        dataset_identity = {
            "dataset_id": DATASET_ID,
            "dataset_revision": DATASET_REVISION,
            "dataset_config": f"humaneval-{args.language}",
        }
    if args.max_tasks:
        ranked = sorted(
            range(len(dataset)),
            key=lambda index: sha256_text("ganesh-mini-public-v1:" + dataset[index]["name"]),
        )
        dataset = [dataset[index] for index in sorted(ranked[: min(args.max_tasks, len(dataset))])]
    manifest = {
        "schema_version": "ganesh-mini-public-multipl-e-generation/v1",
        "status": "in_progress",
        **dataset_identity,
        "task_count": len(dataset),
        "selection": "all" if not args.max_tasks else "lowest-sha256(ganesh-mini-public-v1:name)",
        "selected_task_names": [problem["name"] for problem in dataset],
        "model_id": args.model_id,
        "model_sha256": sha256_file(model),
        "llama_cpp_revision": revision,
        "llama_server_sha256": sha256_file(server),
        "device": args.device,
        "context_length": 8192,
        "max_new_tokens": args.max_new_tokens,
        "temperature": 0.0,
        "seed": 0,
        "prompt_template": PROMPT_TEMPLATE,
        "postprocessing": (
            "strip-chat-eos/fence; apply published stop tokens to exact-prefix suffix; "
            "apply published Rust stop to nonmatching full-program response"
            if args.rust_whole_program_stop else
            "strip-chat-eos/fence; apply published stop tokens to exact-prefix suffix"
        ),
    }
    manifest_path = output / "manifest.json"
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text())
        for key, value in manifest.items():
            if key != "status" and previous.get(key) != value:
                raise ValueError(f"existing run manifest disagrees on {key}")
    else:
        write_json_atomic(manifest_path, manifest)
    with LlamaCppServerBackend(
        server=server, model=model, llama_revision=revision, device=args.device,
        parallel=1, context_length=8192, log_path=output / "llama-server.log",
        startup_timeout_seconds=300,
    ) as backend:
        for ordinal, problem in enumerate(dataset):
            name = problem["name"]
            if "/" in name or ".." in name:
                raise ValueError(f"unsafe benchmark task name {name!r}")
            raw_path = output / "raw" / f"{name}.json"
            completion_path = output / "completions" / f"{name}.json.gz"
            if raw_path.exists() and completion_path.exists():
                continue
            if raw_path.exists() != completion_path.exists():
                raise ValueError(f"partial existing task output for {name}")
            user_prompt = PROMPT_TEMPLATE.format(
                language=LANGUAGES[args.language], prefix=problem["prompt"],
            )
            rendered, input_ids = backend.render(user_prompt)
            if len(input_ids) + args.max_new_tokens > 8192:
                raise ValueError(f"context overflow for {name}")
            output_tokens, raw_text, elapsed_ms = backend.generate_batch(
                [input_ids], args.max_new_tokens, True,
            )[0]
            program, exact_prefix = postprocess_program(
                raw_text, problem["prompt"], problem["stop_tokens"],
                stop_nonmatching_full_program=args.rust_whole_program_stop,
            )
            raw = {
                "name": name,
                "ordinal": ordinal,
                "language": args.language,
                "source_prompt_sha256": sha256_text(problem["prompt"]),
                "tests_sha256": sha256_text(problem["tests"]),
                "user_prompt": user_prompt,
                "rendered_prompt_sha256": sha256_text(rendered),
                "rendered_prompt": rendered,
                "input_token_ids": input_ids,
                "output_token_ids": output_tokens,
                "raw_output": raw_text,
                "evaluated_program": program,
                "exact_prefix_match": exact_prefix,
                "elapsed_ms": elapsed_ms,
            }
            completion = {
                "name": name,
                "language": problem["language"],
                "prompt": "",
                "original_prompt": problem["prompt"],
                "tests": problem["tests"],
                "stop_tokens": problem["stop_tokens"],
                "completions": [program],
                "raw_completions": [raw_text],
                "temperature": 0.0,
                "max_tokens": args.max_new_tokens,
            }
            write_json_atomic(raw_path, raw)
            write_gzip_json_atomic(completion_path, completion)
            print(f"{args.language} {ordinal + 1}/{len(dataset)} {name} {len(output_tokens)} tokens", flush=True)
    manifest["status"] = "completed"
    manifest["raw_file_count"] = len(list((output / "raw").glob("*.json")))
    manifest["completion_file_count"] = len(list((output / "completions").glob("*.json.gz")))
    if manifest["raw_file_count"] != len(dataset) or manifest["completion_file_count"] != len(dataset):
        raise ValueError("benchmark generation output count mismatch")
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    write_json_atomic(manifest_path, manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
