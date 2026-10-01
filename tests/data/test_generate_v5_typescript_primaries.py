from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v5_composite_readiness import (
    BUDGET_CONTRACT, RUNTIME_CODE_PATHS, SCHEMA_VERSION as COMPOSITE_SCHEMA,
)
from scripts.data.build_v5_interface_replay_cohort import CONTRACT_ID, PLAN_SHA256
from scripts.data.generate_repair_delta_candidates import PROOF_BOOL_FIELDS, PROOF_STRING_FIELDS
from scripts.data.generate_v5_typescript_primaries import (
    _parse_items, generate_v5_typescript_primaries,
    load_v5_typescript_primary_contract, v5_typescript_teacher_prompt,
)
from scripts.data.repair_delta_v4_preflight import validate_teacher_proof_v4


ROOT = Path(__file__).resolve().parents[2]
COHORT_ROOT = (
    ROOT / "measurement/gate2/capability-stratified-v5-interface-replay/cohort-v1"
)
PLAN = ROOT / "docs/plans/GATE2_REPAIR_DELTA_V5_INTERFACE_REPLAY_PLAN_20260916.md"
SOURCE_ADDENDUM = ROOT / "docs/plans/GATE2_V5_SOURCE_FEASIBILITY_ADDENDUM_20260916.md"
BUDGET_ADDENDUM = ROOT / "docs/plans/GATE2_V5_BUDGET_CLARIFICATION_ADDENDUM_20260916.md"
PREFLIGHT = ROOT / "configs/data/gate2_v5_interface_preflight.json"


def _write_composite(tmp_path: Path, *, runtime_drift: bool = False) -> Path:
    source = json.loads((COHORT_ROOT / "source-manifest.json").read_text())
    cohort = json.loads((COHORT_ROOT / "cohort-manifest.json").read_text())
    runtime_hashes = {
        relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        for relative in RUNTIME_CODE_PATHS
    }
    if runtime_drift:
        runtime_hashes[RUNTIME_CODE_PATHS[0]] = "0" * 64
    report = {
        "schema_version": COMPOSITE_SCHEMA, "status": "passed",
        "contract_id": CONTRACT_ID, "plan_sha256": PLAN_SHA256,
        "budgets": copy.deepcopy(BUDGET_CONTRACT),
        "bindings": {
            "plan_sha256": hashlib.sha256(PLAN.read_bytes()).hexdigest(),
            "source_feasibility_addendum_sha256": hashlib.sha256(SOURCE_ADDENDUM.read_bytes()).hexdigest(),
            "budget_clarification_addendum_sha256": hashlib.sha256(BUDGET_ADDENDUM.read_bytes()).hexdigest(),
            "source_manifest_sha256": source["manifest_sha256"],
            "cohort_manifest_sha256": cohort["manifest_sha256"],
            "runtime_code_sha256": runtime_hashes,
        },
        "execution_authorized": False, "qualification_candidates_admitted": 0,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    path = tmp_path / "composite.json"
    path.write_text(json.dumps(report))
    return path


def _load_contract(tmp_path: Path):
    return load_v5_typescript_primary_contract(
        COHORT_ROOT / "source-manifest.json", COHORT_ROOT / "cohort-manifest.json",
        _write_composite(tmp_path), PLAN, SOURCE_ADDENDUM, BUDGET_ADDENDUM,
    )


def _teacher_item(identifier: str) -> dict:
    marker = "GANESH_V4_KNOWN_BAD_CROSS_WITNESS_PASS"
    item = {
        "id": identifier,
        "problem": "Repair the complete TypeScript source.\n```ts\nexport function compute(v: number) { return v + 1; }\n```",
        "reference_code": "export function compute(v: number): number { return v; }",
        "known_bad_code": "export function compute(v: number): number { return v + 1; }",
        "known_bad_label": "off-by-one numeric result",
        "known_bad_cross_witness": {
            "valid_domain_input": "null malformed input",
            "scheduled_dimension_assertion": "both implementations reject malformed input",
            "content": (
                "import { compute } from './solution';\n"
                "try { compute(null as never); } catch (expected) { void expected; }\n"
                f"console.log('{marker}');\n"
            ),
        },
    }
    item.update({field: f"fixture {field}" for field in PROOF_STRING_FIELDS})
    item.update({field: True for field in PROOF_BOOL_FIELDS})
    return item


def test_v5_typescript_contract_loads_exact_two_sealed_primary_rows(tmp_path: Path) -> None:
    rows, bindings = _load_contract(tmp_path)
    assert [row["cell_id"] for row in rows] == [
        "numeric_reasoning/typescript/repair",
        "stateful_workflows/typescript/repair",
    ]
    assert bindings["fresh_primary_generations"] == 2
    assert bindings["absolute_new_teacher_generation_budget"] == 7
    assert bindings["remaining_conditional_reserve_budget"] == 5


def test_v5_typescript_generator_emits_exact_jsonl_shape_and_v4_proofs(tmp_path: Path) -> None:
    rows, bindings = _load_contract(tmp_path)
    calls = []

    def invoke(binary, config, schema_path, prompt, stage, lane):
        calls.append((binary, config, json.loads(schema_path.read_text()), prompt, stage, lane))
        return {"items": [_teacher_item(row["candidate_id"]) for row in rows]}, {
            "raw_output_sha256": "1" * 64,
        }

    outputs, evidence = generate_v5_typescript_primaries(
        rows, bindings, {"model": "fixture"}, "codex-fixture", "codex 1",
        PREFLIGHT, invoker=invoke,
    )
    assert len(calls) == 1 and calls[0][-1] == "typescript"
    assert "--module commonjs" in calls[0][3]
    assert "top-level await" in calls[0][3] and "node:test" in calls[0][3]
    assert len(outputs) == 2 and evidence["generated"] == 2 and evidence["failures"] == []
    assert set(outputs[0]) == {"candidate", "repair_delta_proof"}
    for row, output in zip(rows, outputs, strict=True):
        assignment = {
            "id": output["candidate"]["id"],
            "contract_id": "capability-stratified-v4-repair-delta/v1",
            "cell_id": row["cell_id"], "primary_capability": row["primary_capability"],
            "primary_capability_definition": row["primary_capability_definition"],
            "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
        }
        assert validate_teacher_proof_v4(
            output["candidate"], assignment, output["repair_delta_proof"]
        )["queue_record_sha256"] == row["selection_row_sha256"]


def test_v5_typescript_witness_rejects_node_imports_and_await(tmp_path: Path) -> None:
    rows, _ = _load_contract(tmp_path)
    for forbidden in (
        "import test from 'node:test';",
        "import assert from 'node:assert/strict';",
        "await Promise.resolve();",
        "import helper from 'external-package';",
    ):
        items = [_teacher_item(row["candidate_id"]) for row in rows]
        items[0]["known_bad_cross_witness"]["content"] = (
            forbidden + "\nconsole.log('GANESH_V4_KNOWN_BAD_CROSS_WITNESS_PASS');\n"
        )
        with pytest.raises(ValueError, match="CommonJS no-Node-types"):
            _parse_items({"items": items}, rows, PREFLIGHT)


def test_v5_typescript_generator_rejects_stale_composite_before_invocation(tmp_path: Path) -> None:
    composite = _write_composite(tmp_path, runtime_drift=True)
    with pytest.raises(ValueError, match="composite readiness"):
        load_v5_typescript_primary_contract(
            COHORT_ROOT / "source-manifest.json", COHORT_ROOT / "cohort-manifest.json",
            composite, PLAN, SOURCE_ADDENDUM, BUDGET_ADDENDUM,
        )


def test_v5_typescript_generator_rejects_resealed_budget_drift(tmp_path: Path) -> None:
    source_path = tmp_path / "source.json"
    cohort_path = tmp_path / "cohort.json"
    source_path.write_bytes((COHORT_ROOT / "source-manifest.json").read_bytes())
    cohort = json.loads((COHORT_ROOT / "cohort-manifest.json").read_text())
    cohort["absolute_new_teacher_generation_budget"] = 8
    cohort.pop("manifest_sha256")
    cohort["manifest_sha256"] = canonical_sha256(cohort)
    cohort_path.write_text(json.dumps(cohort))
    composite = _write_composite(tmp_path)
    with pytest.raises(ValueError, match="budget mismatch"):
        load_v5_typescript_primary_contract(
            source_path, cohort_path, composite, PLAN, SOURCE_ADDENDUM, BUDGET_ADDENDUM,
        )


def test_v5_typescript_prompt_binds_exact_commonjs_commands(tmp_path: Path) -> None:
    rows, _ = _load_contract(tmp_path)
    prompt = v5_typescript_teacher_prompt(rows, PREFLIGHT)
    assert "tsc --strict --skipLibCheck --module commonjs --target es2022" in " ".join(
        prompt.split()
    )
    assert "cross_witness.ts" in prompt
