import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.build_cross_language_repair_extension import (
    DATASET,
    DERIVATION_KIND,
    SEED,
    build,
    canonical_json,
)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))


def fixture(tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    raw = [
        {"language": "JavaScript", "instruction": "  preserve JS bytes  \n"},
        {"language": "Java", "instruction": "preserve Java bytes"},
        {"language": "JavaScript", "instruction": "already used"},
        {"language": "Python", "instruction": "not selected"},
    ]
    snapshot = tmp_path / "McEval-Instruct.json"
    snapshot.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    metadata = {
        "dataset": DATASET, "uri": "https://example.test/mceval", "revision": "pinned-revision",
        "sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(), "license": "CC-BY-SA-4.0",
        "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
    }
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"sources": {"mceval": metadata}}), encoding="utf-8")
    used_source = {
        **{key: metadata[key] for key in ("dataset", "uri", "revision", "license", "license_uri")},
        "record_id": "row-00002", "source_record_sha256": hashlib.sha256(canonical_json(raw[2])).hexdigest(),
        "transformation": "old",
    }
    current = tmp_path / "current.jsonl"
    current_row = {
        "id": "current-repair", "lane": "javascript", "task_type": "repair",
        "schema_version": "existing/v1", "stimulus": "already used", "source": used_source,
    }
    write_jsonl(current, [current_row])
    prior = tmp_path / "prior.jsonl"; write_jsonl(prior, [])
    v2 = tmp_path / "v2.jsonl"; write_jsonl(v2, [])
    evidence = tmp_path / "evidence.json"
    evidence.write_text(json.dumps({"failures": [{"source_queue_ids": ["current-repair"]}]}), encoding="utf-8")
    return config, snapshot, prior, v2, current, evidence, raw, current_row


def test_builds_two_content_blind_pools_and_preserves_raw_stimulus(tmp_path: Path) -> None:
    config, snapshot, prior, v2, current, evidence, raw, current_row = fixture(tmp_path)
    rows, manifest, union = build(config, snapshot, prior, [v2], current, [evidence])

    assert len(rows) == 2
    by_target = {row["target_lane"]: row for row in rows}
    assert by_target["typescript"]["stimulus"] == raw[0]["instruction"]
    assert by_target["javascript"]["stimulus"] == raw[1]["instruction"]
    assert by_target["typescript"]["source_language"] == "javascript"
    assert by_target["javascript"]["source_language"] == "java"
    assert all(row["lane"] == row["target_lane"] and row["task_type"] == "repair" for row in rows)
    assert all(row["original_role"] == "generation" for row in rows)
    assert all(row["derivation_kind"] == DERIVATION_KIND for row in rows)
    assert all("Content-blind cross-language repair fallback" in row["source"]["transformation"] for row in rows)
    assert manifest["selection_contract"] == {
        "seed": SEED,
        "ordering": "sha256(seed\\0source_language\\0target_lane\\0dataset\\0revision\\0record_id\\0source_record_sha256)",
        "content_blind": True, "capability_keywords_used": False, "evaluation_content_read": False,
        "retries": 0,
        "pool_specs": [
            {"source_language": "javascript", "target_lane": "typescript", "derivation_kind": DERIVATION_KIND},
            {"source_language": "java", "target_lane": "javascript", "derivation_kind": DERIVATION_KIND},
        ],
    }
    assert union.startswith(canonical_json(current_row) + b"\n")
    assert union[len(current.read_bytes()):] == b"".join(canonical_json(row) + b"\n" for row in rows)


def test_is_deterministic_and_excludes_all_lineage_surfaces(tmp_path: Path) -> None:
    args = fixture(tmp_path)[:6]
    first = build(args[0], args[1], args[2], [args[3]], args[4], [args[5]])
    second = build(args[0], args[1], args[2], [args[3]], args[4], [args[5]])
    assert first == second
    rows, manifest, union = first
    assert len({row["id"] for row in rows}) == len(rows)
    assert len({tuple(row["source"][key] for key in ("dataset", "revision", "record_id", "source_record_sha256")) for row in rows}) == len(rows)
    assert manifest["extension"]["sha256"] == hashlib.sha256(
        b"".join(canonical_json(row) + b"\n" for row in rows)
    ).hexdigest()
    body = dict(manifest); seal = body.pop("manifest_sha256")
    assert seal == hashlib.sha256(canonical_json(body)).hexdigest()
    assert manifest["union"]["sha256"] == hashlib.sha256(union).hexdigest()


def test_prior_lineage_exclusion_is_identity_exact(tmp_path: Path) -> None:
    config, snapshot, prior, v2, current, evidence, raw, _ = fixture(tmp_path)
    metadata = json.loads(config.read_text())["sources"]["mceval"]
    excluded = {
        "dataset": metadata["dataset"], "revision": metadata["revision"], "record_id": "row-00000",
        "source_record_sha256": hashlib.sha256(canonical_json(raw[0])).hexdigest(),
    }
    write_jsonl(prior, [{"lineage": excluded}])
    rows, manifest, _union = build(config, snapshot, prior, [v2], current, [evidence])
    assert [row["target_lane"] for row in rows] == ["javascript"]
    assert manifest["pools"]["javascript_to_typescript"]["excluded_roots"] == 2


def test_rejects_hash_drift_and_non_byte_preserving_union(tmp_path: Path) -> None:
    config, snapshot, prior, v2, current, evidence, *_ = fixture(tmp_path)
    changed = json.loads(config.read_text()); changed["sources"]["mceval"]["sha256"] = "0" * 64
    config.write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        build(config, snapshot, prior, [v2], current, [evidence])

    config, snapshot, prior, v2, current, evidence, *_ = fixture(tmp_path / "again")
    current.write_bytes(current.read_bytes().rstrip(b"\n"))
    with pytest.raises(ValueError, match="end with LF"):
        build(config, snapshot, prior, [v2], current, [evidence])
