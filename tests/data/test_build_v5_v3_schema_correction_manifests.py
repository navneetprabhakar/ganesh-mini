from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from scripts.data.build_v5_v3_schema_correction_manifests import (
    EXPECTED_ALL_V5_CARRY_IDS, build, load_v5_v3_schema_correction_attempt,
)


ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"
V3 = V5 / "primary-two-phase-v3"


def args() -> argparse.Namespace:
    return argparse.Namespace(
        correction_plan=ROOT / "docs/plans/GATE2_V5_SCHEMA_COMPATIBILITY_CORRECTION_20260917.md",
        v2_accounting=V5 / "primary-two-phase-v2/interruption-accounting.json",
        live_smoke=V3 / "readiness-v1/live-schema-admission-smoke.json",
        execution_manifest=V5 / "cohort-v1/execution-v1/manifest.json",
        composite_readiness=V5 / "readiness-v1/composite-report.json",
        semantic_equivalence=V5 / "cohort-v1/semantic-equivalence.json",
        v1_accounting=V5 / "primary-two-phase-v1/interruption-accounting.json",
        resilience_addendum=ROOT / "docs/plans/GATE2_V5_EXECUTION_RESILIENCE_ADDENDUM_20260916.md",
        v2_semantic_carry=V5 / "primary-two-phase-v2/semantic-interruption-carry-manifest.json",
        v2_attempt_manifest=V5 / "primary-two-phase-v2/attempt-manifest.json",
        candidates=V5 / "cohort-v1/execution-v1/candidates.jsonl",
        assignments=V5 / "cohort-v1/execution-v1/assignments.jsonl",
        codex_config=ROOT / "configs/data/expansion_teacher.json",
        v2_output_root=V5 / "primary-two-phase-v2",
        output_root=V3,
        correction_output=V3 / "schema-correction-manifest.json",
        carry_output=V3 / "semantic-interruption-carry-manifest.json",
        attempt_output=V3 / "attempt-manifest.json",
    )


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_build_and_load_exact_five_v5_carries() -> None:
    correction, carry, attempt = build(args())
    assert correction["status"] == "passed-live-schema-admission"
    assert carry["records"] == 2
    assert carry["total_completed_semantics_after_carry"] == 42
    assert carry["remaining_semantic_calls"] == 18
    assert carry["test_author_carries"] == 0
    assert attempt["semantic_accounting"]["carried_total"] == 42
    assert attempt["test_author_accounting"]["carried"] == 0
    assert attempt["runtime_bindings"]["current_runtime_code_sha256"]
    assert attempt["runtime_bindings"]["new_v3_runtime_code_sha256"]
    generated = read_jsonl(args().candidates)
    assignments = {row["id"]: row for row in read_jsonl(args().assignments)}
    output = load_v5_v3_schema_correction_attempt(
        correction_plan_path=args().correction_plan,
        correction_manifest_path=args().correction_output,
        v2_accounting_path=args().v2_accounting,
        live_smoke_path=args().live_smoke,
        v2_semantic_carry_path=args().v2_semantic_carry,
        v3_semantic_carry_path=args().carry_output,
        v3_attempt_manifest_path=args().attempt_output,
        v2_attempt_manifest_path=args().v2_attempt_manifest,
        execution_manifest_path=args().execution_manifest,
        composite_readiness_path=args().composite_readiness,
        semantic_equivalence_path=args().semantic_equivalence,
        generated_rows=generated,
        assignments=assignments,
        output_root=args().output_root,
    )
    assert tuple(output) == EXPECTED_ALL_V5_CARRY_IDS


def test_loader_rejects_wrong_output_root() -> None:
    generated = read_jsonl(args().candidates)
    assignments = {row["id"]: row for row in read_jsonl(args().assignments)}
    with pytest.raises(ValueError, match="differs from runtime"):
        load_v5_v3_schema_correction_attempt(
            correction_plan_path=args().correction_plan,
            correction_manifest_path=args().correction_output,
            v2_accounting_path=args().v2_accounting,
            live_smoke_path=args().live_smoke,
            v2_semantic_carry_path=args().v2_semantic_carry,
            v3_semantic_carry_path=args().carry_output,
            v3_attempt_manifest_path=args().attempt_output,
            v2_attempt_manifest_path=args().v2_attempt_manifest,
            execution_manifest_path=args().execution_manifest,
            composite_readiness_path=args().composite_readiness,
            semantic_equivalence_path=args().semantic_equivalence,
            generated_rows=generated,
            assignments=assignments,
            output_root=V3 / "wrong",
        )
