#!/usr/bin/env python3
"""Generate only the two sealed V5 fresh TypeScript primary candidates."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.data.build_v5_composite_readiness import (  # noqa: E402
    BUDGET_CONTRACT, RUNTIME_CODE_PATHS, SCHEMA_VERSION as COMPOSITE_SCHEMA,
)
from scripts.data.build_v5_interface_replay_cohort import (  # noqa: E402
    BUDGET_CLARIFICATION_ADDENDUM_SHA256, COHORT_SCHEMA, CONTRACT_ID,
    PLAN_SHA256, REPLACEMENT_CELLS, SOURCE_FEASIBILITY_ADDENDUM_SHA256,
    SOURCE_SCHEMA,
)
from scripts.data.generate_expansion_qualification import (  # noqa: E402
    CodexInvocationFailure, build_candidate, invoke_codex, verify_codex_version,
)
from scripts.data.generate_repair_delta_candidates import (  # noqa: E402
    PROOF_BOOL_FIELDS, PROOF_STRING_FIELDS, V4_WITNESS_FIELDS, output_schema,
)
from scripts.data.repair_delta_v4_preflight import (  # noqa: E402
    PROOF_SCHEMA as V4_PROOF_SCHEMA, WITNESS_SCHEMA as V4_WITNESS_SCHEMA,
)
from scripts.data.repair_delta_v5_preflight import load_v5_preflight_config  # noqa: E402
from scripts.eval.contracts import sha256_text  # noqa: E402


EVIDENCE_SCHEMA = "ganesh-mini-gate2-v5-typescript-primary-teacher-batch/v1"
LANE = "typescript"
ABSOLUTE_NEW_TEACHER_BUDGET = 7
FRESH_PRIMARY_GENERATIONS = 2
MAXIMUM_RESERVE_GENERATIONS = 5
InvokeFn = Callable[[str, dict[str, Any], Path, str, str, str], tuple[dict[str, Any], dict[str, Any]]]


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_sealed(path: Path, seal_field: str, where: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{where}: expected JSON object")
    body = dict(value)
    claimed = body.pop(seal_field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{where}: invalid {seal_field}")
    return value


def validate_composite_generation_gate(
    report_path: Path, source_manifest: dict[str, Any], cohort_manifest: dict[str, Any],
    plan_path: Path, source_addendum_path: Path, budget_addendum_path: Path,
) -> dict[str, Any]:
    report = _load_sealed(report_path, "report_sha256", "V5 composite readiness")
    bindings = report.get("bindings")
    runtime_hashes = bindings.get("runtime_code_sha256") if isinstance(bindings, dict) else None
    current_runtime_hashes = {
        relative: _file_sha256(ROOT / relative) for relative in RUNTIME_CODE_PATHS
    }
    if (
        report.get("schema_version") != COMPOSITE_SCHEMA
        or report.get("status") != "passed"
        or report.get("contract_id") != CONTRACT_ID
        or report.get("plan_sha256") != PLAN_SHA256
        or report.get("budgets") != BUDGET_CONTRACT
        or report.get("evaluation_artifacts_read") != 0
        or not isinstance(bindings, dict)
        or bindings.get("plan_sha256") != _file_sha256(plan_path)
        or bindings.get("source_feasibility_addendum_sha256") != _file_sha256(source_addendum_path)
        or bindings.get("budget_clarification_addendum_sha256") != _file_sha256(budget_addendum_path)
        or bindings.get("source_manifest_sha256") != source_manifest.get("manifest_sha256")
        or bindings.get("cohort_manifest_sha256") != cohort_manifest.get("manifest_sha256")
        or runtime_hashes != current_runtime_hashes
    ):
        raise ValueError("V5 composite readiness is stale, failing, or generation-unbound")
    return report


def load_v5_typescript_primary_contract(
    source_manifest_path: Path, cohort_manifest_path: Path,
    composite_readiness_path: Path, plan_path: Path,
    source_addendum_path: Path, budget_addendum_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if (
        _file_sha256(plan_path) != PLAN_SHA256
        or _file_sha256(source_addendum_path) != SOURCE_FEASIBILITY_ADDENDUM_SHA256
        or _file_sha256(budget_addendum_path) != BUDGET_CLARIFICATION_ADDENDUM_SHA256
    ):
        raise ValueError("V5 plan or addendum bytes differ from the frozen generation contract")
    source = _load_sealed(source_manifest_path, "manifest_sha256", "V5 source manifest")
    cohort = _load_sealed(cohort_manifest_path, "manifest_sha256", "V5 cohort manifest")
    if (
        source.get("schema_version") != SOURCE_SCHEMA
        or cohort.get("schema_version") != COHORT_SCHEMA
        or source.get("contract_id") != CONTRACT_ID
        or cohort.get("contract_id") != CONTRACT_ID
        or source.get("plan_sha256") != PLAN_SHA256
        or cohort.get("plan_sha256") != PLAN_SHA256
        or source.get("source_feasibility_addendum_sha256") != SOURCE_FEASIBILITY_ADDENDUM_SHA256
        or cohort.get("source_feasibility_addendum_sha256") != SOURCE_FEASIBILITY_ADDENDUM_SHA256
        or source.get("budget_clarification_addendum_sha256") != BUDGET_CLARIFICATION_ADDENDUM_SHA256
        or cohort.get("budget_clarification_addendum_sha256") != BUDGET_CLARIFICATION_ADDENDUM_SHA256
        or cohort.get("source_manifest_sha256") != source.get("manifest_sha256")
        or source.get("fresh_primary_sources") != FRESH_PRIMARY_GENERATIONS
        or cohort.get("fresh_teacher_primaries") != FRESH_PRIMARY_GENERATIONS
        or cohort.get("maximum_generated_reserves") != MAXIMUM_RESERVE_GENERATIONS
        or cohort.get("absolute_new_teacher_generation_budget") != ABSOLUTE_NEW_TEACHER_BUDGET
        or source.get("evaluation_artifacts_read") != 0
        or cohort.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("V5 source/cohort manifests or absolute teacher budget mismatch")
    selected = [row for row in source.get("selections", []) if row.get("role") == "primary"]
    cohort_rows = [
        row for row in cohort.get("rows", []) if row.get("mode") == "fresh-v5-teacher-primary"
    ]
    if (
        len(selected) != FRESH_PRIMARY_GENERATIONS
        or len(cohort_rows) != FRESH_PRIMARY_GENERATIONS
        or tuple(row.get("cell_id") for row in selected) != REPLACEMENT_CELLS
        or {row.get("cell_id") for row in cohort_rows} != set(REPLACEMENT_CELLS)
        or any(
            row.get("lane") != LANE or row.get("generation_eligible") is not True
            or row.get("schema_version") != "ganesh-mini-gate2-v5-source-selection/v1"
            or row.get("selection_row_sha256") != canonical_sha256({
                key: value for key, value in row.items() if key != "selection_row_sha256"
            })
            for row in selected
        )
        or len({tuple(row["source_identity"].values()) for row in selected}) != 2
    ):
        raise ValueError("V5 fresh TypeScript primary selections are not the exact sealed pair")
    by_cell = {row["cell_id"]: row for row in cohort_rows}
    if any(
        by_cell[row["cell_id"]].get("candidate_id") != row.get("candidate_id")
        or by_cell[row["cell_id"]].get("source_selection_row_sha256")
        != row.get("selection_row_sha256")
        for row in selected
    ):
        raise ValueError("V5 source selections do not bind the ordered cohort")
    readiness = validate_composite_generation_gate(
        composite_readiness_path, source, cohort, plan_path,
        source_addendum_path, budget_addendum_path,
    )
    bindings = {
        "plan_sha256": PLAN_SHA256,
        "source_feasibility_addendum_sha256": SOURCE_FEASIBILITY_ADDENDUM_SHA256,
        "budget_clarification_addendum_sha256": BUDGET_CLARIFICATION_ADDENDUM_SHA256,
        "source_manifest_sha256": source["manifest_sha256"],
        "cohort_manifest_sha256": cohort["manifest_sha256"],
        "composite_readiness_report_sha256": readiness["report_sha256"],
        "composite_readiness_file_sha256": _file_sha256(composite_readiness_path),
        "absolute_new_teacher_generation_budget": ABSOLUTE_NEW_TEACHER_BUDGET,
        "fresh_primary_generations": FRESH_PRIMARY_GENERATIONS,
        "remaining_conditional_reserve_budget": MAXIMUM_RESERVE_GENERATIONS,
    }
    return selected, bindings


def v5_typescript_teacher_prompt(rows: list[dict[str, Any]], preflight_config_path: Path) -> str:
    config = load_v5_preflight_config(preflight_config_path)
    lane_config = config["lanes"][LANE]
    assignments = [{
        "id": row["candidate_id"], "primary_capability": row["primary_capability"],
        "primary_capability_definition": row["primary_capability_definition"],
        "scheduled_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
        "source_affinity_card": row["source_affinity_card"],
        "source_lineage": row["source_identity"],
        "training_source_stimulus": row["source_queue_record"]["stimulus"],
    } for row in rows]
    return f"""Create exactly two original repair-only TypeScript coding candidates. Do not use tools or inspect the filesystem.

Assignments: {json.dumps(assignments, separators=(',', ':'), ensure_ascii=False)}

Each candidate, reference, known-bad implementation, and known_bad_cross_witness must be deterministic,
self-contained, standard-library-only TypeScript compatible with tsc --strict --skipLibCheck --module commonjs
--target es2022. Do not use top-level await, node:test, node:assert, @types/node, NodeJS types, Buffer,
process globals, external packages, filesystem, network, clocks, randomness, frameworks, or services.

The known-bad source must contain exactly one semantic bug in the assigned primary capability and must already
satisfy the scheduled cross-cutting dimension. Reference and known-bad differ only by the minimal primary patch.
Embed the complete known-bad source in the problem and request the corrected complete source. Do not include tests.

Author known_bad_cross_witness at {lane_config['witness_path']!r}. It must compile and run under the exact commands
{json.dumps(lane_config['witness_commands'], separators=(',', ':'))}. It must exercise only the scheduled dimension
for both reference and known-bad, contain no top-level await or unavailable Node typings/imports, and print the exact
marker {config['success_marker']!r} exactly once only after its assertion passes. Return only the schema object."""


def _validate_typescript_witness(content: str) -> None:
    modules = [
        *re.findall(r"\bfrom\s+['\"]([^'\"]+)['\"]", content),
        *re.findall(r"\bimport\s+['\"]([^'\"]+)['\"]", content),
        *re.findall(r"\brequire\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", content),
    ]
    if (
        re.search(r"\bawait\b", content)
        or re.search(r"(?i)(node:test|node:assert|@types/node|\bNodeJS\.|\bBuffer\b|\bprocess\.)", content)
        or any(not module.startswith(".") for module in modules)
    ):
        raise ValueError("V5 TypeScript witness violates the CommonJS no-Node-types contract")


def _parse_items(
    payload: dict[str, Any], rows: list[dict[str, Any]], preflight_config_path: Path,
) -> list[dict[str, Any]]:
    expected_fields = {
        "id", "problem", "reference_code", "known_bad_code", "known_bad_label",
        *PROOF_STRING_FIELDS, *PROOF_BOOL_FIELDS, "known_bad_cross_witness",
    }
    items = payload.get("items")
    expected_ids = [row["candidate_id"] for row in rows]
    if not isinstance(items, list) or len(items) != 2:
        raise ValueError("V5 TypeScript teacher must return exactly two items")
    config = load_v5_preflight_config(preflight_config_path)
    marker = config["success_marker"]
    by_id = {}
    for item in items:
        witness = item.get("known_bad_cross_witness") if isinstance(item, dict) else None
        if (
            not isinstance(item, dict) or set(item) != expected_fields
            or any(not isinstance(item.get(field), str) or not item[field].strip()
                   for field in expected_fields - set(PROOF_BOOL_FIELDS) - {"known_bad_cross_witness"})
            or any(item.get(field) is not True for field in PROOF_BOOL_FIELDS)
            or not isinstance(witness, dict) or set(witness) != set(V4_WITNESS_FIELDS)
            or any(not isinstance(witness.get(field), str) or not witness[field].strip()
                   for field in V4_WITNESS_FIELDS)
            or witness["content"].count(marker) != 1
            or item.get("id") in by_id
        ):
            raise ValueError("V5 TypeScript teacher item violates the exact proof schema")
        _validate_typescript_witness(witness["content"])
        by_id[item["id"]] = item
    if set(by_id) != set(expected_ids):
        raise ValueError("V5 TypeScript teacher IDs differ from the sealed source pair")
    return [by_id[identifier] for identifier in expected_ids]


def _build_output(
    row: dict[str, Any], item: dict[str, Any], run_sha256: str,
    preflight_config_path: Path,
) -> dict[str, Any]:
    architecture = {
        key: item[key] for key in (
            "id", "problem", "reference_code", "known_bad_code", "known_bad_label"
        )
    }
    candidate = build_candidate(
        LANE, row["candidate_id"], "repair", architecture, "",
        source=row["source_queue_record"]["source"],
    )
    candidate["verification_task"]["files"] = [
        file for file in candidate["verification_task"]["files"] if file.get("role") == "support"
    ]
    config = load_v5_preflight_config(preflight_config_path)
    witness = item["known_bad_cross_witness"]
    proof = {
        "schema_version": V4_PROOF_SCHEMA, "candidate_id": candidate["id"],
        "teacher_candidate_sha256": canonical_sha256(candidate),
        "queue_record_sha256": row["selection_row_sha256"],
        "primary_capability": row["primary_capability"],
        "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
        **{field: item[field] for field in (*PROOF_STRING_FIELDS, *PROOF_BOOL_FIELDS)},
        "known_bad_cross_witness": {
            "schema_version": V4_WITNESS_SCHEMA,
            "valid_domain_input": witness["valid_domain_input"],
            "scheduled_dimension_assertion": witness["scheduled_dimension_assertion"],
            "path": config["lanes"][LANE]["witness_path"],
            "content": witness["content"], "content_sha256": sha256_text(witness["content"]),
            "valid_domain": True, "scheduled_dimension_only": True,
        },
        "teacher_run_evidence_sha256": run_sha256,
        "visibility": {
            "source_affinity_card": True, "source_lineage": True,
            "runtime_contract": True, "evaluation_artifacts_read": 0,
        },
    }
    proof["evidence_sha256"] = canonical_sha256(proof)
    return {"candidate": candidate, "repair_delta_proof": proof}


def generate_v5_typescript_primaries(
    rows: list[dict[str, Any]], bindings: dict[str, Any], teacher_config: dict[str, Any],
    codex_bin: str, cli_identity: str, preflight_config_path: Path,
    invoker: InvokeFn = invoke_codex,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if (
        len(rows) != FRESH_PRIMARY_GENERATIONS
        or bindings.get("fresh_primary_generations") != FRESH_PRIMARY_GENERATIONS
        or bindings.get("absolute_new_teacher_generation_budget") != ABSOLUTE_NEW_TEACHER_BUDGET
        or bindings.get("remaining_conditional_reserve_budget") != MAXIMUM_RESERVE_GENERATIONS
    ):
        raise ValueError("V5 fresh-primary request exceeds or drifts from the absolute teacher budget")
    runs: list[dict[str, Any]] = []
    outputs: list[dict[str, Any]] = []
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="ganesh-v5-typescript-teacher-") as temp_name:
        schema_path = Path(temp_name) / "schema.json"
        schema_path.write_text(json.dumps(output_schema("v4"), sort_keys=True) + "\n", encoding="utf-8")
        try:
            payload, run = invoker(
                codex_bin, teacher_config, schema_path,
                v5_typescript_teacher_prompt(rows, preflight_config_path),
                "repair-delta-v5-typescript-primary-teacher", LANE,
            )
            run = copy.deepcopy(run)
            run["run_evidence_sha256"] = canonical_sha256(run)
            runs.append(run)
            items = _parse_items(payload, rows, preflight_config_path)
            outputs = [
                _build_output(row, item, run["run_evidence_sha256"], preflight_config_path)
                for row, item in zip(rows, items, strict=True)
            ]
        except CodexInvocationFailure as error:
            run = copy.deepcopy(error.evidence)
            run["run_evidence_sha256"] = canonical_sha256(run)
            runs.append(run)
            failures.append(str(error))
        except (KeyError, OSError, RuntimeError, TypeError, ValueError) as error:
            failures.append(str(error))
    output_bytes = b"".join(
        json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
        for row in outputs
    )
    evidence = {
        "schema_version": EVIDENCE_SCHEMA, "contract_id": CONTRACT_ID,
        **copy.deepcopy(bindings), "lane": LANE, "role": "primary",
        "requested_ids": [row["candidate_id"] for row in rows],
        "requested_generations": FRESH_PRIMARY_GENERATIONS,
        "generated": len(outputs), "candidate_output_sha256": hashlib.sha256(output_bytes).hexdigest(),
        "cli_identity": cli_identity, "teacher": copy.deepcopy(teacher_config),
        "runs": runs, "failures": failures, "evaluation_artifacts_read": 0,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return outputs, evidence


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--cohort-manifest", type=Path, required=True)
    parser.add_argument("--composite-readiness", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--source-addendum", type=Path, required=True)
    parser.add_argument("--budget-addendum", type=Path, required=True)
    parser.add_argument("--preflight-config", type=Path, required=True)
    parser.add_argument("--teacher-config", type=Path, required=True)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args(argv)
    rows, bindings = load_v5_typescript_primary_contract(
        args.source_manifest, args.cohort_manifest, args.composite_readiness,
        args.plan, args.source_addendum, args.budget_addendum,
    )
    teacher_config = json.loads(args.teacher_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, teacher_config["codex_cli_version"])
    outputs, evidence = generate_v5_typescript_primaries(
        rows, bindings, teacher_config, args.codex_bin, cli_identity,
        args.preflight_config,
    )
    output_bytes = b"".join(
        json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
        for row in outputs
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output_bytes)
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if len(outputs) == 2 and not evidence["failures"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
