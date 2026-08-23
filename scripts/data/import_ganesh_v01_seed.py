#!/usr/bin/env python3
"""Deterministically import the authorized Ganesh v0.1 seed from Git objects."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "ganesh-mini-qwen-messages/v1"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LANGUAGES = {
    "python": "Python",
    "go": "Go",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "rust": "Rust",
}


class ImportFailure(RuntimeError):
    """Raised when the source corpus violates the frozen import contract."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def normalized_text_fingerprint(text: str) -> str:
    normalized = " ".join(unicodedata.normalize("NFKC", text).casefold().split())
    return sha256(normalized.encode("utf-8"))


def git_blob(repo: Path, revision: str, source_path: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), "show", f"{revision}:{source_path}"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.decode("utf-8", errors="replace").strip()
        raise ImportFailure(f"cannot read committed source {source_path}: {detail}") from exc


def validate_messages(record: dict[str, Any], source_path: str, line_number: int) -> list[dict[str, str]]:
    messages = record.get("messages")
    location = f"{source_path}:{line_number}"
    if not isinstance(messages, list) or len(messages) != 2:
        raise ImportFailure(f"{location}: messages must contain exactly user and assistant turns")
    expected_roles = ("user", "assistant")
    normalized = []
    for index, (message, expected_role) in enumerate(zip(messages, expected_roles)):
        if not isinstance(message, dict) or set(message) != {"role", "content"}:
            raise ImportFailure(f"{location}: message {index} must contain only role and content")
        if message["role"] != expected_role or not isinstance(message["content"], str) or not message["content"]:
            raise ImportFailure(f"{location}: invalid {expected_role} message")
        normalized.append({"role": expected_role, "content": message["content"]})
    return normalized


def normalize_record(
    record: dict[str, Any],
    *,
    lane: str,
    split: str,
    source_path: str,
    source_revision: str,
    source_file_sha256: str,
    line_number: int,
    raw_line: bytes,
) -> dict[str, Any]:
    messages = validate_messages(record, source_path, line_number)
    record_id = record.get("id") or record.get("source_record_id")
    if not isinstance(record_id, str) or not record_id:
        raise ImportFailure(f"{source_path}:{line_number}: missing stable record ID")
    if record.get("source_record_id") not in (None, record_id):
        raise ImportFailure(f"{source_path}:{line_number}: id and source_record_id disagree")
    if record.get("language") != LANGUAGES[lane]:
        raise ImportFailure(f"{source_path}:{line_number}: expected language {LANGUAGES[lane]}")
    if not isinstance(record.get("task_type"), str) or not record["task_type"]:
        raise ImportFailure(f"{source_path}:{line_number}: missing task_type")

    source_metadata = {
        key: value
        for key, value in record.items()
        if key not in {"id", "language", "messages", "source_record_id", "task_type"}
    }
    user_sha256 = sha256(messages[0]["content"].encode("utf-8"))
    assistant_sha256 = sha256(messages[1]["content"].encode("utf-8"))
    if source_metadata.get("prompt_sha256", user_sha256) != user_sha256:
        raise ImportFailure(f"{source_path}:{line_number}: prompt_sha256 does not match user content")
    if source_metadata.get("teacher_answer_sha256", assistant_sha256) != assistant_sha256:
        raise ImportFailure(f"{source_path}:{line_number}: teacher_answer_sha256 does not match assistant content")
    return {
        "schema_version": SCHEMA_VERSION,
        "id": record_id,
        "language": LANGUAGES[lane],
        "lane": lane,
        "split": split,
        "task_type": record["task_type"],
        "messages": messages,
        "source_metadata": source_metadata,
        "lineage": {
            "source_repository": "ganesh",
            "source_revision": source_revision,
            "source_path": source_path,
            "source_line": line_number,
            "source_file_sha256": source_file_sha256,
            "source_record_sha256": sha256(raw_line),
            "source_record_id": record.get("source_record_id", record_id),
        },
        "content_hashes": {
            "user_sha256": user_sha256,
            "assistant_sha256": assistant_sha256,
            "user_normalized_sha256": normalized_text_fingerprint(messages[0]["content"]),
        },
    }


def duplicate_report(records: list[dict[str, Any]]) -> dict[str, Any]:
    indexes: dict[str, dict[str, list[str]]] = {
        "record_id": defaultdict(list),
        "user_exact": defaultdict(list),
        "user_normalized": defaultdict(list),
        "conversation_exact": defaultdict(list),
    }
    for record in records:
        record_id = record["id"]
        indexes["record_id"][record_id].append(record_id)
        indexes["user_exact"][record["content_hashes"]["user_sha256"]].append(record_id)
        indexes["user_normalized"][record["content_hashes"]["user_normalized_sha256"]].append(record_id)
        conversation = canonical_json(record["messages"])
        indexes["conversation_exact"][sha256(conversation)].append(record_id)
    return {
        name: [
            {"fingerprint": fingerprint, "record_ids": record_ids}
            for fingerprint, record_ids in sorted(groups.items())
            if len(record_ids) > 1
        ]
        for name, groups in indexes.items()
    }


def evaluation_fingerprints(paths: Iterable[Path]) -> tuple[set[str], list[str]]:
    fingerprints: set[str] = set()
    inspected: list[str] = []
    for path in paths:
        inspected.append(str(path))
        raw = path.read_text(encoding="utf-8")
        values: list[Any]
        try:
            decoded = json.loads(raw)
            values = decoded if isinstance(decoded, list) else [decoded]
        except json.JSONDecodeError:
            values = [json.loads(line) for line in raw.splitlines() if line.strip()]
        for value in values:
            if not isinstance(value, dict):
                continue
            prompt = value.get("prompt")
            if isinstance(prompt, dict):
                prompt = prompt.get("text")
            if prompt is None and isinstance(value.get("messages"), list):
                prompt = next((m.get("content") for m in value["messages"] if m.get("role") == "user"), None)
            if isinstance(prompt, str):
                fingerprints.add(normalized_text_fingerprint(prompt))
    return fingerprints, inspected


def run_import(config_path: Path, output_root: Path, manifest_path: Path, evaluation_paths: Iterable[Path] = (), separation_report: Path | None = None, compatibility_report: Path | None = None) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    repo = Path(config["source"]["repository"])
    if not repo.is_absolute():
        repo = PROJECT_ROOT / repo
    revision = config["source"]["revision"]
    records_by_split: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_manifest = []

    for source in config["sources"]:
        blob = git_blob(repo, revision, source["path"])
        actual_sha = sha256(blob)
        if actual_sha != source["sha256"]:
            raise ImportFailure(f"{source['path']}: source SHA-256 mismatch ({actual_sha})")
        lines = blob.splitlines()
        if len(lines) != source["records"]:
            raise ImportFailure(f"{source['path']}: expected {source['records']} records, found {len(lines)}")
        for line_number, raw_line in enumerate(lines, 1):
            try:
                original = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ImportFailure(f"{source['path']}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(original, dict):
                raise ImportFailure(f"{source['path']}:{line_number}: record is not an object")
            records_by_split[source["split"]].append(normalize_record(
                original,
                lane=source["lane"],
                split=source["split"],
                source_path=source["path"],
                source_revision=revision,
                source_file_sha256=actual_sha,
                line_number=line_number,
                raw_line=raw_line,
            ))
        source_manifest.append({**source, "bytes": len(blob)})

    all_records = records_by_split["train"] + records_by_split["validation"]
    duplicates = duplicate_report(all_records)
    if duplicates["record_id"]:
        raise ImportFailure("duplicate record IDs found")
    if duplicates["conversation_exact"]:
        raise ImportFailure("exact duplicate conversations found")

    eval_fingerprints, eval_inputs = evaluation_fingerprints(evaluation_paths)
    overlaps = sorted(
        record["id"] for record in all_records
        if record["content_hashes"]["user_normalized_sha256"] in eval_fingerprints
    )
    if overlaps:
        raise ImportFailure(f"evaluation overlap found in {len(overlaps)} seed records")

    output_root.mkdir(parents=True, exist_ok=True)
    output_files: dict[str, dict[str, Any]] = {}
    for split in ("train", "validation"):
        output_path = output_root / f"{split}.jsonl"
        payload = b"".join(canonical_json(record) for record in records_by_split[split])
        output_path.write_bytes(payload)
        output_files[split] = {
            "path": str(output_path),
            "records": len(records_by_split[split]),
            "bytes": len(payload),
            "sha256": sha256(payload),
        }

    counts = {
        split: dict(sorted(Counter(record["lane"] for record in split_records).items()))
        for split, split_records in sorted(records_by_split.items())
    }
    separation = None
    if separation_report is not None:
        report = json.loads(separation_report.read_text(encoding="utf-8"))
        claimed = report.get("report_sha256") or report.get("evidence_sha256") or report.get("manifest_sha256")
        unsigned = dict(report); unsigned.pop("report_sha256",None); unsigned.pop("evidence_sha256",None); unsigned.pop("manifest_sha256",None)
        if claimed != sha256(json.dumps(unsigned,sort_keys=True,separators=(",", ":")).encode()):
            raise ImportFailure("global evaluation separation report seal is invalid")
        if report.get("counts",{}).get("seed_records") != len(all_records):
            raise ImportFailure("global evaluation separation report seed count mismatch")
        separation = {"path":str(separation_report),"sha256":sha256(separation_report.read_bytes()),"seal":claimed}
    compatibility = None
    if compatibility_report is not None:
        report = json.loads(compatibility_report.read_text(encoding="utf-8")); claimed=report.get("evidence_sha256"); unsigned=dict(report); unsigned.pop("evidence_sha256",None)
        if claimed != sha256(json.dumps(unsigned,sort_keys=True,separators=(",", ":")).encode()) or report.get("status") != "passed" or len(report.get("records",[])) != len(all_records):
            raise ImportFailure("current-toolchain compatibility evidence is invalid or incomplete")
        compatibility={"status":"passed","scope":report["scope"],"path":str(compatibility_report),"sha256":sha256(compatibility_report.read_bytes()),"seal":claimed,"records":len(report["records"])}
    manifest = {
        "schema_version": "ganesh-mini-seed-manifest/v1",
        "source_repository": "ganesh",
        "source_revision": revision,
        "source_files": source_manifest,
        "outputs": output_files,
        "counts_by_split_and_lane": counts,
        "total_records": len(all_records),
        "integrity": {
            "schema_validation": "passed",
            "source_hash_validation": "passed",
            "record_id_duplicates": len(duplicates["record_id"]),
            "exact_conversation_duplicates": len(duplicates["conversation_exact"]),
            "exact_user_duplicate_groups": len(duplicates["user_exact"]),
            "normalized_user_duplicate_groups": len(duplicates["user_normalized"]),
        },
        "duplicates": duplicates,
        "evaluation_overlap": {
            "status": "passed" if eval_inputs else "not_run_no_evaluation_manifests",
            "inputs": eval_inputs,
            "normalized_prompt_overlaps": overlaps,
            "global_separation": separation,
        },
        "compatibility": {
            "qwen_messages_schema": "passed",
            "current_language_toolchain_execution": compatibility or "not_run_no_compatibility_report"
        },
    }
    manifest["manifest_sha256"] = sha256(json.dumps(manifest,ensure_ascii=False,sort_keys=True,separators=(",", ":")).encode())
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_bytes(canonical_json(manifest))
    return manifest


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/data/ganesh_v01_seed.json"))
    parser.add_argument("--output-root", type=Path, default=Path("data/seed/ganesh_v01"))
    parser.add_argument("--manifest", type=Path, default=Path("manifests/datasets/ganesh_v01_seed.json"))
    parser.add_argument("--evaluation-manifest", action="append", type=Path, default=[])
    parser.add_argument("--separation-report", type=Path)
    parser.add_argument("--compatibility-report", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        manifest = run_import(args.config, args.output_root, args.manifest, args.evaluation_manifest, args.separation_report, args.compatibility_report)
    except (ImportFailure, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"seed import failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"total_records": manifest["total_records"], "outputs": manifest["outputs"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
