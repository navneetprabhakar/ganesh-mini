#!/usr/bin/env python3
"""Build the immutable V6 teacher/semantic carry and ordered cohort manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.admit_repair_delta import teacher_candidate_sha256
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_repair_delta_evidence import _semantic_evidence


V6_CONTRACT_ID = "capability-stratified-v6-canonical-test-replay/v1"
V6_PLAN_SHA256 = "4fe6a1374c01a0a682bf256c91a141b36b26680bdb5279049070f4f143418ec1"
V5_CONTRACT_ID = "capability-stratified-v5-interface-replay/v1"
V5_PLAN_SHA256 = "132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b"
V5_EXECUTION_MANIFEST_SEAL = "138c0dff1263278cae17bdab4c497f00fabec336f5ffded26daf0a30fae51e9d"
V5_SEMANTIC_EQUIVALENCE_SEAL = "e3e868f32ac86821e946b619f3e140c62d397c80f2af259395ce203ebc721e30"
V5_V1_SEMANTIC_CARRY_SEAL = "7139e4686f5cf772ecf9db2e0e30653564a612e9979b2aa90f8f92b1d5faeafb"
V5_V2_SEMANTIC_CARRY_SEAL = "f8a158319e08b822d29b3074061e06e04a45b1a1ba453fadefdec8ba96845ac8"
V5_TERMINAL_INVENTORY_SEAL = "6e1512cf01b00272120e041b74487bfc66105627d01db13e9f9a1b1bbe99796d"
V5_QUALIFICATION_SEAL = "f169894cc32557388ec7812180d1524502af1ae35c310e8f31f3c4177e5452e5"

CARRY_SCHEMA = "ganesh-mini-gate2-v6-immutable-carry-manifest/v1"
COHORT_SCHEMA = "ganesh-mini-gate2-v6-ordered-cohort-manifest/v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[bytes]]:
    raw = [line for line in path.read_bytes().splitlines() if line.strip()]
    return [json.loads(line) for line in raw], raw


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    body = dict(value)
    claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def _semantic_without_terminal_binding(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    prior = result.pop("pre_test_semantic_evidence_sha256", None)
    if prior is not None and prior != result.get("evidence_sha256"):
        raise ValueError("terminal semantic evidence has an invalid pre-test binding")
    body = dict(result)
    claimed = body.pop("evidence_sha256", None)
    if claimed != canonical_sha256(body):
        raise ValueError("semantic evidence is not sealed")
    return result


def _semantic_sources(
    equivalence: dict[str, Any], v1_carry: dict[str, Any], v2_carry: dict[str, Any],
) -> dict[str, tuple[str, dict[str, Any]]]:
    sources: dict[str, tuple[str, dict[str, Any]]] = {}
    groups = (
        ("v4-equivalence", equivalence.get("equivalences", []), "equivalence_row_sha256"),
        ("v5-v1-interruption-carry", v1_carry.get("rows", []), "carry_row_sha256"),
        ("v5-v2-interruption-carry", v2_carry.get("rows", []), "carry_row_sha256"),
    )
    expected = {"v4-equivalence": 37, "v5-v1-interruption-carry": 3, "v5-v2-interruption-carry": 2}
    for kind, rows, row_seal in groups:
        if not isinstance(rows, list) or len(rows) != expected[kind]:
            raise ValueError(f"{kind}: unexpected semantic row count")
        for row in rows:
            body = dict(row)
            claimed = body.pop(row_seal, None)
            identifier = row.get("candidate_id")
            if (
                claimed != canonical_sha256(body)
                or not isinstance(identifier, str)
                or identifier in sources
                or not isinstance(row.get("semantic_evidence"), dict)
            ):
                raise ValueError(f"{kind}: unsealed, duplicate, or malformed semantic row")
            sources[identifier] = (kind, row)
    return sources


def build(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    if file_sha256(args.plan) != V6_PLAN_SHA256:
        raise ValueError("V6 plan hash differs from the frozen canonical plan")
    execution = load_sealed(args.v5_execution_manifest, "manifest_sha256")
    equivalence = load_sealed(args.v5_semantic_equivalence, "manifest_sha256")
    v1_carry = load_sealed(args.v5_v1_semantic_carry, "manifest_sha256")
    v2_carry = load_sealed(args.v5_v2_semantic_carry, "manifest_sha256")
    inventory = load_sealed(args.v5_terminal_inventory, "report_sha256")
    qualification = load_sealed(args.v5_qualification, "report_sha256")
    if (
        execution.get("manifest_sha256") != V5_EXECUTION_MANIFEST_SEAL
        or execution.get("contract_id") != V5_CONTRACT_ID
        or execution.get("plan_sha256") != V5_PLAN_SHA256
        or execution.get("records") != 60
        or equivalence.get("manifest_sha256") != V5_SEMANTIC_EQUIVALENCE_SEAL
        or v1_carry.get("manifest_sha256") != V5_V1_SEMANTIC_CARRY_SEAL
        or v2_carry.get("manifest_sha256") != V5_V2_SEMANTIC_CARRY_SEAL
        or inventory.get("report_sha256") != V5_TERMINAL_INVENTORY_SEAL
        or inventory.get("generated") != 60
        or inventory.get("terminal_rejected") != 31
        or inventory.get("ready") != 29
        or inventory.get("unresolved") != 0
        or qualification.get("report_sha256") != V5_QUALIFICATION_SEAL
        or qualification.get("status") != "qualification-failed"
        or qualification.get("contract", {}).get("identifier") != V5_CONTRACT_ID
    ):
        raise ValueError("V5 controlling inputs do not match the terminal sealed run")

    candidates, candidate_raw = read_jsonl(args.v5_candidates)
    assignments, assignment_raw = read_jsonl(args.v5_assignments)
    ordered_ids = execution.get("ordered_candidate_ids")
    if (
        not isinstance(ordered_ids, list)
        or len(ordered_ids) != 60
        or len(set(ordered_ids)) != 60
        or file_sha256(args.v5_candidates) != execution.get("candidate_output", {}).get("sha256")
        or file_sha256(args.v5_assignments) != execution.get("assignment_output", {}).get("sha256")
        or canonical_sha256(candidates) != execution.get("generated_rows_sha256")
        or canonical_sha256(assignments) != execution.get("assignments_sha256")
        or [row.get("candidate", {}).get("id") for row in candidates] != ordered_ids
        or [row.get("id") for row in assignments] != ordered_ids
    ):
        raise ValueError("V5 execution rows, hashes, or canonical order differ")

    terminal_path = Path(inventory.get("terminal_artifacts", {}).get("path", ""))
    terminal_rows, terminal_raw = read_jsonl(terminal_path)
    if (
        terminal_path.resolve() != args.v5_terminal_artifacts.resolve()
        or file_sha256(terminal_path) != inventory.get("terminal_artifacts", {}).get("sha256")
        or len(terminal_rows) != 60
        or [row.get("candidate_id") for row in terminal_rows] != ordered_ids
    ):
        raise ValueError("V5 terminal artifacts differ from their terminal inventory")

    semantic_sources = _semantic_sources(equivalence, v1_carry, v2_carry)
    carry_rows: list[dict[str, Any]] = []
    cohort_rows: list[dict[str, Any]] = []
    source_counts = {"v4-equivalence": 0, "v5-v1-interruption-carry": 0,
                     "v5-v2-interruption-carry": 0, "v5-v3-fresh-review": 0}
    for ordinal, (generated, assignment, terminal) in enumerate(
        zip(candidates, assignments, terminal_rows, strict=True)
    ):
        candidate = generated.get("candidate")
        proof = generated.get("repair_delta_proof")
        identifier = ordered_ids[ordinal]
        payload = terminal.get("envelope", terminal)
        terminal_semantic = payload.get("evidence", {}).get("semantic_review")
        proof_body = dict(proof) if isinstance(proof, dict) else {}
        proof_claimed = proof_body.pop("evidence_sha256", None)
        if (
            not isinstance(candidate, dict)
            or not isinstance(proof, dict)
            or not isinstance(terminal_semantic, dict)
            or candidate.get("id") != identifier
            or assignment.get("id") != identifier
            or (payload.get("assignment") is not None and payload.get("assignment") != assignment)
            or terminal.get("cell_id") not in (None, assignment.get("cell_id"))
            or proof_claimed != canonical_sha256(proof_body)
            or proof.get("candidate_id") != identifier
            or proof.get("teacher_candidate_sha256") != teacher_candidate_sha256(candidate)
        ):
            raise ValueError(f"{identifier}: teacher, proof, assignment, or terminal binding differs")
        source = semantic_sources.get(identifier)
        if source is None:
            source_kind = "v5-v3-fresh-review"
            stage_path = args.v5_v3_codex_runs / f"{identifier}.semantic_review.json"
            stage = load_sealed(stage_path, "artifact_sha256")
            if (
                stage.get("candidate_id") != identifier
                or not isinstance(stage.get("response"), dict)
            ):
                raise ValueError(f"{identifier}: V5 V3 semantic stage is missing or unbound")
            evidence = _semantic_evidence(
                candidate, assignment, dict(stage["response"]),
                stage.get("run", {}).get("run_evidence_sha256"),
            )
            semantic_lineage = {
                "kind": source_kind, "path": str(stage_path),
                "file_sha256": file_sha256(stage_path),
                "artifact_sha256": stage["artifact_sha256"],
            }
        else:
            source_kind, source_row = source
            evidence = source_row["semantic_evidence"]
            semantic_lineage = {
                "kind": source_kind,
                "source_row_sha256": source_row.get("equivalence_row_sha256")
                or source_row.get("carry_row_sha256"),
            }
        terminal_prior = terminal_semantic.get("pre_test_semantic_evidence_sha256")
        if (
            evidence.get("candidate_sha256") != canonical_sha256(candidate)
            or (terminal_prior is not None and terminal_prior != evidence.get("evidence_sha256"))
            or (terminal_prior is None and terminal_semantic != evidence)
        ):
            raise ValueError(f"{identifier}: carried semantic evidence changed")
        source_counts[source_kind] += 1
        carry_row: dict[str, Any] = {
            "schema_version": "ganesh-mini-gate2-v6-immutable-carry/v1",
            "contract_id": V6_CONTRACT_ID,
            "ordinal": ordinal,
            "candidate_id": identifier,
            "cell_id": assignment.get("cell_id"),
            "lane": assignment.get("lane"),
            "primary_capability": assignment.get("primary_capability"),
            "assigned_cross_cutting_dimension": assignment.get("assigned_cross_cutting_dimension"),
            "v5_candidate_row_sha256": hashlib.sha256(candidate_raw[ordinal]).hexdigest(),
            "v5_assignment_row_sha256": hashlib.sha256(assignment_raw[ordinal]).hexdigest(),
            "v5_terminal_row_sha256": hashlib.sha256(terminal_raw[ordinal]).hexdigest(),
            "candidate_sha256": canonical_sha256(candidate),
            "teacher_proof_evidence_sha256": proof_claimed,
            "semantic_evidence": evidence,
            "semantic_evidence_sha256": canonical_sha256(evidence),
            "semantic_lineage": semantic_lineage,
            "teacher_generation_calls": 0,
            "semantic_review_calls": 0,
            "v5_test_or_disposition_carried": False,
            "evaluation_artifacts_read": 0,
        }
        carry_row["carry_row_sha256"] = canonical_sha256(carry_row)
        carry_rows.append(carry_row)
        cohort_row: dict[str, Any] = {
            "schema_version": "ganesh-mini-gate2-v6-ordered-cohort-row/v1",
            "contract_id": V6_CONTRACT_ID,
            "ordinal": ordinal,
            "candidate_id": identifier,
            "cell_id": assignment.get("cell_id"),
            "lane": assignment.get("lane"),
            "primary_capability": assignment.get("primary_capability"),
            "primary_capability_definition": assignment.get("primary_capability_definition"),
            "assigned_cross_cutting_dimension": assignment.get("assigned_cross_cutting_dimension"),
            "mode": "immutable-v5-teacher-semantic-carry",
            "carry_row_sha256": carry_row["carry_row_sha256"],
        }
        cohort_row["cohort_row_sha256"] = canonical_sha256(cohort_row)
        cohort_rows.append(cohort_row)
    if source_counts != {
        "v4-equivalence": 37, "v5-v1-interruption-carry": 3,
        "v5-v2-interruption-carry": 2, "v5-v3-fresh-review": 18,
    }:
        raise ValueError("V5 semantic lineage does not cover the exact 37+3+2+18 partition")

    carry_manifest: dict[str, Any] = {
        "schema_version": CARRY_SCHEMA,
        "status": "sealed",
        "contract_id": V6_CONTRACT_ID,
        "plan_sha256": V6_PLAN_SHA256,
        "source_contract_id": V5_CONTRACT_ID,
        "v5_execution_manifest_sha256": V5_EXECUTION_MANIFEST_SEAL,
        "v5_semantic_equivalence_manifest_sha256": V5_SEMANTIC_EQUIVALENCE_SEAL,
        "v5_v1_semantic_carry_manifest_sha256": V5_V1_SEMANTIC_CARRY_SEAL,
        "v5_v2_semantic_carry_manifest_sha256": V5_V2_SEMANTIC_CARRY_SEAL,
        "v5_terminal_inventory_report_sha256": V5_TERMINAL_INVENTORY_SEAL,
        "v5_qualification_report_sha256": V5_QUALIFICATION_SEAL,
        "v5_candidates_file_sha256": file_sha256(args.v5_candidates),
        "v5_assignments_file_sha256": file_sha256(args.v5_assignments),
        "v5_terminal_artifacts_file_sha256": file_sha256(terminal_path),
        "records": 60,
        "rows": carry_rows,
        "rows_sha256": canonical_sha256(carry_rows),
        "semantic_lineage_counts": source_counts,
        "teacher_generation_calls": 0,
        "semantic_review_calls": 0,
        "test_author_carries": 0,
        "executable_result_carries": 0,
        "admission_or_disposition_carries": 0,
        "evaluation_artifacts_read": 0,
    }
    carry_manifest["manifest_sha256"] = canonical_sha256(carry_manifest)
    cohort_manifest: dict[str, Any] = {
        "schema_version": COHORT_SCHEMA,
        "status": "sealed-ready-for-implementation-readiness",
        "contract_id": V6_CONTRACT_ID,
        "plan_sha256": V6_PLAN_SHA256,
        "carry_manifest_sha256": carry_manifest["manifest_sha256"],
        "records": 60,
        "rows": cohort_rows,
        "rows_sha256": canonical_sha256(cohort_rows),
        "ordered_candidate_ids": ordered_ids,
        "ordered_candidate_ids_sha256": canonical_sha256(ordered_ids),
        "budgets": {
            "teacher_generation_calls": 0,
            "semantic_review_calls": 0,
            "fresh_test_author_calls": 60,
            "maximum_structural_reauthor_calls": 6,
            "maximum_fresh_blind_delta_audit_calls": 60,
            "delta_audit_correction_calls": 0,
            "candidate_reserves": 0,
        },
        "evaluation_artifacts_read": 0,
    }
    cohort_manifest["manifest_sha256"] = canonical_sha256(cohort_manifest)
    return carry_manifest, cohort_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "plan", "v5-execution-manifest", "v5-candidates", "v5-assignments",
        "v5-semantic-equivalence", "v5-v1-semantic-carry", "v5-v2-semantic-carry",
        "v5-terminal-inventory", "v5-terminal-artifacts", "v5-qualification",
        "v5-v3-codex-runs", "carry-output", "cohort-output",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args(argv)
    carry, cohort = build(args)
    for path, value in ((args.carry_output, carry), (args.cohort_output, cohort)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "sealed", "records": 60,
                      "carry_manifest_sha256": carry["manifest_sha256"],
                      "cohort_manifest_sha256": cohort["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
