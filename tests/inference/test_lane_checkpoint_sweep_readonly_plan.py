import json
from pathlib import Path

import pytest

from scripts.inference.build_lane_checkpoint_sweep_readonly_plan import REUSED_INPUTS, build
from scripts.inference.build_lane_checkpoint_sweep_upload_plan import canonical_sha256


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "measurement/gate4/lane-stratified-probe-checkpoint-sweep-20260910"


def test_readonly_plan_binds_receipt_inputs_and_forbids_mutation() -> None:
    plan = build(BASE, "20260910T150000Z")

    assert plan["status"] == "pending-explicit-gcloud-readonly-approval"
    assert plan["approved_upload_receipt_sha256"] == "6da07f1fcfa4296828e2a8cf406873d1f347d9436fa852f389c09fad087170b1"
    assert len(plan["generation_pinned_inputs"]) == 12
    assert set(REUSED_INPUTS) <= set(plan["generation_pinned_inputs"])
    assert all(row["uri"].rsplit("#", 1)[-1].isdigit() for row in plan["generation_pinned_inputs"].values())
    assert all(len(row["sha256"]) == 64 for row in plan["generation_pinned_inputs"].values())
    assert any("create, start, stop" in operation for operation in plan["forbidden_operations"])
    assert plan["inspection_plan_sha256"] == canonical_sha256({
        key: value for key, value in plan.items() if key != "inspection_plan_sha256"
    })


def test_repository_readonly_plan_matches_builder() -> None:
    plan = json.loads((BASE / "gcloud-readonly-inspection-plan.json").read_text())

    assert plan == build(BASE, plan["planned_attempt_id"])


def test_readonly_plan_rejects_invalid_attempt_id() -> None:
    with pytest.raises(ValueError, match="invalid attempt"):
        build(BASE, "tomorrow")
