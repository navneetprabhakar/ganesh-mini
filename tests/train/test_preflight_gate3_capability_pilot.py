import json
import hashlib
import sys
from types import SimpleNamespace
from argparse import Namespace
from pathlib import Path

import pytest

from scripts.train.preflight_gate3_capability_pilot import ROOT, assess, verify_model_inventory
from scripts.train.build_gate3_capability_card import (build_draft, bind_provider,
    probe_cuda_host, GCLOUD_BUCKET, GCLOUD_PROJECT, GCLOUD_PROVIDER_SCHEMA,
    GCLOUD_TEARDOWN_SCHEMA)
from scripts.train.run_sft import CAPABILITY_CARD_SCHEMA, canonical_sha256, validate_capability_pilot_invocation
from scripts.train.measure_gate3_capability_throughput import select_probe_rows


CONFIG = ROOT / "configs/train/gate3_capability_pilot_v1.json"


def test_current_pilot_inputs_pass_but_no_card_is_ready():
    result = assess(CONFIG)
    assert result["records"] == 900
    assert result["input_tokens"] == 651639
    assert result["validation_records"] == 50
    assert result["static_inputs_passed"] is True
    assert result["execution_card_ready"] is False
    assert result["training_executed"] is False
    draft = build_draft(CONFIG)
    assert draft["status"] == "prepared-not-executable"
    assert draft["provider_execution"] is None
    assert draft["selected_recipe"]["lr_selection_budget_seen_tokens_per_candidate"] == 651639


@pytest.mark.parametrize("field,value", [
    ("schema_version", "ganesh-mini-expansion-pilot-config/v1"),
    ("input_tokens", 2438853),
    ("sequence_length", 3072),
])
def test_old_schema_or_changed_budget_fails_closed(tmp_path: Path, field: str, value):
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    if field == "schema_version":
        config[field] = value
    elif field == "input_tokens":
        config["data"][field] = value
    else:
        config["recipe"][field] = value
    changed = tmp_path / "config.json"
    changed.write_text(json.dumps(config), encoding="utf-8")
    with pytest.raises(ValueError):
        assess(changed)


def test_runner_rejects_old_card_before_model_load(monkeypatch):
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    card = build_draft(CONFIG)
    monkeypatch.setattr("scripts.train.preflight_gate3_capability_pilot.assess",
                        lambda _: {"static_inputs_passed": True, "host_os_and_cuda_detected": True})
    monkeypatch.setattr("scripts.train.preflight_gate3_capability_pilot.verify_model_inventory",
                        lambda *_: {"files_verified": 13})
    monkeypatch.setattr("scripts.train.build_gate3_capability_card.EVIDENCE_FILES", ())
    args = Namespace(config=CONFIG, model_dir=ROOT / "models/qwen3.5-2b-15852e8",
                     prepared_manifest=ROOT / config["data"]["prepared_manifest_path"],
                     prepared_data=ROOT / config["data"]["prepared_train_path"],
                     validation_data=ROOT / config["data"]["prepared_validation_path"],
                     phase="lr-candidate", maximum_seen_tokens=651639,
                     hourly_cost_usd=1.0, prior_cost_usd=0.0, cost_ceiling_usd=2.0)
    recipe = card["selected_recipe"]
    card["provider_execution"] = {"schema_version": "ganesh-mini-capability-pilot-provider/v1",
                                  "provider": "non-gcloud", "measured_input_tokens_per_second": 100,
                                  "durable_backup_uri": "s3://test-only/pilot",
                                  "hourly_cost_usd": 1.0, "prior_cost_usd": 0.0,
                                  "cost_ceiling_usd": 2.0}
    validate_capability_pilot_invocation(args, card, config, card["inputs"]["config_sha256"])
    old = dict(card, schema_version="ganesh-mini-expansion-pilot-card/v1")
    with pytest.raises(RuntimeError, match="separate card"):
        validate_capability_pilot_invocation(args, old, config, card["inputs"]["config_sha256"])
    changed = dict(card, selected_recipe=dict(recipe, lora_rank=16))
    with pytest.raises(RuntimeError, match="recipe differs"):
        validate_capability_pilot_invocation(args, changed, config, card["inputs"]["config_sha256"])
    assert canonical_sha256(card) != canonical_sha256(old)


def test_runner_accepts_only_bounded_gcloud_provider_identity(monkeypatch):
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    card = build_draft(CONFIG)
    monkeypatch.setattr("scripts.train.preflight_gate3_capability_pilot.assess",
                        lambda _: {"static_inputs_passed": True,
                                   "host_os_and_cuda_detected": True})
    monkeypatch.setattr("scripts.train.preflight_gate3_capability_pilot.verify_model_inventory",
                        lambda *_: {"files_verified": 13})
    monkeypatch.setattr("scripts.train.build_gate3_capability_card.EVIDENCE_FILES", ())
    monkeypatch.setattr("scripts.train.preflight_gate3_capability_pilot.sealed",
                        lambda path, _: ({"status": "passed", "instance_id": "test-host",
                                           "model_revision": card["model"]["revision"],
                                           "prepared_train_sha256": card["inputs"]["prepared_data_sha256"]}
                                         if path.name == "probe.json" else
                                         {"schema_version": GCLOUD_TEARDOWN_SCHEMA,
                                          "durable_backup_uri":
                                              f"gs://{GCLOUD_BUCKET}/ganesh-mini-1.0/gate3/"
                                              "capability-pilot/test-attempt/candidate-1e-5",
                                          "instance_id": "test-host",
                                          "backup_before_delete": True,
                                          "double_exact_resource_absence": True,
                                          "provider_stop_seconds": 7200}))
    args = Namespace(config=CONFIG, model_dir=ROOT / "models/qwen3.5-2b-15852e8",
                     prepared_manifest=ROOT / config["data"]["prepared_manifest_path"],
                     prepared_data=ROOT / config["data"]["prepared_train_path"],
                     validation_data=ROOT / config["data"]["prepared_validation_path"],
                     phase="lr-candidate", maximum_seen_tokens=651639,
                     hourly_cost_usd=0.881021512, prior_cost_usd=0,
                     cost_ceiling_usd=5)
    provider = {
        "schema_version": GCLOUD_PROVIDER_SCHEMA, "provider": "gcloud",
        "project": GCLOUD_PROJECT, "bucket": GCLOUD_BUCKET,
        "zone": "us-central1-b", "maximum_vm_seconds": 7200,
        "region": "us-central1", "instance_id": "test-host",
        "durable_backup_uri": (f"gs://{GCLOUD_BUCKET}/ganesh-mini-1.0/"
                               "gate3/capability-pilot/test-attempt/candidate-1e-5"),
        "throughput_evidence_path": "probe.json",
        "teardown_plan_path": "teardown.json",
        "measured_input_tokens_per_second": 329,
        "hourly_cost_usd": "0.881021512", "prior_cost_usd": "0",
        "cost_ceiling_usd": "5",
    }
    card["provider_execution"] = provider
    validate_capability_pilot_invocation(args, card, config, card["inputs"]["config_sha256"])
    for changed in (dict(provider, project="other-project"),
                    dict(provider, provider="fake-gcloud"),
                    dict(provider, maximum_vm_seconds=14400)):
        card["provider_execution"] = changed
        with pytest.raises(RuntimeError, match="provider"):
            validate_capability_pilot_invocation(args, card, config,
                                                 card["inputs"]["config_sha256"])


def test_cuda_minimum_uses_approved_l4_usable_floor_but_other_gpu_remains_strict(monkeypatch):
    monkeypatch.setattr("scripts.train.build_gate3_capability_card.platform.system", lambda: "Linux")
    gpu = SimpleNamespace(name="NVIDIA L4", total_memory=23_659_151_360)
    fake_torch = SimpleNamespace(cuda=SimpleNamespace(
        is_available=lambda: True, device_count=lambda: 1,
        get_device_properties=lambda _: gpu, is_bf16_supported=lambda: True))
    monkeypatch.setitem(sys.modules, "torch", fake_torch)
    assert probe_cuda_host()["gpu_vram_bytes"] == 23_659_151_360
    gpu.total_memory = 22 * 1024**3 - 1
    with pytest.raises(RuntimeError, match="required"):
        probe_cuda_host()
    gpu.name = "NVIDIA A100"
    gpu.total_memory = 23_999_999_999
    with pytest.raises(RuntimeError, match="required"):
        probe_cuda_host()


def test_model_inventory_checks_file_bytes_and_extras(tmp_path: Path):
    model = tmp_path / "model"
    model.mkdir()
    payload = b"pinned-model-byte-sample"
    (model / "sample.bin").write_bytes(payload)
    item = {"path": "sample.bin", "size": len(payload),
            "git_oid": hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest(),
            "sha256": hashlib.sha256(payload).hexdigest()}
    inventory = tmp_path / "inventory.json"
    inventory.write_text(json.dumps({"model_id": "Qwen/Qwen3.5-2B",
                                     "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc",
                                     "files": [item]}))
    assert verify_model_inventory(model, inventory)["files_verified"] == 1
    item["git_oid"] = "0" * 40  # LFS pointer identity is not the downloaded blob.
    inventory.write_text(json.dumps({"model_id": "Qwen/Qwen3.5-2B",
                                     "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc",
                                     "files": [item]}))
    assert verify_model_inventory(model, inventory)["files_verified"] == 1
    (model / "extra.bin").write_bytes(b"unbound")
    with pytest.raises(ValueError, match="file inventory"):
        verify_model_inventory(model, inventory)


def test_throughput_probe_uses_longest_unique_training_rows():
    rows = [{"source_id": str(index), "input_ids": list(range(index + 1))}
            for index in range(20)]
    selected = select_probe_rows(rows)
    assert [row["source_id"] for row in selected] == [str(index) for index in range(19, 3, -1)]
    rows[-1]["source_id"] = rows[-2]["source_id"]
    with pytest.raises(ValueError, match="source-duplicated"):
        select_probe_rows(rows)


def test_gcloud_capability_card_requires_same_host_probe_backup_and_teardown(tmp_path: Path, monkeypatch):
    draft = build_draft(CONFIG)
    instance_id = "test-actual-host-123"
    uri = (f"gs://{GCLOUD_BUCKET}/ganesh-mini-1.0/gate3/capability-pilot/"
           "test-attempt/candidate-1e-5")
    host = {"os": "Linux", "gpu_name": "NVIDIA L4",
            "gpu_vram_bytes": 23_659_151_360, "cuda_device_count": 1,
            "bf16_supported": True}
    monkeypatch.setattr("scripts.train.build_gate3_capability_card.probe_cuda_host", lambda: host)

    def write_sealed(name: str, body: dict) -> tuple[str, str]:
        body = dict(body)
        body["report_sha256"] = canonical_sha256(body)
        path = tmp_path / name
        path.write_text(json.dumps(body), encoding="utf-8")
        return name, hashlib.sha256(path.read_bytes()).hexdigest()

    throughput_path, throughput_sha = write_sealed("throughput.json", {
        "schema_version": "ganesh-mini-capability-pilot-throughput/v1",
        "status": "passed", "instance_id": instance_id,
        "model_revision": draft["model"]["revision"],
        "recipe_sha256": canonical_sha256(draft["selected_recipe"]),
        "prepared_manifest_sha256": draft["inputs"]["prepared_manifest_sha256"],
        "prepared_train_sha256": draft["inputs"]["prepared_data_sha256"],
        "measured_input_tokens_per_second": 329.0,
    })
    backup_path, backup_sha = write_sealed("backup.json", {
        "status": "passed", "durable_backup_uri": uri,
        "roundtrip_verified": True,
    })
    teardown_path, teardown_sha = write_sealed("teardown.json", {
        "schema_version": GCLOUD_TEARDOWN_SCHEMA,
        "durable_backup_uri": uri, "instance_id": instance_id,
        "backup_before_delete": True,
        "double_exact_resource_absence": True,
        "provider_stop_seconds": 7200,
    })
    provider = {
        "schema_version": GCLOUD_PROVIDER_SCHEMA, "provider": "gcloud",
        "project": GCLOUD_PROJECT, "bucket": GCLOUD_BUCKET,
        "zone": "us-central1-b", "maximum_vm_seconds": 7200,
        "instance_id": instance_id, "measured_on_instance_id": instance_id,
        "region": "us-central1", "gpu_name": "NVIDIA L4",
        "gpu_vram_bytes": host["gpu_vram_bytes"],
        "durable_backup_uri": uri, "backup_roundtrip_verified": True,
        "throughput_evidence_path": throughput_path,
        "throughput_evidence_sha256": throughput_sha,
        "backup_roundtrip_path": backup_path,
        "backup_roundtrip_sha256": backup_sha,
        "teardown_plan_path": teardown_path,
        "teardown_plan_sha256": teardown_sha,
        "measured_input_tokens_per_second": 329.0,
        "hourly_cost_usd": "0.881021512", "prior_cost_usd": "0",
        "cost_ceiling_usd": "5",
    }
    evidence = tmp_path / "provider.json"

    def bind(value: dict):
        body = dict(value)
        body["evidence_sha256"] = canonical_sha256(body)
        evidence.write_text(json.dumps(body), encoding="utf-8")
        return bind_provider(draft, evidence, root=tmp_path)

    card = bind(provider)
    assert card["status"] == "ready"
    assert card["expected_training_seconds_with_margin"] == 2971
    assert card["provider_execution"]["provider"] == "gcloud"
    with pytest.raises(ValueError, match="bounded project"):
        bind(dict(provider, project="other-project"))
    with pytest.raises(ValueError, match="backup roundtrip"):
        bind(dict(provider, durable_backup_uri=f"gs://{GCLOUD_BUCKET}/other-prefix"))
    with pytest.raises(ValueError, match="host"):
        bind(dict(provider, measured_on_instance_id="old-qualification-host"))

    bad_teardown = json.loads((tmp_path / teardown_path).read_text())
    bad_teardown.pop("report_sha256")
    bad_teardown["backup_before_delete"] = False
    bad_teardown["report_sha256"] = canonical_sha256(bad_teardown)
    (tmp_path / teardown_path).write_text(json.dumps(bad_teardown), encoding="utf-8")
    provider["teardown_plan_sha256"] = hashlib.sha256((tmp_path / teardown_path).read_bytes()).hexdigest()
    with pytest.raises(ValueError, match="teardown"):
        bind(provider)
