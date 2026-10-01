#!/usr/bin/env python3
"""Versioned V7 readiness primitives for order-insensitive JSON objects.

V6 remains immutable.  V7 accepts either JSON member order, requires the exact
role-key set, and always processes roles in the controller's canonical order.
"""

from __future__ import annotations

import json
from typing import Any

from scripts.data import repair_delta_v6_readiness as v6
from scripts.data.build_capability_corpus_plan import canonical_sha256


CONTRACT_ID = "capability-stratified-v7-order-insensitive-canonical-test-replay/v1"
RESPONSE_SCHEMA_VERSION = "ganesh-mini-repair-delta-v7-test-author-response/v1"
ROLES = v6.ROLES
CANONICAL_LANE_INTERFACES = v6.CANONICAL_LANE_INTERFACES
validate_lane_interface = v6.validate_lane_interface


def author_projection(candidate: dict[str, Any], assignment: dict[str, Any]) -> dict[str, Any]:
    return v6.test_author_projection(candidate, assignment)


def response_schema() -> dict[str, Any]:
    schema = v6.response_schema()
    schema["$id"] = RESPONSE_SCHEMA_VERSION
    return schema


def parse_response_json(text: str) -> dict[str, Any]:
    """Parse provider JSON while rejecting duplicate serialized object keys."""
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate serialized JSON key: {key}")
            result[key] = value
        return result

    try:
        parsed = json.loads(text, object_pairs_hook=no_duplicates)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid provider JSON: {exc}") from exc
    validate_response(parsed)
    return parsed


def author_prompt(projection: dict[str, Any]) -> str:
    # JSON objects are unordered.  The provider must emit the exact role set;
    # deterministic role sequencing is exclusively controller-owned.
    return v6.test_author_prompt(projection).replace(
        "Return exactly primary_discrimination and cross_cutting;",
        "Return exactly the object keys primary_discrimination and cross_cutting; JSON member order is irrelevant;",
    )


# Public production aliases are deliberately marked non-tests for pytest's
# imported-callable discovery.
test_author_projection = author_projection
test_author_projection.__test__ = False
test_author_prompt = author_prompt
test_author_prompt.__test__ = False


def validate_response(response: Any) -> dict[str, Any]:
    if not isinstance(response, dict) or set(response) != set(ROLES):
        raise ValueError("V7 response must contain the exact two role keys")
    for role in ROLES:
        value = response.get(role)
        if not isinstance(value, dict) or set(value) != {"content", "case_ids"}:
            raise ValueError(f"{role} must contain only content and case_ids")
        content, case_ids = value.get("content"), value.get("case_ids")
        minimum = 2 if role == "primary_discrimination" else 1
        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"{role} content must be non-empty")
        if (
            not isinstance(case_ids, list)
            or len(case_ids) < minimum
            or any(not isinstance(item, str) or not item.strip() for item in case_ids)
            or len(set(case_ids)) != len(case_ids)
        ):
            raise ValueError(f"{role} case_ids violate minimum or local uniqueness")
    return response


def inject_controller_paths(lane: str, response: Any) -> dict[str, Any]:
    response = validate_response(response)
    if lane not in CANONICAL_LANE_INTERFACES:
        raise ValueError(f"unsupported V7 lane: {lane}")
    interface = CANONICAL_LANE_INTERFACES[lane]
    roles = []
    for ordinal, role in enumerate(ROLES):
        value = response[role]
        logical_path = f"roles/{ordinal + 1:02d}-{role}/{interface['test_path']}"
        roles.append({
            "role": role,
            "logical_path": logical_path,
            "canonical_execution_path": interface["test_path"],
            "candidate_path": interface["candidate_path"],
            "commands": [list(command) for command in interface["commands"]],
            "content": value["content"],
            "case_ids": list(value["case_ids"]),
            "raw_role_sha256": canonical_sha256(value),
            "injected_path_sha256": canonical_sha256({
                "role": role,
                "logical_path": logical_path,
                "canonical_execution_path": interface["test_path"],
                "candidate_path": interface["candidate_path"],
            }),
        })
    result = {"lane": lane, "interface": interface, "roles": roles}
    result["injection_sha256"] = canonical_sha256(result)
    return result
