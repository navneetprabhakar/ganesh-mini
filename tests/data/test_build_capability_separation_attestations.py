import json
from pathlib import Path

import pytest

from scripts.data.build_capability_separation_attestations import (
    PASS_FIELDS,
    build_report,
    canonical_sha256,
)
from scripts.eval.contracts import sha256_text


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def code_item(code: str, **extra: object) -> dict:
    return {"label": "fixture", "code": code, "sha256": sha256_text(code), **extra}


def file_item(content: str, **extra: object) -> dict:
    return {"content": content, "sha256": sha256_text(content), **extra}


def candidate(identifier: str, prompt: str, reference: str, test: str, known_bad: str) -> dict:
    result = {
        "schema_version": "ganesh-mini-expansion-candidate/v1",
        "id": identifier,
        "lane": "python",
        "task_type": "generation",
        "messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": reference}],
        "source": {},
        "rights": {},
        "verification_task": {
            "schema_version": "1.0",
            "task_id": identifier,
            "surface": "training_admission",
            "language": "python",
            "family": "python",
            "task_type": "generation",
            "prompt": {"text": prompt},
            "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
            "candidate_path": "solution.py",
            "validation": {
                "reference": code_item(reference),
                "known_bad": [code_item(known_bad, label="bad")],
            },
            "files": [file_item(test, path="test_solution.py", role="test")],
            "runtime_id": "python-3.12.11",
            "limits": {"timeout_seconds": 5, "memory_mb": 256, "cpus": 1, "pids": 64, "output_bytes": 65536},
        },
        "test_origin": "independent",
        "qualification_assignment": {"ignored": "by base-candidate hashing"},
        "teacher_evidence": {"ignored": "by base-candidate hashing"},
    }
    result["verification_task"]["prompt"]["sha256"] = sha256_text(prompt)
    return result


def evaluation_task(task_id: str, prompt: str, reference: str, test: str, known_bad: str) -> dict:
    # Minimal valid synthetic task contract used by evaluation_index.
    return {
        "schema_version": "1.0",
        "task_id": task_id,
        "surface": "development",
        "language": "python",
        "task_type": "generation",
        "family": "python",
        "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "candidate_path": "solution.py",
        "files": [file_item(test, path="test_solution.py", role="test")],
        "validation": {
            "reference": code_item(reference),
            "known_bad": [code_item(known_bad, label="bad")],
        },
        "runtime_id": "python-3.12.11",
        "limits": {"timeout_seconds": 5, "memory_mb": 256, "cpus": 1, "pids": 64, "output_bytes": 65536},
    }


def surfaces(tmp_path: Path, rows: list[dict]) -> tuple[Path, Path, Path]:
    candidates = tmp_path / "candidates.jsonl"
    training = tmp_path / "training.jsonl"
    evaluation = tmp_path / "eval.task.json"
    write_jsonl(candidates, rows)
    write_jsonl(training, [{
        "messages": [
            {"role": "user", "content": "Prior task about a completely separate queue implementation."},
            {"role": "assistant", "content": "def prior_queue():\n    return ['separate']\n"},
        ]
    }])
    evaluation.write_text(json.dumps(evaluation_task(
        "private-eval", "Evaluate a separate bounded accumulator without shared wording.",
        "def eval_accumulate(xs):\n    return sum(xs)\n",
        "from solution import eval_accumulate\nassert eval_accumulate([2, 3]) == 5\n",
        "def eval_accumulate(xs):\n    return 0\n",
    )), encoding="utf-8")
    return candidates, training, evaluation


def test_pass_report_is_sealed_compatible_and_content_free(tmp_path: Path) -> None:
    row = candidate(
        "candidate-1", "Implement a stable Unicode bucketizer for twelve independent labels and preserve order.",
        "def bucketize(xs):\n    return list(dict.fromkeys(xs))\n",
        "from solution import bucketize\nassert bucketize(['a', 'a', 'b']) == ['a', 'b']\n",
        "def bucketize(xs):\n    return sorted(set(xs))\n",
    )
    candidates, training, evaluation = surfaces(tmp_path, [row])
    report = build_report(candidates, [training], [evaluation])

    assert report["status"] == "passed"
    assert report["evaluation_artifacts_read_by_construction"] == 0
    assert all(report["records"][0][field] is True for field in PASS_FIELDS)
    base = {key: row[key] for key in row if key not in {"qualification_assignment", "teacher_evidence"}}
    assert report["records"][0]["candidate_sha256"] == canonical_sha256(base)
    body = dict(report)
    assert body.pop("report_sha256") == canonical_sha256(body)
    assert report["comparison_manifest_sha256"] == canonical_sha256(report["comparison_manifest"])
    serialized = json.dumps(report)
    assert "private-eval" not in serialized
    assert "Evaluate a separate" not in serialized
    assert str(evaluation) not in serialized


@pytest.mark.parametrize("artifact", ["prompt", "reference", "test", "known_bad"])
def test_fails_evaluation_checks_for_prompt_and_every_code_artifact(tmp_path: Path, artifact: str) -> None:
    values = {
        "prompt": "Implement a stable Unicode bucketizer for twelve independent labels and preserve order.",
        "reference": "def bucketize(xs):\n    return list(dict.fromkeys(xs))\n",
        "test": "from solution import bucketize\nassert bucketize(['a', 'a', 'b']) == ['a', 'b']\n",
        "known_bad": "def bucketize(xs):\n    return sorted(set(xs))\n",
    }
    row = candidate("candidate-1", **values)
    candidates, training, evaluation = surfaces(tmp_path, [row])
    task = json.loads(evaluation.read_text())
    if artifact == "prompt":
        task["prompt"] = {"text": values[artifact], "sha256": sha256_text(values[artifact])}
    elif artifact == "reference":
        task["validation"]["reference"] = code_item(values[artifact])
    elif artifact == "known_bad":
        task["validation"]["known_bad"] = [code_item(values[artifact], label="bad")]
    else:
        task["files"] = [file_item(values[artifact], path="test_solution.py", role="test")]
    evaluation.write_text(json.dumps(task), encoding="utf-8")

    report = build_report(candidates, [training], [evaluation])
    record = report["records"][0]
    assert report["status"] == "failed"
    if artifact == "prompt":
        assert not record["exact_evaluation_passed"]
        assert not record["normalized_evaluation_passed"]
        assert not record["fuzzy_evaluation_passed"]
    else:
        assert not record["exact_evaluation_passed"]
        assert not record["normalized_evaluation_passed"]


def test_training_normalized_and_peer_fuzzy_collisions_fail_both_peers(tmp_path: Path) -> None:
    prompt = "Implement a stable Unicode bucketizer for twelve independent labels and preserve order."
    first = candidate(
        "candidate-1", prompt,
        "def bucketize(xs):\n    return list(dict.fromkeys(xs))\n",
        "from solution import bucketize\nassert bucketize(['a']) == ['a']\n",
        "def bucketize(xs):\n    return []\n",
    )
    second = candidate(
        "candidate-2", prompt.upper(),
        "def distinct(xs):\n    return list(dict.fromkeys(xs))\n",
        "from solution import distinct\nassert distinct(['b']) == ['b']\n",
        "def distinct(xs):\n    return []\n",
    )
    candidates, training, evaluation = surfaces(tmp_path, [first, second])
    training_row = {"messages": [
        {"role": "user", "content": "Unrelated training request long enough to enter the fuzzy comparison index."},
        {"role": "assistant", "content": first["messages"][1]["content"].upper()},
    ]}
    write_jsonl(training, [training_row])

    report = build_report(candidates, [training], [evaluation])
    by_id = {row["id"]: row for row in report["records"]}
    assert not by_id["candidate-1"]["normalized_training_passed"]
    assert not by_id["candidate-1"]["fuzzy_training_passed"]
    assert not by_id["candidate-2"]["fuzzy_training_passed"]


def test_fails_closed_on_bad_candidate_code_hash_and_empty_surfaces(tmp_path: Path) -> None:
    row = candidate(
        "candidate-1", "Implement a stable Unicode bucketizer for twelve independent labels and preserve order.",
        "def bucketize(xs):\n    return list(dict.fromkeys(xs))\n",
        "from solution import bucketize\nassert bucketize(['a']) == ['a']\n",
        "def bucketize(xs):\n    return []\n",
    )
    row["verification_task"]["files"][0]["sha256"] = "0" * 64
    candidates, training, evaluation = surfaces(tmp_path, [row])
    with pytest.raises(ValueError, match="hash mismatch"):
        build_report(candidates, [training], [evaluation])
    row["verification_task"]["files"][0]["sha256"] = sha256_text(
        row["verification_task"]["files"][0]["content"]
    )
    write_jsonl(candidates, [row])
    with pytest.raises(ValueError, match="prior training corpus"):
        build_report(candidates, [], [evaluation])
