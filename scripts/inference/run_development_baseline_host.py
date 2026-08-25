#!/usr/bin/env python3
"""Run the frozen Qwen development baseline from a sealed Linux host workspace.

The CUDA model process runs inside the qualified image. It reaches the host
Docker daemon only to start the already-pinned, network-disabled verifier
containers. Verifier temporary directories live on an identically mounted
host/container path so Docker bind mounts cannot resolve inside the wrong
filesystem namespace.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

_previous_bytecode_setting = sys.dont_write_bytecode
sys.dont_write_bytecode = True
try:
    from scripts.eval.verify_runtime_images import audit as audit_runtime_images
finally:
    sys.dont_write_bytecode = _previous_bytecode_setting


MODEL_ID = "Qwen/Qwen3.5-2B"
REVISION = "15852e8c16360a2fea060d615a32b45270f8a8fc"
CONFIG_RELATIVE = Path("configs/inference/qwen_base_development.json")
MODEL_RELATIVE = Path("models/qwen3.5-2b-15852e8")
OUTPUT_RELATIVE = Path("measurement/inference/development/qwen3.5-2b-base-v1")
RUNTIMES_RELATIVE = Path("configs/eval/runtimes.json")


def docker_attempt_id(attempt_id: str) -> str:
    """Preserve the evidence ID while deriving a Docker-safe lowercase ID."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,62}", attempt_id):
        raise ValueError("invalid baseline attempt ID")
    return attempt_id.lower()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def verify_workspace(root: Path, manifest_path: Path, archive_path: Path) -> dict[str, Any]:
    manifest = load_sealed(manifest_path, "manifest_sha256")
    if (
        manifest.get("schema_version") != "ganesh-mini-development-evaluation-workspace/v1"
        or manifest.get("status") != "sealed"
        or manifest.get("surface") != "development"
        or manifest.get("task_count") != 180
    ):
        raise ValueError("development workspace manifest contract mismatch")
    archive = manifest.get("archive", {})
    if archive_path.stat().st_size != archive.get("size_bytes") or file_sha256(archive_path) != archive.get("sha256"):
        raise ValueError("development workspace archive identity mismatch")
    expected: dict[str, tuple[int, str]] = {}
    for row in manifest.get("files", []):
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts or str(relative) in expected:
            raise ValueError("development workspace manifest contains an unsafe or duplicate path")
        expected[str(relative)] = (int(row["size_bytes"]), row["sha256"])
    observed = {
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file()
    }
    if observed != set(expected):
        raise ValueError("extracted development workspace file set mismatch")
    for relative, (size, digest) in expected.items():
        path = root / relative
        if path.stat().st_size != size or file_sha256(path) != digest:
            raise ValueError(f"extracted development workspace identity mismatch: {relative}")
    return manifest


def verify_bundle(bundle_path: Path, archive_path: Path, runtimes_path: Path) -> dict[str, Any]:
    bundle = load_sealed(bundle_path, "manifest_sha256")
    if (
        bundle.get("schema_version") != "ganesh-mini-verifier-image-bundle/v1"
        or bundle.get("status") != "prepared-adopted"
        or bundle.get("platform") != "linux/amd64"
    ):
        raise ValueError("verifier image bundle contract mismatch")
    archive = bundle.get("archive", {})
    if archive_path.stat().st_size != archive.get("size_bytes") or file_sha256(archive_path) != archive.get("sha256"):
        raise ValueError("verifier image archive identity mismatch")
    adopted = bundle.get("adopted_runtime_config", {})
    if file_sha256(runtimes_path) != adopted.get("sha256"):
        raise ValueError("adopted runtime configuration identity mismatch")
    return bundle


def docker_image_id(docker: str, image: str) -> str:
    result = subprocess.run(
        [docker, "image", "inspect", "--format", "{{.Id}}", image],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"CUDA image unavailable: {result.stderr.strip()}")
    return result.stdout.strip()


def require_fresh_container_name(docker: str, name: str) -> None:
    result = subprocess.run(
        [docker, "container", "inspect", name],
        check=False, capture_output=True, text=True, timeout=30,
    )
    if result.returncode == 0:
        raise RuntimeError(f"baseline container name is not fresh: {name}")
    if result.returncode != 1:
        raise RuntimeError(f"baseline container freshness check failed: {result.stderr.strip()}")


def build_container_argv(
    *, docker: str, image: str, container_name: str, workspace: Path,
    model: Path, output: Path, shared_tmp: Path, docker_socket: Path,
) -> list[str]:
    return [
        docker, "run", "--pull=never", "--name", container_name,
        "--gpus", "device=0", "--network", "none", "--cpus", "12",
        "--memory", "72g", "--pids-limit", "4096", "--read-only",
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=8g",
        "--tmpfs", "/var/cache/triton:rw,exec,nosuid,nodev,size=1g",
        "--mount", f"type=bind,src={workspace},dst=/workspace,readonly",
        "--mount", f"type=bind,src={model},dst=/workspace/{MODEL_RELATIVE},readonly",
        "--mount", f"type=bind,src={output},dst=/workspace/{OUTPUT_RELATIVE}",
        "--mount", f"type=bind,src={shared_tmp},dst={shared_tmp}",
        "--mount", f"type=bind,src={docker_socket},dst=/var/run/docker.sock",
        "--mount", f"type=bind,src={docker},dst=/usr/local/bin/docker,readonly",
        "--env", "HF_HUB_OFFLINE=1", "--env", "TRANSFORMERS_OFFLINE=1",
        "--env", "PYTHONPATH=/workspace", "--env", f"TMPDIR={shared_tmp}",
        "--env", "TRITON_CACHE_DIR=/var/cache/triton",
        "--entrypoint", "python", image,
        "/workspace/scripts/inference/run_evaluation.py",
        "--config", f"/workspace/{CONFIG_RELATIVE}",
    ]


def validate_completed_run(path: Path) -> dict[str, Any]:
    run = load_sealed(path, "run_sha256")
    accounting = run.get("task_accounting", {})
    model = run.get("model", {})
    if (
        run.get("schema_version") != "ganesh-mini-inference-run/v2"
        or run.get("classification") != "private_development_baseline"
        or model.get("model_id") != MODEL_ID
        or model.get("revision") != REVISION
        or accounting.get("expected") != 180
        or accounting.get("completed") != 180
        or accounting.get("pending") != 0
        or len(run.get("tasks", [])) != 180
    ):
        raise ValueError("baseline run did not satisfy the frozen completion contract")
    return run


def execute(args: argparse.Namespace) -> dict[str, Any]:
    if platform.system() != "Linux" or platform.machine() not in {"x86_64", "amd64"}:
        raise RuntimeError("development baseline host must be Linux/AMD64")
    container_attempt_id = docker_attempt_id(args.attempt_id)
    workspace = args.workspace.resolve(strict=True)
    model = args.model.resolve(strict=True)
    output = args.output.resolve()
    shared_tmp = args.shared_tmp.resolve()
    output.mkdir(parents=True, exist_ok=True)
    shared_tmp.mkdir(parents=True, exist_ok=True)
    manifest = verify_workspace(workspace, args.workspace_manifest.resolve(strict=True), args.workspace_archive.resolve(strict=True))
    bundle = verify_bundle(
        args.verifier_bundle.resolve(strict=True), args.verifier_archive.resolve(strict=True),
        workspace / RUNTIMES_RELATIVE,
    )
    docker = shutil.which("docker")
    if docker is None:
        raise RuntimeError("Docker CLI is unavailable")
    docker_socket = args.docker_socket.resolve(strict=True)
    if not docker_socket.is_socket():
        raise RuntimeError("Docker socket is unavailable")
    observed_cuda_id = docker_image_id(docker, args.cuda_image)
    if observed_cuda_id != args.cuda_image_id:
        raise RuntimeError("CUDA image identity mismatch")
    load = subprocess.run(
        [docker, "load", "--input", str(args.verifier_archive.resolve(strict=True))],
        check=False, capture_output=True, text=True, timeout=600,
    )
    if load.returncode != 0:
        raise RuntimeError(f"verifier image load failed: {load.stderr.strip()}")
    readiness = audit_runtime_images(workspace / RUNTIMES_RELATIVE)
    readiness_path = output / "runtime-image-readiness.json"
    readiness_path.write_text(json.dumps(readiness, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if readiness["status"] != "ready" or readiness["ready"] != readiness["expected"]:
        raise RuntimeError(f"verifier runtime images are not ready: {readiness['failures']}")
    name = f"ganesh-qwen-base-{container_attempt_id}"
    require_fresh_container_name(docker, name)
    argv = build_container_argv(
        docker=docker, image=args.cuda_image, container_name=name, workspace=workspace,
        model=model, output=output, shared_tmp=shared_tmp, docker_socket=docker_socket,
    )
    stdout_path, stderr_path = output / "controller.stdout.log", output / "controller.stderr.log"
    try:
        with stdout_path.open("ab") as stdout, stderr_path.open("ab") as stderr:
            result = subprocess.run(argv, check=False, stdout=stdout, stderr=stderr, timeout=args.max_seconds)
    except subprocess.TimeoutExpired as error:
        subprocess.run([docker, "rm", "-f", name], check=False, capture_output=True, timeout=30)
        raise RuntimeError(f"baseline controller exceeded {args.max_seconds} seconds") from error
    finally:
        subprocess.run([docker, "rm", "-f", name], check=False, capture_output=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"baseline model container exited {result.returncode}; resumable evidence is preserved")
    run = validate_completed_run(output / "run.json")
    evidence: dict[str, Any] = {
        "schema_version": "ganesh-mini-development-baseline-host/v1",
        "status": "passed",
        "attempt_id": args.attempt_id,
        "model": {"model_id": MODEL_ID, "revision": REVISION},
        "cuda_image": {"ref": args.cuda_image, "image_id": observed_cuda_id},
        "workspace": {"manifest_sha256": manifest["manifest_sha256"], "archive_sha256": manifest["archive"]["sha256"]},
        "verifier_bundle": {"manifest_sha256": bundle["manifest_sha256"], "archive_sha256": bundle["archive"]["sha256"], "runtime_readiness_sha256": readiness["evidence_sha256"]},
        "sandbox": {"outer_network": "none", "docker_socket": "host", "shared_tmp": str(shared_tmp), "verifier_network": "none"},
        "execution": {"max_seconds": args.max_seconds, "returncode": result.returncode},
        "run": {"path": str(output / "run.json"), "run_sha256": run["run_sha256"], "task_accounting": run["task_accounting"]},
        "logs": {"stdout_sha256": file_sha256(stdout_path), "stderr_sha256": file_sha256(stderr_path)},
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    evidence_path = output / "host-execution.json"
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return evidence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--workspace-manifest", type=Path, required=True)
    parser.add_argument("--workspace-archive", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--verifier-bundle", type=Path, required=True)
    parser.add_argument("--verifier-archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shared-tmp", type=Path, required=True)
    parser.add_argument("--docker-socket", type=Path, default=Path("/var/run/docker.sock"))
    parser.add_argument("--cuda-image", required=True)
    parser.add_argument("--cuda-image-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--max-seconds", type=int, required=True)
    args = parser.parse_args()
    if not 600 <= args.max_seconds <= 21600:
        parser.error("--max-seconds must be between 600 and 21600")
    return args


def main() -> int:
    try:
        evidence = execute(parse_args())
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(f"development baseline failed: {error}", file=os.sys.stderr)
        return 1
    print(json.dumps({"status": evidence["status"], "run": evidence["run"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
