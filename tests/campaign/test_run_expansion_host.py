from __future__ import annotations

import argparse
import json
import subprocess
from decimal import Decimal
from pathlib import Path

from scripts.campaign.run_expansion_host import ExpansionCampaign, default_config_relative
from scripts.campaign.run_host import canonical_sha256

ROOT = Path(__file__).resolve().parents[2]


def test_default_config_is_selected_from_sealed_card_generation() -> None:
    assert default_config_relative({"schema_version": "ganesh-mini-expansion-pilot-card/v1"}).name == "expansion_pilot_v1.json"
    assert default_config_relative({"schema_version": "ganesh-mini-expansion-pilot-card/v2"}).name == "expansion_capacity_probe_v2.json"
    assert default_config_relative({"schema_version": "ganesh-mini-expansion-pilot-card/v3"}).name == "expansion_lane_stratified_probe_v3.json"
    assert default_config_relative({"schema_version": "ganesh-mini-expansion-pilot-card/v4"}).name == "gradient_conflict_probe_v4.json"


def campaign(tmp_path: Path) -> ExpansionCampaign:
    args = argparse.Namespace(
        attempt_id="20260909T010000Z",
        eval_workspace=tmp_path / "eval",
        train_workspace=tmp_path / "train",
        max_seconds=28800,
        finalization_reserve_seconds=1800,
        hourly_cost_usd=Decimal("0.853624312"),
        absolute_cost_ceiling_usd=Decimal("7.5"),
        cuda_image="ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1-liger082",
        config_relative=Path("configs/train/expansion_pilot_v1.json"),
        model=tmp_path / "model",
        output=tmp_path / "output",
        shared_tmp=tmp_path / "shared",
    )
    return ExpansionCampaign(args)


def test_expansion_container_is_bounded_for_g2_standard_8(tmp_path: Path) -> None:
    value = campaign(tmp_path)
    value.docker = "/usr/bin/docker"
    command = value.docker_base("GANESH-EXPANSION", tmp_path / "workspace")
    assert command[command.index("--cpus") + 1] == "8"
    assert command[command.index("--memory") + 1] == "30g"
    assert command[command.index("--network") + 1] == "none"
    assert "--pull=never" in command
    assert "--read-only" in command


def test_training_receives_provider_absolute_ceiling(tmp_path: Path, monkeypatch) -> None:
    value = campaign(tmp_path)
    value.docker = "/usr/bin/docker"
    captured: list[str] = []

    def run(command, **kwargs):
        captured.extend(command)
        destination = value.output / "training" / "expansion-pilot"
        report = {"status": "complete", "state": {"seen_tokens": 100}}
        report["evidence_sha256"] = canonical_sha256(report)
        (destination / "run-evidence.json").write_text(json.dumps(report))

    monkeypatch.setattr(value, "run", run)
    config = {
        "data": {
            "prepared_manifest_path": "manifest.json",
            "prepared_train_path": "train.jsonl",
            "prepared_validation_path": "validation.jsonl",
        },
        "recipe": {"learning_rate": 0.00001},
        "control": {"maximum_seen_tokens": 100, "maximum_wall_seconds": 21600},
    }
    card = {
        "status": "ready",
        "provider_execution": {"prior_cost_usd": 0.0},
    }
    card["card_sha256"] = canonical_sha256(card)
    card_path = tmp_path / "card.json"
    card_path.write_text(json.dumps(card))
    value.train_expansion(card_path, config)
    assert captured[captured.index("--cost-ceiling-usd") + 1] == "7.5"
    assert captured[captured.index("--prior-cost-usd") + 1] == "0.0"


def test_gate4_startup_installs_docker_noninteractively() -> None:
    startup = (ROOT / "scripts/inference/gcloud_startup_expansion_pilot.sh").read_text()
    install = startup.index('dpkg --force-confold -i "$work_dir"/docker-bundle/debs/*.deb')
    assert startup.index("export DEBIAN_FRONTEND=noninteractive") < install
    assert startup.index("export DEBCONF_NONINTERACTIVE_SEEN=true") < install
    assert startup.index("export NEEDRESTART_MODE=a") < install


def test_gate4_startup_closes_loggers_before_terminal_inventory() -> None:
    startup = (ROOT / "scripts/inference/gcloud_startup_expansion_pilot.sh").read_text()
    assert "exec > >(tee" not in startup
    assert 'wait "$stdout_tee_pid" "$stderr_tee_pid"' in startup
    finish = startup[startup.index("finish() {"):startup.index("trap finish EXIT")]
    assert finish.index("stop_loggers") < finish.index("write_inventory") < finish.index("final_backup")


def test_gate4_background_jobs_do_not_hold_fifo_log_descriptors() -> None:
    startup = (ROOT / "scripts/inference/gcloud_startup_expansion_pilot.sh").read_text()
    assert '> /var/log/ganesh-gate4-watchdog.log 2>&1 & watchdog_pid=$!' in startup
    assert '2>> "$evidence_dir/nvml-samples.stderr.log" & nvml_pid=$!' in startup
    assert 'checkpoint_loop > /var/log/ganesh-gate4-checkpoint-loop.log 2>&1 & checkpoint_pid=$!' in startup


def test_gradient_audit_stop_is_terminal_without_training_or_evaluation(tmp_path: Path, monkeypatch) -> None:
    value = campaign(tmp_path)
    value.docker = "/usr/bin/docker"

    run_options: dict[str, object] = {}

    def run(command, **kwargs):
        run_options.update(kwargs)
        destination = value.output / "training" / "expansion-pilot"
        audit = {"audit_sha256": "a" * 64, "decision": {"stage_2_allowed": False}}
        report = {"status": "gradient-audit-stop", "state": {"seen_tokens": 0, "optimizer_steps": 0, "gradient_conflict_audit": audit}}
        report["evidence_sha256"] = canonical_sha256(report)
        (destination / "run-evidence.json").write_text(json.dumps(report))

    monkeypatch.setattr(value, "run", run)
    config = {
        "data": {"prepared_manifest_path": "manifest.json", "prepared_train_path": "train.jsonl", "prepared_validation_path": "validation.jsonl"},
        "recipe": {"learning_rate": 0.00001},
        "control": {"maximum_seen_tokens": 100, "maximum_wall_seconds": 21600},
    }
    card = {"status": "ready", "provider_execution": {"prior_cost_usd": 0.0}}
    card["card_sha256"] = canonical_sha256(card)
    card_path = tmp_path / "card.json"
    card_path.write_text(json.dumps(card))
    destination = value.train_expansion(card_path, config)
    assert destination == value.output / "training" / "expansion-pilot"
    assert value.phases[-1]["evidence"]["decision"] == "gradient-audit-stop"
    assert run_options["allowed_returncodes"] == (0, 2)


def test_non_promoting_canary_is_a_completed_adjudication(tmp_path: Path, monkeypatch) -> None:
    value = campaign(tmp_path)
    value.args.eval_workspace.mkdir()
    (value.args.eval_workspace / "scripts/eval").mkdir(parents=True)

    def run(command, **kwargs):
        output = Path(command[command.index("--output") + 1])
        report = {
            "schema_version": "ganesh-mini-expansion-canary-adjudication/v1",
            "status": "do-not-promote",
            "failed_checks": ["net_pass_gain"],
        }
        report["report_sha256"] = canonical_sha256(report)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report))
        return subprocess.CompletedProcess(command, 2)

    monkeypatch.setattr(subprocess, "run", run)
    report = value.adjudicate_canary(tmp_path / "card.json", tmp_path / "terminal.json", tmp_path / "candidate")
    assert report["status"] == "do-not-promote"
    assert value.phases[-1]["status"] == "passed"
    assert value.phases[-1]["evidence"]["decision"] == "do-not-promote"
