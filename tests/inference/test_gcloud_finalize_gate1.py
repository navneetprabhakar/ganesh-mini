from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_finalizer_orders_verified_backup_before_deletion_and_backs_teardown() -> None:
    script = (ROOT / "scripts/inference/gcloud_finalize_gate1.sh").read_text(encoding="utf-8")
    backup = script.index("gcloud_backup_manifest.py")
    terminal = script.index("verify_gate1_terminal.py")
    deletion_gate = script.index("verify_deletion_gate.py")
    delete_vm = script.index('gcloud compute instances delete')
    delete_subnet = script.index('gcloud compute networks subnets delete')
    absence = script.index("verify_absence_proof.py")
    post_delete_backup = script.index("gcloud_backup_manifest.py", absence)
    admission = script.index("admit_gate1_baseline.py")
    assert backup < terminal < deletion_gate < delete_vm < delete_subnet < absence < post_delete_backup < admission
    assert "--phase gate1-baseline" in script
    assert "cmp \"$card\" \"$terminal_dir/execution-card.json\"" in script
    assert "post-delete-final-backup-manifest.json" in script
    assert "wrapper-failure-backup-manifest.json" in script
    assert 'if [[ "$terminal_status" == 0 ]]' in script
    assert "canonical baseline admission was correctly skipped" in script


def test_finalizer_uses_only_exact_card_bound_resource_variables() -> None:
    script = (ROOT / "scripts/inference/gcloud_finalize_gate1.sh").read_text(encoding="utf-8")
    assert "invalid executable card" in script
    assert "finalizer source commit does not match" in script
    assert "run directory must be empty" in script
    assert "resources=execution['resources']" in script
    assert '--filter="name=(\'$instance\')"' in script
    assert '--filter="name=(\'$disk\')"' in script
