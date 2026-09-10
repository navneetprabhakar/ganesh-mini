from scripts.eval.analyze_lane_stratified_trajectory import archetype, candidate_point, transition


def task(passed: bool) -> dict:
    return {
        "task": {"language": "go"},
        "extraction": {"extracted_code_sha256": str(passed)},
        "verification": {"result": {"passed": passed}},
    }


def test_transition_reports_exact_gains_and_losses() -> None:
    before = {"a": task(False), "b": task(True), "c": task(False)}
    after = {"a": task(True), "b": task(False), "c": task(False)}
    assert transition(before, after) == {"gains": ["a"], "losses": ["b"]}


def test_archetype_removes_only_the_lane_prefix() -> None:
    assert archetype("dev-t1-typescript-collapse-runs", "typescript") == "collapse-runs"


def test_candidate_point_uses_paired_passes_without_guessing_failure_cause() -> None:
    base = {"a": task(False), "b": task(True)}
    candidate = {"a": task(True), "b": task(False)}
    result = candidate_point("p", candidate, base, run_sha256="a" * 64, seen_tokens=10)
    assert result["gains_vs_base"] == ["a"]
    assert result["losses_vs_base"] == ["b"]
    assert "failure_categories" not in result
