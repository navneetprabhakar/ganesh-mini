#!/usr/bin/env python3
"""Apply the single permitted correction to executable qualification rejects.

The critic boundary is deliberately asymmetric.  A failed reference run may
only expose the specification and independently authored tests to a test
critic.  A known-bad implementation accepted by the tests may only expose the
specification, reference, and known-bad contract to an architect critic.
Evaluation artifacts are never inputs to this program.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.data.generate_capability_qualification import seal_run  # noqa: E402
from scripts.data.generate_expansion_qualification import (  # noqa: E402
    ARCHITECT_SCHEMA,
    TEST_SCHEMA,
    CodexInvocationFailure,
    build_candidate,
    canonical_json,
    exact_items,
    invoke_codex,
    verify_codex_version,
)
from scripts.eval.contracts import sha256_text  # noqa: E402


ANSWER_SUFFIX = "\n\nReturn only the complete source file; do not include Markdown fences or prose."
EVIDENCE_SCHEMA = "ganesh-mini-capability-qualification-correction/v1"
REPORT_SCHEMA = "ganesh-mini-capability-qualification-correction-report/v1"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def candidate_sha256(candidate: dict[str, Any]) -> str:
    """Hash the training candidate, excluding generation/audit attachments."""
    return canonical_sha256({
        key: value for key, value in candidate.items()
        if key not in {"qualification_assignment", "teacher_evidence"}
    })


def _base_problem(candidate: dict[str, Any]) -> str:
    problem = candidate["messages"][0]["content"]
    if not problem.endswith(ANSWER_SUFFIX):
        raise ValueError(f"{candidate.get('id')}: generated prompt suffix is missing")
    return problem[:-len(ANSWER_SUFFIX)]


def _test_file(candidate: dict[str, Any]) -> dict[str, Any]:
    tests = [item for item in candidate["verification_task"]["files"] if item.get("role") == "test"]
    if len(tests) != 1:
        raise ValueError(f"{candidate.get('id')}: correction requires exactly one test file")
    return tests[0]


def _architecture(candidate: dict[str, Any]) -> dict[str, str]:
    validation = candidate["verification_task"]["validation"]
    known_bad = validation["known_bad"]
    if len(known_bad) != 1:
        raise ValueError(f"{candidate.get('id')}: correction requires exactly one known-bad implementation")
    return {
        "id": candidate["id"],
        "problem": _base_problem(candidate),
        "reference_code": validation["reference"]["code"],
        "known_bad_code": known_bad[0]["code"],
        "known_bad_label": known_bad[0]["label"],
    }


def classify_rejection(reason: str) -> str:
    if reason == "reference solution failed behavioral verification":
        return "reference-verification"
    if reason.startswith("tests accepted known-bad implementation:"):
        return "tests-accepted-known-bad"
    raise ValueError(f"rejection is not safely correctable: {reason}")


def _rejections(value: Any) -> list[dict[str, Any]]:
    rows = value.get("rejected") if isinstance(value, dict) else value
    if not isinstance(rows, list) or not rows:
        raise ValueError("executable admission rejection evidence must be a non-empty list")
    seen: set[str] = set()
    for row in rows:
        if (
            not isinstance(row, dict)
            or not isinstance(row.get("id"), str)
            or not row["id"]
            or row["id"] in seen
            or not isinstance(row.get("reason"), str)
        ):
            raise ValueError("rejection evidence has malformed or duplicate IDs")
        classify_rejection(row["reason"])
        seen.add(row["id"])
    return rows


def _validate_candidate(candidate: dict[str, Any]) -> None:
    assignment = candidate.get("qualification_assignment")
    teacher = candidate.get("teacher_evidence")
    if (
        not isinstance(candidate.get("id"), str)
        or not isinstance(candidate.get("lane"), str)
        or not isinstance(candidate.get("task_type"), str)
        or not isinstance(assignment, dict)
        or not isinstance(assignment.get("cell_id"), str)
        or not isinstance(assignment.get("source_queue_id"), str)
        or not isinstance(candidate.get("source"), dict)
        or not isinstance(teacher, dict)
    ):
        raise ValueError(f"{candidate.get('id')}: incomplete qualification candidate")
    if teacher.get("correction_passes") is not None or teacher.get("correction") is not None:
        raise ValueError(f"{candidate['id']}: a second correction pass is prohibited")
    _architecture(candidate)
    _test_file(candidate)


def reference_test_critic_prompt(lane: str, candidates: list[dict[str, Any]]) -> str:
    visible = [
        {"id": row["id"], "specification": _base_problem(row), "test_code": _test_file(row)["content"]}
        for row in candidates
    ]
    return f"""Correct independently authored {lane} behavioral tests using only their specifications and current tests.
Do not use tools or inspect the filesystem. You have not seen any reference implementation, known-bad
implementation, teacher context, verifier output, source stimulus, or evaluation artifact.
Items: {json.dumps(visible, separators=(",", ":"), ensure_ascii=False)}

For every exact id return one complete deterministic standard-library-only test file in test_code. Remove or
correct expectations that do not follow from the specification, while retaining strong normal, boundary,
malformed, ordering, stability, and non-mutation coverage only where the specification requires it. Do not change
or weaken the specification. Audit that every input is constructible and the file compiles. Return only the
schema-constrained object."""


def known_bad_architect_critic_prompt(lane: str, candidates: list[dict[str, Any]]) -> str:
    visible = [_architecture(row) for row in candidates]
    return f"""Correct these {lane} reference/known-bad contracts using only the specification, reference, known-bad
implementation, and known-bad label. Do not use tools or inspect the filesystem. You have not seen any tests,
test-author context, verifier output, source stimulus, or evaluation artifact.
Items: {json.dumps(visible, separators=(",", ":"), ensure_ascii=False)}

For every exact id return problem, reference_code, known_bad_code, and known_bad_label. Preserve problem exactly.
The reference must satisfy every stated requirement. The known-bad implementation must remain plausible, differ
from the reference by exactly one semantic bug, and the label must accurately identify it. Do not weaken or alter
the specification to accommodate either implementation. Return only the schema-constrained object."""


def _replace_tests(candidate: dict[str, Any], test_code: str) -> dict[str, Any]:
    replacement = copy.deepcopy(candidate)
    content = test_code.strip() + "\n"
    test = _test_file(replacement)
    test.update(content=content, sha256=sha256_text(content))
    return replacement


def _replace_architecture(candidate: dict[str, Any], item: dict[str, str]) -> dict[str, Any]:
    if item["problem"] != _base_problem(candidate):
        raise ValueError(f"{candidate['id']}: architect critic changed the frozen specification")
    replacement = build_candidate(
        candidate["lane"], candidate["id"], candidate["task_type"], item,
        _test_file(candidate)["content"], source=copy.deepcopy(candidate["source"]),
    )
    replacement["test_origin"] = candidate["test_origin"]
    replacement["qualification_assignment"] = copy.deepcopy(candidate["qualification_assignment"])
    replacement["teacher_evidence"] = copy.deepcopy(candidate["teacher_evidence"])
    return replacement


def _mark_correction(
    replacement: dict[str, Any], parent: dict[str, Any], correction_class: str,
    run: dict[str, Any], rejection: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    parent_sha = candidate_sha256(parent)
    corrected_sha = candidate_sha256(replacement)
    if corrected_sha == parent_sha:
        raise ValueError(f"{parent['id']}: critic produced no candidate change")
    evidence: dict[str, Any] = {
        "schema_version": EVIDENCE_SCHEMA,
        "id": parent["id"],
        "lane": parent["lane"],
        "task_type": parent["task_type"],
        "cell_id": parent["qualification_assignment"]["cell_id"],
        "source_queue_id": parent["qualification_assignment"]["source_queue_id"],
        "source_identity": {
            key: parent["source"].get(key) for key in ("dataset", "revision", "record_id")
        },
        "correction_passes": 1,
        "correction_class": correction_class,
        "parent_candidate_sha256": parent_sha,
        "corrected_candidate_sha256": corrected_sha,
        "rejection_evidence_sha256": canonical_sha256(rejection),
        "critic_run_evidence_sha256": run["run_evidence_sha256"],
        "visibility": {
            "specification_visible": True,
            "tests_visible": correction_class == "reference-verification",
            "reference_visible": correction_class == "tests-accepted-known-bad",
            "known_bad_visible": correction_class == "tests-accepted-known-bad",
            "verifier_output_visible": False,
            "evaluation_artifacts_read": 0,
        },
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    teacher = copy.deepcopy(replacement["teacher_evidence"])
    teacher["correction_passes"] = 1
    teacher["correction"] = {
        "parent_candidate_sha256": parent_sha,
        "corrected_candidate_sha256": corrected_sha,
        "correction_class": correction_class,
        "correction_evidence_sha256": evidence["evidence_sha256"],
        "critic_run_evidence_sha256": run["run_evidence_sha256"],
    }
    replacement["teacher_evidence"] = teacher
    return replacement, evidence


def correct_candidates(
    candidates: list[dict[str, Any]], rejection_value: Any,
    config: dict[str, Any], codex_bin: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_id: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        _validate_candidate(candidate)
        if candidate["id"] in by_id:
            raise ValueError("candidate input contains duplicate IDs")
        by_id[candidate["id"]] = candidate
    rejections = _rejections(rejection_value)
    if any(row["id"] not in by_id for row in rejections):
        raise ValueError("rejection evidence references an unknown candidate")

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    rejection_by_id = {row["id"]: row for row in rejections}
    for rejection in rejections:
        candidate = by_id[rejection["id"]]
        grouped[(candidate["lane"], classify_rejection(rejection["reason"]))].append(candidate)

    replacements: dict[str, dict[str, Any]] = {}
    correction_evidence: list[dict[str, Any]] = []
    runs: list[dict[str, Any]] = []
    for (lane, correction_class), rows in sorted(grouped.items()):
        expected_ids = [row["id"] for row in rows]
        if correction_class == "reference-verification":
            payload, run = invoke_codex(
                codex_bin, config, TEST_SCHEMA, reference_test_critic_prompt(lane, rows),
                "capability-reference-test-critic", lane,
            )
            run = seal_run(run)
            items = exact_items(payload, expected_ids, {"id", "test_code"})
            proposed = [_replace_tests(row, item["test_code"]) for row, item in zip(rows, items, strict=True)]
        elif correction_class == "tests-accepted-known-bad":
            payload, run = invoke_codex(
                codex_bin, config, ARCHITECT_SCHEMA, known_bad_architect_critic_prompt(lane, rows),
                "capability-known-bad-architect-critic", lane,
            )
            run = seal_run(run)
            items = exact_items(
                payload, expected_ids,
                {"id", "problem", "reference_code", "known_bad_code", "known_bad_label"},
            )
            proposed = [_replace_architecture(row, item) for row, item in zip(rows, items, strict=True)]
        else:  # pragma: no cover - classification is fail-closed before grouping
            raise ValueError(f"unsupported correction class: {correction_class}")
        runs.append(run)
        for parent, replacement in zip(rows, proposed, strict=True):
            if (
                replacement["id"] != parent["id"]
                or replacement["lane"] != parent["lane"]
                or replacement["task_type"] != parent["task_type"]
                or replacement["source"] != parent["source"]
                or replacement["qualification_assignment"] != parent["qualification_assignment"]
            ):
                raise ValueError(f"{parent['id']}: correction changed frozen identity, cell, or source lineage")
            marked, evidence = _mark_correction(
                replacement, parent, correction_class, run, rejection_by_id[parent["id"]],
            )
            replacements[parent["id"]] = marked
            correction_evidence.append(evidence)

    output = [replacements.get(row["id"], copy.deepcopy(row)) for row in candidates]
    return output, correction_evidence, runs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--rejections", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--codex-bin", default="codex")
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    candidates = read_jsonl(args.input)
    rejection_value = json.loads(args.rejections.read_text(encoding="utf-8"))
    try:
        corrected, records, runs = correct_candidates(candidates, rejection_value, config, args.codex_bin)
        payload = b"".join(canonical_json(row) + b"\n" for row in corrected)
        status = "corrected-not-reviewed-not-admitted"
        failure = None
    except CodexInvocationFailure as exc:
        corrected, records, runs, payload = [], [], [seal_run(exc.evidence)], b""
        status = "correction-failed-not-admitted"
        failure = {"type": type(exc).__name__, "reason": str(exc)}
    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA,
        "status": status,
        "cli_identity": cli_identity,
        "teacher": config,
        "input": {"sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(), "records": len(candidates)},
        "rejections_sha256": hashlib.sha256(args.rejections.read_bytes()).hexdigest(),
        "requested_corrections": len(_rejections(rejection_value)),
        "completed_corrections": len(records),
        "corrections": records,
        "runs": runs,
        "output_sha256": hashlib.sha256(payload).hexdigest() if payload else None,
        "output": (
            {
                "path": str(args.output), "bytes": len(payload),
                "records": len(corrected), "sha256": hashlib.sha256(payload).hexdigest(),
            }
            if payload else None
        ),
        "evaluation_artifacts_read": 0,
        "failure": failure,
    }
    report["report_sha256"] = canonical_sha256(report)
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    if failure is not None:
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    print(json.dumps({"status": status, "corrected": len(records), "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
