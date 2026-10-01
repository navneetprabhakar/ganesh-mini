from argparse import Namespace
from pathlib import Path

from scripts.data.activate_capability_scale_test_reauthors import activate
from scripts.data.seal_capability_scale_canary import run


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "measurement/gate3/capability-scale-v1"
V1 = BASE / "canary-v1"
V2 = BASE / "canary-v2-reserves"


def test_test_reauthor_activation_is_exact_and_blind() -> None:
    rows, report = activate(
        V2 / "matrix/terminal-artifacts.jsonl", V2 / "matrix/matrix-report.json",
    )
    assert report["activated"] == 2
    assert {row["candidate_id"] for row in rows} == {
        "cap-scale-associative_aggregation-go-repair-reserve-06",
        "cap-scale-associative_aggregation-typescript-generation-reserve-05",
    }
    assert all(row["correction_count"] == 1 for row in rows)
    assert all(not row["author_visibility"]["verifier_outputs_visible"] for row in rows)


def test_sealed_canary_resolves_exact_lane_task_matrix() -> None:
    candidates, result = run(Namespace(
        original_candidates=V1 / "teacher/candidates.jsonl",
        reserve_candidates=V2 / "teacher/candidates.jsonl",
        original_semantic=V1 / "semantic/combined-semantic.jsonl",
        reserve_semantic=V2 / "semantic/combined-semantic.jsonl",
        original_matrix=V1 / "matrix-passed/terminal-artifacts.jsonl",
        original_matrix_report=V1 / "matrix-passed/matrix-report.json",
        reserve_matrix=V2 / "matrix/terminal-artifacts.jsonl",
        reserve_matrix_report=V2 / "matrix/matrix-report.json",
        correction_matrix=V2 / "matrix-reauthor/terminal-artifacts.jsonl",
        correction_matrix_report=V2 / "matrix-reauthor/matrix-report.json",
    ))
    assert result["report"]["status"] == "passed"
    assert result["report"]["admitted"] == len(candidates) == 12
    assert sum(row["correction_count"] for row in result["records"]) == 2
    assert len({(row["lane"], row["task_type"]) for row in result["records"]}) == 12
