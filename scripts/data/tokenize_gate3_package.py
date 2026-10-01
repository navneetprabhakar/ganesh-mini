#!/usr/bin/env python3
"""Measure untruncated Gate 3 package tokens and the frozen lane objective."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_separation_attestations import PASS_FIELDS
from scripts.train.prepare_seed import attach_objective_weights
from scripts.train.response_only import ResponseOnlyError, build_response_only_encoding


ROOT = Path(__file__).resolve().parents[2]
MODEL_REVISION = "15852e8c16360a2fea060d615a32b45270f8a8fc"
TARGETS = {"go": .2, "java": .2, "javascript": .1, "typescript": .1, "python": .2, "rust": .2}


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sealed(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    if body.pop("report_sha256", None) != canonical_sha256(body):
        raise ValueError("separation report seal differs")
    return value


def _rows(path: Path) -> list[dict]:
    data = path.read_bytes()
    if not data or not data.endswith(b"\n"):
        raise ValueError("package JSONL input is incomplete")
    return [json.loads(line) for line in data.splitlines()]


def build(capability_path: Path, replay_path: Path, separation_path: Path, tokenizer: object, template_path: Path) -> dict:
    capability, replay = _rows(capability_path), _rows(replay_path)
    package = capability + replay
    if (len(capability), len(replay)) != (720, 180) or len({row["id"] for row in package}) != 900:
        raise ValueError("package shape or IDs differ")
    separation = _sealed(separation_path)
    if separation.get("status") != "passed" or separation.get("package_rows_sha256") != canonical_sha256(package):
        raise ValueError("package separation not passed or row binding differs")
    by_id = {row["id"]: row for row in package}
    sep_rows = separation.get("records")
    if not isinstance(sep_rows, list) or len(sep_rows) != 900 or any(
        item.get("id") not in by_id or item.get("row_sha256") != canonical_sha256(by_id[item["id"]])
        or any(item.get(field) is not True for field in PASS_FIELDS)
        for item in sep_rows
    ):
        raise ValueError("separation does not attest every package row")
    encoded = []
    failures = []
    for row in package:
        try:
            value = build_response_only_encoding(tokenizer, row["messages"], max_length=2944)
            input_ids = value.encoding["input_ids"]
            labels = value.encoding["labels"]
            if not isinstance(input_ids, list) or not isinstance(labels, list) or len(input_ids) != len(labels):
                raise ValueError("tokenizer returned malformed rows")
            if labels[:value.prompt_token_count] != [-100] * value.prompt_token_count or labels[value.prompt_token_count:] != input_ids[value.prompt_token_count:]:
                raise ValueError("response-only label boundary differs")
            encoded.append({"id": row["id"], "source_id": row["id"], "lane": row["lane"], "input_ids": input_ids,
                            "labels": labels, "prompt_token_count": value.prompt_token_count})
        except (ResponseOnlyError, ValueError) as exc:
            failures.append({"id": row["id"], "failure_class": type(exc).__name__, "reason": str(exc)})
    token_records = []
    mass = Counter()
    if not failures:
        weighted, shares = attach_objective_weights(encoded, TARGETS, 8)
        if any(abs(shares[lane] - target) > 1e-6 for lane, target in TARGETS.items()):
            raise ValueError("family objective weight balance differs")
        for item in weighted:
            token_records.append({"id": item["id"], "row_sha256": canonical_sha256(by_id[item["id"]]),
                                  "input_tokens": len(item["input_ids"]), "supervised_tokens": item["response_token_count"],
                                  "objective_weight": item["objective_weight"]})
            mass[item["lane"]] += item["objective_weight"]
    report = {
        "schema_version": "ganesh-mini-gate3-package-tokenization/v1",
        "status": "passed" if not failures else "failed",
        "package_rows_sha256": canonical_sha256(package),
        "capability_file_sha256": _file_sha(capability_path),
        "replay_file_sha256": _file_sha(replay_path),
        "separation_report_sha256": separation["report_sha256"],
        "tokenizer_revision": MODEL_REVISION,
        "chat_template_sha256": _file_sha(template_path),
        "maximum_sequence_length": 2944,
        "response_only_labels_verified": not failures,
        "objective_method": "unique-row-token-weighted-five-family-v2",
        "family_targets": TARGETS,
        "realized_family_weight_mass": dict(mass),
        "evaluation_artifacts_read_by_construction": 0,
        "failures": failures,
        "records": token_records,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("capability", "replay", "separation", "output"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("output already exists")
    from transformers import AutoTokenizer
    model = ROOT / "models/qwen3.5-2b-15852e8"
    tokenizer = AutoTokenizer.from_pretrained(model, local_files_only=True)
    report = build(args.capability, args.replay, args.separation, tokenizer, model / "chat_template.jinja")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": report["status"], "records": len(report["records"]), "failures": len(report["failures"]), "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
