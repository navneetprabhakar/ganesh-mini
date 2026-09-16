from copy import deepcopy

import pytest

from scripts.data.build_capability_corpus_plan import CAPABILITIES
from scripts.data.build_repair_delta_queue import AFFINITY_FIELDS
from scripts.data.run_repair_source_ontology import output_schema, validate_payload


def payload() -> dict:
    verdicts = []
    for index, capability in enumerate(CAPABILITIES):
        accepted = index == 0
        verdicts.append({
            "primary_capability": capability, "decision": "accept" if accepted else "reject",
            "capability_operation": "bounded operation" if accepted else "unrelated operation",
            "defect_affordance": "off by one" if accepted else "no matching defect",
            **{field: accepted for field in AFFINITY_FIELDS},
        })
    return {"items": [{"source_queue_id": "source-1", "verdicts": verdicts}]}


def test_schema_and_payload_require_exact_full_ontology() -> None:
    schema = output_schema(1)
    assert schema["properties"]["items"]["minItems"] == 1
    rows = validate_payload(payload(), ["source-1"])
    assert len(rows[0]["verdicts"]) == 10


@pytest.mark.parametrize("mutation", ["duplicate", "accept_false", "ids"])
def test_payload_fails_closed(mutation: str) -> None:
    value = deepcopy(payload())
    if mutation == "duplicate":
        value["items"][0]["verdicts"][1]["primary_capability"] = value["items"][0]["verdicts"][0]["primary_capability"]
    elif mutation == "accept_false":
        value["items"][0]["verdicts"][0][AFFINITY_FIELDS[0]] = False
    else:
        value["items"][0]["source_queue_id"] = "other"
    with pytest.raises(ValueError):
        validate_payload(value, ["source-1"])
