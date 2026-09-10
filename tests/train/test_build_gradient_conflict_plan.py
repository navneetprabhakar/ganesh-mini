import json

import pytest

from scripts.train.build_gradient_conflict_plan import build, canonical_sha256


def trajectory(tmp_path, *, stable_fail: int = 21):
    value = {
        "schema_version": "ganesh-mini-lane-stratified-checkpoint-trajectory/v1",
        "status": "complete-do-not-promote",
        "trajectory_summary": {"stable_fail_tasks": stable_fail, "status_changing_tasks": 8},
        "conclusion": {"any_checkpoint_passed_continuation_rule": False},
    }
    value["report_sha256"] = canonical_sha256(value)
    path = tmp_path / "trajectory.json"
    path.write_text(json.dumps(value))
    return path


def test_plan_is_non_executable_and_conditionally_gates_pcgrad(tmp_path, monkeypatch) -> None:
    path = trajectory(tmp_path)
    monkeypatch.setattr("scripts.train.build_gradient_conflict_plan.ROOT", tmp_path)
    plan = build(path)
    assert plan["status"] == "local-design-only-not-executable"
    assert plan["stage_1_gradient_audit"]["optimizer_steps"] == 0
    assert plan["stage_2_conditional_probe"]["maximum_seen_tokens"] == 466614
    assert plan["gcloud_authority"] == "none" and plan["promotion_authority"] == "none"
    claimed = plan.pop("plan_sha256")
    assert claimed == canonical_sha256(plan)


def test_plan_rejects_a_different_failure_shape(tmp_path, monkeypatch) -> None:
    path = trajectory(tmp_path, stable_fail=20)
    monkeypatch.setattr("scripts.train.build_gradient_conflict_plan.ROOT", tmp_path)
    with pytest.raises(ValueError, match="does not support"):
        build(path)
