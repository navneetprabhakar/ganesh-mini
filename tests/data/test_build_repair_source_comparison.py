import json
from pathlib import Path

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_repair_source_comparison import build_comparison
from scripts.eval.contracts import sha256_text


def task(prompt: str) -> dict:
    code = "def solve(value):\n    return value\n"
    bad = "def solve(value):\n    return None\n"
    test = "from solution import solve\nassert solve(1) == 1\n"
    return {
        "schema_version": "1.0", "task_id": "private-id", "surface": "development",
        "language": "python", "family": "python", "task_type": "generation",
        "runtime_id": "python-locked", "candidate_path": "solution.py",
        "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "files": [{"path": "test.py", "role": "test", "content": test, "sha256": sha256_text(test)}],
        "validation": {
            "reference": {"label": "reference", "code": code, "sha256": sha256_text(code)},
            "known_bad": [{"label": "bad", "code": bad, "sha256": sha256_text(bad)}],
        },
        "limits": {"timeout_seconds": 10, "memory_mb": 256, "cpus": 1.0, "pids": 64,
                   "output_bytes": 65536},
    }


def test_comparison_exposes_only_source_exclusions(tmp_path: Path) -> None:
    prompt = "Implement a deterministic function that returns the supplied integer unchanged."
    eval_root = tmp_path / "private"; eval_root.mkdir()
    (eval_root / "secret.task.json").write_text(json.dumps(task(prompt)))
    source = tmp_path / "source.jsonl"
    source.write_text("\n".join(json.dumps(row) for row in [
        {"id": "same", "stimulus": prompt},
        {"id": "different", "stimulus": "Create a stable queue that preserves insertion order for unique keys."},
    ]) + "\n")

    report = build_comparison(source, [eval_root], fuzzy_limit=0, minimum_tokens=4)

    assert report["excluded_source_queue_ids"] == ["same"]
    assert report["visibility"] == {
        "evaluation_content_exposed_to_construction": False,
        "evaluation_identifiers_exposed_to_construction": False,
        "evaluation_paths_exposed_to_construction": False,
    }
    serialized = json.dumps(report)
    assert "private-id" not in serialized and "secret.task.json" not in serialized and prompt not in serialized
    body = dict(report); claimed = body.pop("comparison_sha256")
    assert claimed == canonical_sha256(body)


def test_duplicate_source_ids_fail_closed(tmp_path: Path) -> None:
    eval_path = tmp_path / "one.task.json"
    eval_path.write_text(json.dumps(task("A sufficiently long private evaluation prompt for hashing.")))
    source = tmp_path / "source.jsonl"
    row = {"id": "duplicate", "stimulus": "A source stimulus with enough words for comparison."}
    source.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n")

    try:
        build_comparison(source, [eval_path])
    except ValueError as exc:
        assert "duplicate" in str(exc)
    else:
        raise AssertionError("duplicate source IDs must fail closed")
