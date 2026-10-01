from __future__ import annotations

import hashlib
import json
from collections import Counter

import pytest

from scripts.data import select_capability_broad_replay as replay
from scripts.data.build_capability_corpus_plan import CAPABILITIES, LANES, TASK_TYPES, canonical_sha256


def encoded(rows: list[dict]) -> bytes:
    return b"".join(json.dumps(row, sort_keys=True).encode() + b"\n" for row in rows)


def source(identifier: str) -> dict:
    return {
        "dataset": "synthetic", "revision": "fixed", "record_id": identifier,
        "source_record_sha256": hashlib.sha256(identifier.encode()).hexdigest(),
        "license": "CC-BY-4.0", "uri": "synthetic://source",
    }


def rights() -> dict:
    return {key: True for key in replay.RIGHTS}


@pytest.fixture
def inputs(monkeypatch: pytest.MonkeyPatch) -> tuple[bytes, bytes, dict]:
    capability = [
        {
            "id": f"cap-{capability}-{lane}-{task_type}-{position}",
            "cell_id": f"{capability}/{lane}/{task_type}", "lane": lane, "task_type": task_type,
            "source": source(f"cap-{capability}-{lane}-{task_type}-{position}"), "rights": rights(),
        }
        for capability in CAPABILITIES for lane in LANES for task_type in TASK_TYPES
        for position in range(6)
    ]
    previous = [
        {
            "id": f"prior-{lane}-{task_type}-{position}", "lane": lane, "task_type": task_type,
            **({"lineage": source(f"prior-{lane}-{task_type}-{position}")} if position == 0 else
               {"source": source(f"prior-{lane}-{task_type}-{position}")}),
            "rights": rights(), "messages": [{"role": "user", "content": "synthetic"}],
            "verification": {"status": "passed"},
        }
        for lane in LANES for task_type in TASK_TYPES for position in range(269)
    ][:3225]
    prior_bytes, capability_bytes = encoded(previous), encoded(capability)
    monkeypatch.setattr(replay, "PRIOR_CORPUS_SHA256", hashlib.sha256(prior_bytes).hexdigest())
    manifest = {
        "schema_version": "ganesh-mini-gate3-capability-720-seal/v1", "status": "passed",
        "plan_sha256": replay.PLAN_SHA256, "records": 720,
        "capability_rows_sha256": hashlib.sha256(capability_bytes).hexdigest(),
        "evaluation_artifacts_read": 0,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    return prior_bytes, capability_bytes, manifest


def test_selects_exact_byte_preserved_and_deterministic_180(inputs: tuple[bytes, bytes, dict]) -> None:
    prior, capability, manifest = inputs
    selected, report = replay.select(prior, capability, manifest)
    repeated, repeated_report = replay.select(prior, capability, manifest)
    assert (selected, report) == (repeated, repeated_report)
    original_lines = set(prior.splitlines(keepends=True))
    assert all(line in original_lines for line in selected.splitlines(keepends=True))
    rows = [json.loads(line) for line in selected.splitlines()]
    assert Counter((row["lane"], row["task_type"]) for row in rows) == {
        (lane, task_type): 15 for lane in LANES for task_type in TASK_TYPES
    }
    assert len({row["id"] for row in rows}) == 180
    assert len({replay.source_key(row) for row in rows}) == 180
    assert report["replay_jsonl_sha256"] == hashlib.sha256(selected).hexdigest()
    assert report["manifest_sha256"] == canonical_sha256({k: v for k, v in report.items() if k != "manifest_sha256"})


def test_requires_passed_720_row_seal(inputs: tuple[bytes, bytes, dict]) -> None:
    prior, capability, manifest = inputs
    bad = {**manifest, "status": "running"}
    bad["manifest_sha256"] = canonical_sha256({k: v for k, v in bad.items() if k != "manifest_sha256"})
    with pytest.raises(ValueError, match="sealed 720-row admission"):
        replay.select(prior, capability, bad)
    with pytest.raises(ValueError, match="sealed 720-row admission"):
        replay.select(prior, capability + b"\n", manifest)


def test_rejects_capability_source_reuse(inputs: tuple[bytes, bytes, dict]) -> None:
    prior, capability, manifest = inputs
    rows = [json.loads(line) for line in capability.splitlines()]
    rows[1]["source"] = rows[0]["source"]
    changed = encoded(rows)
    manifest = {**manifest, "capability_rows_sha256": hashlib.sha256(changed).hexdigest()}
    manifest["manifest_sha256"] = canonical_sha256({k: v for k, v in manifest.items() if k != "manifest_sha256"})
    with pytest.raises(ValueError, match="reuses a source"):
        replay.select(prior, changed, manifest)


def test_rejects_prior_hash_drift(inputs: tuple[bytes, bytes, dict]) -> None:
    prior, capability, manifest = inputs
    with pytest.raises(ValueError, match="frozen prior corpus hash differs"):
        replay.select(prior + b"\n", capability, manifest)


def test_skips_prior_rows_sharing_a_capability_source(
    inputs: tuple[bytes, bytes, dict], monkeypatch: pytest.MonkeyPatch,
) -> None:
    prior, capability, manifest = inputs
    rows = [json.loads(line) for line in prior.splitlines()]
    capability_source = json.loads(capability.splitlines()[0])["source"]
    rows[0]["lineage"] = capability_source
    changed = encoded(rows)
    monkeypatch.setattr(replay, "PRIOR_CORPUS_SHA256", hashlib.sha256(changed).hexdigest())
    selected, _ = replay.select(changed, capability, manifest)
    assert rows[0]["id"] not in {json.loads(line)["id"] for line in selected.splitlines()}


def test_rejects_unapproved_prior_rights(
    inputs: tuple[bytes, bytes, dict], monkeypatch: pytest.MonkeyPatch,
) -> None:
    prior, capability, manifest = inputs
    rows = [json.loads(line) for line in prior.splitlines()]
    rows[0]["rights"]["model_training"] = False
    changed = encoded(rows)
    monkeypatch.setattr(replay, "PRIOR_CORPUS_SHA256", hashlib.sha256(changed).hexdigest())
    with pytest.raises(ValueError, match="incomplete approved rights"):
        replay.select(changed, capability, manifest)


def test_rejects_conflicting_prior_lineage(
    inputs: tuple[bytes, bytes, dict], monkeypatch: pytest.MonkeyPatch,
) -> None:
    prior, capability, manifest = inputs
    rows = [json.loads(line) for line in prior.splitlines()]
    rows[0]["source"] = source("different")
    changed = encoded(rows)
    monkeypatch.setattr(replay, "PRIOR_CORPUS_SHA256", hashlib.sha256(changed).hexdigest())
    with pytest.raises(ValueError, match="conflicting source and lineage"):
        replay.select(changed, capability, manifest)


def test_rejects_changed_capability_assignment_source(inputs: tuple[bytes, bytes, dict]) -> None:
    prior, capability, manifest = inputs
    rows = [json.loads(line) for line in capability.splitlines()]
    rows[0]["qualification_assignment"] = {
        "source_identity": {"dataset": "different", "revision": "fixed", "record_id": "different"},
        "source_record_sha256": rows[0]["source"]["source_record_sha256"],
    }
    changed = encoded(rows)
    manifest = {**manifest, "capability_rows_sha256": hashlib.sha256(changed).hexdigest()}
    manifest["manifest_sha256"] = canonical_sha256({k: v for k, v in manifest.items() if k != "manifest_sha256"})
    with pytest.raises(ValueError, match="qualification source identity differs"):
        replay.select(prior, changed, manifest)
