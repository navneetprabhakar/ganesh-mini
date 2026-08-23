import pytest

from scripts.train.run_sft import bounded_training_wall, five_family_validation, planned_end


def row(tokens: int) -> dict:
    return {"attention_mask":[1]*tokens}


def test_lr_budget_extends_to_complete_accumulation_boundary() -> None:
    rows=[row(10) for _ in range(20)]
    assert planned_end(rows,55,8)==8


def test_full_schedule_keeps_nondivisible_final_batch() -> None:
    rows=[row(10) for _ in range(11)]
    assert planned_end(rows,110,8)==11


def test_validation_macro_counts_javascript_and_typescript_as_one_family() -> None:
    result=five_family_validation({
        "go":[1.0],"java":[2.0],"javascript":[3.0],"typescript":[5.0],"python":[6.0],"rust":[7.0]
    })
    assert result["javascript_typescript_family_mean"]==4.0
    assert result["five_family_macro_mean"]==4.0


def test_validation_macro_fails_closed_when_a_lane_is_empty() -> None:
    with pytest.raises(RuntimeError,match="every frozen lane"):
        five_family_validation({
            "go":[1.0],"java":[2.0],"javascript":[3.0],"typescript":[],"python":[6.0],"rust":[7.0]
        })


def test_training_wall_reserves_finalization_from_both_bounds() -> None:
    assert bounded_training_wall(21600,10000)==9400
    assert bounded_training_wall(5000,10000)==4400


def test_training_wall_rejects_an_envelope_too_small_to_finalize() -> None:
    with pytest.raises(RuntimeError,match="insufficient training and finalization"):
        bounded_training_wall(650,10000)
