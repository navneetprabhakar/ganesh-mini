from __future__ import annotations

import json
from pathlib import Path

import pytest

import scripts.data.build_v4_repair_source_union as subject
from scripts.data.build_capability_corpus_plan import canonical_sha256


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows))


def row(identifier: str, record_id: str) -> dict:
    return {
        "id": identifier,
        "source": {
            "dataset": "fixture", "revision": "r1", "record_id": record_id,
            "source_record_sha256": (record_id[0] * 64),
        },
    }


def fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    parent = tmp_path / "parent.jsonl"
    extension = tmp_path / "extension.jsonl"
    write_jsonl(parent, [row("parent-1", "a-record")])
    write_jsonl(extension, [row(f"extension-{index}", f"b-{index}") for index in range(3000)])
    monkeypatch.setattr(subject, "PARENT_SHA256", subject.file_sha256(parent))
    manifest = {
        "schema_version": subject.EXTENSION_MANIFEST_SCHEMA,
        "status": "sealed-inactive-source-extension",
        "plan_sha256": subject.PLAN_SHA256,
        "extension": {
            "sha256": subject.file_sha256(extension), "bytes": extension.stat().st_size,
            "records": 3000,
        },
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_path = tmp_path / "extension-manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    return parent, extension, manifest_path


def test_builds_byte_prefix_union(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    parent, extension, manifest = fixture(tmp_path, monkeypatch)
    payload, report = subject.build(parent, extension, manifest)
    assert payload == parent.read_bytes() + extension.read_bytes()
    assert report["status"] == "sealed-classification-eligible"
    assert report["union"]["records"] == 3001
    assert report["union"]["parent_is_exact_byte_prefix"] is True
    body = dict(report); claimed = body.pop("manifest_sha256")
    assert claimed == canonical_sha256(body)


def test_rejects_duplicate_lineage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    parent, extension, manifest = fixture(tmp_path, monkeypatch)
    rows = [json.loads(line) for line in extension.read_text().splitlines()]
    rows[0]["source"] = row("unused", "a-record")["source"]
    write_jsonl(extension, rows)
    value = json.loads(manifest.read_text())
    value["extension"].update(
        sha256=subject.file_sha256(extension), bytes=extension.stat().st_size,
    )
    value.pop("manifest_sha256")
    value["manifest_sha256"] = canonical_sha256(value)
    manifest.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="overlaps"):
        subject.build(parent, extension, manifest)
