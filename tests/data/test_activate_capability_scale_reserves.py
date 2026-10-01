from pathlib import Path

from scripts.data.activate_capability_scale_reserves import activate


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "measurement/gate3/capability-scale-v1"
CANARY = BASE / "canary-v1"


def test_activate_exact_canary_delta_replacements() -> None:
    rows, report = activate(
        BASE / "source-queue.jsonl", BASE / "source-queue-manifest.json",
        CANARY / "delta/delta-terminal-artifacts.jsonl",
        CANARY / "delta/delta-audit-report.json",
    )
    assert report["status"] == "activated"
    assert report["terminal_failures"] == report["activated"] == 7
    assert len({row["reserve_candidate_id"] for row in rows}) == 7
    assert len({row["cell_id"] for row in rows}) == 7
    assert all(row["evaluation_artifacts_read"] == 0 for row in rows)
