from decimal import Decimal
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts.campaign import run_host

from scripts.campaign.run_host import (
    CONTAINER_ADAPTER,
    CONTAINER_CONTROL,
    CONTAINER_MODEL,
    CONTAINER_OUTPUT,
    CONTAINER_TRAINING,
    Campaign,
    canonical_sha256,
    docker_container_name,
    external_mount,
    lr_label,
    select_lr_evidence,
    verify_completed_candidate,
)


def test_canonical_campaign_seal_is_order_independent() -> None:
    assert canonical_sha256({"b": 2, "a": 1}) == canonical_sha256({"a": 1, "b": 2})


def test_campaign_uses_lowercase_docker_names_for_utc_attempt_ids() -> None:
    assert docker_container_name("ganesh-train-20260825T061157Z-main") == "ganesh-train-20260825t061157z-main"
    assert lr_label(0.00001)=="lr-1e-5"
    assert lr_label(0.00003)=="lr-3e-5"


def test_v2_lr_selection_uses_balanced_30_task_canary() -> None:
    lanes=("go","java","javascript","typescript","python","rust")
    low=[]
    for index in range(30):
        task_id=f"task-{index}"; low.append({"task_id":task_id,"language":lanes[index%6],"passed":False,"result_sha256":f"{index:064x}"})
    high=[dict(row) for row in low]; high[0]["passed"]=True
    run=lambda lr:{"status":"complete","identities":{"phase":"lr-candidate","learning_rate":str(lr)},"state":{"seen_tokens":461235},"evidence_sha256":str(lr).encode().hex().ljust(64,"0")[:64]}
    evidence=select_lr_evidence(low,high,run(0.00001),run(0.00003),low_lr=0.00001,high_lr=0.00003,budget=461235,rule="frozen")
    assert evidence["selected_learning_rate"]==0.00003
    assert evidence["surface"]=="development-canary"


def test_remaining_fails_before_finalization_margin(tmp_path: Path) -> None:
    args = type("Args", (), {
        "output": tmp_path, "max_seconds": 1000, "attempt_id": "test",
        "hourly_cost_usd": Decimal("1"),
    })()
    campaign = Campaign(args)
    campaign.started -= 500
    with pytest.raises(RuntimeError, match="insufficient bounded time"):
        campaign.remaining(0)


def test_phase_ledger_is_hash_sealed(tmp_path: Path) -> None:
    args = type("Args", (), {
        "output": tmp_path, "max_seconds": 3600, "attempt_id": "test",
        "hourly_cost_usd": Decimal("1"),
    })()
    campaign = Campaign(args)
    campaign.record("isolation", "passed", roots=2)
    import json
    value = json.loads((tmp_path / "phase-ledger.json").read_text())
    claimed = value.pop("evidence_sha256")
    assert canonical_sha256(value) == claimed


def test_campaign_mounts_external_state_outside_read_only_workspace(tmp_path: Path) -> None:
    model = tmp_path / "model"
    workspace = tmp_path / "workspace"
    output = tmp_path / "output"
    shared_tmp = tmp_path / "shared-tmp"
    for path in (model, workspace, output, shared_tmp):
        path.mkdir()
    args = type("Args", (), {
        "output": output, "max_seconds": 3600, "attempt_id": "test",
        "hourly_cost_usd": Decimal("1"), "model": model,
    })()
    campaign = Campaign(args)
    campaign.docker = "/usr/bin/docker"
    base = " ".join(map(str, campaign.docker_base("ganesh-test", workspace)))
    assert "dst=/workspace,readonly" in base
    assert f"dst={CONTAINER_MODEL},readonly" in base
    assert "dst=/workspace/models" not in base

    training = tmp_path / "training"
    destination = output / "evaluation" / "candidate"
    config = output / "candidate.json"
    training.mkdir(); destination.mkdir(parents=True); config.write_text("{}")
    mounts = " ".join((
        f"type=bind,src={training.resolve()},dst={CONTAINER_TRAINING},readonly",
        f"type=bind,src={destination},dst={CONTAINER_OUTPUT}",
        f"type=bind,src={output},dst={CONTAINER_CONTROL},readonly",
    ))
    assert CONTAINER_ADAPTER == CONTAINER_TRAINING / "adapter-final"
    assert "/workspace/artifacts" not in mounts
    assert "/workspace/measurement" not in mounts
    assert "/workspace/configs" not in mounts

    with pytest.raises(ValueError, match="beneath /workspace"):
        external_mount(model, Path("/workspace/models/base"), readonly=True)


def test_campaign_loads_and_audits_verifiers_without_rerunning_gate1(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    eval_workspace = tmp_path / "workspace"
    verifier_archive = tmp_path / "verifiers.tar"
    verifier_manifest = tmp_path / "verifiers.json"
    output = tmp_path / "output"
    (eval_workspace / "configs/eval").mkdir(parents=True)
    (eval_workspace / "configs/eval/runtimes.json").write_text("{}")
    verifier_archive.write_bytes(b"archive")
    verifier_manifest.write_text("{}")
    calls: list[list[str]] = []

    monkeypatch.setattr(run_host, "verify_bundle", lambda *_: {
        "manifest_sha256": "a" * 64,
        "archive": {"sha256": "b" * 64},
    })
    monkeypatch.setattr(run_host, "audit_runtime_images", lambda *_: {
        "status": "ready", "ready": 6, "expected": 6,
        "failures": [], "evidence_sha256": "c" * 64,
    })
    monkeypatch.setattr(run_host.subprocess, "run", lambda argv, **_: (
        calls.append(argv) or SimpleNamespace(returncode=0, stderr="")
    ))
    campaign = Campaign(SimpleNamespace(
        output=output, max_seconds=3600, attempt_id="test",
        hourly_cost_usd=Decimal("1"), eval_workspace=eval_workspace,
        verifier_archive=verifier_archive, verifier_manifest=verifier_manifest,
    ))
    campaign.docker = "/usr/bin/docker"

    campaign.prepare_verifier_images()

    assert calls == [["/usr/bin/docker", "load", "--input", str(verifier_archive.resolve())]]
    assert (output / "verifier-runtime-readiness.json").is_file()
    assert campaign.phases[-1]["name"] == "verifier-runtime-images"


def test_campaign_stops_before_training_when_verifier_load_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    eval_workspace = tmp_path / "workspace"
    verifier_archive = tmp_path / "verifiers.tar"
    verifier_manifest = tmp_path / "verifiers.json"
    (eval_workspace / "configs/eval").mkdir(parents=True)
    (eval_workspace / "configs/eval/runtimes.json").write_text("{}")
    verifier_archive.write_bytes(b"archive")
    verifier_manifest.write_text("{}")
    monkeypatch.setattr(run_host, "verify_bundle", lambda *_: {
        "manifest_sha256": "a" * 64,
        "archive": {"sha256": "b" * 64},
    })
    monkeypatch.setattr(run_host.subprocess, "run", lambda *_args, **_kwargs: SimpleNamespace(
        returncode=1, stderr="load rejected",
    ))
    campaign = Campaign(SimpleNamespace(
        output=tmp_path / "output", max_seconds=3600, attempt_id="test",
        hourly_cost_usd=Decimal("1"), eval_workspace=eval_workspace,
        verifier_archive=verifier_archive, verifier_manifest=verifier_manifest,
    ))
    campaign.docker = "/usr/bin/docker"

    with pytest.raises(RuntimeError, match="verifier image load failed: load rejected"):
        campaign.prepare_verifier_images()


def test_completed_candidate_import_is_bound_to_current_training_contract(tmp_path: Path) -> None:
    candidate_root = tmp_path / "candidate"
    adapter = candidate_root / "adapter-final"
    adapter.mkdir(parents=True)
    for name, content in (
        ("README.md", b"adapter"),
        ("adapter_config.json", b"{}"),
        ("adapter_model.safetensors", b"weights"),
    ):
        (adapter / name).write_bytes(content)
    recipe = {"recipe_id": "bf16-lora-conservative-v2"}
    card = {
        "status": "ready",
        "inputs": {"config_sha256": "b" * 64, "prepared_manifest_sha256": "c" * 64},
        "model": {"revision": "15852e8c16360a2fea060d615a32b45270f8a8fc"},
        "selected_recipe": recipe,
    }
    card["card_sha256"] = canonical_sha256(card)
    identities = {
        "card_sha256": card["card_sha256"],
        "config_sha256": "b" * 64,
        "prepared_manifest_sha256": "c" * 64,
        "prepared_data_sha256": "d" * 64,
        "validation_data_sha256": "e" * 64,
        "model_revision": "15852e8c16360a2fea060d615a32b45270f8a8fc",
        "recipe_sha256": canonical_sha256(recipe),
        "learning_rate": "1e-05",
        "phase": "lr-candidate",
    }
    adapter_files = {
        path.name: run_host.file_sha256(path) for path in sorted(adapter.iterdir())
    }
    run = {
        "schema_version": "ganesh-mini-sft-run/v2",
        "status": "complete",
        "identities": identities,
        "state": {"seen_tokens": 461235},
        "planned_end_row": 1399,
        "save_reload": {"passed": True},
        "adapter_files": adapter_files,
    }
    run["evidence_sha256"] = canonical_sha256(run)
    (candidate_root / "run-evidence.json").write_text(json.dumps(run))
    archive = tmp_path / "candidate.tar.gz"
    archive.write_bytes(b"sealed archive")
    files = [
        {"path": str(path.relative_to(candidate_root)), "size_bytes": path.stat().st_size, "sha256": run_host.file_sha256(path)}
        for path in sorted(candidate_root.rglob("*")) if path.is_file()
    ]
    manifest = {
        "schema_version": "ganesh-mini-completed-candidate/v1",
        "status": "sealed",
        "candidate": {
            "label": "lr-1e-5", "learning_rate": 0.00001,
            "run_evidence_sha256": run["evidence_sha256"],
            "seen_tokens": 461235, "unique_train_records": 1399,
        },
        "model": {"revision": identities["model_revision"]},
        "training_inputs": {key: identities[key] for key in (
            "card_sha256", "config_sha256", "prepared_manifest_sha256",
            "prepared_data_sha256", "validation_data_sha256", "recipe_sha256",
        )},
        "files": files,
        "archive": {"size_bytes": archive.stat().st_size, "sha256": run_host.file_sha256(archive)},
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_path = tmp_path / "candidate.json"
    manifest_path.write_text(json.dumps(manifest))

    observed_manifest, observed_run = verify_completed_candidate(
        candidate_root, manifest_path, archive,
        expected_learning_rate=0.00001, expected_tokens=461235,
        expected_records=1399,
        expected_model_revision=identities["model_revision"], training_card=card,
    )
    assert observed_manifest["manifest_sha256"] == manifest["manifest_sha256"]
    assert observed_run["evidence_sha256"] == run["evidence_sha256"]

    (adapter / "adapter_model.safetensors").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="file identity mismatch"):
        verify_completed_candidate(
            candidate_root, manifest_path, archive,
            expected_learning_rate=0.00001, expected_tokens=461235,
            expected_records=1399,
            expected_model_revision=identities["model_revision"], training_card=card,
        )
