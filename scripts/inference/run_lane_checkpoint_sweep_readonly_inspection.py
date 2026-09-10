#!/usr/bin/env python3
"""Execute only the approved read-only checks for the v3 checkpoint sweep."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from scripts.inference.build_lane_checkpoint_sweep_upload_plan import canonical_sha256
from scripts.inference.build_lane_checkpoint_sweep_upload_receipt import load_sealed
from scripts.inference.run_lane_probe_readonly_inspection import run_json


ROOT = Path(__file__).resolve().parents[2]
PROJECT = "executespecv1"
SERVICE_ACCOUNT = "1061994342941-compute@developer.gserviceaccount.com"
BUCKET = "ganesh-gate0-model-transfer-1061994342941"


def execute(root: Path = ROOT) -> dict[str, Any]:
    base = root / "measurement/gate4/lane-stratified-probe-checkpoint-sweep-20260910"
    plan = load_sealed(base / "gcloud-readonly-inspection-plan.json", "inspection_plan_sha256")
    approval = load_sealed(base / "gcloud-readonly-inspection-approval.json", "approval_sha256")
    if (
        plan.get("status") != "pending-explicit-gcloud-readonly-approval"
        or approval.get("status") != "approved"
        or approval.get("approved_plan_sha256") != plan["inspection_plan_sha256"]
    ):
        raise ValueError("read-only approval does not bind the sealed plan")
    gcloud = shutil.which("gcloud")
    if not gcloud:
        raise RuntimeError("gcloud is unavailable")
    evidence = base / "inspection"
    run_json(gcloud, ["compute", "zones", "describe", plan["zone"], f"--project={PROJECT}"], evidence / "provider/zone.json")
    run_json(gcloud, ["compute", "machine-types", "describe", "g2-standard-8", f"--zone={plan['zone']}", f"--project={PROJECT}"], evidence / "provider/machine-type.json")
    run_json(gcloud, ["compute", "accelerator-types", "describe", "nvidia-l4", f"--zone={plan['zone']}", f"--project={PROJECT}"], evidence / "provider/accelerator-type.json")
    run_json(gcloud, ["compute", "regions", "describe", plan["region"], f"--project={PROJECT}"], evidence / "provider/region.json")
    absence_commands = {
        "instance": ["compute", "instances", "describe", plan["planned_resource_names"]["instance"], f"--zone={plan['zone']}", f"--project={PROJECT}"],
        "disk": ["compute", "disks", "describe", plan["planned_resource_names"]["disk"], f"--zone={plan['zone']}", f"--project={PROJECT}"],
        "network": ["compute", "networks", "describe", plan["planned_resource_names"]["network"], f"--project={PROJECT}"],
        "subnet": ["compute", "networks", "subnets", "describe", plan["planned_resource_names"]["subnet"], f"--region={plan['region']}", f"--project={PROJECT}"],
    }
    for name, command in absence_commands.items():
        code, _ = run_json(gcloud, command, evidence / f"absence/{name}.json", expected_codes={1})
        if code != 1:
            raise RuntimeError(f"planned {name} unexpectedly exists")
    run_json(gcloud, ["storage", "buckets", "get-iam-policy", f"gs://{BUCKET}", f"--project={PROJECT}"], evidence / "iam/bucket-policy.json")
    run_json(gcloud, ["projects", "get-iam-policy", PROJECT, "--flatten=bindings[].members", f"--filter=bindings.members:serviceAccount:{SERVICE_ACCOUNT}"], evidence / "iam/project-roles.json")
    run_json(gcloud, ["iam", "service-accounts", "get-iam-policy", SERVICE_ACCOUNT, f"--project={PROJECT}"], evidence / "iam/service-account-policy.json")
    for name, row in sorted(plan["generation_pinned_inputs"].items()):
        run_json(gcloud, ["storage", "objects", "describe", row["uri"], f"--project={PROJECT}"], evidence / f"objects/{name}.json")
    summary = {
        "schema_version": "ganesh-mini-lane-checkpoint-sweep-readonly-command-summary/v1",
        "status": "commands-complete",
        "inspection_plan_sha256": plan["inspection_plan_sha256"],
        "approval_sha256": approval["approval_sha256"],
        "provider_checks": 4,
        "absence_checks": 4,
        "iam_checks": 3,
        "object_checks": len(plan["generation_pinned_inputs"]),
        "cloud_mutations": [],
    }
    summary["summary_sha256"] = canonical_sha256(summary)
    (evidence / "command-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    summary = execute(args.root.resolve())
    print(json.dumps({"status": summary["status"], "summary_sha256": summary["summary_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
