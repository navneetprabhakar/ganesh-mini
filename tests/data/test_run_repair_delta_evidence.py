from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_repair_delta_evidence import (
    IsolatedCodexAdapter,
    load_campaign_inputs,
    load_separation_sidecars,
)


def write_primary_inputs(tmp_path: Path, records: int = 60):
    queue = []
    for index in range(120):
        role = "primary" if index < 60 else "reserve"
        cell_index = index if index < 60 else index - 60
        cell = f"cap-{cell_index // 6}/lane-{cell_index % 6}/repair"
        queue.append({
            "id": f"id-{index}", "role": role, "cell_id": cell,
            "contract_id": "capability-stratified-v3-repair-delta/v1",
        })
    queue_path = tmp_path / "queue.jsonl"
    queue_path.write_text("".join(json.dumps(row) + "\n" for row in queue))
    manifest = {
        "schema_version": "ganesh-mini-repair-delta-queue-manifest/v1",
        "plan_sha256": "4023a896300112f9f93f2a16698d549f203e3e75b4e71ae054f3a98463e2f0f0",
        "queue_sha256": hashlib.sha256(queue_path.read_bytes()).hexdigest(), "assignments": 120,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_path = tmp_path / "queue-manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    generated = [{"candidate": {"id": f"id-{index}"}, "repair_delta_proof": {}} for index in range(records)]
    candidate_path = tmp_path / "teacher.jsonl"
    candidate_path.write_text("".join(json.dumps(row) + "\n" for row in generated))
    evidence = {
        "schema_version": "ganesh-mini-repair-delta-teacher-batch/v1",
        "plan_sha256": manifest["plan_sha256"], "queue_manifest_sha256": manifest["manifest_sha256"],
        "role": "primary", "candidate_output_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "requested_ids": [f"id-{index}" for index in range(records)], "generated": records,
        "failures": [], "evaluation_artifacts_read": 0,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    evidence_path = tmp_path / "teacher-evidence.json"
    evidence_path.write_text(json.dumps(evidence))
    return queue_path, manifest_path, candidate_path, evidence_path, manifest


def test_loads_exact_sealed_primary_campaign_and_rejects_cardinality(tmp_path: Path) -> None:
    queue, manifest, candidates, evidence, sealed_manifest = write_primary_inputs(tmp_path)
    generated, assignments, loaded = load_campaign_inputs(
        queue, manifest, [candidates], [evidence], "primary",
    )
    assert len(generated) == len(assignments) == 60
    assert loaded["manifest_sha256"] == sealed_manifest["manifest_sha256"]

    other = tmp_path / "short"
    other.mkdir()
    queue, manifest, candidates, evidence, _ = write_primary_inputs(other, 59)
    with pytest.raises(ValueError, match="exactly all 60"):
        load_campaign_inputs(queue, manifest, [candidates], [evidence], "primary")


def test_teacher_batch_content_drift_and_unpaired_batches_fail_closed(tmp_path: Path) -> None:
    queue, manifest, candidates, evidence, _ = write_primary_inputs(tmp_path)
    with pytest.raises(ValueError, match="pairs"):
        load_campaign_inputs(queue, manifest, [candidates], [], "primary")
    candidates.write_text(candidates.read_text() + "{}\n")
    with pytest.raises(ValueError, match="teacher batch"):
        load_campaign_inputs(queue, manifest, [candidates], [evidence], "primary")


def test_isolated_codex_adapter_seals_and_resumes_exact_projection(tmp_path: Path) -> None:
    config = {"model": "fixture", "codex_cli_version": "fixture"}
    calls = []

    def invoke(binary, config_value, schema_path, prompt, stage, lane):
        calls.append((binary, stage, lane, json.loads(schema_path.read_text())))
        return {
            "repair_delta_requires_primary_capability": True,
            "scheduled_dimension_is_concrete_and_secondary": True,
            "known_bad_already_satisfies_scheduled_dimension": True,
            "cross_dimension_only_patch_cannot_solve": True,
            "capability_remains_substantive_without_cross_clause": True,
            "generic_boilerplate_is_not_primary": True,
            "rationale": "fixture",
        }, {"prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "raw_output": "fixture"}

    projection = {
        "id": "safe-id", "specification": "repair it", "embedded_known_bad": "bad",
        "primary_capability": "numeric", "assigned_cross_cutting_dimension": "malformed",
    }
    with patch("scripts.data.run_repair_delta_evidence.invoke_codex", side_effect=invoke):
        adapter = IsolatedCodexAdapter("semantic_review", config, "codex-fixture", tmp_path, "codex 1")
        first = adapter(projection)
        second = adapter(projection)
    assert first == second and len(calls) == 1
    artifact = json.loads((tmp_path / "safe-id.semantic_review.json").read_text())
    body = dict(artifact); claimed = body.pop("artifact_sha256")
    assert claimed == canonical_sha256(body)
    assert artifact["evaluation_artifacts_read"] == 0

    changed = dict(projection, specification="drift")
    with pytest.raises(ValueError, match="run drift"):
        adapter(changed)


def test_separation_sidecars_are_sealed_and_candidate_bound(tmp_path: Path) -> None:
    candidate = {"id": "safe-id", "value": 1}
    row = {
        "candidate_id": "safe-id", "candidate_sha256": canonical_sha256(candidate),
        "comparison_contract_sha256": "9" * 64,
        "evaluation_artifacts_read_by_construction": 0,
    }
    row["evidence_sha256"] = canonical_sha256(row)
    path = tmp_path / "separation.jsonl"
    path.write_text(json.dumps(row) + "\n")
    lookup = load_separation_sidecars(path, "9" * 64)
    assert lookup(candidate)["evidence_sha256"] == row["evidence_sha256"]
    with pytest.raises(ValueError, match="absent"):
        lookup({"id": "safe-id", "value": 2})
