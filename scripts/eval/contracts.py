from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


LANGUAGE_FAMILY = {
    "go": "go",
    "java": "java",
    "javascript": "javascript_typescript",
    "typescript": "javascript_typescript",
    "python": "python",
    "rust": "rust",
}

CANDIDATE_PATH = {
    "go": "solution.go",
    "java": "Solution.java",
    "javascript": "solution.js",
    "typescript": "solution.ts",
    "python": "solution.py",
    "rust": "solution.rs",
}

SURFACES = {"synthetic_harness", "diagnostic", "development", "decision"}
TASK_TYPES = {"generation", "repair"}
SHA256_LEN = 64


class ContractError(ValueError):
    """Raised when evidence does not satisfy the fail-closed contract."""


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_object(value: Any) -> str:
    return sha256_bytes(canonical_json(value))


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")


def _exact_keys(value: dict[str, Any], required: Iterable[str], where: str) -> None:
    expected = set(required)
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ContractError(f"{where}: key mismatch; missing={missing}, extra={extra}")


def _dict(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{where}: expected object")
    return value


def _string(value: Any, where: str, *, nonempty: bool = False) -> str:
    if not isinstance(value, str) or (nonempty and not value):
        raise ContractError(f"{where}: expected {'non-empty ' if nonempty else ''}string")
    return value


def _sha(value: Any, where: str) -> str:
    text = _string(value, where)
    if len(text) != SHA256_LEN or any(char not in "0123456789abcdef" for char in text):
        raise ContractError(f"{where}: expected lowercase SHA-256")
    return text


def _safe_relative_path(value: Any, where: str) -> str:
    text = _string(value, where, nonempty=True)
    path = PurePosixPath(text)
    if path.is_absolute() or ".." in path.parts or "." in path.parts or "\\" in text:
        raise ContractError(f"{where}: path must be normalized, relative, and remain under the task root")
    if any(part == "" for part in path.parts):
        raise ContractError(f"{where}: invalid empty path segment")
    return text


def _validate_hashed_text(value: Any, where: str, *, allow_empty: bool = False) -> None:
    item = _dict(value, where)
    _exact_keys(item, ("text", "sha256"), where)
    text = _string(item["text"], f"{where}.text", nonempty=not allow_empty)
    if _sha(item["sha256"], f"{where}.sha256") != sha256_text(text):
        raise ContractError(f"{where}: content hash mismatch")


def validate_task(
    task: Any, *, require_files: bool = True, require_test_file: bool = True,
) -> dict[str, Any]:
    task = _dict(task, "task")
    _exact_keys(
        task,
        (
            "schema_version", "task_id", "surface", "language", "family",
            "task_type", "prompt", "rendered_prompt", "candidate_path", "files",
            "runtime_id", "limits", "validation",
        ),
        "task",
    )
    if task["schema_version"] != "1.0":
        raise ContractError("task.schema_version: unsupported version")
    _string(task["task_id"], "task.task_id", nonempty=True)
    if task["surface"] not in SURFACES:
        raise ContractError("task.surface: unknown surface")
    language = task["language"]
    if language not in LANGUAGE_FAMILY:
        raise ContractError("task.language: unknown language")
    if task["family"] != LANGUAGE_FAMILY[language]:
        raise ContractError("task.family: does not match language")
    if task["task_type"] not in TASK_TYPES:
        raise ContractError("task.task_type: unknown task type")
    _validate_hashed_text(task["prompt"], "task.prompt")
    _validate_hashed_text(task["rendered_prompt"], "task.rendered_prompt")
    candidate_path = _safe_relative_path(task["candidate_path"], "task.candidate_path")
    if candidate_path != CANDIDATE_PATH[language]:
        raise ContractError(f"task.candidate_path: must be {CANDIDATE_PATH[language]!r} for {language}")
    _string(task["runtime_id"], "task.runtime_id", nonempty=True)

    files = task["files"]
    if not isinstance(files, list) or require_files and not files:
        raise ContractError(
            "task.files: expected non-empty array" if require_files
            else "task.files: expected array"
        )
    seen_paths: set[str] = set()
    test_count = 0
    for index, raw_file in enumerate(files):
        where = f"task.files[{index}]"
        item = _dict(raw_file, where)
        _exact_keys(item, ("path", "role", "content", "sha256"), where)
        path = _safe_relative_path(item["path"], f"{where}.path")
        if path == candidate_path:
            raise ContractError(f"{where}.path: cannot overwrite candidate path")
        if path in seen_paths:
            raise ContractError(f"{where}.path: duplicate path")
        seen_paths.add(path)
        if item["role"] not in {"test", "support"}:
            raise ContractError(f"{where}.role: invalid role")
        test_count += item["role"] == "test"
        content = _string(item["content"], f"{where}.content")
        if _sha(item["sha256"], f"{where}.sha256") != sha256_text(content):
            raise ContractError(f"{where}: content hash mismatch")
    if require_test_file and test_count == 0:
        raise ContractError("task.files: at least one test file is required")

    limits = _dict(task["limits"], "task.limits")
    _exact_keys(limits, ("timeout_seconds", "memory_mb", "cpus", "pids", "output_bytes"), "task.limits")
    ranges = {
        "timeout_seconds": (1, 120), "memory_mb": (64, 2048),
        "cpus": (0.01, 2), "pids": (8, 256), "output_bytes": (1024, 1048576),
    }
    for name, (low, high) in ranges.items():
        value = limits[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not low <= value <= high:
            raise ContractError(f"task.limits.{name}: outside [{low}, {high}]")
    for name in ("timeout_seconds", "memory_mb", "pids", "output_bytes"):
        if not isinstance(limits[name], int) or isinstance(limits[name], bool):
            raise ContractError(f"task.limits.{name}: expected integer")

    validation = _dict(task["validation"], "task.validation")
    _exact_keys(validation, ("reference", "known_bad"), "task.validation")
    artifacts = [("reference", validation["reference"])]
    if not isinstance(validation["known_bad"], list) or not validation["known_bad"]:
        raise ContractError("task.validation.known_bad: expected non-empty array")
    artifacts.extend((f"known_bad[{i}]", value) for i, value in enumerate(validation["known_bad"]))
    for label, raw_artifact in artifacts:
        where = f"task.validation.{label}"
        artifact = _dict(raw_artifact, where)
        _exact_keys(artifact, ("label", "code", "sha256"), where)
        _string(artifact["label"], f"{where}.label", nonempty=True)
        code = _string(artifact["code"], f"{where}.code")
        if _sha(artifact["sha256"], f"{where}.sha256") != sha256_text(code):
            raise ContractError(f"{where}: content hash mismatch")
    return task


def validate_result(result: Any) -> dict[str, Any]:
    result = _dict(result, "result")
    top_keys = (
        "schema_version", "task_id", "surface", "language", "family", "task_sha256",
        "prompt_sha256", "rendered_prompt_sha256", "model", "inference", "candidate",
        "verifier", "passed", "result_sha256",
    )
    _exact_keys(result, top_keys, "result")
    if result["schema_version"] != "1.0":
        raise ContractError("result.schema_version: unsupported version")
    _string(result["task_id"], "result.task_id", nonempty=True)
    if result["surface"] not in SURFACES or result["language"] not in LANGUAGE_FAMILY:
        raise ContractError("result: invalid surface or language")
    if result["family"] != LANGUAGE_FAMILY[result["language"]]:
        raise ContractError("result.family: does not match language")
    for name in ("task_sha256", "prompt_sha256", "rendered_prompt_sha256"):
        _sha(result[name], f"result.{name}")

    model = _dict(result["model"], "result.model")
    _exact_keys(model, ("model_id", "revision", "artifact_sha256", "serving_contract_sha256"), "result.model")
    _string(model["model_id"], "result.model.model_id", nonempty=True)
    _string(model["revision"], "result.model.revision", nonempty=True)
    _sha(model["artifact_sha256"], "result.model.artifact_sha256")
    _sha(model["serving_contract_sha256"], "result.model.serving_contract_sha256")

    inference = _dict(result["inference"], "result.inference")
    _exact_keys(inference, ("parameters", "parameters_sha256", "started_at", "completed_at"), "result.inference")
    _dict(inference["parameters"], "result.inference.parameters")
    if _sha(inference["parameters_sha256"], "result.inference.parameters_sha256") != sha256_object(inference["parameters"]):
        raise ContractError("result.inference: parameters hash mismatch")
    _string(inference["started_at"], "result.inference.started_at", nonempty=True)
    _string(inference["completed_at"], "result.inference.completed_at", nonempty=True)

    candidate = _dict(result["candidate"], "result.candidate")
    _exact_keys(candidate, ("raw_output", "raw_output_sha256", "extracted_code", "extracted_code_sha256", "extractor_id"), "result.candidate")
    for field, hash_field in (("raw_output", "raw_output_sha256"), ("extracted_code", "extracted_code_sha256")):
        text = _string(candidate[field], f"result.candidate.{field}")
        if _sha(candidate[hash_field], f"result.candidate.{hash_field}") != sha256_text(text):
            raise ContractError(f"result.candidate: {field} hash mismatch")
    _string(candidate["extractor_id"], "result.candidate.extractor_id", nonempty=True)

    verifier = _dict(result["verifier"], "result.verifier")
    verifier_keys = (
        "runtime_id", "image", "image_id", "commands", "exit_codes", "timed_out",
        "stdout", "stdout_sha256", "stderr", "stderr_sha256", "duration_ms",
        "sandbox_contract_sha256",
    )
    _exact_keys(verifier, verifier_keys, "result.verifier")
    _string(verifier["runtime_id"], "result.verifier.runtime_id", nonempty=True)
    image = _string(verifier["image"], "result.verifier.image", nonempty=True)
    if "@sha256:" not in image or len(image.rsplit("@sha256:", 1)[1]) != SHA256_LEN:
        raise ContractError("result.verifier.image: image must use immutable digest")
    image_id = _string(verifier["image_id"], "result.verifier.image_id")
    if not image_id.startswith("sha256:") or len(image_id) != 71:
        raise ContractError("result.verifier.image_id: invalid image ID")
    if not isinstance(verifier["commands"], list) or not all(
        isinstance(command, list) and command and all(isinstance(part, str) for part in command)
        for command in verifier["commands"]
    ):
        raise ContractError("result.verifier.commands: invalid argv list")
    if not isinstance(verifier["exit_codes"], list) or not all(type(code) is int for code in verifier["exit_codes"]):
        raise ContractError("result.verifier.exit_codes: invalid exit codes")
    if type(verifier["timed_out"]) is not bool or type(result["passed"]) is not bool:
        raise ContractError("result: timed_out and passed must be booleans")
    for field, hash_field in (("stdout", "stdout_sha256"), ("stderr", "stderr_sha256")):
        text = _string(verifier[field], f"result.verifier.{field}")
        if _sha(verifier[hash_field], f"result.verifier.{hash_field}") != sha256_text(text):
            raise ContractError(f"result.verifier: {field} hash mismatch")
    if type(verifier["duration_ms"]) is not int or verifier["duration_ms"] < 0:
        raise ContractError("result.verifier.duration_ms: invalid duration")
    _sha(verifier["sandbox_contract_sha256"], "result.verifier.sandbox_contract_sha256")
    expected_pass = (
        not verifier["timed_out"]
        and len(verifier["exit_codes"]) == len(verifier["commands"])
        and bool(verifier["exit_codes"])
        and all(code == 0 for code in verifier["exit_codes"])
    )
    if result["passed"] != expected_pass:
        raise ContractError("result.passed: inconsistent with verifier evidence")
    supplied_hash = _sha(result["result_sha256"], "result.result_sha256")
    unhashed = dict(result)
    del unhashed["result_sha256"]
    if supplied_hash != sha256_object(unhashed):
        raise ContractError("result.result_sha256: evidence hash mismatch")
    return result
