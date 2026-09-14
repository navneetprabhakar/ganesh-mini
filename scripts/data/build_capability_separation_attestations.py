#!/usr/bin/env python3
"""Build content-free separation attestations for Gate 2 candidates.

This is the only capability-qualification construction stage allowed to read
frozen evaluation artifacts.  Its output deliberately contains only aggregate
input identities/counts and per-candidate pass/fail bits; evaluation text,
code, paths, task IDs, and collision identities are never serialized.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_expansion import (  # noqa: E402
    RECORD_KEYS,
    _tokens,
    canonical_json,
    evaluation_index,
    normalized_sha256,
    read_jsonl,
    simhash,
)
from scripts.eval.contracts import sha256_text  # noqa: E402
from scripts.eval.contracts import validate_task  # noqa: E402


SCHEMA_VERSION = "ganesh-mini-capability-separation-attestation/v1"
MANIFEST_SCHEMA_VERSION = "ganesh-mini-capability-separation-comparison-manifest/v1"
PASS_FIELDS = (
    "exact_training_passed",
    "normalized_training_passed",
    "fuzzy_training_passed",
    "exact_evaluation_passed",
    "normalized_evaluation_passed",
    "fuzzy_evaluation_passed",
)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _physical_jsonl(path: Path) -> list[Any]:
    try:
        return read_jsonl(path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSONL input: {path}") from exc


def _base_candidate(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict) or not RECORD_KEYS.issubset(raw):
        raise ValueError("candidate does not contain the expansion record contract")
    candidate = {key: raw[key] for key in RECORD_KEYS}
    if not isinstance(candidate.get("id"), str) or not candidate["id"]:
        raise ValueError("candidate id must be non-empty")
    messages = candidate.get("messages")
    task = candidate.get("verification_task")
    if (
        not isinstance(messages, list)
        or len(messages) != 2
        or [message.get("role") for message in messages if isinstance(message, dict)] != ["user", "assistant"]
        or not all(isinstance(message.get("content"), str) and message["content"] for message in messages)
        or not isinstance(task, dict)
    ):
        raise ValueError(f"{candidate['id']}: malformed messages or verification task")
    try:
        prompt = task["prompt"]["text"]
        reference = task["validation"]["reference"]
        known_bad = task["validation"]["known_bad"]
        files = task["files"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"{candidate['id']}: incomplete verification task") from exc
    if prompt != messages[0]["content"] or reference.get("code") != messages[1]["content"]:
        raise ValueError(f"{candidate['id']}: messages differ from verification task")
    if not isinstance(known_bad, list) or not known_bad or not isinstance(files, list) or not files:
        raise ValueError(f"{candidate['id']}: tests/files and known-bad code are required")
    try:
        validate_task({**task, "surface": "synthetic_harness"})
    except ValueError as exc:
        raise ValueError(f"{candidate['id']}: invalid verification task: {exc}") from exc
    for label, item in [
        ("reference", reference),
        *[("known_bad", item) for item in known_bad],
        *[("file", item) for item in files],
    ]:
        field = "content" if label == "file" else "code"
        if not isinstance(item, dict) or not isinstance(item.get(field), str) or not item[field]:
            raise ValueError(f"{candidate['id']}: malformed {label} code")
        if item.get("sha256") != sha256_text(item[field]):
            raise ValueError(f"{candidate['id']}: {label} code hash mismatch")
    return candidate


def _record_messages(raw: Any) -> list[dict[str, Any]]:
    """Extract messages from admitted, wrapped, or generated training rows."""
    if not isinstance(raw, dict):
        raise ValueError("training corpus row is not an object")
    for value in (raw, raw.get("record"), raw.get("candidate"), raw.get("training_candidate")):
        if isinstance(value, dict) and isinstance(value.get("messages"), list):
            messages = value["messages"]
            if not messages or any(
                not isinstance(item, dict)
                or not isinstance(item.get("role"), str)
                or not isinstance(item.get("content"), str)
                or not item["content"]
                for item in messages
            ):
                break
            return messages
    raise ValueError("training corpus row has no valid messages")


def _code_values(candidate: dict[str, Any]) -> list[str]:
    task = candidate["verification_task"]
    values = [candidate["messages"][1]["content"], task["validation"]["reference"]["code"]]
    values.extend(item["code"] for item in task["validation"]["known_bad"])
    values.extend(item["content"] for item in task["files"])
    # Preserve order while removing the duplicated assistant/reference value.
    return list(dict.fromkeys(values))


def _load_training(paths: Iterable[Path]) -> tuple[dict[str, set[Any]], list[dict[str, Any]]]:
    index: dict[str, set[Any]] = {
        "prompt_exact": set(), "prompt_normalized": set(), "prompt_fuzzy": set(),
        "code_exact": set(), "code_normalized": set(),
    }
    inputs: list[dict[str, Any]] = []
    input_ordinal = 0
    for path in paths:
        files = sorted(path.rglob("*.jsonl")) if path.is_dir() else [path]
        if not files:
            raise ValueError(f"training corpus input contains no JSONL files: {path}")
        for source in files:
            rows = _physical_jsonl(source)
            if not rows:
                raise ValueError(f"training corpus file is empty: {source}")
            for raw in rows:
                messages = _record_messages(raw)
                prompts = [item["content"] for item in messages if item["role"] == "user"]
                code = [item["content"] for item in messages if item["role"] == "assistant"]
                if not prompts or not code:
                    raise ValueError("training corpus row must contain user and assistant messages")
                for prompt in prompts:
                    index["prompt_exact"].add(sha256_text(prompt))
                    index["prompt_normalized"].add(normalized_sha256(prompt))
                    index["prompt_fuzzy"].add((simhash(prompt), len(_tokens(prompt))))
                for value in code:
                    index["code_exact"].add(sha256_text(value))
                    index["code_normalized"].add(normalized_sha256(value))
            inputs.append({
                "kind": "training_jsonl", "ordinal": input_ordinal,
                "sha256": file_sha256(source), "bytes": source.stat().st_size, "records": len(rows),
            })
            input_ordinal += 1
    if not inputs:
        raise ValueError("at least one prior training corpus is required")
    return index, inputs


def _evaluation_files(paths: Iterable[Path]) -> list[Path]:
    result: list[Path] = []
    for path in paths:
        files = sorted(path.rglob("*.task.json")) if path.is_dir() else [path]
        result.extend(files)
    if not result:
        raise ValueError("at least one frozen evaluation task is required")
    if len(set(result)) != len(result):
        raise ValueError("evaluation roots contain duplicate task files")
    return result


def _load_evaluation(paths: list[Path]) -> tuple[dict[str, set[Any]], list[dict[str, Any]]]:
    # Reuse the frozen contract validator and exact code index from admission.
    base = evaluation_index(paths)
    index: dict[str, set[Any]] = {
        "prompt_exact": set(), "prompt_normalized": set(base["prompts"]),
        "prompt_fuzzy": {(value, tokens) for value, _source, tokens in base["prompt_simhashes"]},
        "code_exact": set(base["code_hashes"]), "code_normalized": set(),
    }
    inputs: list[dict[str, Any]] = []
    for ordinal, path in enumerate(paths):
        try:
            task = json.loads(path.read_text(encoding="utf-8"))
            prompt = task["prompt"]["text"]
            code_items = [task["validation"]["reference"], *task["validation"]["known_bad"], *task["files"]]
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
            raise ValueError(f"invalid evaluation task: {path}") from exc
        index["prompt_exact"].add(sha256_text(prompt))
        for item in code_items:
            value = item["content"] if "content" in item else item["code"]
            index["code_normalized"].add(normalized_sha256(value))
        inputs.append({
            "kind": "evaluation_task", "ordinal": ordinal,
            "sha256": file_sha256(path), "bytes": path.stat().st_size,
        })
    return index, inputs


def _fuzzy_overlap(prompt: str, values: set[Any], limit: int, minimum_tokens: int) -> bool:
    count = len(_tokens(prompt))
    if count < minimum_tokens:
        return False
    fingerprint = simhash(prompt)
    return any(
        other_tokens >= minimum_tokens and (fingerprint ^ other).bit_count() <= limit
        for other, other_tokens in values
    )


def _surface_results(
    candidate: dict[str, Any], index: dict[str, set[Any]], fuzzy_limit: int, minimum_tokens: int,
) -> tuple[bool, bool, bool]:
    prompt = candidate["messages"][0]["content"]
    code = _code_values(candidate)
    exact = sha256_text(prompt) not in index["prompt_exact"] and all(
        sha256_text(value) not in index["code_exact"] for value in code
    )
    normalized = normalized_sha256(prompt) not in index["prompt_normalized"] and all(
        normalized_sha256(value) not in index["code_normalized"] for value in code
    )
    fuzzy = not _fuzzy_overlap(prompt, index["prompt_fuzzy"], fuzzy_limit, minimum_tokens)
    return exact, normalized, fuzzy


def build_report(
    candidate_path: Path,
    training_paths: list[Path],
    evaluation_roots: list[Path],
    fuzzy_limit: int = 3,
    minimum_tokens: int = 12,
) -> dict[str, Any]:
    if fuzzy_limit < 0 or minimum_tokens <= 0:
        raise ValueError("fuzzy limit must be non-negative and minimum tokens positive")
    raw_candidates = _physical_jsonl(candidate_path)
    if not raw_candidates:
        raise ValueError("candidate input is empty")
    candidates = [_base_candidate(raw) for raw in raw_candidates]
    identifiers = [candidate["id"] for candidate in candidates]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("candidate IDs are duplicated")

    training, training_inputs = _load_training(training_paths)
    evaluation_paths = _evaluation_files(evaluation_roots)
    evaluation, evaluation_inputs = _load_evaluation(evaluation_paths)

    # Peer candidates form part of the prospective training surface.  Mark
    # every participant in a collision, independent of input order.
    prompt_exact = Counter(sha256_text(item["messages"][0]["content"]) for item in candidates)
    prompt_normalized = Counter(normalized_sha256(item["messages"][0]["content"]) for item in candidates)
    code_exact = Counter(value for item in candidates for value in {sha256_text(v) for v in _code_values(item)})
    code_normalized = Counter(value for item in candidates for value in {normalized_sha256(v) for v in _code_values(item)})
    peer_fuzzy = [(item["id"], simhash(item["messages"][0]["content"]), len(_tokens(item["messages"][0]["content"]))) for item in candidates]

    records: list[dict[str, Any]] = []
    for candidate in candidates:
        identifier = candidate["id"]
        prompt = candidate["messages"][0]["content"]
        code = _code_values(candidate)
        training_result = list(_surface_results(candidate, training, fuzzy_limit, minimum_tokens))
        if prompt_exact[sha256_text(prompt)] > 1 or any(code_exact[sha256_text(value)] > 1 for value in code):
            training_result[0] = False
        if prompt_normalized[normalized_sha256(prompt)] > 1 or any(code_normalized[normalized_sha256(value)] > 1 for value in code):
            training_result[1] = False
        prompt_tokens = len(_tokens(prompt))
        if prompt_tokens >= minimum_tokens and any(
            other_id != identifier
            and other_tokens >= minimum_tokens
            and (simhash(prompt) ^ other_hash).bit_count() <= fuzzy_limit
            for other_id, other_hash, other_tokens in peer_fuzzy
        ):
            training_result[2] = False
        evaluation_result = _surface_results(candidate, evaluation, fuzzy_limit, minimum_tokens)
        records.append({
            "id": identifier,
            "candidate_sha256": canonical_sha256(candidate),
            **dict(zip(PASS_FIELDS[:3], training_result, strict=True)),
            **dict(zip(PASS_FIELDS[3:], evaluation_result, strict=True)),
        })

    failures = Counter(field for row in records for field in PASS_FIELDS if row[field] is not True)
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "policy": {
            "exact": "raw SHA-256 equality for prompts and all candidate reference/test/known-bad code",
            "normalized": "NFKC casefolded whitespace-normalized SHA-256 equality for prompts and code",
            "fuzzy": "prompt SimHash only, including peer candidates",
            "prompt_simhash_max_hamming": fuzzy_limit,
            "minimum_fuzzy_tokens": minimum_tokens,
            "peer_candidate_comparison": True,
            "fail_closed": True,
        },
        "candidate_input": {
            "sha256": file_sha256(candidate_path), "bytes": candidate_path.stat().st_size,
            "records": len(candidates),
        },
        "training_inputs": training_inputs,
        "evaluation_inputs": evaluation_inputs,
        "comparison_counts": {
            "candidates": len(candidates),
            "prior_training_records": sum(item["records"] for item in training_inputs),
            "evaluation_tasks": len(evaluation_inputs),
            "failed_by_check": {field: failures.get(field, 0) for field in PASS_FIELDS},
        },
        "content_exposure": {
            "evaluation_content_serialized": 0,
            "evaluation_paths_or_task_ids_serialized": 0,
            "collision_identities_serialized": 0,
        },
    }
    comparison_manifest_sha256 = canonical_sha256(manifest)
    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": "passed" if not failures else "failed",
        "evaluation_artifacts_read_by_construction": 0,
        "comparison_stage_evaluation_artifacts_read": len(evaluation_inputs),
        "comparison_manifest": manifest,
        "comparison_manifest_sha256": comparison_manifest_sha256,
        "records": records,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--training-corpus", type=Path, action="append", required=True)
    parser.add_argument("--evaluation-root", type=Path, action="append", required=True)
    parser.add_argument("--prompt-simhash-max-hamming", type=int, default=3)
    parser.add_argument("--minimum-fuzzy-tokens", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    report = build_report(
        args.candidates, args.training_corpus, args.evaluation_root,
        args.prompt_simhash_max_hamming, args.minimum_fuzzy_tokens,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"], "records": len(report["records"]),
        "comparison_manifest_sha256": report["comparison_manifest_sha256"],
    }, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
