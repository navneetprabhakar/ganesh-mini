import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.build_repair_delta_queue import (
    AFFINITY_FIELDS,
    PLAN_SHA256,
    QUALIFICATION_DATASETS,
    affinity_prompt,
    build,
    canonical_json,
    load_affinity,
    load_separation_bindings,
    load_v4_affinity_aggregate_context,
    match_two_slot_sources,
    ontology_affinity_prompt,
    repair_cells,
    source_key,
    V4_CONTRACT_ID,
    V4_PLAN_SHA256,
    V4_SEED,
)
from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))


def fixture(tmp_path: Path):
    sources = []
    affinity = []
    for cell in repair_cells():
        for ordinal in range(2):
            dataset = QUALIFICATION_DATASETS[ordinal]
            source_id = f"source-{cell['primary_capability']}-{cell['lane']}-{ordinal}"
            source = {
                "id": source_id, "lane": cell["lane"], "task_type": "repair",
                "source": {"dataset": dataset, "revision": "rev", "record_id": source_id,
                           "source_record_sha256": hashlib.sha256(source_id.encode()).hexdigest()},
                "stimulus": f"repair code for {cell['primary_capability']}",
            }
            sources.append(source)
            raw_output = json.dumps({"decision": "accept", "operation": "concrete", "defect": "concrete"})
            evidence = {
                "schema_version": "ganesh-mini-repair-source-affinity/v1",
                "source_queue_id": source_id, "cell_id": cell["cell_id"], "decision": "accept",
                "selection_rank": ordinal,
                **{field: True for field in AFFINITY_FIELDS},
                "capability_operation": "a concrete operation", "defect_affordance": "a concrete defect",
                "source_record_sha256": source["source"]["source_record_sha256"],
                "stimulus_sha256": hashlib.sha256(source["stimulus"].encode()).hexdigest(),
                "prompt_sha256": hashlib.sha256(affinity_prompt(cell, source).encode()).hexdigest(),
                "raw_output": raw_output, "output_sha256": hashlib.sha256(raw_output.encode()).hexdigest(),
                "runtime_parameters": {"model": "fixture"},
                "separation_attestation_sha256": "PLACEHOLDER", "evaluation_artifacts_read": 0,
            }
            affinity.append(evidence)
    source_path = tmp_path / "sources.jsonl"; write_jsonl(source_path, sources)
    separation = {
        "source_queue_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "exact_normalized_fuzzy_exclusion_complete": True, "evaluation_content_exposed": False,
        "eligible_source_queue_ids": [row["id"] for row in sources],
    }
    separation["attestation_sha256"] = canonical_sha256(separation)
    separation_path = tmp_path / "separation.json"; separation_path.write_text(json.dumps(separation))
    for evidence in affinity:
        evidence["separation_attestation_sha256"] = separation["attestation_sha256"]
        evidence["evidence_sha256"] = canonical_sha256(evidence)
    affinity_path = tmp_path / "affinity.jsonl"; write_jsonl(affinity_path, affinity)
    prior = tmp_path / "prior.jsonl"; write_jsonl(prior, [])
    v2 = tmp_path / "v2.jsonl"; write_jsonl(v2, [])
    plan = Path(__file__).resolve().parents[2] / "docs/plans/GATE2_REPAIR_DELTA_QUALIFICATION_PLAN_20260914.md"
    return plan, source_path, prior, v2, separation_path, affinity_path


def test_builds_60_primaries_and_60_cell_bound_reserves(tmp_path: Path) -> None:
    args = fixture(tmp_path)
    rows, manifest = build(args[0], args[1], args[2], [args[3]], args[4], args[5])
    assert len(rows) == 120
    assert sum(row["role"] == "primary" for row in rows) == 60
    assert sum(row["role"] == "reserve" for row in rows) == 60
    assert len({row["cell_id"] for row in rows}) == 60
    assert len({(row["source"]["dataset"], row["source"]["record_id"]) for row in rows}) == 120
    assert all(row["generation_eligible"] == (row["role"] == "primary") for row in rows)
    assert manifest["absolute_candidate_budget"] == 66
    assert manifest["maximum_reserve_generation_eligible"] == 6
    assert manifest["approved_source_datasets"] == list(QUALIFICATION_DATASETS)
    assert manifest["dataset_counts"] == {
        "primary": {"Multilingual-Multimodal-NLP/McEval-Instruct": 30, "m-a-p/MdEval-Instruct": 30},
        "reserve": {"Multilingual-Multimodal-NLP/McEval-Instruct": 30, "m-a-p/MdEval-Instruct": 30},
    }


def test_queue_and_manifest_are_deterministic_and_sealed(tmp_path: Path) -> None:
    args = fixture(tmp_path)
    first, manifest = build(args[0], args[1], args[2], [args[3]], args[4], args[5])
    second, repeated = build(args[0], args[1], args[2], [args[3]], args[4], args[5])
    assert first == second and manifest == repeated
    payload = b"".join(canonical_json(row) + b"\n" for row in first)
    assert manifest["queue_sha256"] == hashlib.sha256(payload).hexdigest()
    seal = manifest.pop("manifest_sha256")
    assert seal == canonical_sha256(manifest)


def test_v4_selection_uses_distinct_plan_contract_seed_and_schemas(tmp_path: Path) -> None:
    args = fixture(tmp_path)
    v4_plan = Path(__file__).resolve().parents[2] / "docs/plans/GATE2_REPAIR_DELTA_V4_QUALIFICATION_PLAN_20260916.md"
    assert hashlib.sha256(v4_plan.read_bytes()).hexdigest() == V4_PLAN_SHA256

    affinity_rows = [json.loads(line) for line in args[5].read_text().splitlines()]
    separation = json.loads(args[4].read_text())
    affinity_summary = tmp_path / "affinity-summary.json"
    summary = {
        "schema_version": "ganesh-mini-repair-source-ontology-aggregate/v1",
        "plan_sha256": V4_PLAN_SHA256, "compatible_plan_sha256s": [],
        "status": "coverage-complete",
        "source_queue_sha256": hashlib.sha256(args[1].read_bytes()).hexdigest(),
        "separation_attestation_sha256s": [separation["attestation_sha256"]],
        "unique_sources": len({row["source_queue_id"] for row in affinity_rows}),
        "combined_evidence_sha256": hashlib.sha256(args[5].read_bytes()).hexdigest(),
        "evaluation_artifacts_read": 0,
    }
    summary["aggregate_sha256"] = canonical_sha256(summary)
    affinity_summary.write_text(json.dumps(summary), encoding="utf-8")

    rows, manifest = build(
        v4_plan, args[1], args[2], [args[3]], args[4], args[5],
        contract_version="v4", affinity_summary_path=affinity_summary,
        tooling_readiness_sha256="b" * 64,
    )

    assert all(row["contract_id"] == V4_CONTRACT_ID for row in rows)
    assert all(row["schema_version"] == "ganesh-mini-repair-delta-v4-assignment/v1" for row in rows)
    assert all(row["id"].startswith("cap-v4-") for row in rows)
    assert manifest["schema_version"] == "ganesh-mini-repair-delta-v4-queue-manifest/v1"
    assert manifest["plan_sha256"] == V4_PLAN_SHA256
    assert manifest["contract_id"] == V4_CONTRACT_ID
    assert manifest["contract_version"] == "v4"
    assert manifest["seed"] == V4_SEED
    assert manifest["inputs"]["affinity_aggregate"]["aggregate_sha256"] == summary["aggregate_sha256"]
    assert manifest["inputs"]["tooling_readiness_report_sha256"] == "b" * 64

    with pytest.raises(ValueError, match="v4 plan hash mismatch"):
        build(
            args[0], args[1], args[2], [args[3]], args[4], args[5],
            contract_version="v4", affinity_summary_path=affinity_summary,
        )


def test_v4_build_requires_sealed_affinity_aggregate_summary(tmp_path: Path) -> None:
    args = fixture(tmp_path)
    v4_plan = Path(__file__).resolve().parents[2] / "docs/plans/GATE2_REPAIR_DELTA_V4_QUALIFICATION_PLAN_20260916.md"
    with pytest.raises(ValueError, match="sealed affinity aggregate summary"):
        build(
            v4_plan, args[1], args[2], [args[3]], args[4], args[5],
            contract_version="v4", tooling_readiness_sha256="b" * 64,
        )


def test_v4_build_requires_validated_tooling_readiness_seal(tmp_path: Path) -> None:
    args = fixture(tmp_path)
    v4_plan = Path(__file__).resolve().parents[2] / "docs/plans/GATE2_REPAIR_DELTA_V4_QUALIFICATION_PLAN_20260916.md"
    with pytest.raises(ValueError, match="tooling-readiness"):
        build(v4_plan, args[1], args[2], [args[3]], args[4], args[5], contract_version="v4")


def test_ontology_prompt_preserves_native_form_and_exposes_projected_derivation() -> None:
    native = {
        "id": "native", "lane": "javascript", "task_type": "repair", "stimulus": "fix it",
        "source": {"dataset": "dataset", "revision": "revision", "record_id": "record",
                   "source_record_sha256": "a" * 64, "transformation": "native transformation"},
    }
    expected_native_visible = [{
        "source_queue_id": "native", "lane": "javascript", "task_type": "repair", "stimulus": "fix it",
        "source_lineage": {"dataset": "dataset", "revision": "revision", "record_id": "record",
                           "source_record_sha256": "a" * 64},
    }]
    native_prompt = ontology_affinity_prompt([native])
    expected_native_prompt = f"""Classify each training-only repair stimulus independently against every capability. Do not use tools or inspect files.
Capability ontology: {json.dumps(CAPABILITIES, separators=(',', ':'), sort_keys=True)}
Inputs: {json.dumps(expected_native_visible, separators=(',', ':'), ensure_ascii=False)}

For every input return exactly one verdict for every ontology capability. Multiple capabilities may pass. Accept a
capability only when the stimulus contains that capability-specific operation plus an identifiable defect affordance,
can become one self-contained standard-library-only source file, is actual code-repair material, and requires no
filesystem, network, clock, randomness, installation, external dependency, framework, or service. For a rejection,
set each boolean independently and explain the actual operation and defect affordance (or their absence). Do not force
the source into a capability. Return only the fixed structured contract. Evaluation separation is handled elsewhere."""
    assert native_prompt == expected_native_prompt
    assert "source_language" not in native_prompt

    projected = {
        **native, "id": "projected", "lane": "typescript", "source_language": "javascript",
        "target_lane": "typescript", "original_role": "generation",
        "derivation_kind": "cross_language_repair_fallback",
        "source": {**native["source"], "transformation": "verbatim JS projected to TypeScript repair"},
    }
    prompt = ontology_affinity_prompt([projected])
    assert '"source_language":"javascript"' in prompt
    assert '"target_lane":"typescript"' in prompt
    assert '"original_role":"generation"' in prompt
    assert '"derivation_kind":"cross_language_repair_fallback"' in prompt
    assert '"transformation":"verbatim JS projected to TypeScript repair"' in prompt


def test_ontology_prompt_rejects_partial_projected_metadata() -> None:
    source = {
        "id": "partial", "lane": "typescript", "task_type": "repair", "stimulus": "fix it",
        "source_language": "javascript",
        "source": {"dataset": "dataset", "revision": "revision", "record_id": "record",
                   "source_record_sha256": "a" * 64, "transformation": "projection"},
    }
    with pytest.raises(ValueError, match="incomplete derivation metadata"):
        ontology_affinity_prompt([source])


def test_unsealed_affinity_evidence_fails_closed(tmp_path: Path) -> None:
    args = fixture(tmp_path)
    rows = [json.loads(line) for line in args[5].read_text().splitlines()]
    rows[0]["capability_operation_present"] = False
    write_jsonl(args[5], rows)
    try:
        build(args[0], args[1], args[2], [args[3]], args[4], args[5])
    except ValueError as exc:
        assert "affinity" in str(exc)
    else:
        raise AssertionError("modified affinity evidence must fail")


def test_source_key_reads_v2_admission_envelope_lineage() -> None:
    envelope = {
        "candidate": {
            "source": {"dataset": "dataset", "revision": "revision", "record_id": "record"},
        },
        "qualification": {"source_queue_id": "source-queue-id"},
    }
    assert source_key(envelope) == ("dataset", "revision", "record")


def write_attestation(path: Path, source_path: Path, eligible_ids: list[str]) -> str:
    value = {
        "source_queue_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "exact_normalized_fuzzy_exclusion_complete": True,
        "evaluation_content_exposed": False,
        "eligible_source_queue_ids": eligible_ids,
    }
    value["attestation_sha256"] = canonical_sha256(value)
    path.write_text(json.dumps(value), encoding="utf-8")
    return value["attestation_sha256"]


def test_build_accepts_multiple_exact_source_separation_bindings(tmp_path: Path) -> None:
    args = fixture(tmp_path)
    source_rows = [json.loads(line) for line in args[1].read_text().splitlines()]
    first_rows = source_rows[::2]
    second_rows = source_rows[1::2]
    first_queue = tmp_path / "first-source-snapshot.jsonl"; write_jsonl(first_queue, first_rows)
    second_queue = tmp_path / "second-source-snapshot.jsonl"; write_jsonl(second_queue, second_rows)
    first_attestation = tmp_path / "first-attestation.json"
    second_attestation = tmp_path / "second-attestation.json"
    first_sha = write_attestation(first_attestation, first_queue, [row["id"] for row in first_rows])
    second_sha = write_attestation(second_attestation, second_queue, [row["id"] for row in second_rows])
    first_ids = {row["id"] for row in first_rows}
    affinity_rows = [json.loads(line) for line in args[5].read_text().splitlines()]
    for row in affinity_rows:
        row["separation_attestation_sha256"] = first_sha if row["source_queue_id"] in first_ids else second_sha
        row.pop("evidence_sha256")
        row["evidence_sha256"] = canonical_sha256(row)
    write_jsonl(args[5], affinity_rows)

    rows, manifest = build(
        args[0], args[1], args[2], [args[3]],
        [(first_attestation, first_queue), (second_attestation, second_queue)], args[5],
    )

    assert len(rows) == 120
    assert {row["source_separation_attestation_sha256"] for row in rows} == {first_sha, second_sha}
    assert [item["attestation_sha256"] for item in manifest["inputs"]["separation_bindings"]] == [
        first_sha, second_sha,
    ]


def test_separation_binding_rejects_nonidentical_final_queue_superset(tmp_path: Path) -> None:
    first = ontology_source("source-1")
    bound_queue = tmp_path / "bound.jsonl"; write_jsonl(bound_queue, [first])
    attestation = tmp_path / "attestation.json"
    write_attestation(attestation, bound_queue, [first["id"]])
    modified = deepcopy(first); modified["stimulus"] = "changed after separation"
    with pytest.raises(ValueError, match="changed or omitted an eligible bound repair row"):
        load_separation_bindings([(attestation, bound_queue)], {modified["id"]: modified})


def test_separation_binding_allows_and_records_non_repair_only_differences(tmp_path: Path) -> None:
    repair = ontology_source("repair-source")
    generation = deepcopy(ontology_source("generation-source")); generation["task_type"] = "generation"
    bound_queue = tmp_path / "bound.jsonl"; write_jsonl(bound_queue, [repair, generation])
    attestation = tmp_path / "attestation.json"
    attestation_sha256 = write_attestation(attestation, bound_queue, [repair["id"], generation["id"]])
    changed_generation = deepcopy(generation); changed_generation["stimulus"] = "generation-only drift"

    eligibility, manifests = load_separation_bindings(
        [(attestation, bound_queue)],
        {repair["id"]: repair, changed_generation["id"]: changed_generation},
    )

    assert eligibility == {attestation_sha256: {repair["id"]}}
    assert manifests[0]["bound_repair_projection_count"] == 1
    repair_payload = canonical_json(repair) + b"\n"
    assert manifests[0]["bound_repair_projection_sha256"] == hashlib.sha256(repair_payload).hexdigest()
    assert manifests[0]["bound_non_repair_projection_count"] == 1
    assert manifests[0]["non_repair_changed_or_colliding_count"] == 1
    assert manifests[0]["non_repair_missing_from_final_count"] == 0
    assert manifests[0]["non_repair_difference_count"] == 1


def test_separation_binding_allows_and_records_missing_non_repair_row(tmp_path: Path) -> None:
    repair = ontology_source("repair-source")
    generation = deepcopy(ontology_source("generation-source")); generation["task_type"] = "generation"
    bound_queue = tmp_path / "bound.jsonl"; write_jsonl(bound_queue, [repair, generation])
    attestation = tmp_path / "attestation.json"
    write_attestation(attestation, bound_queue, [repair["id"], generation["id"]])

    _eligibility, manifests = load_separation_bindings(
        [(attestation, bound_queue)], {repair["id"]: repair},
    )

    assert manifests[0]["non_repair_missing_from_final_count"] == 1
    assert manifests[0]["non_repair_changed_or_colliding_count"] == 0
    assert manifests[0]["non_repair_difference_count"] == 1


def test_separation_binding_rejects_missing_eligible_repair_row(tmp_path: Path) -> None:
    repair = ontology_source("repair-source")
    bound_queue = tmp_path / "bound.jsonl"; write_jsonl(bound_queue, [repair])
    attestation = tmp_path / "attestation.json"
    write_attestation(attestation, bound_queue, [repair["id"]])
    with pytest.raises(ValueError, match="changed or omitted an eligible bound repair row"):
        load_separation_bindings([(attestation, bound_queue)], {})


def test_affinity_rejects_source_not_eligible_under_its_claimed_attestation(tmp_path: Path) -> None:
    source = ontology_source("source-1")
    row = ontology_row(source, [source], "a" * 64)
    path = tmp_path / "ontology.jsonl"; write_jsonl(path, [row])
    with pytest.raises(ValueError, match="ontology evidence"):
        load_affinity(path, {"a" * 64: set()}, {source["id"]: source})


def ontology_source(identifier: str) -> dict:
    stimulus = f"repair the bounded operation in {identifier}"
    return {
        "id": identifier, "lane": "python", "task_type": "repair", "stimulus": stimulus,
        "source": {
            "dataset": "m-a-p/MdEval-Instruct", "revision": "rev", "record_id": identifier,
            "source_record_sha256": hashlib.sha256(identifier.encode()).hexdigest(),
        },
    }


def ontology_row(source: dict, batch: list[dict], separation_sha256: str) -> dict:
    verdicts = []
    from scripts.data.build_capability_corpus_plan import CAPABILITIES

    for capability in CAPABILITIES:
        verdicts.append({
            "primary_capability": capability, "decision": "accept",
            "capability_operation": f"operation for {capability}", "defect_affordance": "one defect",
            **{field: True for field in AFFINITY_FIELDS},
        })
    prompt = ontology_affinity_prompt(batch)
    raw_output = json.dumps({"items": []})
    value = {
        "schema_version": "ganesh-mini-repair-source-ontology/v1", "plan_sha256": PLAN_SHA256,
        "source_queue_id": source["id"], "lane": source["lane"], "selection_rank": 0,
        "source_identity": {key: source["source"][key] for key in ("dataset", "revision", "record_id")},
        "source_record_sha256": source["source"]["source_record_sha256"],
        "stimulus_sha256": hashlib.sha256(source["stimulus"].encode()).hexdigest(),
        "batch_source_queue_ids": [row["id"] for row in batch],
        "batch_source_records_sha256": canonical_sha256(batch), "verdicts": verdicts,
        "raw_prompt": prompt, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "raw_output": raw_output, "output_sha256": hashlib.sha256(raw_output.encode()).hexdigest(),
        "runtime_parameters": {"model": "fixture"}, "run_evidence": {},
        "separation_attestation_sha256": separation_sha256, "evaluation_artifacts_read": 0,
    }
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def test_loads_full_ontology_evidence_and_binds_source_to_batch(tmp_path: Path) -> None:
    separation_sha256 = "a" * 64
    first, second = ontology_source("source-1"), ontology_source("source-2")
    path = tmp_path / "ontology.jsonl"
    row = ontology_row(first, [first], separation_sha256)
    write_jsonl(path, [row])
    loaded = load_affinity(path, separation_sha256, {first["id"]: first, second["id"]: second})
    assert len(loaded) == 10
    assert all(key[1] == first["id"] for key in loaded)
    assert all(value["classification_mode"] == "full_ontology" for value in loaded.values())

    mismatched = ontology_row(first, [second], separation_sha256)
    write_jsonl(path, [mismatched])
    with pytest.raises(ValueError, match="ontology evidence"):
        load_affinity(path, separation_sha256, {first["id"]: first, second["id"]: second})


def test_loads_cross_lane_ontology_batch_with_exact_prompt_binding(tmp_path: Path) -> None:
    separation_sha256 = "b" * 64
    first, second = ontology_source("source-python"), ontology_source("source-go")
    second["lane"] = "go"
    path = tmp_path / "ontology.jsonl"
    batch = [first, second]
    write_jsonl(path, [
        ontology_row(first, batch, separation_sha256),
        ontology_row(second, batch, separation_sha256),
    ])
    loaded = load_affinity(path, separation_sha256, {first["id"]: first, second["id"]: second})
    assert len(loaded) == 20
    assert ("associative_aggregation/go/repair", second["id"]) in loaded


def test_v4_mixed_plan_affinity_validates_then_ignores_excluded_v3_source(tmp_path: Path) -> None:
    separation_sha256 = "c" * 64
    carried = ontology_source("carried-v3-source")
    fresh = ontology_source("fresh-v4-source")
    carried_row = ontology_row(carried, [carried], separation_sha256)
    fresh_row = ontology_row(fresh, [fresh], separation_sha256)
    fresh_row["plan_sha256"] = V4_PLAN_SHA256
    fresh_row.pop("evidence_sha256")
    fresh_row["evidence_sha256"] = canonical_sha256(fresh_row)
    path = tmp_path / "mixed-affinity.jsonl"
    write_jsonl(path, [carried_row, fresh_row])
    sources = {row["id"]: row for row in (carried, fresh)}

    loaded = load_affinity(
        path, separation_sha256, sources, plan_sha256=V4_PLAN_SHA256,
        allowed_plan_sha256s={PLAN_SHA256, V4_PLAN_SHA256},
        candidate_source_ids={fresh["id"]},
    )

    assert len(loaded) == len(CAPABILITIES)
    assert {source_id for _cell_id, source_id in loaded} == {fresh["id"]}

    carried_row["stimulus_sha256"] = "0" * 64
    carried_row.pop("evidence_sha256")
    carried_row["evidence_sha256"] = canonical_sha256(carried_row)
    write_jsonl(path, [carried_row, fresh_row])
    with pytest.raises(ValueError, match="ontology evidence"):
        load_affinity(
            path, separation_sha256, sources, plan_sha256=V4_PLAN_SHA256,
            allowed_plan_sha256s={PLAN_SHA256, V4_PLAN_SHA256},
            candidate_source_ids={fresh["id"]},
        )


def test_v4_affinity_context_requires_explicit_sealed_v3_compatibility(tmp_path: Path) -> None:
    separation_sha256 = "d" * 64
    carried = ontology_source("carried-v3-source")
    fresh = ontology_source("fresh-v4-source")
    carried_row = ontology_row(carried, [carried], separation_sha256)
    fresh_row = ontology_row(fresh, [fresh], separation_sha256)
    fresh_row["plan_sha256"] = V4_PLAN_SHA256
    fresh_row.pop("evidence_sha256")
    fresh_row["evidence_sha256"] = canonical_sha256(fresh_row)
    evidence = tmp_path / "mixed.jsonl"; write_jsonl(evidence, [carried_row, fresh_row])
    source_queue = tmp_path / "sources.jsonl"; write_jsonl(source_queue, [carried, fresh])
    summary = {
        "schema_version": "ganesh-mini-repair-source-ontology-aggregate/v1",
        "plan_sha256": V4_PLAN_SHA256,
        "compatible_plan_sha256s": [PLAN_SHA256],
        "status": "coverage-complete",
        "source_queue_sha256": hashlib.sha256(source_queue.read_bytes()).hexdigest(),
        "separation_attestation_sha256s": [separation_sha256],
        "unique_sources": 2,
        "combined_evidence_sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
        "evaluation_artifacts_read": 0,
    }
    summary["aggregate_sha256"] = canonical_sha256(summary)
    summary_path = tmp_path / "summary.json"; summary_path.write_text(json.dumps(summary))

    allowed, context = load_v4_affinity_aggregate_context(
        summary_path, evidence, summary["source_queue_sha256"], {separation_sha256},
    )
    assert allowed == {PLAN_SHA256, V4_PLAN_SHA256}
    assert context["aggregate_sha256"] == summary["aggregate_sha256"]

    summary["compatible_plan_sha256s"] = []
    summary.pop("aggregate_sha256")
    summary["aggregate_sha256"] = canonical_sha256(summary)
    summary_path.write_text(json.dumps(summary))
    with pytest.raises(ValueError, match="aggregate context"):
        load_v4_affinity_aggregate_context(
            summary_path, evidence, summary["source_queue_sha256"], {separation_sha256},
        )


def match_source(identifier: str, dataset: str = "fixture-dataset", lane: str = "python") -> dict:
    source = ontology_source(identifier)
    source["lane"] = lane
    source["source"]["dataset"] = dataset
    return source


def accepted_edge(cell_id: str, source: dict, rank: int) -> dict:
    raw_output = f"accepted-{cell_id}-{source['id']}"
    return {
        "decision": "accept", "classification_mode": "full_ontology", "selection_rank": rank,
        "source_record_sha256": source["source"]["source_record_sha256"],
        "stimulus_sha256": hashlib.sha256(source["stimulus"].encode()).hexdigest(),
        "raw_output": raw_output, "output_sha256": hashlib.sha256(raw_output.encode()).hexdigest(),
    }


def test_two_slot_matching_is_deterministic_and_globally_unique() -> None:
    datasets = ("dataset-a", "dataset-b")
    cells = [
        {"cell_id": "cap-a/python/repair", "lane": "python"},
        {"cell_id": "cap-b/python/repair", "lane": "python"},
    ]
    sources = {row["id"]: row for row in (
        match_source("s1", datasets[0]), match_source("s2", datasets[1]),
        match_source("s3", datasets[0]), match_source("s4", datasets[1]),
    )}
    affinity = {}
    # The graph is coupled across cohorts: cap-b must consume s1/s2, so cap-a
    # must use s3/s4 while every cohort still receives one source per dataset.
    for cell, identifiers in ((cells[0], ("s1", "s3", "s4")), (cells[1], ("s1", "s2"))):
        for rank, identifier in enumerate(identifiers):
            affinity[(cell["cell_id"], identifier)] = accepted_edge(cell["cell_id"], sources[identifier], rank)
    first = match_two_slot_sources(cells, sources, affinity, datasets)
    second = match_two_slot_sources(cells, sources, deepcopy(affinity), datasets)
    assert first == second
    assert len(first) == 4 and len(set(first.values())) == 4
    assert {first[(role, cells[1]["cell_id"])] for role in ("primary", "reserve")} == {"s1", "s2"}
    for role in ("primary", "reserve"):
        assert {
            sources[first[(role, cell["cell_id"])]]['source']['dataset'] for cell in cells
        } == set(datasets)


def test_matching_allows_either_dataset_for_every_language() -> None:
    datasets = ("dataset-a", "dataset-b")
    cells = [
        {"cell_id": "cap-a/python/repair", "lane": "python"},
        {"cell_id": "cap-b/go/repair", "lane": "go"},
    ]
    sources = {row["id"]: row for row in (
        match_source("python-a-1", datasets[0], "python"),
        match_source("python-a-2", datasets[0], "python"),
        match_source("go-b-1", datasets[1], "go"),
        match_source("go-b-2", datasets[1], "go"),
    )}
    affinity = {}
    for cell, identifiers in ((cells[0], ("python-a-1", "python-a-2")), (cells[1], ("go-b-1", "go-b-2"))):
        for rank, identifier in enumerate(identifiers):
            affinity[(cell["cell_id"], identifier)] = accepted_edge(cell["cell_id"], sources[identifier], rank)
    matched = match_two_slot_sources(cells, sources, affinity, datasets)
    assert len(set(matched.values())) == 4
    assert all(sources[matched[(role, cells[0]["cell_id"])]]['source']['dataset'] == datasets[0]
               for role in ("primary", "reserve"))
    assert all(sources[matched[(role, cells[1]["cell_id"])]]['source']['dataset'] == datasets[1]
               for role in ("primary", "reserve"))


def test_matching_rejects_dataset_quota_infeasibility() -> None:
    datasets = ("dataset-a", "dataset-b")
    cells = [
        {"cell_id": "cap-a/python/repair", "lane": "python"},
        {"cell_id": "cap-b/python/repair", "lane": "python"},
    ]
    sources = {row["id"]: row for row in (
        match_source("s1", datasets[0]), match_source("s2", datasets[0]),
        match_source("s3", datasets[0]), match_source("s4", datasets[0]),
    )}
    affinity = {
        (cell["cell_id"], identifier): accepted_edge(cell["cell_id"], source, rank)
        for cell in cells
        for rank, (identifier, source) in enumerate(sources.items())
    }
    with pytest.raises(ValueError, match="30/30 cohort quotas"):
        match_two_slot_sources(cells, sources, affinity, datasets)


def test_matching_supports_three_ordered_datasets_with_half_cohort_ceiling() -> None:
    datasets = ("dataset-a", "dataset-b", "dataset-c")
    cells = [
        {"cell_id": f"cap-{ordinal}/python/repair", "lane": "python"}
        for ordinal in range(4)
    ]
    source_datasets = (datasets[0], datasets[0], datasets[1], datasets[2])
    sources = {}
    affinity = {}
    for cell, dataset in zip(cells, source_datasets):
        for ordinal in range(2):
            source = match_source(f"{cell['cell_id']}-{ordinal}", dataset)
            sources[source["id"]] = source
            affinity[(cell["cell_id"], source["id"])] = accepted_edge(
                cell["cell_id"], source, ordinal,
            )

    first = match_two_slot_sources(cells, sources, affinity, datasets)
    second = match_two_slot_sources(cells, sources, deepcopy(affinity), datasets)

    assert first == second
    assert len(first) == 8 and len(set(first.values())) == 8
    for role in ("primary", "reserve"):
        counts = {
            dataset: sum(
                sources[first[(role, cell["cell_id"])]]['source']['dataset'] == dataset
                for cell in cells
            )
            for dataset in datasets
        }
        assert counts == {"dataset-a": 2, "dataset-b": 1, "dataset-c": 1}


def test_matching_rejects_single_or_duplicate_approved_dataset_lists() -> None:
    with pytest.raises(ValueError, match="at least two distinct approved datasets"):
        match_two_slot_sources([], {}, {}, ("dataset-a",))
    with pytest.raises(ValueError, match="at least two distinct approved datasets"):
        match_two_slot_sources([], {}, {}, ("dataset-a", "dataset-a"))


def test_matching_fails_closed_on_source_from_unapproved_dataset() -> None:
    cell = {"cell_id": "cap-a/python/repair", "lane": "python"}
    approved = match_source("approved", "dataset-a")
    unknown = match_source("unknown", "dataset-c")
    sources = {row["id"]: row for row in (approved, unknown)}
    affinity = {
        (cell["cell_id"], row["id"]): accepted_edge(cell["cell_id"], row, rank)
        for rank, row in enumerate((approved, unknown))
    }
    with pytest.raises(ValueError, match="unapproved datasets"):
        match_two_slot_sources([cell], sources, affinity, ("dataset-a", "dataset-b"))


def test_matching_rejects_three_dataset_ceiling_infeasibility() -> None:
    datasets = ("dataset-a", "dataset-b", "dataset-c")
    cells = [
        {"cell_id": f"cap-{ordinal}/python/repair", "lane": "python"}
        for ordinal in range(4)
    ]
    sources = {}
    affinity = {}
    for cell in cells:
        for ordinal in range(2):
            source = match_source(f"{cell['cell_id']}-{ordinal}", datasets[0])
            sources[source["id"]] = source
            affinity[(cell["cell_id"], source["id"])] = accepted_edge(
                cell["cell_id"], source, ordinal,
            )
    with pytest.raises(ValueError, match="per-dataset cohort ceilings"):
        match_two_slot_sources(cells, sources, affinity, datasets)


def test_build_threads_three_approved_datasets_into_matcher_and_manifest(tmp_path: Path) -> None:
    args = fixture(tmp_path)
    third_dataset = "approved-dataset-c"
    source_rows = [json.loads(line) for line in args[1].read_text().splitlines()]
    affinity_rows = [json.loads(line) for line in args[5].read_text().splitlines()]
    first_cell = repair_cells()[0]
    changed_ids = {
        f"source-{first_cell['primary_capability']}-{first_cell['lane']}-{ordinal}"
        for ordinal in range(2)
    }
    sources_by_id = {row["id"]: row for row in source_rows}
    for identifier in changed_ids:
        sources_by_id[identifier]["source"]["dataset"] = third_dataset
    write_jsonl(args[1], source_rows)

    separation = {
        "source_queue_sha256": hashlib.sha256(args[1].read_bytes()).hexdigest(),
        "exact_normalized_fuzzy_exclusion_complete": True,
        "evaluation_content_exposed": False,
        "eligible_source_queue_ids": [row["id"] for row in source_rows],
    }
    separation["attestation_sha256"] = canonical_sha256(separation)
    args[4].write_text(json.dumps(separation), encoding="utf-8")
    for row in affinity_rows:
        row["separation_attestation_sha256"] = separation["attestation_sha256"]
        if row["source_queue_id"] in changed_ids:
            source = sources_by_id[row["source_queue_id"]]
            row["prompt_sha256"] = hashlib.sha256(
                affinity_prompt(first_cell, source).encode()
            ).hexdigest()
        row.pop("evidence_sha256")
        row["evidence_sha256"] = canonical_sha256(row)
    write_jsonl(args[5], affinity_rows)

    approved = (*QUALIFICATION_DATASETS, third_dataset)
    rows, manifest = build(
        args[0], args[1], args[2], [args[3]], args[4], args[5], approved,
    )
    repeated_rows, repeated_manifest = build(
        args[0], args[1], args[2], [args[3]], args[4], args[5], approved,
    )

    assert (rows, manifest) == (repeated_rows, repeated_manifest)
    assert len(rows) == 120
    assert len({source_key(row) for row in rows}) == 120
    assert manifest["approved_source_datasets"] == list(approved)
    for role in ("primary", "reserve"):
        counts = manifest["dataset_counts"][role]
        assert counts[third_dataset] == 1
        assert sum(counts.values()) == 60
        assert len(counts) == 3
        assert max(counts.values()) == 30


def test_two_slot_matching_rejects_duplicate_lineage_identities() -> None:
    cell = {"cell_id": "cap-a/python/repair", "lane": "python"}
    first, second = match_source("s1"), match_source("s2")
    second["source"]["record_id"] = first["source"]["record_id"]
    sources = {row["id"]: row for row in (first, second)}
    affinity = {(cell["cell_id"], identifier): accepted_edge(cell["cell_id"], source, rank)
                for rank, (identifier, source) in enumerate(sources.items())}
    with pytest.raises(ValueError, match="duplicate lineage"):
        match_two_slot_sources([cell], sources, affinity, ("fixture-dataset", "other-dataset"))
