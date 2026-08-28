import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.build_expansion_source_queue import build_queue, canonical_json, infer_fence_lane


def source(dataset: str, revision: str, license_name: str, sha256: str) -> dict:
    return {
        "dataset": dataset, "uri": f"https://example.invalid/{dataset}", "revision": revision,
        "filename": "fixture", "sha256": sha256, "license": license_name,
        "license_uri": "https://example.invalid/license",
    }


def write_sources(tmp_path: Path) -> tuple[Path, Path, bytes, bytes]:
    mceval_rows = [
        {"instruction": f"Implement stable transform {lane} {index}", "output": "unused", "language": lane, "source": "McEval-Instruct"}
        for lane in ("Go", "Java", "JavaScript", "TypeScript", "Python", "Rust") for index in range(3)
    ]
    mceval_bytes = json.dumps(mceval_rows).encode()
    mceval = tmp_path / "mceval.json"; mceval.write_bytes(mceval_bytes)
    mdeval_rows = [
        {"messages": [{"role": "user", "content": f"```{lane}\nbug\n``` Fix it."}, {"role": "assistant", "content": "fixed"}]}
        for lane in ("go", "java", "javascript", "typescript", "python", "rust")
    ]
    mdeval_bytes = b"".join(canonical_json(row) + b"\n" for row in mdeval_rows)
    mdeval = tmp_path / "mdeval.jsonl"; mdeval.write_bytes(mdeval_bytes)
    return mceval, mdeval, mceval_bytes, mdeval_bytes


def test_build_queue_is_balanced_deterministic_and_uses_repair_fallback(tmp_path: Path) -> None:
    mceval, mdeval, mceval_bytes, mdeval_bytes = write_sources(tmp_path)
    targets = {lane: {"generation": 2, "repair": 2} for lane in ("go", "java", "javascript", "typescript", "python", "rust")}
    config = {
        "seed": "fixture", "stimulus_max_chars": 1000, "candidate_targets": targets,
        "sources": {
            "mceval": source("mceval", "a", "CC-BY-SA-4.0", hashlib.sha256(mceval_bytes).hexdigest()),
            "mdeval": source("mdeval", "b", "MIT", hashlib.sha256(mdeval_bytes).hexdigest()),
        },
    }
    first, report = build_queue(config, mceval, mdeval)
    second, _ = build_queue(config, mceval, mdeval)
    assert first == second
    assert len(first) == 24
    assert len({row["id"] for row in first}) == 24
    assert all(report["counts"][lane] == {"generation": 2, "repair": 2} for lane in targets)
    assert all(report["availability"][lane]["repair_fallback_used"] == 1 for lane in targets)
    assert all(row["source"]["source_record_sha256"] for row in first)


def test_snapshot_hash_mismatch_fails_closed(tmp_path: Path) -> None:
    mceval, mdeval, _, mdeval_bytes = write_sources(tmp_path)
    config = {
        "seed": "fixture", "stimulus_max_chars": 1000,
        "candidate_targets": {lane: {"generation": 1, "repair": 1} for lane in ("go", "java", "javascript", "typescript", "python", "rust")},
        "sources": {
            "mceval": source("mceval", "a", "CC-BY-SA-4.0", "0" * 64),
            "mdeval": source("mdeval", "b", "MIT", hashlib.sha256(mdeval_bytes).hexdigest()),
        },
    }
    with pytest.raises(ValueError, match="expected"):
        build_queue(config, mceval, mdeval)


def test_language_inference_requires_one_explicit_fence_language() -> None:
    assert infer_fence_lane([{"content": "```ts\nlet x = 1\n```"}]) == "typescript"
    assert infer_fence_lane([{"content": "no language fence"}]) is None
    assert infer_fence_lane([{"content": "```go\nx\n``` and ```rust\ny\n```"}]) is None
