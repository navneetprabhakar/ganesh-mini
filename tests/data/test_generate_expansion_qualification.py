import json
from pathlib import Path

from scripts.data.generate_expansion_qualification import (
    ARCHITECT_SCHEMA,
    build_candidate,
    codex_command,
    parse_events,
    task_specs,
    critic_test_prompt,
)
from scripts.eval.contracts import validate_task


def teacher_config() -> dict:
    return {
        "model": "gpt-5.6-sol",
        "reasoning_effort": "medium",
        "service_tier": "priority",
    }


def test_task_specs_preserve_sixty_forty_split() -> None:
    specs = task_specs("python", 10)
    assert [item["task_type"] for item in specs].count("generation") == 6
    assert [item["task_type"] for item in specs].count("repair") == 4
    assert len({item["id"] for item in specs}) == 10


def test_codex_command_is_ephemeral_isolated_and_schema_constrained(tmp_path: Path) -> None:
    command = codex_command(
        "codex", teacher_config(), ARCHITECT_SCHEMA, tmp_path / "out.json", tmp_path, "prompt",
    )
    assert command[:2] == ["codex", "exec"]
    assert "--ephemeral" in command
    assert "--ignore-user-config" in command
    assert "--ignore-rules" in command
    assert command[command.index("--sandbox") + 1] == "read-only"
    assert command[command.index("-m") + 1] == "gpt-5.6-sol"
    assert command[command.index("--output-schema") + 1] == str(ARCHITECT_SCHEMA.resolve())
    assert command[command.index("-C") + 1] == str(tmp_path.resolve())
    assert "--dangerously-bypass-approvals-and-sandbox" not in command
    assert command[-1] == "prompt"


def test_parse_events_extracts_usage_and_rejectable_tools() -> None:
    stdout = "\n".join([
        json.dumps({"type": "item.completed", "item": {"type": "agent_message"}}),
        json.dumps({"type": "item.started", "item": {"type": "command_execution"}}),
        json.dumps({"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 2}}),
    ])
    events, usage, disallowed = parse_events(stdout)
    assert len(events) == 3
    assert usage == {"input_tokens": 10, "output_tokens": 2}
    assert disallowed == ["command_execution"]


def test_parse_events_accepts_only_the_specific_completed_transport_fallback() -> None:
    stdout = "\n".join([
        json.dumps({"type": "item.completed", "item": {
            "type": "error",
            "message": "Falling back from WebSockets to HTTPS transport. unexpected status 403 Forbidden",
        }}),
        json.dumps({"type": "turn.completed", "usage": {"input_tokens": 1}}),
    ])
    _, usage, disallowed = parse_events(stdout)
    assert usage == {"input_tokens": 1}
    assert disallowed == []

    unrelated = json.dumps({"type": "item.completed", "item": {
        "type": "error", "message": "Tool execution failed",
    }})
    _, _, disallowed = parse_events(unrelated)
    assert disallowed == ["error"]


def test_test_critic_never_receives_reference_or_known_bad() -> None:
    architecture = [{
        "id": "x", "problem": "Implement x.", "reference_code": "SECRET_REFERENCE",
        "known_bad_code": "SECRET_BAD", "known_bad_label": "secret label",
    }]
    prompt = critic_test_prompt("python", architecture, [{"id": "x", "test_code": "assert True"}])
    assert "Implement x." in prompt
    assert "assert True" in prompt
    assert "SECRET_REFERENCE" not in prompt
    assert "SECRET_BAD" not in prompt


def test_build_candidate_creates_valid_training_admission_task() -> None:
    architecture = {
        "id": "codex-v1-python-generation-01",
        "problem": "Implement add_one.",
        "reference_code": "def add_one(x):\n    return x + 1",
        "known_bad_code": "def add_one(x):\n    return x",
        "known_bad_label": "missing increment",
    }
    candidate = build_candidate(
        "python", architecture["id"], "generation", architecture,
        "from solution import add_one\nassert add_one(1) == 2",
    )
    validate_task({**candidate["verification_task"], "surface": "synthetic_harness"})
    assert candidate["verification_task"]["surface"] == "training_admission"
    assert candidate["source"]["dataset"] == "codex-cli/gpt-5.6-sol"
    assert candidate["source"]["license"] == "user-owned-output"
    assert candidate["test_origin"] == "independent_teacher"
    assert candidate["verification_task"]["validation"]["reference"]["code"].endswith("\n")


def test_go_candidate_includes_module_support_file() -> None:
    architecture = {
        "id": "codex-v1-go-generation-01",
        "problem": "Implement Add.",
        "reference_code": "package solution\nfunc Add(a, b int) int { return a + b }",
        "known_bad_code": "package solution\nfunc Add(a, b int) int { return a - b }",
        "known_bad_label": "subtracts",
    }
    candidate = build_candidate(
        "go", architecture["id"], "generation", architecture,
        "package solution\nimport \"testing\"\nfunc TestAdd(t *testing.T) { if Add(1, 2) != 3 { t.Fail() } }",
    )
    files = candidate["verification_task"]["files"]
    assert [(item["path"], item["role"]) for item in files] == [
        ("go.mod", "support"), ("solution_test.go", "test"),
    ]
