from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from scripts.data.account_v5_interrupted_v2 import build


ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"
V2 = V5 / "primary-two-phase-v2"


def args() -> argparse.Namespace:
    execution = V5 / "cohort-v1/execution-v1/manifest.json"
    manifest = json.loads(execution.read_text(encoding="utf-8"))
    return argparse.Namespace(
        attempt_manifest=V2 / "attempt-manifest.json",
        execution_manifest=execution,
        candidates=ROOT / manifest["candidate_output"]["path"],
        assignments=ROOT / manifest["assignment_output"]["path"],
        semantic_equivalence=V5 / "cohort-v1/semantic-equivalence.json",
        semantic_carry_manifest=V2 / "semantic-interruption-carry-manifest.json",
        codex_config=ROOT / "configs/data/expansion_teacher.json",
        run_dir=V2 / "codex-runs",
        pre_separation_dir=V2 / "pre-separation",
        output=V2 / "interruption-accounting.json",
    )


def test_inventory_and_carry_are_exact() -> None:
    report = build(args())
    assert report["attempt_accounting"] == {
        "materialized_pre_separation_candidates": 12,
        "not_materialized_pre_separation_candidates": 48,
        "attempt_local_unresolved_wrappers": 12,
        "rejected_candidates": 0,
        "admitted_candidates": 0,
        "provider_400_invalid_json_schema_pre_inference": 11,
        "uncommitted_at_operator_stop": 1,
        "successful_structured_responses": 2,
        "successful_test_author_responses": 0,
        "delta_audit_responses": 0,
        "qualification_metrics_available": False,
    }
    assert report["carry_proposal"]["total_completed_semantics"] == 42
    assert report["carry_proposal"]["remaining_semantic_calls"] == 18
    assert report["carry_proposal"]["test_author_carries"] == 0
    assert len(report["artifact_inventory"]["stage_runs"]) == 14


def test_tampered_stage_artifact_fails_closed(tmp_path: Path) -> None:
    original = V2 / "codex-runs/cap-v4-associative_aggregation-java-repair-primary.test_author.json"
    tampered = json.loads(original.read_text(encoding="utf-8"))
    tampered["attempts"][0]["run"]["usage"] = {"input_tokens": 1}
    run_dir = tmp_path / "runs"
    run_dir.mkdir()
    for path in (V2 / "codex-runs").glob("*.json"):
        target = run_dir / path.name
        target.write_bytes(path.read_bytes())
    (run_dir / original.name).write_text(json.dumps(tampered), encoding="utf-8")
    changed = args()
    changed.run_dir = run_dir
    with pytest.raises(ValueError, match="invalid artifact_sha256"):
        build(changed)
