#!/usr/bin/env python3
"""Seal untruncated token length before qualifying the single reserve draft."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.train.response_only import ResponseOnlyError, build_response_only_encoding


ROOT = Path(__file__).resolve().parents[2]
REQUEST_ID = "cap-scale-binary_and_bitwise-typescript-repair-reserve-06"
MAX_TOKENS = 2944


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sealed(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    if body.pop("report_sha256", None) != canonical_sha256(body):
        raise ValueError("report seal differs")
    return value


def build(candidates_path: Path, teacher_report_path: Path, activation_report_path: Path) -> dict:
    activation = sealed(activation_report_path)
    teacher = sealed(teacher_report_path)
    candidates = [json.loads(line) for line in candidates_path.read_text(encoding="utf-8").splitlines()]
    if (activation.get("status") != "activated" or activation.get("activated") != 1 or
        teacher.get("status") != "passed" or teacher.get("mode") != "activated-reserves" or
        teacher.get("requested") != 1 or teacher.get("counts") != {"generated": 1} or
        teacher.get("candidates_sha256") != canonical_sha256(candidates) or len(candidates) != 1):
        raise ValueError("one-draft teacher evidence differs from activation")
    candidate = candidates[0]
    if candidate.get("id") != REQUEST_ID or candidate.get("qualification_assignment", {}).get("cell_id") != "binary_and_bitwise/typescript/repair":
        raise ValueError("teacher candidate differs from approved reserve")
    from transformers import AutoTokenizer
    model = ROOT / "models/qwen3.5-2b-15852e8"
    tokenizer = AutoTokenizer.from_pretrained(model, local_files_only=True)
    try:
        encoding = build_response_only_encoding(tokenizer, candidate["messages"], max_length=MAX_TOKENS)
        count = len(encoding.encoding["input_ids"])
        response_tokens = encoding.response_token_count
        status = "passed"
        failure = None
    except ResponseOnlyError as exc:
        status = "failed"
        failure = str(exc)
        # Measure the full turn without truncation to preserve the exact overage.
        count = len(tokenizer.apply_chat_template(candidate["messages"], tokenize=True, return_dict=True,
                                                  add_generation_prompt=False, enable_thinking=False)["input_ids"])
        response_tokens = None
    report = {
        "schema_version": "ganesh-mini-gate3-token-length-precheck/v1",
        "status": status,
        "candidate_id": REQUEST_ID,
        "candidate_sha256": canonical_sha256(candidate),
        "candidates_file_sha256": file_sha(candidates_path),
        "teacher_report_sha256": teacher["report_sha256"],
        "activation_report_sha256": activation["report_sha256"],
        "tokenizer_revision": "15852e8c16360a2fea060d615a32b45270f8a8fc",
        "chat_template_sha256": file_sha(model / "chat_template.jinja"),
        "maximum_sequence_length": MAX_TOKENS,
        "completed_turn_tokens": count,
        "response_tokens": response_tokens,
        "failure": failure,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("candidates", "teacher_report", "activation_report", "output"):
        parser.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("output already exists")
    report = build(args.candidates, args.teacher_report, args.activation_report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({key: report[key] for key in ("status", "completed_turn_tokens", "report_sha256")}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
