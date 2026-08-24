from __future__ import annotations

import json
import subprocess
from unittest.mock import patch

import pytest

from scripts.inference.build_gate1_gcloud_execution import build, canonical_sha256
from scripts.inference.build_gate1_gcloud_preparation import ROOT


APPROVAL = (
    "Approved: one Gate 1 exact-Qwen baseline G2 L4 Flex-start request in us-east1-b "
    "on g2-standard-12, maximum provisioning wait 2 hours, maximum runtime 4 hours, "
    "and USD 4.40 incremental cost."
)


def generation(uri: str, sha256: str, size: int) -> dict:
    return {"uri": uri, "sha256": sha256, "size_bytes": size}


def bindings() -> dict:
    preparation = json.loads((ROOT / "measurement/gate1/gcloud/preparation.json").read_text())
    gate0 = json.loads((ROOT / "measurement/cuda/gcloud/20260824T180957Z/gpu_run_plan.json").read_text())
    local = preparation["local_inputs"]
    value = {
        "schema_version": "ganesh-mini-gate1-gcloud-bindings/v1",
        "status": "verified-generation-pinned",
        "run_id": "gate1-qwen-base-east1-v1",
        "preparation_sha256": preparation["preparation_sha256"],
        "preflight": {
            "project": "executespecv1",
            "region": "us-east1",
            "zone": "us-east1-b",
            "machine_type": "g2-standard-12",
            "gcs_bucket": "ganesh-gate0-model-transfer-1061994342941",
            "gcs_prefix": "ganesh-mini-1.0/gate1/test",
            "boot_image": "projects/dl/global/images/pinned",
            "price_passed": True,
            "quota_passed": True,
            "machine_type_available": True,
            "exact_resources_absent": True,
            "bucket_round_trip_passed": True,
        },
        "cost": {
            "conservative_hourly_usd": "1.000416348",
            "support_reserve_usd": "0.35",
            "absolute_cost_ceiling_usd": "4.40",
        },
        "resources": {"instance": "vm", "disk": "disk", "network": "net", "subnet": "subnet"},
        "inputs": {
            "workspace_archive": generation("gs://b/w#1", local["workspace_archive"]["sha256"], local["workspace_archive"]["size_bytes"]),
            "workspace_manifest": generation("gs://b/wm#2", local["workspace_manifest"]["sha256"], local["workspace_manifest"]["size_bytes"]),
            "verifier_archive": generation("gs://b/v#3", local["verifier_archive"]["sha256"], local["verifier_archive"]["size_bytes"]),
            "verifier_manifest": generation("gs://b/vm#4", local["verifier_manifest"]["sha256"], local["verifier_manifest"]["size_bytes"]),
            "model_archive": generation(gate0["input"]["model_uri"], gate0["input"]["model_sha256"], gate0["input"]["model_bytes"]),
            "cuda_image_archive": generation(gate0["input"]["image_uri"], gate0["input"]["image_sha256"], gate0["input"]["image_bytes"]),
            "docker_bundle": generation(gate0["input"]["docker_bundle_uri"], gate0["input"]["docker_bundle_sha256"], gate0["input"]["docker_bundle_bytes"]),
        },
        "launch": {
            "controller": generation("gs://b/c#5", local["controller"]["sha256"], local["controller"]["size_bytes"]),
            "metadata_wrapper": generation("gs://b/m#6", local["metadata_wrapper"]["sha256"], local["metadata_wrapper"]["size_bytes"]),
        },
    }
    value["bindings_sha256"] = canonical_sha256(value)
    return value


def head() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def test_builds_exact_authorized_generation_pinned_card() -> None:
    card = build(bindings(), APPROVAL, head(), require_clean=False)
    claimed = card.pop("execution_sha256")
    assert claimed == canonical_sha256(card)
    assert card["status"] == "authorized-executable"
    assert card["evaluation"]["expected_task_count"] == 180
    assert card["execution"]["maximum_run_seconds"] == 14400
    assert card["cost"]["conservative_upper_usd"] == "4.351665392"
    assert all(row["uri"].rsplit("#", 1)[-1].isdigit() for row in card["inputs"].values())


def test_rejects_approval_that_does_not_bind_the_exact_card() -> None:
    with pytest.raises(ValueError, match="approval text"):
        build(bindings(), "approved", head(), require_clean=False)


def test_rejects_unpinned_or_drifted_input() -> None:
    value = bindings()
    value["inputs"]["workspace_archive"]["uri"] = "gs://b/w"
    value["bindings_sha256"] = canonical_sha256({k: v for k, v in value.items() if k != "bindings_sha256"})
    with pytest.raises(ValueError, match="generation-pinned"):
        build(value, APPROVAL, head(), require_clean=False)


def test_rejects_invalid_bindings_seal() -> None:
    value = bindings()
    value["run_id"] = "drifted"
    with pytest.raises(ValueError, match="bindings seal"):
        build(value, APPROVAL, head(), require_clean=False)


def test_rejects_cost_above_approval() -> None:
    value = bindings()
    value["cost"]["conservative_hourly_usd"] = "1.10"
    value["bindings_sha256"] = canonical_sha256({k: v for k, v in value.items() if k != "bindings_sha256"})
    with pytest.raises(ValueError, match="cost preflight"):
        build(value, APPROVAL, head(), require_clean=False)


def test_rejects_tracked_worktree_drift_when_sealing() -> None:
    with patch("scripts.inference.build_gate1_gcloud_execution.tracked_worktree_clean", return_value=False):
        with pytest.raises(ValueError, match="tracked worktree must be clean"):
            build(bindings(), APPROVAL, head())
