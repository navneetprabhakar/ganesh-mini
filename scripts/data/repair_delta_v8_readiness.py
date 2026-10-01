#!/usr/bin/env python3
"""V8 single-role correction schema, prompts, and local validators."""

from __future__ import annotations

import json
import re
from typing import Any, Mapping

from scripts.data.repair_delta_v7_readiness import validate_lane_interface


CONTRACT_ID = "capability-stratified-v8-two-role-correction/v1"
RESPONSE_SCHEMA_VERSION = "ganesh-mini-repair-delta-v8-single-role-response/v1"


def response_schema() -> dict[str, Any]:
    return {
        "$id": RESPONSE_SCHEMA_VERSION,
        "type": "object", "additionalProperties": False,
        "required": ["content", "case_ids"],
        "properties": {
            "content": {"type": "string", "minLength": 1},
            "case_ids": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}},
        },
    }


def test_author_prompt(projection: Mapping[str, Any]) -> str:
    role = projection.get("role")
    if role not in {"primary_discrimination", "cross_cutting"}:
        raise ValueError("unsupported V8 role")
    special = str(projection.get("role_constraints", "")).strip()
    if not special:
        raise ValueError("V8 projection lacks role constraints")
    common = (
        "Use exactly the supplied canonical filename, command, and local binding. Use standard-library, "
        "deterministic tests only. You have not seen the reference, V7 tests/outcomes, verifier output, "
        "teacher proof, semantic review, source data, or evaluation content. Do not use tools or inspect "
        "the filesystem. Return only the schema-constrained object."
    )
    return f"{special} {common}\nInput: {json.dumps(dict(projection), separators=(',', ':'), ensure_ascii=False)}"


def validate_response(projection: Mapping[str, Any], response: Any) -> dict[str, Any]:
    if not isinstance(response, dict) or set(response) != {"content", "case_ids"}:
        raise ValueError("V8 response must contain only content and case_ids")
    content, case_ids = response["content"], response["case_ids"]
    minimum = 2 if projection.get("role") == "primary_discrimination" else 1
    if not isinstance(content, str) or not content.strip():
        raise ValueError("V8 content must be non-empty")
    if not isinstance(case_ids, list) or len(case_ids) < minimum or len(set(case_ids)) != len(case_ids) or any(not isinstance(x, str) or not x.strip() for x in case_ids):
        raise ValueError("V8 case_ids violate minimum or uniqueness")
    findings = validate_lane_interface(str(projection.get("lane")), content)
    if findings:
        raise ValueError(f"V8 lane interface findings: {findings}")
    if projection.get("semantic_guard") == "rust-no-internal-key" and re.search(r"kind\.(?:audit|audited)|metadata\s*\(\)\s*\.\s*get", content):
        raise ValueError("V8 Rust primary asserts an unspecified internal metadata key")
    if projection.get("semantic_guard") == "python-no-primary-digest-dataflow" and re.search(r"\b(?:patch|mock|sha256|hexdigest|digest)\b", content, re.I):
        raise ValueError("V8 Python cross reasserts primary digest dataflow")
    return response


test_author_prompt.__test__ = False
