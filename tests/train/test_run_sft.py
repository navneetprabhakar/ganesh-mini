from scripts.train.run_sft import planned_end


def row(tokens: int) -> dict:
    return {"attention_mask":[1]*tokens}


def test_lr_budget_extends_to_complete_accumulation_boundary() -> None:
    rows=[row(10) for _ in range(20)]
    assert planned_end(rows,55,8)==8


def test_full_schedule_keeps_nondivisible_final_batch() -> None:
    rows=[row(10) for _ in range(11)]
    assert planned_end(rows,110,8)==11
