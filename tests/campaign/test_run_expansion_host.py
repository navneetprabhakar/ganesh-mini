from __future__ import annotations

import argparse
import json
import subprocess
from decimal import Decimal
from pathlib import Path

from scripts.campaign.run_expansion_host import ExpansionCampaign
from scripts.campaign.run_host import canonical_sha256


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
    value.train_expansion(tmp_path / "card.json", config)
    assert captured[captured.index("--cost-ceiling-usd") + 1] == "7.5"


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
