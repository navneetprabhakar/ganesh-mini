import time
from unittest.mock import patch

from scripts.data.generate_expansion_source_batch import (
    generate_batch,
    select_batch,
    select_custom_batch,
    select_planned_batch,
    source_architect_prompt,
    teacher_shards,
)


def draft(identifier: str, lane: str = "python", task_type: str = "generation") -> dict:
    return {
        "schema_version": "ganesh-mini-expansion-draft/v1", "id": identifier,
        "lane": lane, "task_type": task_type, "stimulus": "an untrusted source task",
        "source": {"dataset": "x"},
    }


def test_select_batch_filters_before_offset() -> None:
    rows = [draft("go", "go"), draft("py-1"), draft("py-2"), draft("repair", task_type="repair")]
    assert [row["id"] for row in select_batch(rows, "python", "generation", 1, 1)] == ["py-2"]


def test_planned_batch_uses_six_generation_and_four_repair() -> None:
    rows = [draft(f"g-{index}") for index in range(12)] + [draft(f"r-{index}", task_type="repair") for index in range(8)]
    selected = select_planned_batch(rows, "python", 1)
    assert [row["id"] for row in selected] == [
        "g-6", "g-7", "g-8", "g-9", "g-10", "g-11", "r-4", "r-5", "r-6", "r-7",
    ]


def test_custom_batch_can_stop_a_completed_stratum() -> None:
    rows = [draft(f"g-{index}") for index in range(12)] + [draft(f"r-{index}", task_type="repair") for index in range(8)]
    assert [row["id"] for row in select_custom_batch(rows, "python", 6, 4, 8, 0)] == [
        "g-6", "g-7", "g-8", "g-9",
    ]


def test_source_prompt_demands_original_self_contained_transformation() -> None:
    prompt = source_architect_prompt("python", [draft("x", task_type="repair")])
    assert "untrusted source material" in prompt
    assert "Do not copy its wording" in prompt
    assert "embed the complete known-bad source" in prompt
    assert "independent" not in prompt.casefold()  # architect is not told about downstream test implementation


def test_teacher_shards_are_balanced_contiguous_and_order_preserving() -> None:
    rows = [{"id": str(index)} for index in range(10)]
    shards = teacher_shards(rows, 2)
    assert [[row["id"] for row in shard] for shard in shards] == [
        ["0", "1", "2", "3", "4"],
        ["5", "6", "7", "8", "9"],
    ]
    assert [row for shard in shards for row in shard] == rows


def test_parallel_teacher_shards_reassemble_in_original_order() -> None:
    rows = [draft(str(index)) for index in range(4)]

    def fake_generate(shard, _config, _codex_bin):
        if shard[0]["id"] == "0":
            time.sleep(0.02)
        return ([{"id": row["id"]} for row in shard], [{"first": shard[0]["id"]}], None)

    with patch("scripts.data.generate_expansion_source_batch.generate_shard", side_effect=fake_generate):
        candidates, runs, failures = generate_batch(rows, {}, "codex", teacher_workers=2)
    assert [row["id"] for row in candidates] == ["0", "1", "2", "3"]
    assert runs == [{"first": "0"}, {"first": "2"}]
    assert failures == []
