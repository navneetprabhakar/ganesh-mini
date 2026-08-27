from __future__ import annotations

import math

import pytest

from scripts.train.prepare_seed import LANES, attach_objective_weights


def prepared(source_id: str, lane: str, response_tokens: int) -> dict:
    return {"source_id":source_id,"id":source_id,"lane":lane,"input_ids":[1]+[2]*response_tokens,"attention_mask":[1]*(response_tokens+1),"labels":[-100]+[2]*response_tokens,"prompt_token_count":1,"rendered_prompt_sha256":"a"*64}


def test_unique_row_weights_reconstruct_exact_five_family_objective() -> None:
    targets={"go":0.2,"java":0.2,"javascript":0.1,"typescript":0.1,"python":0.2,"rust":0.2}
    rows=[]
    for lane in LANES:
        rows.extend((prepared(f"{lane}-short",lane,1),prepared(f"{lane}-long",lane,9)))
    weighted,shares=attach_objective_weights(rows,targets,8)
    assert len(weighted)==len({row["source_id"] for row in weighted})==12
    assert all(math.isclose(shares[lane],targets[lane],abs_tol=1e-12) for lane in LANES)
    assert next(row for row in weighted if row["id"]=="go-long")["objective_weight"]==pytest.approx(9*next(row for row in weighted if row["id"]=="go-short")["objective_weight"])


def test_duplicate_source_rows_are_rejected_instead_of_oversampled() -> None:
    targets={"go":0.2,"java":0.2,"javascript":0.1,"typescript":0.1,"python":0.2,"rust":0.2}
    with pytest.raises(ValueError,match="unique source"):
        attach_objective_weights([prepared("same","go",1),prepared("same","go",2)],targets,8)
