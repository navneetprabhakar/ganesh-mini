from __future__ import annotations

import copy

import pytest

from scripts.data.repair_delta_v7_readiness import (
    CANONICAL_LANE_INTERFACES,
    RESPONSE_SCHEMA_VERSION,
    inject_controller_paths,
    parse_response_json,
    response_schema,
    validate_response,
)


def _response() -> dict:
    return {
        "primary_discrimination": {"content": "primary", "case_ids": ["p1", "p2"]},
        "cross_cutting": {"content": "cross", "case_ids": ["c1"]},
    }


def test_v7_schema_is_versioned_and_has_exact_role_properties() -> None:
    schema = response_schema()
    assert schema["$id"] == RESPONSE_SCHEMA_VERSION
    assert set(schema["properties"]) == {"primary_discrimination", "cross_cutting"}


def test_v7_accepts_reversed_json_member_order() -> None:
    response = _response()
    reversed_response = {"cross_cutting": response["cross_cutting"], "primary_discrimination": response["primary_discrimination"]}
    assert validate_response(reversed_response) == reversed_response


def test_v7_serialized_parser_rejects_duplicate_keys() -> None:
    text = '{"primary_discrimination":{"content":"p","case_ids":["1","2"]},"cross_cutting":{"content":"c","case_ids":["1"]},"cross_cutting":{"content":"d","case_ids":["2"]}}'
    with pytest.raises(ValueError, match="duplicate serialized JSON key"):
        parse_response_json(text)


@pytest.mark.parametrize("lane", CANONICAL_LANE_INTERFACES)
def test_v7_controller_processes_reversed_input_in_canonical_role_order(lane: str) -> None:
    response = _response()
    reversed_response = {"cross_cutting": response["cross_cutting"], "primary_discrimination": response["primary_discrimination"]}
    injected = inject_controller_paths(lane, reversed_response)
    assert [row["role"] for row in injected["roles"]] == ["primary_discrimination", "cross_cutting"]


@pytest.mark.parametrize("mutation", [
    lambda value: value.update({"extra": {}}),
    lambda value: value.pop("cross_cutting"),
    lambda value: value["primary_discrimination"].update({"path": "x"}),
])
def test_v7_still_requires_exact_keys(mutation) -> None:
    response = copy.deepcopy(_response())
    mutation(response)
    with pytest.raises(ValueError):
        validate_response(response)
