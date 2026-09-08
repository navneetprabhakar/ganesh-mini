import json
from pathlib import Path

import pytest

from scripts.data.verify_versioned_recovery import execute_record, outcome, race_runtime


def result(codes, commands=None, **kwargs):
    return {"exit_codes": codes, "commands": commands or [["run"]], "timed_out": False,
            "stdout": "", "stderr": "", **kwargs}


@pytest.mark.parametrize("value,expected", [
    (result([0]), "passed"),
    (result([1]), "behavioral-failure-requires-review"),
    (result([1], [["compile"], ["run"]]), "compile-or-load-failure-not-semantic-proof"),
    (result([1], stderr="SyntaxError: invalid syntax"), "compile-or-load-failure-not-semantic-proof"),
    (result([], timed_out=True), "timeout-not-semantic-proof"),
    (result([125]), "infrastructure-failure"),
])
def test_outcome_does_not_promote_compile_timeout_or_host_errors(value, expected):
    assert outcome(value) == expected


def test_all_program_evidence_survives_reference_failure(tmp_path):
    candidate = {"id": "derived", "messages": [{}, {"content": "REF"}],
                 "verification_task": {"validation": {"known_bad": [{"code": "BAD"}]}}}
    parent = {"messages": [{}, {"content": "PARENT"}]}
    calls = []
    def verifier(task, code, runtime):
        calls.append(code)
        return result([1] if code == "REF" else [0])
    summary = execute_record(candidate, parent, Path("unused"), tmp_path, verifier)
    assert calls == ["REF", "BAD", "PARENT"]
    assert not summary["directionality_passed"]
    assert len(list(tmp_path.glob("*.json"))) == 4
    assert json.loads((tmp_path / "derived-reference.json").read_text())["code"] == "REF"
    with pytest.raises(FileExistsError):
        execute_record(candidate, parent, Path("unused"), tmp_path, verifier)


def test_exception_evidence_is_not_known_bad_success(tmp_path):
    candidate = {"id": "derived", "messages": [{}, {"content": "REF"}],
                 "verification_task": {"validation": {"known_bad": []}}}
    parent = {"messages": [{}, {"content": "PARENT"}]}
    def verifier(*args):
        raise RuntimeError("host unavailable")
    summary = execute_record(candidate, parent, Path("unused"), tmp_path, verifier)
    assert not summary["directionality_passed"]
    assert summary["results"][0]["outcome"] == "verifier-exception-not-behavioral-proof"


def test_race_contract_keeps_image_and_original_config():
    original = {"runtimes": {"go-1.22.12": {"commands": [["go", "test", "./..."]], "image_id": "pinned"}}}
    derived = race_runtime(original)
    assert derived["runtimes"]["go-1.22.12"]["commands"] == [["go", "test", "-race", "./..."]]
    assert derived["runtimes"]["go-1.22.12"]["image_id"] == "pinned"
    assert original["runtimes"]["go-1.22.12"]["commands"] == [["go", "test", "./..."]]
