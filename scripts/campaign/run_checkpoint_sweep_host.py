#!/usr/bin/env python3
"""Run the sealed Gate 4 checkpoint sweep locally, without promotion authority."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.campaign.run_host import (  # noqa: E402
    CUDA_IMAGE_ID,
    CONTAINER_ADAPTER,
    CONTAINER_MODEL,
    CONTAINER_OUTPUT,
    CONTAINER_TRAINING,
    Campaign,
    atomic_json,
    canonical_sha256,
    docker_container_name,
    external_mount,
    file_sha256,
    load_sealed,
    verify_workspace,
)


EXPECTED_CONFIG_COUNT = 5
BASE_TASKS = Path("measurement/inference/development/qwen3.5-2b-base-v1/tasks")
WORKSPACE_SCHEMA = "ganesh-mini-checkpoint-sweep-workspace/v1"


def verify_files(root: Path, rows: list[dict[str, Any]], *, label: str) -> None:
    expected: dict[str, dict[str, Any]] = {}
    for row in rows:
        relative = row.get("path")
        if not isinstance(relative, str) or not relative or relative in expected:
            raise ValueError(f"{label} has duplicate or invalid file entries")
        expected[relative] = row
    observed = {
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file() and path != root / "manifest.json"
    }
    if observed != set(expected):
        raise ValueError(f"{label} runtime file set mismatch")
    for relative in expected:
        path = root / relative
        row = expected[relative]
        size = row.get("size_bytes", row.get("size"))
        if path.is_symlink() or path.stat().st_size != size or file_sha256(path) != row.get("sha256"):
            raise ValueError(f"{label} file identity mismatch: {relative}")


def verify_result_tasks(result_dir: Path, run: dict[str, Any]) -> None:
    expected: dict[str, str] = {}
    for row in run.get("tasks", []):
        task_id, digest = row.get("task_id"), row.get("evidence_sha256")
        if (
            not isinstance(task_id, str)
            or not isinstance(digest, str)
            or row.get("status") != "complete"
            or task_id in expected
        ):
            raise ValueError("evaluation run has invalid or duplicate task bindings")
        expected[task_id] = digest
    observed = {path.stem for path in (result_dir / "tasks").glob("*.json")}
    if observed != set(expected):
        raise ValueError("evaluation run task file set mismatch")
    for task_id, digest in expected.items():
        evidence = load_sealed(result_dir / "tasks" / f"{task_id}.json", "evidence_sha256")
        if evidence["evidence_sha256"] != digest or evidence.get("task", {}).get("task_id") != task_id:
            raise ValueError(f"evaluation task escaped run binding: {task_id}")


def verify_training_and_sweep(
    training: Path,
    terminal_path: Path,
    config_dir: Path,
    final_canary: Path,
) -> tuple[dict[str, Any], list[tuple[str, Path]], dict[str, Any]]:
    """Bind every runtime input before the first CUDA evaluation starts."""
    run = load_sealed(training / "run-evidence.json", "evidence_sha256")
    if run.get("schema_version") != "ganesh-mini-sft-run/v2" or run.get("status") != "complete":
        raise ValueError("checkpoint sweep requires completed training evidence")
    terminal = load_sealed(terminal_path, "report_sha256")
    if (
        terminal.get("schema_version") != "ganesh-mini-expansion-pilot-terminal/v1"
        or terminal.get("status") != "passed"
        or terminal.get("run_evidence_sha256") != run["evidence_sha256"]
        or terminal.get("adapter_files") != run.get("adapter_files")
    ):
        raise ValueError("checkpoint sweep requires the matching passed training terminal")
    final_adapter = training / "adapter-final"
    observed_final = {path.name: file_sha256(path) for path in sorted(final_adapter.iterdir()) if path.is_file()}
    if observed_final != run.get("adapter_files"):
        raise ValueError("final adapter escaped completed training evidence")

    manifest = load_sealed(config_dir / "manifest.json", "manifest_sha256")
    labels = sorted(manifest.get("config_sha256", {}))
    measured_final = manifest.get("measured_final_checkpoint")
    if (
        manifest.get("schema_version") != "ganesh-mini-checkpoint-sweep/v1"
        or manifest.get("status") != "diagnostic-only"
        or manifest.get("promotion_authority") != "none"
        or manifest.get("training_run_evidence_sha256") != run["evidence_sha256"]
        or manifest.get("unmeasured_checkpoint_count") != EXPECTED_CONFIG_COUNT
        or len(labels) != EXPECTED_CONFIG_COUNT
        or not isinstance(measured_final, str)
        or set(manifest.get("checkpoint_manifest_sha256", {})) != {*labels, measured_final}
        or manifest.get("task_count_per_checkpoint") != 30
    ):
        raise ValueError("checkpoint sweep manifest contract mismatch")
    observed_configs = {path.stem for path in config_dir.glob("*.json") if path.name != "manifest.json"}
    if observed_configs != set(labels):
        raise ValueError("checkpoint sweep must contain exactly the five sealed configs")

    for label in [*labels, measured_final]:
        checkpoint_root = training / "checkpoints" / label
        checkpoint = load_sealed(checkpoint_root / "manifest.json", "manifest_sha256")
        if (
            checkpoint.get("schema_version") != "ganesh-mini-checkpoint/v1"
            or checkpoint.get("status") != "complete"
            or checkpoint.get("identities") != run.get("identities")
            or checkpoint["manifest_sha256"] != manifest["checkpoint_manifest_sha256"].get(label)
        ):
            raise ValueError(f"checkpoint manifest escaped completed training evidence: {label}")
        verify_files(checkpoint_root, checkpoint.get("files", []), label=label)

    configs: list[tuple[str, Path]] = []
    for label in labels:
        path = config_dir / f"{label}.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        adapter = config.get("adapter", {})
        if (
            canonical_sha256(config) != manifest["config_sha256"][label]
            or config.get("classification") != "private_candidate_development"
            or config.get("allowed_surface") != "development"
            or config.get("expected_task_count") != 30
            or config.get("execution", {}).get("required_device") != "cuda"
            or adapter.get("dir") != f"/training/checkpoints/{label}/adapter"
            or adapter.get("checkpoint_manifest") != f"/training/checkpoints/{label}/manifest.json"
            or adapter.get("run_evidence") != "/training/run-evidence.json"
        ):
            raise ValueError(f"checkpoint config contract mismatch: {label}")
        configs.append((label, path))

    final_run = load_sealed(final_canary / "run.json", "run_sha256")
    accounting = final_run.get("task_accounting", {})
    if (
        accounting.get("completed") != 30
        or accounting.get("pending") != 0
        or final_run.get("model", {}).get("training_run_evidence_sha256") != run["evidence_sha256"]
    ):
        raise ValueError("existing final canary is not complete or training-bound")
    verify_result_tasks(final_canary, final_run)
    return manifest, configs, final_run


class CheckpointSweepCampaign(Campaign):
    def docker_base(self, name: str, workspace: Path) -> list[str]:
        return [
            self.docker,
            "run", "--pull=never", "--rm", "--name", docker_container_name(name),
            "--label", f"ganesh.campaign={self.args.attempt_id}",
            "--gpus", "device=0", "--network", "none", "--cpus", "8", "--memory", "30g",
            "--pids-limit", "4096", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=8g",
            "--tmpfs", "/var/cache/triton:rw,exec,nosuid,nodev,size=1g",
            "--mount", f"type=bind,src={workspace.resolve()},dst=/workspace,readonly",
            "--mount", external_mount(self.args.model, CONTAINER_MODEL, readonly=True),
            "--env", "CUDA_VISIBLE_DEVICES=0", "--env", "HF_HUB_OFFLINE=1",
            "--env", "TRANSFORMERS_OFFLINE=1", "--env", "PYTHONPATH=/workspace",
            "--env", "TRITON_CACHE_DIR=/var/cache/triton", "--workdir", "/workspace",
        ]

    def evaluate(self, label: str, config: Path) -> Path:
        destination = self.output / "results" / label
        destination.mkdir(parents=True, exist_ok=False)
        command = self.docker_base(f"ganesh-sweep-{self.args.attempt_id}-{label}", self.args.eval_workspace)
        command += [
            "--mount", external_mount(self.args.training, CONTAINER_TRAINING, readonly=True),
            "--mount", external_mount(destination, CONTAINER_OUTPUT),
            "--mount", external_mount(self.args.config_dir, Path("/control/configs"), readonly=True),
            "--mount", external_mount(self.args.shared_tmp, self.args.shared_tmp.resolve()),
            "--mount", "type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock",
            "--mount", f"type=bind,src={self.docker},dst=/usr/local/bin/docker,readonly",
            "--env", f"TMPDIR={self.args.shared_tmp.resolve()}",
            "--entrypoint", "python", self.args.cuda_image,
            "/workspace/scripts/inference/run_evaluation.py",
            "--config", f"/control/configs/{config.name}",
            "--model-dir", str(CONTAINER_MODEL),
            "--adapter-dir", str(CONTAINER_TRAINING / "checkpoints" / label / "adapter"),
            "--output-dir", str(CONTAINER_OUTPUT),
        ]
        self.run(command, log_name=f"evaluate-{label}", timeout=min(self.remaining(), self.args.per_checkpoint_max_seconds))
        run = load_sealed(destination / "run.json", "run_sha256")
        accounting = run.get("task_accounting", {})
        if (
            accounting.get("completed") != 30
            or accounting.get("pending") != 0
            or run.get("model", {}).get("training_run_evidence_sha256") != self.training_run_sha256
            or run.get("model", {}).get("checkpoint_manifest_sha256") != self.sweep_manifest["checkpoint_manifest_sha256"][label]
        ):
            raise RuntimeError(f"{label} checkpoint evaluation is incomplete or identity-unbound")
        verify_result_tasks(destination, run)
        self.record(f"evaluate-{label}", "passed", run_sha256=run["run_sha256"], passed=accounting["passed"])
        return destination

    def summarize(self) -> dict[str, Any]:
        report_path = self.output / "checkpoint-sweep-result.json"
        env = {**os.environ, "PYTHONPATH": str(self.args.eval_workspace)}
        self.run([
            sys.executable,
            str(self.args.eval_workspace / "scripts/eval/summarize_checkpoint_sweep.py"),
            "--manifest", str(self.args.config_dir / "manifest.json"),
            "--base-tasks", str(self.args.eval_workspace / BASE_TASKS),
            "--results", str(self.output / "results"),
            "--final-tasks", str(self.args.final_canary / "tasks"),
            "--output", str(report_path),
        ], log_name="summarize-checkpoint-sweep", timeout=min(self.remaining(), 600), env=env)
        report = load_sealed(report_path, "report_sha256")
        if (
            report.get("status") != "complete-diagnostic"
            or report.get("promotion_authority") != "none"
            or report.get("sweep_manifest_sha256") != self.sweep_manifest["manifest_sha256"]
            or report.get("training_run_evidence_sha256") != self.training_run_sha256
            or len(report.get("checkpoints", [])) != EXPECTED_CONFIG_COUNT + 1
        ):
            raise RuntimeError("checkpoint sweep summary escaped diagnostic contract")
        self.record("summarize-checkpoint-sweep", "passed", report_sha256=report["report_sha256"])
        return report

    def execute(self) -> dict[str, Any]:
        if platform.system() != "Linux" or platform.machine() not in {"x86_64", "amd64"}:
            raise RuntimeError("checkpoint sweep host must be Linux/AMD64")
        if not self.docker or not Path("/var/run/docker.sock").is_socket():
            raise RuntimeError("Docker host runtime is unavailable")
        if self.args.cuda_image_id != CUDA_IMAGE_ID:
            raise RuntimeError("checkpoint sweep escaped the qualified CUDA image")
        verify_workspace(
            self.args.eval_workspace, self.args.eval_manifest, self.args.eval_archive,
            WORKSPACE_SCHEMA,
        )
        self.sweep_manifest, configs, final_run = verify_training_and_sweep(
            self.args.training, self.args.training_terminal, self.args.config_dir, self.args.final_canary,
        )
        self.training_run_sha256 = self.sweep_manifest["training_run_evidence_sha256"]
        self.record(
            "sealed-input-admission", "passed",
            sweep_manifest_sha256=self.sweep_manifest["manifest_sha256"],
            training_run_evidence_sha256=self.training_run_sha256,
            final_canary_run_sha256=final_run["run_sha256"], config_count=len(configs),
            promotion_authority="none",
        )
        self.prepare_verifier_images()
        # subprocess.run is intentionally awaited inside evaluate: never overlap CUDA checkpoints.
        for label, config in configs:
            self.evaluate(label, config)
        summary = self.summarize()
        result: dict[str, Any] = {
            "schema_version": "ganesh-mini-checkpoint-sweep-campaign-result/v1",
            "status": "complete-diagnostic",
            "attempt_id": self.args.attempt_id,
            "elapsed_seconds": round(time.monotonic() - self.started, 3),
            "sweep_manifest_sha256": self.sweep_manifest["manifest_sha256"],
            "training_run_evidence_sha256": self.training_run_sha256,
            "summary_report_sha256": summary["report_sha256"],
            "final_canary_run_sha256": final_run["run_sha256"],
            "evaluated_checkpoints": [label for label, _ in configs],
            "included_final_checkpoint": self.sweep_manifest["measured_final_checkpoint"],
            "promotion_authority": "none",
            "phases": self.phases,
        }
        result["result_sha256"] = canonical_sha256(result)
        atomic_json(self.output / "campaign-result.json", result)
        return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-workspace", type=Path, required=True)
    parser.add_argument("--eval-manifest", type=Path, required=True)
    parser.add_argument("--eval-archive", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--training", type=Path, required=True)
    parser.add_argument("--training-terminal", type=Path, required=True)
    parser.add_argument("--config-dir", type=Path, required=True)
    parser.add_argument("--final-canary", type=Path, required=True)
    parser.add_argument("--verifier-manifest", type=Path, required=True)
    parser.add_argument("--verifier-archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shared-tmp", type=Path, required=True)
    parser.add_argument("--cuda-image", required=True)
    parser.add_argument("--cuda-image-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--max-seconds", type=int, required=True)
    parser.add_argument("--per-checkpoint-max-seconds", type=int, default=3600)
    parser.add_argument("--finalization-reserve-seconds", type=int, default=600)
    args = parser.parse_args()
    if not 3600 <= args.max_seconds <= 28800:
        parser.error("invalid sweep time envelope")
    if not 600 <= args.per_checkpoint_max_seconds <= 7200:
        parser.error("invalid per-checkpoint time envelope")
    if not 600 <= args.finalization_reserve_seconds < args.max_seconds:
        parser.error("invalid finalization reserve")
    return args


def main() -> int:
    try:
        CheckpointSweepCampaign(parse_args()).execute()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        print(f"checkpoint sweep failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
