from pathlib import Path

from scripts.eval.build_retention_slice import build,canonical_sha256


ROOT=Path(__file__).resolve().parents[2]


def test_retention_slice_is_frozen_balanced_and_sealed() -> None:
    report=build(ROOT); unsigned=dict(report); claimed=unsigned.pop("manifest_sha256")
    assert canonical_sha256(unsigned)==claimed and report["task_count"]==12
    assert {lane:sum(row["language"]==lane for row in report["tasks"]) for lane in {row["language"] for row in report["tasks"]}}=={"go":2,"java":2,"javascript":2,"typescript":2,"python":2,"rust":2}
