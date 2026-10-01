#!/usr/bin/env python3
"""Fail-closed loaders and accounting rules for the sealed V5 cohort."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256


CONTRACT_ID = "capability-stratified-v5-interface-replay/v1"
PLAN_SHA256 = "132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b"
SOURCE_ADDENDUM_SHA256 = "01a8415fa9122f163aa58f5cf6578bb1ff2502346cb197a11af14b373d922da3"
BUDGET_ADDENDUM_SHA256 = "1933b409b656ab90cf4a82e44b0b2b7dc29d4701d3a162add64db179319a4899"
EXCLUSION_SCHEMA = "ganesh-mini-gate2-v5-exclusion-ledger/v1"
CARRY_SCHEMA = "ganesh-mini-gate2-v5-immutable-carry-manifest/v1"
SOURCE_SCHEMA = "ganesh-mini-gate2-v5-source-manifest/v1"
COHORT_SCHEMA = "ganesh-mini-gate2-v5-ordered-cohort-manifest/v1"
REPLACEMENT_CELLS = {
    "numeric_reasoning/typescript/repair",
    "stateful_workflows/typescript/repair",
}
UNRESERVED_CELL = "graph_and_tree/java/repair"
TERMINAL_BUDGET = 65
NEW_TEACHER_BUDGET = 7
EFFECTIVE_MAX_RESERVES = 5


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    body = dict(value)
    claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def _validate_row_seals(rows: Any, field: str, expected: int, label: str) -> list[dict[str, Any]]:
    if not isinstance(rows, list) or len(rows) != expected:
        raise ValueError(f"V5 {label} must contain exactly {expected} rows")
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"V5 {label} contains a malformed row")
        body = dict(row)
        claimed = body.pop(field, None)
        if claimed != canonical_sha256(body):
            raise ValueError(f"V5 {label} row seal mismatch")
    return rows


def load_v5_contract(
    *, plan_path: Path, source_addendum_path: Path, budget_addendum_path: Path,
    exclusion_path: Path,
    carry_path: Path, source_path: Path, cohort_path: Path,
) -> dict[str, Any]:
    """Load and cross-bind the immutable V5 cohort and its 59 reserves."""
    if file_sha256(plan_path) != PLAN_SHA256:
        raise ValueError("V5 plan hash differs from the frozen contract")
    if file_sha256(source_addendum_path) != SOURCE_ADDENDUM_SHA256:
        raise ValueError("V5 source-feasibility addendum hash differs")
    if file_sha256(budget_addendum_path) != BUDGET_ADDENDUM_SHA256:
        raise ValueError("V5 budget-clarification addendum hash differs")
    exclusion = _sealed(exclusion_path, "ledger_sha256")
    carries = _sealed(carry_path, "manifest_sha256")
    sources = _sealed(source_path, "manifest_sha256")
    cohort = _sealed(cohort_path, "manifest_sha256")
    for value, schema in (
        (exclusion, EXCLUSION_SCHEMA), (carries, CARRY_SCHEMA),
        (sources, SOURCE_SCHEMA), (cohort, COHORT_SCHEMA),
    ):
        if (
            value.get("schema_version") != schema
            or value.get("contract_id") != CONTRACT_ID
            or value.get("plan_sha256") != PLAN_SHA256
            or value.get("budget_clarification_addendum_sha256") != BUDGET_ADDENDUM_SHA256
            or value.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError("V5 contract artifact identity or separation marker differs")
    for value in (carries, sources, cohort):
        if value.get("source_feasibility_addendum_sha256") != SOURCE_ADDENDUM_SHA256:
            raise ValueError("V5 artifact does not bind the source-feasibility addendum")
    if (
        sources.get("exclusion_ledger_sha256") != exclusion["ledger_sha256"]
        or cohort.get("exclusion_ledger_sha256") != exclusion["ledger_sha256"]
        or cohort.get("carry_manifest_sha256") != carries["manifest_sha256"]
        or cohort.get("source_manifest_sha256") != sources["manifest_sha256"]
    ):
        raise ValueError("V5 manifests do not cross-bind")

    carry_rows = _validate_row_seals(carries.get("rows"), "carry_row_sha256", 58, "carry manifest")
    source_rows = _validate_row_seals(sources.get("selections"), "selection_row_sha256", 61, "source manifest")
    cohort_rows = _validate_row_seals(cohort.get("rows"), "cohort_row_sha256", 60, "ordered cohort")
    if carries.get("rows_sha256") != canonical_sha256(carry_rows):
        raise ValueError("V5 carry rows hash differs")
    if sources.get("selections_sha256") != canonical_sha256(source_rows):
        raise ValueError("V5 source selections hash differs")
    if cohort.get("ordered_cohort_sha256") != canonical_sha256(cohort_rows):
        raise ValueError("V5 ordered cohort hash differs")

    primary_sources = [row for row in source_rows if row.get("role") == "primary"]
    reserve_sources = [row for row in source_rows if row.get("role") == "reserve"]
    if (
        len(primary_sources) != 2 or len(reserve_sources) != 59
        or sources.get("fresh_primary_sources") != 2
        or sources.get("prebound_reserve_sources") != 59
        or sources.get("unreserved_cells") != [UNRESERVED_CELL]
        or sources.get("unique_selected_source_identities") != 61
        or cohort.get("records") != 60
        or cohort.get("immutable_carries") != 58
        or cohort.get("fresh_teacher_primaries") != 2
        or cohort.get("prebound_reserves") != 59
        or cohort.get("unreserved_cells") != [UNRESERVED_CELL]
        or cohort.get("absolute_terminal_candidate_budget") != TERMINAL_BUDGET
        or cohort.get("absolute_new_teacher_generation_budget") != NEW_TEACHER_BUDGET
        or cohort.get("maximum_generated_reserves") != EFFECTIVE_MAX_RESERVES
    ):
        raise ValueError("V5 cohort counts or budgets differ from the amended contract")
    modes = Counter(row.get("mode") for row in cohort_rows)
    if modes != {"immutable-v4-teacher-carry": 58, "fresh-v5-teacher-primary": 2}:
        raise ValueError("V5 cohort is not exactly 58 carries plus two fresh primaries")
    if [row.get("ordinal") for row in cohort_rows] != list(range(60)):
        raise ValueError("V5 cohort ordinal order differs")
    primary_ids = [row.get("candidate_id") for row in cohort_rows]
    primary_cells = [row.get("cell_id") for row in cohort_rows]
    if (
        any(not isinstance(item, str) or not item for item in primary_ids + primary_cells)
        or len(set(primary_ids)) != 60 or len(set(primary_cells)) != 60
        or {row["cell_id"] for row in cohort_rows if row["mode"] == "fresh-v5-teacher-primary"}
        != REPLACEMENT_CELLS
    ):
        raise ValueError("V5 primary identities or replacement cells differ")
    carry_by_hash = {row["carry_row_sha256"]: row for row in carry_rows}
    primary_by_hash = {row["selection_row_sha256"]: row for row in primary_sources}
    for row in cohort_rows:
        if row["mode"] == "immutable-v4-teacher-carry":
            carried = carry_by_hash.get(row.get("carry_row_sha256"))
            if carried is None or (carried.get("v4_candidate_id"), carried.get("cell_id")) != (
                row["candidate_id"], row["cell_id"],
            ):
                raise ValueError("V5 carry cohort row does not bind its immutable V4 artifact")
        else:
            fresh = primary_by_hash.get(row.get("source_selection_row_sha256"))
            if fresh is None or (fresh.get("candidate_id"), fresh.get("cell_id")) != (
                row["candidate_id"], row["cell_id"],
            ):
                raise ValueError("V5 fresh cohort row does not bind its source selection")
    reserve_cells = [row.get("cell_id") for row in reserve_sources]
    if (
        len(set(reserve_cells)) != 59 or UNRESERVED_CELL in reserve_cells
        or set(reserve_cells) != set(primary_cells) - {UNRESERVED_CELL}
        or len({row.get("candidate_id") for row in reserve_sources}) != 59
    ):
        raise ValueError("V5 59-reserve exception semantics differ")
    return {
        "plan_sha256": PLAN_SHA256,
        "source_addendum_sha256": SOURCE_ADDENDUM_SHA256,
        "budget_addendum_sha256": BUDGET_ADDENDUM_SHA256,
        "exclusion_ledger_sha256": exclusion["ledger_sha256"],
        "carry_manifest_sha256": carries["manifest_sha256"],
        "source_manifest_sha256": sources["manifest_sha256"],
        "cohort_manifest_sha256": cohort["manifest_sha256"],
        "primary_rows": cohort_rows,
        "reserve_rows": reserve_sources,
        "ordered_primary_ids": primary_ids,
        "unreserved_cell": UNRESERVED_CELL,
        "terminal_budget": TERMINAL_BUDGET,
        "new_teacher_budget": NEW_TEACHER_BUDGET,
        "effective_max_reserves": EFFECTIVE_MAX_RESERVES,
    }


def validate_terminal_order(rows: list[Any], expected_ids: list[str], schema: str) -> None:
    actual: list[Any] = []
    for row in rows:
        if (
            not isinstance(row, dict) or row.get("schema_version") != schema
            or row.get("status") not in {"ready-for-admission", "terminal-rejected", "unresolved"}
        ):
            raise ValueError("V5 final accounting requires canonical terminal artifacts")
        actual.append(row.get("candidate_id"))
    if actual != expected_ids:
        if len(actual) != len(expected_ids) or set(actual) != set(expected_ids):
            raise ValueError("V5 terminal artifacts do not cover the exact bound cohort")
        raise ValueError("V5 terminal artifacts do not preserve bound cohort order")


def cohort_binding(
    contract: dict[str, Any], cohort: str,
    reserve_eligibility_path: Path | None = None,
) -> dict[str, Any]:
    if cohort == "primary":
        rows = contract["primary_rows"]
    elif cohort == "reserve":
        if reserve_eligibility_path is None:
            raise ValueError("V5 reserve admission requires sealed reserve eligibility")
        eligibility = _sealed(reserve_eligibility_path, "eligibility_sha256")
        rejected = eligibility.get("rejected_cell_ids")
        rejected_ids = eligibility.get("rejected_candidate_ids")
        primary_cell_by_id = {
            row["candidate_id"]: row["cell_id"] for row in contract["primary_rows"]
        }
        if (
            eligibility.get("schema_version") != "ganesh-mini-repair-delta-v5-reserve-eligibility/v1"
            or eligibility.get("contract_id") != CONTRACT_ID
            or eligibility.get("plan_sha256") != PLAN_SHA256
            or eligibility.get("source_feasibility_addendum_sha256") != SOURCE_ADDENDUM_SHA256
            or eligibility.get("budget_clarification_addendum_sha256") != BUDGET_ADDENDUM_SHA256
            or eligibility.get("cohort_manifest_sha256") != contract["cohort_manifest_sha256"]
            or eligibility.get("source_manifest_sha256") != contract["source_manifest_sha256"]
            or eligibility.get("first_pass_thresholds_passed") is not True
            or eligibility.get("evaluation_artifacts_read") != 0
            or not isinstance(rejected, list)
            or not 1 <= len(rejected) <= EFFECTIVE_MAX_RESERVES
            or len(set(rejected)) != len(rejected)
            or not isinstance(rejected_ids, list)
            or len(rejected_ids) != len(rejected)
            or len(set(rejected_ids)) != len(rejected_ids)
            or {primary_cell_by_id.get(identifier) for identifier in rejected_ids} != set(rejected)
            or eligibility.get("reserves_authorized") != len(rejected)
            or UNRESERVED_CELL in rejected
        ):
            raise ValueError("V5 reserve eligibility is malformed or violates amended budgets")
        reserve_by_cell = {row["cell_id"]: row for row in contract["reserve_rows"]}
        primary_cell_order = [row["cell_id"] for row in contract["primary_rows"]]
        if any(cell not in reserve_by_cell for cell in rejected):
            raise ValueError("V5 reserve eligibility names a cell without a prebound reserve")
        rows = [reserve_by_cell[cell] for cell in primary_cell_order if cell in set(rejected)]
    else:
        raise ValueError("V5 cohort must be primary or reserve")
    ids = [row["candidate_id"] for row in rows]
    value: dict[str, Any] = {
        "schema_version": "ganesh-mini-repair-delta-v5-cohort-binding/v1",
        "contract_id": CONTRACT_ID,
        "cohort": cohort,
        "cohort_manifest_sha256": contract["cohort_manifest_sha256"],
        "source_manifest_sha256": contract["source_manifest_sha256"],
        "ordered_candidate_ids": ids,
        "ordered_candidate_ids_sha256": canonical_sha256(ids),
        "records": len(ids),
        "absolute_terminal_candidate_budget": TERMINAL_BUDGET,
        "absolute_new_teacher_generation_budget": NEW_TEACHER_BUDGET,
    }
    value["binding_sha256"] = canonical_sha256(value)
    return value
