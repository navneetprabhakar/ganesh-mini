import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


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
