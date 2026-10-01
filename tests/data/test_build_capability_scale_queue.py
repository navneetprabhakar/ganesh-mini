from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from scripts.data.build_capability_scale_queue import build, source_key


ROOT = Path(__file__).resolve().parents[2]


def inputs() -> argparse.Namespace:
    v3 = ROOT / "measurement/gate2/capability-stratified-v3-repair-delta/primary-teacher"
    v4 = ROOT / "measurement/gate2/capability-stratified-v4-repair-delta"
    return argparse.Namespace(
        plan=ROOT / "docs/plans/GATE3_CAPABILITY_SCALE_CONSTRUCTION_PLAN_20260917.md",
        entry_manifest=ROOT / "measurement/gate3/training-entry-v1/manifest.json",
        lineage=ROOT / "measurement/gate3/training-entry-v1/qualified-lineage.jsonl",
        source_queue=ROOT / "datasets/cache/expansion-v1/source-queue-v1.jsonl",
        prior_corpus=ROOT / "datasets/cache/expansion-v1/pilot-sealed-3225/train.jsonl",
        v2_envelopes=ROOT / "measurement/gate2/capability-stratified-v2/admission-campaign-final-v2/admission-envelopes.jsonl",
        v3_candidates=[v3 / lane / "candidates.jsonl" for lane in ("go", "java", "javascript", "typescript", "python", "rust")],
        v4_candidates=[v4 / version / lane / "candidates.jsonl" for version in ("teacher-v1", "teacher-v2", "teacher-v3") for lane in ("go", "java", "javascript", "typescript", "python", "rust")],
        v5_candidates=ROOT / "measurement/gate2/capability-stratified-v5-interface-replay/cohort-v1/execution-v1/candidates.jsonl",
        v5_assignments=ROOT / "measurement/gate2/capability-stratified-v5-interface-replay/cohort-v1/execution-v1/assignments.jsonl",
        output=ROOT / "unused-scale-queue.jsonl",
        manifest=ROOT / "unused-scale-manifest.json",
    )


def test_builds_exact_source_unique_546_plus_165_queue() -> None:
    rows, manifest = build(inputs())
    assert len(rows) == manifest["records"] == 711
    assert manifest["first_pass_records"] == 546
    assert manifest["reserve_records"] == 165
    assert manifest["first_pass_by_task_type"] == {"generation": 246, "repair": 300}
    assert len({source_key(row) for row in rows}) == 711
    assert manifest["historical_draft_accounting"]["total"] == 489
    assert manifest["historical_draft_accounting"]["remaining_under_1200"] == 711
    assert all(row["evaluation_artifacts_read"] == 0 for row in rows)


def test_queue_has_exact_cell_deficits_and_bounded_reserves() -> None:
    rows, manifest = build(inputs())
    entry = __import__("json").loads(inputs().entry_manifest.read_text())
    first = {}
    reserve = {}
    for row in rows:
        target = first if row["cohort"] == "first_pass" else reserve
        target[row["cell_id"]] = target.get(row["cell_id"], 0) + 1
    assert first == entry["cell_top_up"]
    assert set(reserve.values()) == {1, 2}
    assert sum(value == 2 for value in reserve.values()) == 45
    assert manifest["reserve_allocation"]["maximum_per_cell"] == 2


def test_rejects_plan_drift(tmp_path: Path) -> None:
    values = inputs()
    changed = tmp_path / "plan.md"
    changed.write_text(values.plan.read_text() + "\nchanged\n")
    values.plan = changed
    with pytest.raises(ValueError, match="frozen input hash differs"):
        build(values)
