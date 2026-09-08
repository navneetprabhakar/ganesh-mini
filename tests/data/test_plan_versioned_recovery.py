import copy
import json

import pytest

from scripts.data.admit_expansion import canonical_json
from scripts.data.plan_versioned_recovery import digest, make_plan, write_plan


def inputs():
    row = {
        "id": "exp-v1-python-generation-0001", "lane": "python", "task_type": "generation",
        "source": {"revision": "pinned", "record_id": "source-1", "license": "MIT"},
        "rights": {key: True for key in ("prompt", "answer", "tests", "redistribution", "model_training")},
    }
    candidates = canonical_json(row) + b"\n"
    holds = canonical_json({"holds": [{"id": row["id"], "reason": "wrong required field"}]})
    request = {
        "version": "r1", "parent_corpus_sha256": digest(candidates),
        "hold_ledger_sha256": digest(holds),
        "selections": [{"parent_id": row["id"], "parent_candidate_sha256": digest(canonical_json(row)),
                        "change_class": "contract-clarification", "rationale": "Specify required field",
                        "review_evidence": "review.md"}],
    }
    return candidates, holds, request


def test_plan_preserves_parent_and_new_identity():
    candidates, holds, request = inputs()
    before = copy.deepcopy(request)
    plan = make_plan(candidates, holds, canonical_json(request))
    assert request == before
    record = plan["records"][0]
    assert record["id"] == "exp-v1-recovery-r1-python-generation-0001"
    assert record["parent_source"] == json.loads(candidates)["source"]
    assert record["parent_rights"] == json.loads(candidates)["rights"]
    assert record["status"] == "planned-not-generated-not-admitted"
    seal = plan.pop("plan_sha256")
    assert digest(canonical_json(plan)) == seal


@pytest.mark.parametrize("field", ["parent_corpus_sha256", "hold_ledger_sha256"])
def test_rejects_unbound_inputs(field):
    candidates, holds, request = inputs()
    request[field] = "bad"
    with pytest.raises(ValueError, match="hash mismatch"):
        make_plan(candidates, holds, canonical_json(request))


@pytest.mark.parametrize("field,value", [
    ("parent_id", "unknown"), ("parent_candidate_sha256", "bad"),
    ("change_class", "pad-trivial-task"), ("rationale", ""), ("review_evidence", ""),
])
def test_rejects_invalid_selection(field, value):
    candidates, holds, request = inputs()
    request["selections"][0][field] = value
    with pytest.raises(ValueError):
        make_plan(candidates, holds, canonical_json(request))


def test_rejects_duplicate_selection_and_unsafe_version():
    candidates, holds, request = inputs()
    request["selections"] *= 2
    with pytest.raises(ValueError, match="duplicate recovery"):
        make_plan(candidates, holds, canonical_json(request))
    request["version"] = "../../outside"
    with pytest.raises(ValueError, match="version"):
        make_plan(candidates, holds, canonical_json(request))


def test_output_is_create_only(tmp_path):
    candidates, holds, request = inputs()
    plan = make_plan(candidates, holds, canonical_json(request))
    target = tmp_path / "recovery"
    write_plan(target, plan)
    original = (target / "plan.json").read_bytes()
    with pytest.raises(FileExistsError):
        write_plan(target, {"overwritten": True})
    assert (target / "plan.json").read_bytes() == original
