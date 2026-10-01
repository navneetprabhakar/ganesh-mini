#!/usr/bin/env python3
"""Build a non-executable Gate 3 draft or bind measured non-GCloud CUDA evidence."""

from __future__ import annotations

import argparse
import json
import math
import platform
from decimal import Decimal
from pathlib import Path

from scripts.train.preflight_gate3_capability_pilot import ROOT, assess, canonical_sha, file_sha, resolve, sealed
from scripts.train.cuda_host_floor import assess_cuda_host


CARD_SCHEMA = "ganesh-mini-capability-pilot-card/v1"
PROVIDER_SCHEMA = "ganesh-mini-capability-pilot-provider/v1"
GCLOUD_PROVIDER_SCHEMA = "ganesh-mini-capability-pilot-gcloud-provider/v1"
GCLOUD_TEARDOWN_SCHEMA = "ganesh-mini-gate3-gcloud-teardown/v1"
GCLOUD_PROJECT = "executespecv1"
GCLOUD_BUCKET = "ganesh-gate0-model-transfer-1061994342941"
GCLOUD_ZONES = frozenset({"us-east1-b", "us-east1-c", "us-east1-d",
                          "us-central1-a", "us-central1-b", "us-central1-c"})
EVIDENCE_FILES = (
    ("throughput_evidence_path", "throughput_evidence_sha256"),
    ("backup_roundtrip_path", "backup_roundtrip_sha256"),
    ("teardown_plan_path", "teardown_plan_sha256"),
)


def build_draft(config_path: Path, root: Path = ROOT) -> dict:
    static = assess(config_path, root)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    seed_path = resolve(root, config["recipe"]["qualified_seed_recipe_path"])
    recipe = json.loads(seed_path.read_text(encoding="utf-8"))["recipes"]["primary"]
    recipe["lr_selection_budget_seen_tokens_per_candidate"] = 651639
    card = {
        "schema_version": CARD_SCHEMA,
        "status": "prepared-not-executable",
        "reason": "actual_cuda_host_throughput_cost_backup_and_teardown_not_bound",
        "run_id": config["run_id"],
        "inputs": {
            "config_sha256": file_sha(config_path),
            "package_seal_sha256": config["data"]["package_seal_sha256"],
            "prepared_manifest_sha256": config["data"]["prepared_manifest_sha256"],
            "prepared_data_sha256": config["data"]["prepared_train_sha256"],
            "validation_data_sha256": config["data"]["prepared_validation_sha256"],
        },
        "model": config["model"],
        "selected_recipe": recipe,
        "control": config["control"],
        "evaluation": config["evaluation"],
        "runtime": {
            "uv_lock_sha256": file_sha(resolve(root, "uv.lock")),
            "pyproject_sha256": file_sha(resolve(root, "pyproject.toml")),
            "runner_sha256": file_sha(resolve(root, "scripts/train/run_sft.py")),
        },
        "static_preflight": {
            "status": static["status"],
            "records": static["records"],
            "input_tokens": static["input_tokens"],
        },
        "provider_execution": None,
        "failed_checks": [],
    }
    card["card_sha256"] = canonical_sha(card)
    return card


def probe_cuda_host() -> dict:
    if platform.system() != "Linux":
        raise ValueError("pilot execution requires Linux")
    import torch
    if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
        raise ValueError("pilot execution requires exactly one CUDA GPU")
    properties = torch.cuda.get_device_properties(0)
    assess_cuda_host(torch)
    return {"os": "Linux", "gpu_name": properties.name,
            "gpu_vram_bytes": properties.total_memory, "cuda_device_count": 1,
            "bf16_supported": True}


def bind_provider(draft: dict, evidence_path: Path, root: Path = ROOT) -> dict:
    claimed = draft.get("card_sha256")
    body = {key: value for key, value in draft.items() if key != "card_sha256"}
    if claimed != canonical_sha(body) or draft.get("status") != "prepared-not-executable" or draft.get("provider_execution") is not None:
        raise ValueError("provider binding requires an intact non-executable draft")
    provider = sealed(evidence_path, "evidence_sha256")
    gcloud = provider.get("schema_version") == GCLOUD_PROVIDER_SCHEMA
    if gcloud:
        if (provider.get("provider") != "gcloud" or
            provider.get("project") != GCLOUD_PROJECT or
            provider.get("bucket") != GCLOUD_BUCKET or
            provider.get("zone") not in GCLOUD_ZONES or
            provider.get("region") != provider.get("zone", "").rsplit("-", 1)[0] or
            provider.get("maximum_vm_seconds") != 7200):
            raise ValueError("GCloud provider escaped the bounded project, zone, or VM limit")
    elif provider.get("schema_version") != PROVIDER_SCHEMA or provider.get("provider", "").lower() in {"", "gcloud", "google-cloud", "gcp"}:
        raise ValueError("provider must be identified non-GCloud compute")
    if not provider.get("instance_id") or not provider.get("region"):
        raise ValueError("provider instance and region required")
    for path_key, hash_key in EVIDENCE_FILES:
        claimed_hash = provider.get(hash_key)
        if (not isinstance(claimed_hash, str) or len(claimed_hash) != 64 or
            any(character not in "0123456789abcdef" for character in claimed_hash) or
            file_sha(resolve(root, provider[path_key])) != claimed_hash):
            raise ValueError(f"{path_key} is absent or hash-mismatched")
    throughput = sealed(resolve(root, provider["throughput_evidence_path"]), "report_sha256")
    if (throughput.get("schema_version") != "ganesh-mini-capability-pilot-throughput/v1" or
        throughput.get("status") != "passed" or
        throughput.get("instance_id") != provider["instance_id"] or
        throughput.get("model_revision") != draft["model"]["revision"] or
        throughput.get("recipe_sha256") != canonical_sha(draft["selected_recipe"]) or
        throughput.get("prepared_manifest_sha256") != draft["inputs"]["prepared_manifest_sha256"] or
        throughput.get("prepared_train_sha256") != draft["inputs"]["prepared_data_sha256"] or
        throughput.get("measured_input_tokens_per_second") != provider.get("measured_input_tokens_per_second")):
        raise ValueError("throughput evidence does not bind pilot model, recipe, and host")
    backup = sealed(resolve(root, provider["backup_roundtrip_path"]), "report_sha256")
    if (backup.get("status") != "passed" or
        backup.get("durable_backup_uri") != provider.get("durable_backup_uri") or
        backup.get("roundtrip_verified") is not True):
        raise ValueError("durable backup roundtrip evidence differs")
    backup_uri = provider.get("durable_backup_uri", "")
    if gcloud:
        prefix = f"gs://{GCLOUD_BUCKET}/ganesh-mini-1.0/gate3/capability-pilot/"
        if (not backup_uri.startswith(prefix) or
            any(part in {"", ".", ".."} for part in backup_uri[len(prefix):].split("/")) or
            not provider.get("backup_roundtrip_verified")):
            raise ValueError("bounded GCS backup roundtrip required")
        teardown = sealed(resolve(root, provider["teardown_plan_path"]), "report_sha256")
        if (teardown.get("schema_version") != GCLOUD_TEARDOWN_SCHEMA or
            teardown.get("durable_backup_uri") != backup_uri or
            teardown.get("instance_id") != provider["instance_id"] or
            teardown.get("backup_before_delete") is not True or
            teardown.get("double_exact_resource_absence") is not True or
            teardown.get("provider_stop_seconds") != 7200):
            raise ValueError("GCloud teardown contract differs")
    elif (not backup_uri or backup_uri.startswith("gs://") or
          "storage.googleapis.com" in backup_uri or
          not provider.get("backup_roundtrip_verified")):
        raise ValueError("non-GCloud durable backup roundtrip required")
    host = probe_cuda_host()
    if (provider.get("gpu_name") != host["gpu_name"] or
        provider.get("gpu_vram_bytes") != host["gpu_vram_bytes"] or
        provider.get("measured_on_instance_id") != provider["instance_id"]):
        raise ValueError("provider measurement does not bind this CUDA host")
    rate = Decimal(str(provider.get("measured_input_tokens_per_second", 0)))
    hourly = Decimal(str(provider.get("hourly_cost_usd", 0)))
    prior = Decimal(str(provider.get("prior_cost_usd", -1)))
    ceiling = Decimal(str(provider.get("cost_ceiling_usd", 0)))
    if not rate.is_finite() or not hourly.is_finite() or not prior.is_finite() or not ceiling.is_finite() or rate <= 0 or hourly <= 0 or prior < 0 or ceiling <= prior:
        raise ValueError("provider throughput or cost envelope invalid")
    training_seconds = math.ceil(Decimal(651639) / rate * Decimal("1.5"))
    reserve = draft["control"]["finalization_reserve_seconds"]
    if (training_seconds + reserve > draft["control"]["maximum_wall_seconds"] or
        (gcloud and training_seconds + reserve > provider["maximum_vm_seconds"]) or
        prior + hourly * Decimal(training_seconds + reserve) / Decimal(3600) > ceiling):
        raise ValueError("measured throughput does not fit wall and cost ceilings")
    card = dict(body)
    card["status"] = "ready"
    card["reason"] = "actual_non_gcloud_cuda_host_and_bounded_evidence_bound"
    card["provider_execution"] = provider
    card["host"] = host
    card["expected_training_seconds_with_margin"] = training_seconds
    card["card_sha256"] = canonical_sha(card)
    return card


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/train/gate3_capability_pilot_v1.json")
    parser.add_argument("--provider-evidence", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    draft = build_draft(args.config)
    card = bind_provider(draft, args.provider_evidence) if args.provider_evidence else draft
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(card, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": card["status"], "card_sha256": card["card_sha256"]}, sort_keys=True))
    return 0 if card["status"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
