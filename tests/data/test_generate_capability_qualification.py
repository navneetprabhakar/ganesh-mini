import hashlib
import json
import time
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.data.generate_capability_qualification import (
    architect_prompt,
    generate_batch,
    load_queue,
    qualification_metadata,
    select_batch,
    teacher_shards,
)


def row(identifier: str, lane: str = "python", capability: str = "parsing_and_encoding") -> dict:
    return {
        "schema_version": "ganesh-mini-capability-qualification-draft/v1",
        "id": identifier,
        "cell_id": f"{capability}/{lane}/generation",
        "primary_capability": capability,
        "primary_capability_definition": "parse a bounded structured representation",
        "assigned_cross_cutting_dimension": "malformed_input",
        "lane": lane,
        "task_type": "generation",
        "source_queue_id": f"source-{identifier}",
        "source": {
            "dataset": "training-only", "revision": "abc", "record_id": identifier,
            "source_record_sha256": "1" * 64,
        },
        "stimulus": "Build an unrelated parser with an external framework.",
    }


def test_prompt_binds_capability_dimension_runtime_and_lineage_without_old_boilerplate() -> None:
    prompt = architect_prompt("python", [row("q-1")])
    assert "parsing_and_encoding" in prompt
    assert "malformed_input" in prompt
    assert "python" in prompt and "solution.py" in prompt
    assert '"dataset":"training-only"' in prompt
    assert '"record_id":"q-1"' in prompt
    assert "Do not turn the task into generic" in prompt
    assert "Explicitly define empty, malformed, boundary, ordering, aliasing, and mutation" not in prompt


def test_select_batch_is_lane_local_and_bounded() -> None:
    rows = [row(f"py-{index}") for index in range(12)] + [row("go-0", lane="go")]
    assert [item["id"] for item in select_batch(rows, "python", 1, 10)] == ["py-10", "py-11"]
    with pytest.raises(ValueError, match="batch-size"):
        select_batch(rows, "python", 0, 11)


def test_metadata_seals_assignment_and_source_lineage() -> None:
    metadata = qualification_metadata(row("q-1"))
    seal = metadata.pop("assignment_sha256")
    encoded = json.dumps(metadata, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    assert seal == hashlib.sha256(encoded).hexdigest()
    assert metadata["source_identity"] == {
        "dataset": "training-only", "revision": "abc", "record_id": "q-1",
    }


def test_load_queue_fails_when_queue_hash_differs_from_sealed_manifest(tmp_path: Path) -> None:
    queue_path = tmp_path / "queue.jsonl"
    queue_path.write_text(json.dumps(row("q-1")) + "\n", encoding="utf-8")
    manifest = {
        "schema_version": "ganesh-mini-capability-qualification-queue-manifest/v1",
        "status": "ready-for-isolated-teacher-qualification",
        "records": 240, "cells": 120, "unique_source_identities": 240,
        "selection": {"evaluation_surfaces_read": 0}, "queue_sha256": "0" * 64,
    }
    raw = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    manifest["manifest_sha256"] = hashlib.sha256(raw).hexdigest()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="sealed contract"):
        load_queue(queue_path, manifest_path)


def test_repository_qualification_queue_matches_its_sealed_manifest() -> None:
    root = Path(__file__).resolve().parents[2]
    rows, manifest = load_queue(
        root / "datasets/cache/capability-stratified-v2/qualification-queue.jsonl",
        root / "measurement/gate2/capability-stratified-v2/qualification-queue-manifest.json",
    )
    assert len(rows) == 240
    assert manifest["queue_sha256"] == "0cf1a51055d58c4ae0c454aad0f6b8e844cae27517a16516f59bbe428a967c9f"


def test_teacher_shards_and_parallel_results_preserve_queue_order() -> None:
    rows = [row(str(index)) for index in range(4)]
    assert [[item["id"] for item in shard] for shard in teacher_shards(rows, 2)] == [["0", "1"], ["2", "3"]]

    def fake_generate(shard, _config, _codex_bin):
        if shard[0]["id"] == "0":
            time.sleep(0.02)
        return ([{"id": item["id"]} for item in shard], [{"first": shard[0]["id"]}], None)

    with patch("scripts.data.generate_capability_qualification.generate_shard", side_effect=fake_generate):
        candidates, runs, failures = generate_batch(rows, {}, "codex", teacher_workers=2)
    assert [item["id"] for item in candidates] == ["0", "1", "2", "3"]
    assert runs == [{"first": "0"}, {"first": "2"}]
    assert failures == []


def test_any_shard_failure_discards_partial_candidates() -> None:
    rows = [row(str(index)) for index in range(2)]

    def fake_generate(shard, _config, _codex_bin):
        if shard[0]["id"] == "1":
            return [], [], "teacher failed"
        return [{"id": "0"}], [], None

    with patch("scripts.data.generate_capability_qualification.generate_shard", side_effect=fake_generate):
        candidates, _runs, failures = generate_batch(rows, {}, "codex", teacher_workers=2)
    assert candidates == []
    assert failures == [{"lane": "python", "shard": "1", "reason": "teacher failed"}]
