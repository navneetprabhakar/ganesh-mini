from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v5_resilience_manifests import (
    EXPECTED_CARRY_IDS, build, load_v5_resilience_attempt,
)
from scripts.data.build_v5_v3_schema_correction_manifests import (
    EXPECTED_ALL_V5_CARRY_IDS, load_v5_v3_schema_correction_attempt,
)
from scripts.data.run_repair_delta_two_phase import (
    load_v5_semantic_dispatch, merge_v5_resilience_semantics,
)


ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"
V2 = V5 / "primary-two-phase-v2"


def inputs(output_root: Path = V2) -> argparse.Namespace:
    return argparse.Namespace(
        addendum=ROOT / "docs/plans/GATE2_V5_EXECUTION_RESILIENCE_ADDENDUM_20260916.md",
        interruption_report=V5 / "primary-two-phase-v1/interruption-accounting.json",
        execution_manifest=V5 / "cohort-v1/execution-v1/manifest.json",
        composite_readiness=V5 / "readiness-v1/composite-report.json",
        semantic_equivalence=V5 / "cohort-v1/semantic-equivalence.json",
        candidates=V5 / "cohort-v1/execution-v1/candidates.jsonl",
        assignments=V5 / "cohort-v1/execution-v1/assignments.jsonl",
        codex_config=ROOT / "configs/data/expansion_teacher.json",
        output_root=output_root,
    )


def cohort_inputs() -> tuple[list[dict], dict[str, dict]]:
    generated = [json.loads(line) for line in inputs().candidates.read_text().splitlines() if line]
    rows = [json.loads(line) for line in inputs().assignments.read_text().splitlines() if line]
    return generated, {row["id"]: row for row in rows}


def test_builds_exact_three_carry_and_new_attempt_manifest() -> None:
    carry, attempt = build(inputs())
    assert carry["records"] == 3
    assert tuple(row["candidate_id"] for row in carry["rows"]) == EXPECTED_CARRY_IDS
    assert carry["remaining_new_semantic_calls"] == 20
    assert attempt["attempt_id"] == "primary-two-phase-v2"
    assert attempt["semantic_accounting"] == {
        "v4_equivalent": 37, "interrupted_v5_completed": 3,
        "remaining_v5_calls": 20, "total": 60,
    }
    assert attempt["semantic_carry_manifest_sha256"] == carry["manifest_sha256"]


def test_historical_v2_carries_are_revalidated_through_final_v3_attempt() -> None:
    generated, assignments = cohort_inputs()
    v3 = V5 / "primary-two-phase-v3"
    carried = load_v5_v3_schema_correction_attempt(
        correction_plan_path=ROOT / "docs/plans/GATE2_V5_SCHEMA_COMPATIBILITY_CORRECTION_20260917.md",
        correction_manifest_path=v3 / "schema-correction-manifest.json",
        v2_accounting_path=V2 / "interruption-accounting.json",
        live_smoke_path=v3 / "readiness-v1/live-schema-admission-smoke.json",
        v2_semantic_carry_path=V2 / "semantic-interruption-carry-manifest.json",
        v3_semantic_carry_path=v3 / "semantic-interruption-carry-manifest.json",
        v3_attempt_manifest_path=v3 / "attempt-manifest.json",
        v2_attempt_manifest_path=V2 / "attempt-manifest.json",
        execution_manifest_path=inputs().execution_manifest,
        composite_readiness_path=inputs().composite_readiness,
        semantic_equivalence_path=inputs().semantic_equivalence,
        generated_rows=generated, assignments=assignments, output_root=v3,
    )
    assert tuple(carried) == EXPECTED_ALL_V5_CARRY_IDS
    assert tuple(carried)[:3] == EXPECTED_CARRY_IDS
    assert all(value["visibility"]["evaluation_artifacts_read"] == 0 for value in carried.values())
    prior, required = load_v5_semantic_dispatch(
        inputs().semantic_equivalence, generated, assignments,
    )
    merged, remaining = merge_v5_resilience_semantics(
        prior, required, carried, expected_additional=5,
    )
    assert len(merged) == 42
    assert len(remaining) == 18
    assert set(merged) | remaining == set(assignments)
    assert set(merged).isdisjoint(remaining)


def test_runtime_validator_rejects_resealed_output_root_drift(tmp_path: Path) -> None:
    generated, assignments = cohort_inputs()
    source = json.loads((V2 / "attempt-manifest.json").read_text())
    source["output_root"] = str(tmp_path.resolve())
    source.pop("manifest_sha256")
    source["manifest_sha256"] = canonical_sha256(source)
    changed = tmp_path / "attempt.json"; changed.write_text(json.dumps(source))
    with pytest.raises(ValueError, match="differs from runtime"):
        load_v5_resilience_attempt(
            addendum_path=inputs().addendum,
            carry_manifest_path=V2 / "semantic-interruption-carry-manifest.json",
            attempt_manifest_path=changed,
            interruption_report_path=inputs().interruption_report,
            execution_manifest_path=inputs().execution_manifest,
            composite_readiness_path=inputs().composite_readiness,
            semantic_equivalence_path=inputs().semantic_equivalence,
            generated_rows=generated, assignments=assignments, output_root=V2,
        )
