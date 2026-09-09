#!/usr/bin/env python3
"""Seal the authorized Gate 4 capacity-probe read-only inspection."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "measurement/gate4/capacity-probe-20260909"
PLAN_SHA = "50b3783cb1287bfa3a44e00772db6f24bfd2b70b8d102b1b9f537276042fd521"
UPLOAD_RECEIPT_SHA = "ad5c9ae541bc0ef53a0c0fdbdb9a49512e002a01920ee95e3d927fb6c4464e01"
SERVICE_ACCOUNT = "1061994342941-compute@developer.gserviceaccount.com"

REUSED_INPUTS = {
    "model_archive": ("model_archive.json", "846221797a5b57db5d7184680df4e74641a61504f687f86b81d85a471bb8c930", 3618248781),
    "cuda_image_archive": ("cuda_image_archive.json", "40a69cdc316c215ce98b42627f98a62bcb35d563cec9615b9c6e5fe4550ca799", 8236332782),
    "docker_bundle": ("docker_bundle.json", "2de5e2625e77f38d895d32bb69592970d017dcdc6494ca807421eb8ff0065245", 73522586),
    "verifier_archive": ("verifier_archive.json", "1c5c8196cdcc595d755ea506f774dee8a5699e495fe67d7c4441e7a06c21b972", 918639104),
    "verifier_manifest": ("verifier_manifest.json", "c4d0d44afb97ba02ae9bb52a6d4a79af68ce1fd1aea3583765085170acb4ff75", 17481),
    "controller": ("controller.json", "a0006bdb1ef68b3f4fe063fcfafae2b3631c26ddcd51d4611224e9e8b189327c", 11598),
}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build(root: Path = ROOT, checked_at: str = "2026-09-09T17:50:47Z") -> dict[str, Any]:
    base = root / "measurement/gate4/capacity-probe-20260909"
    plan = load(base / "gcloud-readonly-inspection-plan.json")
    if plan.get("inspection_plan_sha256") != PLAN_SHA:
        raise ValueError("inspection plan seal mismatch")

    upload = load(base / "upload/upload-receipt.json")
    if upload.get("receipt_sha256") != UPLOAD_RECEIPT_SHA or upload.get("status") != "complete":
        raise ValueError("upload receipt is not the approved completed receipt")

    inputs: dict[str, Any] = {}
    for name, (filename, sha256, size) in REUSED_INPUTS.items():
        metadata = load(base / "inspection/objects" / filename)
        if int(metadata["size"]) != size or not metadata["storage_url"].endswith("#" + str(metadata["generation"])):
            raise ValueError(f"reused input metadata mismatch: {name}")
        inputs[name] = {
            "generation_uri": metadata["storage_url"], "sha256": sha256,
            "size_bytes": size, "metadata_match": True,
            "content_sha256_basis": "prior exact-generation verified binding",
        }

    upload_names = {
        "train_workspace_archive": "new-train-workspace-tar-gz.json",
        "train_workspace_manifest": "new-train-workspace-manifest-json.json",
        "evaluation_workspace_archive": "new-evaluation-workspace-tar-gz.json",
        "evaluation_workspace_manifest": "new-evaluation-workspace-manifest-json.json",
    }
    for name, filename in upload_names.items():
        # Select by destination suffix because source naming differs for evaluation files.
        suffixes = {
            "train_workspace_archive": "train-workspace.tar.gz",
            "train_workspace_manifest": "train-workspace.manifest.json",
            "evaluation_workspace_archive": "evaluation-workspace.tar.gz",
            "evaluation_workspace_manifest": "evaluation-workspace.manifest.json",
        }
        row = next(item for item in upload["objects"] if item["destination"].endswith(suffixes[name]))
        metadata = load(base / "inspection/objects" / filename)
        if metadata["storage_url"] != row["generation_uri"] or int(metadata["size"]) != row["size_bytes"]:
            raise ValueError(f"new input metadata mismatch: {name}")
        inputs[name] = {
            "generation_uri": row["generation_uri"], "sha256": row["sha256"],
            "size_bytes": row["size_bytes"], "metadata_match": True,
            "content_sha256_basis": "approved upload receipt exact-generation roundtrip",
        }

    region = load(base / "inspection/provider/region.json")
    l4_quota = next(q for q in region["quotas"] if q["metric"] == "NVIDIA_L4_GPUS")
    bucket_policy = load(base / "inspection/iam/bucket-policy.json")
    object_admin = any(
        binding.get("role") == "roles/storage.objectAdmin"
        and f"serviceAccount:{SERVICE_ACCOUNT}" in binding.get("members", [])
        for binding in bucket_policy["bindings"]
    )
    if not object_admin:
        raise ValueError("VM service account lacks bucket objectAdmin binding")

    absence = {}
    for resource in ("instance", "disk", "network", "subnet"):
        code = int((base / f"inspection/absence/{resource}.exit-code").read_text().strip())
        stderr = (base / f"inspection/absence/{resource}.stderr").read_text()
        if code != 1 or "not found" not in stderr.lower():
            raise ValueError(f"absence check is not a provider not-found result: {resource}")
        absence[resource] = {"absent": True, "provider_exit_code": code}

    price_path = root / "measurement/gate4/gcloud/20260909T001300Z/raw/price-evidence.json"
    price = load(price_path)
    claimed_price_sha = price.pop("evidence_sha256")
    if claimed_price_sha != canonical_sha256(price):
        raise ValueError("price evidence seal mismatch")

    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capacity-probe-gcloud-readonly-inspection/v1",
        "status": "complete-ready-for-separate-proposal",
        "checked_at": checked_at,
        "authorization": {"inspection_plan_sha256": PLAN_SHA, "scope": "read-only-only"},
        "planned_attempt_id": plan["planned_attempt_id"],
        "resource_absence": absence,
        "provider": {
            "project": plan["project"], "region": plan["region"], "zone": plan["zone"],
            "zone_status": load(base / "inspection/provider/zone.json")["status"],
            "machine_type": {"name": "g2-standard-8", "guest_cpus": 8, "memory_mb": 32768},
            "accelerator_type": "nvidia-l4",
            "l4_quota": {"limit": l4_quota["limit"], "usage": l4_quota["usage"]},
            "capacity_claimed": False,
        },
        "iam": {
            "vm_service_account": SERVICE_ACCOUNT,
            "bucket": "ganesh-gate0-model-transfer-1061994342941",
            "bucket_role": "roles/storage.objectAdmin",
            "bucket_binding_present": True,
            "project_role_observed": "roles/cloudsql.client",
        },
        "inputs": inputs,
        "embedded_metadata_wrapper": {
            "path": "scripts/inference/gcloud_expansion_metadata_wrapper.sh",
            "sha256": "587ebff6c5dc4156375eeaffafcd8b5ac432a1989255222553db3ee0cf7bbd20",
            "size_bytes": 2691,
            "gcs_object_required": False,
        },
        "pricing": {
            "billing_mode": "standard-on-demand",
            "compute_hourly_usd": "0.853624312",
            "pd_balanced_gib_hourly_usd": "0.000136986",
            "same_day_price_evidence_path": str(price_path.relative_to(root)),
            "same_day_price_evidence_sha256": claimed_price_sha,
            "sources": price["sources"],
        },
        "conclusion": {
            "prerequisites_passed": True,
            "execution_authorized": False,
            "next_boundary": "construct and request explicit approval for one exact sealed VM execution proposal",
            "caveat": "quota and resource-type availability do not guarantee point-in-time L4 capacity",
        },
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=BASE / "gcloud-readonly-inspection-report.json")
    parser.add_argument("--checked-at", default="2026-09-09T17:50:47Z")
    args = parser.parse_args()
    report = build(checked_at=args.checked_at)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
