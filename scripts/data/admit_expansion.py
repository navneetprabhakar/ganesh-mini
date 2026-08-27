#!/usr/bin/env python3
"""Fail-closed admission for execution-verified multilingual SFT expansion rows."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

from scripts.eval.contracts import ContractError, sha256_object, sha256_text, validate_task
from scripts.verify.sandbox import infrastructure_failure, verify


SCHEMA_VERSION = "ganesh-mini-expansion-candidate/v1"
LANES = {"go", "java", "javascript", "typescript", "python", "rust"}
LANGUAGE_NAMES = {"go": "Go", "java": "Java", "javascript": "JavaScript", "typescript": "TypeScript", "python": "Python", "rust": "Rust"}
TASK_TYPES = {"generation", "repair"}
RECORD_KEYS = {
    "schema_version", "id", "lane", "task_type", "messages", "source",
    "rights", "verification_task", "test_origin",
}
SOURCE_KEYS = {
    "dataset", "uri", "revision", "record_id", "license", "license_uri",
    "source_record_sha256", "transformation",
}


class AdmissionFailure(ValueError):
    """Raised when an expansion candidate violates the frozen contract."""

    def __init__(self, message: str, evidence: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.evidence = evidence


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def normalized_text(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def normalized_sha256(value: str) -> str:
    return hashlib.sha256(normalized_text(value).encode()).hexdigest()


def _tokens(value: str) -> list[str]:
    token = ""
    tokens: list[str] = []
    for char in normalized_text(value):
        if char.isalnum() or char == "_":
            token += char
        elif token:
            tokens.append(token)
            token = ""
    if token:
        tokens.append(token)
    return tokens


def simhash(value: str) -> int:
    weights = [0] * 64
    tokens = _tokens(value)
    features = tokens if len(tokens) < 5 else [" ".join(tokens[index:index + 5]) for index in range(len(tokens) - 4)]
    for feature in features:
        digest = int.from_bytes(hashlib.sha256(feature.encode()).digest()[:8], "big")
        for bit in range(64):
            weights[bit] += 1 if digest & (1 << bit) else -1
    return sum((1 << bit) for bit, weight in enumerate(weights) if weight >= 0)


def _sha(value: Any, where: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise AdmissionFailure(f"{where}: expected lowercase SHA-256")
    return value


def evaluation_index(paths: Iterable[Path]) -> dict[str, Any]:
    prompts: dict[str, str] = {}
    prompt_simhashes: list[tuple[int, str, int]] = []
    code_hashes: dict[str, str] = {}
    inspected: list[str] = []
    for root in paths:
        candidates = sorted(root.rglob("*.task.json")) if root.is_dir() else [root]
        for path in candidates:
            task = json.loads(path.read_text(encoding="utf-8"))
            validate_task(task)
            inspected.append(str(path))
            prompt = task["prompt"]["text"]
            prompts.setdefault(normalized_sha256(prompt), str(path))
            prompt_simhashes.append((simhash(prompt), str(path), len(_tokens(prompt))))
            values = [task["validation"]["reference"], *task["validation"]["known_bad"]]
            for value in values:
                code_hashes.setdefault(value["sha256"], str(path))
            for item in task["files"]:
                code_hashes.setdefault(item["sha256"], str(path))
    return {"prompts": prompts, "prompt_simhashes": prompt_simhashes, "code_hashes": code_hashes, "inspected": inspected}


def validate_candidate(record: Any, config: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != RECORD_KEYS:
        raise AdmissionFailure("record keys do not match expansion candidate contract")
    if record["schema_version"] != SCHEMA_VERSION:
        raise AdmissionFailure("unsupported candidate schema")
    if not isinstance(record["id"], str) or not record["id"]:
        raise AdmissionFailure("id must be non-empty")
    if record["lane"] not in LANES or record["task_type"] not in TASK_TYPES:
        raise AdmissionFailure("unknown lane or task type")
    messages = record["messages"]
    if not isinstance(messages, list) or len(messages) != 2 or [message.get("role") for message in messages if isinstance(message, dict)] != ["user", "assistant"]:
        raise AdmissionFailure("messages must be exactly user then assistant")
    if any(set(message) != {"role", "content"} or not isinstance(message["content"], str) or not message["content"] for message in messages):
        raise AdmissionFailure("invalid message content")
    source = record["source"]
    if not isinstance(source, dict) or set(source) != SOURCE_KEYS:
        raise AdmissionFailure("source keys do not match provenance contract")
    if any(not isinstance(source[key], str) or not source[key] for key in SOURCE_KEYS - {"source_record_sha256"}):
        raise AdmissionFailure("source provenance fields must be non-empty")
    _sha(source["source_record_sha256"], "source.source_record_sha256")
    configured_source = config.get("sources", {}).get(source["dataset"])
    if not isinstance(configured_source, dict) or configured_source.get("revision") != source["revision"]:
        raise AdmissionFailure("source dataset/revision is not admitted")
    if source["license"] not in config["allowed_licenses"] or configured_source.get("license") != source["license"]:
        raise AdmissionFailure("source license is not admitted")
    rights = record["rights"]
    if not isinstance(rights, dict) or set(rights) != set(config["required_rights"]) or not all(value is True for value in rights.values()):
        raise AdmissionFailure("all required rights must be explicitly true")
    if record["test_origin"] not in config["allowed_test_origins"]:
        raise AdmissionFailure("behavioral tests are not independent")
    task = record["verification_task"]
    if not isinstance(task, dict) or task.get("surface") != "training_admission":
        raise AdmissionFailure("verification task must use the training_admission surface")
    validation_task = {**task, "surface": "synthetic_harness"}
    try:
        validate_task(validation_task)
    except ContractError as exc:
        raise AdmissionFailure(str(exc)) from exc
    if task["task_id"] != record["id"]:
        raise AdmissionFailure("verification task must be training-only and share the record ID")
    if task["language"] != record["lane"] or task["task_type"] != record["task_type"]:
        raise AdmissionFailure("verification task lane/type mismatch")
    if task["prompt"]["text"] != messages[0]["content"] or task["validation"]["reference"]["code"] != messages[1]["content"]:
        raise AdmissionFailure("messages differ from verified prompt/reference")
    if not task["validation"]["known_bad"]:
        raise AdmissionFailure("at least one known-bad implementation is required")
    return record


def admit_records(
    records: Iterable[Any], config: dict[str, Any], eval_index: dict[str, Any],
    runtime_config: Path, verifier: Callable[[dict[str, Any], str, Path], dict[str, Any]] = verify,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_prompts: set[str] = set()
    seen_conversations: set[str] = set()
    seen_prompt_simhashes: list[tuple[int, str, int]] = []
    fuzzy_limit = config["deduplication"]["prompt_simhash_max_hamming"]
    minimum_tokens = config["deduplication"]["minimum_fuzzy_tokens"]
    for line_number, raw_record in enumerate(records, 1):
        record_id = raw_record.get("id", f"line-{line_number}") if isinstance(raw_record, dict) else f"line-{line_number}"
        try:
            record = validate_candidate(raw_record, config)
            prompt = record["messages"][0]["content"]
            answer = record["messages"][1]["content"]
            prompt_hash = normalized_sha256(prompt)
            conversation_hash = hashlib.sha256(canonical_json(record["messages"])).hexdigest()
            if record["id"] in seen_ids or prompt_hash in seen_prompts or conversation_hash in seen_conversations:
                raise AdmissionFailure("duplicate within expansion candidates")
            if prompt_hash in eval_index["prompts"]:
                raise AdmissionFailure(f"exact evaluation prompt overlap: {eval_index['prompts'][prompt_hash]}")
            if sha256_text(answer) in eval_index["code_hashes"]:
                raise AdmissionFailure(f"exact evaluation code overlap: {eval_index['code_hashes'][sha256_text(answer)]}")
            task = record["verification_task"]
            candidate_code = [*task["validation"]["known_bad"], *task["files"]]
            for value in candidate_code:
                if value["sha256"] in eval_index["code_hashes"]:
                    raise AdmissionFailure(f"exact evaluation harness/code overlap: {eval_index['code_hashes'][value['sha256']]}")
            prompt_tokens = len(_tokens(prompt))
            if prompt_tokens >= minimum_tokens:
                candidate_simhash = simhash(prompt)
                for other_hash, source, other_tokens in eval_index["prompt_simhashes"]:
                    if other_tokens >= minimum_tokens and (candidate_simhash ^ other_hash).bit_count() <= fuzzy_limit:
                        raise AdmissionFailure(f"fuzzy evaluation prompt overlap: {source}")
                for other_hash, source_id, other_tokens in seen_prompt_simhashes:
                    if other_tokens >= minimum_tokens and (candidate_simhash ^ other_hash).bit_count() <= fuzzy_limit:
                        raise AdmissionFailure(f"fuzzy expansion prompt overlap: {source_id}")
            executable_task = {**task, "surface": "synthetic_harness"}
            reference_result = verifier(executable_task, answer, runtime_config)
            infrastructure = infrastructure_failure(reference_result)
            if infrastructure:
                raise AdmissionFailure(
                    f"reference verifier infrastructure failure: {infrastructure}",
                    {"reference": reference_result},
                )
            if reference_result["timed_out"] or any(code != 0 for code in reference_result["exit_codes"]):
                raise AdmissionFailure(
                    "reference solution failed behavioral verification",
                    {"reference": reference_result},
                )
            known_bad_results = []
            for known_bad in task["validation"]["known_bad"]:
                result = verifier(executable_task, known_bad["code"], runtime_config)
                infrastructure = infrastructure_failure(result)
                if infrastructure:
                    raise AdmissionFailure(
                        f"known-bad verifier infrastructure failure: {infrastructure}",
                        {"reference": reference_result, "known_bad": [{"label": known_bad["label"], "result": result}]},
                    )
                if not result["timed_out"] and result["exit_codes"] and all(code == 0 for code in result["exit_codes"]):
                    raise AdmissionFailure(
                        f"tests accepted known-bad implementation: {known_bad['label']}",
                        {"reference": reference_result, "known_bad": [{"label": known_bad["label"], "result": result}]},
                    )
                known_bad_results.append({"label": known_bad["label"], "result": result})
            evidence = {
                "schema_version": "ganesh-mini-expansion-verification/v1",
                "task_sha256": sha256_object(task),
                "reference": reference_result,
                "known_bad": known_bad_results,
            }
            evidence["evidence_sha256"] = sha256_object(evidence)
            admitted = {
                "schema_version": "ganesh-mini-qwen-messages/v1",
                "id": record["id"], "language": LANGUAGE_NAMES[record["lane"]], "lane": record["lane"],
                "split": "train", "task_type": record["task_type"], "messages": record["messages"],
                "lineage": record["source"], "rights": record["rights"],
                "content_hashes": {
                    "user_sha256": sha256_text(prompt), "assistant_sha256": sha256_text(answer),
                    "user_normalized_sha256": prompt_hash, "conversation_sha256": conversation_hash,
                    "test_sha256s": [item["sha256"] for item in task["files"]],
                },
                "verification": evidence,
            }
            accepted.append(admitted)
            seen_ids.add(record["id"]); seen_prompts.add(prompt_hash); seen_conversations.add(conversation_hash)
            if prompt_tokens >= minimum_tokens:
                seen_prompt_simhashes.append((simhash(prompt), record["id"], prompt_tokens))
        except (AdmissionFailure, ContractError, KeyError, TypeError, ValueError) as exc:
            rejection = {"line": line_number, "id": record_id, "reason": str(exc)}
            if isinstance(exc, AdmissionFailure) and exc.evidence is not None:
                rejection["evidence"] = exc.evidence
            rejected.append(rejection)
    return accepted, rejected


def read_jsonl(path: Path) -> list[Any]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/data/expansion_v1.json"))
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--evaluation-root", type=Path, action="append", default=[])
    parser.add_argument("--runtime-config", type=Path, default=Path("configs/eval/runtimes.json"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--seal", action="store_true", help="require the complete frozen 6,000-row balance before succeeding")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    roots = args.evaluation_root or [Path("eval")]
    index = evaluation_index(roots)
    accepted, rejected = admit_records(read_jsonl(args.input), config, index, args.runtime_config)
    lane_counts = Counter(row["lane"] for row in accepted)
    type_counts = Counter(row["task_type"] for row in accepted)
    balance_passed = (
        len(accepted) == config["target_records"]
        and dict(lane_counts) == config["lane_targets"]
        and dict(type_counts) == config["task_type_targets"]
    )
    status = "passed" if not rejected and (balance_passed or not args.seal) else "failed"
    payload = b"".join(canonical_json(row) + b"\n" for row in accepted)
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_bytes(payload)
    report = {
        "schema_version": "ganesh-mini-expansion-admission/v1", "status": status,
        "mode": "sealed" if args.seal else "candidate", "input": str(args.input),
        "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "evaluation_files_inspected": len(index["inspected"]),
        "accepted": len(accepted), "rejected": rejected,
        "counts_by_lane": dict(sorted(lane_counts.items())),
        "counts_by_task_type": dict(sorted(type_counts.items())),
        "balance_passed": balance_passed,
        "output": {"path": str(args.output), "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()},
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    report["report_sha256"] = sha256_object(report)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "accepted": len(accepted), "rejected": len(rejected), "balance_passed": balance_passed}, sort_keys=True))
    return 0 if status == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
