#!/usr/bin/env python3
"""Seal the authorized Gate 4 lane-probe read-only inspection."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "measurement/gate4/lane-stratified-probe-20260910"
PLAN_SHA = "32804a7e859b7567910f62bc4b403fa3781a6d26b826a033775c7174d9526be4"
RECEIPT_SHA = "f3e127d0db29b4623fef251e76852ac1c3428fbb67d74ab79eaa1d4b00cf8e4f"
SERVICE_ACCOUNT = "1061994342941-compute@developer.gserviceaccount.com"


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def build(root: Path = ROOT, checked_at: str = "2026-09-10T04:20:07Z") -> dict[str, Any]:
    base = root / "measurement/gate4/lane-stratified-probe-20260910"
    plan = load_sealed(base / "gcloud-readonly-inspection-plan.json", "inspection_plan_sha256")
    receipt = load_sealed(base / "upload/upload-receipt.json", "receipt_sha256")
    summary = load_sealed(base / "inspection/command-summary.json", "summary_sha256")
    if plan["inspection_plan_sha256"] != PLAN_SHA or receipt["receipt_sha256"] != RECEIPT_SHA or receipt["receipt_sha256"] != plan["approved_upload_receipt_sha256"]:
        raise ValueError("inspection authorization chain mismatch")
    if summary.get("status") != "commands-complete" or summary.get("inspection_plan_sha256") != PLAN_SHA or summary.get("cloud_mutations") != []:
        raise ValueError("read-only command summary is incomplete")

    prior = load_sealed(root / "measurement/gate4/capacity-probe-20260909/gcloud-readonly-inspection-report.json", "report_sha256")
    inputs = {name: dict(row) for name, row in prior["inputs"].items() if name in {"model_archive", "cuda_image_archive", "docker_bundle", "verifier_archive", "verifier_manifest", "controller"}}
    for row in receipt["objects"]:
        key = {
            "train-workspace.tar.gz": "train_workspace_archive",
            "train-workspace.manifest.json": "train_workspace_manifest",
            "evaluation-workspace.tar.gz": "evaluation_workspace_archive",
            "evaluation-workspace.manifest.json": "evaluation_workspace_manifest",
        }[Path(row["destination"]).name]
        inputs[key] = {
            "generation_uri": row["generation_uri"], "sha256": row["sha256"],
            "size_bytes": row["size_bytes"], "content_sha256_basis": "approved upload receipt exact-generation roundtrip",
        }
    for name, row in inputs.items():
        metadata = json.loads((base / f"inspection/objects/{name}.json").read_text())
        if metadata.get("storage_url") != row["generation_uri"] or int(metadata.get("size", -1)) != row["size_bytes"]:
            raise ValueError(f"input metadata mismatch: {name}")
        row["metadata_match"] = True

    absence = {}
    for resource in ("instance", "disk", "network", "subnet"):
        code = int((base / f"inspection/absence/{resource}.json.exit-code").read_text().strip())
        stderr = (base / f"inspection/absence/{resource}.json.stderr").read_text()
        if code != 1 or "not found" not in stderr.lower():
            raise ValueError(f"absence check is not a provider not-found result: {resource}")
        absence[resource] = {"absent": True, "provider_exit_code": code}

    region = json.loads((base / "inspection/provider/region.json").read_text())
    quota = next(item for item in region["quotas"] if item["metric"] == "NVIDIA_L4_GPUS")
    zone = json.loads((base / "inspection/provider/zone.json").read_text())
    machine = json.loads((base / "inspection/provider/machine-type.json").read_text())
    accelerator = json.loads((base / "inspection/provider/accelerator-type.json").read_text())
    bucket_policy = json.loads((base / "inspection/iam/bucket-policy.json").read_text())
    object_admin = any(binding.get("role") == "roles/storage.objectAdmin" and f"serviceAccount:{SERVICE_ACCOUNT}" in binding.get("members", []) for binding in bucket_policy["bindings"])
    if not object_admin:
        raise ValueError("VM service account lacks bucket objectAdmin")
    project_roles = json.loads((base / "inspection/iam/project-roles.json").read_text())
    observed_roles = sorted({row.get("bindings", {}).get("role") for row in project_roles if row.get("bindings", {}).get("members") == f"serviceAccount:{SERVICE_ACCOUNT}"})
    price = load_sealed(base / "inspection/provider/price-evidence.json", "evidence_sha256")

    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-lane-stratified-probe-gcloud-readonly-inspection/v1",
        "status": "complete-ready-for-separate-proposal",
        "checked_at": checked_at,
        "authorization": {"inspection_plan_sha256": PLAN_SHA, "scope": "read-only-only"},
        "command_summary_sha256": summary["summary_sha256"],
        "planned_attempt_id": plan["planned_attempt_id"],
        "resource_absence": absence,
        "provider": {
            "project": plan["project"], "region": plan["region"], "zone": plan["zone"],
            "zone_status": zone.get("status"),
            "machine_type": {"name": machine.get("name"), "guest_cpus": machine.get("guestCpus"), "memory_mb": machine.get("memoryMb")},
            "accelerator_type": accelerator.get("name"),
            "l4_quota": {"limit": quota["limit"], "usage": quota["usage"]},
            "capacity_claimed": False,
        },
        "iam": {
            "vm_service_account": SERVICE_ACCOUNT,
            "bucket": "ganesh-gate0-model-transfer-1061994342941",
            "bucket_role": "roles/storage.objectAdmin",
            "bucket_binding_present": True,
            "project_roles_observed": observed_roles,
        },
        "inputs": inputs,
        "embedded_metadata_wrapper": {
            "path": "scripts/inference/gcloud_expansion_metadata_wrapper.sh",
            "sha256": "587ebff6c5dc4156375eeaffafcd8b5ac432a1989255222553db3ee0cf7bbd20",
            "size_bytes": 2691,
            "gcs_object_required": False,
        },
        "pricing": {
            "billing_mode": price["billing_mode"],
            "compute_hourly_usd": str(price["machine"]["hourly_cost_usd"]),
            "pd_balanced_gib_hourly_usd": str(price["boot_disk"]["rate_usd_per_gib_hour"]),
            "same_day_price_evidence_path": "measurement/gate4/lane-stratified-probe-20260910/inspection/provider/price-evidence.json",
            "same_day_price_evidence_sha256": price["evidence_sha256"],
            "sources": price["sources"],
        },
        "conclusion": {
            "prerequisites_passed": True,
            "execution_authorized": False,
            "next_boundary": "construct and request explicit approval for one exact sealed VM execution proposal",
            "caveat": "quota and resource-type availability do not guarantee point-in-time L4 capacity",
        },
    }
    expected_provider = report["provider"]
    if expected_provider["zone_status"] != "UP" or expected_provider["machine_type"] != {"name": "g2-standard-8", "guest_cpus": 8, "memory_mb": 32768} or expected_provider["accelerator_type"] != "nvidia-l4":
        raise ValueError("provider contract mismatch")
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=BASE / "gcloud-readonly-inspection-report.json")
    parser.add_argument("--checked-at", default="2026-09-10T04:20:07Z")
    args = parser.parse_args()
    report = build(checked_at=args.checked_at)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
