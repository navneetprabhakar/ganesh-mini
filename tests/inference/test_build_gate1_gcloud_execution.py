from __future__ import annotations

import json
import subprocess
from unittest.mock import patch

import pytest

from scripts.inference.build_gate1_gcloud_execution import build, canonical_sha256
from scripts.inference.build_gate1_gcloud_preparation import ROOT


APPROVAL = (
    "Approved: one staged Gate 3 G2 L4 Flex-start campaign in us-east1-b "
    "on g2-standard-12, maximum provisioning wait 2 hours, maximum runtime 3 hours, "
    "and USD 3.50 incremental cost."
)


def generation(uri: str, sha256: str, size: int) -> dict:
    return {"uri": uri, "sha256": sha256, "size_bytes": size}


def bindings() -> dict:
    preparation = json.loads((ROOT / "measurement/gate3/gcloud/preparation.json").read_text())
    local = preparation["local_inputs"]
    value = {
        "schema_version": "ganesh-mini-gate3-gcloud-bindings/v3",
        "status": "verified-generation-pinned",
        "run_id": "20260827T000000Z",
        "preparation_sha256": preparation["preparation_sha256"],
        "preflight": {
            "project": "executespecv1",
            "region": "us-east1",
            "zone": "us-east1-b",
            "machine_type": "g2-standard-12",
            "gcs_bucket": "ganesh-gate0-model-transfer-1061994342941",
            "gcs_prefix": "ganesh-mini-1.0/gate3/20260827T000000Z",
            "boot_image": "projects/dl/global/images/pinned",
            "service_account": "1061994342941-compute@developer.gserviceaccount.com",
            "price_passed": True,
            "quota_passed": True,
            "machine_type_available": True,
            "exact_resources_absent": True,
            "bucket_round_trip_passed": True,
            "service_account_bucket_access_passed": True,
        },
        "cost": {
            "conservative_hourly_usd": "1.000416348",
            "support_reserve_usd": "0.35",
            "absolute_cost_ceiling_usd": "3.50",
        },
        "resources": {"instance": "vm", "disk": "disk", "network": "net", "subnet": "subnet"},
        "inputs": {
            "workspace_archive": generation("gs://b/w#1", local["workspace_archive"]["sha256"], local["workspace_archive"]["size_bytes"]),
            "workspace_manifest": generation("gs://b/wm#2", local["workspace_manifest"]["sha256"], local["workspace_manifest"]["size_bytes"]),
            "training_workspace_archive": generation("gs://b/tw#7", local["training_workspace_archive"]["sha256"], local["training_workspace_archive"]["size_bytes"]),
            "training_workspace_manifest": generation("gs://b/twm#8", local["training_workspace_manifest"]["sha256"], local["training_workspace_manifest"]["size_bytes"]),
            "completed_candidate_archive": generation("gs://b/cc#15", local["completed_candidate_archive"]["sha256"], local["completed_candidate_archive"]["size_bytes"]),
            "completed_candidate_manifest": generation("gs://b/ccm#16", local["completed_candidate_manifest"]["sha256"], local["completed_candidate_manifest"]["size_bytes"]),
            "gate0_report": generation("gs://b/g0#9", local["gate0_report"]["sha256"], local["gate0_report"]["size_bytes"]),
            "gate1_report": generation("gs://b/g1#11", local["gate1_report"]["sha256"], local["gate1_report"]["size_bytes"]),
            "gate2_report": generation("gs://b/g2#10", local["gate2_report"]["sha256"], local["gate2_report"]["size_bytes"]),
            "verifier_archive": generation("gs://b/v#3", local["verifier_archive"]["sha256"], local["verifier_archive"]["size_bytes"]),
            "verifier_manifest": generation("gs://b/vm#4", local["verifier_manifest"]["sha256"], local["verifier_manifest"]["size_bytes"]),
            "model_archive": generation("gs://b/model#12", local["model_archive"]["sha256"], local["model_archive"]["size_bytes"]),
            "cuda_image_archive": generation("gs://b/image#13", local["cuda_image_archive"]["sha256"], local["cuda_image_archive"]["size_bytes"]),
            "docker_bundle": generation("gs://b/docker#14", local["docker_bundle"]["sha256"], local["docker_bundle"]["size_bytes"]),
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
    assert card["schema_version"] == "ganesh-mini-gate3-gcloud-execution/v3"
    assert card["evaluation"]["expected_task_count"] == 180
    assert card["execution"]["maximum_run_seconds"] == 10800
    assert card["execution"]["automatic_restart"] is False
    assert card["execution"]["service_account"] == "1061994342941-compute@developer.gserviceaccount.com"
    assert card["cost"]["conservative_upper_usd"] == "3.351249044"
    assert card["gate_range"] == [3, 3]
    assert card["training"]["lr_candidates"] == [0.00001, 0.00003]
    assert card["training"]["imported_lr_candidates"] == [0.00001]
    assert card["training"]["trained_lr_candidates"] == [0.00003]
    assert card["training"]["unique_train_records"] == 1399
    assert card["training"]["main_seen_tokens"] == 0
    assert all(row["uri"].rsplit("#", 1)[-1].isdigit() for row in card["inputs"].values())


def test_builds_card_for_an_explicitly_approved_fallback_zone() -> None:
    value = bindings()
    value["preflight"]["zone"] = "us-east1-c"
    value["bindings_sha256"] = canonical_sha256({k: v for k, v in value.items() if k != "bindings_sha256"})
    approval = APPROVAL.replace("us-east1-b", "us-east1-c")
    card = build(value, approval, head(), require_clean=False)
    assert card["execution"]["zone"] == "us-east1-c"


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
    value["cost"]["conservative_hourly_usd"] = "1.20"
    value["bindings_sha256"] = canonical_sha256({k: v for k, v in value.items() if k != "bindings_sha256"})
    with pytest.raises(ValueError, match="cost preflight"):
        build(value, APPROVAL, head(), require_clean=False)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("service_account_bucket_access_passed", False, "preflight did not pass"),
        ("service_account", "unexpected@example.invalid", "service_account mismatch"),
    ],
)
def test_rejects_unverified_vm_service_account_bucket_access(field, value, message) -> None:
    candidate = bindings()
    candidate["preflight"][field] = value
    candidate["bindings_sha256"] = canonical_sha256(
        {key: row for key, row in candidate.items() if key != "bindings_sha256"}
    )
    with pytest.raises(ValueError, match=message):
        build(candidate, APPROVAL, head(), require_clean=False)


def test_rejects_tracked_worktree_drift_when_sealing() -> None:
    with patch("scripts.inference.build_gate1_gcloud_execution.tracked_worktree_clean", return_value=False):
        with pytest.raises(ValueError, match="tracked worktree must be clean"):
            build(bindings(), APPROVAL, head())
