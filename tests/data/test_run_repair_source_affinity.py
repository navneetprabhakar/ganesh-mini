import hashlib
import json

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_repair_delta_queue import AFFINITY_FIELDS, affinity_prompt, repair_cells
from scripts.data.run_repair_source_affinity import (
    build_affinity_row, build_attestation, plan_requests, validate_payload, verify_completed,
)


def source(identifier: str, lane: str = "python") -> dict:
    stimulus = f"repair numeric source {identifier}"
    return {
        "id": identifier, "lane": lane, "task_type": "repair", "stimulus": stimulus,
        "source": {"dataset": "training", "revision": "rev", "record_id": identifier,
                   "source_record_sha256": hashlib.sha256(stimulus.encode()).hexdigest()},
    }


def comparison(path, source_path, excluded=()):
    value = {
        "schema_version": "ganesh-mini-content-free-source-comparison/v1",
        "source_queue_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "comparison_manifest_sha256": "a" * 64,
        "exact_normalized_fuzzy_comparison_complete": True,
        "excluded_source_queue_ids": list(excluded),
        "visibility": {
            "evaluation_content_exposed_to_construction": False,
            "evaluation_identifiers_exposed_to_construction": False,
            "evaluation_paths_exposed_to_construction": False,
        },
    }
    value["comparison_sha256"] = canonical_sha256(value)
    path.write_text(json.dumps(value))


def test_attestation_exposes_only_eligible_source_ids(tmp_path) -> None:
    source_path = tmp_path / "sources.jsonl"
    source_path.write_text("\n".join(json.dumps(source(name)) for name in ("a", "b")) + "\n")
    comparison_path = tmp_path / "comparison.json"; comparison(comparison_path, source_path, ["b"])
    attestation = build_attestation(source_path, comparison_path)
    assert attestation["eligible_source_queue_ids"] == ["a"]
    assert attestation["evaluation_content_exposed"] is False
    body = dict(attestation); seal = body.pop("attestation_sha256")
    assert seal == canonical_sha256(body)


def test_request_plan_is_deterministic_unique_and_repair_only() -> None:
    rows = []
    for cell in repair_cells():
        rows.extend(source(f"{cell['cell_id']}-{index}", cell["lane"]) for index in range(2))
    eligible = {row["id"] for row in rows}
    first = plan_requests(rows, eligible, set(), 2)
    second = plan_requests(rows, eligible, set(), 2)
    assert first == second and len(first) == 120
    assert len({item["source"]["id"] for item in first}) == 120
    assert all(item["source"]["task_type"] == "repair" for item in first)


def accepted_payload() -> dict:
    return {
        "decision": "accept", "capability_operation": "numeric scaling",
        "defect_affordance": "wrong rounding", **{field: True for field in AFFINITY_FIELDS},
    }


def test_accept_requires_every_affinity_condition() -> None:
    payload = accepted_payload(); payload[AFFINITY_FIELDS[0]] = False
    with pytest.raises(ValueError, match="inconsistent"):
        validate_payload(payload)


def test_affinity_row_preserves_and_seals_exact_prompt_output(tmp_path) -> None:
    cell = next(cell for cell in repair_cells() if cell["lane"] == "python")
    src = source("x")
    request = {"cell": cell, "source": src, "selection_rank": 0}
    prompt = affinity_prompt(cell, src); raw_output = json.dumps(accepted_payload())
    config = {"model": "fixture"}; run = {"final_output": raw_output, "prompt": prompt}
    row = build_affinity_row(request, accepted_payload(), prompt, raw_output, run, config, "codex-cli fixture", "b" * 64)
    assert row["raw_prompt"] == prompt and row["raw_output"] == raw_output
    assert row["prompt_sha256"] == hashlib.sha256(prompt.encode()).hexdigest()
    path = tmp_path / "row.json"; path.write_text(json.dumps(row))
    assert verify_completed(path, request, config, "codex-cli fixture", "b" * 64) == row
