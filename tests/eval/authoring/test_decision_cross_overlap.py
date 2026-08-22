from scripts.eval.authoring.audit_decision_tranches1_2_overlap import ROOT, build
from scripts.eval.contracts import load_json, sha256_object


def test_decision_tranches1_2_are_disjoint_and_bound() -> None:
    report = build()
    assert report["status"] == "passed"
    assert [row["task_count"] for row in report["manifests"]] == [60, 60]
    assert report["exact_prompt_overlaps"] == []
    assert report["normalized_prompt_overlaps"] == []
    assert report["duplicate_task_ids"] == []
    stored = load_json(ROOT / "manifests/evaluation/private/decision-tranches1-2-cross-overlap.json")
    claimed = stored.pop("report_sha256")
    assert sha256_object(stored) == claimed == report["report_sha256"]
