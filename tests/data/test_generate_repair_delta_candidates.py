import hashlib
import json

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_repair_delta_candidates import (
    DEFAULT_V4_PREFLIGHT_CONFIG, PROOF_BOOL_FIELDS, PROOF_STRING_FIELDS,
    build_output, exact_items, load_reserve_eligibility, output_schema, select_rows,
    teacher_prompt,
)
from scripts.data.repair_delta_v4_preflight import (
    CONTRACT_ID as V4_CONTRACT_ID,
    PROOF_SCHEMA as V4_PROOF_SCHEMA,
    load_preflight_config,
    validate_teacher_proof_v4,
)


def assignment(
    identifier: str, role: str = "primary", lane: str = "python", contract_version: str = "v3",
) -> dict:
    return {
        "schema_version": (
            "ganesh-mini-repair-delta-assignment/v1" if contract_version == "v3"
            else "ganesh-mini-repair-delta-v4-assignment/v1"
        ),
        "contract_id": (
            "capability-stratified-v3-repair-delta/v1" if contract_version == "v3"
            else V4_CONTRACT_ID
        ), "id": identifier,
        "role": role, "generation_eligible": role == "primary",
        "cell_id": f"numeric_reasoning/{lane}/repair", "primary_capability": "numeric_reasoning",
        "primary_capability_definition": "integer-safe arithmetic", "assigned_cross_cutting_dimension": "malformed_input",
        "lane": lane, "task_type": "repair", "source_queue_id": f"source-{identifier}",
        "source": {"dataset": "training", "revision": "rev", "record_id": identifier,
                   "source_record_sha256": hashlib.sha256(identifier.encode()).hexdigest()},
        "stimulus": "repair a numeric calculation", "source_affinity_evidence_sha256": "a" * 64,
        "source_affinity_card": {"capability_operation": "scale integers", "defect_affordance": "wrong rounding"},
    }


def teacher_item(identifier: str) -> dict:
    return {
        "id": identifier, "problem": "Repair code.", "reference_code": "def f():\n    return 1",
        "known_bad_code": "def f():\n    return 0", "known_bad_label": "uses wrong arithmetic",
        **{field: f"proof for {field}" for field in PROOF_STRING_FIELDS},
        **{field: True for field in PROOF_BOOL_FIELDS},
    }


def v4_teacher_item(identifier: str) -> dict:
    value = teacher_item(identifier)
    marker = load_preflight_config(DEFAULT_V4_PREFLIGHT_CONFIG)["success_marker"]
    value["known_bad_cross_witness"] = {
        "valid_domain_input": "None is explicitly covered by the malformed-input clause",
        "scheduled_dimension_assertion": "f(None) raises TypeError or ValueError",
        "content": (
            "from solution import f\n"
            "try:\n    f(None)\nexcept (TypeError, ValueError):\n    pass\n"
            "else:\n    raise AssertionError('must reject malformed input')\n"
            f"print('{marker}')\n"
        ),
    }
    return value


def test_prompt_requires_primary_bug_and_secondary_already_correct() -> None:
    prompt = teacher_prompt("python", [assignment("x")])
    assert "bug MUST alter the assigned primary capability" in prompt
    assert "must already implement the scheduled cross-cutting dimension correctly" in prompt
    assert "wrong rounding" in prompt and "malformed_input" in prompt
    assert "evaluation" not in json.dumps([assignment("x")])


def test_schema_and_parser_require_true_proof_booleans() -> None:
    assert set(PROOF_BOOL_FIELDS).issubset(output_schema()["properties"]["items"]["items"]["required"])
    item = teacher_item("x")
    assert exact_items({"items": [item]}, ["x"])[0] == item
    item["known_bad_already_satisfies_scheduled_dimension"] = False
    with pytest.raises(ValueError, match="repair-delta"):
        exact_items({"items": [item]}, ["x"])


def test_proof_is_separate_and_candidate_has_no_fake_test() -> None:
    result = build_output(assignment("x"), teacher_item("x"), "b" * 64)
    assert result["candidate"]["schema_version"] == "ganesh-mini-expansion-candidate/v1"
    assert not [file for file in result["candidate"]["verification_task"]["files"] if file.get("role") == "test"]
    proof = result["repair_delta_proof"]
    assert proof["known_bad_already_satisfies_scheduled_dimension"] is True
    body = dict(proof); seal = body.pop("evidence_sha256")
    assert seal == canonical_sha256(body)


def test_v4_generator_emits_exact_teacher_bound_cross_witness_proof() -> None:
    row = assignment("x", contract_version="v4")
    item = v4_teacher_item("x")
    schema = output_schema("v4")["properties"]["items"]["items"]
    assert "known_bad_cross_witness" in schema["required"]
    parsed = exact_items({"items": [item]}, ["x"], "v4", "python")
    prompt = teacher_prompt("python", [row], "v4")
    config = load_preflight_config(DEFAULT_V4_PREFLIGHT_CONFIG)
    assert config["success_marker"] in prompt
    assert config["lanes"]["python"]["witness_path"] in prompt

    result = build_output(row, parsed[0], "b" * 64, "v4")
    proof = result["repair_delta_proof"]
    assert proof["schema_version"] == V4_PROOF_SCHEMA
    assert proof["known_bad_cross_witness"]["path"] == "cross_witness.py"
    assert proof["known_bad_cross_witness"]["content"].count(config["success_marker"]) == 1
    assert validate_teacher_proof_v4(result["candidate"], row, proof) is proof

    with pytest.raises(ValueError, match="contract differs"):
        build_output(assignment("x"), item, "b" * 64, "v4")


def test_v4_go_uses_frozen_120_second_execution_envelope() -> None:
    row = assignment("go-timeout", lane="go", contract_version="v4")
    item = v4_teacher_item("go-timeout")
    result = build_output(row, item, "b" * 64, "v4")

    assert result["candidate"]["verification_task"]["limits"]["timeout_seconds"] == 120


def test_v4_witness_marker_is_exactly_once_and_v3_schema_is_unchanged() -> None:
    assert "known_bad_cross_witness" not in output_schema()["properties"]["items"]["items"]["required"]
    item = v4_teacher_item("x")
    marker = load_preflight_config(DEFAULT_V4_PREFLIGHT_CONFIG)["success_marker"]
    item["known_bad_cross_witness"]["content"] += f"print('{marker}')\n"
    with pytest.raises(ValueError, match="known_bad_cross_witness"):
        exact_items({"items": [item]}, ["x"], "v4", "python")


def test_primary_and_reserve_eligibility_are_bounded(tmp_path) -> None:
    primaries = [assignment(str(index)) for index in range(10)]
    assert select_rows(primaries, "python", "primary") == primaries
    reserves = [assignment("r1", "reserve"), assignment("r2", "reserve")]
    assert select_rows(reserves, "python", "reserve", {reserves[1]["cell_id"]}) == reserves
    with pytest.raises(ValueError, match="sealed eligibility"):
        select_rows(reserves, "python", "reserve")

    eligibility = {
        "schema_version": "ganesh-mini-repair-delta-reserve-eligibility/v1",
        "queue_manifest_sha256": "a" * 64, "first_pass_thresholds_passed": True,
        "rejected_cell_ids": [f"cap-{index}/python/repair" for index in range(7)],
        "evaluation_artifacts_read": 0,
    }
    eligibility["eligibility_sha256"] = canonical_sha256(eligibility)
    path = tmp_path / "eligibility.json"; path.write_text(json.dumps(eligibility))
    with pytest.raises(ValueError, match="sealed passing"):
        load_reserve_eligibility(path, "a" * 64)
