#!/usr/bin/env python3
"""Content-free separation audit of the exact 720+180 Gate 3 package."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.admit_expansion import _tokens, normalized_sha256, simhash
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_scale_queue import PRIOR_CORPUS_SHA256, source_key
from scripts.data.build_capability_separation_attestations import (
    PASS_FIELDS, _evaluation_files, _load_evaluation, _record_messages,
)
from scripts.eval.contracts import sha256_text


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sealed(path: Path, key: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    if body.pop(key, None) != canonical_sha256(body):
        raise ValueError(f"invalid sealed input: {path}")
    return value


def _rows(path: Path) -> list[dict[str, Any]]:
    data = path.read_bytes()
    if not data or not data.endswith(b"\n"):
        raise ValueError("JSONL input must be nonempty and newline terminated")
    rows = [json.loads(line) for line in data.splitlines()]
    if any(not isinstance(row, dict) for row in rows):
        raise ValueError("JSONL input includes a non-object")
    return rows


def _content(row: dict[str, Any]) -> tuple[str, list[str]]:
    messages = _record_messages(row)
    if [message["role"] for message in messages] != ["user", "assistant"]:
        raise ValueError("package row does not have one user and one assistant message")
    prompt, answer = (message["content"] for message in messages)
    values = [answer]
    task = row.get("verification_task")
    if task is not None:
        if not isinstance(task, dict):
            raise ValueError("malformed verification task")
        try:
            if task["prompt"]["text"] != prompt or task["validation"]["reference"]["code"] != answer:
                raise ValueError("verification task differs from training messages")
            values.extend(item["code"] for item in task["validation"]["known_bad"])
            values.extend(item["content"] for item in task["files"] if item.get("role") != "support")
        except (KeyError, TypeError) as exc:
            raise ValueError("incomplete verification task") from exc
    return prompt, list(dict.fromkeys(values))


def _index(rows: list[dict[str, Any]]) -> dict[str, set[Any]]:
    result: dict[str, set[Any]] = {key: set() for key in (
        "prompt_exact", "prompt_normalized", "prompt_fuzzy", "code_exact", "code_normalized",
    )}
    for row in rows:
        prompt, code = _content(row)
        result["prompt_exact"].add(sha256_text(prompt))
        result["prompt_normalized"].add(normalized_sha256(prompt))
        result["prompt_fuzzy"].add((simhash(prompt), len(_tokens(prompt))))
        result["code_exact"].update(sha256_text(value) for value in code)
        result["code_normalized"].update(normalized_sha256(value) for value in code)
    return result


def _against(prompt: str, code: list[str], index: dict[str, set[Any]]) -> tuple[bool, bool, bool]:
    exact = sha256_text(prompt) not in index["prompt_exact"] and all(sha256_text(value) not in index["code_exact"] for value in code)
    normalized = normalized_sha256(prompt) not in index["prompt_normalized"] and all(normalized_sha256(value) not in index["code_normalized"] for value in code)
    tokens = len(_tokens(prompt))
    fingerprint = simhash(prompt)
    fuzzy = tokens < 12 or not any(other_tokens >= 12 and (fingerprint ^ other).bit_count() <= 3 for other, other_tokens in index["prompt_fuzzy"])
    return exact, normalized, fuzzy


def build(
    capability_path: Path, capability_manifest_path: Path, replay_path: Path,
    replay_manifest_path: Path, prior_path: Path, evaluation_roots: list[Path],
) -> dict[str, Any]:
    capability_manifest = _sealed(capability_manifest_path, "manifest_sha256")
    replay_manifest = _sealed(replay_manifest_path, "manifest_sha256")
    if capability_manifest.get("status") != "passed" or capability_manifest.get("capability_rows_sha256") != _file_sha(capability_path):
        raise ValueError("capability rows are not the sealed 720 admission")
    if replay_manifest.get("capability_manifest_sha256") != capability_manifest["manifest_sha256"] or replay_manifest.get("replay_jsonl_sha256") != _file_sha(replay_path):
        raise ValueError("replay selection does not bind the sealed capability cohort")
    if _file_sha(prior_path) != PRIOR_CORPUS_SHA256:
        raise ValueError("prior corpus differs from frozen input")
    capability, replay, prior = _rows(capability_path), _rows(replay_path), _rows(prior_path)
    if (len(capability), len(replay), len(prior)) != (720, 180, 3225):
        raise ValueError("unexpected corpus size")
    package = capability + replay
    ids = [row.get("id") for row in package]
    if any(not isinstance(identifier, str) or not identifier for identifier in ids) or len(set(ids)) != 900:
        raise ValueError("package IDs are not unique")
    if len({source_key(row) for row in package}) != 900:
        raise ValueError("package sources are not unique")
    replay_ids = {row["id"] for row in replay}
    prior_by_id = {row["id"]: row for row in prior}
    if len(prior_by_id) != 3225 or any(prior_by_id.get(row["id"]) != row for row in replay):
        raise ValueError("replay rows are not byte-preserved prior records")
    prior_remaining = [row for row in prior if row["id"] not in replay_ids]
    if len(prior_remaining) != 3045:
        raise ValueError("prior-corpus leave-out count differs")
    for row in package:
        _content(row)
    previous = _index(prior_remaining)
    evaluation_paths = _evaluation_files(evaluation_roots)
    if len(evaluation_paths) != 540:
        raise ValueError("frozen evaluation surface is not 540 tasks")
    evaluation, eval_inputs = _load_evaluation(evaluation_paths)
    contents = {row["id"]: _content(row) for row in package}
    prompt_exact = Counter(sha256_text(contents[row["id"]][0]) for row in package)
    prompt_normalized = Counter(normalized_sha256(contents[row["id"]][0]) for row in package)
    code_exact = Counter(value for row in package for value in {sha256_text(code) for code in contents[row["id"]][1]})
    code_normalized = Counter(value for row in package for value in {normalized_sha256(code) for code in contents[row["id"]][1]})
    peer_fuzzy = [(row["id"], simhash(contents[row["id"]][0]), len(_tokens(contents[row["id"]][0]))) for row in package]
    records = []
    for row in package:
        identifier = row["id"]
        prompt, code = contents[identifier]
        training = list(_against(prompt, code, previous))
        if prompt_exact[sha256_text(prompt)] > 1 or any(code_exact[sha256_text(value)] > 1 for value in code):
            training[0] = False
        if prompt_normalized[normalized_sha256(prompt)] > 1 or any(code_normalized[normalized_sha256(value)] > 1 for value in code):
            training[1] = False
        tokens = len(_tokens(prompt))
        fingerprint = simhash(prompt)
        if tokens >= 12 and any(other_id != identifier and other_tokens >= 12 and
                                (fingerprint ^ other_hash).bit_count() <= 3
                                for other_id, other_hash, other_tokens in peer_fuzzy):
            training[2] = False
        eval_result = _against(prompt, code, evaluation)
        records.append({
            "id": identifier, "row_sha256": canonical_sha256(row),
            **dict(zip(PASS_FIELDS[:3], training, strict=True)),
            **dict(zip(PASS_FIELDS[3:], eval_result, strict=True)),
        })
    failures = Counter(field for row in records for field in PASS_FIELDS if row[field] is not True)
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-package-separation/v1",
        "status": "passed" if not failures else "failed",
        "package_rows_sha256": canonical_sha256(package),
        "capability_manifest_sha256": capability_manifest["manifest_sha256"],
        "replay_manifest_sha256": replay_manifest["manifest_sha256"],
        "input_file_sha256": {"capability": _file_sha(capability_path), "replay": _file_sha(replay_path), "prior": _file_sha(prior_path)},
        "comparison_counts": {"package": 900, "prior_after_replay_exclusion": 3045, "evaluation_tasks": 540, "failed_by_check": {field: failures[field] for field in PASS_FIELDS}},
        "comparison_policy": "exact/normalized prompt and authored code; prompt SimHash <=3 with >=12 tokens; package peers included; 180 exact replay rows excluded from prior comparison; support files excluded",
        "evaluation_artifacts_read_by_construction": 0,
        "comparison_stage_evaluation_artifacts_read": len(eval_inputs),
        "evaluation_input_digests": [{"sha256": item["sha256"], "bytes": item["bytes"]} for item in eval_inputs],
        "content_exposure": {"evaluation_content_serialized": 0, "evaluation_paths_or_task_ids_serialized": 0, "collision_identities_serialized": 0},
        "records": records,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("capability", "capability_manifest", "replay", "replay_manifest", "prior", "output"):
        parser.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    parser.add_argument("--evaluation-root", type=Path, action="append", required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("output already exists")
    report = build(args.capability, args.capability_manifest, args.replay, args.replay_manifest, args.prior, args.evaluation_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": report["status"], "records": 900, "failed_by_check": report["comparison_counts"]["failed_by_check"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
