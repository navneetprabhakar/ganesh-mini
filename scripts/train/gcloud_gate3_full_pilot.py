#!/usr/bin/env python3
"""Bound one Gate 3 full-epoch LR candidate per approved L4 VM.

This is a prospective controller. It must not be executed before its exact
plan SHA and new incremental ceiling are explicitly accepted by Navneet.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

from scripts.train.gcloud_gate3_qualification import (
    BUCKET, IMAGE, PROJECT, ROOT,
    region_for, run, save, seal, sha, upload,
)


SCHEMA = "ganesh-mini-gate3-gcloud-full-pilot/v1"
PLAN_PATH = ROOT / "docs/plans/GATE3_FULL_PILOT_GCLOUD_EXECUTION_20260930.md"
PLAN_SHA = "d4659d3b503d4eb0a0a38d5af6129f668ccef7994a7f678e920ced1a5e55dd09"
WORKSPACE_SHA = "a9eee2d31de0cf3728d10c8ee5652615006df83dbb371cf942a4e4ee79a036d8"
MATERIALIZER_SHA = "422a0559cf25de3d505304fcdcdf7aa1a92968268297c837a1ad14e2b5268b58"
PILOT_ZONES = frozenset({"us-central1-a", "us-central1-b", "us-central1-c",
                         "us-east1-b", "us-east1-c", "us-east1-d"})
PRICE_HOURLY = Decimal("0.881021512")
CEILING = Decimal("15")
LR_PRIOR = {"1e-5": Decimal("0"), "3e-5": Decimal("3")}
LR_CEILING = {"1e-5": Decimal("3"), "3e-5": Decimal("6")}
RETRY_AUTHORIZATION = "navneet-under-budget-retry-20260930"
REFUSAL_SUPPORT_RESERVE = Decimal("0.05")


def boundary(card: dict) -> None:
    body = dict(card)
    claimed = body.pop("execution_sha256", None)
    if claimed != seal(body):
        raise ValueError("full-pilot execution card seal differs")
    if (card.get("schema_version") != SCHEMA or
        card.get("plan_sha256") != PLAN_SHA or
        card.get("project") != PROJECT or
        card.get("bucket") != BUCKET or
        card.get("zone") not in PILOT_ZONES or
        card.get("learning_rate") not in LR_PRIOR or
        card.get("maximum_vm_seconds") != 7200 or
        card.get("maximum_additional_training_allocations") != 2 or
        card.get("probe_rows") != 16 or
        card.get("training_rows") != 900 or
        card.get("training_input_tokens") != 651639 or
        card.get("decision_tasks_opened") != 0 or
        card.get("absolute_incremental_ceiling_usd") != str(CEILING) or
        card.get("hourly_cost_usd") != str(PRICE_HOURLY) or
        not LR_PRIOR[card["learning_rate"]] <= Decimal(card.get("prior_cost_usd", "-1")) <= LR_CEILING[card["learning_rate"]] - PRICE_HOURLY * 2 or
        Decimal(card.get("candidate_cost_ceiling_usd", "-1")) != LR_CEILING[card["learning_rate"]] or
        card.get("inputs", {}).get("workspace_archive", {}).get("sha256") != WORKSPACE_SHA or
        card.get("inputs", {}).get("model_materializer", {}).get("sha256") != MATERIALIZER_SHA):
        raise ValueError("full-pilot scope, input or cost boundary differs")
    if not card["prefix"].startswith(
        f"gs://{BUCKET}/ganesh-mini-1.0/gate3/capability-pilot/"):
        raise ValueError("evidence prefix escaped bounded bucket")
    if LR_PRIOR[card["learning_rate"]] + PRICE_HOURLY * 2 > LR_CEILING[card["learning_rate"]]:
        raise ValueError("candidate provider STOP exceeds cost ceiling")
    if (Decimal(card["prior_cost_usd"]) > LR_PRIOR[card["learning_rate"]]) != (
        card.get("retry_authorization") == RETRY_AUTHORIZATION):
        raise ValueError("allocated retry authorization differs")


def _allocated_cost_reserve(attempt: Path) -> Decimal:
    backup = json.loads((attempt / "terminal-backup-verification.json").read_text())
    if backup.get("status") != "verified" or backup.get("object_count", 0) < 5:
        raise ValueError("allocated attempt backup is not independently verified")
    states = sorted(attempt.glob("terminal-instance-*.json"))
    if len(states) != 1:
        raise ValueError("allocated attempt has no unique terminal provider state")
    state = json.loads(json.loads(states[0].read_text())["stdout"])
    if state.get("status") != "TERMINATED":
        raise ValueError("allocated attempt is not terminal")
    seconds = (datetime.fromisoformat(state["lastStopTimestamp"]) -
               datetime.fromisoformat(state["lastStartTimestamp"])).total_seconds()
    if not 0 < seconds <= 7200:
        raise ValueError("allocated attempt exceeded provider STOP")
    measured = PRICE_HOURLY * Decimal(str(seconds)) / Decimal(3600)
    conservative = measured + Decimal("0.50") + REFUSAL_SUPPORT_RESERVE
    return (conservative * 4).to_integral_value(rounding=ROUND_CEILING) / 4


def _prior_allocation_check(parent: Path, learning_rate: str, plan_sha: str) -> Decimal:
    if plan_sha != PLAN_SHA or sha(PLAN_PATH) != PLAN_SHA:
        raise ValueError("exact approved full-pilot plan required")
    completed = set()
    retry_reserve = Decimal("0")
    for path in parent.glob("*/execution-card.json"):
        card = json.loads(path.read_text())
        if card.get("schema_version") != SCHEMA:
            continue
        boundary(card)
        create = path.parent / "create-instance.json"
        refusal = path.parent / "refusal-finalization.json"
        if not create.exists():
            raise ValueError("unresolved full-pilot preparation; never duplicate")
        result = json.loads(create.read_text())
        if result["exit_code"] == 0:
            if not (path.parent / "finalization.json").exists():
                raise ValueError("allocated candidate not finalized")
            finished = json.loads((path.parent / "finalization.json").read_text())
            if finished.get("status") != "terminal-backup-verified-and-exact-resources-absent-twice":
                raise ValueError("allocated candidate teardown differs")
            reserve = _allocated_cost_reserve(path.parent)
            if finished.get("training_exit_code") != 0:
                if card["learning_rate"] == learning_rate:
                    retry_reserve += reserve
                continue
            report_path = path.parent / "terminal-roundtrip/output/training/run-evidence.json"
            if not report_path.is_file():
                raise ValueError("earlier candidate lacks sealed full-epoch report")
            report = json.loads(report_path.read_text())
            claimed = report.pop("evidence_sha256", None)
            if (claimed != seal(report) or report.get("status") != "complete" or
                report.get("schema_version") != "ganesh-mini-sft-run/v2" or
                report.get("state", {}).get("seen_tokens") != 651639 or
                report.get("save_reload", {}).get("passed") is not True):
                raise ValueError("earlier candidate full-epoch evidence differs")
            completed.add(card["learning_rate"])
        elif not refusal.exists():
            raise ValueError("capacity refusal must be finalized before another zone")
    if learning_rate == "3e-5" and "1e-5" not in completed:
        raise ValueError("first learning-rate candidate must be completed before second")
    if learning_rate in completed:
        raise ValueError("allocated candidate already exists")
    prior = LR_PRIOR[learning_rate] + retry_reserve
    if prior + PRICE_HOURLY * 2 > LR_CEILING[learning_rate]:
        raise ValueError("allocated retry no longer fits candidate cost ceiling")
    return prior


def prepare(out: Path, zone: str, learning_rate: str, approved_plan_sha: str) -> None:
    if not WORKSPACE_SHA:
        raise ValueError("workspace SHA is not pinned; controller is not launch-ready")
    if learning_rate not in LR_PRIOR or zone not in PILOT_ZONES:
        raise ValueError("candidate or zone escaped frozen set")
    prior_cost = _prior_allocation_check(out.parent, learning_rate, approved_plan_sha)
    if out.exists():
        raise ValueError("unused evidence directory required")
    datetime.strptime(out.name, "%Y%m%dT%H%M%SZ")
    out.mkdir(parents=True)
    prefix = (f"gs://{BUCKET}/ganesh-mini-1.0/gate3/capability-pilot/"
              f"{out.name}/candidate-{learning_rate}")
    qualified = json.loads((ROOT / "measurement/gate3/capability-scale-v1/"
                            "gcloud-qualification/20260930T131906Z/execution-card.json").read_text())
    inputs = {key: qualified["inputs"][key] for key in
              ("model_archive", "cuda_image_archive", "docker_bundle")}
    for name, row in inputs.items():
        meta = run(out, f"inspect-{name}", "storage", "objects", "describe",
                   row["uri"], "--format=json")
        if (str(meta["generation"]) != row["uri"].rsplit("#", 1)[1] or
            int(meta["size"]) != row["size_bytes"]):
            raise ValueError("pinned input object differs")
    region = region_for(zone)
    quota = run(out, "region", "compute", "regions", "describe", region,
                "--format=json")
    quotas = {entry["metric"]: entry for entry in quota["quotas"]}
    if quotas["NVIDIA_L4_GPUS"]["limit"] - quotas["NVIDIA_L4_GPUS"]["usage"] < 1:
        raise ValueError("no L4 quota")
    boot = run(out, "boot-image", "compute", "images", "describe", IMAGE,
               "--project=deeplearning-platform-release", "--format=json")
    if boot["status"] != "READY" or boot["id"] != "5785010291456121629":
        raise ValueError("pinned boot image differs")
    archive = ROOT / "artifacts/train/gate3-capability-pilot-v2/workspace-v8.tar.gz"
    manifest = ROOT / "artifacts/train/gate3-capability-pilot-v2/workspace-v8-manifest.json"
    workspace = json.loads(manifest.read_text())
    if sha(archive) != WORKSPACE_SHA or workspace["archive_sha256"] != WORKSPACE_SHA:
        raise ValueError("workspace archive differs")
    if any("/eval/" in row["path"] for row in workspace["files"]):
        raise ValueError("evaluation content in training workspace")
    for label, path in (("workspace_archive", archive),
                        ("workspace_manifest", manifest),
                        ("model_materializer", ROOT / "scripts/train/inspect_model_archive.py")):
        inputs[label] = upload(out, prefix, label, path)
    stem = f"ganesh-g3-pilot-{out.name.lower()}"
    card = {
        "schema_version": SCHEMA,
        "status": "authorized-full-pilot-training-candidate-only",
        "plan_sha256": approved_plan_sha,
        "project": PROJECT, "bucket": BUCKET, "zone": zone,
        "instance": stem, "disk": stem,
        "network": stem + "-net", "subnet": stem + "-subnet",
        "prefix": prefix,
        "learning_rate": learning_rate,
        "maximum_vm_seconds": 7200,
        "maximum_additional_training_allocations": 2,
        "probe_rows": 16, "training_rows": 900,
        "training_input_tokens": 651639,
        "decision_tasks_opened": 0,
        "absolute_incremental_ceiling_usd": str(CEILING),
        "hourly_cost_usd": str(PRICE_HOURLY),
        "prior_cost_usd": str(prior_cost),
        "candidate_cost_ceiling_usd": str(LR_CEILING[learning_rate]),
        "provider_two_hour_upper_usd": str(PRICE_HOURLY * 2),
        "machine_type": "g2-standard-8",
        "boot_image": boot["selfLink"], "boot_image_id": boot["id"],
        "cuda_image_id": qualified["cuda_image_id"],
        "inputs": inputs,
        "teardown_requires": "terminal GCS inventory independently downloaded twice before deletion",
    }
    if prior_cost > LR_PRIOR[learning_rate]:
        card["retry_authorization"] = RETRY_AUTHORIZATION
    card["execution_sha256"] = seal(card)
    boundary(card)
    save(out / "execution-card.json", card)
    startup = ROOT / "scripts/train/gcloud_gate3_full_pilot_startup.sh"
    launch_inputs = {
        "card": upload(out, prefix, "card", out / "execution-card.json"),
        "startup": upload(out, prefix, "startup", startup),
    }
    save(out / "launch-inputs.json", launch_inputs)
    print(json.dumps({"status": "staged", "learning_rate": learning_rate,
                      "card_sha256": card["execution_sha256"]}))


def launch(out: Path) -> None:
    card = json.loads((out / "execution-card.json").read_text())
    boundary(card)
    launch_inputs = json.loads((out / "launch-inputs.json").read_text())
    for kind, key in (("instances", "instance"), ("disks", "disk"),
                      ("networks", "network")):
        if run(out, "absence-" + key, "compute", kind, "list",
               f"--filter=name={card[key]}", "--format=json"):
            raise ValueError("exact resource already exists")
    if run(out, "absence-subnet", "compute", "networks", "subnets", "list",
           f"--filter=name={card['subnet']}", "--format=json"):
        raise ValueError("exact subnet already exists")
    run(out, "create-network", "compute", "networks", "create",
        card["network"], "--subnet-mode=custom")
    run(out, "create-subnet", "compute", "networks", "subnets", "create",
        card["subnet"], f"--region={region_for(card['zone'])}",
        f"--network={card['network']}", "--range=10.244.1.0/28",
        "--enable-private-ip-google-access")
    startup = out / "roundtrip/gcloud_gate3_full_pilot_startup.sh"
    if sha(startup) != launch_inputs["startup"]["sha256"]:
        raise ValueError("startup snapshot differs")
    metadata = ",".join((f"ganesh-project={PROJECT}",
                         f"ganesh-prefix={card['prefix']}",
                         f"ganesh-card-uri={launch_inputs['card']['uri']}",
                         f"ganesh-card-sha={launch_inputs['card']['sha256']}"))
    run(out, "create-instance", "compute", "instances", "create", card["instance"],
        f"--zone={card['zone']}", "--machine-type=g2-standard-8",
        f"--image={card['boot_image']}", "--boot-disk-size=200GB",
        "--boot-disk-type=pd-balanced", f"--boot-disk-device-name={card['disk']}",
        f"--network-interface=network={card['network']},subnet={card['subnet']},no-address",
        "--service-account=1061994342941-compute@developer.gserviceaccount.com",
        "--scopes=cloud-platform", "--provisioning-model=STANDARD",
        "--max-run-duration=2h", "--instance-termination-action=STOP",
        "--maintenance-policy=TERMINATE", "--no-restart-on-failure",
        "--reservation-affinity=none", f"--metadata={metadata}",
        f"--metadata-from-file=startup-script={startup}",
        "--labels=project=ganesh-mini,gate=g3,purpose=pilot", "--format=json")
    print(json.dumps({"status": "launched", "instance": card["instance"]}))


def inspect(out: Path) -> dict:
    card = json.loads((out / "execution-card.json").read_text())
    boundary(card)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    state = run(out, "status-" + stamp, "compute", "instances", "describe",
                card["instance"], f"--zone={card['zone']}", "--format=json")
    if state["status"] not in ("TERMINATED", "STOPPING"):
        try:
            run(out, "serial-" + stamp, "compute", "instances",
                "get-serial-port-output", card["instance"], f"--zone={card['zone']}")
        except RuntimeError:
            pass
    print(json.dumps({"status": state["status"], "instance": state["name"]}))
    return state


def watch(out: Path) -> None:
    card = json.loads((out / "execution-card.json").read_text())
    boundary(card)
    if (out / "watcher-started.json").exists():
        raise ValueError("watcher already started")
    save(out / "watcher-started.json", {
        "pid": os.getpid(), "instance": card["instance"],
        "started_at": datetime.now(timezone.utc).isoformat(),
    })
    deadline = time.monotonic() + 8100
    while time.monotonic() < deadline:
        if inspect(out)["status"] == "TERMINATED":
            finalize(out)
            return
        time.sleep(60)
    raise RuntimeError("watch bound reached; preserve disk for recovery")


def finalize(out: Path) -> None:
    card = json.loads((out / "execution-card.json").read_text())
    boundary(card)
    target = out / "terminal-roundtrip"
    subprocess.run(("python3", str(ROOT / "scripts/cuda/gcloud_backup_manifest.py"),
                    "--project", PROJECT, "--prefix", card["prefix"] + "/terminal",
                    "--output", str(out / "terminal-backup-verification.json"),
                    "--download-dir", str(target)), check=True)
    lines = (target / "runtime-files.sha256").read_text().splitlines()
    for line in lines:
        digest, relative = line.split("  ", 1)
        path = (target / relative).resolve()
        if not path.is_relative_to(target.resolve()) or sha(path) != digest:
            raise ValueError("terminal runtime inventory differs")
    if not lines or not (target / "startup-exit-code.txt").exists():
        raise ValueError("terminal backup incomplete")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    state = run(out, "terminal-instance-" + stamp, "compute", "instances",
                "describe", card["instance"], f"--zone={card['zone']}",
                "--format=json")
    if state["status"] != "TERMINATED":
        raise ValueError("producer still running; preserve resources")
    run(out, "delete-instance", "compute", "instances", "delete",
        card["instance"], f"--zone={card['zone']}", "--quiet")
    run(out, "delete-subnet", "compute", "networks", "subnets", "delete",
        card["subnet"], f"--region={region_for(card['zone'])}", "--quiet")
    run(out, "delete-network", "compute", "networks", "delete",
        card["network"], "--quiet")
    for number in (1, 2):
        for kind, key in (("instances", "instance"), ("disks", "disk"),
                          ("networks", "network")):
            if run(out, f"absence-{key}-{number}", "compute", kind, "list",
                   f"--filter=name={card[key]}", "--format=json"):
                raise ValueError("resource remains after teardown")
        if run(out, f"absence-subnet-{number}", "compute", "networks",
               "subnets", "list", f"--filter=name={card['subnet']}",
               "--format=json"):
            raise ValueError("subnet remains after teardown")
    for kind in ("instances", "disks", "addresses"):
        run(out, "project-" + kind + "-after", "compute", kind, "list",
            "--format=json")
    save(out / "finalization.json", {
        "status": "terminal-backup-verified-and-exact-resources-absent-twice",
        "training_exit_code": int((target / "startup-exit-code.txt").read_text()),
        "prefix": card["prefix"],
    })
    run(out, "backup-local-evidence", "storage", "rsync", str(out),
        card["prefix"] + "/local-evidence", "--recursive")
    print(json.dumps({"status": "finalized", "evidence": str(out)}))


def failure_finalize(out: Path) -> None:
    card = json.loads((out / "execution-card.json").read_text())
    boundary(card)
    result = json.loads((out / "create-instance.json").read_text())
    if result["exit_code"] == 0 or "ZONE_RESOURCE_POOL_EXHAUSTED" not in result["stderr"]:
        raise ValueError("not an exact capacity refusal")
    for kind, key in (("instances", "instance"), ("disks", "disk")):
        if run(out, "refusal-absence-" + key, "compute", kind, "list",
               f"--filter=name={card[key]}", "--format=json"):
            raise ValueError("VM or disk exists; preserve before cleanup")
    run(out, "backup-refusal", "storage", "rsync", str(out),
        card["prefix"] + "/launch-refusal", "--recursive")
    subprocess.run(("python3", str(ROOT / "scripts/cuda/gcloud_backup_manifest.py"),
                    "--project", PROJECT,
                    "--prefix", card["prefix"] + "/launch-refusal",
                    "--output", str(out / "refusal-backup-verification.json"),
                    "--download-dir", str(out / "refusal-roundtrip")), check=True)
    run(out, "delete-refusal-subnet", "compute", "networks", "subnets",
        "delete", card["subnet"], f"--region={region_for(card['zone'])}", "--quiet")
    run(out, "delete-refusal-network", "compute", "networks", "delete",
        card["network"], "--quiet")
    for number in (1, 2):
        for kind, key in (("instances", "instance"), ("disks", "disk"),
                          ("networks", "network")):
            if run(out, f"refusal-absence-{key}-{number}", "compute", kind,
                   "list", f"--filter=name={card[key]}", "--format=json"):
                raise ValueError("resource remains after refusal cleanup")
        if run(out, f"refusal-absence-subnet-{number}", "compute", "networks",
               "subnets", "list", f"--filter=name={card['subnet']}",
               "--format=json"):
            raise ValueError("subnet remains after refusal cleanup")
    save(out / "refusal-finalization.json", {
        "status": "capacity-refusal-preserved-resources-absent-twice",
        "gpu_runtime_cost_usd": "0",
    })
    run(out, "backup-refusal-cleanup", "storage", "rsync", str(out),
        card["prefix"] + "/cleanup-evidence", "--recursive",
        "--exclude=refusal-roundtrip/.*")
    print(json.dumps({"status": "refusal-finalized"}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "launch", "inspect",
                                          "watch", "finalize", "failure_finalize"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--zone", default="us-central1-b")
    parser.add_argument("--learning-rate", choices=tuple(LR_PRIOR))
    parser.add_argument("--approved-plan-sha")
    args = parser.parse_args()
    out = args.output.resolve()
    if args.stage == "prepare":
        prepare(out, args.zone, args.learning_rate, args.approved_plan_sha)
    else:
        globals()[args.stage](out)


if __name__ == "__main__":
    main()
