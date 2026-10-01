from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.freeze_training_entry_lineage import build, lineage_row


ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "measurement/gate2/capability-stratified-v2/admission-campaign-final-v2"
V9 = ROOT / "measurement/gate2/capability-stratified-v9-literal-key-guard/final-v1"


def args() -> argparse.Namespace:
    return argparse.Namespace(
        plan=ROOT / "docs/plans/GATE3_TRAINING_ENTRY_ASSESSMENT_PLAN_20260917.md",
        v2_admitted=V2 / "admitted.jsonl",
        v2_admission=V2 / "admission-report.json",
        v2_qualification=V2 / "qualification-summary.json",
        v9_candidates=V9 / "complete-candidates.jsonl",
        v9_qualification=V9 / "qualification-summary-v9.json",
        v9_separation=V9 / "global-separation-report.json",
        assignments=(
            ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"
            / "cohort-v1/execution-v1/assignments.jsonl"
        ),
        v5_cohort_manifest=(
            ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"
            / "cohort-v1/execution-v1/manifest.json"
        ),
        v7_terminal=(
            ROOT / "measurement/gate2/capability-stratified-v7-order-insensitive-canonical-test-replay"
            / "final-v1/terminal-artifacts.jsonl"
        ),
        v7_qualification=(
            ROOT / "measurement/gate2/capability-stratified-v7-order-insensitive-canonical-test-replay"
            / "qualification-summary-v7.json"
        ),
        lineage_output=ROOT / "unused-lineage.jsonl",
        manifest_output=ROOT / "unused-manifest.json",
    )


def test_build_freezes_complete_inventory_and_balanced_120_cell_anchors() -> None:
    rows, manifest = build(args())
    assert manifest["status"] == "passed"
    assert manifest["records"] == 174
    assert manifest["cells"] == manifest["cell_anchors"] == 120
    assert manifest["unique_record_ids"] == 174
    assert manifest["unique_source_identities"] == 174
    assert manifest["generation_records"] == 114
    assert manifest["repair_records"] == 60
    assert len({row["cell_id"] for row in rows}) == 120
    assert len([row for row in rows if row["cell_anchor"]]) == 120
    assert [row["ordinal"] for row in rows] == list(range(174))
    assert all(row["evaluation_artifacts_read"] == 0 for row in rows)
    assert sum(manifest["cell_top_up"].values()) == 546
    assert manifest["construction_target"] == {
        "qualified_seed_records": 174,
        "additional_generation_records": 246,
        "additional_repair_records": 300,
        "additional_new_records": 546,
        "broad_replay_records": 180,
        "final_pilot_records": 900,
    }


def test_generation_selection_is_lexicographically_first_per_cell() -> None:
    rows, _ = build(args())
    admitted = [json.loads(line) for line in args().v2_admitted.read_text().splitlines() if line]
    by_cell: dict[str, list[str]] = {}
    for value in admitted:
        if value["record"]["task_type"] == "generation":
            by_cell.setdefault(value["qualification"]["cell_id"], []).append(value["record"]["id"])
    selected = {
        row["cell_id"]: row["record_id"]
        for row in rows if row["origin"] == "v2-generation" and row["cell_anchor"]
    }
    assert selected == {cell: min(ids) for cell, ids in by_cell.items()}


def test_lineage_row_rejects_incomplete_rights() -> None:
    candidate = json.loads(args().v9_candidates.read_text().splitlines()[0])
    assignment = json.loads(args().assignments.read_text().splitlines()[0])
    candidate = deepcopy(candidate)
    candidate["rights"]["model_training"] = False
    with pytest.raises(ValueError, match="incomplete training or publication rights"):
        lineage_row(
            ordinal=0, origin="v9-repair", record=candidate,
            cell_id=assignment["cell_id"], capability=assignment["primary_capability"],
            dimension=assignment["assigned_cross_cutting_dimension"], qualification={}, anchor=True,
        )


def test_build_rejects_plan_hash_drift(tmp_path: Path) -> None:
    changed = tmp_path / "plan.md"
    changed.write_text(args().plan.read_text() + "\nchanged\n")
    values = args()
    values.plan = changed
    with pytest.raises(ValueError, match="frozen file hash differs"):
        build(values)
