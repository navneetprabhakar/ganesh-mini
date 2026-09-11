#!/usr/bin/env python3
"""Seal the read-only GCloud inspection boundary for the v4 probe."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REUSED_INPUTS = ("model_archive", "cuda_image_archive", "docker_bundle", "verifier_archive", "verifier_manifest")
UPLOADED_INPUTS = {
    "train-workspace.tar.gz": "train_workspace_archive",
    "train-workspace.manifest.json": "train_workspace_manifest",
    "evaluation-workspace.tar.gz": "evaluation_workspace_archive",
    "evaluation-workspace.manifest.json": "evaluation_workspace_manifest",
    "startup-controller.sh": "controller",
}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def build(receipt_path: Path, prior_report_path: Path) -> dict[str, Any]:
    receipt = load_sealed(receipt_path, "receipt_sha256")
    prior = load_sealed(prior_report_path, "report_sha256")
    if receipt.get("schema_version") != "ganesh-mini-gradient-conflict-probe-gcloud-upload-receipt/v1" or receipt.get("status") != "complete-exact-generation-roundtrip-verified":
        raise ValueError("v4 upload receipt is not complete")
    if prior.get("status") != "complete-ready-for-separate-proposal":
        raise ValueError("prior provider/input report is not reusable")
    inputs = {name: dict(prior["inputs"][name]) for name in REUSED_INPUTS}
    for row in receipt["objects"]:
        name = Path(row["destination"]).name
        if name not in UPLOADED_INPUTS or row.get("byte_identical") is not True:
            raise ValueError("upload receipt object set or verification is invalid")
        inputs[UPLOADED_INPUTS[name]] = {
            "generation_uri": row["generation_uri"],
            "sha256": row["sha256"],
            "size_bytes": row["size_bytes"],
        }
    if set(inputs) != {*REUSED_INPUTS, *UPLOADED_INPUTS.values()}:
        raise ValueError("inspection input inventory is incomplete")
    attempt_id = "20260911T020000Z"
    stem = "ganesh-mini-g4-grad-20260911t020000z"
    plan: dict[str, Any] = {
        "schema_version": "ganesh-mini-gradient-conflict-probe-gcloud-readonly-plan/v1",
        "status": "pending-explicit-gcloud-readonly-approval",
        "approved_upload_receipt_sha256": receipt["receipt_sha256"],
        "reused_input_report_sha256": prior["report_sha256"],
        "project": "executespecv1",
        "region": "us-east1",
        "zone": "us-east1-c",
        "planned_attempt_id": attempt_id,
        "planned_resource_names": {"instance": stem, "disk": stem, "network": f"{stem}-net", "subnet": f"{stem}-subnet"},
        "inputs": inputs,
        "allowed_read_only_checks": [
            "describe us-east1-c status, g2-standard-8, NVIDIA L4 visibility, and regional quota usage",
            "verify the four exact planned resource names are absent",
            "read the intended VM service-account IAM bindings relevant to GCS access",
            "verify all ten generation-pinned inputs remain readable with matching metadata",
            "obtain current public/provider Standard g2-standard-8 and pd-balanced price evidence",
        ],
        "forbidden_operations": [
            "create, start, stop, update, delete, or attach any compute, disk, network, subnet, address, router, firewall, accelerator, or service-account resource",
            "upload, overwrite, delete, restore, or mutate any GCS object",
            "bind or upload an executable training card",
            "train, evaluate, promote, merge, quantize, publish, or open decision tasks",
        ],
        "output": "one sealed read-only prerequisite report used only to construct a separately approved execution proposal",
    }
    plan["inspection_plan_sha256"] = canonical_sha256(plan)
    return plan


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, default=root / "measurement/gate4/gradient-conflict-probe-20260911/upload/upload-receipt.json")
    parser.add_argument("--prior-report", type=Path, default=root / "measurement/gate4/capacity-probe-20260909/gcloud-readonly-inspection-report.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = build(args.receipt, args.prior_report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": plan["status"], "inspection_plan_sha256": plan["inspection_plan_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
