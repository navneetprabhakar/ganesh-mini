import hashlib
import json
from pathlib import Path

import pytest

from scripts.train.build_gate3_gcloud_provider_evidence import build
from scripts.train.build_gate3_capability_card import GCLOUD_BUCKET
from scripts.train.preflight_gate3_capability_pilot import canonical_sha


def test_actual_host_roundtrip_produces_sealed_provider(tmp_path: Path):
    root = tmp_path
    throughput = root / "throughput.json"
    report = {
        "schema_version": "ganesh-mini-capability-pilot-throughput/v1",
        "status": "passed", "instance_id": "123456789",
        "gpu_name": "NVIDIA L4", "gpu_vram_bytes": 23_659_151_360,
        "measured_input_tokens_per_second": 329.66,
    }
    report["report_sha256"] = canonical_sha(report)
    throughput.write_text(json.dumps(report))
    source = root / "source.txt"
    copy = root / "copy.txt"
    source.write_bytes(b"roundtrip-payload")
    copy.write_bytes(source.read_bytes())
    prefix = (f"gs://{GCLOUD_BUCKET}/ganesh-mini-1.0/gate3/"
              "capability-pilot/20260930T000000Z/candidate-1e-5")

    def invoke(**changes):
        arguments = dict(root=root, throughput_path=throughput,
                         roundtrip_source=source, roundtrip_copy=copy,
                         roundtrip_object_uri=prefix + "/preflight/source.txt#123",
                         output_dir=root / "provider", instance_id="123456789",
                         instance_name="ganesh-g3-pilot-20260930t000000z",
                         zone="us-central1-b", durable_backup_uri=prefix,
                         hourly_cost_usd="0.881021512", prior_cost_usd="0",
                         cost_ceiling_usd="5")
        arguments.update(changes)
        return build(**arguments)

    result = invoke()
    assert result["provider"] == "gcloud"
    assert result["throughput_evidence_sha256"] == hashlib.sha256(throughput.read_bytes()).hexdigest()
    assert result["evidence_sha256"] == canonical_sha({
        key: value for key, value in result.items() if key != "evidence_sha256"})
    assert json.loads((root / "provider/teardown-plan.json").read_text())["backup_before_delete"] is True


@pytest.mark.parametrize("changed,pattern", [
    ({"zone": "asia-south1-a"}, "GCloud identity"),
    ({"cost_ceiling_usd": "1"}, "provider STOP"),
    ({"instance_id": "different"}, "actual-host"),
])
def test_provider_evidence_fails_closed_before_output(tmp_path: Path, changed: dict, pattern: str):
    root = tmp_path
    report = {
        "schema_version": "ganesh-mini-capability-pilot-throughput/v1",
        "status": "passed", "instance_id": "123456789",
        "gpu_name": "NVIDIA L4", "gpu_vram_bytes": 23_659_151_360,
        "measured_input_tokens_per_second": 329.66,
    }
    report["report_sha256"] = canonical_sha(report)
    throughput = root / "throughput.json"
    throughput.write_text(json.dumps(report))
    source = root / "source.txt"
    copy = root / "copy.txt"
    source.write_bytes(b"pinned")
    copy.write_bytes(b"pinned")
    prefix = (f"gs://{GCLOUD_BUCKET}/ganesh-mini-1.0/gate3/"
              "capability-pilot/20260930T000000Z/candidate-1e-5")
    args = dict(root=root, throughput_path=throughput,
                roundtrip_source=source, roundtrip_copy=copy,
                roundtrip_object_uri=prefix + "/preflight/source.txt#123",
                output_dir=root / "provider", instance_id="123456789",
                instance_name="ganesh-g3-pilot-20260930t000000z",
                zone="us-central1-b", durable_backup_uri=prefix,
                hourly_cost_usd="0.881021512", prior_cost_usd="0",
                cost_ceiling_usd="5")
    args.update(changed)
    with pytest.raises(ValueError, match=pattern):
        build(**args)
    assert not (root / "provider").exists()


def test_roundtrip_byte_mismatch_is_rejected(tmp_path: Path):
    report = {
        "schema_version": "ganesh-mini-capability-pilot-throughput/v1",
        "status": "passed", "instance_id": "123456789",
        "gpu_name": "NVIDIA L4", "gpu_vram_bytes": 23_659_151_360,
        "measured_input_tokens_per_second": 329.66,
    }
    report["report_sha256"] = canonical_sha(report)
    throughput = tmp_path / "throughput.json"
    throughput.write_text(json.dumps(report))
    source = tmp_path / "source.txt"
    copy = tmp_path / "copy.txt"
    source.write_bytes(b"pinned")
    copy.write_bytes(b"tampered")
    prefix = (f"gs://{GCLOUD_BUCKET}/ganesh-mini-1.0/gate3/"
              "capability-pilot/20260930T000000Z/candidate-1e-5")
    with pytest.raises(ValueError, match="roundtrip bytes"):
        build(root=tmp_path, throughput_path=throughput,
              roundtrip_source=source, roundtrip_copy=copy,
              roundtrip_object_uri=prefix + "/preflight/source.txt#123",
              output_dir=tmp_path / "provider", instance_id="123456789",
              instance_name="ganesh-g3-pilot-20260930t000000z",
              zone="us-central1-b", durable_backup_uri=prefix,
              hourly_cost_usd="0.881021512", prior_cost_usd="0",
              cost_ceiling_usd="5")
