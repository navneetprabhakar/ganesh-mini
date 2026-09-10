#!/usr/bin/env python3
"""Seal the authorized v3 checkpoint-sweep read-only inspection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.inference.build_lane_checkpoint_sweep_upload_plan import canonical_sha256
from scripts.inference.build_lane_checkpoint_sweep_upload_receipt import load_sealed


ROOT = Path(__file__).resolve().parents[2]
SERVICE_ACCOUNT = "1061994342941-compute@developer.gserviceaccount.com"


def build(root: Path, checked_at: str) -> dict[str, Any]:
    base = root / "measurement/gate4/lane-stratified-probe-checkpoint-sweep-20260910"
    plan = load_sealed(base / "gcloud-readonly-inspection-plan.json", "inspection_plan_sha256")
    approval = load_sealed(base / "gcloud-readonly-inspection-approval.json", "approval_sha256")
    summary = load_sealed(base / "inspection/command-summary.json", "summary_sha256")
    if (
        approval.get("approved_plan_sha256") != plan["inspection_plan_sha256"]
        or summary.get("inspection_plan_sha256") != plan["inspection_plan_sha256"]
        or summary.get("approval_sha256") != approval["approval_sha256"]
        or summary.get("status") != "commands-complete"
        or summary.get("cloud_mutations") != []
    ):
        raise ValueError("read-only authorization chain mismatch")
    inputs = {}
    for name, expected in sorted(plan["generation_pinned_inputs"].items()):
        metadata = json.loads((base / f"inspection/objects/{name}.json").read_text())
        if metadata.get("storage_url") != expected["uri"] or int(metadata.get("size", -1)) != expected["size_bytes"]:
            raise ValueError(f"input metadata mismatch: {name}")
        inputs[name] = {
            **expected,
            "metadata_match": True,
            "content_sha256_basis": (
                "approved exact-generation byte roundtrip"
                if name.startswith("uploaded_")
                else "previous verified immutable-generation evidence"
            ),
        }
    absence = {}
    for resource in ("instance", "disk", "network", "subnet"):
        code = int((base / f"inspection/absence/{resource}.json.exit-code").read_text().strip())
        stderr = (base / f"inspection/absence/{resource}.json.stderr").read_text()
        if code != 1 or "not found" not in stderr.lower():
            raise ValueError(f"provider absence check failed: {resource}")
        absence[resource] = {"absent": True, "provider_exit_code": code}
    region = json.loads((base / "inspection/provider/region.json").read_text())
    quota = next(item for item in region["quotas"] if item["metric"] == "NVIDIA_L4_GPUS")
    zone = json.loads((base / "inspection/provider/zone.json").read_text())
    machine = json.loads((base / "inspection/provider/machine-type.json").read_text())
    accelerator = json.loads((base / "inspection/provider/accelerator-type.json").read_text())
    bucket_policy = json.loads((base / "inspection/iam/bucket-policy.json").read_text())
    object_admin = any(
        binding.get("role") == "roles/storage.objectAdmin"
        and f"serviceAccount:{SERVICE_ACCOUNT}" in binding.get("members", [])
        for binding in bucket_policy.get("bindings", [])
    )
    if not object_admin:
        raise ValueError("VM service account lacks bucket objectAdmin")
    project_roles = json.loads((base / "inspection/iam/project-roles.json").read_text())
    observed_roles = sorted({
        row.get("bindings", {}).get("role")
        for row in project_roles
        if row.get("bindings", {}).get("members") == f"serviceAccount:{SERVICE_ACCOUNT}"
    })
    price = load_sealed(
        root / "measurement/gate4/lane-stratified-probe-20260910/inspection/provider/price-evidence.json",
        "evidence_sha256",
    )
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-lane-checkpoint-sweep-gcloud-readonly-report/v1",
        "status": "complete-ready-for-separate-proposal",
        "checked_at": checked_at,
        "authorization": {
            "inspection_plan_sha256": plan["inspection_plan_sha256"],
            "approval_sha256": approval["approval_sha256"],
            "scope": "read-only-only",
        },
        "command_summary_sha256": summary["summary_sha256"],
        "planned_attempt_id": plan["planned_attempt_id"],
        "planned_resource_names": plan["planned_resource_names"],
        "resource_absence": absence,
        "provider": {
            "project": plan["project"],
            "region": plan["region"],
            "zone": plan["zone"],
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
        "pricing": {
            "billing_mode": price["billing_mode"],
            "compute_hourly_usd": str(price["machine"]["hourly_cost_usd"]),
            "pd_balanced_gib_hourly_usd": str(price["boot_disk"]["rate_usd_per_gib_hour"]),
            "same_day_price_evidence_sha256": price["evidence_sha256"],
            "sources": price["sources"],
        },
        "conclusion": {
            "prerequisites_passed": True,
            "execution_authorized": False,
            "next_boundary": "construct and request explicit approval for one exact diagnostic-only VM proposal",
            "caveat": "quota and resource-type availability do not guarantee point-in-time L4 capacity",
        },
    }
    if (
        report["provider"]["zone_status"] != "UP"
        or report["provider"]["machine_type"] != {"name": "g2-standard-8", "guest_cpus": 8, "memory_mb": 32768}
        or report["provider"]["accelerator_type"] != "nvidia-l4"
        or report["provider"]["l4_quota"]["usage"] + 1 > report["provider"]["l4_quota"]["limit"]
    ):
        raise ValueError("provider prerequisite mismatch")
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--checked-at", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = build(args.root.resolve(), args.checked_at)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"report_sha256": report["report_sha256"], "status": report["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
