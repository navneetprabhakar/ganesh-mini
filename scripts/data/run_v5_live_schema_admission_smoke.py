#!/usr/bin/env python3
"""Run one content-free live admission smoke for the production V5 response schema."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import (
    CodexInvocationFailure, invoke_codex, verify_codex_version,
)
from scripts.data.run_repair_delta_evidence import (
    V5_TEST_AUTHOR_RESPONSE_SCHEMA_VERSION, _add_tests_v5, _response_schema, _stage_prompt,
)
from scripts.eval.contracts import sha256_text


REPORT_SCHEMA = "ganesh-mini-v5-live-schema-admission-smoke/v1"
RUN_KIND = "repair-delta-v5-schema-admission-smoke"
LANE = "python"
PRODUCTION_CONFIG_PATH = ROOT / "configs/data/expansion_teacher.json"
V3_READINESS_OUTPUT = (
    ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"
    / "primary-two-phase-v3/readiness-v1/live-schema-admission-smoke.json"
)
SYNTHETIC_PROJECTION = {
    "id": "v5-schema-admission-smoke",
    "lane": LANE,
    "specification": (
        "Synthetic schema-only fixture: define tests for a function that returns the sum of two integers."
    ),
    "embedded_known_bad": "def add(left, right):\n    return left - right\n",
    "primary_capability": "synthetic_integer_addition",
    "primary_capability_definition": "Distinguish addition from subtraction on two fixed integer pairs.",
    "assigned_cross_cutting_dimension": "synthetic_type_error",
}
SYNTHETIC_CANDIDATE = {
    "id": SYNTHETIC_PROJECTION["id"],
    "lane": LANE,
    "messages": [{"role": "user", "content": SYNTHETIC_PROJECTION["specification"]}],
    "verification_task": {
        "files": [],
        "validation": {
            "known_bad": [{"sha256": sha256_text(SYNTHETIC_PROJECTION["embedded_known_bad"])}],
        },
    },
}
SYNTHETIC_ASSIGNMENT = {
    "primary_capability": SYNTHETIC_PROJECTION["primary_capability"],
    "assigned_cross_cutting_dimension": SYNTHETIC_PROJECTION[
        "assigned_cross_cutting_dimension"
    ],
}
Invoker = Callable[[str, dict[str, Any], Path, str, str, str], tuple[dict[str, Any], dict[str, Any]]]


def _seal_report(value: dict[str, Any]) -> dict[str, Any]:
    value["report_sha256"] = canonical_sha256(value)
    return value


def _controls(
    config: dict[str, Any], config_file_sha256: str, cli_identity: str,
) -> tuple[dict[str, Any], str, dict[str, Any]]:
    schema = _response_schema("test_author", "v5")
    prompt = _stage_prompt("test_author", copy.deepcopy(SYNTHETIC_PROJECTION), "v5")
    controls = {
        "response_schema": schema,
        "response_schema_sha256": canonical_sha256(schema),
        "response_schema_version": V5_TEST_AUTHOR_RESPONSE_SCHEMA_VERSION,
        "prompt": prompt,
        "prompt_sha256": sha256_text(prompt),
        "config_sha256": canonical_sha256(config),
        "config_file_sha256": config_file_sha256,
        "cli_identity": cli_identity,
        "cli_identity_sha256": sha256_text(cli_identity),
        "run_kind": RUN_KIND,
        "lane": LANE,
    }
    return schema, prompt, controls


def _base_report(controls: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": REPORT_SCHEMA,
        "status": "failed",
        "contract": "capability-stratified-v5-interface-replay/v1",
        "purpose": "content-free-live-response-schema-admission",
        "controls": controls,
        "model_calls": 1,
        "content_scope": {
            "synthetic_fixed_prompt_only": True,
            "candidate_artifacts_read": 0,
            "source_artifacts_read": 0,
            "evaluation_artifacts_read": 0,
        },
        "raw_run": None,
        "raw_run_sha256": None,
        "response": None,
        "response_sha256": None,
        "application_evidence": None,
        "failure": None,
    }


def _attach_run(report: dict[str, Any], run: dict[str, Any]) -> None:
    report["raw_run"] = copy.deepcopy(run)
    report["raw_run_sha256"] = canonical_sha256(run)


def _run_contract_error(
    run: dict[str, Any], response: dict[str, Any], expected_prompt_sha256: str,
) -> str | None:
    events = run.get("events")
    agent_response = isinstance(events, list) and any(
        isinstance(event, dict)
        and event.get("type") == "item.completed"
        and isinstance(event.get("item"), dict)
        and event["item"].get("type") == "agent_message"
        for event in events
    )
    observed_disallowed = [] if not isinstance(events, list) else [
        event["item"].get("type")
        for event in events
        if isinstance(event, dict)
        and isinstance(event.get("item"), dict)
        and event["item"].get("type") not in {None, "reasoning", "agent_message"}
    ]
    if run.get("timed_out") is not False:
        return "live schema-admission call timed out or omitted timeout status"
    if run.get("returncode") != 0:
        return "live schema-admission call did not exit zero"
    if run.get("event_parse_error") is not None:
        return "live schema-admission call emitted invalid event JSONL"
    if run.get("disallowed_tool_item_types") or observed_disallowed:
        return "live schema-admission call used a disallowed tool"
    if not isinstance(run.get("usage"), dict):
        return "live schema-admission call omitted terminal usage"
    if not agent_response:
        return "live schema-admission call omitted a completed agent response"
    if run.get("run_kind") != RUN_KIND or run.get("lane") != LANE:
        return "live schema-admission raw run has the wrong invocation identity"
    if run.get("prompt_sha256") != expected_prompt_sha256:
        return "live schema-admission raw run is not bound to the fixed prompt"
    try:
        final_payload = json.loads(run.get("final_output", ""))
    except (json.JSONDecodeError, TypeError):
        return "live schema-admission raw final output is not JSON"
    if final_payload != response:
        return "live schema-admission parsed response differs from raw final output"
    return None


def run_v5_live_schema_admission_smoke(
    config: dict[str, Any], config_file_sha256: str, cli_identity: str,
    codex_bin: str = "codex", invoker: Invoker = invoke_codex,
) -> dict[str, Any]:
    """Execute exactly one synthetic call and return a sealed pass/fail report."""
    schema, prompt, controls = _controls(config, config_file_sha256, cli_identity)
    report = _base_report(controls)
    try:
        with tempfile.TemporaryDirectory(prefix="ganesh-v5-schema-admission-") as temp_name:
            schema_path = Path(temp_name) / "schema.json"
            schema_path.write_text(
                json.dumps(schema, sort_keys=True) + "\n", encoding="utf-8",
            )
            response, run = invoker(
                codex_bin, config, schema_path, prompt, RUN_KIND, LANE,
            )
    except CodexInvocationFailure as exc:
        _attach_run(report, exc.evidence)
        report["failure"] = {
            "classification": "invocation-failure",
            "exception_type": type(exc).__name__,
            "reason": str(exc),
        }
        return _seal_report(report)

    _attach_run(report, run)
    run_error = _run_contract_error(run, response, controls["prompt_sha256"])
    if run_error is not None:
        report["failure"] = {
            "classification": "run-contract-failure", "reason": run_error,
        }
        return _seal_report(report)

    report["response"] = copy.deepcopy(response)
    report["response_sha256"] = canonical_sha256(response)
    try:
        _, evidence = _add_tests_v5(
            copy.deepcopy(SYNTHETIC_CANDIDATE),
            copy.deepcopy(SYNTHETIC_ASSIGNMENT),
            copy.deepcopy(response),
            report["raw_run_sha256"],
        )
    except (KeyError, TypeError, ValueError) as exc:
        report["failure"] = {
            "classification": "application-contract-failure",
            "exception_type": type(exc).__name__,
            "reason": str(exc),
        }
        return _seal_report(report)

    report["status"] = "passed"
    report["application_evidence"] = evidence
    return _seal_report(report)


def validate_v5_live_schema_admission_smoke_report(
    report: Any, config: dict[str, Any], config_file_sha256: str, cli_identity: str,
) -> dict[str, Any]:
    """Validate a passing smoke report against the current production controls."""
    if not isinstance(report, dict):
        raise ValueError("V5 live schema-admission smoke report is missing")
    body = dict(report); claimed = body.pop("report_sha256", None)
    _, _, expected_controls = _controls(config, config_file_sha256, cli_identity)
    raw_run = report.get("raw_run")
    response = report.get("response")
    if (
        set(report) != {
            "schema_version", "status", "contract", "purpose", "controls",
            "model_calls", "content_scope", "raw_run", "raw_run_sha256",
            "response", "response_sha256", "application_evidence", "failure",
            "report_sha256",
        }
        or claimed != canonical_sha256(body)
        or report.get("schema_version") != REPORT_SCHEMA
        or report.get("status") != "passed"
        or report.get("contract") != "capability-stratified-v5-interface-replay/v1"
        or report.get("purpose") != "content-free-live-response-schema-admission"
        or report.get("controls") != expected_controls
        or report.get("model_calls") != 1
        or report.get("content_scope") != {
            "synthetic_fixed_prompt_only": True,
            "candidate_artifacts_read": 0,
            "source_artifacts_read": 0,
            "evaluation_artifacts_read": 0,
        }
        or not isinstance(raw_run, dict)
        or report.get("raw_run_sha256") != canonical_sha256(raw_run)
        or not isinstance(response, dict)
        or report.get("response_sha256") != canonical_sha256(response)
        or report.get("failure") is not None
        or _run_contract_error(raw_run, response, expected_controls["prompt_sha256"])
        is not None
    ):
        raise ValueError("V5 live schema-admission smoke report is invalid or unbound")
    _, expected_evidence = _add_tests_v5(
        copy.deepcopy(SYNTHETIC_CANDIDATE), copy.deepcopy(SYNTHETIC_ASSIGNMENT),
        copy.deepcopy(response), report["raw_run_sha256"],
    )
    if report.get("application_evidence") != expected_evidence:
        raise ValueError("V5 live schema-admission application evidence differs")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=PRODUCTION_CONFIG_PATH)
    parser.add_argument("--output", type=Path, default=V3_READINESS_OUTPUT)
    parser.add_argument("--codex-bin", default="codex")
    args = parser.parse_args(argv)
    if args.config.resolve() != PRODUCTION_CONFIG_PATH.resolve():
        raise ValueError("V5 live schema smoke requires the exact production Codex config path")
    config_bytes = args.config.read_bytes()
    config = json.loads(config_bytes)
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    report = run_v5_live_schema_admission_smoke(
        config, hashlib.sha256(config_bytes).hexdigest(), cli_identity, args.codex_bin,
    )
    if report["status"] == "passed":
        validate_v5_live_schema_admission_smoke_report(
            report, config, hashlib.sha256(config_bytes).hexdigest(), cli_identity,
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"], "report_sha256": report["report_sha256"],
        "response_schema_sha256": report["controls"]["response_schema_sha256"],
    }, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
