from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_launcher_orders_approval_preflight_upload_card_network_and_vm() -> None:
    script = (ROOT / "scripts/inference/gcloud_launch_gate1.sh").read_text(encoding="utf-8")
    approval = script.index("approval does not bind")
    identity = script.index("gcloud config get-value account")
    absence = script.index('gcloud compute instances list --zones="$zone"', identity)
    roundtrip = script.index("roundtrip_uri=")
    upload = script.index("upload_bind workspace_archive")
    card = script.index("build_gate1_gcloud_execution.py")
    network = script.index('gcloud compute networks create')
    subnet = script.index('gcloud compute networks subnets create')
    vm = script.index('gcloud compute instances create')
    assert approval < identity < absence < roundtrip < upload < card < network < subnet < vm


def test_launcher_is_bounded_private_and_uses_exact_artifacts() -> None:
    script = (ROOT / "scripts/inference/gcloud_launch_gate1.sh").read_text(encoding="utf-8")
    for token in (
        "--provisioning-model=FLEX_START",
        "--request-valid-for-duration=2h",
        "--max-run-duration=18h",
        "--instance-termination-action=DELETE",
        "--no-address",
        "--enable-private-ip-google-access",
        "--reservation-affinity=none",
        "common-cu129-ubuntu-2204-nvidia-580-v20260818",
    ):
        assert token in script
    assert "tracked worktree must be clean" in script
    assert "price evidence is older than 24 hours" in script
    assert "price evidence is dated in the future" in script
    assert "standard-fallback" in script
    assert "${run_id,,}" not in script
    assert "tr '[:upper:]' '[:lower:]'" in script


def test_launcher_cleans_failed_create_only_after_verified_backup() -> None:
    script = (ROOT / "scripts/inference/gcloud_launch_gate1.sh").read_text(encoding="utf-8")
    backup = script.index("launch-failure-backup-manifest.json")
    instance = script.index('gcloud compute instances delete')
    disk = script.index('gcloud compute disks delete')
    subnet = script.index('gcloud compute networks subnets delete')
    network = script.index('gcloud compute networks delete')
    assert backup < instance < disk < subnet < network
    assert "refusing resource deletion" in script
    absence = script.index("launch-failure-cleanup.json")
    final_backup = script.index("launch-failure-final-backup-manifest.json")
    assert network < absence < final_backup


def test_launcher_backs_preflight_before_resource_creation() -> None:
    script = (ROOT / "scripts/inference/gcloud_launch_gate1.sh").read_text(encoding="utf-8")
    backup = script.index("preflight-backup-manifest.json")
    network = script.index('resource_stage=1')
    assert backup < network
