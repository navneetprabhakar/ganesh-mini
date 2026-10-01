import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from scripts.train.gcloud_gate3_full_pilot import (
    BUCKET, CEILING, LR_CEILING, LR_PRIOR, MATERIALIZER_SHA,
    PLAN_SHA, PRICE_HOURLY, PROJECT, SCHEMA, WORKSPACE_SHA,
    ROOT, _prior_allocation_check, boundary, prepare, seal, sha,
)


def card(learning_rate: str = "1e-5") -> dict:
    value = {
        "schema_version": SCHEMA,
        "plan_sha256": PLAN_SHA,
        "project": PROJECT, "bucket": BUCKET,
        "zone": "us-central1-b",
        "learning_rate": learning_rate,
        "maximum_vm_seconds": 7200,
        "maximum_additional_training_allocations": 2,
        "probe_rows": 16, "training_rows": 900,
        "training_input_tokens": 651639,
        "decision_tasks_opened": 0,
        "absolute_incremental_ceiling_usd": str(CEILING),
        "hourly_cost_usd": str(PRICE_HOURLY),
        "prior_cost_usd": str(LR_PRIOR[learning_rate]),
        "candidate_cost_ceiling_usd": str(LR_CEILING[learning_rate]),
        "prefix": (f"gs://{BUCKET}/ganesh-mini-1.0/gate3/"
                   "capability-pilot/20260930T000000Z/candidate-1e-5"),
        "inputs": {
            "workspace_archive": {"sha256": WORKSPACE_SHA},
            "model_materializer": {"sha256": MATERIALIZER_SHA},
        },
    }
    value["execution_sha256"] = seal(value)
    return value


def test_full_pilot_card_accepts_only_exact_scope_and_budget():
    valid = card()
    boundary(valid)
    east = dict(valid, zone="us-east1-c")
    east["execution_sha256"] = seal({k: v for k, v in east.items()
                                      if k != "execution_sha256"})
    boundary(east)
    for key, wrong in (("zone", "asia-south1-a"),
                       ("maximum_vm_seconds", 14400),
                       ("training_input_tokens", 651638),
                       ("decision_tasks_opened", 1),
                       ("absolute_incremental_ceiling_usd", "25")):
        changed = dict(valid, **{key: wrong})
        changed["execution_sha256"] = seal({k: v for k, v in changed.items()
                                             if k != "execution_sha256"})
        with pytest.raises(ValueError, match="boundary"):
            boundary(changed)


def test_prepare_rejects_unapproved_plan_before_any_gcloud(tmp_path: Path):
    out = tmp_path / "20260930T000000Z"
    with pytest.raises(ValueError, match="approved full-pilot plan"):
        prepare(out, "us-central1-b", "1e-5", "0" * 64)
    assert not out.exists()


def test_startup_cli_paths_match_frozen_data_config():
    config = json.loads((ROOT / "configs/train/gate3_capability_pilot_v1.json").read_text())
    startup = (ROOT / "scripts/train/gcloud_gate3_full_pilot_startup.sh").read_text()
    for option, key in (("--prepared-manifest", "prepared_manifest_path"),
                        ("--prepared-data", "prepared_train_path"),
                        ("--validation-data", "prepared_validation_path")):
        assert f"{option} {config['data'][key]} " in startup


def test_prepare_seals_training_only_card_without_real_gcloud(tmp_path: Path, monkeypatch):
    prior = json.loads((ROOT / "measurement/gate3/capability-scale-v1/"
                        "gcloud-qualification/20260930T131906Z/execution-card.json").read_text())
    pinned = {name: prior["inputs"][name] for name in
              ("model_archive", "cuda_image_archive", "docker_bundle")}

    def fake_run(out, label, *args):
        if label.startswith("inspect-"):
            item = pinned[label.removeprefix("inspect-")]
            return {"generation": item["uri"].rsplit("#", 1)[1],
                    "size": str(item["size_bytes"])}
        if label == "region":
            return {"quotas": [{"metric": "NVIDIA_L4_GPUS", "limit": 1,
                                "usage": 0}]}
        if label == "boot-image":
            return {"status": "READY", "id": "5785010291456121629",
                    "selfLink": "https://example.invalid/pinned-image"}
        raise AssertionError(f"unexpected command: {label} {args}")

    def fake_upload(out, prefix, label, path):
        return {"uri": prefix + "/input/" + path.name + "#123",
                "sha256": sha(path), "size_bytes": path.stat().st_size}

    monkeypatch.setattr("scripts.train.gcloud_gate3_full_pilot.run", fake_run)
    monkeypatch.setattr("scripts.train.gcloud_gate3_full_pilot.upload", fake_upload)
    out = tmp_path / "20260930T000000Z"
    prepare(out, "us-central1-b", "1e-5", PLAN_SHA)
    result = json.loads((out / "execution-card.json").read_text())
    boundary(result)
    assert result["inputs"]["workspace_archive"]["sha256"] == WORKSPACE_SHA
    assert result["learning_rate"] == "1e-5"
    assert result["maximum_vm_seconds"] == 7200
    assert result["decision_tasks_opened"] == 0


def test_prior_allocated_candidate_cannot_be_repeated(tmp_path: Path):
    with pytest.raises(ValueError, match="first learning-rate"):
        _prior_allocation_check(tmp_path, "3e-5", PLAN_SHA)
    first = tmp_path / "20260930T000000Z"
    first.mkdir()
    (first / "execution-card.json").write_text(json.dumps(card()))
    (first / "create-instance.json").write_text(json.dumps({"exit_code": 0}))
    (first / "finalization.json").write_text(json.dumps({
        "status": "terminal-backup-verified-and-exact-resources-absent-twice",
        "training_exit_code": 0}))
    (first / "terminal-backup-verification.json").write_text(json.dumps({
        "status": "verified", "object_count": 17}))
    started = datetime(2026, 9, 30, 19, 30, tzinfo=timezone.utc)
    state = {"status": "TERMINATED", "lastStartTimestamp": started.isoformat(),
             "lastStopTimestamp": (started + timedelta(seconds=800)).isoformat()}
    (first / "terminal-instance-20260930T200000Z.json").write_text(
        json.dumps({"stdout": json.dumps(state)}))
    with pytest.raises(ValueError, match="lacks sealed full-epoch report"):
        _prior_allocation_check(tmp_path, "3e-5", PLAN_SHA)
    report = {"schema_version": "ganesh-mini-sft-run/v2", "status": "complete",
              "state": {"seen_tokens": 651639}, "save_reload": {"passed": True}}
    report["evidence_sha256"] = seal(report)
    report_path = first / "terminal-roundtrip/output/training/run-evidence.json"
    report_path.parent.mkdir(parents=True)
    report_path.write_text(json.dumps(report))
    assert _prior_allocation_check(tmp_path, "3e-5", PLAN_SHA) == LR_PRIOR["3e-5"]
    with pytest.raises(ValueError, match="already exists"):
        _prior_allocation_check(tmp_path, "1e-5", PLAN_SHA)
    report["state"]["seen_tokens"] = 651638
    report["evidence_sha256"] = seal({key: value for key, value in report.items()
                                      if key != "evidence_sha256"})
    report_path.write_text(json.dumps(report))
    with pytest.raises(ValueError, match="full-epoch evidence differs"):
        _prior_allocation_check(tmp_path, "3e-5", PLAN_SHA)
    (first / "finalization.json").write_text(json.dumps({
        "status": "terminal-backup-verified-and-exact-resources-absent-twice",
        "training_exit_code": 1}))
    with pytest.raises(ValueError, match="first learning-rate"):
        _prior_allocation_check(tmp_path, "3e-5", PLAN_SHA)
    assert _prior_allocation_check(tmp_path, "1e-5", PLAN_SHA) == Decimal("0.75")
