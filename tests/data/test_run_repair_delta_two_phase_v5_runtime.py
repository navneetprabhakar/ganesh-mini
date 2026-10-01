from __future__ import annotations

import json
import sys
import types
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_repair_delta_evidence import _semantic_evidence, semantic_projection
from scripts.data.run_repair_delta_evidence import StageInvocationFailure
from scripts.data.run_repair_delta_two_phase import (
    V5_ASSEMBLY_SCHEMA,
    V5_CONTRACT_ID,
    _v5_cached_invocation_replay_eligible,
    load_v5_semantic_dispatch,
    main,
    merge_v5_resilience_semantics,
    prepare_candidate_v5,
)
from tests.data.test_run_repair_delta_two_phase import (
    delta, generated_and_assignment, semantic,
)


def _v5_author(_projection: dict) -> dict:
    return {
        "primary_discrimination": {
            "path": "test_primary.py",
            "content": "from solution import compute_total\nassert compute_total([2, 3]) == 5\nassert compute_total([-2, 3]) == 1\n",
            "case_ids": ["positive", "signed"],
        },
        "cross_cutting": {
            "path": "test_cross.py",
            "content": "from solution import compute_total\ntry:\n compute_total(None)\nexcept TypeError:\n pass\n",
            "case_ids": ["none"],
        },
        "_run_sha256": "2" * 64,
    }


def test_v5_preflight_precedes_carried_semantic_without_new_review(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    generated, assignment = generated_and_assignment()
    assignment["contract_id"] = V5_CONTRACT_ID
    proof = generated["repair_delta_proof"]
    proof["schema_version"] = "ganesh-mini-repair-delta-v4-proof/v1"
    proof["evidence_sha256"] = canonical_sha256({
        key: value for key, value in proof.items() if key != "evidence_sha256"
    })
    calls: list[str] = []
    preflight = {"marker": "v5", "evidence_sha256": ""}
    preflight["evidence_sha256"] = canonical_sha256({"marker": "v5"})

    def fake_preflight(*_args, **_kwargs):
        calls.append("preflight")
        return deepcopy(preflight)

    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.execute_v5_interface_preflight",
        fake_preflight,
    )
    candidate = generated["candidate"]
    response = semantic(semantic_projection(candidate, assignment))
    run_sha = response.pop("_run_sha256")
    carried = _semantic_evidence(candidate, assignment, response, run_sha)

    def forbidden_semantic(_projection):
        raise AssertionError("equivalent V4 review must not trigger a V5 reviewer call")

    artifact = prepare_candidate_v5(
        generated, assignment, forbidden_semantic, _v5_author, delta,
        tmp_path / "runtime.json", tmp_path / "v5.json", tmp_path / "v4.json",
        carried,
    )
    assert calls == ["preflight"]
    assert artifact["status"] == "awaiting-separation"
    assert artifact["pre_separation_execution_scope"] == "v5-interface-preflight-only"
    assert artifact["evidence"]["interface_preflight"] == preflight
    assert artifact["evidence"]["semantic_review"]["reviewer_run_evidence_sha256"] == "1" * 64


def test_v5_semantic_manifest_dispatches_exactly_37_carries_and_23_new(
    tmp_path: Path,
) -> None:
    base_generated, base_assignment = generated_and_assignment()
    generated_rows = []
    assignments = {}
    equivalences = []
    required = []
    for ordinal in range(60):
        generated = deepcopy(base_generated)
        candidate = generated["candidate"]
        identifier = f"candidate-{ordinal:02d}"
        candidate["id"] = identifier
        candidate["verification_task"]["task_id"] = identifier
        candidate["source"]["record_id"] = f"source-{ordinal:02d}"
        assignment = deepcopy(base_assignment)
        assignment.update({
            "id": identifier, "contract_id": V5_CONTRACT_ID,
            "cell_id": f"capability-{ordinal:02d}/python/repair",
            "primary_capability": f"capability-{ordinal:02d}",
            "mode": (
                "fresh-v5-teacher-primary" if ordinal >= 58
                else "immutable-v4-teacher-carry"
            ),
        })
        generated_rows.append(generated)
        assignments[identifier] = assignment
        if ordinal < 37:
            response = semantic({})
            run_sha = response.pop("_run_sha256")
            evidence = _semantic_evidence(candidate, assignment, response, run_sha)
            row = {
                "candidate_id": identifier,
                "candidate_sha256": canonical_sha256(candidate),
                "cell_id": assignment["cell_id"],
                "semantic_projection_sha256": canonical_sha256(
                    semantic_projection(candidate, assignment)
                ),
                "semantic_evidence": evidence,
                "semantic_evidence_sha256": evidence["evidence_sha256"],
            }
            row["equivalence_row_sha256"] = canonical_sha256(row)
            equivalences.append(row)
        else:
            required.append({
                "ordinal": ordinal, "candidate_id": identifier,
                "cell_id": assignment["cell_id"],
                "reason": (
                    "fresh-v5-teacher-primary" if ordinal >= 58
                    else "no-equivalent-v4-review"
                ),
            })
    manifest = {
        "schema_version": "ganesh-mini-gate2-v5-semantic-equivalence-manifest/v1",
        "contract_id": V5_CONTRACT_ID,
        "plan_sha256": "132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b",
        "equivalences": equivalences,
        "equivalences_sha256": canonical_sha256(equivalences),
        "equivalent_reviews": 37,
        "review_required": required,
        "review_required_sha256": canonical_sha256(required),
        "new_reviews_required": 23,
        "evaluation_artifacts_read": 0,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    path = tmp_path / "semantic.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    carried, new = load_v5_semantic_dispatch(path, generated_rows, assignments)
    assert len(carried) == 37
    assert len(new) == 23
    assert set(carried).isdisjoint(new)
    manifest["review_required"].pop()
    manifest["manifest_sha256"] = canonical_sha256({
        key: value for key, value in manifest.items() if key != "manifest_sha256"
    })
    path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="semantic equivalence manifest"):
        load_v5_semantic_dispatch(path, generated_rows, assignments)


def test_v5_interface_failure_uses_v5_terminal_schema(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from scripts.data.repair_delta_v5_preflight import V5PreflightFailure

    generated, assignment = generated_and_assignment()
    assignment["contract_id"] = V5_CONTRACT_ID
    evidence = {"retry_rows": [], "evidence_sha256": canonical_sha256({"retry_rows": []})}

    def fail(*_args, **_kwargs):
        raise V5PreflightFailure("cwd remained unavailable", status="unresolved", evidence=evidence)

    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.execute_v5_interface_preflight", fail,
    )
    artifact = prepare_candidate_v5(
        generated, assignment, semantic, _v5_author, delta,
        tmp_path / "runtime.json", tmp_path / "v5.json", tmp_path / "v4.json",
    )
    assert artifact["schema_version"] == V5_ASSEMBLY_SCHEMA
    assert artifact["status"] == "unresolved"
    assert artifact["terminal_stage"] == "interface_preflight"


def test_v5_stage_invocation_failure_is_candidate_local_terminal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    generated, assignment = generated_and_assignment()
    assignment["contract_id"] = V5_CONTRACT_ID
    proof = generated["repair_delta_proof"]
    proof["schema_version"] = "ganesh-mini-repair-delta-v4-proof/v1"
    proof["evidence_sha256"] = canonical_sha256({
        key: value for key, value in proof.items() if key != "evidence_sha256"
    })
    preflight = {"marker": "v5"}
    preflight["evidence_sha256"] = canonical_sha256(preflight)
    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.execute_v5_interface_preflight",
        lambda *_args, **_kwargs: deepcopy(preflight),
    )
    invocation = {
        "schema_version": "ganesh-mini-repair-delta-v5-stage-invocation-failure/v1",
        "candidate_id": generated["candidate"]["id"], "attempts": [{"raw": "preserved"}],
    }
    invocation["artifact_sha256"] = canonical_sha256(invocation)

    def fail_semantic(_projection):
        raise StageInvocationFailure("provider unavailable", invocation)

    artifact = prepare_candidate_v5(
        generated, assignment, fail_semantic, _v5_author, delta,
        tmp_path / "runtime.json", tmp_path / "v5.json", tmp_path / "v4.json",
    )
    assert artifact["schema_version"] == V5_ASSEMBLY_SCHEMA
    assert artifact["status"] == "unresolved"
    assert artifact["terminal_stage"] == "semantic_review_invocation"
    assert artifact["evidence"]["stage_invocation_failure"] == invocation
    assert artifact["evidence"]["interface_preflight"] == preflight


def test_cached_unresolved_invocation_is_reopened_only_by_eligible_adapter() -> None:
    class Adapter:
        def __init__(self, eligible: bool) -> None:
            self.eligible = eligible
            self.calls = []

        def has_eligible_correction(self, identifier: str) -> bool:
            self.calls.append(identifier)
            return self.eligible

    artifact = {
        "status": "unresolved", "terminal_stage": "semantic_review_invocation",
    }
    eligible = Adapter(True)
    assert _v5_cached_invocation_replay_eligible(artifact, "candidate-1", eligible) is True
    assert eligible.calls == ["candidate-1"]
    assert _v5_cached_invocation_replay_eligible(artifact, "candidate-1", Adapter(False)) is False
    assert _v5_cached_invocation_replay_eligible(
        {**artifact, "status": "terminal-rejected"}, "candidate-1", eligible,
    ) is False


def test_v5_resilience_merge_is_exactly_40_carries_and_20_new() -> None:
    carried = {f"carried-{ordinal}": {"ordinal": ordinal} for ordinal in range(37)}
    required = {f"new-{ordinal}" for ordinal in range(23)}
    interrupted = {f"new-{ordinal}": {"ordinal": ordinal} for ordinal in range(3)}

    merged, remaining = merge_v5_resilience_semantics(carried, required, interrupted)

    assert len(merged) == 40
    assert len(remaining) == 20
    assert set(interrupted) <= set(merged)
    assert set(interrupted).isdisjoint(remaining)
    with pytest.raises(ValueError, match="overlap or differ"):
        merge_v5_resilience_semantics(
            carried, required, {**interrupted, "carried-0": {"ordinal": 99}},
        )
    with pytest.raises(ValueError, match="overlap or differ"):
        merge_v5_resilience_semantics(carried, required, {"new-0": {}})

    five = {f"new-{ordinal}": {"ordinal": ordinal} for ordinal in range(5)}
    merged_v3, remaining_v3 = merge_v5_resilience_semantics(
        carried, required, five, expected_additional=5,
    )
    assert len(merged_v3) == 42
    assert len(remaining_v3) == 18
    assert set(merged_v3).isdisjoint(remaining_v3)


def test_v5_cli_validates_resilience_before_adapter_construction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []
    generated = [{"candidate": {"id": f"candidate-{ordinal}"}} for ordinal in range(60)]
    assignments = {
        f"candidate-{ordinal}": {"id": f"candidate-{ordinal}"} for ordinal in range(60)
    }
    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.load_v5_assembled_inputs",
        lambda *_args, **_kwargs: (generated, assignments, {"manifest_sha256": "a" * 64}),
    )

    def validate_resilience(**kwargs):
        events.append("resilience-validation")
        assert kwargs["composite_readiness_path"] == tmp_path / "composite.json"
        assert kwargs["output_root"] == tmp_path / "primary-two-phase-v2"
        return {f"candidate-{ordinal}": {"evidence_sha256": str(ordinal)} for ordinal in range(3)}

    monkeypatch.setattr(
        "scripts.data.build_v5_resilience_manifests.load_v5_resilience_attempt",
        validate_resilience,
    )
    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.verify_codex_version",
        lambda *_args: "codex-cli 1.2.3",
    )

    class StopAfterAdapter(RuntimeError):
        pass

    def adapter(*_args, **_kwargs):
        events.append("adapter-construction")
        raise StopAfterAdapter

    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.IsolatedCodexAdapter", adapter,
    )
    config = tmp_path / "codex.json"
    config.write_text(json.dumps({"codex_cli_version": "1.2.3"}), encoding="utf-8")
    args = [
        "--contract-version", "v5", "--cohort", "primary",
        "--codex-config", str(config), "--runtime-config", str(tmp_path / "runtime.json"),
        "--training-corpus", str(tmp_path / "train.jsonl"),
        "--evaluation-root", str(tmp_path / "evaluation"),
        "--output-root", str(tmp_path / "primary-two-phase-v2"),
        "--v5-candidates", str(tmp_path / "candidates.jsonl"),
        "--v5-assignments", str(tmp_path / "assignments.jsonl"),
        "--v5-assembly-manifest", str(tmp_path / "assembly.json"),
        "--v5-composite-readiness", str(tmp_path / "composite.json"),
        "--v5-semantic-equivalence", str(tmp_path / "semantic.json"),
        "--v5-resilience-addendum", str(tmp_path / "addendum.md"),
        "--v5-semantic-interruption-carry", str(tmp_path / "carry.json"),
        "--v5-attempt-manifest", str(tmp_path / "attempt.json"),
        "--v5-interruption-report", str(tmp_path / "interruption.json"),
    ]
    with pytest.raises(StopAfterAdapter):
        main(args)
    assert events == ["resilience-validation", "adapter-construction"]


def test_v5_v3_cli_validates_smoke_and_five_carries_before_adapter_without_v2_scan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []
    generated = [{"candidate": {"id": f"candidate-{ordinal}"}} for ordinal in range(60)]
    assignments = {
        f"candidate-{ordinal}": {"id": f"candidate-{ordinal}"} for ordinal in range(60)
    }
    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.load_v5_assembled_inputs",
        lambda *_args, **_kwargs: (generated, assignments, {"manifest_sha256": "a" * 64}),
    )

    def validate_v3(**kwargs):
        events.append("v3-validation")
        assert kwargs["live_smoke_path"] == tmp_path / "live-smoke.json"
        assert kwargs["v2_accounting_path"] == tmp_path / "v2-accounting.json"
        assert kwargs["output_root"] == tmp_path / "primary-two-phase-v3"
        assert all("codex-runs" not in str(value) and "pre-separation" not in str(value)
                   for value in kwargs.values() if isinstance(value, Path))
        return {f"candidate-{ordinal}": {"evidence_sha256": str(ordinal)} for ordinal in range(5)}

    module_name = "scripts.data.build_v5_v3_schema_correction_manifests"
    monkeypatch.setitem(
        sys.modules, module_name,
        types.SimpleNamespace(load_v5_v3_schema_correction_attempt=validate_v3),
    )
    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.verify_codex_version",
        lambda *_args: "codex-cli 1.2.3",
    )

    class StopAfterAdapter(RuntimeError):
        pass

    def adapter(*args, **_kwargs):
        events.append("adapter-construction")
        assert args[3] == tmp_path / "primary-two-phase-v3" / "codex-runs"
        raise StopAfterAdapter

    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.IsolatedCodexAdapter", adapter,
    )
    config = tmp_path / "codex.json"
    config.write_text(json.dumps({"codex_cli_version": "1.2.3"}), encoding="utf-8")
    args = [
        "--contract-version", "v5", "--cohort", "primary",
        "--codex-config", str(config), "--runtime-config", str(tmp_path / "runtime.json"),
        "--training-corpus", str(tmp_path / "train.jsonl"),
        "--evaluation-root", str(tmp_path / "evaluation"),
        "--output-root", str(tmp_path / "primary-two-phase-v3"),
        "--v5-candidates", str(tmp_path / "candidates.jsonl"),
        "--v5-assignments", str(tmp_path / "assignments.jsonl"),
        "--v5-assembly-manifest", str(tmp_path / "assembly.json"),
        "--v5-composite-readiness", str(tmp_path / "composite.json"),
        "--v5-semantic-equivalence", str(tmp_path / "semantic.json"),
        "--v5-semantic-interruption-carry", str(tmp_path / "v2-carry.json"),
        "--v5-attempt-manifest", str(tmp_path / "v2-attempt.json"),
        "--v5-schema-correction-plan", str(tmp_path / "correction.md"),
        "--v5-schema-correction-manifest", str(tmp_path / "correction-manifest.json"),
        "--v5-v2-accounting", str(tmp_path / "v2-accounting.json"),
        "--v5-live-schema-smoke", str(tmp_path / "live-smoke.json"),
        "--v5-v3-semantic-carry", str(tmp_path / "v3-carry.json"),
        "--v5-v3-attempt-manifest", str(tmp_path / "v3-attempt.json"),
    ]
    with pytest.raises(StopAfterAdapter):
        main(args)
    assert events == ["v3-validation", "adapter-construction"]


def test_repository_v5_v3_production_cli_reaches_adapter_only_after_real_startup_gate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = Path(__file__).resolve().parents[2]
    v5 = root / "measurement/gate2/capability-stratified-v5-interface-replay"
    execution = v5 / "cohort-v1/execution-v1"
    v2 = v5 / "primary-two-phase-v2"
    v3 = v5 / "primary-two-phase-v3"
    events: list[str] = []
    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.verify_codex_version",
        lambda *_args: events.append("identity") or "codex-cli 0.116.0",
    )

    class StopAfterGate(RuntimeError):
        pass

    def adapter(*args, **_kwargs):
        events.append("adapter")
        assert args[3] == v3 / "codex-runs"
        raise StopAfterGate

    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.IsolatedCodexAdapter", adapter,
    )
    args = [
        "--contract-version", "v5", "--cohort", "primary",
        "--codex-config", str(root / "configs/data/expansion_teacher.json"),
        "--runtime-config", str(root / "configs/eval/runtimes.json"),
        "--training-corpus", str(tmp_path / "unused-training.jsonl"),
        "--evaluation-root", str(tmp_path / "unused-evaluation"),
        "--output-root", str(v3),
        "--v5-candidates", str(execution / "candidates.jsonl"),
        "--v5-assignments", str(execution / "assignments.jsonl"),
        "--v5-assembly-manifest", str(execution / "manifest.json"),
        "--v5-composite-readiness", str(v5 / "readiness-v1/composite-report.json"),
        "--v5-semantic-equivalence", str(v5 / "cohort-v1/semantic-equivalence.json"),
        "--v5-semantic-interruption-carry", str(v2 / "semantic-interruption-carry-manifest.json"),
        "--v5-attempt-manifest", str(v2 / "attempt-manifest.json"),
        "--v5-schema-correction-plan",
        str(root / "docs/plans/GATE2_V5_SCHEMA_COMPATIBILITY_CORRECTION_20260917.md"),
        "--v5-schema-correction-manifest", str(v3 / "schema-correction-manifest.json"),
        "--v5-v2-accounting", str(v2 / "interruption-accounting.json"),
        "--v5-live-schema-smoke", str(v3 / "readiness-v1/live-schema-admission-smoke.json"),
        "--v5-v3-semantic-carry", str(v3 / "semantic-interruption-carry-manifest.json"),
        "--v5-v3-attempt-manifest", str(v3 / "attempt-manifest.json"),
    ]
    with pytest.raises(StopAfterGate):
        main(args)
    assert events == ["identity", "adapter"]
