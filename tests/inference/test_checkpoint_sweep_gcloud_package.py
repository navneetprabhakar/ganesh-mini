import hashlib
import json
import sys
import tarfile
from pathlib import Path

import pytest

from scripts.inference.build_checkpoint_sweep_gcloud_proposal import (
    INPUT_KEYS, RECOVERY_GENERATION, RECOVERY_SHA256, RECOVERY_SIZE, build, canonical_sha256,
    load_bindings,
)
from scripts.inference.build_checkpoint_sweep_workspace import (
    ADDITIONS,
    RUNTIME_ADDITIONS,
    build as build_workspace,
    config_additions,
)
from scripts.inference.build_checkpoint_sweep_startup import build as build_startup
from scripts.inference.build_checkpoint_sweep_gcloud_execution import (
    build as build_execution,
    load_sealed as load_execution_input,
    main as build_execution_main,
)

ROOT = Path(__file__).resolve().parents[2]
UPLOAD_PLAN = ROOT / "measurement/gate4/checkpoint-sweep-20260909/gcloud-upload-plan.json"
UPLOAD_PLAN_V2 = ROOT / "measurement/gate4/checkpoint-sweep-20260909/gcloud-upload-plan-v2.json"
BINDINGS = ROOT / "measurement/gate4/checkpoint-sweep-20260909/gcloud-input-bindings.json"
BINDINGS_V2 = ROOT / "measurement/gate4/checkpoint-sweep-20260909/gcloud-input-bindings-v2.json"
PROPOSAL = ROOT / "measurement/gate4/checkpoint-sweep-20260909/gcloud-execution-proposal.json"
PROPOSAL_V2 = ROOT / "measurement/gate4/checkpoint-sweep-20260909/gcloud-execution-proposal-v2.json"
UPLOAD_RECEIPT = ROOT / "measurement/gate4/checkpoint-sweep-20260909/gcloud-upload-receipt.json"
UPLOAD_RECEIPT_V2 = ROOT / "measurement/gate4/checkpoint-sweep-20260909/gcloud-upload-receipt-v2.json"
ATTEMPT = ROOT / "measurement/gate4/checkpoint-sweep-20260909/attempts/20260909T105950Z"
APPROVAL = ATTEMPT / "approval.json"
EXECUTION_CARD = ATTEMPT / "execution-card.json"


def bindings() -> dict:
    inputs = {key: {"uri": f"gs://bucket/{key}#123", "sha256": "a" * 64, "size_bytes": 1} for key in INPUT_KEYS}
    inputs["recovery_archive"] = {
        "uri": f"gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/expansion-pilot-v1/attempts/20260909T025013Z/finalization/ganesh-mini-gate4-terminal-20260909T025013Z.tar.gz#{RECOVERY_GENERATION}",
        "sha256": RECOVERY_SHA256, "size_bytes": RECOVERY_SIZE,
    }
    value = {"schema_version": "ganesh-mini-checkpoint-sweep-gcloud-bindings/v1", "project": "executespecv1", "inputs": inputs}
    value["bindings_sha256"] = canonical_sha256(value)
    return value


def test_builds_pending_evaluation_only_two_hour_proposal() -> None:
    proposal = build(bindings())
    assert proposal["status"] == "pending-explicit-execution-approval"
    assert proposal["promotion_authority"] == "none" and proposal["training_allowed"] is False
    assert proposal["resource"] == proposal["resource"] | {
        "machine_type": "g2-standard-8", "accelerator": "1x NVIDIA L4", "external_ip": False,
        "automatic_restart": False, "boot_disk_auto_delete": True, "maximum_vm_lifetime_seconds": 7200,
    }
    assert proposal["cost"]["compute_upper_usd"] == "1.707248624"
    assert proposal["cost"]["boot_disk_upper_usd"] == "0.054794400"
    assert proposal["cost"]["provider_upper_usd"] == "1.762043024"
    assert proposal["cost"]["absolute_cost_ceiling_usd"] == "2.25"


def test_rejects_reconstructed_or_unpinned_recovery_archive() -> None:
    value = bindings(); value["inputs"]["recovery_archive"]["uri"] = "gs://bucket/archive"
    value["bindings_sha256"] = canonical_sha256({k: v for k, v in value.items() if k != "bindings_sha256"})
    with pytest.raises(ValueError, match="generation-pinned"):
        build(value)
    value = bindings(); value["inputs"]["recovery_archive"]["uri"] = value["inputs"]["recovery_archive"]["uri"].replace(RECOVERY_GENERATION, "999")
    value["bindings_sha256"] = canonical_sha256({k: v for k, v in value.items() if k != "bindings_sha256"})
    with pytest.raises(ValueError, match="verified Gate 4 terminal"):
        build(value)


def test_shell_contract_is_offline_bounded_and_terminal_backed_up() -> None:
    controller = (ROOT / "scripts/inference/gcloud_startup_checkpoint_sweep.sh").read_text()
    wrapper = (ROOT / "scripts/inference/gcloud_checkpoint_sweep_metadata_wrapper.sh").read_text()
    runtime = (ROOT / "scripts/campaign/run_checkpoint_sweep_host.py").read_text()
    for token in ("g2-standard-8", "MAX_SECONDS\":7200", "runtime-terminal-$attempt_id", "shutdown -h now", "boot_disk_auto_delete\":True"):
        assert token in controller
    assert '"--network", "none"' in runtime and '"--pull=never"' in runtime
    assert "dpkg --force-confold" in controller and "DEBIAN_FRONTEND=noninteractive" in controller
    assert f"#{RECOVERY_GENERATION}" in controller and RECOVERY_SHA256 in controller
    assert "launch URI must include a GCS generation" in wrapper
    assert wrapper.index("gcloud storage rsync") < wrapper.rindex("shutdown -h now")
    assert "/var/run/docker.sock" in runtime and "dst=/usr/local/bin/docker" in runtime
    assert "run_checkpoint_sweep_host.py" in controller
    restore = controller.index("exec 1>&3 2>&4")
    drain = controller.index('wait "$stdout_tee_pid" "$stderr_tee_pid" || status=92')
    inventory = controller.index("write_inventory || status=91")
    assert restore < drain < inventory


def test_workspace_package_is_deterministic_and_contains_sweep_runtime(tmp_path: Path) -> None:
    first = tmp_path / "first.tar.gz"; first_manifest = tmp_path / "first.json"
    second = tmp_path / "second.tar.gz"; second_manifest = tmp_path / "second.json"
    one = build_workspace(first, first_manifest); two = build_workspace(second, second_manifest)
    assert first.read_bytes() == second.read_bytes()
    assert one["archive"] == two["archive"] and one["promotion_authority"] == "none"
    with tarfile.open(first, "r:gz") as archive:
        names = set(archive.getnames())
    assert set(ADDITIONS) <= names


def test_workspace_package_accepts_candidate_specific_configs(tmp_path: Path) -> None:
    config_dir = "measurement/gate4/lane-stratified-probe-checkpoint-sweep-20260910/configs"
    archive = tmp_path / "candidate.tar.gz"
    manifest = build_workspace(
        archive,
        tmp_path / "candidate.json",
        base_manifest=ROOT / "artifacts/eval/workspaces/development-v7.manifest.json",
        additions=(*RUNTIME_ADDITIONS, *config_additions(config_dir)),
    )

    assert manifest["source_development_workspace_manifest"].endswith("development-v7.manifest.json")
    with tarfile.open(archive, "r:gz") as bundle:
        names = set(bundle.getnames())
    assert f"{config_dir}/manifest.json" in names
    assert "measurement/gate4/checkpoint-sweep-20260909/configs/manifest.json" not in names


def test_candidate_startup_uses_exact_config_dir_without_legacy_recovery_identity(tmp_path: Path) -> None:
    config_dir = "measurement/gate4/lane-stratified-probe-checkpoint-sweep-20260910/configs"
    output = tmp_path / "startup.sh"
    manifest = build_startup(
        ROOT / "scripts/inference/gcloud_startup_checkpoint_sweep.sh",
        config_dir,
        output,
        tmp_path / "startup.json",
    )
    rendered = output.read_text()

    assert f'configs="$work/workspace/{config_dir}"' in rendered
    assert "1788935240864459" not in rendered
    assert "RECOVERY_ARCHIVE_URI" in rendered
    assert manifest["training_allowed"] is False


def test_upload_only_plan_binds_exact_local_inputs_and_forbids_compute() -> None:
    plan = json.loads(UPLOAD_PLAN.read_text(encoding="utf-8"))
    claimed = plan.pop("upload_plan_sha256")

    assert claimed == canonical_sha256(plan)
    assert plan["status"] == "pending-explicit-gcloud-upload-approval"
    assert plan["object_count"] == 4
    assert plan["maximum_new_bytes"] == sum(row["size_bytes"] for row in plan["objects"])
    assert "create or start compute" in plan["forbidden_operations"]
    assert all(len(row["sha256"]) == 64 and row["size_bytes"] > 0 for row in plan["objects"])


def test_corrected_upload_plan_binds_three_current_inputs_and_no_compute() -> None:
    plan = load_execution_input(UPLOAD_PLAN_V2, "upload_plan_sha256")
    assert plan["source_commit"] == "1a5a2e0b201bf689b8374e6d2275aa0a47c60f4a"
    assert plan["object_count"] == 3
    assert plan["maximum_new_bytes"] == sum(row["size_bytes"] for row in plan["objects"])
    assert "create or start compute" in plan["forbidden_operations"]
    for row in plan["objects"]:
        source = ROOT / row["source"]
        assert source.stat().st_size == row["size_bytes"]
        assert hashlib.sha256(source.read_bytes()).hexdigest() == row["sha256"]
        assert "/input/1a5a2e0/" in row["destination"]


def test_corrected_upload_receipt_and_replacement_proposal_bind_exact_generations() -> None:
    plan = load_execution_input(UPLOAD_PLAN_V2, "upload_plan_sha256")
    receipt = load_execution_input(UPLOAD_RECEIPT_V2, "receipt_sha256")
    bound = load_bindings(BINDINGS_V2)
    proposal = load_execution_input(PROPOSAL_V2, "proposal_sha256")
    uploaded = {
        (row["name"], row["generation"]): (row["sha256"], row["size_bytes"], row["roundtrip"])
        for row in receipt["objects"]
    }

    assert receipt["approval"]["approved_upload_plan_sha256"] == plan["upload_plan_sha256"]
    assert receipt["bytes_uploaded"] == plan["maximum_new_bytes"]
    assert receipt["compute_or_infrastructure_action_performed"] is False
    assert proposal == build(bound)
    assert proposal["bindings_sha256"] == bound["bindings_sha256"]
    assert proposal["cost"]["absolute_cost_ceiling_usd"] == "2.25"
    assert proposal["training_allowed"] is False
    for key in ("workspace_archive", "workspace_manifest", "controller"):
        row = bound["inputs"][key]
        name, generation = row["uri"].removeprefix(
            "gs://ganesh-gate0-model-transfer-1061994342941/"
        ).rsplit("#", 1)
        assert uploaded[(name, generation)] == (row["sha256"], row["size_bytes"], "passed")


def test_committed_proposal_matches_generation_bindings_and_verified_upload() -> None:
    bound = load_bindings(BINDINGS)
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    receipt = json.loads(UPLOAD_RECEIPT.read_text(encoding="utf-8"))
    receipt_claimed = receipt.pop("receipt_sha256")

    assert proposal == build(bound)
    assert receipt_claimed == canonical_sha256(receipt)
    assert receipt["status"] == "verified-complete"
    assert receipt["compute_or_infrastructure_action_performed"] is False
    assert receipt["bindings_sha256"] == bound["bindings_sha256"]
    uploaded = {
        (row["name"], row["generation"]): (row["sha256"], row["size_bytes"], row["roundtrip"])
        for row in receipt["objects"]
    }
    for key in ("workspace_archive", "workspace_manifest", "controller", "metadata_wrapper"):
        row = bound["inputs"][key]
        name, generation = row["uri"].removeprefix("gs://ganesh-gate0-model-transfer-1061994342941/").rsplit("#", 1)
        assert uploaded[(name, generation)] == (row["sha256"], row["size_bytes"], "passed")


def test_real_approval_builds_the_exact_sealed_single_attempt_card(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    proposal = load_execution_input(PROPOSAL, "proposal_sha256")
    approval = load_execution_input(APPROVAL, "approval_sha256")
    committed = json.loads(EXECUTION_CARD.read_text(encoding="utf-8"))
    output = tmp_path / "execution-card.json"

    monkeypatch.setattr(sys, "argv", [
        "build_checkpoint_sweep_gcloud_execution.py",
        "--proposal", str(PROPOSAL),
        "--approval", str(APPROVAL),
        "--attempt-id", committed["execution"]["attempt_id"],
        "--source-commit", committed["source_commit"],
        "--output", str(output),
    ])
    assert build_execution_main() == 0

    generated = json.loads(output.read_text(encoding="utf-8"))
    expected = build_execution(
        proposal, approval, committed["execution"]["attempt_id"], committed["source_commit"],
    )
    assert generated == expected == committed
    assert generated["approval"] == {
        "proposal_sha256": proposal["proposal_sha256"],
        "approval_sha256": approval["approval_sha256"],
    }
    assert approval["approved_proposal_sha256"] == proposal["proposal_sha256"]
    assert approval["approved_scope"] == "one diagnostic-only checkpoint-sweep execution"
    assert generated["execution"]["gcs_prefix"].endswith(
        f"/attempts/{generated['execution']['attempt_id']}"
    )
    claimed = generated.pop("execution_sha256")
    assert claimed == canonical_sha256(generated)
