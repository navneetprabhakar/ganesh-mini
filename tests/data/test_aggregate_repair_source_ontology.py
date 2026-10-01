import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.aggregate_repair_source_ontology import aggregate
from scripts.data.build_capability_corpus_plan import CAPABILITIES, LANES, canonical_sha256
from scripts.data.build_repair_delta_queue import AFFINITY_FIELDS, PLAN_SHA256, canonical_json, ontology_affinity_prompt
from scripts.data.run_repair_source_ontology import CAMPAIGN_SCHEMA, build_row


def source(identifier: str, lane: str, record_id: str | None = None) -> dict:
    return {
        "id": identifier,
        "lane": lane,
        "task_type": "repair",
        "stimulus": f"repair stimulus for {identifier}",
        "source": {
            "dataset": "fixture/dataset",
            "revision": "fixture-revision",
            "record_id": record_id or identifier,
            "source_record_sha256": hashlib.sha256(identifier.encode()).hexdigest(),
        },
    }


def evidence(
    source_row: dict, capability: str, rank: int, separation: str = "a" * 64,
    plan_sha256: str = PLAN_SHA256,
) -> dict:
    verdicts = []
    for name in CAPABILITIES:
        accepted = name == capability
        verdicts.append({
            "primary_capability": name,
            "decision": "accept" if accepted else "reject",
            "capability_operation": "matching operation" if accepted else "unrelated operation",
            "defect_affordance": "matching defect" if accepted else "unrelated defect",
            **{field: accepted for field in AFFINITY_FIELDS},
        })
    item = {"source_queue_id": source_row["id"], "verdicts": verdicts}
    raw_output = json.dumps({"items": [item]}, sort_keys=True)
    run = {"final_output": raw_output, "exit_code": 0}
    run["run_evidence_sha256"] = canonical_sha256(run)
    return build_row(
        source_row, item, ontology_affinity_prompt([source_row]), run,
        {"fixture": True}, "codex fixture", separation, rank, [source_row], plan_sha256,
    )


def write_wave(
    root: Path, name: str, rows: list[dict], *, status: str = "complete",
    failures: list[dict] | None = None, selected: int | None = None,
    separation: str = "a" * 64, plan_sha256: str = PLAN_SHA256,
) -> tuple[Path, Path]:
    evidence_path = root / f"{name}.jsonl"
    payload = b"".join(canonical_json(row) + b"\n" for row in rows)
    evidence_path.write_bytes(payload)
    coverage = {lane: {capability: 0 for capability in CAPABILITIES} for lane in LANES}
    for row in rows:
        for verdict in row["verdicts"]:
            if verdict["decision"] == "accept":
                coverage[row["lane"]][verdict["primary_capability"]] += 1
    summary = {
        "schema_version": CAMPAIGN_SCHEMA,
        "plan_sha256": plan_sha256,
        "status": status,
        "selected": selected if selected is not None else len(rows),
        "completed": len(rows),
        "failures": failures or [],
        "coverage": coverage,
        "output_sha256": hashlib.sha256(payload).hexdigest(),
        "offset": 0,
        "per_lane": 1,
        "batch_size": 1,
        "separation_attestation_sha256": separation,
        "evaluation_artifacts_read": 0,
    }
    summary["summary_sha256"] = canonical_sha256(summary)
    summary_path = root / f"{name}-summary.json"
    summary_path.write_text(json.dumps(summary, sort_keys=True) + "\n", encoding="utf-8")
    return evidence_path, summary_path


def write_sources(path: Path, rows: list[dict]) -> None:
    path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))


def test_combines_waves_preserves_failed_manifest_and_reports_complete_cells(tmp_path: Path) -> None:
    sources = []
    first_rows = []
    second_rows = []
    rank = 0
    for lane in LANES:
        for capability in CAPABILITIES:
            for copy_index in range(2):
                row = source(f"{lane}-{capability}-{copy_index}", lane)
                sources.append(row)
                target = first_rows if copy_index == 0 else second_rows
                target.append(evidence(row, capability, rank))
                rank += 1
    source_path = tmp_path / "sources.jsonl"
    write_sources(source_path, sources)
    failed = [{"source_queue_ids": ["failed-source"], "reason": "fixture failure"}]
    wave1 = write_wave(tmp_path, "wave-1", first_rows, status="failed", failures=failed, selected=len(first_rows) + 1)
    wave2 = write_wave(tmp_path, "wave-2", second_rows)

    rows, summary = aggregate(source_path, [wave1, wave2])

    assert len(rows) == 120
    assert summary["status"] == "coverage-complete"
    assert summary["coverage"]["all_cells_meet_minimum"] is True
    assert summary["coverage"]["cells_meeting_minimum"] == 60
    assert summary["failed_wave_count"] == 1
    assert summary["waves"][0]["campaign_manifest"]["failures"] == failed
    assert all(value["cells_meeting_minimum"] == 10 for value in summary["coverage"]["by_lane"].values())
    assert all(value["cells_meeting_minimum"] == 6 for value in summary["coverage"]["by_capability"].values())


def test_rejects_duplicate_source_id_across_waves(tmp_path: Path) -> None:
    row = source("source-1", "python")
    source_path = tmp_path / "sources.jsonl"; write_sources(source_path, [row])
    value = evidence(row, "numeric_reasoning", 0)
    wave1 = write_wave(tmp_path, "wave-1", [value])
    wave2 = write_wave(tmp_path, "wave-2", [value])
    with pytest.raises(ValueError, match="duplicate source queue ID"):
        aggregate(source_path, [wave1, wave2])


def test_combines_waves_bound_to_different_separation_attestations(tmp_path: Path) -> None:
    first = source("source-1", "python")
    second = source("source-2", "python")
    source_path = tmp_path / "sources.jsonl"; write_sources(source_path, [first, second])
    first_sha = "a" * 64
    second_sha = "b" * 64
    wave1 = write_wave(
        tmp_path, "wave-1", [evidence(first, "numeric_reasoning", 0, first_sha)], separation=first_sha,
    )
    wave2 = write_wave(
        tmp_path, "wave-2", [evidence(second, "numeric_reasoning", 1, second_sha)], separation=second_sha,
    )

    rows, summary = aggregate(source_path, [wave1, wave2])

    assert len(rows) == 2
    assert summary["separation_attestation_sha256s"] == [first_sha, second_sha]
    assert [row["separation_attestation_sha256"] for row in rows] == [first_sha, second_sha]


def test_rejects_wave_row_bound_to_different_attestation_than_summary(tmp_path: Path) -> None:
    row = source("source-1", "python")
    source_path = tmp_path / "sources.jsonl"; write_sources(source_path, [row])
    wave = write_wave(
        tmp_path, "wave", [evidence(row, "numeric_reasoning", 0, "b" * 64)], separation="a" * 64,
    )
    with pytest.raises(ValueError, match="incomplete or unsealed"):
        aggregate(source_path, [wave])


def test_rejects_duplicate_lineage_under_different_ids(tmp_path: Path) -> None:
    first = source("source-1", "python", "same-record")
    second = source("source-2", "python", "same-record")
    source_path = tmp_path / "sources.jsonl"; write_sources(source_path, [first, second])
    wave1 = write_wave(tmp_path, "wave-1", [evidence(first, "numeric_reasoning", 0)])
    wave2 = write_wave(tmp_path, "wave-2", [evidence(second, "numeric_reasoning", 1)])
    with pytest.raises(ValueError, match="duplicate source lineage"):
        aggregate(source_path, [wave1, wave2])


@pytest.mark.parametrize("mutation", ["evidence_seal", "source_binding", "batch_binding", "summary_seal"])
def test_tampering_fails_closed(tmp_path: Path, mutation: str) -> None:
    row = source("source-1", "python")
    source_path = tmp_path / "sources.jsonl"; write_sources(source_path, [row])
    value = evidence(row, "numeric_reasoning", 0)
    if mutation == "evidence_seal":
        value["lane"] = "rust"
    elif mutation == "source_binding":
        value["source_record_sha256"] = "f" * 64
        body = dict(value); body.pop("evidence_sha256")
        value["evidence_sha256"] = canonical_sha256(body)
    elif mutation == "batch_binding":
        value["batch_source_records_sha256"] = "f" * 64
        body = dict(value); body.pop("evidence_sha256")
        value["evidence_sha256"] = canonical_sha256(body)
    wave = write_wave(tmp_path, "wave", [value])
    if mutation == "summary_seal":
        summary = json.loads(wave[1].read_text(encoding="utf-8"))
        summary["completed"] = 2
        wave[1].write_text(json.dumps(summary), encoding="utf-8")
    with pytest.raises(ValueError):
        aggregate(source_path, [wave])


def test_rejects_partial_successful_batch(tmp_path: Path) -> None:
    first = source("source-1", "python")
    second = source("source-2", "python")
    value = evidence(first, "numeric_reasoning", 0)
    value["batch_source_queue_ids"] = [first["id"], second["id"]]
    value["batch_source_records_sha256"] = canonical_sha256([first, second])
    prompt = ontology_affinity_prompt([first, second])
    value["raw_prompt"] = prompt
    value["prompt_sha256"] = hashlib.sha256(prompt.encode()).hexdigest()
    second_item = json.loads(evidence(second, "numeric_reasoning", 1)["raw_output"])["items"][0]
    output = json.dumps({"items": [json.loads(value["raw_output"])["items"][0], second_item]}, sort_keys=True)
    value["raw_output"] = output; value["output_sha256"] = hashlib.sha256(output.encode()).hexdigest()
    value["run_evidence"] = {"final_output": output, "exit_code": 0}
    value["run_evidence"]["run_evidence_sha256"] = canonical_sha256(value["run_evidence"])
    value["runtime_parameters"]["run_evidence_sha256"] = value["run_evidence"]["run_evidence_sha256"]
    body = dict(value); body.pop("evidence_sha256")
    value["evidence_sha256"] = canonical_sha256(body)
    source_path = tmp_path / "sources.jsonl"; write_sources(source_path, [first, second])
    wave = write_wave(tmp_path, "wave", [value])
    with pytest.raises(ValueError, match="partial successful batch"):
        aggregate(source_path, [wave])


def test_v4_carries_sealed_v3_aggregate_and_merges_new_wave(tmp_path: Path) -> None:
    v4_plan = "b" * 64
    old = source("v3-source", "python")
    new = source("v4-source", "python")
    predecessor_queue = tmp_path / "v3-sources.jsonl"; write_sources(predecessor_queue, [old])
    predecessor_wave = write_wave(
        tmp_path, "v3-wave", [evidence(old, "numeric_reasoning", 0)],
    )
    carried_rows, carried_summary = aggregate(predecessor_queue, [predecessor_wave])
    carried_evidence = tmp_path / "v3-final-evidence.jsonl"; write_sources(carried_evidence, carried_rows)
    carried_summary_path = tmp_path / "v3-final-summary.json"
    carried_summary_path.write_text(json.dumps(carried_summary, sort_keys=True) + "\n", encoding="utf-8")

    union_queue = tmp_path / "v4-union.jsonl"; write_sources(union_queue, [old, new])
    v4_wave = write_wave(
        tmp_path, "v4-wave", [evidence(new, "numeric_reasoning", 1, "c" * 64, v4_plan)],
        separation="c" * 64, plan_sha256=v4_plan,
    )
    rows, summary = aggregate(
        union_queue, [v4_wave], v4_plan, (PLAN_SHA256,),
        ((carried_evidence, carried_summary_path, predecessor_queue),),
    )

    assert [row["source_queue_id"] for row in rows] == ["v3-source", "v4-source"]
    assert summary["plan_sha256"] == v4_plan
    assert summary["compatible_plan_sha256s"] == [PLAN_SHA256]
    assert summary["carry_forward_count"] == 1
    assert summary["carry_forwards"][0]["aggregate_sha256"] == carried_summary["aggregate_sha256"]
    assert summary["coverage"]["cells"]["numeric_reasoning/python/repair"]["accepted_unique_sources"] == 2


def test_v4_carry_forward_requires_explicit_compatibility_and_exact_union_binding(tmp_path: Path) -> None:
    v4_plan = "b" * 64
    old = source("v3-source", "python")
    new = source("v4-source", "python")
    predecessor_queue = tmp_path / "v3-sources.jsonl"; write_sources(predecessor_queue, [old])
    predecessor_wave = write_wave(tmp_path, "v3-wave", [evidence(old, "numeric_reasoning", 0)])
    carried_rows, carried_summary = aggregate(predecessor_queue, [predecessor_wave])
    carried_evidence = tmp_path / "v3-final-evidence.jsonl"; write_sources(carried_evidence, carried_rows)
    carried_summary_path = tmp_path / "v3-final-summary.json"
    carried_summary_path.write_text(json.dumps(carried_summary) + "\n", encoding="utf-8")
    union_queue = tmp_path / "v4-union.jsonl"; write_sources(union_queue, [old, new])
    v4_wave = write_wave(
        tmp_path, "v4-wave", [evidence(new, "numeric_reasoning", 1, "c" * 64, v4_plan)],
        separation="c" * 64, plan_sha256=v4_plan,
    )

    with pytest.raises(ValueError, match="carry-forward is invalid"):
        aggregate(
            union_queue, [v4_wave], v4_plan, (),
            ((carried_evidence, carried_summary_path, predecessor_queue),),
        )

    changed = deepcopy(old); changed["stimulus"] = "changed carried stimulus"
    write_sources(union_queue, [changed, new])
    with pytest.raises(ValueError, match="incomplete or unsealed"):
        aggregate(
            union_queue, [v4_wave], v4_plan, (PLAN_SHA256,),
            ((carried_evidence, carried_summary_path, predecessor_queue),),
        )


def test_v4_carry_forward_rejects_tampered_aggregate_summary(tmp_path: Path) -> None:
    v4_plan = "b" * 64
    old = source("v3-source", "python")
    new = source("v4-source", "python")
    predecessor_queue = tmp_path / "v3-sources.jsonl"; write_sources(predecessor_queue, [old])
    predecessor_wave = write_wave(tmp_path, "v3-wave", [evidence(old, "numeric_reasoning", 0)])
    carried_rows, carried_summary = aggregate(predecessor_queue, [predecessor_wave])
    carried_evidence = tmp_path / "v3-final-evidence.jsonl"; write_sources(carried_evidence, carried_rows)
    carried_summary["unique_sources"] = 2
    carried_summary_path = tmp_path / "v3-final-summary.json"
    carried_summary_path.write_text(json.dumps(carried_summary) + "\n", encoding="utf-8")
    union_queue = tmp_path / "v4-union.jsonl"; write_sources(union_queue, [old, new])
    v4_wave = write_wave(
        tmp_path, "v4-wave", [evidence(new, "numeric_reasoning", 1, "c" * 64, v4_plan)],
        separation="c" * 64, plan_sha256=v4_plan,
    )
    with pytest.raises(ValueError, match="carry-forward is invalid"):
        aggregate(
            union_queue, [v4_wave], v4_plan, (PLAN_SHA256,),
            ((carried_evidence, carried_summary_path, predecessor_queue),),
        )
