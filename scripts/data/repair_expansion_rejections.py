#!/usr/bin/env python3
"""Repair rejected Codex expansion candidates without changing accepted rows."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from scripts.data.generate_expansion_qualification import (
    ARCHITECT_SCHEMA,
    TEST_SCHEMA,
    CodexInvocationFailure,
    build_candidate,
    canonical_json,
    critic_test_prompt,
    exact_items,
    invoke_codex,
    verify_codex_version,
)


ANSWER_SUFFIX = "\n\nReturn only the complete source file; do not include Markdown fences or prose."


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").split("\n") if line.strip()]


def base_problem(candidate: dict[str, Any]) -> str:
    problem = candidate["messages"][0]["content"]
    if not problem.endswith(ANSWER_SUFFIX):
        raise ValueError(f"{candidate['id']}: generated prompt suffix is missing")
    return problem[: -len(ANSWER_SUFFIX)]


def architecture(candidate: dict[str, Any]) -> dict[str, str]:
    validation = candidate["verification_task"]["validation"]
    known_bad = validation["known_bad"]
    if len(known_bad) != 1:
        raise ValueError(f"{candidate['id']}: repair supports exactly one known-bad implementation")
    return {
        "id": candidate["id"],
        "problem": base_problem(candidate),
        "reference_code": validation["reference"]["code"],
        "known_bad_code": known_bad[0]["code"],
        "known_bad_label": known_bad[0]["label"],
    }


def test_code(candidate: dict[str, Any]) -> str:
    tests = [item for item in candidate["verification_task"]["files"] if item["role"] == "test"]
    if len(tests) != 1:
        raise ValueError(f"{candidate['id']}: repair supports exactly one test file")
    return tests[0]["content"]


def classify_rejection(reason: str) -> str:
    if reason == "reference solution failed behavioral verification":
        return "reference"
    if reason.startswith("tests accepted known-bad implementation:"):
        return "tests"
    raise ValueError(f"rejection is not teacher-repairable: {reason}")


def corrected_source(candidate: dict[str, Any], annotation: str) -> dict[str, str]:
    source = copy.deepcopy(candidate["source"])
    source["transformation"] += f"; {annotation}"
    return source


def reference_repair_prompt(
    lane: str,
    candidates: list[dict[str, Any]],
    rejections: dict[str, dict[str, Any]],
) -> str:
    visible = []
    for candidate in candidates:
        item = architecture(candidate)
        item["test_code"] = test_code(candidate)
        item["verifier_result"] = json.dumps(
            rejections[candidate["id"]].get("evidence", {}).get("reference", {}),
            sort_keys=True,
            separators=(",", ":"),
        )
        visible.append(item)
    return f"""Correct these {lane} reference implementations against their specification and previously independent tests.
Do not use tools or inspect the filesystem. The tests were authored without seeing reference or known-bad code.
Items: {json.dumps(visible, separators=(",", ":"), ensure_ascii=False)}

Return every exact id with problem, reference_code, known_bad_code, and known_bad_label. Preserve problem text
exactly. Correct the reference so it satisfies the problem and tests. Preserve exactly one plausible semantic bug
in known_bad_code and keep the label accurate. Do not weaken the specification or tests. Return only the
schema-constrained object."""


def repair_candidates(
    candidates: list[dict[str, Any]],
    report: dict[str, Any],
    config: dict[str, Any],
    codex_bin: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]]:
    by_id = {candidate["id"]: candidate for candidate in candidates}
    rejections = {item["id"]: item for item in report["rejected"]}
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record_id, rejection in rejections.items():
        if record_id not in by_id:
            raise ValueError(f"admission rejection references unknown candidate: {record_id}")
        candidate = by_id[record_id]
        grouped[(candidate["lane"], classify_rejection(rejection["reason"]))].append(candidate)

    replacements: dict[str, dict[str, Any]] = {}
    runs: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    architect_fields = {"id", "problem", "reference_code", "known_bad_code", "known_bad_label"}
    for (lane, repair_type), rows in sorted(grouped.items()):
        expected_ids = [row["id"] for row in rows]
        try:
            if repair_type == "reference":
                payload, evidence = invoke_codex(
                    codex_bin, config, ARCHITECT_SCHEMA,
                    reference_repair_prompt(lane, rows, rejections), "reference-repair", lane,
                )
                runs.append(evidence)
                repaired = exact_items(payload, expected_ids, architect_fields)
                repaired_by_id = {item["id"]: item for item in repaired}
                for row in rows:
                    item = repaired_by_id[row["id"]]
                    if item["problem"] != base_problem(row):
                        raise ValueError(f"{row['id']}: reference repair changed frozen problem text")
                    replacement = build_candidate(
                        lane, row["id"], row["task_type"], item, test_code(row),
                        source=corrected_source(row, "reference corrected against independent tests"),
                    )
                    replacements[row["id"]] = replacement
            else:
                architecture_items = [architecture(row) for row in rows]
                test_items = [{"id": row["id"], "test_code": test_code(row)} for row in rows]
                payload, evidence = invoke_codex(
                    codex_bin, config, TEST_SCHEMA,
                    critic_test_prompt(lane, architecture_items, test_items), "rejection-test-critic", lane,
                )
                runs.append(evidence)
                repaired = exact_items(payload, expected_ids, {"id", "test_code"})
                repaired_by_id = {item["id"]: item["test_code"] for item in repaired}
                for row in rows:
                    item = architecture(row)
                    replacement = build_candidate(
                        lane, row["id"], row["task_type"], item, repaired_by_id[row["id"]],
                        source=corrected_source(row, "independent tests strengthened after rejection"),
                    )
                    replacements[row["id"]] = replacement
        except (KeyError, OSError, RuntimeError, TypeError, ValueError) as exc:
            if isinstance(exc, CodexInvocationFailure):
                runs.append(exc.evidence)
            failures.append({"lane": lane, "repair_type": repair_type, "reason": str(exc)})

    output = [replacements.get(candidate["id"], candidate) for candidate in candidates]
    return output, runs, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--admission-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--codex-bin", default="codex")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    candidates = read_jsonl(args.input)
    report = json.loads(args.admission_report.read_text(encoding="utf-8"))
    if report["input_sha256"] != hashlib.sha256(args.input.read_bytes()).hexdigest():
        raise ValueError("admission report does not bind the supplied candidate input")
    repaired, runs, failures = repair_candidates(candidates, report, config, args.codex_bin)
    payload = b"".join(canonical_json(row) + b"\n" for row in repaired)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    evidence = {
        "schema_version": "ganesh-mini-expansion-rejection-repair/v1",
        "teacher": config,
        "cli_identity": cli_identity,
        "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "admission_report_sha256": report["report_sha256"],
        "requested_repairs": len(report["rejected"]),
        "output_sha256": hashlib.sha256(payload).hexdigest(),
        "failures": failures,
        "runs": runs,
    }
    evidence["evidence_sha256"] = hashlib.sha256(canonical_json(evidence)).hexdigest()
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"requested": len(report["rejected"]), "runs": len(runs), "failures": len(failures)}, sort_keys=True))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
