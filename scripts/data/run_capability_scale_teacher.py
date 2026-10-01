#!/usr/bin/env python3
"""Run resumable, per-request Gate 3 capability-scale teacher construction."""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_scale_queue import source_key
from scripts.data.prepare_capability_scale_prospective_replacement import PLAN_SHA256 as PROSPECTIVE_PLAN_SHA256
from scripts.data.generate_capability_qualification import architect_prompt, qualification_metadata
from scripts.data.generate_expansion_qualification import (
    ARCHITECT_SCHEMA, CodexInvocationFailure, build_candidate, exact_items,
    invoke_codex, verify_codex_version,
)


QUEUE_SEAL = "f3e3e312625ec85f067c0089f40b16ed4591fe320745445e34f23825a3dc6d55"
QUEUE_SHA256 = "a8d9eb96cdbdb8ccd4ec126b512c71ae832856beff9dd46a799c99571eefba51"
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
PROMPT_CONTRACT_V1 = "capability-scale-teacher-prompt/v1"
PROMPT_CONTRACT_V2 = "capability-scale-primary-delta-teacher-prompt/v2"


def scale_architect_prompt(row: dict[str, Any], prompt_contract: str) -> str:
    if prompt_contract == PROMPT_CONTRACT_V1:
        return architect_prompt(row["lane"], [row])
    if prompt_contract != PROMPT_CONTRACT_V2:
        raise ValueError(f"unknown teacher prompt contract: {prompt_contract}")
    base = architect_prompt(row["lane"], [row])
    binding = f"""

This request is bound to primary capability `{row['primary_capability']}`:
{row['primary_capability_definition']}
The scheduled cross-cutting dimension is `{row['assigned_cross_cutting_dimension']}`.

The reference and known-bad implementations must differ by exactly one independent semantic defect, and that
defect must specifically exercise the assigned primary capability. The known-bad implementation must already
satisfy the scheduled cross-cutting dimension; do not make the cross-cutting dimension the defect. For a repair
item, the complete buggy source embedded in the problem must have that same primary-capability defect. Before
returning, compare reference and known-bad line by line and reject your own draft unless this exact delta rule holds.
"""
    return base + binding + "\nReturn only the schema-constrained object."


def _sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_queue(queue_path: Path, manifest_path: Path) -> list[dict[str, Any]]:
    manifest = _sealed(manifest_path, "manifest_sha256")
    rows = _jsonl(queue_path)
    required = {
        "schema_version", "id", "cell_id", "cohort", "primary_capability",
        "primary_capability_definition", "assigned_cross_cutting_dimension",
        "lane", "task_type", "source_queue_id", "source", "stimulus",
        "evaluation_artifacts_read", "request_sha256",
    }
    original = (
        manifest.get("manifest_sha256") == QUEUE_SEAL
        and manifest.get("queue_sha256") == QUEUE_SHA256
        and manifest.get("status") == "ready-for-first-pass-construction"
        and len(rows) == 711
    )
    prospective = (
        manifest.get("schema_version") == "ganesh-mini-gate3-prospective-replacement-manifest/v1"
        and manifest.get("status") == "source-prebound-not-generated"
        and manifest.get("original_queue_manifest_sha256") == QUEUE_SEAL
        and manifest.get("original_queue_sha256") == QUEUE_SHA256
        and manifest.get("plan_sha256") == PROSPECTIVE_PLAN_SHA256
        and manifest.get("evaluation_artifacts_read") == 0
        and manifest.get("teacher_drafts_before") == 1058
        and manifest.get("maximum_teacher_drafts_after") == 1059
        and manifest.get("global_teacher_draft_cap") == 1200
        and len(rows) == 1
        and rows[0].get("id") == "cap-scale-associative_aggregation-python-repair-prospective-01"
        and rows[0].get("cell_id") == "associative_aggregation/python/repair"
        and rows[0].get("cohort") == "prospective_replacement"
        and rows[0].get("request_sha256") == manifest.get("request_sha256")
        and rows[0].get("source_queue_id") == manifest.get("selected_source_queue_id")
        and source_key(rows[0]).replace("\0", "|") == manifest.get("selected_source_identity")
        and rows[0].get("source", {}).get("source_record_sha256") == manifest.get("selected_source_record_sha256")
    )
    if (
        not (original or prospective)
        or any(set(row) != required for row in rows)
        or any(row.get("request_sha256") != canonical_sha256({k: v for k, v in row.items() if k != "request_sha256"}) for row in rows)
        or len({row["id"] for row in rows}) != len(rows)
        or any(row.get("evaluation_artifacts_read") != 0 for row in rows)
    ):
        raise ValueError("capability-scale queue differs from its sealed contract")
    return rows


def select_rows(rows: list[dict[str, Any]], mode: str) -> list[dict[str, Any]]:
    first = [row for row in rows if row["cohort"] == "first_pass"]
    if mode == "first-pass":
        return first
    if mode != "canary":
        raise ValueError("mode must be canary or first-pass")
    selected: list[dict[str, Any]] = []
    for lane in LANES:
        for task_type in ("generation", "repair"):
            matches = [row for row in first if row["lane"] == lane and row["task_type"] == task_type]
            if not matches:
                raise ValueError(f"missing canary for {lane}/{task_type}")
            selected.append(matches[0])
    return selected


def select_activated_reserves(
    rows: list[dict[str, Any]], activation_path: Path, activation_report_path: Path,
) -> list[dict[str, Any]]:
    report = _sealed(activation_report_path, "report_sha256")
    activations = _jsonl(activation_path)
    if (
        report.get("status") != "activated"
        or report.get("queue_manifest_sha256") != QUEUE_SEAL
        or report.get("activated") != len(activations)
        or report.get("activation_rows_sha256") != canonical_sha256(activations)
    ):
        raise ValueError("reserve activation report does not bind activation rows")
    by_request = {row["request_sha256"]: row for row in rows}
    selected: list[dict[str, Any]] = []
    for activation in activations:
        body = dict(activation); claimed = body.pop("activation_sha256", None)
        row = by_request.get(activation.get("reserve_request_sha256"))
        if (
            claimed != canonical_sha256(body) or row is None or row["cohort"] != "reserve"
            or row["id"] != activation.get("reserve_candidate_id")
            or row["cell_id"] != activation.get("cell_id")
            or activation.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError("activated reserve differs from sealed queue binding")
        selected.append(row)
    if len({row["id"] for row in selected}) != len(selected):
        raise ValueError("reserve activation contains duplicate requests")
    return selected


def select_remaining_first_pass(
    rows: list[dict[str, Any]], consumed_teacher_report_path: Path,
) -> list[dict[str, Any]]:
    report = _sealed(consumed_teacher_report_path, "report_sha256")
    consumed = report.get("selected_request_sha256s")
    if (
        report.get("status") != "passed" or report.get("mode") != "canary"
        or not isinstance(consumed, list) or len(consumed) != 12 or len(set(consumed)) != 12
    ):
        raise ValueError("consumed canary teacher report is not the exact passing 12-request seal")
    first = [row for row in rows if row["cohort"] == "first_pass"]
    first_shas = {row["request_sha256"] for row in first}
    if not set(consumed) <= first_shas:
        raise ValueError("consumed canary requests differ from the first-pass queue")
    remaining = [row for row in first if row["request_sha256"] not in set(consumed)]
    if len(remaining) != 534:
        raise ValueError("remaining first-pass selection is not exactly 534")
    return remaining


def _candidate(row: dict[str, Any], architecture: dict[str, str], run_sha256: str) -> dict[str, Any]:
    candidate = build_candidate(
        row["lane"], row["id"], row["task_type"], architecture, "pending",
        source=row["source"],
    )
    candidate["verification_task"]["files"] = [
        item for item in candidate["verification_task"]["files"] if item.get("role") == "support"
    ]
    candidate["test_origin"] = "pending-v9-canonical-independent-author"
    candidate["qualification_assignment"] = qualification_metadata(row)
    candidate["teacher_evidence"] = {
        "architect_run_evidence_sha256": run_sha256,
        "request_sha256": row["request_sha256"],
        "evaluation_artifacts_read": 0,
    }
    return candidate


def _write_atomic(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _write_atomic_text(path: Path, value: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def run_one(
    row: dict[str, Any], config: dict[str, Any], codex_bin: str,
    cli_identity: str, run_dir: Path, prompt_contract: str = PROMPT_CONTRACT_V2,
) -> dict[str, Any]:
    prompt = scale_architect_prompt(row, prompt_contract)
    input_sha = canonical_sha256({
        "request": row, "prompt": prompt,
        "schema_path": str(ARCHITECT_SCHEMA),
        "schema_sha256": hashlib.sha256(ARCHITECT_SCHEMA.read_bytes()).hexdigest(),
        "config": config, "cli_identity": cli_identity,
        "prompt_contract": prompt_contract,
    })
    path = run_dir / f"{row['id']}.teacher.json"
    if path.exists():
        artifact = json.loads(path.read_text(encoding="utf-8"))
        body = dict(artifact); claimed = body.pop("artifact_sha256", None)
        if claimed != canonical_sha256(body) or artifact.get("input_sha256") != input_sha:
            raise ValueError(f"{row['id']}: sealed teacher artifact drift")
        return artifact
    evidence: dict[str, Any] = {}
    try:
        payload, evidence = invoke_codex(
            codex_bin, config, ARCHITECT_SCHEMA, prompt,
            "capability-scale-source-architect", row["lane"],
        )
        items = exact_items(
            payload, [row["id"]],
            {"id", "problem", "reference_code", "known_bad_code", "known_bad_label"},
        )
        run_evidence = copy.deepcopy(evidence)
        run_sha = canonical_sha256(run_evidence)
        candidate = _candidate(row, items[0], run_sha)
        artifact = {
            "schema_version": "ganesh-mini-capability-scale-teacher-artifact/v1",
            "prompt_contract": prompt_contract,
            "status": "generated",
            "candidate_id": row["id"], "cell_id": row["cell_id"],
            "input_sha256": input_sha, "request_sha256": row["request_sha256"],
            "candidate": candidate, "candidate_sha256": canonical_sha256(candidate),
            "run": run_evidence, "run_evidence_sha256": run_sha,
            "evaluation_artifacts_read": 0,
        }
    except CodexInvocationFailure as exc:
        artifact = {
            "schema_version": "ganesh-mini-capability-scale-teacher-artifact/v1",
            "prompt_contract": prompt_contract,
            "status": "invocation-failed",
            "candidate_id": row["id"], "cell_id": row["cell_id"],
            "input_sha256": input_sha, "request_sha256": row["request_sha256"],
            "failure": copy.deepcopy(exc.evidence), "reason": str(exc),
            "evaluation_artifacts_read": 0,
        }
    except (KeyError, TypeError, ValueError) as exc:
        artifact = {
            "schema_version": "ganesh-mini-capability-scale-teacher-artifact/v1",
            "prompt_contract": prompt_contract,
            "status": "response-rejected",
            "candidate_id": row["id"], "cell_id": row["cell_id"],
            "input_sha256": input_sha, "request_sha256": row["request_sha256"],
            "run": copy.deepcopy(evidence),
            "run_evidence_sha256": canonical_sha256(evidence),
            "reason": f"{type(exc).__name__}: {exc}",
            "evaluation_artifacts_read": 0,
        }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    _write_atomic(path, artifact)
    return artifact


def run(args: argparse.Namespace) -> dict[str, Any]:
    queue = load_queue(args.queue, args.queue_manifest)
    if args.mode == "prospective-replacement":
        if len(queue) != 1 or queue[0]["cohort"] != "prospective_replacement":
            raise ValueError("prospective mode requires the one-row sealed extension")
        rows = queue
    elif args.mode == "activated-reserves":
        if args.activation is None or args.activation_report is None:
            raise ValueError("activated-reserves mode requires activation rows and report")
        rows = select_activated_reserves(queue, args.activation, args.activation_report)
    elif args.mode == "remaining-first-pass":
        if args.consumed_teacher_report is None:
            raise ValueError("remaining-first-pass mode requires the consumed canary teacher report")
        rows = select_remaining_first_pass(queue, args.consumed_teacher_report)
    else:
        rows = select_rows(queue, args.mode)
    config = json.loads(args.teacher_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    args.run_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any] | None] = [None] * len(rows)

    def invoke(index: int) -> tuple[int, dict[str, Any]]:
        return index, run_one(
            rows[index], config, args.codex_bin, cli_identity, args.run_dir, args.prompt_contract,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        for index, artifact in executor.map(invoke, range(len(rows))):
            results[index] = artifact
    terminal = [value for value in results if value is not None]
    generated = [value["candidate"] for value in terminal if value["status"] == "generated"]
    counts = dict(sorted(__import__("collections").Counter(value["status"] for value in terminal).items()))
    report = {
        "schema_version": "ganesh-mini-capability-scale-teacher-report/v1",
        "status": "passed" if counts == {"generated": len(rows)} else "failed",
        "mode": args.mode, "requested": len(rows), "counts": counts,
        "prompt_contract": args.prompt_contract,
        "queue_manifest_sha256": _sealed(args.queue_manifest, "manifest_sha256")["manifest_sha256"],
        "selected_request_sha256s": [row["request_sha256"] for row in rows],
        "terminal_artifact_sha256s": [value["artifact_sha256"] for value in terminal],
        "candidates_sha256": canonical_sha256(generated),
        "cli_identity": cli_identity, "config_sha256": canonical_sha256(config),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_atomic_text(
        args.output_dir / "candidates.jsonl",
        "".join(json.dumps(value, sort_keys=True) + "\n" for value in generated),
    )
    _write_atomic(args.output_dir / "teacher-report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--teacher-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument(
        "--mode", choices=("canary", "first-pass", "remaining-first-pass", "activated-reserves", "prospective-replacement"),
        required=True,
    )
    parser.add_argument("--activation", type=Path)
    parser.add_argument("--activation-report", type=Path)
    parser.add_argument("--consumed-teacher-report", type=Path)
    parser.add_argument(
        "--prompt-contract", choices=(PROMPT_CONTRACT_V1, PROMPT_CONTRACT_V2),
        default=PROMPT_CONTRACT_V2,
    )
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = run(args)
    print(json.dumps({"status": report["status"], "counts": report["counts"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
