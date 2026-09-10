#!/usr/bin/env python3
"""Seal the read-only prerequisite inspection for the v3 checkpoint sweep."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from scripts.inference.build_lane_checkpoint_sweep_upload_plan import canonical_sha256
from scripts.inference.build_lane_checkpoint_sweep_upload_receipt import load_sealed


REUSED_INPUTS = {
    "model_archive": {
        "uri": "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/expansion-pilot-v1/input/model-rehydrated.tar.gz#1788910413265608",
        "sha256": "846221797a5b57db5d7184680df4e74641a61504f687f86b81d85a471bb8c930",
        "size_bytes": 3618248781,
    },
    "cuda_image_archive": {
        "uri": "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/expansion-pilot-v1/input/cuda-image-rehydrated.docker.tar.zst#1788913987238416",
        "sha256": "40a69cdc316c215ce98b42627f98a62bcb35d563cec9615b9c6e5fe4550ca799",
        "size_bytes": 8236332782,
    },
    "docker_bundle": {
        "uri": "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/expansion-pilot-v1/input/docker-bundle-rehydrated.tar.gz#1788911568845494",
        "sha256": "2de5e2625e77f38d895d32bb69592970d017dcdc6494ca807421eb8ff0065245",
        "size_bytes": 73522586,
    },
    "verifier_archive": {
        "uri": "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/expansion-pilot-v1/input/verifier-images-amd64-v1.tar#1788912580629555",
        "sha256": "1c5c8196cdcc595d755ea506f774dee8a5699e495fe67d7c4441e7a06c21b972",
        "size_bytes": 918639104,
    },
    "verifier_manifest": {
        "uri": "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/training/expansion-pilot-v1/input/verifier-images-amd64-v1.manifest.json#1788912199982420",
        "sha256": "c4d0d44afb97ba02ae9bb52a6d4a79af68ce1fd1aea3583765085170acb4ff75",
        "size_bytes": 17481,
    },
    "metadata_wrapper": {
        "uri": "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/input/bcea1f8/gcloud_checkpoint_sweep_metadata_wrapper.sh#1788943280777084",
        "sha256": "03b3128656bd3d7a787fdbaa5a81057895556420611b9bca2388ace20207ca52",
        "size_bytes": 2159,
    },
}


def build(base: Path, attempt_id: str) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9]{8}T[0-9]{6}Z", attempt_id):
        raise ValueError("invalid attempt ID")
    receipt = load_sealed(base / "upload/upload-receipt.json", "receipt_sha256")
    if receipt.get("status") != "complete" or receipt.get("compute_or_infrastructure_actions") != []:
        raise ValueError("completed upload receipt is required")
    uploaded = {
        row["generation_uri"].rsplit("/", 1)[-1].split("#", 1)[0]: {
            "uri": row["generation_uri"],
            "sha256": row["sha256"],
            "size_bytes": row["size_bytes"],
        }
        for row in receipt["objects"]
    }
    if set(uploaded) != {
        "workspace.tar.gz", "workspace.manifest.json", "startup.sh", "startup.manifest.json",
        "recovery.tar.gz", "recovery.manifest.json",
    }:
        raise ValueError("upload receipt has the wrong object set")
    inputs = {**REUSED_INPUTS, **{f"uploaded_{name}": row for name, row in uploaded.items()}}
    compact_attempt = attempt_id.lower().replace(":", "")
    plan: dict[str, Any] = {
        "schema_version": "ganesh-mini-lane-checkpoint-sweep-gcloud-readonly-plan/v1",
        "status": "pending-explicit-gcloud-readonly-approval",
        "purpose": "verify exact inputs and provider prerequisites before proposing diagnostic-only checkpoint evaluation",
        "project": "executespecv1",
        "region": "us-east1",
        "zone": "us-east1-c",
        "planned_attempt_id": attempt_id,
        "approved_upload_receipt_sha256": receipt["receipt_sha256"],
        "planned_resource_names": {
            "instance": f"ganesh-mini-g4-v3-sweep-{compact_attempt}",
            "disk": f"ganesh-mini-g4-v3-sweep-{compact_attempt}",
            "subnet": f"ganesh-mini-g4-v3-sweep-{compact_attempt}-subnet",
            "network": f"ganesh-mini-g4-v3-sweep-{compact_attempt}-net",
        },
        "generation_pinned_inputs": inputs,
        "allowed_read_only_checks": [
            "describe us-east1-c status, g2-standard-8, NVIDIA L4 availability, and quota usage",
            "verify the four exact planned resource names are absent",
            "read the intended VM service-account IAM roles relevant to GCS access",
            "verify all twelve generation-pinned input objects remain readable with matching name, size, and hashes established by their immutable evidence",
            "obtain current public/provider price evidence for Standard g2-standard-8 and pd-balanced storage",
        ],
        "forbidden_operations": [
            "create, start, stop, update, delete, or attach any compute, disk, network, subnet, address, router, firewall, accelerator, or service-account resource",
            "upload, overwrite, delete, restore, or mutate any GCS object",
            "bind or upload an executable evaluation card",
            "train, evaluate, select, promote, merge, quantize, publish, or open decision tasks",
        ],
        "output": "one sealed read-only report used only to construct a separately approved execution proposal",
    }
    plan["inspection_plan_sha256"] = canonical_sha256(plan)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = build(args.base.resolve(), args.attempt_id)
    args.output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"inspection_plan_sha256": plan["inspection_plan_sha256"], "status": plan["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
