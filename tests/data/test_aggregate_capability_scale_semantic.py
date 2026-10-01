from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.data.aggregate_capability_scale_semantic import aggregate


ROOT = Path(__file__).resolve().parents[2]
CANARY = ROOT / "measurement/gate3/capability-scale-v1/canary-v1"


def test_aggregate_sealed_canary_semantic_evidence() -> None:
    rows, report = aggregate(CANARY / "teacher/candidates.jsonl", CANARY / "semantic")
    assert report["status"] == "complete"
    assert report["counts"] == {"reviewed": 12, "passed": 11, "rejected": 1}
    assert len(rows) == 12
    assert sum(row["visibility"]["evaluation_artifacts_read"] for row in rows) == 0


def test_aggregate_rejects_tampered_batch(tmp_path: Path) -> None:
    source = CANARY / "semantic"
    for path in source.iterdir():
        (tmp_path / path.name).write_bytes(path.read_bytes())
    target = next(tmp_path.glob("*.semantic.jsonl"))
    values = target.read_text(encoding="utf-8").splitlines()
    row = json.loads(values[0]); row["verdict"] = "reject"
    values[0] = json.dumps(row, sort_keys=True)
    target.write_text("\n".join(values) + "\n", encoding="utf-8")
    with pytest.raises(ValueError):
        aggregate(CANARY / "teacher/candidates.jsonl", tmp_path)
