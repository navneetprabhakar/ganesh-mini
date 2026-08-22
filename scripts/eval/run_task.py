from __future__ import annotations

import argparse
from pathlib import Path

from scripts.eval.contracts import (
    load_json, sha256_object, sha256_text, validate_result, validate_task, write_json,
)
from scripts.verify.sandbox import verify


def build_result(
    task: dict,
    raw_output: str,
    extracted_code: str,
    extractor_id: str,
    model: dict,
    inference: dict,
    verifier: dict,
) -> dict:
    validate_task(task)
    result = {
        "schema_version": "1.0",
        "task_id": task["task_id"],
        "surface": task["surface"],
        "language": task["language"],
        "family": task["family"],
        "task_sha256": sha256_object(task),
        "prompt_sha256": task["prompt"]["sha256"],
        "rendered_prompt_sha256": task["rendered_prompt"]["sha256"],
        "model": model,
        "inference": dict(inference),
        "candidate": {
            "raw_output": raw_output,
            "raw_output_sha256": sha256_text(raw_output),
            "extracted_code": extracted_code,
            "extracted_code_sha256": sha256_text(extracted_code),
            "extractor_id": extractor_id,
        },
        "verifier": verifier,
        "passed": (
            not verifier["timed_out"]
            and len(verifier["exit_codes"]) == len(verifier["commands"])
            and bool(verifier["exit_codes"])
            and all(code == 0 for code in verifier["exit_codes"])
        ),
    }
    result["inference"]["parameters_sha256"] = sha256_object(result["inference"]["parameters"])
    result["result_sha256"] = sha256_object(result)
    validate_result(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify one model output and write immutable evaluation evidence.")
    parser.add_argument("--task", type=Path, required=True)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--extracted-code", type=Path, required=True)
    parser.add_argument("--extractor-id", required=True)
    parser.add_argument("--model", type=Path, required=True, help="JSON object matching result.model")
    parser.add_argument("--inference", type=Path, required=True, help="JSON object with parameters/start/completion")
    parser.add_argument("--runtimes", type=Path, default=Path("configs/eval/runtimes.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    task = validate_task(load_json(args.task))
    raw_output = args.raw_output.read_text(encoding="utf-8")
    code = args.extracted_code.read_text(encoding="utf-8")
    verifier = verify(task, code, args.runtimes)
    result = build_result(
        task, raw_output, code, args.extractor_id,
        load_json(args.model), load_json(args.inference), verifier,
    )
    write_json(args.output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
