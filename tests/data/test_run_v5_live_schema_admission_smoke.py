from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import CodexInvocationFailure
from scripts.data.run_repair_delta_evidence import _response_schema, _stage_prompt
from scripts.data.run_v5_live_schema_admission_smoke import (
    LANE, REPORT_SCHEMA, RUN_KIND, SYNTHETIC_PROJECTION,
    run_v5_live_schema_admission_smoke,
    validate_v5_live_schema_admission_smoke_report,
)


def valid_response() -> dict:
    return {
        "primary_discrimination": {
            "path": "primary_test.py",
            "content": "assert 1 + 2 == 3\nassert -1 + 2 == 1",
            "case_ids": ["positive", "signed"],
        },
        "cross_cutting": {
            "path": "cross_test.py",
            "content": "try:\n    int('not-an-int')\nexcept ValueError:\n    pass",
            "case_ids": ["type-error"],
        },
    }


def valid_run(response: dict | None = None) -> dict:
    response = valid_response() if response is None else response
    prompt = _stage_prompt("test_author", SYNTHETIC_PROJECTION, "v5")
    return {
        "run_kind": RUN_KIND,
        "lane": LANE,
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "returncode": 0,
        "stdout_jsonl": "fixture",
        "stderr": "",
        "final_output": json.dumps(response),
        "events": [
            {"type": "item.completed", "item": {"type": "agent_message"}},
            {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5}},
        ],
        "usage": {"input_tokens": 10, "output_tokens": 5},
        "disallowed_tool_item_types": [],
        "event_parse_error": None,
        "timed_out": False,
    }


def test_live_schema_smoke_is_one_call_content_free_and_fully_sealed() -> None:
    calls = []
    config = {"model": "fixture", "codex_cli_version": "1.2.3", "execution": {}}

    def invoke(binary, passed_config, schema_path, prompt, run_kind, lane):
        calls.append({
            "binary": binary, "config": copy.deepcopy(passed_config),
            "schema": json.loads(schema_path.read_text()), "prompt": prompt,
            "run_kind": run_kind, "lane": lane,
        })
        return valid_response(), valid_run()

    report = run_v5_live_schema_admission_smoke(
        config, "f" * 64, "codex-cli 1.2.3", "codex-fixture", invoke,
    )

    assert len(calls) == 1
    assert calls[0]["schema"] == _response_schema("test_author", "v5")
    assert calls[0]["config"] == config
    assert calls[0]["run_kind"] == RUN_KIND and calls[0]["lane"] == LANE
    assert report["schema_version"] == REPORT_SCHEMA
    assert report["status"] == "passed"
    assert report["model_calls"] == 1
    assert report["content_scope"] == {
        "synthetic_fixed_prompt_only": True,
        "candidate_artifacts_read": 0,
        "source_artifacts_read": 0,
        "evaluation_artifacts_read": 0,
    }
    assert report["controls"]["response_schema_sha256"] == canonical_sha256(
        _response_schema("test_author", "v5")
    )
    assert report["controls"]["config_sha256"] == canonical_sha256(config)
    assert report["controls"]["config_file_sha256"] == "f" * 64
    assert report["raw_run_sha256"] == canonical_sha256(report["raw_run"])
    assert report["response_sha256"] == canonical_sha256(report["response"])
    body = dict(report); claimed = body.pop("report_sha256")
    assert claimed == canonical_sha256(body)
    assert validate_v5_live_schema_admission_smoke_report(
        report, config, "f" * 64, "codex-cli 1.2.3",
    ) is report

    tampered = copy.deepcopy(report)
    tampered["controls"]["response_schema_sha256"] = "0" * 64
    tampered.pop("report_sha256")
    tampered["report_sha256"] = canonical_sha256(tampered)
    with pytest.raises(ValueError, match="invalid or unbound"):
        validate_v5_live_schema_admission_smoke_report(
            tampered, config, "f" * 64, "codex-cli 1.2.3",
        )


@pytest.mark.parametrize(
    ("mutation", "reason"),
    [
        (lambda run: run.update(returncode=1), "exit zero"),
        (lambda run: run.update(usage=None), "terminal usage"),
        (lambda run: run.update(events=[]), "agent response"),
        (
            lambda run: run.update(disallowed_tool_item_types=["command_execution"]),
            "disallowed tool",
        ),
        (lambda run: run.update(timed_out=True), "timed out"),
    ],
)
def test_live_schema_smoke_fails_closed_on_run_contract(mutation, reason: str) -> None:
    run = valid_run(); mutation(run)
    calls = []

    def invoke(*_args):
        calls.append(1)
        return valid_response(), run

    report = run_v5_live_schema_admission_smoke(
        {"model": "fixture"}, "a" * 64, "codex-cli 1", invoker=invoke,
    )
    assert calls == [1]
    assert report["status"] == "failed"
    assert report["failure"]["classification"] == "run-contract-failure"
    assert reason in report["failure"]["reason"]
    assert report["raw_run_sha256"] == canonical_sha256(run)


@pytest.mark.parametrize("response", [
    {"primary_discrimination": valid_response()["primary_discrimination"]},
    {
        **valid_response(),
        "primary_discrimination": {
            **valid_response()["primary_discrimination"],
            "case_ids": ["duplicate", "duplicate"],
        },
    },
])
def test_live_schema_smoke_rejects_invalid_or_duplicate_application_payload(response: dict) -> None:
    report = run_v5_live_schema_admission_smoke(
        {"model": "fixture"}, "b" * 64, "codex-cli 1",
        invoker=lambda *_args: (response, valid_run(response)),
    )
    assert report["status"] == "failed"
    assert report["failure"]["classification"] == "application-contract-failure"
    assert report["response_sha256"] == canonical_sha256(response)


def test_live_schema_smoke_seals_raw_invocation_failure() -> None:
    run = valid_run(); run["returncode"] = 1

    def invoke(*_args):
        raise CodexInvocationFailure("provider rejected schema", run)

    report = run_v5_live_schema_admission_smoke(
        {"model": "fixture"}, "c" * 64, "codex-cli 1", invoker=invoke,
    )
    assert report["status"] == "failed"
    assert report["failure"] == {
        "classification": "invocation-failure",
        "exception_type": "CodexInvocationFailure",
        "reason": "provider rejected schema",
    }
    assert report["raw_run"] == run
    assert report["raw_run_sha256"] == canonical_sha256(run)
