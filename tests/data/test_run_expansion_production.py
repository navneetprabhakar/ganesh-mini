import json

import pytest

from scripts.data.run_expansion_production import (
    Corpus, frozen_targets, recovery_requires_generation, selection, sha256_bytes, unfinished_batch,
    verify_reusable_candidates,
    verifier_infrastructure_rejections,
)


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


def test_unfinished_batch_requires_at_most_one_per_lane() -> None:
    entry = {"kind": "production", "lane": "java", "name": "java-1", "status": "failed"}
    state = {"batches": [entry]}
    assert unfinished_batch(state, "java") is entry
    state["batches"].append({**entry, "name": "java-2", "status": "running"})
    with pytest.raises(ValueError, match="multiple unfinished"):
        unfinished_batch(state, "java")


def test_reusable_candidates_are_bound_to_hash_and_selection(tmp_path) -> None:
    candidate = tmp_path / "candidates.jsonl"
    candidate.write_bytes(b'{"id":"one"}\n')
    plan = {"generation_start": 6, "generation_count": 6, "repair_start": 4, "repair_count": 4}
    evidence = tmp_path / "teacher-evidence.json"
    evidence.write_text(json.dumps({
        "candidate_output_sha256": sha256_bytes(candidate.read_bytes()),
        "selection": {"lane": "java", **plan},
    }))
    verify_reusable_candidates(candidate, evidence, "java", plan)
    candidate.write_bytes(b'{"id":"changed"}\n')
    with pytest.raises(ValueError, match="candidate hash"):
        verify_reusable_candidates(candidate, evidence, "java", plan)


def test_empty_interrupted_batch_regenerates_same_recorded_selection(tmp_path) -> None:
    batch = tmp_path / "batch"
    batch.mkdir()
    plan = {"generation_start": 6, "generation_count": 6, "repair_start": 4, "repair_count": 4}
    assert recovery_requires_generation(
        batch, batch / "candidates.jsonl", batch / "teacher-evidence.json", "java", plan,
    )


def test_partial_or_unsealed_interrupted_batch_fails_closed(tmp_path) -> None:
    batch = tmp_path / "batch"
    batch.mkdir()
    plan = {"generation_start": 6, "generation_count": 6, "repair_start": 4, "repair_count": 4}
    candidate = batch / "candidates.jsonl"
    evidence = batch / "teacher-evidence.json"
    candidate.write_text('{"id":"one"}\n')
    with pytest.raises(ValueError, match="only one"):
        recovery_requires_generation(batch, candidate, evidence, "java", plan)
    candidate.unlink()
    (batch / "unexpected.json").write_text("{}")
    with pytest.raises(ValueError, match="unsealed artifacts"):
        recovery_requires_generation(batch, candidate, evidence, "java", plan)


def test_infrastructure_rejections_are_separated_from_teacher_repairs() -> None:
    report = {"rejected": [
        {"id": "infra", "reason": "known-bad verifier infrastructure failure: container runtime exit code [125]"},
        {"id": "repair", "reason": "reference solution failed behavioral verification"},
    ]}
    assert [row["id"] for row in verifier_infrastructure_rejections(report)] == ["infra"]
