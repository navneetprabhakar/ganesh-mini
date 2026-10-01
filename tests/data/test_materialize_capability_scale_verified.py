from __future__ import annotations

from pathlib import Path

from scripts.data.materialize_capability_scale_verified import materialize


ROOT = Path(__file__).resolve().parents[2]
SCALE = ROOT / "measurement/gate3/capability-scale-v1"


def test_exact_546_verified_envelopes_are_materialized() -> None:
    rows, report = materialize(SCALE, SCALE / "provisional-assembly-v2")
    assert len(rows) == report["records"] == 546
    assert report["stage_counts"] == {"canary": 12, "first_pass": 518, "reserve": 15, "prospective": 1}
    assert all(
        len([item for item in row["verification_task"]["files"] if item["role"] == "test"]) == 2
        for row in rows
    )
    assert len({row["id"] for row in rows}) == 546
