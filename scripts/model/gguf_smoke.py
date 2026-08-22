#!/usr/bin/env python3
"""Run the pinned text-only serving contract against base F16 and Q8 GGUFs."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--source-model-dir", type=Path, required=True)
    parser.add_argument("--inference-evidence", type=Path, required=True)
    parser.add_argument("--llama-cli", type=Path, required=True)
    parser.add_argument("--converter", type=Path, required=True)
    parser.add_argument("--quantizer", type=Path, required=True)
    parser.add_argument("--llama-revision", required=True)
    parser.add_argument("--f16", type=Path, required=True)
    parser.add_argument("--q8", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text())
    upstream = json.loads(args.inference_evidence.read_text())
    prompt = upstream["rendered_prompt"]
    user_prompt = upstream["messages"][0]["content"]
    results = []
    for quantization, model_path in (("F16", args.f16), ("Q8_0", args.q8)):
        command = [
            str(args.llama_cli), "-m", str(model_path), "-p", user_prompt,
            "-n", "48", "-c", str(contract["serving_contract"]["context_length"]),
            "--temp", "0", "--seed", "0", "-ngl", "999",
            "--no-display-prompt", "--no-warmup", "-cnv", "-st",
            "--chat-template-kwargs", '{"enable_thinking":false}', "--reasoning", "off",
        ]
        started = time.monotonic()
        try:
            completed = subprocess.run(
                command, text=True, capture_output=True, timeout=args.timeout_seconds, check=False
            )
            returncode = completed.returncode
            stdout = completed.stdout
            stderr = completed.stderr
            timed_out = False
        except subprocess.TimeoutExpired as exc:
            returncode = None
            stdout = (exc.stdout or b"").decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            stderr = (exc.stderr or b"").decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            timed_out = True
        wall = time.monotonic() - started
        passed = returncode == 0 and "def add" in stdout and "return a + b" in stdout
        results.append({
            "quantization": quantization,
            "passed": passed,
            "path": str(model_path.resolve()),
            "bytes": model_path.stat().st_size,
            "sha256": sha256_file(model_path),
            "command": command,
            "returncode": returncode,
            "timed_out": timed_out,
            "timeout_seconds": args.timeout_seconds,
            "stdout": stdout,
            "stderr": stderr,
            "wall_seconds": wall,
        })
    evidence = {
        "schema_version": 1,
        "kind": "base_gguf_f16_q8_smoke",
        "passed": all(item["passed"] for item in results),
        "model_id": contract["model_id"],
        "revision": contract["revision"],
        "llama_cpp_revision": args.llama_revision,
        "llama_cli_sha256": sha256_file(args.llama_cli),
        "converter_sha256": sha256_file(args.converter),
        "quantizer_sha256": sha256_file(args.quantizer),
        "export_contract": {
            "f16_command": [str(args.converter), str(args.source_model_dir), "--outtype", "f16"],
            "q8_command": [str(args.quantizer), "<F16_GGUF>", "<Q8_GGUF>", "Q8_0"],
        },
        "rendered_prompt": prompt,
        "rendered_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "user_prompt": user_prompt,
        "results": results,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    evidence["evidence_sha256"] = digest(evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    return 0 if evidence["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
