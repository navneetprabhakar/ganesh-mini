#!/usr/bin/env python3
"""Seal actual-host GCloud pilot evidence after an independent GCS roundtrip.

This prepares a provider binding; it never creates a training card or VM.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path

from scripts.train.build_gate3_capability_card import (
    GCLOUD_BUCKET, GCLOUD_PROJECT, GCLOUD_PROVIDER_SCHEMA,
    GCLOUD_TEARDOWN_SCHEMA, GCLOUD_ZONES,
)
from scripts.train.preflight_gate3_capability_pilot import (
    ROOT, canonical_sha, file_sha, sealed,
)


def _save(path: Path, body: dict, seal_field: str) -> dict:
    value = dict(body)
    value[seal_field] = canonical_sha(value)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return value


def _relative(root: Path, path: Path) -> str:
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("provider evidence escaped training workspace")
    return str(resolved.relative_to(root.resolve()))


def build(
    *, root: Path, throughput_path: Path, roundtrip_source: Path,
    roundtrip_copy: Path, roundtrip_object_uri: str, output_dir: Path,
    instance_id: str, instance_name: str, zone: str, durable_backup_uri: str,
    hourly_cost_usd: str, prior_cost_usd: str, cost_ceiling_usd: str,
) -> dict:
    root = root.resolve()
    _relative(root, throughput_path)
    _relative(root, output_dir)
    prefix = f"gs://{GCLOUD_BUCKET}/ganesh-mini-1.0/gate3/capability-pilot/"
    suffix = durable_backup_uri.removeprefix(prefix)
    if (zone not in GCLOUD_ZONES or not instance_id or
        not instance_name.startswith("ganesh-g3-pilot-") or
        not durable_backup_uri.startswith(prefix) or
        any(part in {"", ".", ".."} for part in suffix.split("/")) or
        not roundtrip_object_uri.startswith(durable_backup_uri + "/preflight/") or
        "#" not in roundtrip_object_uri or
        not roundtrip_object_uri.rsplit("#", 1)[1].isdigit()):
        raise ValueError("GCloud identity, prefix, or pinned roundtrip escaped bound")
    hourly = Decimal(hourly_cost_usd)
    prior = Decimal(prior_cost_usd)
    ceiling = Decimal(cost_ceiling_usd)
    if (not all(value.is_finite() for value in (hourly, prior, ceiling)) or
        hourly <= 0 or prior < 0 or ceiling <= prior or
        prior + hourly * Decimal(2) > ceiling):
        raise ValueError("two-hour provider STOP does not fit candidate cost ceiling")
    throughput = sealed(throughput_path, "report_sha256")
    if (throughput.get("schema_version") != "ganesh-mini-capability-pilot-throughput/v1" or
        throughput.get("status") != "passed" or
        throughput.get("instance_id") != instance_id or
        throughput.get("gpu_name") != "NVIDIA L4" or
        throughput.get("gpu_vram_bytes", 0) < 22 * 1024**3 or
        throughput.get("measured_input_tokens_per_second", 0) <= 0):
        raise ValueError("actual-host throughput qualification differs")
    source_sha = file_sha(roundtrip_source)
    if source_sha != file_sha(roundtrip_copy) or roundtrip_source.stat().st_size != roundtrip_copy.stat().st_size:
        raise ValueError("independent GCS roundtrip bytes differ")
    output_dir.mkdir(parents=True, exist_ok=False)
    backup_path = output_dir / "backup-roundtrip.json"
    _save(backup_path, {
        "schema_version": "ganesh-mini-gate3-gcloud-backup-roundtrip/v1",
        "status": "passed", "durable_backup_uri": durable_backup_uri,
        "roundtrip_object_uri": roundtrip_object_uri,
        "source_sha256": source_sha,
        "source_size_bytes": roundtrip_source.stat().st_size,
        "roundtrip_verified": True,
        "scope": "preflight write/read only; terminal checkpoint backup is still required",
    }, "report_sha256")
    teardown_path = output_dir / "teardown-plan.json"
    _save(teardown_path, {
        "schema_version": GCLOUD_TEARDOWN_SCHEMA,
        "durable_backup_uri": durable_backup_uri,
        "instance_id": instance_id,
        "instance_name": instance_name,
        "disk_name": instance_name,
        "network_name": instance_name + "-net",
        "subnet_name": instance_name + "-subnet",
        "zone": zone,
        "backup_before_delete": True,
        "double_exact_resource_absence": True,
        "provider_stop_seconds": 7200,
    }, "report_sha256")
    provider = {
        "schema_version": GCLOUD_PROVIDER_SCHEMA,
        "provider": "gcloud", "project": GCLOUD_PROJECT,
        "bucket": GCLOUD_BUCKET, "zone": zone,
        "region": zone.rsplit("-", 1)[0],
        "instance_id": instance_id,
        "measured_on_instance_id": instance_id,
        "instance_name": instance_name,
        "maximum_vm_seconds": 7200,
        "gpu_name": throughput["gpu_name"],
        "gpu_vram_bytes": throughput["gpu_vram_bytes"],
        "durable_backup_uri": durable_backup_uri,
        "backup_roundtrip_verified": True,
        "throughput_evidence_path": _relative(root, throughput_path),
        "throughput_evidence_sha256": file_sha(throughput_path),
        "backup_roundtrip_path": _relative(root, backup_path),
        "backup_roundtrip_sha256": file_sha(backup_path),
        "teardown_plan_path": _relative(root, teardown_path),
        "teardown_plan_sha256": file_sha(teardown_path),
        "measured_input_tokens_per_second": throughput["measured_input_tokens_per_second"],
        "hourly_cost_usd": hourly_cost_usd,
        "prior_cost_usd": prior_cost_usd,
        "cost_ceiling_usd": cost_ceiling_usd,
    }
    return _save(output_dir / "provider-evidence.json", provider, "evidence_sha256")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--throughput", type=Path, required=True)
    parser.add_argument("--roundtrip-source", type=Path, required=True)
    parser.add_argument("--roundtrip-copy", type=Path, required=True)
    parser.add_argument("--roundtrip-object-uri", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--instance-name", required=True)
    parser.add_argument("--zone", required=True)
    parser.add_argument("--durable-backup-uri", required=True)
    parser.add_argument("--hourly-cost-usd", required=True)
    parser.add_argument("--prior-cost-usd", required=True)
    parser.add_argument("--cost-ceiling-usd", required=True)
    args = parser.parse_args()
    result = build(root=args.root, throughput_path=args.throughput,
                   roundtrip_source=args.roundtrip_source,
                   roundtrip_copy=args.roundtrip_copy,
                   roundtrip_object_uri=args.roundtrip_object_uri,
                   output_dir=args.output_dir, instance_id=args.instance_id,
                   instance_name=args.instance_name, zone=args.zone,
                   durable_backup_uri=args.durable_backup_uri,
                   hourly_cost_usd=args.hourly_cost_usd,
                   prior_cost_usd=args.prior_cost_usd,
                   cost_ceiling_usd=args.cost_ceiling_usd)
    print(json.dumps({"status": "provider-evidence-sealed",
                      "evidence_sha256": result["evidence_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
