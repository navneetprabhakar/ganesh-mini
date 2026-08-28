from scripts.data.run_expansion_production import Corpus, frozen_targets, selection


def targets() -> dict:
    return {lane: {"generation": 6, "repair": 4} for lane in ("go", "java", "javascript", "typescript", "python", "rust")}


def admitted(identifier: str, lane: str = "python", task_type: str = "generation", prompt: str | None = None) -> dict:
    text = prompt or f"Implement {identifier} with explicit behavior and deterministic output."
    return {
        "id": identifier, "lane": lane, "task_type": task_type,
        "messages": [{"content": text}, {"content": "answer"}],
        "content_hashes": {"conversation_sha256": identifier.rjust(64, "0")[-64:]},
    }


def test_frozen_targets_split_each_lane_sixty_forty() -> None:
    config = {"lane_targets": {lane: 10 for lane in targets()}}
    assert frozen_targets(config) == targets()


def test_selection_stops_completed_stratum() -> None:
    corpus = Corpus([], targets())
    for index in range(4):
        assert corpus.add(admitted(f"r{index}", task_type="repair")) is None
    plan = selection(corpus, "python", {"generation": 2, "repair": 4}, {"generation": 20, "repair": 20})
    assert plan == {"generation_start": 2, "generation_count": 6, "repair_start": 4, "repair_count": 0}


def test_corpus_rejects_duplicate_and_quota_surplus() -> None:
    corpus = Corpus([], targets())
    first = admitted("1")
    assert corpus.add(first) is None
    assert corpus.add(admitted("2", prompt=first["messages"][0]["content"])) is not None
    for index in range(2, 7):
        assert corpus.add(admitted(str(index))) is None
    assert corpus.add(admitted("7")) == "quota already met"
