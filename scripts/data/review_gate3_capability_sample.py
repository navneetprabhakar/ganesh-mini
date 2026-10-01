#!/usr/bin/env python3
"""Freeze and run two independent, blind capability-quality review batches."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256
from scripts.data.generate_expansion_qualification import invoke_codex, verify_codex_version
from scripts.data.run_capability_scale_delta_audits import _write_json_atomic, _write_jsonl_atomic
from scripts.data.run_capability_scale_final_matrix import _jsonl, _sealed


MATERIALIZED_SEAL = "8f27cb55c1b6fedea24b2a2e7d086a78203b327c94022fa18f08a213a0a1023b"
CHECKS = (
    "prompt_clarity", "api_consistency", "test_independence", "non_triviality",
    "idiomatic_code", "dependency_isolation", "realistic_known_bad_failure",
    "primary_capability_alignment", "cross_cutting_alignment",
)
REVIEWERS = {"generation": "independent-blind-codex-reviewer-generation", "repair": "independent-blind-codex-reviewer-repair"}


def schema() -> dict[str, Any]:
    item = {
        "type": "object", "additionalProperties": False,
        "required": ["id", "checks", "verdict", "reason"],
        "properties": {
            "id": {"type": "string"},
            "checks": {"type": "object", "additionalProperties": False,
                       "required": list(CHECKS),
                       "properties": {key: {"type": "boolean"} for key in CHECKS}},
            "verdict": {"type": "string", "enum": ["pass", "fail"]},
            "reason": {"type": "string"},
        },
    }
    return {"type": "object", "additionalProperties": False,
            "required": ["items"], "properties": {"items": {"type": "array", "items": item}}}


def selection(rows_path: Path, materialized_report_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    report = _sealed(json.loads(materialized_report_path.read_text(encoding="utf-8")), "report_sha256", "materialized scale")
    rows = _jsonl(rows_path)
    if (
        report.get("report_sha256") != MATERIALIZED_SEAL
        or report.get("materialized_rows_sha256") != canonical_sha256(rows)
        or len(rows) != 546 or report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("review input is not the sealed 546-row materialization")
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        cap = row.get("qualification_assignment", {}).get("primary_capability")
        if cap not in CAPABILITIES or row.get("task_type") not in REVIEWERS:
            raise ValueError(f"{row.get('id')}: missing quality-review stratum")
        buckets[(cap, row["task_type"])].append(row)
    selected: list[dict[str, Any]] = []
    for cap in sorted(CAPABILITIES):
        for kind in ("generation", "repair"):
            group = buckets[(cap, kind)]
            if not group:
                raise ValueError(f"{cap}/{kind}: empty review stratum")
            ranked = sorted(group, key=lambda row: (
                hashlib.sha256(f"{MATERIALIZED_SEAL}\0{cap}\0{kind}\0{row['id']}".encode()).hexdigest(),
                row["id"],
            ))
            selected.append(ranked[0])
    result: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-blind-quality-selection/v1",
        "status": "selected-not-reviewed", "population": 546, "selected": 20,
        "materialized_report_sha256": MATERIALIZED_SEAL,
        "selected_ids": [row["id"] for row in selected],
        "selected_candidate_sha256s": [canonical_sha256(row) for row in selected],
        "selection_rule": "minimum SHA-256 of materialized seal, capability, task type, and record ID; one generation and one repair per capability",
        "evaluation_artifacts_read": 0,
    }
    result["report_sha256"] = canonical_sha256(result)
    return selected, result


def projection(row: dict[str, Any]) -> dict[str, Any]:
    task = row["verification_task"]
    assignment = row["qualification_assignment"]
    return {
        "id": row["id"], "lane": row["lane"], "task_type": row["task_type"],
        "primary_capability": assignment["primary_capability"],
        "cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        "specification": row["messages"][0]["content"],
        "reference_code": task["validation"]["reference"]["code"],
        "known_bad_code": task["validation"]["known_bad"][0]["code"],
        "independent_tests": [item["content"] for item in task["files"] if item["role"] == "test"],
    }


def prompt(rows: list[dict[str, Any]]) -> str:
    visible = [projection(row) for row in rows]
    return (
        "Independently review these training-only coding examples. Do not use tools or inspect the filesystem. "
        "You are blind to source records, teacher drafts, admission outcomes, prior reviews, and all evaluation tasks. "
        "Assess each exact ID separately. Check prompt clarity, public API consistency, independence and strength of "
        "the two tests, nontriviality, idiomatic reference code, dependency isolation, plausibility of the known-bad "
        "defect, substantive primary-capability alignment, and concrete but orthogonal cross-cutting behavior. "
        "Mark verdict pass only when every check is true. Do not repair or reinterpret a record. Give a short reason "
        "for the verdict. Return only the schema-constrained object.\nItems: "
        + json.dumps(visible, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    )


def validate_payload(payload: dict[str, Any], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items = payload.get("items")
    ids = [row["id"] for row in rows]
    if not isinstance(items, list) or len(items) != len(ids) or [item.get("id") for item in items if isinstance(item, dict)] != ids:
        raise ValueError("review output does not cover exact selected IDs in order")
    for item in items:
        if not isinstance(item, dict) or set(item) != {"id", "checks", "verdict", "reason"}:
            raise ValueError("quality review output shape differs")
        checks = item["checks"]
        if not isinstance(checks, dict) or set(checks) != set(CHECKS) or any(type(value) is not bool for value in checks.values()):
            raise ValueError("quality review checks are incomplete")
        if item["verdict"] not in ("pass", "fail") or (item["verdict"] == "pass") != all(checks.values()):
            raise ValueError("quality review verdict contradicts check flags")
        if not isinstance(item["reason"], str) or not item["reason"].strip():
            raise ValueError("quality review reason is absent")
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--materialized-report", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    args = parser.parse_args()
    selected, manifest = selection(args.candidates, args.materialized_report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sample_path, manifest_path = args.output_dir / "selected.jsonl", args.output_dir / "selection-report.json"
    if sample_path.exists() or manifest_path.exists():
        if not sample_path.exists() or not manifest_path.exists() or _jsonl(sample_path) != selected or json.loads(manifest_path.read_text()) != manifest:
            raise ValueError("frozen quality sample differs")
    else:
        _write_jsonl_atomic(sample_path, selected)
        _write_json_atomic(manifest_path, manifest)
    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    schema_path = args.output_dir / "review-schema.json"
    schema_text = json.dumps(schema(), indent=2, sort_keys=True) + "\n"
    if schema_path.exists() and schema_path.read_text(encoding="utf-8") != schema_text:
        raise ValueError("quality review schema drift")
    if not schema_path.exists():
        schema_path.write_text(schema_text, encoding="utf-8")
    artifacts: list[dict[str, Any]] = []
    for kind in ("generation", "repair"):
        batch = [row for row in selected if row["task_type"] == kind]
        review_prompt = prompt(batch)
        path = args.output_dir / f"{kind}-review.json"
        if path.exists():
            artifact = _sealed(json.loads(path.read_text(encoding="utf-8")), "artifact_sha256", kind)
            if artifact.get("prompt_sha256") != hashlib.sha256(review_prompt.encode()).hexdigest():
                raise ValueError(f"{kind}: review prompt drift")
        else:
            payload, evidence = invoke_codex(args.codex_bin, config, schema_path, review_prompt, "gate3-blind-quality", kind)
            items = validate_payload(payload, batch)
            artifact = {
                "schema_version": "ganesh-mini-gate3-blind-quality-batch/v1",
                "reviewer_id": REVIEWERS[kind], "reviewer_kind": "independent-codex-cli",
                "task_type": kind, "selection_report_sha256": manifest["report_sha256"],
                "candidate_ids": [row["id"] for row in batch],
                "candidate_sha256s": [canonical_sha256(row) for row in batch],
                "prompt_sha256": hashlib.sha256(review_prompt.encode()).hexdigest(),
                "schema_sha256": hashlib.sha256(schema_text.encode()).hexdigest(),
                "cli_identity": cli_identity, "items": items,
                "run_evidence": evidence, "run_evidence_sha256": canonical_sha256(evidence),
                "evaluation_artifacts_read": 0,
            }
            artifact["artifact_sha256"] = canonical_sha256(artifact)
            _write_json_atomic(path, artifact)
        validate_payload({"items": artifact["items"]}, batch)
        artifacts.append(artifact)
    all_items = [item for artifact in artifacts for item in artifact["items"]]
    failed = [item["id"] for item in all_items if item["verdict"] != "pass"]
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-blind-quality-result/v1",
        "status": "passed" if not failed else "failed",
        "selection_report_sha256": manifest["report_sha256"],
        "reviewer_kinds": [artifact["reviewer_kind"] for artifact in artifacts],
        "reviewer_ids": [artifact["reviewer_id"] for artifact in artifacts],
        "batch_artifact_sha256s": [artifact["artifact_sha256"] for artifact in artifacts],
        "reviewed": 20, "failed_ids": failed,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    result_path = args.output_dir / "quality-review-report.json"
    if result_path.exists() and json.loads(result_path.read_text()) != report:
        raise ValueError("quality review result already exists with different evidence")
    if not result_path.exists():
        _write_json_atomic(result_path, report)
    print(json.dumps({"status": report["status"], "reviewed": 20, "failed": len(failed), "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())
