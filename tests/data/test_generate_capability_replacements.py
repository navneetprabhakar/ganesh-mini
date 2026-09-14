from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.data.generate_capability_replacements import build_replacement_queue, empty_cells


def queue() -> list[dict]:
    rows = []
    for cell in range(2):
        for ordinal in range(2):
            rows.append({
                "id": f"q-{cell}-{ordinal}", "cell_id": f"cap-{cell}/python/generation",
                "primary_capability": f"cap-{cell}", "primary_capability_definition": "definition",
                "assigned_cross_cutting_dimension": "malformed_input", "lane": "python",
                "task_type": "generation", "source_queue_id": f"source-{cell}-{ordinal}",
                "source": {"dataset": "fixture", "revision": "r", "record_id": f"old-{cell}-{ordinal}"},
                "stimulus": "old",
            })
    return rows


def semantic() -> dict:
    return {
        "schema_version": "ganesh-mini-capability-semantic-review-report/v1",
        "status": "complete", "evaluation_artifacts_read": 0,
        "records": [
            {
                "id": row["id"], "primary_capability": row["primary_capability"],
                "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
                "verdict": "reject" if row["cell_id"].startswith("cap-0/") else "pass",
            }
            for row in queue()
        ],
    }


def sources() -> list[dict]:
    return [
        {
            "id": f"fresh-{index}", "lane": "python", "task_type": "generation",
            "source": {"dataset": "fixture", "revision": "r", "record_id": f"fresh-{index}"},
            "stimulus": f"fresh {index}",
        }
        for index in range(3)
    ]


def test_derives_only_empty_cells_and_assigns_one_fresh_bound_replacement() -> None:
    rows = build_replacement_queue(queue(), semantic(), sources(), [], "a" * 64)
    assert len(rows) == 1
    assert rows[0]["cell_id"] == "cap-0/python/generation"
    assert rows[0]["replacement_attempt"] == 1
    assert rows[0]["original_queue_ids"] == ["q-0-0", "q-0-1"]
    assert rows[0]["source"]["record_id"].startswith("fresh-")
    assert rows[0]["id"] not in {row["id"] for row in queue()}


def test_rejects_incomplete_or_duplicate_disposition_evidence() -> None:
    missing = semantic(); missing["records"].pop()
    with pytest.raises(ValueError, match="all 240 originals"):
        empty_cells(queue(), missing)
    duplicate = semantic(); duplicate["records"][1] = deepcopy(duplicate["records"][0])
    with pytest.raises(ValueError, match="all 240 originals|duplicate"):
        empty_cells(queue(), duplicate)


def test_replacement_source_cannot_reuse_original_or_prior_lineage() -> None:
    reused = [{
        "id": "only", "lane": "python", "task_type": "generation",
        "source": queue()[0]["source"], "stimulus": "same",
    }]
    with pytest.raises(ValueError, match="no collision-free"):
        build_replacement_queue(queue(), semantic(), reused, [], "a" * 64)

