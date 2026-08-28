from scripts.data.restore_expansion_repair_lineage import restore


def row(identifier: str, answer: str = "old") -> dict:
    return {
        "id": identifier, "messages": [{"content": "p"}, {"content": answer}],
        "source": {"dataset": "pinned", "transformation": "source transform"},
    }


def test_restore_changes_only_rejected_row_source() -> None:
    original = [row("accepted"), row("rejected")]
    repaired = [row("accepted"), {**row("rejected", "new"), "source": {"dataset": "codex", "transformation": "wrong"}}]
    report = {"rejected": [{"id": "rejected", "reason": "reference solution failed behavioral verification"}]}
    output = restore(original, repaired, report)
    assert output[0] == original[0]
    assert output[1]["messages"][1]["content"] == "new"
    assert output[1]["source"] == {
        "dataset": "pinned", "transformation": "source transform; reference corrected against independent tests",
    }
