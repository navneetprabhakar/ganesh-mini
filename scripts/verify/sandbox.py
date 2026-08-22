from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from scripts.eval.contracts import ContractError, sha256_object, sha256_text, validate_task


SANDBOX_CONTRACT = {
    "backend": "docker",
    "network": "none",
    "read_only_root": True,
    "cap_drop": "ALL",
    "no_new_privileges": True,
    "pull": "never",
    "shell": False,
    "tmpfs": [
        "/tmp:rw,noexec,nosuid,nodev,size=64m",
        "/exec:rw,exec,nosuid,nodev,size=256m",
    ],
    "ulimit_nofile": "128:128",
}


def load_runtime(path: Path, runtime_id: str, language: str, candidate_path: str) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    if set(config) != {"schema_version", "runtimes"} or config["schema_version"] != "1.0":
        raise ContractError("runtime config: unsupported or unexpected keys")
    runtime = config["runtimes"].get(runtime_id)
    if not isinstance(runtime, dict):
        raise ContractError(f"runtime config: missing {runtime_id!r}")
    if set(runtime) != {"language", "image", "candidate_path", "commands"}:
        raise ContractError("runtime config: unexpected runtime keys")
    if runtime["language"] != language or runtime["candidate_path"] != candidate_path:
        raise ContractError("runtime config: language or candidate path mismatch")
    image = runtime["image"]
    if not isinstance(image, str) or "@sha256:" not in image:
        raise ContractError("runtime config: image is not digest-pinned")
    digest = image.rsplit("@sha256:", 1)[1]
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise ContractError("runtime config: malformed image digest")
    commands = runtime["commands"]
    if not isinstance(commands, list) or not commands or not all(
        isinstance(command, list) and command and all(isinstance(part, str) and part for part in command)
        for command in commands
    ):
        raise ContractError("runtime config: commands must be non-empty argv arrays")
    return runtime


def _inspect_image(image: str) -> str:
    try:
        process = subprocess.run(
            ["docker", "image", "inspect", image, "--format", "{{.Id}}"],
            check=False, capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ContractError(f"docker image inspection failed: {error}") from error
    image_id = process.stdout.strip()
    if process.returncode != 0 or not image_id.startswith("sha256:") or len(image_id) != 71:
        raise ContractError(f"docker image unavailable or invalid: {process.stderr.strip()}")
    requested_digest = image.rsplit("@", 1)[1]
    if image_id != requested_digest:
        raise ContractError(f"docker image ID {image_id} differs from requested digest {requested_digest}")
    return image_id


def _docker_argv(image: str, command: list[str], root: Path, limits: dict[str, Any]) -> list[str]:
    return [
        "docker", "run", "--rm", "--pull", "never", "--init",
        "--network", "none", "--read-only", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges", "--pids-limit", str(limits["pids"]),
        "--cpus", str(limits["cpus"]), "--memory", f"{limits['memory_mb']}m",
        "--ulimit", "nofile=128:128",
        "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=64m",
        "--tmpfs", "/exec:rw,exec,nosuid,nodev,size=256m",
        "--user", f"{os.getuid()}:{os.getgid()}",
        "--mount", f"type=bind,src={root},dst=/work", "--workdir", "/work",
        "--env", "HOME=/tmp", "--env", "TMPDIR=/exec",
        "--env", "GOTMPDIR=/exec", "--env", "NO_COLOR=1",
        "--entrypoint", command[0], image, *command[1:],
    ]


def verify(task: dict[str, Any], code: str, runtime_config: Path) -> dict[str, Any]:
    validate_task(task)
    runtime = load_runtime(runtime_config, task["runtime_id"], task["language"], task["candidate_path"])
    image_id = _inspect_image(runtime["image"])
    limits = task["limits"]
    stdout_parts: list[str] = []
    stderr_parts: list[str] = []
    exit_codes: list[int] = []
    timed_out = False
    start = time.monotonic()

    with tempfile.TemporaryDirectory(prefix="ganesh-eval-") as temporary:
        root = Path(temporary).resolve()
        for item in task["files"]:
            target = (root / item["path"]).resolve()
            if root not in target.parents:
                raise ContractError("task file escaped sandbox root")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(item["content"], encoding="utf-8")
        candidate = (root / task["candidate_path"]).resolve()
        candidate.parent.mkdir(parents=True, exist_ok=True)
        candidate.write_text(code, encoding="utf-8")

        deadline = start + limits["timeout_seconds"]
        for command in runtime["commands"]:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                break
            try:
                process = subprocess.run(
                    _docker_argv(runtime["image"], command, root, limits),
                    check=False, capture_output=True, text=True, timeout=remaining,
                    env={"PATH": os.environ.get("PATH", "")},
                )
            except subprocess.TimeoutExpired as error:
                timed_out = True
                stdout_parts.append(error.stdout or "")
                stderr_parts.append(error.stderr or "")
                break
            except OSError as error:
                stderr_parts.append(str(error))
                exit_codes.append(127)
                break
            stdout_parts.append(process.stdout)
            stderr_parts.append(process.stderr)
            exit_codes.append(process.returncode)
            if process.returncode != 0:
                break

    output_limit = limits["output_bytes"]
    stdout = "".join(stdout_parts).encode("utf-8")[:output_limit].decode("utf-8", errors="replace")
    stderr = "".join(stderr_parts).encode("utf-8")[:output_limit].decode("utf-8", errors="replace")
    duration_ms = max(0, round((time.monotonic() - start) * 1000))
    return {
        "runtime_id": task["runtime_id"],
        "image": runtime["image"],
        "image_id": image_id,
        "commands": runtime["commands"],
        "exit_codes": exit_codes,
        "timed_out": timed_out,
        "stdout": stdout,
        "stdout_sha256": sha256_text(stdout),
        "stderr": stderr,
        "stderr_sha256": sha256_text(stderr),
        "duration_ms": duration_ms,
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
    }
