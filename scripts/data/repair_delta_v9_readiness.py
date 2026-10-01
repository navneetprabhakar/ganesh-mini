#!/usr/bin/env python3
"""V9 literal-only Rust key guard over the unchanged V8 provider contract."""
import re
from typing import Any, Mapping
from scripts.data.repair_delta_v8_readiness import response_schema, test_author_prompt
from scripts.data.repair_delta_v7_readiness import validate_lane_interface

CONTRACT_ID="capability-stratified-v9-literal-key-guard/v1"

def validate_response(projection: Mapping[str,Any], response: Any) -> dict[str,Any]:
    if not isinstance(response,dict) or set(response)!={"content","case_ids"}: raise ValueError("V9 response must contain only content and case_ids")
    content=response["content"]; ids=response["case_ids"]; minimum=2 if projection.get("role")=="primary_discrimination" else 1
    if not isinstance(content,str) or not content.strip() or not isinstance(ids,list) or len(ids)<minimum or len(set(ids))!=len(ids) or any(not isinstance(x,str) or not x.strip() for x in ids): raise ValueError("V9 content/case_ids invalid")
    findings=validate_lane_interface(str(projection.get("lane")),content)
    if findings: raise ValueError(f"V9 lane interface findings: {findings}")
    if projection.get("semantic_guard")=="rust-no-internal-key" and re.search(r"['\"]kind\.(?:audit|audited)['\"]",content): raise ValueError("V9 Rust primary asserts a literal unspecified internal key")
    if projection.get("semantic_guard")=="python-no-primary-digest-dataflow" and re.search(r"\b(?:patch|mock|sha256|hexdigest|digest)\b",content,re.I): raise ValueError("V9 Python cross reasserts primary digest dataflow")
    return response

test_author_prompt.__test__=False
