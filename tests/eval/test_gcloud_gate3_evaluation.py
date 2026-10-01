"""Local-only boundary tests; never invoke the GCloud CLI."""

from pathlib import Path
import json
import os
import shutil
import subprocess

import pytest

from scripts.eval import gcloud_gate3_evaluation as provider


STAGING = Path("measurement/gate3/capability-scale-v1/full-pilot-eval/candidate-staging-v1")


def test_real_canary_staging_is_exactly_bound():
    card = provider._stage_inputs(STAGING, "canary")
    assert card["card_sha256"] == "2c2ead6df00e2e9769ee1562216d8d6340b1d99ad1f079ec6bee9dceb502a8ff"
    assert card["selected_learning_rate"] is None


def test_real_canary_staging_cannot_run_development():
    with pytest.raises(ValueError, match="sealed canary selection"):
        provider._stage_inputs(STAGING, "development")


def test_local_prior_reserve_is_conservative(tmp_path):
    # A live evaluation preparation is intentionally unresolved and must not
    # make this read-only training-cost check depend on the current job state.
    assert provider._prior_cost(tmp_path, "canary") == provider.Decimal("3.25")
    assert provider.training_cost_reserve(provider.RESUMABLE_ATTEMPT) == provider.Decimal("0.75")


def test_boundary_rejects_budget_and_scope_changes():
    card = sample_card()
    provider.boundary(card)
    for field, value in (("decision_tasks_opened", 1), ("maximum_vm_seconds", 7201),
                         ("prior_cost_reserve_usd", "8")):
        altered = dict(card); altered[field] = value
        altered.pop("execution_sha256")
        altered["execution_sha256"] = provider.seal(altered)
        with pytest.raises(ValueError):
            provider.boundary(altered)


def sample_card():
    card = {
        "schema_version": provider.SCHEMA, "plan_sha256": provider.PLAN_SHA,
        "project": provider.PROJECT, "bucket": provider.BUCKET,
        "zone": "us-central1-b", "phase": "canary", "machine_type": "g2-standard-8",
        "maximum_vm_seconds": 7200, "absolute_incremental_ceiling_usd": "15",
        "hourly_cost_usd": str(provider.PRICE_HOURLY), "decision_tasks_opened": 0,
        "evaluation_workspace_manifest_sha256": provider.WORKSPACE_SEAL,
        "canary_manifest_sha256": provider.CANARY_SEAL, "cuda_image_id": provider.IMAGE_ID,
        "prefix": f"gs://{provider.BUCKET}/ganesh-mini-1.0/gate3/capability-pilot/evaluation/test/canary",
        "prior_cost_reserve_usd": "3.25",
        "instance": "ganesh-g3-eval-test", "disk": "ganesh-g3-eval-test",
        "network": "ganesh-g3-eval-test-net", "subnet": "ganesh-g3-eval-test-subnet",
        "boot_image": "https://example.invalid/pinned-boot-image",
        "inputs": {"cuda_host_floor": {"sha256": provider.CUDA_FLOOR_SHA},
                   "model_preflight_module": {"sha256": provider.MODEL_PREFLIGHT_SHA}},
    }
    card["execution_sha256"] = provider.seal(card)
    return card


def test_prepare_rejects_wrong_approval_before_remote_call(tmp_path, monkeypatch):
    monkeypatch.setattr(provider, "run", lambda *args: pytest.fail("remote call made"))
    with pytest.raises(ValueError, match="approved GCloud plan"):
        provider.prepare(tmp_path / "20261001T000000Z", STAGING, "canary", "us-central1-b", "wrong")


def test_development_requires_sealed_selection_before_remote_call(tmp_path, monkeypatch):
    monkeypatch.setattr(provider, "run", lambda *args: pytest.fail("remote call made"))
    with pytest.raises(ValueError, match="development requires a sealed canary selection"):
        provider.prepare(tmp_path / "20261001T000000Z", STAGING, "development", "us-central1-b", provider.PLAN_SHA)


def test_launch_refuses_project_overlap_before_create(tmp_path, monkeypatch):
    out = tmp_path / "attempt"; out.mkdir()
    provider.save(out / "execution-card.json", sample_card())
    provider.save(out / "launch-inputs.json", {
        "card": {"sha256": provider.sha(out / "execution-card.json")},
        "startup": {"sha256": "pinned"},
    })
    calls = []
    monkeypatch.setattr(provider, "_verified_snapshot", lambda *_args: out / "startup.sh")

    def fake_run(_out, label, *args):
        calls.append(label)
        if label == "project-instances-before":
            return [{"name": "unrelated-running-vm"}]
        pytest.fail(f"provider should stop before {label}")

    monkeypatch.setattr(provider, "run", fake_run)
    with pytest.raises(ValueError, match="refuse overlap"):
        provider.launch(out)
    assert calls == ["project-instances-before"]


def test_launch_requires_verified_startup_before_network_create(tmp_path, monkeypatch):
    out = tmp_path / "attempt"; out.mkdir()
    provider.save(out / "execution-card.json", sample_card())
    provider.save(out / "launch-inputs.json", {
        "card": {"sha256": provider.sha(out / "execution-card.json")},
        "startup": {"sha256": "pinned"},
    })
    monkeypatch.setattr(provider, "run", lambda *_args: pytest.fail("remote call made"))
    with pytest.raises(ValueError, match="independently verified card snapshot"):
        provider.launch(out)


def test_finalize_verifies_terminal_backup_before_delete(tmp_path, monkeypatch):
    out = tmp_path / "attempt"; out.mkdir()
    provider.save(out / "execution-card.json", sample_card())
    events = []

    def fake_backup(argv, *, check):
        events.append("backup-verified")
        target = out / "terminal-roundtrip"
        target.mkdir()
        (target / "startup-exit-code.txt").write_text("0\n")
        digest = provider.sha(target / "startup-exit-code.txt")
        (target / "runtime-files.sha256").write_text(f"{digest}  ./startup-exit-code.txt\n")
        (out / "terminal-backup-verification.json").write_text('{"status":"verified"}')

    def fake_run(_out, label, *args):
        events.append(label)
        if label.startswith("terminal-instance-"):
            return {"status": "TERMINATED"}
        return []

    monkeypatch.setattr(provider.subprocess, "run", fake_backup)
    monkeypatch.setattr(provider, "run", fake_run)
    monkeypatch.setattr(provider, "complete_local_mirror", lambda _out: events.append("control-mirror"))
    provider.finalize(out)
    assert events.index("backup-verified") < events.index("delete-instance")
    assert (out / "finalization.json").is_file()


def test_v2_requires_pinned_preflight_and_old_card_is_exact_only():
    card = sample_card()
    card["inputs"]["model_preflight_module"]["sha256"] = "0" * 64
    card.pop("execution_sha256"); card["execution_sha256"] = provider.seal(card)
    with pytest.raises(ValueError, match="preflight"):
        provider.boundary(card)
    card = sample_card(); card["schema_version"] = provider.LEGACY_SCHEMA
    card.pop("execution_sha256"); card["execution_sha256"] = provider.seal(card)
    with pytest.raises(ValueError, match="legacy"):
        provider.boundary(card)


def test_pinned_preflight_resolves_materializer_import_from_sealed_workspace(tmp_path):
    archive = provider.ROOT / "measurement/gate3/capability-scale-v1/full-pilot-eval/evaluation-workspace-v1.tar.gz"
    subprocess.run(("tar", "-xzf", str(archive), "-C", str(tmp_path)), check=True)
    target = tmp_path / "scripts/train/preflight_gate3_capability_pilot.py"
    assert not target.parent.exists()  # source 587-file archive remains unchanged
    target.parent.mkdir()
    source = provider.ROOT / "scripts/train/preflight_gate3_capability_pilot.py"
    assert provider.sha(source) == provider.MODEL_PREFLIGHT_SHA
    shutil.copyfile(source, target)
    materializer = provider.ROOT / "scripts/train/inspect_model_archive.py"
    result = subprocess.run(("python3", "-B", str(materializer), "--help"), cwd=tmp_path,
                            env={**os.environ, "PYTHONPATH": str(tmp_path)},
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "--materialize-dir" in result.stdout


def test_docker_readonly_materializer_import_rehearsal(tmp_path):
    if shutil.which("docker") is None:
        pytest.skip("local Docker unavailable")
    if subprocess.run(("docker", "image", "inspect", "python:3.12-slim"),
                      capture_output=True).returncode:
        pytest.skip("local Python image unavailable; never pull")
    archive = provider.ROOT / "measurement/gate3/capability-scale-v1/full-pilot-eval/evaluation-workspace-v1.tar.gz"
    subprocess.run(("tar", "-xzf", str(archive), "-C", str(tmp_path)), check=True)
    target = tmp_path / "scripts/train/preflight_gate3_capability_pilot.py"
    target.parent.mkdir()
    shutil.copyfile(provider.ROOT / "scripts/train/preflight_gate3_capability_pilot.py", target)
    result = subprocess.run(("docker", "run", "--pull=never", "--rm", "--network", "none",
                             "--read-only", "--cpus", "1", "--memory", "512m", "--pids-limit", "64",
                             "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
                             "--mount", f"type=bind,src={tmp_path},dst=/workspace,readonly",
                             "--mount", f"type=bind,src={provider.ROOT / 'scripts/train/inspect_model_archive.py'},dst=/materializer.py,readonly",
                             "--env", "PYTHONPATH=/workspace", "--entrypoint", "python3",
                             "python:3.12-slim", "-B", "/materializer.py", "--help"),
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    assert "--materialize-dir" in result.stdout


def test_mirror_inventory_omits_only_redundant_roundtrips(tmp_path):
    (tmp_path / "finalization.json").write_text("sealed")
    for name in provider.MIRROR_EXCLUDES:
        folder = tmp_path / name; folder.mkdir()
        (folder / "large.tar").write_text("redundant")
    assert provider._mirror_inventory(tmp_path) == {"finalization.json": (provider.sha(tmp_path / "finalization.json"), 6)}


def test_exact_failed_attempt_control_mirror_is_bounded_and_verified(tmp_path, monkeypatch):
    out = tmp_path / "20260930T231842Z"; out.mkdir()
    card = sample_card(); card["schema_version"] = provider.LEGACY_SCHEMA
    card.pop("execution_sha256"); card["execution_sha256"] = provider.seal(card)
    monkeypatch.setattr(provider, "RESUMABLE_ATTEMPT", out)
    monkeypatch.setattr(provider, "RESUME_CARD_SHA", card["execution_sha256"])
    provider.save(out / "execution-card.json", card)
    provider.save(out / "finalization.json", {
        "status": "terminal-backup-verified-and-exact-resources-absent-twice",
        "prefix": card["prefix"], "evaluation_exit_code": 1})
    provider.save(out / "terminal-backup-verification.json", {
        "status": "verified", "prefix": card["prefix"] + "/terminal"})
    for number in (1, 2):
        for key in ("instance", "disk", "network", "subnet"):
            provider.save(out / f"absence-{key}-{number}.json",
                          {"exit_code": 0, "stdout": "[]", "stderr": ""})
    redundant = out / "resume-roundtrip"; redundant.mkdir()
    (redundant / "verifier.tar").write_bytes(b"large-data")
    monkeypatch.setattr(provider, "run", lambda *_args: [])
    calls = []

    def fake_call(_out, label, args, *, timeout):
        calls.append((label, args, timeout))
        return subprocess.CompletedProcess(args, 0, "", "")

    def fake_backup(argv, *, check, timeout):
        output = Path(argv[argv.index("--output") + 1])
        prefix = argv[argv.index("--prefix") + 1]
        rows = []
        for relative, (digest, size) in provider._mirror_inventory(out).items():
            rows.append({"object_uri": prefix + "/" + relative,
                         "downloaded_sha256": digest, "size": size})
        output.write_text(json.dumps({"status": "verified", "prefix": prefix, "objects": rows}))

    monkeypatch.setattr(provider, "_call", fake_call)
    monkeypatch.setattr(provider.subprocess, "run", fake_backup)
    provider.complete_local_mirror(out)
    assert len(calls) == 1 and calls[0][2] == 900
    excludes = [arg for arg in calls[0][1] if arg.startswith("--exclude=")]
    assert len(excludes) == 1
    assert "resume-roundtrip/.*" in excludes[0]
    assert (out / "local-control-mirror-verification.json").is_file()


def test_control_mirror_refuses_missing_double_absence_before_remote_call(tmp_path, monkeypatch):
    out = tmp_path / "20260930T231842Z"; out.mkdir()
    card = sample_card()
    provider.save(out / "execution-card.json", card)
    provider.save(out / "finalization.json", {
        "status": "terminal-backup-verified-and-exact-resources-absent-twice", "prefix": card["prefix"]})
    provider.save(out / "terminal-backup-verification.json", {
        "status": "verified", "prefix": card["prefix"] + "/terminal"})
    monkeypatch.setattr(provider, "run", lambda *_args: pytest.fail("remote call before proof"))
    with pytest.raises(FileNotFoundError):
        provider.complete_local_mirror(out)


def test_exact_partial_attempt_can_resume_but_never_duplicate_card(tmp_path, monkeypatch):
    out = tmp_path / "20260930T231842Z"; out.mkdir()
    monkeypatch.setattr(provider, "RESUMABLE_ATTEMPT", out)
    for name in ("evaluation_workspace", "evaluation_manifest", "candidate_inputs", "staging_card"):
        for action in ("upload", "metadata", "roundtrip"):
            (out / f"{action}-{name}.json").write_text('{"exit_code":0}')
    provider._resume_boundary(out, "canary", "us-central1-b", True)
    with pytest.raises(ValueError, match="only the exact"):
        provider._resume_boundary(out, "canary", "us-central1-c", True)
    (out / "execution-card.json").write_text("{}")
    with pytest.raises(ValueError, match="invalid execution_sha256"):
        provider._resume_boundary(out, "canary", "us-central1-b", True)


def test_reused_object_requires_fresh_generation_and_hash_roundtrip(tmp_path, monkeypatch):
    source = tmp_path / "verifier.tar"; source.write_bytes(b"pinned-image-archive")
    out = tmp_path / "attempt"; out.mkdir()
    reuse = {"uri": "gs://example/old/verifier.tar#123", "sha256": provider.sha(source),
             "size_bytes": source.stat().st_size}
    monkeypatch.setattr(provider, "_describe_object", lambda *_: {"generation": "123", "size": source.stat().st_size})
    calls = []

    def fake_call(_out, label, args, *, timeout):
        calls.append((label, args, timeout))
        assert label.startswith("download-") and args[2] == reuse["uri"]
        shutil.copyfile(source, args[3])
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(provider, "_call", fake_call)
    binding = provider._upload_verified(out, "gs://example/new", "verifier_images", source, reuse=reuse)
    assert binding == {"uri": reuse["uri"], "sha256": reuse["sha256"], "size_bytes": reuse["size_bytes"]}
    assert len(calls) == 1 and calls[0][2] == provider.LARGE_OBJECT_TIMEOUT
    assert json.loads(next(out.glob("resume-verified-*.json")).read_text())["status"] == "verified"


def test_resume_launch_reuses_exact_network_and_starts_instance_once(tmp_path, monkeypatch):
    out = tmp_path / "20260930T231842Z"; out.mkdir()
    stem = f"ganesh-g3-eval-{out.name.lower()}"
    card = sample_card()
    card.update({"instance": stem, "disk": stem, "network": stem + "-net",
                 "subnet": stem + "-subnet", "zone": "us-central1-b"})
    card.pop("execution_sha256"); card["execution_sha256"] = provider.seal(card)
    provider.save(out / "execution-card.json", card)
    monkeypatch.setattr(provider, "RESUMABLE_ATTEMPT", out)
    monkeypatch.setattr(provider, "RESUME_CARD_SHA", card["execution_sha256"])
    monkeypatch.setattr(provider, "_prior_cost", lambda *args, **kwargs: provider.Decimal("3.25"))
    launch_inputs = {}
    for name in ("card", "startup"):
        snapshot = out / "resume-roundtrip" / f"{name}-1-file"
        snapshot.parent.mkdir(exist_ok=True)
        snapshot.write_bytes((out / "execution-card.json").read_bytes() if name == "card" else b"startup")
        binding = {"uri": f"gs://example/{name}#1", "sha256": provider.sha(snapshot),
                   "size_bytes": snapshot.stat().st_size}
        launch_inputs[name] = binding
        provider.save(out / f"resume-verified-{name}-1.json",
                      {"status": "verified", "roundtrip_path": str(snapshot), **binding})
    provider.save(out / "launch-inputs.json", launch_inputs)
    provider.save(out / "create-network.json", {"exit_code": 0,
        "command": ["compute", "networks", "create", card["network"], "--subnet-mode=custom"]})
    provider.save(out / "create-subnet.json", {"exit_code": 0,
        "command": ["compute", "networks", "subnets", "create", card["subnet"],
                    "--region=us-central1", f"--network={card['network']}",
                    "--range=10.244.2.0/28", "--enable-private-ip-google-access"]})
    calls = []
    network_link = f"https://compute.googleapis.com/compute/v1/projects/{provider.PROJECT}/global/networks/{card['network']}"

    def fake_run(_out, label, *args):
        calls.append((label, args))
        if label.startswith("resume-network-state"):
            return {"name": card["network"], "selfLink": network_link, "autoCreateSubnetworks": False}
        if label.startswith("resume-subnet-state"):
            return {"name": card["subnet"], "network": network_link,
                    "ipCidrRange": "10.244.2.0/28", "privateIpGoogleAccess": True,
                    "region": "https://compute.googleapis.com/compute/v1/projects/x/regions/us-central1"}
        return []

    monkeypatch.setattr(provider, "run", fake_run)
    provider.resume_launch(out)
    creates = [args for label, args in calls if label == "create-instance"]
    assert len(creates) == 1
    assert "--max-run-duration=2h" in creates[0]
    assert "--instance-termination-action=STOP" in creates[0]
    assert any(arg.startswith("--metadata-from-file=startup-script=") for arg in creates[0])


def test_resume_launch_blocks_changed_subnet_before_vm_create(tmp_path, monkeypatch):
    out = tmp_path / "20260930T231842Z"; out.mkdir()
    monkeypatch.setattr(provider, "RESUMABLE_ATTEMPT", out)
    provider.save(out / "execution-card.json", sample_card())
    monkeypatch.setattr(provider, "RESUME_CARD_SHA", sample_card()["execution_sha256"])
    monkeypatch.setattr(provider, "_prior_cost", lambda *args, **kwargs: provider.Decimal("3.25"))
    with pytest.raises(ValueError):
        provider.resume_launch(out)
