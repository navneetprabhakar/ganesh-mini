import hashlib
import json
import time
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.data.review_capability_qualification import (
    build_semantic_evidence,
    campaign_descriptor,
    exact_review_items,
    load_evidence,
    review_batch,
    review_prompt,
    select_batch,
)


def candidate(identifier: str, lane: str = "python") -> dict:
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1",
        "id": identifier,
        "lane": lane,
        "task_type": "generation",
        "messages": [
            {"role": "user", "content": f"Implement parse_{identifier}(text)."},
            {"role": "assistant", "content": "def parse_x(text):\n    return text\n"},
        ],
        "qualification_assignment": {
            "cell_id": f"parsing_and_encoding/{lane}/generation",
            "primary_capability": "parsing_and_encoding",
            "primary_capability_definition": "parse a structured representation",
            "assigned_cross_cutting_dimension": "malformed_input",
        },
    }


def test_prompt_has_only_specification_and_assigned_ontology() -> None:
    prompt = review_prompt([candidate("q-1")])
    assert "Implement parse_q-1(text)." in prompt
    assert "parsing_and_encoding" in prompt and "malformed_input" in prompt
    assert "def parse_x" not in prompt
    assert "reference implementations" in prompt
    assert "tests" in prompt
    assert '"messages"' not in prompt
    assert "qualification_assignment" not in prompt


def test_semantic_evidence_matches_admission_contract_and_is_sealed() -> None:
    item = candidate("q-1")
    evidence = build_semantic_evidence(item, {
        "id": "q-1", "verdict": "pass", "primary_capability_is_substantive": True,
        "generic_edge_case_boilerplate_is_primary": False, "rationale": "Parsing drives the required behavior.",
    }, "a" * 64)
    assert evidence["primary_capability"] == "parsing_and_encoding"
    assert evidence["visibility"]["specification_and_assigned_labels_only"] is True
    assert evidence["visibility"]["verifier_outputs_visible"] is False
    assert evidence["visibility"]["evaluation_artifacts_read"] == 0
    assert load_evidence(evidence) == evidence


def test_inconsistent_pass_verdict_is_rejected() -> None:
    with pytest.raises(ValueError, match="internally inconsistent"):
        build_semantic_evidence(candidate("q-1"), {
            "id": "q-1", "verdict": "pass", "primary_capability_is_substantive": False,
            "generic_edge_case_boilerplate_is_primary": False, "rationale": "Incidental capability.",
        }, "a" * 64)


def test_review_output_accepts_booleans_and_restores_request_order() -> None:
    items = exact_review_items({"items": [
        {"id": "b", "verdict": "reject", "primary_capability_is_substantive": False,
         "generic_edge_case_boilerplate_is_primary": True, "rationale": "Generic."},
        {"id": "a", "verdict": "pass", "primary_capability_is_substantive": True,
         "generic_edge_case_boilerplate_is_primary": False, "rationale": "Substantive."},
    ]}, ["a", "b"])
    assert [item["id"] for item in items] == ["a", "b"]


def test_lane_batch_selection_is_deterministic_and_bounded() -> None:
    rows = [candidate(f"py-{index}") for index in range(12)] + [candidate("go-0", "go")]
    assert [row["id"] for row in select_batch(rows, "python", 1, 10)] == ["py-10", "py-11"]
    with pytest.raises(ValueError, match="invalid"):
        select_batch(rows, "python", 0, 11)


def test_parallel_review_reassembles_in_input_order_and_fails_closed(tmp_path: Path) -> None:
    rows = [candidate(str(index)) for index in range(4)]

    def successful(shard, _config, _codex, _schema):
        if shard[0]["id"] == "0":
            time.sleep(0.02)
        return ([{"candidate_sha256": row["id"]} for row in shard], [{"first": shard[0]["id"]}], None)

    with patch("scripts.data.review_capability_qualification.review_shard", side_effect=successful):
        reviews, runs, failures = review_batch(rows, {}, "codex", tmp_path / "schema", workers=2)
    assert [row["candidate_sha256"] for row in reviews] == ["0", "1", "2", "3"]
    assert runs == [{"first": "0"}, {"first": "2"}]
    assert failures == []

    def failing(shard, _config, _codex, _schema):
        return ([], [], "failed") if shard[0]["id"] == "2" else ([{"candidate_sha256": "ok"}], [], None)

    with patch("scripts.data.review_capability_qualification.review_shard", side_effect=failing):
        reviews, _runs, failures = review_batch(rows, {}, "codex", tmp_path / "schema", workers=2)
    assert reviews == []
    assert failures == [{"lane": "python", "shard": "1", "reason": "failed"}]


def test_campaign_hash_binds_exact_candidate_file(tmp_path: Path) -> None:
    path = tmp_path / "candidates.jsonl"
    path.write_text(json.dumps(candidate("q-1")) + "\n", encoding="utf-8")
    descriptor = campaign_descriptor(path, [candidate("q-1")])
    assert descriptor["candidate_input_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    body = dict(descriptor)
    seal = body.pop("campaign_sha256")
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    assert seal == hashlib.sha256(encoded).hexdigest()
