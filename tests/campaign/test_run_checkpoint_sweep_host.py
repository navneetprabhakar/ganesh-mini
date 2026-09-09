from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

from scripts.campaign import run_checkpoint_sweep_host as sweep_host
from scripts.campaign.run_host import canonical_sha256


ROOT = Path(__file__).resolve().parents[2]
RECOVERED = ROOT / "measurement/gate4/gcloud/20260909T025013Z/finalization/terminal/output/campaign"
CONFIGS = ROOT / "measurement/gate4/checkpoint-sweep-20260909/configs"


def args(tmp_path: Path) -> argparse.Namespace:
    return argparse.Namespace(
        attempt_id="local-sweep-test",
        eval_workspace=tmp_path / "eval",
        eval_manifest=tmp_path / "eval-manifest.json",
        eval_archive=tmp_path / "eval.tar.gz",
        model=tmp_path / "model",
        training=tmp_path / "training",
        training_terminal=tmp_path / "terminal.json",
        config_dir=tmp_path / "configs",
        final_canary=tmp_path / "final-canary",
        verifier_manifest=tmp_path / "verifier.json",
        verifier_archive=tmp_path / "verifier.tar",
        output=tmp_path / "output",
        shared_tmp=tmp_path / "shared",
        cuda_image="qualified:image",
        cuda_image_id=sweep_host.CUDA_IMAGE_ID,
        max_seconds=7200,
        per_checkpoint_max_seconds=1200,
        finalization_reserve_seconds=600,
    )


def test_direct_entrypoint_bootstraps_repository_imports(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-I", "-B", str(Path(sweep_host.__file__).resolve()), "--help"],
        cwd=tmp_path, capture_output=True, text=True, check=False, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "--training-terminal" in result.stdout
    assert "--final-canary" in result.stdout


def test_real_sweep_inputs_bind_exactly_five_checkpoints() -> None:
    manifest, configs, final_run = sweep_host.verify_training_and_sweep(
        RECOVERED / "training/expansion-pilot",
        RECOVERED / "training-terminal.json",
        CONFIGS,
        RECOVERED / "evaluation/canary",
    )
    assert manifest["promotion_authority"] == "none"
    assert final_run["run_sha256"] == "ac6a7d5129866285f416d1f7534a4ba9315b9277d42fedda1db41b4c71b70b35"
    assert [label for label, _ in configs] == [
        "tokens-000000406491",
        "tokens-000000814098",
        "tokens-000001224637",
        "tokens-000001629235",
        "tokens-000002036559",
    ]


def test_real_packaged_workspace_matches_runner_schema(tmp_path: Path) -> None:
    archive = ROOT / "artifacts/eval/workspaces/checkpoint-sweep-v2.tar.gz"
    manifest = ROOT / "artifacts/eval/workspaces/checkpoint-sweep-v2.manifest.json"
    with tarfile.open(archive, "r:gz") as bundle:
        bundle.extractall(tmp_path)

    verified = sweep_host.verify_workspace(
        tmp_path,
        manifest,
        archive,
        sweep_host.WORKSPACE_SCHEMA,
    )

    assert verified["schema_version"] == sweep_host.WORKSPACE_SCHEMA


def test_sweep_rejects_an_extra_unsealed_config(tmp_path: Path) -> None:
    config_dir = tmp_path / "configs"
    config_dir.mkdir()
    for source in CONFIGS.iterdir():
        (config_dir / source.name).write_bytes(source.read_bytes())
    (config_dir / "tokens-evil.json").write_text("{}")
    with pytest.raises(ValueError, match="exactly the five sealed configs"):
        sweep_host.verify_training_and_sweep(
            RECOVERED / "training/expansion-pilot",
            RECOVERED / "training-terminal.json",
            config_dir,
            RECOVERED / "evaluation/canary",
        )


def test_sweep_container_is_offline_resource_limited_and_single_gpu(tmp_path: Path) -> None:
    value = sweep_host.CheckpointSweepCampaign(args(tmp_path))
    value.docker = "/usr/bin/docker"
    command = value.docker_base("GANESH-SWEEP", tmp_path / "workspace")
    assert command[command.index("--network") + 1] == "none"
    assert command[command.index("--cpus") + 1] == "8"
    assert command[command.index("--memory") + 1] == "30g"
    assert command[command.index("--gpus") + 1] == "device=0"
    assert "CUDA_VISIBLE_DEVICES=0" in command
    assert "--read-only" in command
    assert "--pull=never" in command


def test_execute_runs_five_serial_evaluations_and_seals_no_authority(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    value = sweep_host.CheckpointSweepCampaign(args(tmp_path))
    value.docker = "/usr/bin/docker"
    labels = [f"tokens-{index:012d}" for index in range(1, 6)]
    configs = [(label, tmp_path / "configs" / f"{label}.json") for label in labels]
    manifest = {
        "manifest_sha256": "a" * 64,
        "training_run_evidence_sha256": "b" * 64,
        "measured_final_checkpoint": "tokens-000000000006",
    }
    observed: list[str] = []

    monkeypatch.setattr(sweep_host.platform, "system", lambda: "Linux")
    monkeypatch.setattr(sweep_host.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(sweep_host.Path, "is_socket", lambda _self: True)
    monkeypatch.setattr(sweep_host, "verify_workspace", lambda *_args: None)
    monkeypatch.setattr(
        sweep_host, "verify_training_and_sweep",
        lambda *_args: (manifest, configs, {"run_sha256": "d" * 64}),
    )
    monkeypatch.setattr(value, "prepare_verifier_images", lambda: observed.append("verifiers"))
    monkeypatch.setattr(value, "evaluate", lambda label, _config: observed.append(label))
    monkeypatch.setattr(value, "summarize", lambda: {"report_sha256": "c" * 64})

    result = value.execute()

    assert observed == ["verifiers", *labels]
    assert result["evaluated_checkpoints"] == labels
    assert result["included_final_checkpoint"] == "tokens-000000000006"
    assert result["final_canary_run_sha256"] == "d" * 64
    assert result["promotion_authority"] == "none"
    written = json.loads((value.output / "campaign-result.json").read_text())
    claimed = written.pop("result_sha256")
    assert claimed == canonical_sha256(written)
