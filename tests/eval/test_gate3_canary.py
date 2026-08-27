from pathlib import Path

from scripts.eval.build_gate3_canary import build


ROOT=Path(__file__).resolve().parents[2]


def test_gate3_canary_is_structural_balanced_and_not_training_eligible(tmp_path: Path) -> None:
    result=build(ROOT,tmp_path/"canary.json")
    assert result["records"]==30
    assert result["lanes"]=={"go":5,"java":5,"javascript":5,"typescript":5,"python":5,"rust":5}
    assert result["checkpoint_triage_allowed"] is True
    assert result["promotion_selection_allowed"] is False
    assert result["training_admission_allowed"] is False
    assert "without reading model results" in result["selection_rule"]
