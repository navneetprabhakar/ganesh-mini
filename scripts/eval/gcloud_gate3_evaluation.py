#!/usr/bin/env python3
"""Fail-closed GCloud provider lifecycle for the frozen Gate 3 evaluations.

This module does not run on import.  Preparation is a GCloud operation and
requires the exact approved plan SHA; callers must never overlap attempts.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import tempfile
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

from scripts.train.gcloud_gate3_qualification import (
    BUCKET, IMAGE, PROJECT, ROOT, region_for, run, save, seal, sha, upload,
)
from scripts.train.gcloud_gate3_full_pilot import (
    CEILING, PILOT_ZONES, PLAN_PATH, PLAN_SHA, PRICE_HOURLY,
    _allocated_cost_reserve as training_cost_reserve,
    _prior_allocation_check,
)

SCHEMA = "ganesh-mini-gate3-gcloud-evaluation/v2"
LEGACY_SCHEMA = "ganesh-mini-gate3-gcloud-evaluation/v1"
STAGING_SCHEMA = "ganesh-mini-gate3-evaluation-staging/v1"
WORKSPACE_SEAL = "8ed2f45d87b3b867a59c6eca03be6e9d991bd1070037bd52311ed63a07585edc"
CANARY_SEAL = "0b7483141ba64ba223bc976ed7711ad847bc1056888be0e7bd9d261b85cffa44"
IMAGE_ID = "sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860"
CUDA_FLOOR_SHA = "b45bfdbff03e37d7c2ffb2b6f82b8077a8e19e1408ffb13bef623cf2a3197f68"
MODEL_PREFLIGHT_SHA = "163582e1087362a1cda943937e65ffb804227810e2f49358926a02706b1d78ff"
SUPPORT_RESERVE = Decimal("5.951827904")  # full original allowance, conservatively retained
STAGE_TRANSFER_OPERATIONS = Decimal("0.55")
TWO_HOUR_UPPER = PRICE_HOURLY * 2
TRAINING_PARENT = ROOT / "measurement/gate3/capability-scale-v1/full-pilot-gcloud"
EVAL_PARENT = ROOT / "measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud"
RESUMABLE_ATTEMPT = EVAL_PARENT / "20260930T231842Z"
RESUME_CARD_SHA = "08ed09f4362a6bd293a488c63e47ac2971b224635d08e5afadfcc31bbe7a1b17"
LARGE_OBJECT_TIMEOUT = 1800
VERIFIER_REUSE = {
    "uri": f"gs://{BUCKET}/ganesh-mini-1.0/gate3/20260827T113051Z/input/verifier-images-amd64-v1.tar#1787831835449316",
    "sha256": "1c5c8196cdcc595d755ea506f774dee8a5699e495fe67d7c4441e7a06c21b972",
    "size_bytes": 918639104,
}


def _sealed(path: Path, field: str) -> dict:
    value = json.loads(path.read_text())
    claimed = value.pop(field, None)
    if claimed != seal(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def _stage_inputs(staging: Path, phase: str) -> dict:
    card = _sealed(staging / "evaluation-card.json", "card_sha256")
    if (card.get("schema_version") != STAGING_SCHEMA or card.get("status") != "prepared-only"
        or card.get("decision_tasks_opened") != 0
        or card.get("evaluation_workspace_manifest_sha256") != WORKSPACE_SEAL
        or card.get("canary_manifest_sha256") != CANARY_SEAL
        or len(card.get("canary_task_ids", [])) != 30):
        raise ValueError("prepared evaluation staging scope differs")
    expected = {"canary-1e-5.json", "canary-3e-5.json"}
    if phase == "development":
        selected = card.get("selected_learning_rate")
        if (selected not in ("1e-5", "3e-5") or
            not isinstance(card.get("selection_report_sha256"), str)):
            raise ValueError("development requires a sealed canary selection")
        artifact = card.get("selection_report_artifact", {})
        selection_path = staging / "selection-report.json"
        if (artifact.get("path") != "selection-report.json" or
            not selection_path.is_file() or sha(selection_path) != artifact.get("sha256")):
            raise ValueError("development selection artifact differs")
        selection = _sealed(selection_path, "report_sha256")
        if (selection.get("report_sha256") != card["selection_report_sha256"] or
            selection.get("status") != "selected" or
            selection.get("selected_learning_rate") != selected or
            selection.get("gate3_quality_passed") is not False or
            selection.get("decision_tasks_opened") != 0):
            raise ValueError("development selection report differs")
        if not any(
            (attempt / "canary-selection.json").is_file()
            and sha(attempt / "canary-selection.json") == sha(selection_path)
            and (attempt / "finalization.json").is_file()
            and json.loads((attempt / "finalization.json").read_text()).get("evaluation_exit_code") == 0
            and (attempt / "terminal-backup-verification.json").is_file()
            and json.loads((attempt / "terminal-backup-verification.json").read_text()).get("status") == "verified"
            for attempt in EVAL_PARENT.iterdir() if attempt.is_dir()
        ):
            raise ValueError("development selection lacks finalized canary evidence")
        expected = {f"development-{selected}.json"}
    elif phase != "canary" or card.get("selected_learning_rate") is not None:
        raise ValueError("canary staging must precede selection")
    for name in expected:
        if name not in card.get("configs", {}) or sha(staging / name) != card["configs"][name]["sha256"]:
            raise ValueError(f"evaluation config differs: {name}")
        config = json.loads((staging / name).read_text())
        if (config.get("classification") != "private_candidate_development" or
            config.get("allowed_surface") != "development" or
            config.get("expected_task_count") != (30 if phase == "canary" else 180) or
            config.get("task_globs") != ["eval/private/development/tranche1/*.task.json" if phase == "canary" else "eval/private/development/**/*.task.json"] or
            config.get("serving") != {"modality": "text-only", "enable_thinking": False, "context_length": 8192, "add_generation_prompt": True} or
            config.get("generation") != {"do_sample": False, "max_new_tokens": 4096, "use_cache": True} or
            config.get("execution", {}).get("required_device") != "cuda" or
            config.get("adapter", {}).get("dir") != f"candidate-inputs/{name.removeprefix(phase + '-').removesuffix('.json')}/adapter-final"):
            raise ValueError("evaluation config escaped frozen phase")
    bundle = staging / "candidate-inputs.tar.gz"
    if sha(bundle) != card["candidate_input_bundle"]["sha256"]:
        raise ValueError("candidate bundle differs")
    workspace_manifest = ROOT / "measurement/gate3/capability-scale-v1/full-pilot-eval/evaluation-workspace-v1.manifest.json"
    workspace = _sealed(workspace_manifest, "manifest_sha256")
    workspace_archive = ROOT / workspace["archive"]["path"]
    if (workspace["manifest_sha256"] != WORKSPACE_SEAL or
        sha(workspace_archive) != card["evaluation_workspace_archive_sha256"]):
        raise ValueError("evaluation workspace differs")
    return card


def _prior_cost(parent: Path, phase: str, *, ignore_unsealed: Path | None = None) -> Decimal:
    # Training controller validates every prior allocation/refusal and both
    # completed epochs; a repeat training allocation is deliberately refused.
    try:
        _prior_allocation_check(TRAINING_PARENT, "3e-5", PLAN_SHA)
    except ValueError as error:
        if "allocated candidate already exists" not in str(error):
            raise
    training = Decimal("0")
    successful = set()
    for path in TRAINING_PARENT.glob("*/execution-card.json"):
        training_card = _sealed(path, "execution_sha256")
        attempt = path.parent
        create = attempt / "create-instance.json"
        if not create.is_file():
            raise ValueError("unresolved training preparation")
        if json.loads(create.read_text())["exit_code"] == 0:
            final = json.loads((attempt / "finalization.json").read_text())
            if final.get("status") != "terminal-backup-verified-and-exact-resources-absent-twice":
                raise ValueError("unfinalized training allocation")
            training += training_cost_reserve(attempt)
            if final.get("training_exit_code") == 0:
                successful.add(training_card["learning_rate"])
        elif not (attempt / "refusal-finalization.json").is_file():
            raise ValueError("unfinalized training refusal")
    if successful != {"1e-5", "3e-5"}:
        raise ValueError("both training candidates must be sealed")
    evaluation = Decimal("0")
    canary_complete = False
    for attempt in parent.iterdir() if parent.is_dir() else ():
        if attempt.is_dir() and attempt != ignore_unsealed and not (attempt / "execution-card.json").is_file():
            raise ValueError("unresolved evaluation staging directory")
    for path in parent.glob("*/execution-card.json"):
        if path.parent == ignore_unsealed:
            continue
        prior = _sealed(path, "execution_sha256")
        if prior.get("schema_version") not in (SCHEMA, LEGACY_SCHEMA):
            raise ValueError("unexpected evaluation attempt card")
        if prior.get("schema_version") == LEGACY_SCHEMA and prior.get("execution_sha256") != RESUME_CARD_SHA:
            raise ValueError("unrecognized legacy evaluation attempt")
        create = path.parent / "create-instance.json"
        if not create.is_file():
            raise ValueError("unresolved evaluation preparation")
        result = json.loads(create.read_text())
        if result["exit_code"] == 0:
            final = json.loads((path.parent / "finalization.json").read_text())
            if final.get("status") != "terminal-backup-verified-and-exact-resources-absent-twice":
                raise ValueError("unfinalized evaluation allocation")
            evaluation += training_cost_reserve(path.parent)
            if prior["phase"] == "canary" and final.get("evaluation_exit_code") == 0:
                canary_complete = True
            if prior["phase"] == phase and final.get("evaluation_exit_code") == 0:
                raise ValueError("evaluation stage already completed")
        elif not (path.parent / "refusal-finalization.json").is_file():
            raise ValueError("unfinalized evaluation refusal")
    if phase == "development" and not canary_complete:
        raise ValueError("canary stage must complete before development")
    # Deliberately reserve the *entire* original support allowance again,
    # despite per-allocation reserves already including transfer/operations.
    prior = training + evaluation
    if prior + TWO_HOUR_UPPER + STAGE_TRANSFER_OPERATIONS + SUPPORT_RESERVE > CEILING:
        raise ValueError("$15 absolute incremental ceiling would be exceeded")
    return prior


def boundary(card: dict) -> None:
    body = dict(card); claimed = body.pop("execution_sha256", None)
    if claimed != seal(body):
        raise ValueError("evaluation execution card seal differs")
    if (card.get("schema_version") not in (SCHEMA, LEGACY_SCHEMA) or card.get("plan_sha256") != PLAN_SHA or
        card.get("project") != PROJECT or card.get("bucket") != BUCKET or
        card.get("zone") not in PILOT_ZONES or card.get("phase") not in ("canary", "development") or
        card.get("machine_type") != "g2-standard-8" or card.get("maximum_vm_seconds") != 7200 or
        card.get("absolute_incremental_ceiling_usd") != str(CEILING) or
        card.get("hourly_cost_usd") != str(PRICE_HOURLY) or
        card.get("decision_tasks_opened") != 0 or
        card.get("evaluation_workspace_manifest_sha256") != WORKSPACE_SEAL or
        card.get("canary_manifest_sha256") != CANARY_SEAL or
        card.get("cuda_image_id") != IMAGE_ID or
        card.get("inputs", {}).get("cuda_host_floor", {}).get("sha256") != CUDA_FLOOR_SHA or
        not card.get("prefix", "").startswith(f"gs://{BUCKET}/ganesh-mini-1.0/gate3/capability-pilot/evaluation/")):
        raise ValueError("evaluation boundary differs")
    if card["schema_version"] == SCHEMA:
        if card.get("inputs", {}).get("model_preflight_module", {}).get("sha256") != MODEL_PREFLIGHT_SHA:
            raise ValueError("model preflight dependency differs")
    elif card.get("execution_sha256") != RESUME_CARD_SHA:
        raise ValueError("unrecognized legacy evaluation card")
    if (Decimal(card["prior_cost_reserve_usd"]) + TWO_HOUR_UPPER +
        STAGE_TRANSFER_OPERATIONS + SUPPORT_RESERVE > CEILING):
        raise ValueError("evaluation card exceeds $15 ceiling")


def _resume_boundary(out: Path, phase: str, zone: str, resume: bool) -> None:
    if not out.exists():
        if resume:
            raise ValueError("resume target does not exist")
        return
    if not resume or out != RESUMABLE_ATTEMPT or phase != "canary" or zone != "us-central1-b":
        raise ValueError("only the exact interrupted canary attempt can resume")
    if not out.is_dir() or any((out / name).exists() for name in
                               ("launch-inputs.json", "create-instance.json", "watcher-started.json")):
        raise ValueError("interrupted attempt already reached launch or VM boundary")
    if (out / "execution-card.json").is_file():
        _sealed(out / "execution-card.json", "execution_sha256")
    expected = {"evaluation_workspace", "evaluation_manifest", "candidate_inputs", "staging_card"}
    observed = {path.name.removeprefix("metadata-").removesuffix(".json")
                for path in out.glob("metadata-*.json")}
    if observed != expected:
        raise ValueError("interrupted attempt object evidence differs")
    for name in expected:
        for prefix in ("upload", "metadata", "roundtrip"):
            record = out / f"{prefix}-{name}.json"
            if not record.is_file() or json.loads(record.read_text()).get("exit_code") != 0:
                raise ValueError("interrupted attempt lacks a completed small-object roundtrip")


def _call(out: Path, label: str, args: tuple[str, ...], *, timeout: int) -> subprocess.CompletedProcess[str]:
    index = 1
    while (out / f"resume-{label}-{index}.json").exists():
        index += 1
    name = out / f"resume-{label}-{index}.json"
    argv = ["gcloud", *args]
    if not any(arg.startswith("--project=") for arg in args):
        argv.append(f"--project={PROJECT}")
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as error:
        save(name, {"command": argv, "timeout_seconds": timeout,
                    "status": "timed-out", "stdout": str(error.stdout or ""),
                    "stderr": str(error.stderr or "")})
        raise
    save(name, {"command": argv, "timeout_seconds": timeout,
                "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    return result


def _describe_object(out: Path, uri: str, label: str) -> dict | None:
    result = _call(out, f"describe-{label}",
                   ("storage", "objects", "describe", uri, "--format=json"), timeout=120)
    if result.returncode:
        if "not found" in result.stderr.lower() or "404" in result.stderr:
            return None
        raise RuntimeError(f"object inspection failed: {result.stderr}")
    value = json.loads(result.stdout)
    if not isinstance(value, dict) or not str(value.get("generation", "")).isdigit():
        raise ValueError("object metadata is incomplete")
    return value


def _upload_verified(out: Path, prefix: str, label: str, path: Path,
                     *, reuse: dict | None = None) -> dict:
    """Reuse only a generation re-downloaded and hashed in this invocation."""
    uri = reuse["uri"].rsplit("#", 1)[0] if reuse else f"{prefix}/input/{path.name}"
    if not path.is_file():
        raise ValueError(f"missing input: {path}")
    expected_sha = sha(path)
    if reuse and (expected_sha != reuse["sha256"] or path.stat().st_size != reuse["size_bytes"]):
        raise ValueError("historical verifier binding differs from local bytes")
    metadata = _describe_object(out, uri, label)
    if reuse and (metadata is None or str(metadata["generation"]) != reuse["uri"].rsplit("#", 1)[1]):
        raise ValueError("historical verifier generation is unavailable or changed")
    old = out / f"metadata-{label}.json"
    if old.is_file():
        previous = json.loads(old.read_text())
        if previous.get("exit_code") != 0:
            raise ValueError("previous object metadata failed")
        previous_value = json.loads(previous["stdout"])
        if metadata is None or str(previous_value["generation"]) != str(metadata["generation"]):
            raise ValueError("previously bound object generation changed")
    if metadata is None:
        result = _call(out, f"upload-{label}",
                       ("storage", "cp", str(path), uri, "--if-generation-match=0"),
                       timeout=LARGE_OBJECT_TIMEOUT)
        if result.returncode:
            raise RuntimeError(f"input upload failed: {result.stderr}")
        metadata = _describe_object(out, uri, label)
    if metadata is None or int(metadata.get("size", -1)) != path.stat().st_size:
        raise ValueError("input object size differs")
    pinned = f"{uri}#{metadata['generation']}"
    index = 1
    while (out / "resume-roundtrip" / f"{label}-{index}-{path.name}").exists():
        index += 1
    target = out / "resume-roundtrip" / f"{label}-{index}-{path.name}"
    target.parent.mkdir(exist_ok=True)
    result = _call(out, f"download-{label}",
                   ("storage", "cp", pinned, str(target)), timeout=LARGE_OBJECT_TIMEOUT)
    if result.returncode or not target.is_file() or target.stat().st_size != path.stat().st_size or sha(target) != expected_sha:
        raise ValueError("independent object generation/size/hash roundtrip failed")
    save(out / f"resume-verified-{label}-{index}.json",
         {"status": "verified", "uri": pinned, "sha256": expected_sha,
          "size_bytes": path.stat().st_size, "roundtrip_path": str(target)})
    return {"uri": pinned, "sha256": expected_sha, "size_bytes": path.stat().st_size}


def prepare(out: Path, staging: Path, phase: str, zone: str, approved_plan_sha: str,
            *, resume: bool = False) -> None:
    if approved_plan_sha != PLAN_SHA or sha(PLAN_PATH) != PLAN_SHA:
        raise ValueError("exact approved GCloud plan SHA required")
    if zone not in PILOT_ZONES:
        raise ValueError("zone escaped frozen set")
    _resume_boundary(out, phase, zone, resume)
    if not (ROOT / "scripts/eval/gcloud_gate3_evaluation_startup.sh").is_file():
        raise ValueError("evaluation startup script is missing")
    datetime.strptime(out.name, "%Y%m%dT%H%M%SZ")
    staged = _stage_inputs(staging, phase)
    prior = _prior_cost(out.parent, phase, ignore_unsealed=out if resume else None)
    if not resume:
        out.mkdir(parents=True)
    qualified = json.loads((ROOT / "measurement/gate3/capability-scale-v1/gcloud-qualification/20260930T131906Z/execution-card.json").read_text())
    prefix = f"gs://{BUCKET}/ganesh-mini-1.0/gate3/capability-pilot/evaluation/{out.name}/{phase}"
    inputs = {key: qualified["inputs"][key] for key in ("model_archive", "cuda_image_archive", "docker_bundle")}
    for name, row in inputs.items():
        meta = run(out, f"resume-inspect-{name}-{len(list(out.glob('resume-inspect-' + name + '-*.json'))) + 1}" if resume else f"inspect-{name}",
                   "storage", "objects", "describe", row["uri"], "--format=json")
        if str(meta["generation"]) != row["uri"].rsplit("#", 1)[1] or int(meta["size"]) != row["size_bytes"]:
            raise ValueError("pinned upstream object differs")
    quota = run(out, f"resume-region-{len(list(out.glob('resume-region-*.json'))) + 1}" if resume else "region",
                "compute", "regions", "describe", region_for(zone), "--format=json")
    quotas = {entry["metric"]: entry for entry in quota["quotas"]}
    if quotas["NVIDIA_L4_GPUS"]["limit"] - quotas["NVIDIA_L4_GPUS"]["usage"] < 1:
        raise ValueError("no L4 quota")
    boot = run(out, f"resume-boot-image-{len(list(out.glob('resume-boot-image-*.json'))) + 1}" if resume else "boot-image", "compute", "images", "describe", IMAGE,
               "--project=deeplearning-platform-release", "--format=json")
    if boot.get("status") != "READY" or boot.get("id") != "5785010291456121629":
        raise ValueError("pinned boot image differs")
    workspace = ROOT / "measurement/gate3/capability-scale-v1/full-pilot-eval/evaluation-workspace-v1.tar.gz"
    verifier = ROOT / "artifacts/eval/verifier-images/amd64-v1/verifier-images-amd64-v1.tar"
    verifier_manifest = ROOT / "artifacts/eval/verifier-images/amd64-v1/manifest.json"
    historical_verifier_binding = ROOT / "measurement/gate3/gcloud/20260827T113051Z/input-metadata/verifier_archive.binding.json"
    if json.loads(historical_verifier_binding.read_text()) != VERIFIER_REUSE:
        raise ValueError("historical verifier object binding differs")
    materializer = ROOT / "scripts/train/inspect_model_archive.py"
    model_preflight = ROOT / "scripts/train/preflight_gate3_capability_pilot.py"
    cuda_floor = ROOT / "scripts/train/cuda_host_floor.py"
    if sha(model_preflight) != MODEL_PREFLIGHT_SHA:
        raise ValueError("model preflight dependency differs")
    if sha(cuda_floor) != CUDA_FLOOR_SHA:
        raise ValueError("CUDA host-floor implementation differs")
    for label, path in (("evaluation_workspace", workspace), ("evaluation_manifest", workspace.with_suffix("").with_suffix(".manifest.json")),
                        ("candidate_inputs", staging / "candidate-inputs.tar.gz"),
                        ("staging_card", staging / "evaluation-card.json"),
                        ("verifier_images", verifier), ("verifier_manifest", verifier_manifest),
                        ("model_materializer", materializer), ("model_preflight_module", model_preflight),
                        ("cuda_host_floor", cuda_floor)):
        if not path.is_file():
            raise ValueError(f"missing evaluation input: {path}")
        inputs[label] = _upload_verified(out, prefix, label, path,
                                         reuse=VERIFIER_REUSE if label == "verifier_images" else None)
    config_names = ("canary-1e-5.json", "canary-3e-5.json") if phase == "canary" else (f"development-{staged['selected_learning_rate']}.json",)
    for name in config_names:
        inputs[name] = _upload_verified(out, prefix, name.removesuffix(".json"), staging / name)
    stem = f"ganesh-g3-eval-{out.name.lower()}"
    card = {"schema_version": SCHEMA, "status": "authorized-evaluation-only",
            "plan_sha256": PLAN_SHA, "project": PROJECT, "bucket": BUCKET,
            "zone": zone, "instance": stem, "disk": stem, "network": stem + "-net", "subnet": stem + "-subnet",
            "prefix": prefix, "phase": phase, "staging_card_sha256": staged["card_sha256"],
            "evaluation_workspace_manifest_sha256": WORKSPACE_SEAL,
            "canary_manifest_sha256": CANARY_SEAL,
            "selected_learning_rate": staged["selected_learning_rate"],
            "selection_report_sha256": staged["selection_report_sha256"],
            "maximum_vm_seconds": 7200, "machine_type": "g2-standard-8",
            "boot_image": boot["selfLink"], "boot_image_id": boot["id"], "cuda_image_id": IMAGE_ID,
            "decision_tasks_opened": 0, "absolute_incremental_ceiling_usd": str(CEILING),
            "hourly_cost_usd": str(PRICE_HOURLY), "prior_cost_reserve_usd": str(prior),
            "provider_two_hour_upper_usd": str(TWO_HOUR_UPPER),
            "stage_transfer_operations_reserve_usd": str(STAGE_TRANSFER_OPERATIONS),
            "support_reserve_usd": str(SUPPORT_RESERVE), "inputs": inputs,
            "teardown_requires": "terminal GCS inventory independently downloaded twice before deletion"}
    card["execution_sha256"] = seal(card)
    boundary(card)
    if (out / "execution-card.json").is_file():
        if _sealed(out / "execution-card.json", "execution_sha256") != card:
            raise ValueError("resumed execution card differs from verified inputs")
    else:
        save(out / "execution-card.json", card)
    startup = ROOT / "scripts/eval/gcloud_gate3_evaluation_startup.sh"
    launch_inputs = {"card": _upload_verified(out, prefix, "card", out / "execution-card.json"),
                     "startup": _upload_verified(out, prefix, "startup", startup)}
    save(out / "launch-inputs.json", launch_inputs)


def _create_instance(out: Path, card: dict, launch_inputs: dict, startup: Path) -> None:
    if sha(startup) != launch_inputs["startup"]["sha256"]:
        raise ValueError("startup snapshot differs")
    metadata = ",".join((f"ganesh-project={PROJECT}", f"ganesh-prefix={card['prefix']}",
                         f"ganesh-card-uri={launch_inputs['card']['uri']}",
                         f"ganesh-card-sha={launch_inputs['card']['sha256']}"))
    run(out, "create-instance", "compute", "instances", "create", card["instance"],
        f"--zone={card['zone']}", "--machine-type=g2-standard-8", f"--image={card['boot_image']}",
        "--boot-disk-size=200GB", "--boot-disk-type=pd-balanced", f"--boot-disk-device-name={card['disk']}",
        f"--network-interface=network={card['network']},subnet={card['subnet']},no-address",
        "--service-account=1061994342941-compute@developer.gserviceaccount.com", "--scopes=cloud-platform",
        "--provisioning-model=STANDARD", "--max-run-duration=2h", "--instance-termination-action=STOP",
        "--maintenance-policy=TERMINATE", "--no-restart-on-failure", "--reservation-affinity=none",
        f"--metadata={metadata}", f"--metadata-from-file=startup-script={startup}",
        "--labels=project=ganesh-mini,gate=g3,purpose=evaluation", "--format=json")


def launch(out: Path) -> None:
    card = _sealed(out / "execution-card.json", "execution_sha256"); boundary(card)
    if not (out / "launch-inputs.json").is_file() or (out / "create-instance.json").exists():
        raise ValueError("attempt not staged or already launched")
    if card["schema_version"] != SCHEMA:
        raise ValueError("new allocation requires current evaluation card schema")
    launch_inputs = json.loads((out / "launch-inputs.json").read_text())
    if launch_inputs["card"]["sha256"] != sha(out / "execution-card.json"):
        raise ValueError("uploaded card binding differs")
    _verified_snapshot(out, "card", launch_inputs["card"])
    startup = _verified_snapshot(out, "startup", launch_inputs["startup"])
    # A second project VM (even with a different name) would breach the
    # one-allocation rule. Addresses/disks are also disallowed at entry.
    for kind in ("instances", "disks", "addresses"):
        if run(out, "project-" + kind + "-before", "compute", kind, "list", "--format=json"):
            raise ValueError(f"project has active {kind}; refuse overlap")
    networks = run(out, "project-networks-before", "compute", "networks", "list", "--format=json")
    if any(row.get("name") != "default" for row in networks):
        raise ValueError("project has a non-default network; refuse overlap")
    for kind, key in (("instances", "instance"), ("disks", "disk"), ("networks", "network")):
        if run(out, "absence-" + key, "compute", kind, "list", f"--filter=name={card[key]}", "--format=json"):
            raise ValueError("exact resource already exists")
    if run(out, "absence-subnet", "compute", "networks", "subnets", "list", f"--filter=name={card['subnet']}", "--format=json"):
        raise ValueError("exact subnet already exists")
    run(out, "create-network", "compute", "networks", "create", card["network"], "--subnet-mode=custom")
    run(out, "create-subnet", "compute", "networks", "subnets", "create", card["subnet"],
        f"--region={region_for(card['zone'])}", f"--network={card['network']}", "--range=10.244.2.0/28",
        "--enable-private-ip-google-access")
    _create_instance(out, card, launch_inputs, startup)


def _fresh_label(out: Path, stem: str) -> str:
    index = 1
    while (out / f"{stem}-{index}.json").exists():
        index += 1
    return f"{stem}-{index}"


def _verified_snapshot(out: Path, kind: str, binding: dict) -> Path:
    records = sorted(out.glob(f"resume-verified-{kind}-*.json"))
    if not records:
        raise ValueError(f"no independently verified {kind} snapshot")
    valid = []
    for record in records:
        row = json.loads(record.read_text())
        path = Path(row.get("roundtrip_path", ""))
        if (row.get("status") == "verified" and row.get("uri") == binding.get("uri") and
            row.get("sha256") == binding.get("sha256") and
            row.get("size_bytes") == binding.get("size_bytes") and
            path.is_file() and path.is_relative_to(out / "resume-roundtrip") and
            path.stat().st_size == binding["size_bytes"] and sha(path) == binding["sha256"]):
            valid.append(path)
    if len(valid) != len(records):
        raise ValueError(f"{kind} roundtrip evidence differs")
    return valid[-1]


def resume_launch(out: Path) -> None:
    """Complete only the exact interrupted launch, never recreate its network."""
    if out != RESUMABLE_ATTEMPT:
        raise ValueError("resume_launch is restricted to the exact interrupted attempt")
    card = _sealed(out / "execution-card.json", "execution_sha256"); boundary(card)
    stem = f"ganesh-g3-eval-{out.name.lower()}"
    if (card["execution_sha256"] != RESUME_CARD_SHA or card["phase"] != "canary" or
        card["zone"] != "us-central1-b" or card["instance"] != stem or
        card["disk"] != stem or card["network"] != stem + "-net" or
        card["subnet"] != stem + "-subnet"):
        raise ValueError("exact interrupted launch card differs")
    if str(_prior_cost(out.parent, "canary", ignore_unsealed=out)) != card["prior_cost_reserve_usd"]:
        raise ValueError("prior cost reserve changed before resumed allocation")
    if (out / "create-instance.json").exists() or (out / "watcher-started.json").exists():
        raise ValueError("instance create or watcher already attempted")
    launch_inputs = json.loads((out / "launch-inputs.json").read_text())
    if launch_inputs["card"]["sha256"] != sha(out / "execution-card.json"):
        raise ValueError("uploaded card binding differs")
    _verified_snapshot(out, "card", launch_inputs["card"])
    startup = _verified_snapshot(out, "startup", launch_inputs["startup"])
    for name, command in (("create-network", ["compute", "networks", "create", card["network"], "--subnet-mode=custom"]),
                          ("create-subnet", ["compute", "networks", "subnets", "create", card["subnet"],
                                             f"--region={region_for(card['zone'])}", f"--network={card['network']}",
                                             "--range=10.244.2.0/28", "--enable-private-ip-google-access"])):
        row = json.loads((out / f"{name}.json").read_text())
        if row.get("exit_code") != 0 or row.get("command") != command:
            raise ValueError(f"{name} prior success/command differs")
    for kind in ("instances", "disks", "addresses"):
        if run(out, _fresh_label(out, "resume-project-" + kind), "compute", kind, "list", "--format=json"):
            raise ValueError(f"project has {kind}; refuse resumed allocation")
    network = run(out, _fresh_label(out, "resume-network-state"), "compute", "networks",
                  "describe", card["network"], "--format=json")
    subnet = run(out, _fresh_label(out, "resume-subnet-state"), "compute", "networks", "subnets",
                 "describe", card["subnet"], f"--region={region_for(card['zone'])}", "--format=json")
    if (network.get("name") != card["network"] or network.get("autoCreateSubnetworks") is not False or
        network.get("selfLink", "").rsplit("/", 1)[-1] != card["network"] or
        subnet.get("name") != card["subnet"] or subnet.get("network") != network.get("selfLink") or
        subnet.get("ipCidrRange") != "10.244.2.0/28" or
        subnet.get("privateIpGoogleAccess") is not True or
        subnet.get("region", "").rsplit("/", 1)[-1] != region_for(card["zone"])):
        raise ValueError("existing exact network/subnet differs")
    for kind, key in (("instances", "instance"), ("disks", "disk")):
        if run(out, _fresh_label(out, "resume-absence-" + key), "compute", kind, "list",
               f"--filter=name={card[key]}", "--format=json"):
            raise ValueError("exact VM or disk already exists")
    _create_instance(out, card, launch_inputs, startup)


def inspect(out: Path) -> dict:
    card = _sealed(out / "execution-card.json", "execution_sha256"); boundary(card)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    state = run(out, "status-" + stamp, "compute", "instances", "describe", card["instance"],
                f"--zone={card['zone']}", "--format=json")
    if state["status"] not in ("TERMINATED", "STOPPING"):
        try:
            run(out, "serial-" + stamp, "compute", "instances", "get-serial-port-output",
                card["instance"], f"--zone={card['zone']}")
        except RuntimeError:
            pass
    return state


def watch(out: Path) -> None:
    card = _sealed(out / "execution-card.json", "execution_sha256"); boundary(card)
    save(out / "watcher-started.json", {"pid": os.getpid(), "instance": card["instance"],
                                         "started_at": datetime.now(timezone.utc).isoformat()})
    deadline = time.monotonic() + 8100
    while time.monotonic() < deadline:
        if inspect(out)["status"] == "TERMINATED":
            finalize(out); return
        time.sleep(60)
    raise RuntimeError("watch bound reached; preserve disk for recovery")


def finalize(out: Path) -> None:
    card = _sealed(out / "execution-card.json", "execution_sha256"); boundary(card)
    target = out / "terminal-roundtrip"
    subprocess.run(("python3", str(ROOT / "scripts/cuda/gcloud_backup_manifest.py"),
                    "--project", PROJECT, "--prefix", card["prefix"] + "/terminal",
                    "--output", str(out / "terminal-backup-verification.json"),
                    "--download-dir", str(target)), check=True)
    verification = json.loads((out / "terminal-backup-verification.json").read_text())
    if verification.get("status") != "verified":
        raise ValueError("terminal backup not verified")
    lines = (target / "runtime-files.sha256").read_text().splitlines()
    for line in lines:
        digest, relative = line.split("  ", 1)
        path = (target / relative).resolve()
        if not path.is_relative_to(target.resolve()) or sha(path) != digest:
            raise ValueError("terminal runtime inventory differs")
    if not lines or not (target / "startup-exit-code.txt").is_file():
        raise ValueError("terminal backup incomplete")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    state = run(out, "terminal-instance-" + stamp, "compute", "instances", "describe",
                card["instance"], f"--zone={card['zone']}", "--format=json")
    if state["status"] != "TERMINATED":
        raise ValueError("producer still running; preserve resources")
    run(out, "delete-instance", "compute", "instances", "delete", card["instance"], f"--zone={card['zone']}", "--quiet")
    run(out, "delete-subnet", "compute", "networks", "subnets", "delete", card["subnet"],
        f"--region={region_for(card['zone'])}", "--quiet")
    run(out, "delete-network", "compute", "networks", "delete", card["network"], "--quiet")
    for number in (1, 2):
        for kind, key in (("instances", "instance"), ("disks", "disk"), ("networks", "network")):
            if run(out, f"absence-{key}-{number}", "compute", kind, "list",
                   f"--filter=name={card[key]}", "--format=json"):
                raise ValueError("resource remains after teardown")
        if run(out, f"absence-subnet-{number}", "compute", "networks", "subnets", "list",
               f"--filter=name={card['subnet']}", "--format=json"):
            raise ValueError("subnet remains after teardown")
    for kind in ("instances", "disks", "addresses"):
        run(out, "project-" + kind + "-after", "compute", kind, "list", "--format=json")
    save(out / "finalization.json", {"status": "terminal-backup-verified-and-exact-resources-absent-twice",
                                     "evaluation_exit_code": int((target / "startup-exit-code.txt").read_text()),
                                     "prefix": card["prefix"]})
    complete_local_mirror(out)


MIRROR_EXCLUDES = ("roundtrip", "resume-roundtrip", "terminal-roundtrip",
                   "refusal-roundtrip", "local-mirror-roundtrip")


def _mirror_inventory(out: Path) -> dict[str, tuple[str, int]]:
    inventory = {}
    for path in out.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(out)
        if (relative.parts[0] in MIRROR_EXCLUDES or
            relative.name.startswith(("resume-local-mirror-", "local-control-mirror-"))):
            continue
        if path.is_symlink():
            raise ValueError("local mirror contains a symlink")
        inventory[str(relative)] = (sha(path), path.stat().st_size)
    return inventory


def complete_local_mirror(out: Path) -> None:
    """Mirror bounded control evidence after verified terminal backup/teardown.

    This is resumable for the exact failed v1 canary attempt. Original input
    roundtrips and terminal downloads are omitted because their immutable GCS
    inputs and terminal prefix have already been independently verified.
    """
    card = _sealed(out / "execution-card.json", "execution_sha256"); boundary(card)
    final = json.loads((out / "finalization.json").read_text())
    terminal = json.loads((out / "terminal-backup-verification.json").read_text())
    if (final.get("status") != "terminal-backup-verified-and-exact-resources-absent-twice" or
        final.get("prefix") != card["prefix"] or terminal.get("status") != "verified" or
        terminal.get("prefix") != card["prefix"] + "/terminal"):
        raise ValueError("terminal backup/teardown must be sealed before local mirror")
    if card["schema_version"] == LEGACY_SCHEMA and out != RESUMABLE_ATTEMPT:
        raise ValueError("legacy recovery only permitted for exact failed attempt")
    for number in (1, 2):
        for kind, key in (("instances", "instance"), ("disks", "disk"),
                          ("networks", "network"), ("subnets", "subnet")):
            name = f"absence-{key}-{number}"
            record = json.loads((out / f"{name}.json").read_text())
            if record.get("exit_code") != 0 or json.loads(record.get("stdout", "null")) != []:
                raise ValueError("recorded exact resource absence differs")
            if run(out, _fresh_label(out, "mirror-absence-" + key), "compute", *("networks", "subnets", "list") if kind == "subnets" else (kind, "list"),
                   f"--filter=name={card[key]}", "--format=json"):
                raise ValueError("exact resource reappeared before local mirror")
    inventory = _mirror_inventory(out)
    if not inventory:
        raise ValueError("empty local control mirror")
    # gcloud's repeated --exclude flags do not accumulate here: only the last
    # one took effect in the v1 mirror. Preserve that partial prefix and use
    # one combined relative-path regex on a clean v2 prefix.
    prefix = card["prefix"] + "/local-evidence-controls-v2"
    exclude_regex = "|".join(f"{name}/.*" for name in MIRROR_EXCLUDES)
    exclude_regex += "|resume-local-mirror-.*|local-control-mirror-.*"
    result = _call(out, "local-mirror-rsync", ("storage", "rsync", str(out), prefix,
                                               "--recursive", f"--exclude={exclude_regex}"), timeout=900)
    if result.returncode:
        raise RuntimeError("local control mirror rsync failed")
    with tempfile.TemporaryDirectory(prefix="ganesh-g3-local-mirror-") as temporary:
        manifest_path = Path(temporary) / "verified.json"
        subprocess.run(("python3", str(ROOT / "scripts/cuda/gcloud_backup_manifest.py"),
                        "--project", PROJECT, "--prefix", prefix,
                        "--output", str(manifest_path), "--download-dir",
                        str(Path(temporary) / "download")), check=True, timeout=900)
        manifest = json.loads(manifest_path.read_text())
        if manifest.get("status") != "verified" or manifest.get("prefix") != prefix:
            raise ValueError("local control mirror verification failed")
        observed = {}
        prefix_path = prefix.split("/", 3)[3].rstrip("/") + "/"
        for row in manifest["objects"]:
            relative = row["object_uri"].split("/", 3)[3].removeprefix(prefix_path)
            observed[relative] = (row["downloaded_sha256"], row["size"])
        if observed != inventory:
            raise ValueError("remote control mirror differs from local inventory")
        save(out / "local-control-mirror-verification.json", manifest)


def failure_finalize(out: Path) -> None:
    card = _sealed(out / "execution-card.json", "execution_sha256"); boundary(card)
    result = json.loads((out / "create-instance.json").read_text())
    if result["exit_code"] == 0 or "ZONE_RESOURCE_POOL_EXHAUSTED" not in result["stderr"]:
        raise ValueError("not an exact capacity refusal")
    for kind, key in (("instances", "instance"), ("disks", "disk")):
        if run(out, "refusal-absence-" + key, "compute", kind, "list",
               f"--filter=name={card[key]}", "--format=json"):
            raise ValueError("VM or disk exists; preserve before cleanup")
    # Preserve the bounded control files; the large input roundtrips were
    # already independently verified at their pinned GCS input generations.
    exclude_regex = "|".join(f"{name}/.*" for name in MIRROR_EXCLUDES)
    exclude_regex += "|resume-local-mirror-.*|local-control-mirror-.*"
    refusal_prefix = card["prefix"] + "/launch-refusal-controls-v2"
    run(out, "backup-refusal", "storage", "rsync", str(out), refusal_prefix,
        "--recursive", f"--exclude={exclude_regex}")
    subprocess.run(("python3", str(ROOT / "scripts/cuda/gcloud_backup_manifest.py"),
                    "--project", PROJECT, "--prefix", refusal_prefix,
                    "--output", str(out / "refusal-backup-verification.json"),
                    "--download-dir", str(out / "refusal-roundtrip")), check=True, timeout=900)
    backup = json.loads((out / "refusal-backup-verification.json").read_text())
    if backup.get("status") != "verified" or backup.get("prefix") != refusal_prefix:
        raise ValueError("refusal control backup not independently verified")
    run(out, "delete-refusal-subnet", "compute", "networks", "subnets", "delete",
        card["subnet"], f"--region={region_for(card['zone'])}", "--quiet")
    run(out, "delete-refusal-network", "compute", "networks", "delete", card["network"], "--quiet")
    for number in (1, 2):
        for kind, key in (("instances", "instance"), ("disks", "disk"), ("networks", "network")):
            if run(out, f"refusal-absence-{key}-{number}", "compute", kind, "list",
                   f"--filter=name={card[key]}", "--format=json"):
                raise ValueError("resource remains after refusal cleanup")
        if run(out, f"refusal-absence-subnet-{number}", "compute", "networks", "subnets", "list",
               f"--filter=name={card['subnet']}", "--format=json"):
            raise ValueError("subnet remains after refusal cleanup")
    save(out / "refusal-finalization.json", {"status": "capacity-refusal-preserved-resources-absent-twice"})
    run(out, "backup-refusal-cleanup", "storage", "rsync", str(out), card["prefix"] + "/cleanup-evidence-controls-v2",
        "--recursive", f"--exclude={exclude_regex}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "launch", "resume_launch", "inspect", "watch", "finalize", "complete_local_mirror", "failure_finalize"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--staging", type=Path)
    parser.add_argument("--phase", choices=("canary", "development"))
    parser.add_argument("--zone", default="us-central1-b")
    parser.add_argument("--approved-plan-sha")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.stage == "prepare":
        if args.staging is None or args.phase is None:
            parser.error("prepare requires --staging and --phase")
        prepare(args.output.resolve(), args.staging.resolve(), args.phase, args.zone,
                args.approved_plan_sha, resume=args.resume)
    else:
        globals()[args.stage](args.output.resolve())


if __name__ == "__main__":
    main()
