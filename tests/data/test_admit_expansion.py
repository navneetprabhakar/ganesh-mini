from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import threading
import time
from unittest.mock import patch

from scripts.data.admit_expansion import admit_records, normalized_sha256, simhash
from scripts.eval.contracts import sha256_text


def task() -> dict:
    prompt = "Implement add_one(value: int) -> int and return only the complete Python source file."
    reference = "def add_one(value: int) -> int:\n    return value + 1\n"
    bad = "def add_one(value: int) -> int:\n    return value\n"
    tests = "from solution import add_one\nassert add_one(0) == 1\nassert add_one(-2) == -1\n"
    return {
        "schema_version": "1.0", "task_id": "source-1", "surface": "training_admission",
        "language": "python", "family": "python", "task_type": "generation",
        "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "candidate_path": "solution.py",
        "files": [{"path": "test_solution.py", "role": "test", "content": tests, "sha256": sha256_text(tests)}],
        "runtime_id": "python-3.11.15",
        "limits": {"timeout_seconds": 30, "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536},
        "validation": {
            "reference": {"label": "independent-reference", "code": reference, "sha256": sha256_text(reference)},
            "known_bad": [{"label": "off-by-one", "code": bad, "sha256": sha256_text(bad)}],
        },
    }


def record() -> dict:
    verification_task = task()
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1", "id": "source-1",
        "lane": "python", "task_type": "generation",
        "messages": [
            {"role": "user", "content": verification_task["prompt"]["text"]},
            {"role": "assistant", "content": verification_task["validation"]["reference"]["code"]},
        ],
        "source": {
            "dataset": "fixture", "uri": "https://example.invalid/fixture", "revision": "abc123",
            "record_id": "one", "license": "MIT", "license_uri": "https://example.invalid/license",
            "source_record_sha256": "a" * 64, "transformation": "independent task and tests",
        },
        "rights": {key: True for key in ("prompt", "answer", "tests", "redistribution", "model_training")},
        "verification_task": verification_task, "test_origin": "independent_author",
    }


def config() -> dict:
    return {
        "allowed_licenses": ["MIT"],
        "required_rights": ["prompt", "answer", "tests", "redistribution", "model_training"],
        "allowed_test_origins": ["independent_author", "independent_teacher"],
        "sources": {"fixture": {"revision": "abc123", "license": "MIT"}},
        "deduplication": {"prompt_simhash_max_hamming": 3, "minimum_fuzzy_tokens": 12},
    }


def empty_index() -> dict:
    return {"prompts": {}, "prompt_simhashes": [], "code_hashes": {}, "inspected": []}


def verifier(task_value: dict, code: str, runtime: Path) -> dict:
    passed = code == task_value["validation"]["reference"]["code"]
    return {"exit_codes": [0 if passed else 1], "timed_out": False, "stderr": "", "stdout": "", "runtime": str(runtime)}


def test_admits_reference_and_rejects_known_bad() -> None:
    accepted, rejected = admit_records([record()], config(), empty_index(), Path("runtime.json"), verifier)
    assert not rejected
    assert len(accepted) == 1
    assert accepted[0]["language"] == "Python"
    assert accepted[0]["verification"]["known_bad"][0]["result"]["exit_codes"] == [1]


def test_reference_and_known_bad_can_verify_concurrently_without_reordering() -> None:
    active = 0
    maximum = 0
    lock = threading.Lock()

    def concurrent_verifier(task_value: dict, code: str, runtime: Path) -> dict:
        nonlocal active, maximum
        with lock:
            active += 1
            maximum = max(maximum, active)
        time.sleep(0.02)
        with lock:
            active -= 1
        passed = code == task_value["validation"]["reference"]["code"]
        return {"exit_codes": [0 if passed else 1], "timed_out": False, "stderr": "", "stdout": ""}

    accepted, rejected = admit_records(
        [record()], config(), empty_index(), Path("runtime.json"), concurrent_verifier, verifier_workers=2,
    )
    assert not rejected and len(accepted) == 1
    assert maximum == 2


@patch("scripts.data.admit_expansion.time.sleep")
def test_retries_infrastructure_failure_and_preserves_attempt_evidence(_sleep) -> None:
    results = iter([
        {"exit_codes": [125], "timed_out": False, "stderr": "OCI runtime create failed", "stdout": ""},
        {"exit_codes": [0], "timed_out": False, "stderr": "", "stdout": ""},
        {"exit_codes": [1], "timed_out": False, "stderr": "assertion failed", "stdout": ""},
    ])

    def transient(task_value: dict, code: str, runtime: Path) -> dict:
        return next(results)

    accepted, rejected = admit_records([record()], config(), empty_index(), Path("runtime.json"), transient)
    assert not rejected and len(accepted) == 1
    retries = accepted[0]["verification"]["reference_runtime_retries"]
    assert len(retries) == 1
    assert retries[0]["result"]["exit_codes"] == [125]


def test_rejects_unadmitted_source() -> None:
    candidate = record(); candidate["source"]["dataset"] = "unknown"
    accepted, rejected = admit_records([candidate], config(), empty_index(), Path("runtime.json"), verifier)
    assert not accepted
    assert "not admitted" in rejected[0]["reason"]


def test_rejects_evaluation_prompt_overlap_before_execution() -> None:
    candidate = record(); prompt = candidate["messages"][0]["content"]
    index = empty_index(); index["prompts"] = {normalized_sha256(prompt): "private.task.json"}
    accepted, rejected = admit_records([candidate], config(), index, Path("runtime.json"), verifier)
    assert not accepted
    assert "exact evaluation prompt overlap" in rejected[0]["reason"]


def test_rejects_tests_that_accept_known_bad() -> None:
    def always_pass(task_value: dict, code: str, runtime: Path) -> dict:
        return {"exit_codes": [0], "timed_out": False, "stderr": "", "stdout": ""}

    accepted, rejected = admit_records([record()], config(), empty_index(), Path("runtime.json"), always_pass)
    assert not accepted
    assert "accepted known-bad" in rejected[0]["reason"]
    assert rejected[0]["evidence"]["known_bad"][0]["result"]["exit_codes"] == [0]


def test_rejects_non_independent_tests_and_duplicate_candidates() -> None:
    weak = record(); weak["test_origin"] = "source_provided"
    duplicate = deepcopy(record())
    accepted, rejected = admit_records([weak, record(), duplicate], config(), empty_index(), Path("runtime.json"), verifier)
    assert len(accepted) == 1
    assert any("not independent" in item["reason"] for item in rejected)
    assert any("duplicate within" in item["reason"] for item in rejected)


def test_simhash_is_stable_under_case_and_whitespace() -> None:
    assert simhash("Alpha   beta gamma") == simhash(" alpha BETA\ngamma ")


def test_rejects_fuzzy_duplicate_within_expansion() -> None:
    first = record()
    second = deepcopy(first); second["id"] = "source-2"; second["verification_task"]["task_id"] = "source-2"
    second["source"]["record_id"] = "two"; second["source"]["source_record_sha256"] = "b" * 64
    # Preserve the same normalized prompt features while changing the exact
    # conversation so this exercises the fuzzy boundary rather than exact dedup.
    second_prompt = first["messages"][0]["content"].replace("Implement", "IMPLEMENT")
    second["messages"][0]["content"] = second_prompt
    second["verification_task"]["prompt"] = {"text": second_prompt, "sha256": sha256_text(second_prompt)}
    second["verification_task"]["rendered_prompt"] = {"text": second_prompt, "sha256": sha256_text(second_prompt)}
    accepted, rejected = admit_records([first, second], config(), empty_index(), Path("runtime.json"), verifier)
    assert len(accepted) == 1
    assert "duplicate within" in rejected[0]["reason"] or "fuzzy expansion" in rejected[0]["reason"]
