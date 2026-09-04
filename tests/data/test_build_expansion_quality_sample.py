from __future__ import annotations

from scripts.data.build_expansion_quality_sample import allocate, build_sample, correction_history


def row(index: int, lane: str, source: str, task_type: str, corrected: bool = False) -> dict:
    suffix = "; reference corrected against independent tests" if corrected else ""
    return {
        "id": f"row-{index:03d}", "lane": lane, "task_type": task_type,
        "lineage": {"dataset": source, "transformation": f"drafted{suffix}"},
    }


def test_allocation_covers_every_stratum_and_has_exact_size() -> None:
    populations = {("go", "a", "generation", "first_pass"): 90, ("go", "a", "generation", "corrected"): 10}
    result = allocate(populations, 20)
    assert sum(result.values()) == 20
    assert result[("go", "a", "generation", "first_pass")] == 18
    assert result[("go", "a", "generation", "corrected")] == 2


def test_sample_is_deterministic_and_stratified() -> None:
    rows = [row(index, "go", "source-a", "generation", index % 7 == 0) for index in range(50)]
    rows += [row(index + 50, "python", "source-b", "repair", index % 5 == 0) for index in range(50)]
    first, first_report = build_sample(rows, "a" * 64, 20)
    second, second_report = build_sample(list(reversed(rows)), "a" * 64, 20)
    assert [item["id"] for item in first] == [item["id"] for item in second]
    assert first_report == second_report
    assert len(first) == 20
    assert {item["rejection_history"] for item in first_report["records"]} == {"first_pass", "corrected"}
    assert {item["lane"] for item in first_report["records"]} == {"go", "python"}


def test_correction_history_comes_from_preserved_lineage() -> None:
    assert correction_history(row(1, "go", "a", "repair")) == "first_pass"
    assert correction_history(row(2, "go", "a", "repair", corrected=True)) == "corrected"
