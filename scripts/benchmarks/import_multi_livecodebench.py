from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from scripts.eval.contracts import canonical_json, load_json, sha256_bytes, sha256_text, write_json


REQUIRED_RECORD_KEYS = {
    "question_title",
    "question_content",
    "platform",
    "question_id",
    "contest_id",
    "contest_date",
    "starter_code",
    "difficulty",
    "public_test_cases",
    "private_test_cases",
    "metadata",
}

BASE_EXCLUSION_REASONS = (
    "conflicting_source_license_metadata",
    "missing_upstream_reference_implementation",
    "missing_independently_rejected_known_bad_implementation",
)


class ImportFailure(ValueError):
    """Raised when pinned source material fails closed integrity checks."""


def _check_sha(path: Path, expected_bytes: int, expected_sha256: str) -> None:
    actual_bytes = path.stat().st_size
    if actual_bytes != expected_bytes:
        raise ImportFailure(f"source bytes mismatch: expected {expected_bytes}, got {actual_bytes}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    actual = digest.hexdigest()
    if actual != expected_sha256:
        raise ImportFailure(f"source SHA-256 mismatch: expected {expected_sha256}, got {actual}")


def download_source(config: dict[str, Any], destination: Path) -> Path:
    data = config["upstream"]["data"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        _check_sha(destination, data["bytes"], data["sha256"])
        return destination
    request = urllib.request.Request(data["download_url"], headers={"User-Agent": "ganesh-mini-benchmark-import/1.0"})
    with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                while chunk := response.read(1024 * 1024):
                    handle.write(chunk)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise
    try:
        _check_sha(temporary, data["bytes"], data["sha256"])
        os.replace(temporary, destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return destination


def _records(path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    with path.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ImportFailure(f"record {index}: malformed JSON: {error}") from error
            if not isinstance(record, dict) or set(record) != REQUIRED_RECORD_KEYS:
                actual = set(record) if isinstance(record, dict) else set()
                raise ImportFailure(
                    f"record {index}: key mismatch; missing={sorted(REQUIRED_RECORD_KEYS - actual)}, "
                    f"extra={sorted(actual - REQUIRED_RECORD_KEYS)}"
                )
            yield index, record


def _validate_record(index: int, record: dict[str, Any]) -> tuple[list[dict[str, str]], str]:
    for name in REQUIRED_RECORD_KEYS:
        if not isinstance(record[name], str):
            raise ImportFailure(f"record {index}.{name}: expected string")
    if not record["question_id"] or not record["question_content"]:
        raise ImportFailure(f"record {index}: empty question ID or content")
    try:
        public_tests = json.loads(record["public_test_cases"])
    except json.JSONDecodeError as error:
        raise ImportFailure(f"record {index}: malformed public tests: {error}") from error
    if not isinstance(public_tests, list) or not public_tests:
        raise ImportFailure(f"record {index}: public tests must be a non-empty list")
    for test_index, test in enumerate(public_tests):
        if not isinstance(test, dict) or set(test) != {"input", "output", "testtype"}:
            raise ImportFailure(f"record {index}: malformed public test {test_index}")
        if not all(isinstance(test[key], str) for key in test):
            raise ImportFailure(f"record {index}: non-string public test field {test_index}")
        if test["testtype"] not in {"stdin", "functional"}:
            raise ImportFailure(f"record {index}: unsupported test type {test['testtype']!r}")
    test_types = {test["testtype"] for test in public_tests}
    if len(test_types) != 1:
        raise ImportFailure(f"record {index}: mixed public test types")
    return public_tests, next(iter(test_types))


def build_outputs(config: dict[str, Any], source: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    data = config["upstream"]["data"]
    _check_sha(source, data["bytes"], data["sha256"])
    exclusions: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    source_type_counts: Counter[str] = Counter()
    platform_counts: Counter[str] = Counter()
    lane_counts: dict[str, dict[str, int]] = {
        lane: {"source_records": 0, "imported": 0, "excluded": 0}
        for lane in config["lanes"]
    }
    row_count = 0
    for index, record in _records(source):
        _, test_type = _validate_record(index, record)
        question_id = record["question_id"]
        if question_id in seen_ids:
            raise ImportFailure(f"record {index}: duplicate question_id {question_id!r}")
        seen_ids.add(question_id)
        row_count += 1
        source_type_counts[test_type] += 1
        platform_counts[record["platform"]] += 1
        record_hash = sha256_bytes(canonical_json(record))
        for lane in config["lanes"]:
            reasons = list(BASE_EXCLUSION_REASONS)
            if test_type == "functional":
                reasons.append("functional_to_stdin_conversion_not_materialized")
            exclusion = {
                "schema_version": "1.0",
                "benchmark_id": config["benchmark_id"],
                "surface": "diagnostic",
                "diagnostic_only": True,
                "decision_evidence": False,
                "status": "excluded",
                "target_language": lane,
                "source": {
                    "repository": data["repository"],
                    "revision": data["revision"],
                    "release_slice": data["release_slice"],
                    "shard": data["shard"],
                    "shard_sha256": data["sha256"],
                    "record_index": index,
                    "question_id": question_id,
                    "record_sha256": record_hash,
                    "question_content_sha256": sha256_text(record["question_content"]),
                    "public_test_cases_sha256": sha256_text(record["public_test_cases"]),
                    "private_test_cases_sha256": sha256_text(record["private_test_cases"]),
                },
                "metadata": {
                    "platform": record["platform"],
                    "contest_date": record["contest_date"],
                    "difficulty": record["difficulty"],
                    "test_type": test_type,
                },
                "reasons": reasons,
            }
            exclusions.append(exclusion)
            lane_counts[lane]["source_records"] += 1
            lane_counts[lane]["excluded"] += 1
    if row_count != data["rows"]:
        raise ImportFailure(f"source row count mismatch: expected {data['rows']}, got {row_count}")
    exclusions.sort(key=lambda item: (item["target_language"], item["source"]["record_index"]))
    manifest = {
        "schema_version": "1.0",
        "benchmark_id": config["benchmark_id"],
        "surface": "diagnostic",
        "diagnostic_only": True,
        "decision_evidence": False,
        "status": "no_compatible_tasks",
        "source": config["upstream"],
        "policy": config["import_policy"],
        "counts": {
            "source_records": row_count,
            "source_test_types": dict(sorted(source_type_counts.items())),
            "source_platforms": dict(sorted(platform_counts.items())),
            "per_lane": lane_counts,
            "imported_tasks": 0,
            "exclusions": len(exclusions),
        },
        "blockers": list(BASE_EXCLUSION_REASONS),
    }
    return exclusions, manifest


def _jsonl_bytes(items: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json(item) + b"\n" for item in items)


def import_benchmark(config_path: Path, source: Path, output_dir: Path, manifest_path: Path) -> dict[str, Any]:
    config = load_json(config_path)
    exclusions, manifest = build_outputs(config, source)
    exclusions_payload = _jsonl_bytes(exclusions)
    exclusions_path = output_dir / "exclusions.jsonl"
    output_dir.mkdir(parents=True, exist_ok=True)
    exclusions_path.write_bytes(exclusions_payload)
    notice = {
        "benchmark_id": config["benchmark_id"],
        "diagnostic_only": True,
        "decision_evidence": False,
        "redistributed_task_content": False,
        "code_license": config["upstream"]["code"],
        "data_license": config["upstream"]["data"]["license"],
    }
    write_json(output_dir / "NOTICE.json", notice)
    manifest["outputs"] = {
        "exclusions": {
            "path": exclusions_path.as_posix(),
            "bytes": len(exclusions_payload),
            "sha256": sha256_bytes(exclusions_payload),
        },
        "tasks": {"count": 0, "reason": "no records satisfy the strict evaluation task contract"},
    }
    write_json(manifest_path, manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Import pinned Multi-LiveCodeBench public diagnostics")
    parser.add_argument("--config", type=Path, default=Path("configs/benchmarks/multi_livecodebench.json"))
    parser.add_argument("--source", type=Path)
    parser.add_argument(
        "--cache",
        type=Path,
        default=Path("datasets/cache/benchmarks/multi_livecodebench/test6.jsonl"),
    )
    parser.add_argument("--output-dir", type=Path, default=Path("eval/public/multi_livecodebench_v6"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("manifests/evaluation/public/multi_livecodebench_v6.json"),
    )
    args = parser.parse_args()
    config = load_json(args.config)
    source = args.source or download_source(config, args.cache)
    manifest = import_benchmark(args.config, source, args.output_dir, args.manifest)
    print(json.dumps(manifest["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
