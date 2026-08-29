from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import uuid
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
    "platform": "linux/amd64",
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
    if set(config) != {"schema_version", "platform", "runtimes"} or config["schema_version"] != "3.0":
        raise ContractError("runtime config: unsupported or unexpected keys")
    if config["platform"] != "linux/amd64":
        raise ContractError("runtime config: verifier platform must be linux/amd64")
    runtime = config["runtimes"].get(runtime_id)
    if not isinstance(runtime, dict):
        raise ContractError(f"runtime config: missing {runtime_id!r}")
    if set(runtime) != {
        "language", "image", "image_id", "manifest_digest", "rootfs_layers",
        "platform", "candidate_path", "commands",
    }:
        raise ContractError("runtime config: unexpected runtime keys")
    if runtime["language"] != language or runtime["candidate_path"] != candidate_path:
        raise ContractError("runtime config: language or candidate path mismatch")
    if runtime["platform"] != config["platform"]:
        raise ContractError("runtime config: runtime platform mismatch")
    image = runtime["image"]
    if not isinstance(image, str) or not image or "@" in image:
        raise ContractError("runtime config: image must be one locally resolvable tag")
    image_id = runtime["image_id"]
    if not isinstance(image_id, str) or not image_id.startswith("sha256:"):
        raise ContractError("runtime config: missing exact image ID")
    digest = image_id.removeprefix("sha256:")
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise ContractError("runtime config: malformed image ID")
    manifest_digest = runtime["manifest_digest"]
    if not isinstance(manifest_digest, str) or not manifest_digest.startswith("sha256:"):
        raise ContractError("runtime config: missing manifest digest")
    digest = manifest_digest.removeprefix("sha256:")
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise ContractError("runtime config: malformed manifest digest")
    layers = runtime["rootfs_layers"]
    if not isinstance(layers, list) or not layers or any(
        not isinstance(layer, str) or not layer.startswith("sha256:") or len(layer) != 71 for layer in layers
    ):
        raise ContractError("runtime config: invalid rootfs layers")
    commands = runtime["commands"]
    if not isinstance(commands, list) or not commands or not all(
        isinstance(command, list) and command and all(isinstance(part, str) and part for part in command)
        for command in commands
    ):
        raise ContractError("runtime config: commands must be non-empty argv arrays")
    return runtime


def _inspect_image(
    image: str, expected_image_id: str, expected_manifest_digest: str,
    expected_rootfs_layers: list[str], expected_platform: str,
) -> str:
    try:
        process = subprocess.run(
            ["docker", "image", "inspect", image, "--format", "{{json .}}"],
            check=False, capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ContractError(f"docker image inspection failed: {error}") from error
    try:
        inspected = json.loads(process.stdout) if process.returncode == 0 else {}
    except json.JSONDecodeError as error:
        raise ContractError(f"docker image inspection returned malformed JSON: {error}") from error
    image_id = inspected.get("Id")
    if not isinstance(image_id, str) or not image_id.startswith("sha256:") or len(image_id) != 71:
        raise ContractError(f"docker image unavailable or invalid: {process.stderr.strip()}")
    descriptor = inspected.get("Descriptor") or {}
    if descriptor:
        if descriptor.get("digest") != expected_manifest_digest:
            raise ContractError("docker image manifest digest differs from required digest")
        if (descriptor.get("annotations") or {}).get("config.digest") != expected_image_id:
            raise ContractError("docker image config digest differs from required digest")
        if image_id not in {expected_manifest_digest, expected_image_id}:
            raise ContractError("docker store ID is inconsistent with the frozen image")
    elif image_id != expected_image_id:
        raise ContractError("classic Docker image ID differs from required config digest")
    if inspected.get("RootFS", {}).get("Layers") != expected_rootfs_layers:
        raise ContractError("docker image rootfs layers differ from required layers")
    observed_platform = f"{inspected.get('Os')}/{inspected.get('Architecture')}"
    if observed_platform != expected_platform:
        raise ContractError(f"docker image platform {observed_platform} differs from required {expected_platform}")
    return expected_image_id


def _docker_argv(
    image: str, platform_name: str, command: list[str], root: Path,
    limits: dict[str, Any], container_name: str,
) -> list[str]:
    return [
        "docker", "run", "--rm", "--pull", "never", "--platform", platform_name, "--init",
        "--name", container_name,
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
        # Docker's CPU quota does not change the CPU count observed by the Go
        # and Rust toolchains.  Without explicit job bounds, a 12-vCPU G2 host
        # can exhaust the task's intentional 64-PID sandbox while compiling
        # ordinary reference code.  Keep compiler parallelism inside the
        # frozen PID limit instead of weakening that security boundary.
        "--env", "GOMAXPROCS=1", "--env", "GOFLAGS=-p=1",
        "--env", "CARGO_BUILD_JOBS=1",
        "--entrypoint", command[0], image, *command[1:],
    ]


def _remove_timed_out_container(container_name: str) -> None:
    """Remove the exact container left behind when docker CLI is timed out."""
    try:
        subprocess.run(
            ["docker", "rm", "--force", container_name],
            check=False, capture_output=True, text=True, timeout=10,
            env={"PATH": os.environ.get("PATH", "")},
        )
    except (OSError, subprocess.TimeoutExpired):
        # Verification still fails closed. A later orphan preflight can surface
        # a daemon that is too unhealthy to complete this bounded cleanup.
        pass


def infrastructure_failure(verifier: dict[str, Any]) -> str | None:
    """Classify verifier-host failures that must never become model scores."""
    stderr = str(verifier.get("stderr", ""))
    lowered = stderr.lower()
    if not verifier.get("timed_out") and not verifier.get("exit_codes"):
        return "verifier returned no process exit code"
    # Docker reserves 125-127 for failures to invoke the container command.
    # Larger values are valid container-process exits (for example, 134 is
    # SIGABRT) and are expected evidence when a known-bad implementation
    # triggers a runtime safety check.
    if any(int(code) in {125, 126, 127} for code in verifier.get("exit_codes", [])):
        return f"container runtime exit code {verifier['exit_codes']}"
    signatures = (
        "resource temporarily unavailable",
        "failed to create new os thread",
        "cgroup: fork rejected",
        "oci runtime create failed",
        "oci runtime exec failed",
        "cannot connect to the docker daemon",
        "error response from daemon",
    )
    for signature in signatures:
        if signature in lowered:
            return f"verifier infrastructure signature: {signature}"
    return None


def _captured_text(value: str | bytes | None) -> str:
    """Normalize TimeoutExpired output, which may be bytes even with text=True."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def verify(task: dict[str, Any], code: str, runtime_config: Path) -> dict[str, Any]:
    validate_task(task)
    runtime = load_runtime(runtime_config, task["runtime_id"], task["language"], task["candidate_path"])
    image_id = _inspect_image(
        runtime["image"], runtime["image_id"], runtime["manifest_digest"],
        runtime["rootfs_layers"], runtime["platform"],
    )
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
            container_name = f"ganesh-verifier-{os.getpid()}-{uuid.uuid4().hex[:12]}"
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                break
            try:
                process = subprocess.run(
                    _docker_argv(
                        runtime["image"], runtime["platform"], command, root, limits,
                        container_name,
                    ),
                    check=False, capture_output=True, text=True, timeout=remaining,
                    env={"PATH": os.environ.get("PATH", "")},
                )
            except subprocess.TimeoutExpired as error:
                timed_out = True
                stdout_parts.append(_captured_text(error.stdout))
                stderr_parts.append(_captured_text(error.stderr))
                _remove_timed_out_container(container_name)
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
        "image": f"{runtime['image'].rsplit(':', 1)[0]}@{runtime['manifest_digest']}",
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
