#!/usr/bin/env python3
"""Freeze the content-blind V5 interface-replay cohort and source bindings.

This constructor performs no model calls and executes no generated code.  It
validates the immutable V4 teacher rows, selects the two V5 TypeScript primary
sources plus fifty-nine reserves from sealed ontology decisions, and emits four
sealed JSON manifests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_repair_delta import teacher_candidate_sha256  # noqa: E402
from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256  # noqa: E402
from scripts.data.build_repair_delta_queue import (  # noqa: E402
    AFFINITY_FIELDS, repair_cells, source_key,
)


PLAN_SHA256 = "132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b"
SOURCE_FEASIBILITY_ADDENDUM_SHA256 = "01a8415fa9122f163aa58f5cf6578bb1ff2502346cb197a11af14b373d922da3"
BUDGET_CLARIFICATION_ADDENDUM_SHA256 = "1933b409b656ab90cf4a82e44b0b2b7dc29d4701d3a162add64db179319a4899"
CONTRACT_ID = "capability-stratified-v5-interface-replay/v1"
V4_CONTRACT_ID = "capability-stratified-v4-repair-delta/v1"
V4_PLAN_SHA256 = "79849d2f8b70ba69572b4c3fa1761bdb413562c6f6d9a12537d93a1724812ef6"
PRIMARY_SEED = "ganesh-mini-gate2-v5-interface-replay-primary-v1"
RESERVE_SEED = "ganesh-mini-gate2-v5-interface-replay-reserve-v1"
REPLACEMENT_CELLS = (
    "numeric_reasoning/typescript/repair",
    "stateful_workflows/typescript/repair",
)
UNRESERVED_CELLS = ("graph_and_tree/java/repair",)
EXCLUSION_SCHEMA = "ganesh-mini-gate2-v5-exclusion-ledger/v1"
CARRY_SCHEMA = "ganesh-mini-gate2-v5-immutable-carry-manifest/v1"
SOURCE_SCHEMA = "ganesh-mini-gate2-v5-source-manifest/v1"
COHORT_SCHEMA = "ganesh-mini-gate2-v5-ordered-cohort-manifest/v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_sealed(path: Path, seal_field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    body = dict(value)
    claimed = body.pop(seal_field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {seal_field}")
    return value


def identity_dict(row: dict[str, Any]) -> dict[str, str]:
    dataset, revision, record_id = source_key(row)
    return {"dataset": dataset, "revision": revision, "record_id": record_id}


def collect_exclusions(
    prior_path: Path, v2_paths: list[Path], v3_path: Path,
    v4_path: Path, v4_rows: list[dict[str, Any]],
) -> tuple[set[tuple[str, str, str]], dict[str, Any]]:
    groups = [("seed", prior_path), *(("v2", path) for path in v2_paths), ("v3", v3_path)]
    identities: set[tuple[str, str, str]] = set()
    inputs: list[dict[str, Any]] = []
    for category, path in groups:
        rows = read_jsonl(path)
        keys = {source_key(row) for row in rows}
        identities.update(keys)
        inputs.append({
            "category": category, "path": str(path), "sha256": file_sha256(path),
            "records": len(rows), "unique_source_identities": len(keys),
        })
    v4_keys = {source_key(row) for row in v4_rows}
    if len(v4_rows) != 120 or len(v4_keys) != 120:
        raise ValueError("V4 queue must contain 120 unique source identities")
    identities.update(v4_keys)
    inputs.append({
        "category": "v4", "path": str(v4_path), "sha256": file_sha256(v4_path),
        "records": 120,
        "unique_source_identities": 120,
    })
    ordered = [
        {"dataset": item[0], "revision": item[1], "record_id": item[2]}
        for item in sorted(identities)
    ]
    ledger: dict[str, Any] = {
        "schema_version": EXCLUSION_SCHEMA, "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256,
        "budget_clarification_addendum_sha256": BUDGET_CLARIFICATION_ADDENDUM_SHA256,
        "inputs": inputs,
        "excluded_source_identities": ordered,
        "excluded_source_identities_sha256": canonical_sha256(ordered),
        "unique_excluded_source_identities": len(ordered),
        "evaluation_artifacts_read": 0,
    }
    ledger["ledger_sha256"] = canonical_sha256(ledger)
    return identities, ledger


def load_v4_queue(queue_path: Path, manifest_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = load_sealed(manifest_path, "manifest_sha256")
    rows = read_jsonl(queue_path)
    if (
        manifest.get("schema_version") != "ganesh-mini-repair-delta-v4-queue-manifest/v1"
        or manifest.get("contract_id") != V4_CONTRACT_ID
        or manifest.get("plan_sha256") != V4_PLAN_SHA256
        or manifest.get("queue_sha256") != file_sha256(queue_path)
        or manifest.get("assignments") != 120 or len(rows) != 120
        or len({row.get("id") for row in rows}) != 120
    ):
        raise ValueError("V4 queue and manifest are unsealed or inconsistent")
    return rows, manifest


def load_v4_teacher_rows(
    candidate_paths: list[Path], evidence_paths: list[Path], manifest_sha256: str,
) -> dict[str, dict[str, Any]]:
    if len(candidate_paths) != 6 or len(evidence_paths) != 6:
        raise ValueError("V4 carry requires exactly six teacher candidate/evidence batches")
    output: dict[str, dict[str, Any]] = {}
    lanes: set[str] = set()
    for candidate_path, evidence_path in zip(candidate_paths, evidence_paths, strict=True):
        evidence = load_sealed(evidence_path, "evidence_sha256")
        raw_lines = [line for line in candidate_path.read_bytes().splitlines() if line.strip()]
        rows = [json.loads(line) for line in raw_lines]
        ids = [row.get("candidate", {}).get("id") for row in rows]
        lane = evidence.get("lane")
        if (
            evidence.get("schema_version") != "ganesh-mini-repair-delta-v4-teacher-batch/v1"
            or evidence.get("contract_id") != V4_CONTRACT_ID
            or evidence.get("plan_sha256") != V4_PLAN_SHA256
            or evidence.get("queue_manifest_sha256") != manifest_sha256
            or evidence.get("role") != "primary" or evidence.get("failures") != []
            or evidence.get("generated") != 10 or len(rows) != 10
            or evidence.get("requested_ids") != ids
            or evidence.get("candidate_output_sha256") != file_sha256(candidate_path)
            or evidence.get("evaluation_artifacts_read") != 0
            or not isinstance(lane, str) or lane in lanes
        ):
            raise ValueError(f"{candidate_path}: invalid V4 teacher batch")
        lanes.add(lane)
        for index, (row, raw_line) in enumerate(zip(rows, raw_lines, strict=True)):
            identifier = row.get("candidate", {}).get("id")
            if not isinstance(identifier, str) or identifier in output:
                raise ValueError("V4 teacher candidate identities are malformed or duplicated")
            output[identifier] = {
                "row": row,
                "artifact": {
                    "path": str(candidate_path), "file_sha256": file_sha256(candidate_path),
                    "row_index": index, "record_sha256": hashlib.sha256(raw_line).hexdigest(),
                },
                "batch": {
                    "path": str(evidence_path), "file_sha256": file_sha256(evidence_path),
                    "evidence_sha256": evidence["evidence_sha256"],
                },
            }
    if lanes != {"go", "java", "javascript", "typescript", "python", "rust"} or len(output) != 60:
        raise ValueError("V4 teacher evidence does not contain exactly 60 primary rows")
    return output


def build_carries(
    cells: list[dict[str, Any]], v4_primary: dict[str, dict[str, Any]],
    teacher_rows: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    by_cell: dict[str, dict[str, Any]] = {}
    for ordinal, cell in enumerate(cells):
        cell_id = cell["cell_id"]
        if cell_id in REPLACEMENT_CELLS:
            continue
        queue_row = next((row for row in v4_primary.values() if row.get("cell_id") == cell_id), None)
        if queue_row is None:
            raise ValueError(f"{cell_id}: missing V4 primary assignment")
        generated = teacher_rows.get(queue_row["id"])
        if generated is None:
            raise ValueError(f"{cell_id}: missing V4 teacher row")
        teacher_row = generated["row"]
        candidate = teacher_row.get("candidate")
        proof = teacher_row.get("repair_delta_proof")
        if not isinstance(candidate, dict) or not isinstance(proof, dict):
            raise ValueError(f"{cell_id}: malformed V4 teacher row")
        proof_body = dict(proof)
        proof_seal = proof_body.pop("evidence_sha256", None)
        assignment_projection = {
            key: queue_row[key] for key in (
                "id", "cell_id", "lane", "primary_capability",
                "primary_capability_definition", "assigned_cross_cutting_dimension",
                "source_queue_id", "source_affinity_evidence_sha256",
                "source_separation_attestation_sha256",
            )
        }
        if (
            candidate.get("id") != queue_row["id"]
            or candidate.get("lane") != cell["lane"]
            or candidate.get("source") != queue_row.get("source")
            or proof_seal != canonical_sha256(proof_body)
            or proof.get("candidate_id") != candidate["id"]
            or proof.get("teacher_candidate_sha256") != teacher_candidate_sha256(candidate)
            or proof.get("queue_record_sha256") != canonical_sha256(queue_row)
            or not isinstance(proof.get("teacher_run_evidence_sha256"), str)
        ):
            raise ValueError(f"{cell_id}: V4 candidate, proof, and assignment do not bind")
        row: dict[str, Any] = {
            "schema_version": "ganesh-mini-gate2-v5-immutable-carry/v1",
            "disposition": "immutable-v4-teacher-carry", "ordinal": ordinal,
            "v4_candidate_id": candidate["id"], "cell_id": cell_id,
            "lane": cell["lane"], "primary_capability": cell["primary_capability"],
            "assigned_cross_cutting_dimension": cell["assigned_cross_cutting_dimension"],
            "source_identity": identity_dict(candidate),
            "source_record_sha256": candidate["source"]["source_record_sha256"],
            "candidate_sha256": canonical_sha256(candidate),
            "teacher_proof_evidence_sha256": proof_seal,
            "teacher_run_evidence_sha256": proof["teacher_run_evidence_sha256"],
            "v4_queue_record_sha256": canonical_sha256(queue_row),
            "v4_assignment_projection": assignment_projection,
            "v4_assignment_projection_sha256": canonical_sha256(assignment_projection),
            "v4_teacher_artifact": generated["artifact"],
            "v4_teacher_batch_evidence": generated["batch"],
        }
        row["carry_row_sha256"] = canonical_sha256(row)
        rows.append(row)
        by_cell[cell_id] = row
    if len(rows) != 58 or set(by_cell) != {cell["cell_id"] for cell in cells} - set(REPLACEMENT_CELLS):
        raise ValueError("immutable carry manifest must contain exactly the frozen 58 cells")
    return rows, by_cell


def load_accepted_sources(
    source_path: Path, evidence_path: Path, summary_path: Path,
    excluded: set[tuple[str, str, str]],
) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], dict[str, Any]], dict[str, Any]]:
    all_source_rows = read_jsonl(source_path)
    source_rows = [row for row in all_source_rows if row.get("task_type") == "repair"]
    if not source_rows:
        raise ValueError("source queue contains no repair sources")
    sources = {row["id"]: row for row in source_rows}
    if len(sources) != len(source_rows):
        raise ValueError("source queue contains duplicate IDs")
    if len({source_key(row) for row in sources.values()}) != len(sources):
        raise ValueError("source queue contains duplicate lineage identities")
    summary = load_sealed(summary_path, "aggregate_sha256")
    if (
        summary.get("schema_version") != "ganesh-mini-repair-source-ontology-aggregate/v1"
        or summary.get("status") != "coverage-complete"
        or summary.get("combined_evidence_sha256") != file_sha256(evidence_path)
        or summary.get("source_queue_sha256") != file_sha256(source_path)
        or summary.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("ontology aggregate is unsealed or inconsistent")
    accepted: dict[tuple[str, str], dict[str, Any]] = {}
    seen_source_ids: set[str] = set()
    evidence_records = 0
    with evidence_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            evidence_records += 1
            row = json.loads(line)
            body = dict(row); claimed = body.pop("evidence_sha256", None)
            source = sources.get(row.get("source_queue_id"))
            if (
                claimed != canonical_sha256(body) or source is None
                or row.get("evaluation_artifacts_read") != 0
                or row.get("source_identity") != identity_dict(source)
                or row.get("source_record_sha256") != source.get("source", {}).get("source_record_sha256")
                or row.get("lane") != source.get("lane")
                or row.get("source_queue_id") in seen_source_ids
                or not isinstance(row.get("verdicts"), list)
            ):
                raise ValueError("ontology evidence row is unsealed or source-unbound")
            seen_source_ids.add(row["source_queue_id"])
            if source_key(source) in excluded:
                continue
            for verdict in row["verdicts"]:
                if not isinstance(verdict, dict) or verdict.get("primary_capability") not in CAPABILITIES:
                    raise ValueError("ontology verdict is malformed")
                if verdict.get("decision") == "accept":
                    if any(verdict.get(field) is not True for field in AFFINITY_FIELDS):
                        raise ValueError("accepted ontology verdict does not pass every frozen boolean")
                    cell_id = f"{verdict['primary_capability']}/{source['lane']}/repair"
                    accepted[(cell_id, source["id"])] = {
                        "evidence_sha256": claimed,
                        "separation_attestation_sha256": row["separation_attestation_sha256"],
                        "capability_operation": verdict["capability_operation"],
                        "defect_affordance": verdict["defect_affordance"],
                    }
    if evidence_records != summary.get("unique_sources") or len(seen_source_ids) != evidence_records:
        raise ValueError("ontology evidence record count differs from its sealed summary")
    return sources, accepted, summary


def rank_key(seed: str, cell: dict[str, Any], source: dict[str, Any]) -> str:
    projection = {
        "seed": seed, "cell_id": cell["cell_id"], "lane": source["lane"],
        "dataset": source["source"]["dataset"], "revision": source["source"]["revision"],
        "record_id": source["source"]["record_id"],
        "source_record_sha256": source["source"]["source_record_sha256"],
        "license": source["source"].get("license"),
    }
    if not isinstance(projection["license"], str) or not projection["license"]:
        raise ValueError("selected source lacks a frozen eligible license identity")
    return canonical_sha256(projection)


def deterministic_match(
    slots: list[tuple[str, dict[str, Any]]], sources: dict[str, dict[str, Any]],
    accepted: dict[tuple[str, str], dict[str, Any]], used: set[str],
    seeds: str | dict[str, str],
) -> dict[tuple[str, str], str]:
    edges: dict[tuple[str, str], list[str]] = {}
    for role, cell in slots:
        key = (role, cell["cell_id"])
        seed = seeds[role] if isinstance(seeds, dict) else seeds
        edges[key] = sorted(
            (source_id for source_id, source in sources.items()
             if source_id not in used and source.get("lane") == cell["lane"]
             and (cell["cell_id"], source_id) in accepted),
            key=lambda source_id: (rank_key(seed, cell, sources[source_id]), source_id),
        )
        if not edges[key]:
            raise ValueError(f"{cell['cell_id']}: no fresh accepted source")
    owner: dict[str, tuple[str, str]] = {}
    assignment: dict[tuple[str, str], str] = {}

    def augment(slot: tuple[str, str], visited: set[str]) -> bool:
        for source_id in edges[slot]:
            if source_id in visited:
                continue
            visited.add(source_id)
            previous = owner.get(source_id)
            if previous is None or augment(previous, visited):
                owner[source_id] = slot
                assignment[slot] = source_id
                return True
        return False

    for slot in [key for key in edges]:
        if not augment(slot, set()):
            raise ValueError("fresh source pool cannot satisfy globally unique V5 slots")
    return assignment


def selection_row(
    role: str, ordinal: int, cell: dict[str, Any], source: dict[str, Any],
    affinity: dict[str, Any], seed: str,
) -> dict[str, Any]:
    identifier = f"cap-v5-{cell['primary_capability']}-{cell['lane']}-repair-{role}"
    projection = {
        "seed": seed, "cell_id": cell["cell_id"], "lane": source["lane"],
        "dataset": source["source"]["dataset"], "revision": source["source"]["revision"],
        "record_id": source["source"]["record_id"],
        "source_record_sha256": source["source"]["source_record_sha256"],
        "license": source["source"].get("license"),
    }
    row: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate2-v5-source-selection/v1",
        "role": role, "generation_eligible": role == "primary", "ordinal": ordinal,
        "candidate_id": identifier, "cell_id": cell["cell_id"], "lane": cell["lane"],
        "primary_capability": cell["primary_capability"],
        "primary_capability_definition": CAPABILITIES[cell["primary_capability"]],
        "assigned_cross_cutting_dimension": cell["assigned_cross_cutting_dimension"],
        "source_queue_id": source["id"], "source_identity": identity_dict(source),
        "source_record_sha256": source["source"]["source_record_sha256"],
        "source_queue_record_sha256": canonical_sha256(source),
        "source_queue_record": source,
        "ontology_evidence_sha256": affinity["evidence_sha256"],
        "source_separation_attestation_sha256": affinity["separation_attestation_sha256"],
        "source_affinity_card": {
            "capability_operation": affinity["capability_operation"],
            "defect_affordance": affinity["defect_affordance"],
        },
        "selection_projection": projection,
        "selection_key_sha256": canonical_sha256(projection),
    }
    row["selection_row_sha256"] = canonical_sha256(row)
    return row


def build(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    if file_sha256(args.plan) != PLAN_SHA256:
        raise ValueError("V5 plan hash differs from the frozen contract")
    if file_sha256(args.source_feasibility_addendum) != SOURCE_FEASIBILITY_ADDENDUM_SHA256:
        raise ValueError("V5 source-feasibility addendum differs from the frozen amendment")
    if file_sha256(args.budget_clarification_addendum) != BUDGET_CLARIFICATION_ADDENDUM_SHA256:
        raise ValueError("V5 budget clarification addendum differs from the frozen amendment")
    cells = repair_cells()
    if (
        len(cells) != 60
        or any([cell["cell_id"] for cell in cells].count(item) != 1 for item in REPLACEMENT_CELLS)
    ):
        raise ValueError("frozen repair-cell matrix is invalid")
    v4_rows, v4_manifest = load_v4_queue(args.v4_queue, args.v4_queue_manifest)
    v4_primary = {row["id"]: row for row in v4_rows if row.get("role") == "primary"}
    if len(v4_primary) != 60:
        raise ValueError("V4 queue lacks its exact 60 primary assignments")
    teacher_rows = load_v4_teacher_rows(
        args.v4_teacher_candidates, args.v4_teacher_evidence, v4_manifest["manifest_sha256"],
    )
    if set(teacher_rows) != set(v4_primary):
        raise ValueError("V4 teacher rows do not exactly match the 60 primary assignments")
    carries, carry_by_cell = build_carries(cells, v4_primary, teacher_rows)
    excluded, ledger = collect_exclusions(
        args.prior_corpus, args.v2_artifact, args.v3_queue, args.v4_queue, v4_rows,
    )
    sources, accepted, ontology_summary = load_accepted_sources(
        args.source_queue, args.ontology_evidence, args.ontology_summary, excluded,
    )
    cell_by_id = {cell["cell_id"]: cell for cell in cells}
    primary_slots = [("primary", cell_by_id[cell_id]) for cell_id in REPLACEMENT_CELLS]
    reserve_slots = [
        ("reserve", cell) for cell in cells if cell["cell_id"] not in UNRESERVED_CELLS
    ]
    assignment = deterministic_match(
        [*primary_slots, *reserve_slots], sources, accepted, set(),
        {"primary": PRIMARY_SEED, "reserve": RESERVE_SEED},
    )
    selected_rows: list[dict[str, Any]] = []
    primary_by_cell: dict[str, dict[str, Any]] = {}
    reserve_by_cell: dict[str, dict[str, Any]] = {}
    for ordinal, cell_id in enumerate(REPLACEMENT_CELLS):
        cell = cell_by_id[cell_id]; source_id = assignment[("primary", cell_id)]
        row = selection_row("primary", ordinal, cell, sources[source_id], accepted[(cell_id, source_id)], PRIMARY_SEED)
        selected_rows.append(row); primary_by_cell[cell_id] = row
    for ordinal, cell in enumerate(cells):
        if cell["cell_id"] in UNRESERVED_CELLS:
            continue
        source_id = assignment[("reserve", cell["cell_id"])]
        row = selection_row("reserve", ordinal, cell, sources[source_id], accepted[(cell["cell_id"], source_id)], RESERVE_SEED)
        selected_rows.append(row); reserve_by_cell[cell["cell_id"]] = row
    identities = [tuple(row["source_identity"].values()) for row in selected_rows]
    if len(selected_rows) != 61 or len(set(identities)) != 61 or any(identity in excluded for identity in identities):
        raise ValueError("V5 primary/reserve selections are reused, excluded, or incomplete")

    carry_manifest: dict[str, Any] = {
        "schema_version": CARRY_SCHEMA, "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256,
        "source_feasibility_addendum_sha256": SOURCE_FEASIBILITY_ADDENDUM_SHA256,
        "budget_clarification_addendum_sha256": BUDGET_CLARIFICATION_ADDENDUM_SHA256,
        "v4_queue_manifest_sha256": v4_manifest["manifest_sha256"],
        "rows": carries, "rows_sha256": canonical_sha256(carries), "records": 58,
        "excluded_replacement_cells": list(REPLACEMENT_CELLS), "evaluation_artifacts_read": 0,
    }
    carry_manifest["manifest_sha256"] = canonical_sha256(carry_manifest)
    source_manifest: dict[str, Any] = {
        "schema_version": SOURCE_SCHEMA, "contract_id": CONTRACT_ID, "plan_sha256": PLAN_SHA256,
        "source_feasibility_addendum_sha256": SOURCE_FEASIBILITY_ADDENDUM_SHA256,
        "budget_clarification_addendum_sha256": BUDGET_CLARIFICATION_ADDENDUM_SHA256,
        "primary_seed": PRIMARY_SEED, "reserve_seed": RESERVE_SEED,
        "exclusion_ledger_sha256": ledger["ledger_sha256"],
        "source_queue": {"path": str(args.source_queue), "sha256": file_sha256(args.source_queue)},
        "ontology": {
            "evidence_path": str(args.ontology_evidence), "evidence_sha256": file_sha256(args.ontology_evidence),
            "summary_path": str(args.ontology_summary), "aggregate_sha256": ontology_summary["aggregate_sha256"],
        },
        "selections": selected_rows, "selections_sha256": canonical_sha256(selected_rows),
        "fresh_primary_sources": 2, "prebound_reserve_sources": 59,
        "unreserved_cells": list(UNRESERVED_CELLS),
        "unique_selected_source_identities": 61, "evaluation_artifacts_read": 0,
    }
    source_manifest["manifest_sha256"] = canonical_sha256(source_manifest)
    cohort_rows: list[dict[str, Any]] = []
    for ordinal, cell in enumerate(cells):
        cell_id = cell["cell_id"]
        common = {
            "ordinal": ordinal, "cell_id": cell_id, "lane": cell["lane"],
            "primary_capability": cell["primary_capability"],
            "assigned_cross_cutting_dimension": cell["assigned_cross_cutting_dimension"],
        }
        if cell_id in carry_by_cell:
            carry = carry_by_cell[cell_id]
            row = {**common, "mode": "immutable-v4-teacher-carry",
                   "candidate_id": carry["v4_candidate_id"], "carry_row_sha256": carry["carry_row_sha256"]}
        else:
            source = primary_by_cell[cell_id]
            row = {**common, "mode": "fresh-v5-teacher-primary",
                   "candidate_id": source["candidate_id"], "source_selection_row_sha256": source["selection_row_sha256"]}
        row["cohort_row_sha256"] = canonical_sha256(row)
        cohort_rows.append(row)
    runtime_sha = file_sha256(args.runtime_config); preflight_sha = file_sha256(args.preflight_config)
    cohort_manifest: dict[str, Any] = {
        "schema_version": COHORT_SCHEMA, "contract_id": CONTRACT_ID, "plan_sha256": PLAN_SHA256,
        "source_feasibility_addendum_sha256": SOURCE_FEASIBILITY_ADDENDUM_SHA256,
        "budget_clarification_addendum_sha256": BUDGET_CLARIFICATION_ADDENDUM_SHA256,
        "runtime_config_sha256": runtime_sha, "preflight_config_sha256": preflight_sha,
        "tool_identity": {
            "builder_path": str(Path(__file__).relative_to(ROOT)),
            "builder_sha256": file_sha256(Path(__file__)), "python": platform.python_version(),
        },
        "carry_manifest_sha256": carry_manifest["manifest_sha256"],
        "source_manifest_sha256": source_manifest["manifest_sha256"],
        "exclusion_ledger_sha256": ledger["ledger_sha256"],
        "rows": cohort_rows, "ordered_cohort_sha256": canonical_sha256(cohort_rows),
        "records": 60, "immutable_carries": 58, "fresh_teacher_primaries": 2,
        "prebound_reserves": 59, "unreserved_cells": list(UNRESERVED_CELLS),
        "absolute_terminal_candidate_budget": 65,
        "absolute_new_teacher_generation_budget": 7,
        "maximum_generated_reserves": 5, "evaluation_artifacts_read": 0,
    }
    cohort_manifest["manifest_sha256"] = canonical_sha256(cohort_manifest)
    return ledger, carry_manifest, source_manifest, cohort_manifest


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--source-feasibility-addendum", type=Path, required=True)
    parser.add_argument("--budget-clarification-addendum", type=Path, required=True)
    parser.add_argument("--v4-queue", type=Path, required=True)
    parser.add_argument("--v4-queue-manifest", type=Path, required=True)
    parser.add_argument("--v4-teacher-candidates", type=Path, action="append", required=True)
    parser.add_argument("--v4-teacher-evidence", type=Path, action="append", required=True)
    parser.add_argument("--source-queue", type=Path, required=True)
    parser.add_argument("--ontology-evidence", type=Path, required=True)
    parser.add_argument("--ontology-summary", type=Path, required=True)
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--v2-artifact", type=Path, action="append", required=True)
    parser.add_argument("--v3-queue", type=Path, required=True)
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--preflight-config", type=Path, required=True)
    parser.add_argument("--exclusion-ledger-output", type=Path, required=True)
    parser.add_argument("--carry-manifest-output", type=Path, required=True)
    parser.add_argument("--source-manifest-output", type=Path, required=True)
    parser.add_argument("--cohort-manifest-output", type=Path, required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    ledger, carries, sources, cohort = build(args)
    write_json(args.exclusion_ledger_output, ledger)
    write_json(args.carry_manifest_output, carries)
    write_json(args.source_manifest_output, sources)
    write_json(args.cohort_manifest_output, cohort)
    print(json.dumps({
        "status": "sealed", "carries": carries["records"],
        "fresh_primaries": sources["fresh_primary_sources"],
        "reserves": sources["prebound_reserve_sources"],
        "cohort_manifest_sha256": cohort["manifest_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
