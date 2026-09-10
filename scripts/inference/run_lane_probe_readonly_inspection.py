#!/usr/bin/env python3
"""Execute only the approved read-only GCloud checks for the lane probe."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLAN_SHA = "32804a7e859b7567910f62bc4b403fa3781a6d26b826a033775c7174d9526be4"
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


def run_json(gcloud: str, arguments: list[str], output: Path, *, expected_codes: set[int] = {0}) -> tuple[int, dict[str, Any] | None]:
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


def execute(root: Path = ROOT) -> dict[str, Any]:
    base = root / "measurement/gate4/lane-stratified-probe-20260910"
    plan = load_sealed(base / "gcloud-readonly-inspection-plan.json", "inspection_plan_sha256")
    if plan["inspection_plan_sha256"] != PLAN_SHA or plan["status"] != "pending-explicit-gcloud-readonly-approval":
        raise ValueError("inspection plan does not match the approved seal")
    receipt = load_sealed(base / "upload/upload-receipt.json", "receipt_sha256")
    if receipt["receipt_sha256"] != plan["approved_upload_receipt_sha256"] or receipt["status"] != "complete":
        raise ValueError("upload receipt does not match inspection plan")
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
    run_json(gcloud, ["projects", "get-iam-policy", PROJECT, f"--flatten=bindings[].members", f"--filter=bindings.members:serviceAccount:{SERVICE_ACCOUNT}"], evidence / "iam/project-roles.json")
    run_json(gcloud, ["iam", "service-accounts", "get-iam-policy", SERVICE_ACCOUNT, f"--project={PROJECT}"], evidence / "iam/service-account-policy.json")

    prior = load_sealed(root / "measurement/gate4/capacity-probe-20260909/gcloud-readonly-inspection-report.json", "report_sha256")
    inputs = {name: row for name, row in prior["inputs"].items() if name in {"model_archive", "cuda_image_archive", "docker_bundle", "verifier_archive", "verifier_manifest", "controller"}}
    for row in receipt["objects"]:
        name = Path(row["destination"]).name
        key = {
            "train-workspace.tar.gz": "train_workspace_archive",
            "train-workspace.manifest.json": "train_workspace_manifest",
            "evaluation-workspace.tar.gz": "evaluation_workspace_archive",
            "evaluation-workspace.manifest.json": "evaluation_workspace_manifest",
        }[name]
        inputs[key] = {"generation_uri": row["generation_uri"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]}
    for name, row in sorted(inputs.items()):
        run_json(gcloud, ["storage", "objects", "describe", row["generation_uri"], f"--project={PROJECT}"], evidence / f"objects/{name}.json")

    summary = {
        "schema_version": "ganesh-mini-lane-probe-readonly-command-summary/v1",
        "status": "commands-complete",
        "inspection_plan_sha256": PLAN_SHA,
        "provider_checks": 4,
        "absence_checks": 4,
        "iam_checks": 3,
        "object_checks": len(inputs),
        "cloud_mutations": [],
    }
    summary["summary_sha256"] = canonical_sha256(summary)
    (evidence / "command-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    report = execute(args.root.resolve())
    print(json.dumps({"status": report["status"], "summary_sha256": report["summary_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
