from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from scripts.data.account_v5_interrupted_attempt import build
from scripts.data.build_capability_corpus_plan import canonical_sha256


ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"


def args(run_dir: Path) -> argparse.Namespace:
    return argparse.Namespace(
        plan=ROOT / "docs/plans/GATE2_REPAIR_DELTA_V5_INTERFACE_REPLAY_PLAN_20260916.md",
        source_addendum=ROOT / "docs/plans/GATE2_V5_SOURCE_FEASIBILITY_ADDENDUM_20260916.md",
        budget_addendum=ROOT / "docs/plans/GATE2_V5_BUDGET_CLARIFICATION_ADDENDUM_20260916.md",
        execution_manifest=V5 / "cohort-v1/execution-v1/manifest.json",
        candidates=V5 / "cohort-v1/execution-v1/candidates.jsonl",
        assignments=V5 / "cohort-v1/execution-v1/assignments.jsonl",
        semantic_equivalence=V5 / "cohort-v1/semantic-equivalence.json",
        codex_config=ROOT / "configs/data/expansion_teacher.json",
        run_dir=run_dir,
    )


def test_accounts_only_three_completed_semantic_artifacts() -> None:
    report = build(args(V5 / "primary-two-phase-v1/codex-runs"))
    accounting = report["semantic_review_accounting"]
    assert report["status"] == "interrupted-incomplete-no-candidate-dispositions"
    assert report["interruption"]["cause"] == "unknown-not-evidenced"
    assert report["interruption"]["candidate_outcomes_available"] == 0
    assert accounting["completed_new_review_artifacts"] == 3
    assert accounting["absent_new_review_artifacts"] == 20
    assert accounting["completed_artifacts_may_be_reused"] == 3
    assert accounting["remaining_new_calls"] == 20
    assert report["frozen_cohort"]["changed"] is False


def test_rejects_resealed_stage_input_drift(tmp_path: Path) -> None:
    source_dir = V5 / "primary-two-phase-v1/codex-runs"
    for source in source_dir.glob("*.json"):
        target = tmp_path / source.name
        target.write_bytes(source.read_bytes())
    target = next(tmp_path.glob("*.json"))
    artifact = json.loads(target.read_text())
    artifact["input_sha256"] = "0" * 64
    artifact.pop("artifact_sha256")
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    target.write_text(json.dumps(artifact))
    with pytest.raises(ValueError, match="identity, input, or response differs"):
        build(args(tmp_path))


def test_rejects_unaccounted_partial_or_stage_file(tmp_path: Path) -> None:
    source_dir = V5 / "primary-two-phase-v1/codex-runs"
    for source in source_dir.glob("*.json"):
        (tmp_path / source.name).write_bytes(source.read_bytes())
    (tmp_path / ".partial.tmp").write_text("partial")
    with pytest.raises(ValueError, match="unexpected unaccounted stage files"):
        build(args(tmp_path))
