from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.benchmarks.import_multi_livecodebench import ImportFailure, import_benchmark
from scripts.eval.contracts import sha256_bytes


def _record(question_id: str, testtype: str = "stdin") -> dict[str, str]:
    return {
        "question_title": "Fixture",
        "question_content": "Read x and print x.",
        "platform": "fixture",
        "question_id": question_id,
        "contest_id": "fixture-contest",
        "contest_date": "2026-01-01T00:00:00",
        "starter_code": "",
        "difficulty": "easy",
        "public_test_cases": json.dumps([{"input": "1", "output": "1", "testtype": testtype}]),
        "private_test_cases": "opaque-upstream-payload",
        "metadata": "{}",
    }


def _fixture(tmp_path: Path, records: list[dict[str, str]]) -> tuple[Path, Path]:
    source = tmp_path / "source.jsonl"
    payload = b"".join(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode() + b"\n" for record in records
    )
    source.write_bytes(payload)
    config = {
        "schema_version": "1.0",
        "benchmark_id": "multi-livecodebench-fixture",
        "surface": "diagnostic",
        "diagnostic_only": True,
        "decision_evidence": False,
        "upstream": {
            "code": {"repository": "code", "revision": "a", "license_expression": "MIT"},
            "data": {
                "repository": "data",
                "revision": "b",
                "release_slice": "fixture",
                "shard": source.name,
                "download_url": "unused",
                "bytes": len(payload),
                "rows": len(records),
                "sha256": sha256_bytes(payload),
                "license": {"status": "conflicting_metadata"},
            },
        },
        "lanes": {lane: f"{lane}-runtime" for lane in ("go", "java", "javascript", "typescript", "python", "rust")},
        "limits": {},
        "import_policy": {
            "require_unambiguous_data_license": True,
            "require_reference_implementation": True,
            "require_known_bad_implementation": True,
            "allow_unsafe_pickle": False,
            "materialize_source_prompts_for_exclusions": False,
        },
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    return config_path, source


def test_import_is_deterministic_and_diagnostic_only(tmp_path: Path) -> None:
    config, source = _fixture(tmp_path, [_record("one"), _record("two", "functional")])
    first_output = tmp_path / "first"
    first_manifest = tmp_path / "first-manifest.json"
    manifest = import_benchmark(config, source, first_output, first_manifest)
    second_output = tmp_path / "second"
    second_manifest = tmp_path / "second-manifest.json"
    repeated = import_benchmark(config, source, second_output, second_manifest)

    assert manifest["counts"] == repeated["counts"]
    assert manifest["source"] == repeated["source"]
    assert manifest["outputs"]["exclusions"]["sha256"] == repeated["outputs"]["exclusions"]["sha256"]
    assert manifest["diagnostic_only"] is True
    assert manifest["decision_evidence"] is False
    assert manifest["counts"]["imported_tasks"] == 0
    assert manifest["counts"]["exclusions"] == 12
    assert first_output.joinpath("exclusions.jsonl").read_bytes() == second_output.joinpath("exclusions.jsonl").read_bytes()
    rows = [json.loads(line) for line in first_output.joinpath("exclusions.jsonl").read_text().splitlines()]
    assert all(row["surface"] == "diagnostic" and row["decision_evidence"] is False for row in rows)
    assert all("question_content" not in row["source"] for row in rows)
    assert any("functional_to_stdin_conversion_not_materialized" in row["reasons"] for row in rows)


def test_import_fails_closed_on_source_hash_mismatch(tmp_path: Path) -> None:
    config, source = _fixture(tmp_path, [_record("one")])
    source.write_text("tampered\n", encoding="utf-8")
    with pytest.raises(ImportFailure, match="source bytes mismatch|source SHA-256 mismatch"):
        import_benchmark(config, source, tmp_path / "output", tmp_path / "manifest.json")


def test_import_rejects_duplicate_question_ids(tmp_path: Path) -> None:
    config, source = _fixture(tmp_path, [_record("duplicate"), _record("duplicate")])
    with pytest.raises(ImportFailure, match="duplicate question_id"):
        import_benchmark(config, source, tmp_path / "output", tmp_path / "manifest.json")
