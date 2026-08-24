import json
import hashlib
import io
import subprocess
from decimal import Decimal
from pathlib import Path

import pytest

from scripts.cuda.gcloud_backup_manifest import generation_uri, stream_sha256


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_image_export_suppresses_unbounded_progress_output() -> None:
    source = (ROOT / "scripts/cuda/prebuild_cuda_image.sh").read_text()
    assert "docker save" in source
    assert "zstd --quiet -T0 -10" in source


def test_resume_export_is_bounded_quiet_and_uses_separate_terminal_prefix() -> None:
    source = (ROOT / "scripts/cuda/gcloud_resume_prebuild_gate0b.sh").read_text()
    assert "set -Eeuo pipefail" in source
    assert "timeout \"$(remaining)\" bash -c 'set -o pipefail; docker save" in source
    assert "zstd --quiet -T0 -10" in source
    assert "prebuild-terminal-attempt2" in source
    assert "prebuild-attempt2" in source
    assert "resumed_from_failed_attempt" in source
    assert "GANESH_PRIOR_BACKUP_MANIFEST_SHA256" in source
    assert "GANESH_BUILD_INPUTS_SHA256" in source
    assert "GANESH_SERIAL_RECOVERY_MANIFEST_SHA256" in source
    assert "GANESH_SERIAL_RECOVERY_FINDING_SHA256" in source
    assert "serial recovery manifest lacks nonempty verified serial output" in source
    assert "serial recovery limitation finding is not bound" in source
    assert "source file is not identical to sealed backup" in source
    assert "resume cost ceiling is not below USD 5" in source
    assert "attempt 2 GCS destinations must be empty" in source


def test_resume_plan_build_input_identity_matches_failed_backup_seal() -> None:
    evidence_root = ROOT / "measurement/cuda/gcloud/20260822T165734Z"
    plan = json.loads((evidence_root / "prebuild_resume_plan.json").read_text())
    manifest = json.loads((evidence_root / "prebuild-failed-backup-manifest.json").read_text())
    row = next(
        item
        for item in manifest["objects"]
        if item["object_uri"].endswith("/artifacts/build-inputs.sha256")
    )
    assert plan["lineage"]["build_inputs_file_sha256"] == row["downloaded_sha256"]


def test_backup_verifier_uses_vm_service_account_compatible_storage_cli() -> None:
    source = (ROOT / "scripts/cuda/gcloud_backup_manifest.py").read_text()
    assert '["gcloud", "storage", "cp"' in source
    assert '["gsutil", "-u"' not in source


def test_backup_verifier_stream_hashes_and_counts_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = b"ganesh-mini-stream-evidence"

    class Process:
        args = ["gcloud", "storage", "cat"]
        returncode = 0
        stdout = io.BytesIO(payload)
        stderr = io.BytesIO()

        def wait(self) -> int:
            return self.returncode

    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: Process())
    digest, size = stream_sha256("project", "gs://bucket/object#1")
    assert digest == hashlib.sha256(payload).hexdigest()
    assert size == len(payload)


def test_backup_verifier_generation_pins_object_reads() -> None:
    metadata = {"bucket": "evidence", "name": "run/result.json", "generation": "12345"}
    assert generation_uri(metadata) == "gs://evidence/run/result.json#12345"
    source = (ROOT / "scripts/cuda/gcloud_backup_manifest.py").read_text()
    assert "stream_sha256(args.project, immutable_uri)" in source
    assert "download(args.project, immutable_uri" in source


def test_backup_verifier_uses_bounded_concurrency() -> None:
    source = (ROOT / "scripts/cuda/gcloud_backup_manifest.py").read_text()
    assert "ThreadPoolExecutor(max_workers=args.workers)" in source
    assert 'default=8' in source
    assert 'args.workers > 32' in source


def test_backup_verifier_stream_fails_closed_on_storage_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class Process:
        args = ["gcloud", "storage", "cat"]
        returncode = 1
        stdout = io.BytesIO(b"partial")
        stderr = io.BytesIO(b"denied")

        def wait(self) -> int:
            return self.returncode

    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: Process())
    with pytest.raises(subprocess.CalledProcessError):
        stream_sha256("project", "gs://bucket/object#1")


def test_prebuild_result_is_bound_to_backup_and_deletion_evidence() -> None:
    evidence_root = ROOT / "measurement/cuda/gcloud/20260822T165734Z"
    result = json.loads((evidence_root / "prebuild_result.json").read_text())
    backup = json.loads((evidence_root / "prebuild-attempt2-backup-manifest.json").read_text())
    deletion = json.loads((evidence_root / "prebuild-attempt2-deletion-gate.json").read_text())
    post_delete = json.loads((evidence_root / "prebuild-post-delete-backup-manifest.json").read_text())

    assert result["status"] == "prebuild-complete-cuda-qualification-pending"
    assert result["attempt_2"]["backup_evidence_sha256"] == backup["evidence_sha256"]
    assert result["attempt_2"]["backup_object_count"] == backup["object_count"]
    assert result["teardown"]["deletion_gate_evidence_sha256"] == deletion["evidence_sha256"]
    assert result["teardown"]["post_delete_backup_sha256"] == post_delete["evidence_sha256"]

    archive = next(
        row for row in backup["objects"] if row["object_uri"].endswith("/cuda-image.docker.tar.zst")
    )
    assert result["attempt_2"]["archive_size_bytes"] == archive["size"]
    assert result["attempt_2"]["archive_sha256"] == archive["downloaded_sha256"]

    cost = result["cost"]
    observed = sum(
        Decimal(str(cost[key]))
        for key in (
            "prior_cumulative_compute_upper_usd",
            "failed_prebuild_attempt_upper_usd",
            "serial_recovery_compute_upper_usd",
            "resume_compute_upper_usd",
            "verification_aggregate_compute_upper_usd",
        )
    )
    assert observed == Decimal(str(cost["cumulative_compute_upper_before_gpu_usd"]))


def test_gpu_startup_preserves_terminal_backup_reserve_and_attempt_isolation() -> None:
    source = (ROOT / "scripts/cuda/gcloud_startup_gate0b.sh").read_text()
    assert 'terminal_prefix="runtime-terminal-$GANESH_ATTEMPT_ID"' in source
    assert 'checkpoint_prefix="runtime-checkpoints/$GANESH_ATTEMPT_ID"' in source
    assert '$checkpoint_prefix/$stamp.tar.gz' in source
    assert 'timeout "$(phase_timeout 180)" sha256sum -c -' in source
    assert "sha256sum -c bundle-files.sha256" in source
    assert 'timeout "$(phase_timeout 120)" bash -c' in source
    assert "GANESH_ABSOLUTE_HARD_DEADLINE_EPOCH" in source
    assert "GANESH_ABSOLUTE_CUMULATIVE_CEILING_USD" in source
    assert 'if total >= ceiling' in source
    assert 'backup_reserved_deadline_epoch="$((hard_deadline_epoch - GANESH_BACKUP_RESERVE_SECONDS))"' in source
    assert "backup_reserved_deadline_epoch < relative_controller_deadline_epoch" in source


def test_metadata_wrapper_generation_pins_and_hashes_controller() -> None:
    source = (ROOT / "scripts/cuda/gcloud_startup_metadata_wrapper.sh").read_text()
    assert "Metadata-Flavor: Google" in source
    assert "controller URI must include a GCS generation" in source
    assert "ganesh-controller-sha256" in source
    assert "ganesh-absolute-hard-deadline-epoch" in source
    assert "ganesh-absolute-cumulative-ceiling-usd" in source
    assert "ganesh-execution-card-uri" in source
    assert "ganesh-execution-card-sha256" in source
    assert "ganesh-execution-card-size" in source
    assert "sha256sum -c -" in source
    assert 'exec "$controller"' in source


def test_gpu_startup_downloads_and_verifies_bound_execution_card() -> None:
    source = (ROOT / "scripts/cuda/gcloud_startup_gate0b.sh").read_text()
    assert "GANESH_EXECUTION_CARD_URI" in source
    assert '"$evidence_dir/execution-card.json"' in source
    assert "GANESH_EXECUTION_CARD_SHA256" in source


def test_standard_a100_execution_card_binds_exact_inputs_and_cost() -> None:
    evidence_root = ROOT / "measurement/cuda/gcloud/20260822T165734Z"
    plan = json.loads((evidence_root / "gpu_run_plan.json").read_text())
    preflight = json.loads((evidence_root / "gpu-preflight-inputs-v2-backup-manifest.json").read_text())
    result = json.loads((evidence_root / "prebuild_result.json").read_text())

    assert plan["status"] == "ready-approved-not-launched"
    assert plan["resource"]["provisioning_model"] == "STANDARD"
    assert plan["resource"]["maximum_run_seconds"] == 1200
    assert plan["network"]["external_ip"] is False and plan["network"]["nat"] is False
    archived = {row["object_uri"].rsplit("/", 1)[-1]: row for row in preflight["objects"]}
    assert plan["inputs"]["controller"]["sha256"] == archived["controller.sh"]["downloaded_sha256"]
    assert plan["inputs"]["metadata_wrapper"]["sha256"] == archived["metadata-wrapper.sh"]["downloaded_sha256"]
    assert plan["inputs"]["preflight_backup_evidence_sha256"] == preflight["evidence_sha256"]
    assert plan["inputs"]["cuda_image_archive"]["sha256"] == result["attempt_2"]["archive_sha256"]
    assert plan["cost"]["prior_cumulative_compute_upper_usd"] == result["cost"]["cumulative_compute_upper_before_gpu_usd"]
