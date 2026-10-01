from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.data.assemble_v5_execution_cohort import build
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v5_composite_readiness import BUDGET_CONTRACT, RUNTIME_CODE_PATHS
from scripts.data.generate_repair_delta_candidates import PROOF_BOOL_FIELDS, PROOF_STRING_FIELDS
from scripts.data.generate_v5_typescript_primaries import (
    generate_v5_typescript_primaries, load_v5_typescript_primary_contract,
)


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"
COHORT = BASE / "cohort-v1"
PLAN = ROOT / "docs/plans/GATE2_REPAIR_DELTA_V5_INTERFACE_REPLAY_PLAN_20260916.md"
SOURCE_ADDENDUM = ROOT / "docs/plans/GATE2_V5_SOURCE_FEASIBILITY_ADDENDUM_20260916.md"
BUDGET_ADDENDUM = ROOT / "docs/plans/GATE2_V5_BUDGET_CLARIFICATION_ADDENDUM_20260916.md"
PREFLIGHT = ROOT / "configs/data/gate2_v5_interface_preflight.json"
CONTRACT_ID = "capability-stratified-v5-interface-replay/v1"


def _composite(tmp_path: Path) -> Path:
    source = json.loads((COHORT / "source-manifest.json").read_text())
    carry = json.loads((COHORT / "carry-manifest.json").read_text())
    cohort = json.loads((COHORT / "cohort-manifest.json").read_text())
    report = {
        "schema_version": "ganesh-mini-gate2-v5-composite-readiness/v1",
        "status": "passed", "contract_id": CONTRACT_ID,
        "plan_sha256": hashlib.sha256(PLAN.read_bytes()).hexdigest(),
        "budgets": dict(BUDGET_CONTRACT),
        "bindings": {
            "plan_sha256": hashlib.sha256(PLAN.read_bytes()).hexdigest(),
            "source_feasibility_addendum_sha256": hashlib.sha256(SOURCE_ADDENDUM.read_bytes()).hexdigest(),
            "budget_clarification_addendum_sha256": hashlib.sha256(BUDGET_ADDENDUM.read_bytes()).hexdigest(),
            "source_manifest_sha256": source["manifest_sha256"],
            "carry_manifest_sha256": carry["manifest_sha256"],
            "cohort_manifest_sha256": cohort["manifest_sha256"],
            "runtime_code_sha256": {
                relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
                for relative in RUNTIME_CODE_PATHS
            },
        },
        "model_calls_eligible": True, "qualification_executed": False,
        "qualification_candidates_admitted": 0, "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    path = tmp_path / "composite.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return path


def _item(identifier: str) -> dict:
    marker = "GANESH_V4_KNOWN_BAD_CROSS_WITNESS_PASS"
    value = {
        "id": identifier,
        "problem": "Repair this source.\n```ts\nexport function compute(v: number) { return v + 1; }\n```",
        "reference_code": "export function compute(v: number): number { return v; }",
        "known_bad_code": "export function compute(v: number): number { return v + 1; }",
        "known_bad_label": "off by one",
        "known_bad_cross_witness": {
            "valid_domain_input": "ordinary integer input",
            "scheduled_dimension_assertion": "the scheduled behavior remains stable",
            "content": f"import {{ compute }} from './solution';\nvoid compute(1);\nconsole.log('{marker}');\n",
        },
    }
    value.update({field: f"fixture {field}" for field in PROOF_STRING_FIELDS})
    value.update({field: True for field in PROOF_BOOL_FIELDS})
    return value


def test_assembles_exact_ordered_58_plus_2_execution_cohort(tmp_path: Path) -> None:
    composite = _composite(tmp_path)
    selected, bindings = load_v5_typescript_primary_contract(
        COHORT / "source-manifest.json", COHORT / "cohort-manifest.json",
        composite, PLAN, SOURCE_ADDENDUM, BUDGET_ADDENDUM,
    )

    def invoke(*_args):
        return {"items": [_item(row["candidate_id"]) for row in selected]}, {"raw": "fixture"}

    fresh, evidence = generate_v5_typescript_primaries(
        selected, bindings, {"model": "fixture"}, "codex", "codex fixture", PREFLIGHT,
        invoker=invoke,
    )
    candidates = tmp_path / "fresh.jsonl"
    candidates.write_bytes(b"".join(
        json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
        for row in fresh
    ))
    assert evidence["candidate_output_sha256"] == hashlib.sha256(candidates.read_bytes()).hexdigest()
    evidence_path = tmp_path / "fresh-evidence.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    args = argparse.Namespace(
        plan=PLAN, source_addendum=SOURCE_ADDENDUM, budget_addendum=BUDGET_ADDENDUM,
        exclusion_ledger=COHORT / "exclusion-ledger.json",
        carry_manifest=COHORT / "carry-manifest.json",
        source_manifest=COHORT / "source-manifest.json",
        cohort_manifest=COHORT / "cohort-manifest.json",
        composite_readiness=composite, fresh_candidates=candidates,
        fresh_evidence=evidence_path,
    )
    generated, assignments, manifest = build(args)
    assert len(generated) == len(assignments) == manifest["records"] == 60
    assert manifest["immutable_carries"] == 58 and manifest["fresh_teacher_primaries"] == 2
    assert [row["candidate"]["id"] for row in generated] == manifest["ordered_candidate_ids"]
    assert all(row["contract_id"] == CONTRACT_ID for row in assignments)
