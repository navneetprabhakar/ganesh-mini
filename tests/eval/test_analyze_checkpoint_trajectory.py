from scripts.eval.analyze_checkpoint_trajectory import counts, outcome, point


def task(task_id: str, language: str, passed: bool, code: str, *, exit_code: int = 0) -> dict:
    return {
        "task": {"task_id": task_id, "language": language},
        "extraction": {"extracted_code_sha256": code},
        "verification": {"result": {"passed": passed, "verifier": {"timed_out": False, "exit_codes": [exit_code]}}},
    }


def test_outcome_distinguishes_compile_behavior_and_timeout() -> None:
    assert outcome(task("a", "go", True, "1")) == "passed"
    assert outcome(task("a", "go", False, "1", exit_code=2)) == "compile-or-load-failure"
    assert outcome(task("a", "go", False, "1", exit_code=0)) == "behavioral-test-failure"
    value = task("a", "go", False, "1")
    value["verification"]["result"]["verifier"]["timed_out"] = True
    assert outcome(value) == "verifier-timeout"


def test_point_reports_paired_transitions_and_family_counts() -> None:
    base = {
        "g": task("g", "go", False, "base-g", exit_code=1),
        "j": task("j", "javascript", True, "base-j"),
        "t": task("t", "typescript", False, "base-t"),
    }
    candidate = {
        "g": task("g", "go", True, "new-g"),
        "j": task("j", "javascript", False, "new-j"),
        "t": task("t", "typescript", True, "base-t"),
    }
    lanes, families = counts(candidate)
    assert lanes["go"] == 1
    assert families["javascript_typescript"] == 1
    result = point("checkpoint", candidate, base, run_sha256="a" * 64, seen_tokens=10)
    assert result["passed"] == 2
    assert result["task_transitions_vs_base"] == {"fail_to_pass": 2, "pass_to_fail": 1}
    assert result["changed_extracted_code_vs_base"] == 2
