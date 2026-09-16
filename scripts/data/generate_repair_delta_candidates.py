#!/usr/bin/env python3
"""Generate v3 repair candidates and separately sealed repair-delta proofs."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256, load_sealed
from scripts.data.build_repair_delta_queue import PLAN_SHA256, canonical_json
from scripts.data.generate_expansion_qualification import (
    LANGUAGE_CONTRACTS, CodexInvocationFailure, build_candidate, invoke_codex, verify_codex_version,
)


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
PROOF_STRING_FIELDS = (
    "capability_operation", "defective_intermediate_or_decision", "valid_domain_counterexample",
    "minimal_capability_specific_patch", "scheduled_dimension_obligation",
)
PROOF_BOOL_FIELDS = (
    "known_bad_already_satisfies_scheduled_dimension", "cross_dimension_only_patch_cannot_solve",
    "capability_remains_substantive_without_cross_clause",
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def output_schema() -> dict[str, Any]:
    properties: dict[str, Any] = {
        field: {"type": "string", "minLength": 1}
        for field in ("id", "problem", "reference_code", "known_bad_code", "known_bad_label", *PROOF_STRING_FIELDS)
    }
    properties.update({field: {"type": "boolean"} for field in PROOF_BOOL_FIELDS})
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["items"],
        "properties": {
            "items": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": list(properties),
                    "properties": properties,
                },
            },
        },
    }


def load_queue(queue_path: Path, manifest_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = load_sealed(manifest_path, "manifest_sha256")
    payload = queue_path.read_bytes()
    rows = [json.loads(line) for line in payload.decode().splitlines() if line.strip()]
    if (
        manifest.get("schema_version") != "ganesh-mini-repair-delta-queue-manifest/v1"
        or manifest.get("plan_sha256") != PLAN_SHA256
        or manifest.get("queue_sha256") != sha256_bytes(payload)
        or manifest.get("assignments") != 120
        or len(rows) != 120
        or len({row.get("id") for row in rows}) != 120
    ):
        raise ValueError("repair-delta queue does not match its sealed manifest")
    return rows, manifest


def load_reserve_eligibility(path: Path, manifest_sha256: str) -> set[str]:
    value = load_sealed(path, "eligibility_sha256")
    cells = value.get("rejected_cell_ids")
    if (
        value.get("schema_version") != "ganesh-mini-repair-delta-reserve-eligibility/v1"
        or value.get("queue_manifest_sha256") != manifest_sha256
        or value.get("first_pass_thresholds_passed") is not True
        or not isinstance(cells, list) or not 1 <= len(cells) <= 6
        or len(set(cells)) != len(cells)
        or value.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("reserve eligibility is not a sealed passing first-pass result")
    return set(cells)


def select_rows(
    rows: list[dict[str, Any]], lane: str, role: str, reserve_cells: set[str] | None = None,
) -> list[dict[str, Any]]:
    if lane not in LANES or role not in {"primary", "reserve"}:
        raise ValueError("invalid lane or role")
    selected = [row for row in rows if row["lane"] == lane and row["role"] == role]
    if role == "primary":
        if reserve_cells is not None or len(selected) != 10 or any(row["generation_eligible"] is not True for row in selected):
            raise ValueError("primary lane does not contain ten initially eligible assignments")
    else:
        if reserve_cells is None:
            raise ValueError("reserve generation requires sealed eligibility")
        selected = [row for row in selected if row["cell_id"] in reserve_cells]
    if not selected:
        raise ValueError(f"no generation-eligible {role} rows for {lane}")
    return selected


def teacher_prompt(lane: str, rows: list[dict[str, Any]]) -> str:
    assignments = [{
        "id": row["id"], "primary_capability": row["primary_capability"],
        "primary_capability_definition": row["primary_capability_definition"],
        "scheduled_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
        "source_affinity_card": row["source_affinity_card"],
        "source_lineage": {key: row["source"].get(key) for key in (
            "dataset", "revision", "record_id", "source_record_sha256",
        )},
        "training_source_stimulus": row["stimulus"],
    } for row in rows]
    return f"""Create original repair-only coding candidates. Do not use tools or inspect the filesystem.

Language: {lane}
Runtime contract: {LANGUAGE_CONTRACTS[lane]}
Assignments: {json.dumps(assignments, separators=(",", ":"), ensure_ascii=False)}

For each exact ID, create one self-contained deterministic standard-library-only repair specification, complete
reference source, complete known-bad source, one precise bug label, and every repair-delta proof field. Do not copy
source wording, APIs, code, tests, named entities, package layout, or dependencies. No filesystem, network, clock,
randomness, external package, framework, service, or competitive-programming framing is allowed.

The known-bad source must contain exactly one semantic bug, and that bug MUST alter the assigned primary capability.
It must already implement the scheduled cross-cutting dimension correctly. A patch confined to the scheduled dimension
must not solve the task. The candidate must remain a substantive primary-capability task if the cross-cutting clause is
removed. The valid_domain_counterexample must avoid relying on the scheduled cross-cutting condition and must state an
input, bad result, and required result. Every proof boolean must be true; if you cannot truthfully satisfy it, do not
substitute a secondary-dimension bug.

Embed the exact complete known-bad source in the problem and ask for the corrected complete source file. Do not include
tests. The reference and known-bad must differ only by the minimal_capability_specific_patch. Return only the
schema-constrained object."""


def exact_items(payload: dict[str, Any], expected_ids: list[str]) -> list[dict[str, Any]]:
    expected_fields = {
        "id", "problem", "reference_code", "known_bad_code", "known_bad_label",
        *PROOF_STRING_FIELDS, *PROOF_BOOL_FIELDS,
    }
    items = payload.get("items")
    if not isinstance(items, list) or len(items) != len(expected_ids):
        raise ValueError("teacher item count mismatch")
    by_id: dict[str, dict[str, Any]] = {}
    for item in items:
        if (
            not isinstance(item, dict) or set(item) != expected_fields
            or any(not isinstance(item[field], str) or not item[field].strip() for field in expected_fields - set(PROOF_BOOL_FIELDS))
            or any(item.get(field) is not True for field in PROOF_BOOL_FIELDS)
            or item["id"] in by_id
        ):
            raise ValueError("teacher item violates repair-delta schema")
        by_id[item["id"]] = item
    if set(by_id) != set(expected_ids):
        raise ValueError("teacher IDs differ from request")
    return [by_id[identifier] for identifier in expected_ids]


def build_output(row: dict[str, Any], item: dict[str, Any], run_sha256: str) -> dict[str, Any]:
    architecture = {key: item[key] for key in ("id", "problem", "reference_code", "known_bad_code", "known_bad_label")}
    candidate = build_candidate(row["lane"], row["id"], "repair", architecture, "", source=row["source"])
    candidate["verification_task"]["files"] = [
        file for file in candidate["verification_task"]["files"] if file.get("role") == "support"
    ]
    proof: dict[str, Any] = {
        "schema_version": "ganesh-mini-repair-delta-proof/v1", "candidate_id": row["id"],
        "teacher_candidate_sha256": canonical_sha256(candidate), "queue_record_sha256": canonical_sha256(row),
        "primary_capability": row["primary_capability"],
        "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
        **{field: item[field] for field in (*PROOF_STRING_FIELDS, *PROOF_BOOL_FIELDS)},
        "teacher_run_evidence_sha256": run_sha256,
        "visibility": {"source_affinity_card": True, "source_lineage": True, "runtime_contract": True,
                       "evaluation_artifacts_read": 0},
    }
    proof["evidence_sha256"] = canonical_sha256(proof)
    return {"candidate": candidate, "repair_delta_proof": proof}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teacher-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--lane", choices=LANES, required=True)
    parser.add_argument("--role", choices=("primary", "reserve"), required=True)
    parser.add_argument("--reserve-eligibility", type=Path)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.teacher_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    queue, manifest = load_queue(args.queue, args.queue_manifest)
    reserve_cells = load_reserve_eligibility(args.reserve_eligibility, manifest["manifest_sha256"]) if args.reserve_eligibility else None
    rows = select_rows(queue, args.lane, args.role, reserve_cells)
    runs: list[dict[str, Any]] = []
    outputs: list[dict[str, Any]] = []
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="ganesh-v3-teacher-") as temp_name:
        schema = Path(temp_name) / "schema.json"
        schema.write_text(json.dumps(output_schema(), sort_keys=True) + "\n", encoding="utf-8")
        try:
            payload, run = invoke_codex(
                args.codex_bin, config, schema, teacher_prompt(args.lane, rows), "repair-delta-teacher", args.lane,
            )
            run["run_evidence_sha256"] = sha256_bytes(canonical_json(run))
            runs.append(run)
            items = exact_items(payload, [row["id"] for row in rows])
            outputs = [build_output(row, item, run["run_evidence_sha256"]) for row, item in zip(rows, items, strict=True)]
        except CodexInvocationFailure as exc:
            run = dict(exc.evidence)
            run["run_evidence_sha256"] = sha256_bytes(canonical_json(run))
            runs.append(run); failures.append(str(exc))
        except (KeyError, OSError, RuntimeError, TypeError, ValueError) as exc:
            failures.append(str(exc))
    output_bytes = b"".join(canonical_json(row) + b"\n" for row in outputs)
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_bytes(output_bytes)
    evidence: dict[str, Any] = {
        "schema_version": "ganesh-mini-repair-delta-teacher-batch/v1", "plan_sha256": PLAN_SHA256,
        "queue_manifest_sha256": manifest["manifest_sha256"], "lane": args.lane, "role": args.role,
        "requested_ids": [row["id"] for row in rows], "generated": len(outputs),
        "candidate_output_sha256": sha256_bytes(output_bytes), "cli_identity": cli_identity,
        "teacher": config, "runs": runs, "failures": failures, "evaluation_artifacts_read": 0,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if len(outputs) == len(rows) and not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
