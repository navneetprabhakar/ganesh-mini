from __future__ import annotations

import json
from pathlib import Path

from scripts.inference.build_gate1_gcloud_preparation import build, canonical_sha256


ROOT = Path(__file__).resolve().parents[2]


def test_gate1_gcloud_preparation_is_sealed_but_not_executable() -> None:
    record = build()
    claimed = record.pop("preparation_sha256")
    assert claimed == canonical_sha256(record)
    assert record["status"] == "prepared-not-executable"
    assert record["gate"] == 1
    assert record["resource_proposal"]["maximum_run_seconds"] == 64800
    assert record["resource_proposal"]["controller_budget_seconds"] + record["resource_proposal"]["backup_reserve_seconds"] == 64800
    assert record["public_price_bound"]["eighteen_hour_conservative_upper_usd"] < record["public_price_bound"]["proposed_absolute_ceiling_usd"]
    assert record["utilization"]["generation_batch_size"] == 4
    assert record["utilization"]["verifier_workers"] == 12
    assert {"execution_card_builder", "terminal_validator", "finalizer", "launcher", "price_evidence_builder", "price_evidence_schema", "baseline_admitter", "baseline_admission_schema", "training_workspace_archive", "training_workspace_manifest"} <= set(record["local_inputs"])
    assert "current_g2_standard_12_price_and_quota_preflight" in record["failed_checks"]


def test_committed_preparation_matches_builder() -> None:
    expected = build()
    observed = json.loads((ROOT / "measurement/gate1/gcloud/preparation.json").read_text(encoding="utf-8"))
    assert observed == expected


def test_gate1_startup_scripts_are_fail_closed() -> None:
    controller = (ROOT / "scripts/inference/gcloud_startup_development_baseline.sh").read_text(encoding="utf-8")
    wrapper = (ROOT / "scripts/inference/gcloud_baseline_metadata_wrapper.sh").read_text(encoding="utf-8")
    assert "set -Eeuo pipefail" in controller and "set -Eeuo pipefail" in wrapper
    assert "must include a GCS generation" in controller
    assert "--network" not in controller or "run_development_baseline_host.py" in controller
    assert "runtime-files.sha256" in controller
    assert "gcloud storage rsync" in controller
    assert controller.count("shutdown -h now") == 1  # hard-deadline watchdog only
    assert "shutdown -h now" in wrapper
    assert wrapper.index("wrapper_backed == 1") < wrapper.rindex("shutdown -h now")
    assert "GANESH_VERIFIER_ARCHIVE_URI" in wrapper
    assert "GANESH_EXECUTION_CARD_INTERNAL_SHA256" in wrapper
    assert "execution card metadata mismatch" in controller
    assert "execution card input mismatch" in controller
