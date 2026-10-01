from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.data.run_capability_scale_teacher import (
    PROMPT_CONTRACT_V2, load_queue, run_one, scale_architect_prompt,
    select_activated_reserves, select_remaining_first_pass, select_rows,
)


ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "measurement/gate3/capability-scale-v1/source-queue.jsonl"
MANIFEST = ROOT / "measurement/gate3/capability-scale-v1/source-queue-manifest.json"
ACTIVATION = ROOT / "measurement/gate3/capability-scale-v1/canary-v1/reserve-activation"


def test_load_and_select_exact_canary_matrix() -> None:
    rows = load_queue(QUEUE, MANIFEST)
    selected = select_rows(rows, "canary")
    assert len(rows) == 711
    assert len(selected) == 12
    assert {(row["lane"], row["task_type"]) for row in selected} == {
        (lane, task_type)
        for lane in ("go", "java", "javascript", "typescript", "python", "rust")
        for task_type in ("generation", "repair")
    }
    assert all(row["cohort"] == "first_pass" for row in selected)


def test_v2_prompt_binds_defect_to_primary_not_cross_cutting() -> None:
    row = select_rows(load_queue(QUEUE, MANIFEST), "canary")[0]
    prompt = scale_architect_prompt(row, PROMPT_CONTRACT_V2)
    assert row["primary_capability_definition"] in prompt
    assert "defect must specifically exercise the assigned primary capability" in prompt
    assert "known-bad implementation must already\nsatisfy the scheduled cross-cutting dimension" in prompt


def test_selects_only_terminally_activated_reserves() -> None:
    selected = select_activated_reserves(
        load_queue(QUEUE, MANIFEST), ACTIVATION / "activated-reserves.jsonl",
        ACTIVATION / "activation-report.json",
    )
    assert len(selected) == 7
    assert all(row["cohort"] == "reserve" for row in selected)
    assert len({row["cell_id"] for row in selected}) == 7


def test_selects_exact_534_unconsumed_first_pass_rows() -> None:
    selected = select_remaining_first_pass(
        load_queue(QUEUE, MANIFEST),
        ROOT / "measurement/gate3/capability-scale-v1/canary-v1/teacher/teacher-report.json",
    )
    assert len(selected) == 534
    assert all(row["cohort"] == "first_pass" for row in selected)
    assert len({row["id"] for row in selected}) == 534


def test_run_one_seals_candidate_without_authored_tests(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    row = select_rows(load_queue(QUEUE, MANIFEST), "canary")[0]
    calls = []

    def fake_invoke(*args, **kwargs):
        calls.append((args, kwargs))
        return {
            "items": [{
                "id": row["id"],
                "problem": "Implement package solution with func Sum(values []int) int.",
                "reference_code": "package solution\nfunc Sum(values []int) int { n:=0; for _,v:=range values { n+=v }; return n }",
                "known_bad_code": "package solution\nfunc Sum(values []int) int { return 0 }",
                "known_bad_label": "returns zero instead of aggregating values",
            }]
        }, {"command": ["codex"], "exit_code": 0}

    monkeypatch.setattr("scripts.data.run_capability_scale_teacher.invoke_codex", fake_invoke)
    config = json.loads((ROOT / "configs/data/expansion_teacher.json").read_text())
    artifact = run_one(row, config, "codex", "codex-cli 0.144.4", tmp_path)
    assert artifact["status"] == "generated"
    assert artifact["candidate"]["test_origin"] == "pending-v9-canonical-independent-author"
    assert all(item["role"] == "support" for item in artifact["candidate"]["verification_task"]["files"])
    assert artifact["candidate"]["teacher_evidence"]["evaluation_artifacts_read"] == 0
    assert len(calls) == 1

    resumed = run_one(row, config, "codex", "codex-cli 0.144.4", tmp_path)
    assert resumed == artifact
    assert len(calls) == 1


def test_loader_rejects_unsealed_queue_copy(tmp_path: Path) -> None:
    changed = tmp_path / "queue.jsonl"
    rows = QUEUE.read_text().splitlines()
    value = json.loads(rows[0]); value["stimulus"] += " changed"
    rows[0] = json.dumps(value, sort_keys=True, separators=(",", ":"))
    changed.write_text("\n".join(rows) + "\n")
    with pytest.raises(ValueError, match="sealed contract"):
        load_queue(changed, MANIFEST)


def test_run_one_seals_structurally_invalid_response(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    row = select_rows(load_queue(QUEUE, MANIFEST), "canary")[0]

    def fake_invoke(*args, **kwargs):
        return {"items": []}, {"command": ["codex"], "exit_code": 0}

    monkeypatch.setattr("scripts.data.run_capability_scale_teacher.invoke_codex", fake_invoke)
    config = json.loads((ROOT / "configs/data/expansion_teacher.json").read_text())
    artifact = run_one(row, config, "codex", "codex-cli 0.144.4", tmp_path)
    assert artifact["status"] == "response-rejected"
    assert artifact["run_evidence_sha256"]
    assert "item count differs" in artifact["reason"]

    resumed = run_one(row, config, "codex", "codex-cli 0.144.4", tmp_path)
    assert resumed == artifact
