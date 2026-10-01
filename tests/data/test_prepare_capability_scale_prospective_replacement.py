from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts.data.build_capability_scale_queue import source_key
from scripts.data.prepare_capability_scale_prospective_replacement import (
    CELL,
    NEW_ID,
    pick_source,
    prepare,
)


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "docs/plans/GATE3_DUPLICATE_RESERVE_PROSPECTIVE_REPLACEMENT_20260924.md"
QUEUE = ROOT / "measurement/gate3/capability-scale-v1/source-queue.jsonl"
MANIFEST = ROOT / "measurement/gate3/capability-scale-v1/source-queue-manifest.json"


def test_prebinds_one_disjoint_source_and_counts_draft() -> None:
    rows, report = prepare(PLAN, QUEUE, MANIFEST)
    assert len(rows) == 1
    assert rows[0]["id"] == NEW_ID
    assert rows[0]["cell_id"] == CELL
    assert rows[0]["cohort"] == "prospective_replacement"
    assert report["selected_source_identity"] == source_key(rows[0]).replace("\0", "|")
    assert report["maximum_teacher_drafts_after"] == 1059
    assert report["global_teacher_draft_cap"] == 1200
    assert report["eligible_source_count"] > 0


def test_source_pool_drift_fails_closed(tmp_path: Path) -> None:
    changed = tmp_path / "plan.md"
    changed.write_bytes(PLAN.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="plan hash drift"):
        prepare(changed, QUEUE, MANIFEST)


def test_duplicate_source_cannot_be_selected() -> None:
    rows, _ = prepare(PLAN, QUEUE, MANIFEST)
    selected = rows[0]
    original = [{"id": f"q-{i}", "cell_id": CELL, "source": {"dataset": "d", "revision": "r", "record_id": f"{i}", "source_record_sha256": f"{i:064x}"}} for i in range(711)]
    original[0]["id"] = "cap-scale-associative_aggregation-python-repair-reserve-06"
    pool = [
        {"id": "only-source", "lane": "python", "task_type": "repair", "source": copy.deepcopy(selected["source"])},
        {"id": "repeat-source", "lane": "python", "task_type": "repair", "source": copy.deepcopy(selected["source"])},
    ]
    prior = [{"source": {"dataset": "prior", "revision": "r", "record_id": f"{i}"}} for i in range(3225)]
    historical = [{"candidate": {"source": {"dataset": "history", "revision": "r", "record_id": f"{i}"}}} for i in range(547)]
    lineage = [{"source_identity": f"entry|r|{i}"} for i in range(174)]
    with pytest.raises(ValueError, match="no uniquely eligible"):
        pick_source(pool, original, prior, historical, lineage)
