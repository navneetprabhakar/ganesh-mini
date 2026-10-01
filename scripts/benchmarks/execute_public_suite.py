#!/usr/bin/env python3
"""Resume the paired, sandboxed six-lane public benchmark slice sequentially."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LANGUAGES = ("go", "java", "js", "ts", "rs", "py")
FULL_COUNTS = {"go": 154, "java": 158, "js": 161, "ts": 159, "rs": 156, "py": 164}
IMAGE = (
    "ghcr.io/nuprl/multipl-e-evaluation@"
    "sha256:2cb4fcd74d89d149f7a3feb177f7d8169cef390a7ea7951c9b84e7ff59ea26cc"
)


def run_logged(command: list[str], log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as log:
        log.write("\n$ " + " ".join(command) + "\n")
        log.flush()
        subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True)


def generation_complete(path: Path, count: int) -> bool:
    manifest_path = path / "manifest.json"
    if not manifest_path.is_file():
        return False
    manifest = json.loads(manifest_path.read_text())
    return (
        manifest.get("status") == "completed"
        and manifest.get("task_count") == count
        and len(list((path / "raw").glob("*.json"))) == count
        and len(list((path / "completions").glob("*.json.gz"))) == count
    )


def verifier_complete(path: Path, count: int) -> bool:
    return len(list((path / "verified").glob("*.results.json.gz"))) == count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--candidate-model", type=Path, required=True)
    parser.add_argument("--upstream-model", type=Path, required=True)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--upstream-id", required=True)
    parser.add_argument("--max-tasks", type=int, default=30)
    parser.add_argument("--run-prefix", default="sha30-v2")
    parser.add_argument("--max-new-tokens", type=int, default=768)
    parser.add_argument("--languages", nargs="+", choices=LANGUAGES,
                        default=list(LANGUAGES))
    args = parser.parse_args()
    if args.max_tasks not in (0, 30):
        raise ValueError("controller supports only the frozen 30-task slice or full suite")
    if args.max_tasks == 0 and args.run_prefix == "sha30-v2":
        raise ValueError("full suite requires a distinct versioned run prefix")
    if not args.run_prefix or "/" in args.run_prefix or ".." in args.run_prefix:
        raise ValueError("unsafe run prefix")
    root = args.output_root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    models = {
        "candidate": (args.candidate_model.resolve(strict=True), args.candidate_id),
        "upstream": (args.upstream_model.resolve(strict=True), args.upstream_id),
    }
    for language in args.languages:
        task_count = FULL_COUNTS[language] if args.max_tasks == 0 else 30
        for side in ("candidate", "upstream"):
            path = root / f"{args.run_prefix}-{side}-{language}"
            model_path, model_id = models[side]
            if not generation_complete(path, task_count):
                print(f"Generating {side} {language}", flush=True)
                generation_command = [
                    sys.executable, "-m", "scripts.benchmarks.run_public_multipl_e",
                    "--language", language,
                    "--model", str(model_path),
                    "--model-id", model_id,
                    "--output-dir", str(path),
                    "--max-tasks", str(args.max_tasks),
                    "--max-new-tokens", str(args.max_new_tokens),
                ]
                if args.max_tasks == 0 and language == "rs":
                    generation_command.append("--rust-whole-program-stop")
                run_logged(generation_command, path / "generation-controller.log")
            if not generation_complete(path, task_count):
                raise ValueError(f"incomplete generation for {side} {language}")
            if not verifier_complete(path, task_count):
                print(f"Verifying {side} {language} in network-disabled container", flush=True)
                verified = path / "verified"
                verified.mkdir(parents=True, exist_ok=True)
                run_logged([
                    "docker", "run", "--rm", "--platform", "linux/amd64",
                    "--network", "none", "--cpus", "2", "--memory", "4g",
                    "--pids-limit", "128", "--cap-drop", "ALL",
                    "--security-opt", "no-new-privileges",
                    "-v", f"{path / 'completions'}:/benchmark:ro",
                    "-v", f"{verified}:/output:rw",
                    IMAGE, "--dir", "/benchmark", "--output-dir", "/output",
                    "--max-workers", "1",
                ], path / "verification-controller.log")
            if not verifier_complete(path, task_count):
                raise ValueError(f"incomplete verifier outputs for {side} {language}")
            print(f"Completed {side} {language}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
