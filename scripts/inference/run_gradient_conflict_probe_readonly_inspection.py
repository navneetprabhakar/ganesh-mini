#!/usr/bin/env python3
"""Execute only an explicitly approved gradient-probe GCloud inspection."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT = "executespecv1"
SERVICE_ACCOUNT = "1061994342941-compute@developer.gserviceaccount.com"
BUCKET = "ganesh-gate0-model-transfer-1061994342941"


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def run_json(gcloud: str, arguments: list[str], output: Path, expected_codes: set[int] = {0}) -> tuple[int, Any]:
    result = subprocess.run([gcloud, *arguments, "--format=json"], text=True, capture_output=True, check=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix(output.suffix + ".stdout").write_text(result.stdout, encoding="utf-8")
    output.with_suffix(output.suffix + ".stderr").write_text(result.stderr, encoding="utf-8")
    output.with_suffix(output.suffix + ".exit-code").write_text(f"{result.returncode}\n", encoding="utf-8")
    if result.returncode not in expected_codes:
        raise RuntimeError(f"read-only command failed ({result.returncode}): {' '.join(arguments)}")
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else None
    if parsed is not None:
        output.write_text(json.dumps(parsed, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result.returncode, parsed


def execute(plan_path: Path, approval_path: Path, evidence: Path) -> dict[str, Any]:
    plan = load_sealed(plan_path, "inspection_plan_sha256")
    approval = load_sealed(approval_path, "approval_sha256")
    if plan.get("status") != "pending-explicit-gcloud-readonly-approval":
        raise ValueError("inspection plan is not pending explicit approval")
    if approval.get("status") != "approved" or approval.get("scope") != "read-only-inspection" or approval.get("approved_plan_sha256") != plan["inspection_plan_sha256"]:
        raise ValueError("approval does not bind the exact read-only plan")
    if plan.get("project") != PROJECT or len(plan.get("inputs", {})) != 10:
        raise ValueError("inspection plan escaped the project or input boundary")
    gcloud = shutil.which("gcloud")
    if not gcloud:
        raise RuntimeError("gcloud is unavailable")

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
        code, _ = run_json(gcloud, command, evidence / f"absence/{name}.json", {1})
        if code != 1:
            raise RuntimeError(f"planned {name} unexpectedly exists")

    run_json(gcloud, ["storage", "buckets", "get-iam-policy", f"gs://{BUCKET}", f"--project={PROJECT}"], evidence / "iam/bucket-policy.json")
    run_json(gcloud, ["projects", "get-iam-policy", PROJECT, "--flatten=bindings[].members", f"--filter=bindings.members:serviceAccount:{SERVICE_ACCOUNT}"], evidence / "iam/project-roles.json")
    run_json(gcloud, ["iam", "service-accounts", "get-iam-policy", SERVICE_ACCOUNT, f"--project={PROJECT}"], evidence / "iam/service-account-policy.json")

    for name, row in sorted(plan["inputs"].items()):
        run_json(gcloud, ["storage", "objects", "describe", row["generation_uri"], f"--project={PROJECT}"], evidence / f"objects/{name}.json")

    summary: dict[str, Any] = {
        "schema_version": "ganesh-mini-gradient-conflict-probe-readonly-command-summary/v1",
        "status": "commands-complete",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "inspection_plan_sha256": plan["inspection_plan_sha256"],
        "approval_sha256": approval["approval_sha256"],
        "provider_checks": 4,
        "absence_checks": 4,
        "iam_checks": 3,
        "object_checks": 10,
        "cloud_mutations": [],
    }
    summary["summary_sha256"] = canonical_sha256(summary)
    (evidence / "command-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--approval", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    summary = execute(args.plan, args.approval, args.evidence)
    print(json.dumps({"status": summary["status"], "summary_sha256": summary["summary_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
