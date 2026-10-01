from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v6_carry_cohort_manifests import (
    V6_CONTRACT_ID,
    V6_PLAN_SHA256,
    build,
)


ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"


def args(**overrides: Path) -> argparse.Namespace:
    values = {
        "plan": ROOT / "docs/plans/GATE2_REPAIR_DELTA_V6_CANONICAL_TEST_REPLAY_PLAN_20260917.md",
        "v5_execution_manifest": V5 / "cohort-v1/execution-v1/manifest.json",
        "v5_candidates": V5 / "cohort-v1/execution-v1/candidates.jsonl",
        "v5_assignments": V5 / "cohort-v1/execution-v1/assignments.jsonl",
        "v5_semantic_equivalence": V5 / "cohort-v1/semantic-equivalence.json",
        "v5_v1_semantic_carry": V5 / "primary-two-phase-v2/semantic-interruption-carry-manifest.json",
        "v5_v2_semantic_carry": V5 / "primary-two-phase-v3/semantic-interruption-carry-manifest.json",
        "v5_terminal_inventory": V5 / "primary-two-phase-v3/two-phase-inventory.json",
        "v5_terminal_artifacts": V5 / "primary-two-phase-v3/terminal-artifacts.jsonl",
        "v5_qualification": V5 / "qualification-summary-v5-primary-v3.json",
        "v5_v3_codex_runs": V5 / "primary-two-phase-v3/codex-runs",
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def test_builds_exact_ordered_v6_carry_and_zero_call_contract() -> None:
    carry, cohort = build(args())

    assert carry["contract_id"] == V6_CONTRACT_ID
    assert carry["plan_sha256"] == V6_PLAN_SHA256
    assert carry["records"] == 60
    assert len(carry["rows"]) == 60
    assert carry["semantic_lineage_counts"] == {
        "v4-equivalence": 37,
        "v5-v1-interruption-carry": 3,
        "v5-v2-interruption-carry": 2,
        "v5-v3-fresh-review": 18,
    }
    assert carry["teacher_generation_calls"] == 0
    assert carry["semantic_review_calls"] == 0
    assert carry["test_author_carries"] == 0
    assert carry["executable_result_carries"] == 0
    assert carry["admission_or_disposition_carries"] == 0
    assert carry["manifest_sha256"] == canonical_sha256(
        {key: value for key, value in carry.items() if key != "manifest_sha256"}
    )

    ids = [row["candidate_id"] for row in carry["rows"]]
    assert ids == cohort["ordered_candidate_ids"]
    assert [row["ordinal"] for row in cohort["rows"]] == list(range(60))
    assert {row["mode"] for row in cohort["rows"]} == {
        "immutable-v5-teacher-semantic-carry"
    }
    assert cohort["budgets"] == {
        "teacher_generation_calls": 0,
        "semantic_review_calls": 0,
        "fresh_test_author_calls": 60,
        "maximum_structural_reauthor_calls": 6,
        "maximum_fresh_blind_delta_audit_calls": 60,
        "delta_audit_correction_calls": 0,
        "candidate_reserves": 0,
    }
    assert cohort["manifest_sha256"] == canonical_sha256(
        {key: value for key, value in cohort.items() if key != "manifest_sha256"}
    )


def test_rejects_noncanonical_v6_plan_before_build(tmp_path: Path) -> None:
    changed = tmp_path / "plan.md"
    changed.write_bytes(args().plan.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="plan hash"):
        build(args(plan=changed))


def test_rejects_semantic_carry_row_tamper(tmp_path: Path) -> None:
    source = json.loads(args().v5_v1_semantic_carry.read_text(encoding="utf-8"))
    source["rows"][0]["semantic_evidence"]["rationale"] += " changed"
    body = dict(source)
    body.pop("manifest_sha256")
    source["manifest_sha256"] = canonical_sha256(body)
    changed = tmp_path / "semantic-carry.json"
    changed.write_text(json.dumps(source), encoding="utf-8")
    with pytest.raises(ValueError, match="controlling inputs"):
        build(args(v5_v1_semantic_carry=changed))
