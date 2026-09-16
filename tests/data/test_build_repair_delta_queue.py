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
    match_two_slot_sources,
    ontology_affinity_prompt,
    repair_cells,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256


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


def test_two_slot_matching_rejects_duplicate_lineage_identities() -> None:
    cell = {"cell_id": "cap-a/python/repair", "lane": "python"}
    first, second = match_source("s1"), match_source("s2")
    second["source"]["record_id"] = first["source"]["record_id"]
    sources = {row["id"]: row for row in (first, second)}
    affinity = {(cell["cell_id"], identifier): accepted_edge(cell["cell_id"], source, rank)
                for rank, (identifier, source) in enumerate(sources.items())}
    with pytest.raises(ValueError, match="duplicate lineage"):
        match_two_slot_sources([cell], sources, affinity, ("fixture-dataset", "other-dataset"))
