#!/usr/bin/env python3
"""Summarize an explicitly selected repair-delta contract without weakening v2."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v5_contract import (
    BUDGET_ADDENDUM_SHA256 as V5_BUDGET_ADDENDUM_SHA256,
    CONTRACT_ID as V5_CONTRACT_ID,
    EFFECTIVE_MAX_RESERVES as V5_MAX_RESERVES,
    NEW_TEACHER_BUDGET as V5_NEW_TEACHER_BUDGET,
    PLAN_SHA256 as V5_PLAN_SHA256,
    SOURCE_ADDENDUM_SHA256 as V5_SOURCE_ADDENDUM_SHA256,
    TERMINAL_BUDGET as V5_TERMINAL_BUDGET,
    UNRESERVED_CELL as V5_UNRESERVED_CELL,
    load_v5_contract,
)


SCHEMA_VERSION = "ganesh-mini-capability-repair-delta-summary/v1"
QUEUE_SCHEMA = "ganesh-mini-repair-delta-queue-manifest/v1"
PLAN_SHA256 = "4023a896300112f9f93f2a16698d549f203e3e75b4e71ae054f3a98463e2f0f0"
V2_SUMMARY_SHA256 = "293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139"
V2_ADMISSION_SHA256 = "c576ef4f5b0f137edac829703eae6d7c4a63cae513544d36471f7ffcf81b7cb7"
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
FIRST_PASS = "first_pass"
RESERVE = "reserve"
QUEUE_SEED = 3503
CONTRACT_ID = "capability-stratified-v3-repair-delta/v1"
V4_PLAN_SHA256 = "79849d2f8b70ba69572b4c3fa1761bdb413562c6f6d9a12537d93a1724812ef6"
V4_CONTRACT_ID = "capability-stratified-v4-repair-delta/v1"
V4_QUEUE_SEED = "ganesh-mini-gate2-v4-repair-delta-queue-v1"


def contract_spec(version: str = "v3") -> dict[str, Any]:
    if version == "v3":
        return {
            "version": "v3", "plan_sha256": PLAN_SHA256, "contract_id": CONTRACT_ID,
            "queue_seed": QUEUE_SEED, "queue_schema": QUEUE_SCHEMA,
            "envelope_schema": "ganesh-mini-repair-delta-envelope/v1",
            "assembly_schema": "ganesh-mini-repair-delta-evidence-assembly/v1",
            "admission_schema": "ganesh-mini-repair-delta-admission-report/v1",
        }
    if version == "v4":
        return {
            "version": "v4", "plan_sha256": V4_PLAN_SHA256, "contract_id": V4_CONTRACT_ID,
            "queue_seed": V4_QUEUE_SEED,
            "queue_schema": "ganesh-mini-repair-delta-v4-queue-manifest/v1",
            "envelope_schema": "ganesh-mini-repair-delta-v4-envelope/v1",
            "assembly_schema": "ganesh-mini-repair-delta-v4-evidence-assembly/v1",
            "admission_schema": "ganesh-mini-repair-delta-v4-admission-report/v1",
        }
    if version == "v5":
        return {
            "version": "v5", "plan_sha256": V5_PLAN_SHA256,
            "contract_id": V5_CONTRACT_ID,
            "envelope_schema": "ganesh-mini-repair-delta-v5-envelope/v1",
            "assembly_schema": "ganesh-mini-repair-delta-v5-evidence-assembly/v1",
            "admission_schema": "ganesh-mini-repair-delta-v5-admission-report/v1",
        }
    raise ValueError(f"unsupported repair-delta contract version {version!r}")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_sealed(path: Path, field: str = "report_sha256") -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop(field, None)
    if not isinstance(claimed, str) or claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field} seal")
    return value


def bound_rows(binding: Any, label: str) -> tuple[Path, list[dict[str, Any]]]:
    if not isinstance(binding, dict) or not isinstance(binding.get("path"), str):
        raise ValueError(f"{label}: missing artifact binding")
    path = Path(binding["path"])
    if not path.is_file() or binding.get("sha256") != file_sha256(path):
        raise ValueError(f"{label}: artifact hash mismatch")
    if "bytes" in binding and binding["bytes"] != path.stat().st_size:
        raise ValueError(f"{label}: artifact byte count mismatch")
    return path, read_jsonl(path)


def candidate_view(row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = row.get("candidate", row.get("training_candidate"))
    qualification = row.get("qualification", row.get("assignment"))
    if not isinstance(candidate, dict) or not isinstance(qualification, dict):
        raise ValueError("qualification input must contain sealed admission envelopes")
    queue_id = qualification.get("queue_id", qualification.get("id", candidate.get("id")))
    if queue_id != candidate.get("id"):
        raise ValueError("candidate and qualification IDs differ")
    return candidate, qualification


def validate_nested_evidence(qualification: dict[str, Any], identifier: str) -> None:
    evidence = qualification.get("evidence")
    required = {"teacher", "test_author", "semantic_review", "separation", "lineage"}
    if not isinstance(evidence, dict) or not required.issubset(evidence):
        raise ValueError(f"{identifier}: v2 nested evidence is incomplete")
    for name in required:
        item = evidence[name]
        if not isinstance(item, dict):
            raise ValueError(f"{identifier}: {name} evidence is malformed")
        body = dict(item)
        claimed = body.pop("evidence_sha256", None)
        if claimed != canonical_sha256(body):
            raise ValueError(f"{identifier}: {name} evidence seal is invalid")


def cell_fields(candidate: dict[str, Any], qualification: dict[str, Any]) -> tuple[str, str, str, str]:
    assignment = candidate.get("qualification_assignment", {})
    cell = qualification.get("cell_id", assignment.get("cell_id", candidate.get("cell_id")))
    capability = qualification.get(
        "primary_capability", assignment.get("primary_capability", candidate.get("primary_capability")),
    )
    lane = candidate.get("lane", qualification.get("lane"))
    task_type = candidate.get("task_type", qualification.get("task_type"))
    if not all(isinstance(item, str) and item for item in (cell, capability, lane, task_type)):
        raise ValueError(f"{candidate.get('id')}: incomplete cell identity")
    return cell, capability, lane, task_type


def admission_disposition(
    report_path: Path, envelope_path: Path, contract_version: str = "v3",
) -> tuple[dict[str, str], dict[str, dict[str, Any]], dict[str, Any]]:
    spec = contract_spec(contract_version)
    report = load_sealed(report_path)
    schema = report.get("schema_version")
    allowed_schemas = {spec["admission_schema"]}
    if contract_version == "v3":
        allowed_schemas.add("ganesh-mini-capability-qualification-admission/v1")
    if schema not in allowed_schemas:
        raise ValueError("unsupported repair-delta admission schema")
    input_binding = report.get("input")
    if (
        not isinstance(input_binding, dict)
        or input_binding.get("path") != str(envelope_path)
        or input_binding.get("sha256") != file_sha256(envelope_path)
        or ("bytes" in input_binding and input_binding["bytes"] != envelope_path.stat().st_size)
    ):
        raise ValueError("admission report does not bind its envelope input")
    admitted_path, admitted = bound_rows(report.get("outputs", {}).get("admitted"), "admitted")
    rejected_binding = report.get("outputs", {}).get("rejected")
    if not isinstance(rejected_binding, dict) or not isinstance(rejected_binding.get("path"), str):
        raise ValueError("rejected: missing artifact binding")
    rejected_path = Path(rejected_binding["path"])
    if (
        not rejected_path.is_file() or rejected_binding.get("sha256") != file_sha256(rejected_path)
        or ("bytes" in rejected_binding and rejected_binding["bytes"] != rejected_path.stat().st_size)
    ):
        raise ValueError("rejected: artifact hash mismatch")
    rejected = json.loads(rejected_path.read_text(encoding="utf-8"))
    if not isinstance(rejected, list):
        raise ValueError("rejected artifact must contain a list")
    if schema == spec["admission_schema"]:
        expected_admitted_schema = {
            "v4": "ganesh-mini-repair-delta-v4-admitted/v1",
            "v5": "ganesh-mini-repair-delta-v5-admitted/v1",
        }.get(contract_version)
        if expected_admitted_schema is not None and any(
            row.get("schema_version") != expected_admitted_schema
            for row in admitted
        ):
            raise ValueError("earlier-contract admitted evidence cannot be relabeled")
        accepted_ids = [row.get("id") for row in admitted]
        admitted_by_id = {row["id"]: row for row in admitted if isinstance(row.get("id"), str)}
        unresolved_binding = report.get("outputs", {}).get("unresolved")
        if not isinstance(unresolved_binding, dict) or not isinstance(unresolved_binding.get("path"), str):
            raise ValueError("unresolved: missing artifact binding")
        unresolved_path = Path(unresolved_binding["path"])
        if (
            not unresolved_path.is_file()
            or unresolved_binding.get("sha256") != file_sha256(unresolved_path)
            or unresolved_binding.get("bytes") != unresolved_path.stat().st_size
        ):
            raise ValueError("unresolved: artifact hash mismatch")
        unresolved = json.loads(unresolved_path.read_text(encoding="utf-8"))
        if not isinstance(unresolved, list):
            raise ValueError("unresolved artifact must contain a list")
        unresolved_ids = [row.get("id") for row in unresolved]
        status_ok = (
            report.get("status") in {"admission-complete", "failed"}
            and report.get("contract_id") == spec["contract_id"]
            and report.get("evaluation_artifacts_read") == 0
            and all(
                isinstance(report.get(field), str) and len(report[field]) == 64
                for field in (
                    "runtime_config_sha256", "admission_config_sha256",
                    "sandbox_contract_sha256", "separation_contract_sha256",
                )
            )
            and report.get("unresolved") == len(unresolved_ids)
            and report.get("counts_by_lane") == dict(sorted(Counter(
                row.get("lane") for row in admitted
            ).items()))
        )
        if contract_version == "v5":
            binding = report.get("v5_cohort_binding")
            body = dict(binding) if isinstance(binding, dict) else {}
            claimed = body.pop("binding_sha256", None)
            input_ids = [
                row.get("candidate_id", row.get("candidate", {}).get("id"))
                for row in read_jsonl(envelope_path)
            ]
            status_ok = status_ok and (
                claimed == canonical_sha256(body)
                and binding.get("schema_version")
                == "ganesh-mini-repair-delta-v5-cohort-binding/v1"
                and binding.get("contract_id") == V5_CONTRACT_ID
                and binding.get("ordered_candidate_ids") == input_ids
                and binding.get("ordered_candidate_ids_sha256") == canonical_sha256(input_ids)
                and binding.get("records") == len(input_ids)
                and binding.get("absolute_terminal_candidate_budget") == V5_TERMINAL_BUDGET
                and binding.get("absolute_new_teacher_generation_budget") == V5_NEW_TEACHER_BUDGET
            )
        qualification_ok = True
    else:
        accepted_ids = [row.get("record", {}).get("id") for row in admitted]
        admitted_by_id = {
            row["record"]["id"]: {
                **row.get("record", {}),
                **{
                    key: value for key, value in row.get("qualification", {}).items()
                    if key != "queue_id"
                },
            }
            for row in admitted if isinstance(row.get("record"), dict)
        }
        status_ok = report.get("mode") == "final" and report.get("status") in {"passed", "failed"}
        unresolved_ids = []
        qualification_ok = all(
            row.get("qualification", {}).get("queue_id") == row.get("record", {}).get("id")
            for row in admitted
        )
    rejected_ids = [row.get("id") for row in rejected]
    if (
        not status_ok
        or not qualification_ok
        or
        any(not isinstance(item, str) or not item for item in [*accepted_ids, *rejected_ids, *unresolved_ids])
        or len(set([*accepted_ids, *rejected_ids, *unresolved_ids])) != len(accepted_ids) + len(rejected_ids) + len(unresolved_ids)
        or report.get("accepted") != len(accepted_ids)
        or report.get("rejected") != len(rejected_ids)
    ):
        raise ValueError("admission dispositions are malformed or do not reconcile")
    return (
        {
            **{item: "admitted" for item in accepted_ids},
            **{item: "rejected" for item in rejected_ids},
            **{item: "unresolved" for item in unresolved_ids},
        },
        admitted_by_id,
        report,
    )


def v2_generation_equivalence(
    summary_path: Path, admission_path: Path, envelope_path: Path,
) -> tuple[dict[str, Any], set[str]]:
    summary = load_sealed(summary_path)
    admission = load_sealed(admission_path)
    if summary.get("report_sha256") != V2_SUMMARY_SHA256 or summary.get("status") != "qualification-failed":
        raise ValueError("sealed v2 qualification failure does not match the frozen contract")
    if admission.get("report_sha256") != V2_ADMISSION_SHA256:
        raise ValueError("sealed v2 admission does not match the frozen contract")
    disposition, admitted_rows, checked_admission = admission_disposition(admission_path, envelope_path)
    if checked_admission != admission:
        raise ValueError("v2 admission changed while checking equivalence")
    envelopes = read_jsonl(envelope_path)
    generation: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for row in envelopes:
        candidate, qualification = candidate_view(row)
        _, _, _, task_type = cell_fields(candidate, qualification)
        if task_type == "generation":
            validate_nested_evidence(qualification, candidate["id"])
            generation.append((candidate, qualification))
    ids = [candidate["id"] for candidate, _ in generation]
    semantic_pass = sum(
        qualification.get("evidence", {}).get("semantic_review", {}).get("verdict") == "pass"
        for _, qualification in generation
    )
    admitted_ids = set(ids) & set(admitted_rows)
    admitted_cells = {
        cell_fields(candidate, qualification)[0]
        for candidate, qualification in generation if candidate["id"] in admitted_ids
    }
    dispositioned = set(ids).issubset(disposition)
    passed = (
        len(ids) == 120 and len(set(ids)) == 120 and semantic_pass == 120
        and dispositioned and len(admitted_ids) == 114 and len(admitted_cells) == 60
    )
    evidence = {
        "passed": passed, "generated": len(ids), "semantic_passed": semantic_pass,
        "dispositioned": sum(item in disposition for item in ids),
        "admitted": len(admitted_ids), "admitted_cells": len(admitted_cells),
        "v2_summary_report_sha256": summary["report_sha256"],
        "v2_admission_report_sha256": admission["report_sha256"],
        "v2_envelopes_sha256": file_sha256(envelope_path),
        "generation_rules_unchanged_by_plan": True,
    }
    return evidence, admitted_cells


def load_queue(
    queue_path: Path, manifest_path: Path, plan_path: Path, contract_version: str = "v3",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    spec = contract_spec(contract_version)
    if file_sha256(plan_path) != spec["plan_sha256"]:
        raise ValueError("repair-delta plan hash differs from the frozen contract")
    manifest = load_sealed(manifest_path, "manifest_sha256")
    if (
        manifest.get("schema_version") != spec["queue_schema"]
        or manifest.get("plan_sha256") != spec["plan_sha256"]
        or contract_version == "v4" and (
            manifest.get("contract_version") != "v4"
            or manifest.get("contract_id") != spec["contract_id"]
        )
    ):
        raise ValueError("unsupported or unbound repair-delta queue manifest")
    rows = read_jsonl(queue_path)
    binding = manifest.get("queue")
    legacy_binding_ok = (
        isinstance(binding, dict) and binding.get("path") == str(queue_path)
        and binding.get("sha256") == file_sha256(queue_path) and binding.get("records") == len(rows)
    )
    current_binding_ok = (
        manifest.get("queue_sha256") == file_sha256(queue_path)
        and manifest.get("assignments") == len(rows)
    )
    if not (legacy_binding_ok or current_binding_ok):
        raise ValueError("repair-delta queue differs from its manifest")
    if len(rows) != 120 or len({row.get("id") for row in rows}) != 120:
        raise ValueError("repair-delta queue must contain 120 unique prebound assignments")
    rows = [dict(row, cohort=row.get("cohort", FIRST_PASS if row.get("role") == "primary" else RESERVE)) for row in rows]
    cohorts = Counter(row.get("cohort") for row in rows)
    if cohorts != {FIRST_PASS: 60, RESERVE: 60}:
        raise ValueError("repair-delta queue must prebind 60 first-pass and 60 reserve assignments")
    cells_by_cohort: dict[str, set[str]] = {FIRST_PASS: set(), RESERVE: set()}
    cell_contracts: dict[str, dict[str, tuple[str, str, str]]] = {FIRST_PASS: {}, RESERVE: {}}
    dimensions: Counter[str] = Counter()
    sources: set[tuple[Any, Any, Any]] = set()
    datasets: dict[str, Counter[str]] = {FIRST_PASS: Counter(), RESERVE: Counter()}
    for row in rows:
        required = ("cell_id", "primary_capability", "lane", "task_type", "assigned_cross_cutting_dimension")
        if (
            not all(isinstance(row.get(key), str) and row[key] for key in required)
            or row["lane"] not in LANES or row["task_type"] != "repair"
            or contract_version == "v4" and row.get("contract_id") != spec["contract_id"]
        ):
            raise ValueError(f"{row.get('id')}: invalid repair-delta assignment")
        cells_by_cohort[row["cohort"]].add(row["cell_id"])
        cell_contracts[row["cohort"]][row["cell_id"]] = (
            row["primary_capability"], row["lane"], row["assigned_cross_cutting_dimension"],
        )
        if row["cohort"] == FIRST_PASS:
            dimensions[row["assigned_cross_cutting_dimension"]] += 1
        source = row.get("source", {})
        identity = (source.get("dataset"), source.get("revision"), source.get("record_id"))
        if None in identity or identity in sources:
            raise ValueError("repair-delta source identities are incomplete or duplicated")
        sources.add(identity)
        datasets[row["cohort"]][source["dataset"]] += 1
    if cells_by_cohort[FIRST_PASS] != cells_by_cohort[RESERVE] or len(cells_by_cohort[FIRST_PASS]) != 60:
        raise ValueError("first-pass and reserve cohorts must prebind the same 60 repair cells")
    if cell_contracts[FIRST_PASS] != cell_contracts[RESERVE]:
        raise ValueError("reserve cell contracts differ from their first-pass assignments")
    first_rows = [row for row in rows if row["cohort"] == FIRST_PASS]
    if (
        sorted(Counter(row["lane"] for row in first_rows).values()) != [10] * 6
        or sorted(Counter(row["primary_capability"] for row in first_rows).values()) != [6] * 10
    ):
        raise ValueError("repair-delta queue is not a ten-capability by six-lane matrix")
    if sorted(dimensions.values()) != [12] * 5:
        raise ValueError("first-pass cross-cutting dimensions must contain twelve assignments each")
    expected_dataset_counts = {
        "primary": dict(sorted(datasets[FIRST_PASS].items())),
        "reserve": dict(sorted(datasets[RESERVE].items())),
    }
    if (
        manifest.get("status") != "sealed-primary-generation-eligible"
        or manifest.get("seed") != spec["queue_seed"]
        or manifest.get("assignments") != 120
        or manifest.get("primary_assignments") != 60
        or manifest.get("cell_bound_reserves") != 60
        or manifest.get("initial_generation_eligible") != 60
        or manifest.get("maximum_reserve_generation_eligible") != 6
        or manifest.get("absolute_candidate_budget") != 66
        or manifest.get("unique_source_identities") != 120
        or manifest.get("evaluation_artifacts_read") != 0
        or manifest.get("dataset_counts") != expected_dataset_counts
        or any(len(value) < 2 or max(value.values(), default=0) > 30 for value in datasets.values())
    ):
        raise ValueError("repair-delta queue manifest constants or dataset counts are invalid")
    return rows, manifest


def load_v5_queue(
    *, plan_path: Path, source_addendum_path: Path, budget_addendum_path: Path,
    exclusion_path: Path, carry_path: Path, source_path: Path, cohort_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    contract = load_v5_contract(
        plan_path=plan_path, source_addendum_path=source_addendum_path,
        budget_addendum_path=budget_addendum_path, exclusion_path=exclusion_path,
        carry_path=carry_path, source_path=source_path, cohort_path=cohort_path,
    )
    rows: list[dict[str, Any]] = []
    for row in contract["primary_rows"]:
        rows.append({
            "id": row["candidate_id"], "cell_id": row["cell_id"],
            "lane": row["lane"], "primary_capability": row["primary_capability"],
            "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
            "task_type": "repair", "cohort": FIRST_PASS,
            "contract_id": V5_CONTRACT_ID, "mode": row["mode"],
        })
    for row in contract["reserve_rows"]:
        rows.append({
            "id": row["candidate_id"], "cell_id": row["cell_id"],
            "lane": row["lane"], "primary_capability": row["primary_capability"],
            "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
            "task_type": "repair", "cohort": RESERVE,
            "contract_id": V5_CONTRACT_ID,
        })
    manifest = {
        "manifest_sha256": contract["cohort_manifest_sha256"],
        "source_manifest_sha256": contract["source_manifest_sha256"],
        "exclusion_ledger_sha256": contract["exclusion_ledger_sha256"],
        "carry_manifest_sha256": contract["carry_manifest_sha256"],
        "source_feasibility_addendum_sha256": V5_SOURCE_ADDENDUM_SHA256,
        "budget_clarification_addendum_sha256": V5_BUDGET_ADDENDUM_SHA256,
        "unreserved_cell": V5_UNRESERVED_CELL,
    }
    return rows, manifest


def cohort_state(
    envelope_path: Path | None, admission_path: Path | None, expected: dict[str, dict[str, Any]], cohort: str,
    contract_version: str = "v3", expected_order: list[str] | None = None,
) -> tuple[dict[str, Any], dict[str, str], dict[str, tuple[str, str, str]]]:
    if envelope_path is None and admission_path is None:
        return {"generated": 0, "dispositioned": 0, "admitted": 0, "rejected": 0}, {}, {}
    if envelope_path is None or admission_path is None:
        raise ValueError(f"{cohort}: envelope and admission report must be supplied together")
    envelopes = read_jsonl(envelope_path)
    if expected_order is not None:
        actual_order = [
            row.get("candidate_id", row.get("candidate", {}).get("id")) for row in envelopes
        ]
        if actual_order != expected_order:
            if len(actual_order) != len(expected_order) or set(actual_order) != set(expected_order):
                raise ValueError(f"{cohort}: terminal artifacts do not cover the exact bound cohort")
            raise ValueError(f"{cohort}: terminal artifacts do not preserve bound cohort order")
    spec = contract_spec(contract_version)
    disposition, admitted_rows, admission_report = admission_disposition(
        admission_path, envelope_path, contract_version,
    )
    metadata: dict[str, tuple[str, str, str]] = {}
    for row in envelopes:
        if row.get("schema_version") == spec["assembly_schema"]:
            body = dict(row); claimed = body.pop("artifact_sha256", None)
            identifier = row.get("candidate_id")
            if claimed != canonical_sha256(body) or not isinstance(identifier, str):
                raise ValueError(f"{cohort}: unsealed evidence assembly artifact")
            if row.get("status") == "ready-for-admission":
                candidate, qualification = candidate_view(row.get("envelope", {}))
                if candidate.get("id") != identifier:
                    raise ValueError(f"{identifier}: assembly envelope ID differs")
            elif row.get("status") in {"terminal-rejected", "unresolved"}:
                queue_row = expected.get(identifier)
                if queue_row is None or row.get("cell_id") != queue_row.get("cell_id"):
                    raise ValueError(f"{identifier}: terminal artifact differs from its prebound cell")
                metadata[identifier] = (
                    queue_row["cell_id"], queue_row["primary_capability"],
                    queue_row["lane"], queue_row["assigned_cross_cutting_dimension"],
                )
                continue
            else:
                raise ValueError(f"{identifier}: unknown assembly disposition")
        else:
            if contract_version in {"v4", "v5"} and row.get("schema_version") != spec["envelope_schema"]:
                raise ValueError(f"{cohort}: earlier-contract evidence cannot be relabeled")
            candidate, qualification = candidate_view(row)
            identifier = candidate["id"]
        queue_row = expected.get(identifier)
        cell, capability, lane, task_type = cell_fields(candidate, qualification)
        assignment = candidate.get("qualification_assignment", {})
        dimension = qualification.get(
            "assigned_cross_cutting_dimension", assignment.get("assigned_cross_cutting_dimension"),
        )
        if (
            queue_row is None or queue_row.get("cohort") != cohort
            or contract_version in {"v4", "v5"} and qualification.get("contract_id") != spec["contract_id"]
            or (cell, capability, lane, task_type, dimension) != (
                queue_row["cell_id"], queue_row["primary_capability"], queue_row["lane"],
                "repair", queue_row["assigned_cross_cutting_dimension"],
            )
            or identifier in metadata
        ):
            raise ValueError(f"{identifier}: candidate differs from its prebound {cohort} assignment")
        metadata[identifier] = (cell, capability, lane, dimension)
    if set(disposition) != set(metadata):
        raise ValueError(f"{cohort}: admission must terminally disposition every supplied candidate")
    if any(
        row.get("cell_id") != metadata[identifier][0]
        or row.get("lane") != metadata[identifier][2]
        or row.get("primary_capability") != metadata[identifier][1]
        or row.get("assigned_cross_cutting_dimension") != metadata[identifier][3]
        for identifier, row in admitted_rows.items()
    ):
        raise ValueError(f"{cohort}: admitted output differs from its prebound assignment")
    return {
        "generated": len(metadata),
        "dispositioned": sum(value in {"admitted", "rejected"} for value in disposition.values()),
        "admitted": sum(value == "admitted" for value in disposition.values()),
        "rejected": sum(value == "rejected" for value in disposition.values()),
        "unresolved": sum(value == "unresolved" for value in disposition.values()),
        "envelopes": {
            "path": str(envelope_path), "sha256": file_sha256(envelope_path),
            "bytes": envelope_path.stat().st_size,
        },
        "admission_report": {
            "path": str(admission_path), "sha256": file_sha256(admission_path),
            "report_sha256": admission_report["report_sha256"],
        },
    }, disposition, metadata


def summarize(
    *, plan_path: Path, queue_path: Path | None, queue_manifest_path: Path | None,
    v2_summary_path: Path, v2_admission_path: Path, v2_envelopes_path: Path,
    first_envelopes_path: Path | None = None, first_admission_path: Path | None = None,
    reserve_envelopes_path: Path | None = None, reserve_admission_path: Path | None = None,
    contract_version: str = "v3",
    source_addendum_path: Path | None = None, budget_addendum_path: Path | None = None,
    exclusion_path: Path | None = None, carry_path: Path | None = None,
    source_path: Path | None = None, cohort_path: Path | None = None,
) -> dict[str, Any]:
    spec = contract_spec(contract_version)
    generation, generation_cells = v2_generation_equivalence(
        v2_summary_path, v2_admission_path, v2_envelopes_path,
    )
    if contract_version == "v5":
        required = (
            source_addendum_path, budget_addendum_path, exclusion_path,
            carry_path, source_path, cohort_path,
        )
        if any(path is None for path in required):
            raise ValueError("V5 qualification requires all sealed cohort/addendum artifacts")
        queue, manifest = load_v5_queue(
            plan_path=plan_path, source_addendum_path=source_addendum_path,
            budget_addendum_path=budget_addendum_path, exclusion_path=exclusion_path,
            carry_path=carry_path, source_path=source_path, cohort_path=cohort_path,
        )
    else:
        if queue_path is None or queue_manifest_path is None:
            raise ValueError("V3/V4 qualification requires queue and queue manifest")
        queue, manifest = load_queue(queue_path, queue_manifest_path, plan_path, contract_version)
    by_id = {row["id"]: row for row in queue}
    ordered_primary = [row["id"] for row in queue if row["cohort"] == FIRST_PASS]
    ordered_reserve = None
    if contract_version == "v5" and reserve_envelopes_path is not None:
        supplied = read_jsonl(reserve_envelopes_path)
        supplied_ids = {
            row.get("candidate_id", row.get("candidate", {}).get("id")) for row in supplied
        }
        ordered_reserve = [
            row["id"] for row in queue
            if row["cohort"] == RESERVE and row["id"] in supplied_ids
        ]
    first, first_disposition, first_meta = cohort_state(
        first_envelopes_path, first_admission_path, by_id, FIRST_PASS, contract_version,
        ordered_primary if contract_version == "v5" and first_envelopes_path is not None else None,
    )
    reserve, reserve_disposition, reserve_meta = cohort_state(
        reserve_envelopes_path, reserve_admission_path, by_id, RESERVE, contract_version,
        ordered_reserve,
    )
    first_admitted = {item for item, state in first_disposition.items() if state == "admitted"}
    first_rejected = {item for item, state in first_disposition.items() if state == "rejected"}
    rejected_cells = {first_meta[item][0] for item in first_rejected}
    reserve_cells = {value[0] for value in reserve_meta.values()}
    maximum_reserves = V5_MAX_RESERVES if contract_version == "v5" else 6
    if len(reserve_meta) > maximum_reserves or not reserve_cells.issubset(rejected_cells):
        limit_label = "five" if contract_version == "v5" else "six"
        raise ValueError(f"reserves exceed {limit_label} or were not generated for first-pass rejected cells")

    lane_counts = Counter(first_meta[item][2] for item in first_admitted)
    capability_counts = Counter(first_meta[item][1] for item in first_admitted)
    dimension_counts = Counter(first_meta[item][3] for item in first_admitted)
    # An unresolved result after its one byte-identical infrastructure replay
    # is terminal under the frozen v3 contract.  It fails the tranche, but it
    # must still count toward completion of the 60-candidate first pass so a
    # terminal infrastructure outcome cannot leave a failed campaign looking
    # indefinitely in progress.
    first_complete = (
        first["generated"] == 60
        and first["dispositioned"] + first.get("unresolved", 0) == 60
    )
    thresholds = {
        "complete_60": first_complete,
        "zero_unresolved": first.get("unresolved", 0) == 0,
        "minimum_54_admitted": first["admitted"] >= 54,
        "minimum_9_per_lane": len(lane_counts) == 6 and min(lane_counts.values(), default=0) >= 9,
        "minimum_5_per_capability": len(capability_counts) == 10 and min(capability_counts.values(), default=0) >= 5,
        "minimum_10_per_dimension": len(dimension_counts) == 5 and min(dimension_counts.values(), default=0) >= 10,
    }
    unreserved_failed = contract_version == "v5" and any(
        first_meta[item][0] == V5_UNRESERVED_CELL
        for item, disposition in first_disposition.items()
        if disposition in {"rejected", "unresolved"}
    )
    if contract_version == "v5":
        thresholds["unreserved_java_graph_tree_passed"] = not unreserved_failed
    first_passed = all(thresholds.values())
    reserve_required = len(first_rejected) if first_complete and first_passed else 0
    if reserve_meta and not first_passed:
        raise ValueError("reserves were generated before every first-pass threshold passed")
    if reserve_required > maximum_reserves:
        raise ValueError(f"first-pass result requires more than {maximum_reserves} reserves")

    repair_admitted_cells = {first_meta[item][0] for item in first_admitted}
    repair_admitted_cells.update(
        reserve_meta[item][0] for item, state in reserve_disposition.items() if state == "admitted"
    )
    reserves_complete = reserve_required == 0 or (
        reserve["generated"] == reserve_required
        and reserve["dispositioned"] == reserve_required
        and reserve_cells == rejected_cells
    )
    final_admitted = first["admitted"] + reserve["admitted"]
    repair_coverage = len(repair_admitted_cells)
    combined_coverage = len(generation_cells) + repair_coverage
    passed = (
        generation["passed"] and first_passed and reserves_complete
        and repair_coverage == 60 and final_admitted >= 60 and combined_coverage == 120
    )
    if passed:
        status = f"qualification-passed-via-{contract_version}-repair-delta"
    elif not generation["passed"] or (first_complete and not first_passed) or (
        first_passed and reserves_complete and repair_coverage < 60
    ):
        status = "qualification-failed"
    else:
        status = "qualification-in-progress"

    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION, "status": status, "gate_passed": passed,
        "contract": {
            "identifier": spec["contract_id"],
            **({"version": contract_version} if contract_version in {"v4", "v5"} else {}),
            "first_pass_candidates": 60, "maximum_reserves": maximum_reserves,
            "absolute_candidate_budget": V5_TERMINAL_BUDGET if contract_version == "v5" else 66,
            **({"absolute_new_teacher_generation_budget": V5_NEW_TEACHER_BUDGET,
                "immutable_carries": 58, "fresh_teacher_primaries": 2,
                "prebound_reserves": 59, "unreserved_cell": V5_UNRESERVED_CELL}
               if contract_version == "v5" else {}),
            "repair_cells": 60, "combined_cells": 120,
        },
        "inputs": {
            "plan": {"path": str(plan_path), "sha256": file_sha256(plan_path)},
            **({
                "v5_cohort_manifest": {"path": str(cohort_path), "sha256": file_sha256(cohort_path),
                                       "manifest_sha256": manifest["manifest_sha256"]},
                "v5_source_manifest": {"path": str(source_path), "sha256": file_sha256(source_path),
                                       "manifest_sha256": manifest["source_manifest_sha256"]},
                "source_feasibility_addendum_sha256": V5_SOURCE_ADDENDUM_SHA256,
                "budget_clarification_addendum_sha256": V5_BUDGET_ADDENDUM_SHA256,
            } if contract_version == "v5" else {
                "queue": {"path": str(queue_path), "sha256": file_sha256(queue_path)},
                "queue_manifest": {"path": str(queue_manifest_path),
                                   "sha256": file_sha256(queue_manifest_path),
                                   "manifest_sha256": manifest["manifest_sha256"]},
            }),
            "evaluation_artifacts_read": 0,
        },
        "generation_equivalence": generation,
        "first_pass": {
            **first, "thresholds": thresholds, "thresholds_passed": first_passed,
            "by_lane_admitted": dict(sorted(lane_counts.items())),
            "by_capability_admitted": dict(sorted(capability_counts.items())),
            "by_dimension_admitted": dict(sorted(dimension_counts.items())),
            "rejected_ids": sorted(first_rejected), "rejected_cells": sorted(rejected_cells),
            **({"unreserved_cell_failed": unreserved_failed} if contract_version == "v5" else {}),
        },
        "reserves": {
            **reserve, "required": reserve_required,
            "eligible_cells": sorted(rejected_cells) if first_passed else [],
            "generated_cells": sorted(reserve_cells), "complete": reserves_complete,
            "remaining_cells": sorted(rejected_cells - reserve_cells),
        },
        "final": {
            "repair_admitted": final_admitted, "repair_cells_covered": repair_coverage,
            "missing_repair_cells": sorted({row["cell_id"] for row in queue if row["cohort"] == FIRST_PASS} - repair_admitted_cells),
            "generation_cells_covered": len(generation_cells), "combined_cells_covered": combined_coverage,
        },
        "pass_requirements": {
            "v2_generation_equivalent": generation["passed"],
            "first_pass_thresholds_met": first_passed,
            "reserves_complete": reserves_complete,
            "repair_60_of_60_cells": repair_coverage == 60,
            "minimum_60_repair_admitted": final_admitted >= 60,
            "combined_120_of_120_cells": combined_coverage == 120,
        },
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def reserve_eligibility(
    report: dict[str, Any], report_path: Path, contract_version: str = "v3",
) -> dict[str, Any]:
    spec = contract_spec(contract_version)
    first = report["first_pass"]
    rejected_ids = first.get("rejected_ids")
    rejected_cells = first.get("rejected_cells")
    if (
        report.get("schema_version") != SCHEMA_VERSION
        or report.get("contract", {}).get("identifier") != spec["contract_id"]
        or contract_version in {"v4", "v5"}
        and report.get("contract", {}).get("version") != contract_version
        or report.get("generation_equivalence", {}).get("passed") is not True
        or first.get("thresholds_passed") is not True
        or first.get("generated") != 60 or first.get("dispositioned") != 60
        or not isinstance(rejected_ids, list) or not isinstance(rejected_cells, list)
        or not 1 <= len(rejected_ids) == len(rejected_cells) <= (
            V5_MAX_RESERVES if contract_version == "v5" else 6
        )
        or contract_version == "v5" and V5_UNRESERVED_CELL in rejected_cells
        or report.get("reserves", {}).get("required") != len(rejected_ids)
        or report.get("reserves", {}).get("generated") != 0
    ):
        raise ValueError("reserve eligibility requires a complete passing first pass within its reserve budget")
    value: dict[str, Any] = {
        "schema_version": (
            "ganesh-mini-repair-delta-v5-reserve-eligibility/v1"
            if contract_version == "v5"
            else "ganesh-mini-repair-delta-reserve-eligibility/v1"
        ),
        "contract_id": spec["contract_id"], "plan_sha256": spec["plan_sha256"],
        **({
            "source_feasibility_addendum_sha256": V5_SOURCE_ADDENDUM_SHA256,
            "budget_clarification_addendum_sha256": V5_BUDGET_ADDENDUM_SHA256,
            "cohort_manifest_sha256": report["inputs"]["v5_cohort_manifest"]["manifest_sha256"],
            "source_manifest_sha256": report["inputs"]["v5_source_manifest"]["manifest_sha256"],
        } if contract_version == "v5" else {
            "queue_manifest_sha256": report["inputs"]["queue_manifest"]["manifest_sha256"],
        }),
        "summary": {
            "path": str(report_path), "sha256": file_sha256(report_path),
            "report_sha256": report["report_sha256"],
        },
        "first_pass_admission_report_sha256": first["admission_report"]["report_sha256"],
        "first_pass_envelopes_sha256": first["envelopes"]["sha256"],
        "first_pass_thresholds_passed": True,
        "rejected_candidate_ids": rejected_ids, "rejected_cell_ids": rejected_cells,
        "reserves_authorized": len(rejected_cells), "evaluation_artifacts_read": 0,
    }
    value["eligibility_sha256"] = canonical_sha256(value)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract-version", choices=("v3", "v4", "v5"), default="v3")
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--queue-manifest", type=Path)
    parser.add_argument("--source-feasibility-addendum", type=Path)
    parser.add_argument("--budget-clarification-addendum", type=Path)
    parser.add_argument("--exclusion-ledger", type=Path)
    parser.add_argument("--carry-manifest", type=Path)
    parser.add_argument("--source-manifest", type=Path)
    parser.add_argument("--cohort-manifest", type=Path)
    parser.add_argument("--v2-summary", type=Path, required=True)
    parser.add_argument("--v2-admission-report", type=Path, required=True)
    parser.add_argument("--v2-envelopes", type=Path, required=True)
    parser.add_argument("--first-pass-envelopes", type=Path)
    parser.add_argument("--first-pass-admission-report", type=Path)
    parser.add_argument("--reserve-envelopes", type=Path)
    parser.add_argument("--reserve-admission-report", type=Path)
    parser.add_argument("--reserve-eligibility-output", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = summarize(
        plan_path=args.plan, queue_path=args.queue, queue_manifest_path=args.queue_manifest,
        v2_summary_path=args.v2_summary, v2_admission_path=args.v2_admission_report,
        v2_envelopes_path=args.v2_envelopes,
        first_envelopes_path=args.first_pass_envelopes,
        first_admission_path=args.first_pass_admission_report,
        reserve_envelopes_path=args.reserve_envelopes,
        reserve_admission_path=args.reserve_admission_report,
        contract_version=args.contract_version,
        source_addendum_path=args.source_feasibility_addendum,
        budget_addendum_path=args.budget_clarification_addendum,
        exclusion_path=args.exclusion_ledger, carry_path=args.carry_manifest,
        source_path=args.source_manifest, cohort_path=args.cohort_manifest,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.reserve_eligibility_output is not None:
        eligibility = reserve_eligibility(report, args.output, args.contract_version)
        args.reserve_eligibility_output.parent.mkdir(parents=True, exist_ok=True)
        args.reserve_eligibility_output.write_text(
            json.dumps(eligibility, indent=2, sort_keys=True) + "\n", encoding="utf-8",
        )
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
