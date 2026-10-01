#!/usr/bin/env python3
"""Version Rust evaluator inputs from immutable full-program generations.

MultiPL-E's Rust tests begin with the function's closing brace. When a chat
model returns a whole program instead of only the requested body, apply the
dataset's published ``\n}`` stop token before appending those tests.
"""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

from scripts.benchmarks.run_public_multipl_e import (
    canonical_sha256,
    sha256_file,
    strip_single_fence,
    write_gzip_json_atomic,
    write_json_atomic,
)


def apply_rust_stop(raw_output: str, stop_tokens: list[str], tests: str) -> str:
    if "\n}" not in stop_tokens or not tests.startswith("}"):
        raise ValueError("Rust benchmark closing-brace contract changed")
    program = strip_single_fence(raw_output)
    position = program.find("\n}")
    if position < 0:
        raise ValueError("generated Rust program lacks published closing stop token")
    return program[:position].rstrip() + "\n"


def derive_side(source: Path, target: Path) -> None:
    if target.exists():
        raise FileExistsError(target)
    manifest = json.loads((source / "manifest.json").read_text())
    original_seal = manifest.pop("manifest_sha256", None)
    if original_seal != canonical_sha256(manifest):
        raise ValueError(f"source manifest seal mismatch: {source}")
    if manifest.get("status") != "completed" or manifest.get("task_count") != 30:
        raise ValueError(f"source generation incomplete: {source}")
    names = manifest["selected_task_names"]
    if len(names) != 30 or len(set(names)) != 30:
        raise ValueError("invalid source task selection")
    for name in names:
        raw_file = source / "raw" / f"{name}.json"
        completion_file = source / "completions" / f"{name}.json.gz"
        raw = json.loads(raw_file.read_text())
        with gzip.open(completion_file, "rt") as stream:
            completion = json.load(stream)
        if raw["name"] != name or completion["name"] != name:
            raise ValueError(f"source task mismatch: {name}")
        if completion["raw_completions"] != [raw["raw_output"]]:
            raise ValueError(f"source raw/completion mismatch: {name}")
        if completion["completions"] != [raw["evaluated_program"]]:
            raise ValueError(f"source evaluated/completion mismatch: {name}")
        corrected = apply_rust_stop(
            raw["raw_output"], completion["stop_tokens"], completion["tests"],
        )
        raw["evaluated_program"] = corrected
        raw["source_raw_json_sha256"] = sha256_file(raw_file)
        completion["completions"] = [corrected]
        completion["source_completion_sha256"] = sha256_file(completion_file)
        write_json_atomic(target / "raw" / f"{name}.json", raw)
        write_gzip_json_atomic(target / "completions" / f"{name}.json.gz", completion)
    manifest["postprocessing"] = (
        "strip-chat-eos/fence; apply published Rust newline-close-brace stop "
        "to full-program response before appended benchmark tests"
    )
    manifest["derivation"] = {
        "source_generation_manifest_sha256": original_seal,
        "source_run_directory": source.name,
        "new_model_generation": False,
    }
    manifest["raw_file_count"] = len(list((target / "raw").glob("*.json")))
    manifest["completion_file_count"] = len(list((target / "completions").glob("*.json.gz")))
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    write_json_atomic(target / "manifest.json", manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    for side in ("candidate", "upstream"):
        derive_side(
            args.root / f"sha30-v2-{side}-rs",
            args.root / f"sha30-v3-{side}-rs",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
