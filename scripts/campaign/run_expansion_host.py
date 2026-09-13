#!/usr/bin/env python3
"""Run the bounded Gate 4 expansion pilot and its conditional evaluation."""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from decimal import Decimal
from pathlib import Path


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
    docker_container_name,
    external_mount,
    load_sealed,
    verify_workspace,
)


BASE_TASKS = Path("measurement/inference/development/qwen3.5-2b-base-v1/tasks")


def default_config_relative(card: dict[str, object]) -> Path:
    schema = card.get("schema_version")
    if schema == "ganesh-mini-expansion-pilot-card/v1":
        return Path("configs/train/expansion_pilot_v1.json")
    if schema == "ganesh-mini-expansion-pilot-card/v2":
        return Path("configs/train/expansion_capacity_probe_v2.json")
    if schema == "ganesh-mini-expansion-pilot-card/v3":
        return Path("configs/train/expansion_lane_stratified_probe_v3.json")
    if schema == "ganesh-mini-expansion-pilot-card/v4":
        return Path("configs/train/gradient_conflict_probe_v4.json")
    raise RuntimeError("unsupported expansion card schema")


class ExpansionCampaign(Campaign):
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
            "--env", "HF_HUB_OFFLINE=1", "--env", "TRANSFORMERS_OFFLINE=1",
            "--env", "PYTHONPATH=/workspace", "--env", "TRITON_CACHE_DIR=/var/cache/triton",
            "--workdir", "/workspace",
        ]

    def train_expansion(self, card: Path, config: dict[str, object]) -> Path:
        destination = self.output / "training" / "expansion-pilot"
        destination.mkdir(parents=True, exist_ok=False)
        execution_card = load_sealed(card, "card_sha256")
        provider = execution_card.get("provider_execution") or {}
        provider_prior_cost = Decimal(str(provider.get("prior_cost_usd", -1)))
        if provider_prior_cost < 0:
            raise RuntimeError("training card has no valid provider prior cost")
        data = config["data"]
        recipe = config["recipe"]
        control = config["control"]
        command = self.docker_base(f"ganesh-train-{self.args.attempt_id}-expansion", self.args.train_workspace)
        command += [
            "--mount", external_mount(destination, Path("/outputs")),
            "--mount", external_mount(card.parent, Path("/control"), readonly=True),
            "--entrypoint", "python", self.args.cuda_image,
            "/workspace/scripts/train/run_sft.py",
            "--phase", "expansion-pilot",
            "--card", f"/control/{card.name}",
            "--model-dir", str(CONTAINER_MODEL),
            "--config", f"/workspace/{self.args.config_relative}",
            "--prepared-manifest", f"/workspace/{data['prepared_manifest_path']}",
            "--prepared-data", f"/workspace/{data['prepared_train_path']}",
            "--validation-data", f"/workspace/{data['prepared_validation_path']}",
            "--output", "/outputs",
            "--learning-rate", str(recipe["learning_rate"]),
            "--maximum-seen-tokens", str(control["maximum_seen_tokens"]),
            "--hourly-cost-usd", str(self.args.hourly_cost_usd),
            "--prior-cost-usd", str(provider_prior_cost),
            "--cost-ceiling-usd", str(self.args.absolute_cost_ceiling_usd),
        ]
        timeout = min(self.remaining(self.args.finalization_reserve_seconds), int(control["maximum_wall_seconds"]))
        # run_sft uses exit 2 for a sealed gradient-audit stop. Validate the
        # resulting evidence below before accepting that code as terminal.
        self.run(
            command,
            log_name="train-expansion-pilot",
            timeout=timeout,
            allowed_returncodes=(0, 2),
        )
        run = load_sealed(destination / "run-evidence.json", "evidence_sha256")
        if run.get("status") == "gradient-audit-stop":
            audit = run.get("state", {}).get("gradient_conflict_audit", {})
            if (
                run.get("state", {}).get("optimizer_steps") != 0
                or run.get("state", {}).get("seen_tokens") != 0
                or audit.get("decision", {}).get("stage_2_allowed") is not False
                or not isinstance(audit.get("audit_sha256"), str)
            ):
                raise RuntimeError("gradient audit stop evidence is invalid")
            self.record("train-expansion-pilot", "passed", evidence_sha256=run["evidence_sha256"], decision="gradient-audit-stop", audit_sha256=audit["audit_sha256"])
            return destination
        if run.get("status") != "complete" or run.get("state", {}).get("seen_tokens") < control["maximum_seen_tokens"]:
            raise RuntimeError("expansion pilot training is incomplete")
        self.record("train-expansion-pilot", "passed", evidence_sha256=run["evidence_sha256"], seen_tokens=run["state"]["seen_tokens"])
        return destination

    def verify_training(self, card: Path, training: Path) -> Path:
        terminal = self.output / "training-terminal.json"
        env = {**os.environ, "PYTHONPATH": str(self.args.train_workspace)}
        self.run([
            sys.executable,
            str(self.args.train_workspace / "scripts/train/verify_expansion_pilot.py"),
            "--card", str(card),
            "--config", str(self.args.train_workspace / self.args.config_relative),
            "--run", str(training / "run-evidence.json"),
            "--adapter-dir", str(training / "adapter-final"),
            "--output", str(terminal),
        ], log_name="verify-expansion-pilot", timeout=min(self.remaining(), 600), env=env)
        report = load_sealed(terminal, "report_sha256")
        if report.get("status") != "passed":
            raise RuntimeError(f"training terminal verification failed: {report.get('failed_checks')}")
        self.record("verify-expansion-pilot", "passed", report_sha256=report["report_sha256"])
        return terminal

    def build_evaluation(self, card: Path, terminal: Path, training: Path) -> Path:
        config_dir = self.output / "evaluation-configs"
        env = {**os.environ, "PYTHONPATH": str(self.args.eval_workspace)}
        self.run([
            sys.executable,
            str(self.args.eval_workspace / "scripts/eval/build_expansion_evaluation.py"),
            "--root", str(self.output),
            "--card", str(card),
            "--terminal", str(terminal),
            "--run", str(training / "run-evidence.json"),
            "--adapter-dir", str(training / "adapter-final"),
            "--output-dir", str(config_dir),
        ], log_name="build-expansion-evaluation", timeout=min(self.remaining(), 600), env=env)
        manifest = load_sealed(config_dir / "manifest.json", "manifest_sha256")
        if manifest.get("status") != "canary-ready-full-blocked":
            raise RuntimeError("expansion evaluation manifest is not canary-ready")
        self.record("build-expansion-evaluation", "passed", manifest_sha256=manifest["manifest_sha256"])
        return config_dir

    def evaluate(self, label: str, config: Path, training: Path, expected: int) -> Path:
        destination = self.output / "evaluation" / label
        destination.mkdir(parents=True, exist_ok=False)
        command = self.docker_base(f"ganesh-eval-{self.args.attempt_id}-{label}", self.args.eval_workspace)
        command += [
            "--mount", external_mount(training, CONTAINER_TRAINING, readonly=True),
            "--mount", external_mount(destination, CONTAINER_OUTPUT),
            "--mount", external_mount(config.parent, Path("/control/configs"), readonly=True),
            "--mount", external_mount(self.args.shared_tmp, self.args.shared_tmp.resolve()),
            "--mount", "type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock",
            "--mount", f"type=bind,src={self.docker},dst=/usr/local/bin/docker,readonly",
            "--env", f"TMPDIR={self.args.shared_tmp.resolve()}",
            "--entrypoint", "python", self.args.cuda_image,
            "/workspace/scripts/inference/run_evaluation.py",
            "--config", f"/control/configs/{config.name}",
            "--model-dir", str(CONTAINER_MODEL),
            "--adapter-dir", str(CONTAINER_ADAPTER),
            "--output-dir", str(CONTAINER_OUTPUT),
        ]
        self.run(command, log_name=f"evaluate-{label}", timeout=min(self.remaining(self.args.finalization_reserve_seconds), 21600))
        run = load_sealed(destination / "run.json", "run_sha256")
        accounting = run.get("task_accounting", {})
        if accounting.get("completed") != expected or accounting.get("pending") != 0:
            raise RuntimeError(f"{label} evaluation is incomplete")
        self.record(f"evaluate-{label}", "passed", run_sha256=run["run_sha256"], passed=accounting["passed"])
        return destination

    def adjudicate_canary(self, card: Path, terminal: Path, candidate: Path) -> dict[str, object]:
        output = self.output / "canary-adjudication.json"
        stdout = self.output / "adjudicate-canary.stdout.log"
        stderr = self.output / "adjudicate-canary.stderr.log"
        env = {**os.environ, "PYTHONPATH": str(self.args.eval_workspace)}
        with stdout.open("ab") as out, stderr.open("ab") as err:
            result = subprocess.run([
                sys.executable,
                str(self.args.eval_workspace / "scripts/eval/adjudicate_expansion_canary.py"),
                "--card", str(card),
                "--terminal", str(terminal),
                "--base-tasks", str(self.args.eval_workspace / BASE_TASKS),
                "--candidate-tasks", str(candidate / "tasks"),
                "--output", str(output),
            ], stdout=out, stderr=err, timeout=min(self.remaining(), 600), env=env, check=False)
        if result.returncode not in {0, 2}:
            raise RuntimeError(f"canary adjudicator exited {result.returncode}")
        report = load_sealed(output, "report_sha256")
        expected_status = "promote-to-full-development" if result.returncode == 0 else "do-not-promote"
        if report.get("status") != expected_status:
            raise RuntimeError("canary exit status and sealed report disagree")
        self.record("adjudicate-canary", "passed", report_sha256=report["report_sha256"], decision=report["status"])
        return report

    def execute(self) -> None:
        if platform.system() != "Linux" or platform.machine() not in {"x86_64", "amd64"}:
            raise RuntimeError("campaign host must be Linux/AMD64")
        if not self.docker or not Path("/var/run/docker.sock").is_socket():
            raise RuntimeError("Docker host runtime is unavailable")
        if self.args.cuda_image_id != CUDA_IMAGE_ID:
            raise RuntimeError("campaign escaped the qualified CUDA image")
        verify_workspace(self.args.eval_workspace, self.args.eval_manifest, self.args.eval_archive, "ganesh-mini-development-evaluation-workspace/v1")
        verify_workspace(self.args.train_workspace, self.args.train_manifest, self.args.train_archive, "ganesh-mini-training-workspace/v1")
        card_path = self.args.card
        card = load_sealed(card_path, "card_sha256")
        if self.args.config_relative is None:
            self.args.config_relative = default_config_relative(card)
        config = json.loads((self.args.train_workspace / self.args.config_relative).read_text())
        provider = card.get("provider_execution") or {}
        schema = config.get("schema_version")
        expected_card_schema = {"ganesh-mini-expansion-pilot-config/v1": "ganesh-mini-expansion-pilot-card/v1", "ganesh-mini-expansion-pilot-config/v2": "ganesh-mini-expansion-pilot-card/v2", "ganesh-mini-expansion-pilot-config/v3": "ganesh-mini-expansion-pilot-card/v3", "ganesh-mini-expansion-pilot-config/v4": "ganesh-mini-expansion-pilot-card/v4"}.get(schema)
        if (
            expected_card_schema is None
            or card.get("schema_version") != expected_card_schema
            or card.get("status") != "ready"
            or provider.get("provider") != "gcloud"
            or provider.get("machine_type") != "g2-standard-8"
            or Decimal(str(provider.get("hourly_cost_usd"))) != self.args.hourly_cost_usd
            or Decimal(str(provider.get("cost_ceiling_usd"))) != self.args.absolute_cost_ceiling_usd
        ):
            raise RuntimeError("executable expansion card/provider contract mismatch")
        self.record("workspace-and-provider-admission", "passed", card_sha256=card["card_sha256"])
        self.prepare_verifier_images()
        training = self.train_expansion(card_path, config)
        run = load_sealed(training / "run-evidence.json", "evidence_sha256")
        if run.get("status") == "gradient-audit-stop":
            self.record("verify-expansion-pilot", "blocked-by-gradient-audit")
            self.record("candidate-evaluation", "blocked-by-gradient-audit")
            status = "completed-gradient-audit-no-conflict"
            final = {
                "schema_version": "ganesh-mini-expansion-campaign-result/v1",
                "status": status,
                "attempt_id": self.args.attempt_id,
                "elapsed_seconds": round(time.monotonic() - self.started, 3),
                "phases": self.phases,
                "projected_compute_cost_usd": str(self.prior_cost()),
            }
            from scripts.campaign.run_host import canonical_sha256
            final["evidence_sha256"] = canonical_sha256(final)
            atomic_json(self.output / "campaign-result.json", final)
            return
        terminal = self.verify_training(card_path, training)
        configs = self.build_evaluation(card_path, terminal, training)
        canary = self.evaluate("canary", configs / "canary.json", training, 30)
        adjudication = self.adjudicate_canary(card_path, terminal, canary)
        if adjudication["status"] == "promote-to-full-development" and schema == "ganesh-mini-expansion-pilot-config/v1":
            self.evaluate("full-development", configs / "full.json", training, 180)
            status = "completed-full-development"
        elif adjudication["status"] == "promote-to-full-development":
            status = "completed-capacity-probe-continuation-screen-passed"
            self.record("full-development", "blocked-by-probe-authority")
        elif schema in {"ganesh-mini-expansion-pilot-config/v2", "ganesh-mini-expansion-pilot-config/v3", "ganesh-mini-expansion-pilot-config/v4"}:
            status = "completed-capacity-probe-continuation-screen-failed"
        else:
            status = "completed-canary-not-promoted"
        final = {
            "schema_version": "ganesh-mini-expansion-campaign-result/v1",
            "status": status,
            "attempt_id": self.args.attempt_id,
            "elapsed_seconds": round(time.monotonic() - self.started, 3),
            "phases": self.phases,
            "projected_compute_cost_usd": str(self.prior_cost()),
        }
        from scripts.campaign.run_host import canonical_sha256
        final["evidence_sha256"] = canonical_sha256(final)
        atomic_json(self.output / "campaign-result.json", final)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-workspace", type=Path, required=True)
    parser.add_argument("--eval-manifest", type=Path, required=True)
    parser.add_argument("--eval-archive", type=Path, required=True)
    parser.add_argument("--train-workspace", type=Path, required=True)
    parser.add_argument("--train-manifest", type=Path, required=True)
    parser.add_argument("--train-archive", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--verifier-manifest", type=Path, required=True)
    parser.add_argument("--verifier-archive", type=Path, required=True)
    parser.add_argument("--config-relative", type=Path)
    parser.add_argument("--card", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shared-tmp", type=Path, required=True)
    parser.add_argument("--cuda-image", required=True)
    parser.add_argument("--cuda-image-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--max-seconds", type=int, required=True)
    parser.add_argument("--finalization-reserve-seconds", type=int, default=1800)
    parser.add_argument("--hourly-cost-usd", type=Decimal, required=True)
    parser.add_argument("--absolute-cost-ceiling-usd", type=Decimal, required=True)
    args = parser.parse_args()
    if not 3600 <= args.max_seconds <= 28800:
        parser.error("invalid campaign time envelope")
    if not 600 <= args.finalization_reserve_seconds < args.max_seconds:
        parser.error("invalid finalization reserve")
    if args.hourly_cost_usd <= 0 or args.absolute_cost_ceiling_usd <= 0:
        parser.error("invalid campaign cost envelope")
    return args


def main() -> int:
    try:
        ExpansionCampaign(parse_args()).execute()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        print(f"expansion campaign failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
