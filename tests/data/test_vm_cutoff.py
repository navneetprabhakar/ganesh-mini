import json
from unittest.mock import patch

import pytest

from scripts.data import watch_vm_cutoff as watcher
from scripts.data import vm_cutoff_verify as runner


def test_cleanup_refuses_changed_instance_identity(tmp_path):
    with patch("sys.argv", ["watch", "--instance-id", "original", "--output", str(tmp_path)]), \
         patch.object(watcher, "run", return_value=json.dumps({"id": "different", "status": "TERMINATED"})) as cloud:
        with pytest.raises(RuntimeError, match="identity changed"):
            watcher.main()
    assert cloud.call_count == 1


def test_cleanup_preserves_disk_without_terminal_backup(tmp_path):
    with patch("sys.argv", ["watch", "--instance-id", "original", "--output", str(tmp_path)]), \
         patch.object(watcher, "run", side_effect=[json.dumps({"id": "original", "status": "TERMINATED"}), "[]", ""] ) as cloud:
        with pytest.raises(RuntimeError, match="terminal backup missing"):
            watcher.main()
    assert not any("delete" in call.args for call in cloud.call_args_list)


def test_failed_qualification_never_runs_full_corpus(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "cutoff.config.json").write_text(json.dumps({"lane_targets": {"go": 2}}))
    rows = [{"lane": "go", "task_type": task, "id": task} for task in ("generation", "repair")]
    with patch.object(runner.admission, "read_jsonl", return_value=rows), \
         patch.object(runner.admission, "evaluation_index", return_value={}), \
         patch.object(runner.admission, "admit_records", return_value=([], [{"reason": "failed"}])) as admit:
        with pytest.raises(RuntimeError, match="qualification failed"):
            runner.main()
    assert admit.call_count == 1
    assert not (tmp_path / "results/final.admission.json").exists()


def test_gcs_audit_mismatch_blocks_cleanup(tmp_path):
    audit = tmp_path / "audit.json"
    audit.write_text("original")
    audit.with_suffix(".json.gcs-verified").write_text("wrong bytes")
    with patch.object(watcher, "run", side_effect=["", '{"generation":"42"}', ""]):
        with pytest.raises(RuntimeError, match="roundtrip failed"):
            watcher.backup_verified(audit)


def test_inventory_preserves_errors_instead_of_claiming_no_resources():
    with patch.object(watcher, "run", side_effect=ValueError("unavailable")):
        result = watcher.billing_resource_inventory()
    assert len(result["errors"]) == 10
    assert not result["resources"]
