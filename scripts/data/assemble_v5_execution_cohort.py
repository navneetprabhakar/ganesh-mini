#!/usr/bin/env python3
"""Assemble the exact ordered V5 58-carry + 2-fresh execution cohort."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_repair_delta import teacher_candidate_sha256  # noqa: E402
from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.data.repair_delta_v5_contract import (  # noqa: E402
    BUDGET_ADDENDUM_SHA256, CONTRACT_ID, PLAN_SHA256, load_v5_contract,
)


ASSIGNMENT_SCHEMA = "ganesh-mini-repair-delta-v5-assignment/v1"
ASSEMBLY_SCHEMA = "ganesh-mini-gate2-v5-execution-cohort-manifest/v1"
READINESS_SCHEMA = "ganesh-mini-gate2-v5-composite-readiness/v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[bytes]]:
    raw = [line for line in path.read_bytes().splitlines() if line.strip()]
    return [json.loads(line) for line in raw], raw


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    body = dict(value); claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def load_carried(carry: dict[str, Any]) -> dict[str, Any]:
    binding = carry.get("v4_teacher_artifact")
    if not isinstance(binding, dict):
        raise ValueError("V5 carry lacks its immutable teacher artifact binding")
    path = Path(binding.get("path", ""))
    rows, raw = read_jsonl(path)
    index = binding.get("row_index")
    if (
        file_sha256(path) != binding.get("file_sha256")
        or not isinstance(index, int) or not 0 <= index < len(rows)
        or hashlib.sha256(raw[index]).hexdigest() != binding.get("record_sha256")
    ):
        raise ValueError("immutable V4 teacher artifact differs from its V5 carry binding")
    generated = rows[index]
    candidate = generated.get("candidate")
    proof = generated.get("repair_delta_proof")
    if (
        not isinstance(candidate, dict) or not isinstance(proof, dict)
        or candidate.get("id") != carry.get("v4_candidate_id")
        or canonical_sha256(candidate) != carry.get("candidate_sha256")
        or proof.get("evidence_sha256") != carry.get("teacher_proof_evidence_sha256")
        or teacher_candidate_sha256(candidate) != proof.get("teacher_candidate_sha256")
    ):
        raise ValueError("carried V4 teacher row differs from its immutable V5 hashes")
    return generated


def assignment_for(
    cohort_row: dict[str, Any], candidate: dict[str, Any], binding: dict[str, Any],
) -> dict[str, Any]:
    definition = binding.get("primary_capability_definition")
    if definition is None and cohort_row["mode"] == "immutable-v4-teacher-carry":
        definition = binding.get("v4_assignment_projection", {}).get(
            "primary_capability_definition"
        )
    if not isinstance(definition, str) or not definition:
        raise ValueError("V5 assignment lacks its frozen primary-capability definition")
    value: dict[str, Any] = {
        "schema_version": ASSIGNMENT_SCHEMA,
        "contract_id": CONTRACT_ID,
        "id": cohort_row["candidate_id"],
        "cell_id": cohort_row["cell_id"],
        "lane": cohort_row["lane"],
        "primary_capability": cohort_row["primary_capability"],
        "primary_capability_definition": definition,
        "assigned_cross_cutting_dimension": cohort_row["assigned_cross_cutting_dimension"],
        "cohort": "first_pass", "role": "primary", "generation_eligible": True,
        "mode": cohort_row["mode"], "source": candidate["source"],
    }
    if cohort_row["mode"] == "immutable-v4-teacher-carry":
        value["carry_row_sha256"] = binding["carry_row_sha256"]
        value["v4_queue_record_sha256"] = binding["v4_queue_record_sha256"]
    else:
        value["source_selection_row_sha256"] = binding["selection_row_sha256"]
        value["source_queue_id"] = binding["source_queue_id"]
        value["source_affinity_card"] = binding["source_affinity_card"]
        value["source_separation_attestation_sha256"] = binding[
            "source_separation_attestation_sha256"
        ]
    value["assignment_sha256"] = canonical_sha256(value)
    return value


def build(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    contract = load_v5_contract(
        plan_path=args.plan, source_addendum_path=args.source_addendum,
        budget_addendum_path=args.budget_addendum, exclusion_path=args.exclusion_ledger,
        carry_path=args.carry_manifest, source_path=args.source_manifest,
        cohort_path=args.cohort_manifest,
    )
    carry_manifest = load_sealed(args.carry_manifest, "manifest_sha256")
    source_manifest = load_sealed(args.source_manifest, "manifest_sha256")
    cohort_manifest = load_sealed(args.cohort_manifest, "manifest_sha256")
    readiness = load_sealed(args.composite_readiness, "report_sha256")
    if (
        readiness.get("schema_version") != READINESS_SCHEMA
        or readiness.get("status") != "passed"
        or readiness.get("contract_id") != CONTRACT_ID
        or readiness.get("plan_sha256") != PLAN_SHA256
        or readiness.get("bindings", {}).get("cohort_manifest_sha256")
        != cohort_manifest["manifest_sha256"]
        or readiness.get("bindings", {}).get("source_manifest_sha256")
        != source_manifest["manifest_sha256"]
        or readiness.get("bindings", {}).get("carry_manifest_sha256")
        != carry_manifest["manifest_sha256"]
        or readiness.get("bindings", {}).get("budget_clarification_addendum_sha256")
        != BUDGET_ADDENDUM_SHA256
    ):
        raise ValueError("V5 composite readiness is not a passing seal for this cohort")

    fresh_rows, _ = read_jsonl(args.fresh_candidates)
    fresh_evidence = load_sealed(args.fresh_evidence, "evidence_sha256")
    if (
        fresh_evidence.get("contract_id") != CONTRACT_ID
        or fresh_evidence.get("plan_sha256") != PLAN_SHA256
        or fresh_evidence.get("budget_clarification_addendum_sha256") != BUDGET_ADDENDUM_SHA256
        or fresh_evidence.get("source_manifest_sha256") != source_manifest["manifest_sha256"]
        or fresh_evidence.get("cohort_manifest_sha256") != cohort_manifest["manifest_sha256"]
        or fresh_evidence.get("composite_readiness_report_sha256") != readiness["report_sha256"]
        or fresh_evidence.get("generated") != 2 or fresh_evidence.get("failures") != []
        or fresh_evidence.get("candidate_output_sha256") != file_sha256(args.fresh_candidates)
        or fresh_evidence.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("fresh V5 teacher evidence is incomplete or cohort-unbound")
    fresh_by_id = {row.get("candidate", {}).get("id"): row for row in fresh_rows}
    if len(fresh_rows) != 2 or len(fresh_by_id) != 2:
        raise ValueError("V5 fresh teacher output must contain exactly two unique candidates")

    carry_by_hash = {row["carry_row_sha256"]: row for row in carry_manifest["rows"]}
    primary_sources = {
        row["selection_row_sha256"]: row for row in source_manifest["selections"]
        if row.get("role") == "primary"
    }
    generated_rows: list[dict[str, Any]] = []
    assignments: list[dict[str, Any]] = []
    for cohort_row in cohort_manifest["rows"]:
        if cohort_row["mode"] == "immutable-v4-teacher-carry":
            binding = carry_by_hash.get(cohort_row.get("carry_row_sha256"))
            if binding is None:
                raise ValueError("V5 cohort references an unknown immutable carry")
            generated = load_carried(binding)
        else:
            binding = primary_sources.get(cohort_row.get("source_selection_row_sha256"))
            generated = fresh_by_id.get(cohort_row["candidate_id"])
            if binding is None or generated is None:
                raise ValueError("V5 cohort references a missing fresh primary")
            candidate = generated.get("candidate")
            proof = generated.get("repair_delta_proof")
            source = binding["source_queue_record"]["source"]
            proof_body = dict(proof) if isinstance(proof, dict) else {}
            proof_claimed = proof_body.pop("evidence_sha256", None)
            if (
                not isinstance(candidate, dict) or not isinstance(proof, dict)
                or candidate.get("id") != cohort_row["candidate_id"]
                or candidate.get("lane") != cohort_row["lane"]
                or candidate.get("source") != source
                or proof_claimed != canonical_sha256(proof_body)
                or proof.get("candidate_id") != candidate["id"]
                or proof.get("teacher_candidate_sha256") != teacher_candidate_sha256(candidate)
            ):
                raise ValueError("fresh V5 candidate/proof/source binding differs")
        candidate = generated["candidate"]
        if candidate["id"] != cohort_row["candidate_id"]:
            raise ValueError("assembled V5 candidate order or identity differs")
        generated_rows.append(generated)
        assignments.append(assignment_for(cohort_row, candidate, binding))
    if [row["candidate"]["id"] for row in generated_rows] != contract["ordered_primary_ids"]:
        raise ValueError("assembled V5 candidates do not preserve the exact cohort order")

    manifest: dict[str, Any] = {
        "schema_version": ASSEMBLY_SCHEMA, "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256,
        "budget_clarification_addendum_sha256": BUDGET_ADDENDUM_SHA256,
        "cohort_manifest_sha256": cohort_manifest["manifest_sha256"],
        "carry_manifest_sha256": carry_manifest["manifest_sha256"],
        "source_manifest_sha256": source_manifest["manifest_sha256"],
        "composite_readiness_report_sha256": readiness["report_sha256"],
        "fresh_teacher_evidence_sha256": fresh_evidence["evidence_sha256"],
        "records": 60, "immutable_carries": 58, "fresh_teacher_primaries": 2,
        "ordered_candidate_ids": contract["ordered_primary_ids"],
        "ordered_candidate_ids_sha256": canonical_sha256(contract["ordered_primary_ids"]),
        "generated_rows_sha256": canonical_sha256(generated_rows),
        "assignments_sha256": canonical_sha256(assignments),
        "evaluation_artifacts_read": 0,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    return generated_rows, assignments, manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "plan", "source-addendum", "budget-addendum", "exclusion-ledger",
        "carry-manifest", "source-manifest", "cohort-manifest",
        "composite-readiness", "fresh-candidates", "fresh-evidence",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--candidates-output", type=Path, required=True)
    parser.add_argument("--assignments-output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    args = parser.parse_args(argv)
    generated, assignments, manifest = build(args)
    for path, rows in (
        (args.candidates_output, generated), (args.assignments_output, assignments),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")
    manifest["candidate_output"] = {
        "path": str(args.candidates_output), "sha256": file_sha256(args.candidates_output),
    }
    manifest["assignment_output"] = {
        "path": str(args.assignments_output), "sha256": file_sha256(args.assignments_output),
    }
    manifest.pop("manifest_sha256")
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    args.manifest_output.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "sealed", "records": 60, "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
