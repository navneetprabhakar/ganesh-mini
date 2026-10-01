import json
from copy import deepcopy

import pytest

from scripts.data.build_capability_corpus_plan import CAPABILITIES
from scripts.data.build_repair_delta_queue import AFFINITY_FIELDS
from scripts.data.run_repair_source_ontology import (
    ensure_attestation,
    load_excluded_source_queue_ids,
    output_schema,
    select_sources,
    selection_key,
    validate_payload,
)


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


def source(identifier: str, lane: str, dataset: str, task_type: str = "repair") -> dict:
    return {
        "id": identifier,
        "lane": lane,
        "task_type": task_type,
        "source": {
            "dataset": dataset,
            "revision": "revision-1",
            "record_id": identifier,
        },
    }


def test_select_sources_honors_requested_lanes_and_dataset_override() -> None:
    dataset = "approved/alternate"
    rows = [
        source("go-b", "go", dataset),
        source("go-a", "go", dataset),
        source("rust-a", "rust", dataset),
        source("java-a", "java", dataset),
        source("go-wrong-dataset", "go", "other/dataset"),
        source("go-generation", "go", dataset, "generation"),
    ]
    selected = select_sources(
        rows,
        eligible_ids={row["id"] for row in rows},
        excluded=set(),
        per_lane=1,
        offset=0,
        lanes=("go", "rust"),
        dataset=dataset,
    )
    expected_go = min(("go-a", "go-b"), key=lambda identifier: selection_key("go", identifier))
    assert [row["id"] for row in selected] == [expected_go, "rust-a"]


def test_select_sources_applies_queue_exclusions_before_deterministic_slice() -> None:
    dataset = "approved/alternate"
    rows = [source(identifier, "go", dataset) for identifier in ("go-a", "go-b", "go-c")]
    ordered = sorted(rows, key=lambda row: selection_key("go", row["id"]))
    selected = select_sources(
        rows,
        eligible_ids={row["id"] for row in rows},
        excluded=set(),
        per_lane=1,
        offset=0,
        lanes=("go",),
        dataset=dataset,
        excluded_source_queue_ids={ordered[0]["id"]},
    )
    assert [row["id"] for row in selected] == [ordered[1]["id"]]


def test_select_sources_rejects_duplicate_repeatable_lanes() -> None:
    rows = [source("go-a", "go", "approved/alternate")]
    with pytest.raises(ValueError, match="contains duplicates"):
        select_sources(
            rows,
            eligible_ids={"go-a"},
            excluded=set(),
            per_lane=1,
            offset=0,
            lanes=("go", "go"),
            dataset="approved/alternate",
        )


def test_ensure_attestation_creates_and_then_validates(tmp_path) -> None:
    path = tmp_path / "nested" / "attestation.json"
    attestation = {"schema_version": "test/v1", "attestation_sha256": "a" * 64}
    ensure_attestation(path, attestation)
    assert path.read_text(encoding="utf-8") == json.dumps(attestation, indent=2, sort_keys=True) + "\n"
    ensure_attestation(path, attestation)

    with pytest.raises(ValueError, match="differs from the sealed comparison"):
        ensure_attestation(path, {**attestation, "attestation_sha256": "b" * 64})


def test_load_excluded_source_queue_ids_accepts_repeatable_subset_queues(tmp_path) -> None:
    bound = [source(identifier, "go", "approved/alternate") for identifier in ("a", "b", "c")]
    first = tmp_path / "first.jsonl"
    second = tmp_path / "second.jsonl"
    first.write_text(json.dumps(bound[0]) + "\n", encoding="utf-8")
    second.write_text(json.dumps(bound[1]) + "\n", encoding="utf-8")
    assert load_excluded_source_queue_ids(bound, [first, second]) == {"a", "b"}


@pytest.mark.parametrize("failure", ["duplicate", "unknown", "malformed"])
def test_load_excluded_source_queue_ids_fails_closed(tmp_path, failure: str) -> None:
    bound = [source("a", "go", "approved/alternate")]
    path = tmp_path / "excluded.jsonl"
    if failure == "duplicate":
        rows = [bound[0], bound[0]]
        message = "not unique"
    elif failure == "unknown":
        rows = [source("unknown", "go", "approved/alternate")]
        message = "absent from the bound source queue"
    else:
        rows = [{"lane": "go"}]
        message = "missing or malformed ID"
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        load_excluded_source_queue_ids(bound, [path])
