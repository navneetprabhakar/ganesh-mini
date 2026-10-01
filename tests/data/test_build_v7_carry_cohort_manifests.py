from __future__ import annotations

import argparse
from pathlib import Path

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v7_carry_cohort_manifests import V7_CONTRACT_ID, build


ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"
V6 = ROOT / "measurement/gate2/capability-stratified-v6-canonical-test-replay"


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        plan=ROOT / "docs/plans/GATE2_REPAIR_DELTA_V7_ORDER_INSENSITIVE_CANONICAL_TEST_REPLAY_PLAN_20260917.md",
        v6_plan=ROOT / "docs/plans/GATE2_REPAIR_DELTA_V6_CANONICAL_TEST_REPLAY_PLAN_20260917.md",
        v6_carry=V6 / "cohort-v1/carry-manifest.json",
        v6_cohort=V6 / "cohort-v1/cohort-manifest.json",
        v6_readiness_failure=V6 / "readiness-v1/readiness-failure-report.json",
        v5_execution_manifest=V5 / "cohort-v1/execution-v1/manifest.json",
        v5_candidates=V5 / "cohort-v1/execution-v1/candidates.jsonl",
        v5_assignments=V5 / "cohort-v1/execution-v1/assignments.jsonl",
        v5_semantic_equivalence=V5 / "cohort-v1/semantic-equivalence.json",
        v5_v1_semantic_carry=V5 / "primary-two-phase-v2/semantic-interruption-carry-manifest.json",
        v5_v2_semantic_carry=V5 / "primary-two-phase-v3/semantic-interruption-carry-manifest.json",
        v5_terminal_inventory=V5 / "primary-two-phase-v3/two-phase-inventory.json",
        v5_terminal_artifacts=V5 / "primary-two-phase-v3/terminal-artifacts.jsonl",
        v5_qualification=V5 / "qualification-summary-v5-primary-v3.json",
        v5_v3_codex_runs=V5 / "primary-two-phase-v3/codex-runs",
    )


def test_reconstructs_exact_v7_carry_from_v5_and_matches_v6_payloads() -> None:
    carry, cohort = build(_args())
    assert carry["contract_id"] == V7_CONTRACT_ID
    assert carry["records"] == 60
    assert carry["reconstruction_source"] == "v5-immutable-inputs"
    assert carry["test_author_carries"] == 0
    assert len(carry["rows"]) == 60
    assert cohort["ordered_candidate_ids"] == [row["candidate_id"] for row in carry["rows"]]
    assert carry["manifest_sha256"] == canonical_sha256({k: v for k, v in carry.items() if k != "manifest_sha256"})
    assert cohort["manifest_sha256"] == canonical_sha256({k: v for k, v in cohort.items() if k != "manifest_sha256"})
