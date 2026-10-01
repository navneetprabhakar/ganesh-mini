from __future__ import annotations

import copy
import hashlib
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v6_readiness import (
    CANONICAL_LANE_INTERFACES,
    REQUIRED_READINESS_COMPONENTS,
    RESPONSE_SCHEMA_VERSION,
    V5_BINDING_FAILURE_IDS,
    V5_HEURISTIC_FALSE_POSITIVE_IDS,
    V5_JAVA_ROLE_PATH_COLLISION_IDS,
    build_composite_readiness_report,
    inject_controller_paths,
    response_schema,
    run_offline_v5_raw_regression,
    test_author_projection,
    test_author_prompt,
    validate_lane_interface,
    validate_response,
)


ROOT = Path(__file__).resolve().parents[2]
V5_ROOT = (
    ROOT / "measurement/gate2/capability-stratified-v5-interface-replay"
    / "primary-two-phase-v3"
)
PLAN = ROOT / "docs/plans/GATE2_REPAIR_DELTA_V6_CANONICAL_TEST_REPLAY_PLAN_20260917.md"
PLAN_SHA256 = "4fe6a1374c01a0a682bf256c91a141b36b26680bdb5279049070f4f143418ec1"


def _response(primary_ids: list[str] | None = None) -> dict:
    return {
        "primary_discrimination": {
            "content": "first role", "case_ids": primary_ids or ["p-1", "p-2"],
        },
        "cross_cutting": {"content": "second role", "case_ids": ["c-1"]},
    }


def test_v6_plan_hash_is_the_canonical_revised_plan() -> None:
    assert hashlib.sha256(PLAN.read_bytes()).hexdigest() == PLAN_SHA256


def test_v6_provider_schema_has_no_paths_or_unsupported_unique_items() -> None:
    schema = response_schema()
    assert schema["$id"] == RESPONSE_SCHEMA_VERSION
    assert schema["required"] == ["primary_discrimination", "cross_cutting"]
    assert set(schema["properties"]) == {"primary_discrimination", "cross_cutting"}
    assert "path" not in repr(schema)
    assert "uniqueItems" not in repr(schema)


def test_v6_projection_and_prompt_bind_canonical_interface_without_reference() -> None:
    candidate = {
        "id": "fixture", "lane": "javascript",
        "messages": [{"role": "user", "content": "Repair it."}],
        "verification_task": {"validation": {"known_bad": [{"code": "bad"}]}},
    }
    assignment = {
        "primary_capability": "numeric_reasoning",
        "primary_capability_definition": "compute numeric results",
        "assigned_cross_cutting_dimension": "malformed_input",
    }
    projection = test_author_projection(candidate, assignment)
    assert projection["canonical_candidate_filename"] == "solution.js"
    assert projection["required_local_binding"] == "require('./solution.js') only"
    assert "reference" not in projection
    prompt = test_author_prompt(projection)
    assert "must pass the visible known-bad" in prompt
    assert "parent-relative" in prompt


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda value: value.update({"extra": {}}), "two ordered role objects"),
        (lambda value: value["primary_discrimination"].update({"path": "x"}), "only content"),
        (lambda value: value["primary_discrimination"].update({"case_ids": ["one"]}), "minimum"),
        (lambda value: value["primary_discrimination"].update({"case_ids": ["x", "x"]}), "uniqueness"),
        (lambda value: value["cross_cutting"].update({"content": ""}), "non-empty"),
    ],
)
def test_v6_response_contract_fails_closed(mutation, message: str) -> None:
    value = _response()
    mutation(value)
    with pytest.raises(ValueError, match=message):
        validate_response(value)


@pytest.mark.parametrize("lane", CANONICAL_LANE_INTERFACES)
def test_controller_injects_distinct_role_paths_and_canonical_execution_paths(lane: str) -> None:
    injected = inject_controller_paths(lane, _response())
    assert [row["role"] for row in injected["roles"]] == [
        "primary_discrimination", "cross_cutting",
    ]
    assert len({row["logical_path"] for row in injected["roles"]}) == 2
    assert {row["canonical_execution_path"] for row in injected["roles"]} == {
        CANONICAL_LANE_INTERFACES[lane]["test_path"]
    }
    assert all(len(row["injected_path_sha256"]) == 64 for row in injected["roles"])


@pytest.mark.parametrize(
    ("lane", "content", "expected"),
    [
        ("go", "package wrong", "go-package"),
        ("java", "class Other { public static void main(String[] x) {} }", "java-entrypoint"),
        ("javascript", "require('../solution.js')", "parent-relative-binding"),
        ("javascript", "require('../index.js')", "javascript-binding"),
        ("javascript", "require(process.env.TARGET_MODULE || process.argv[2])", "dynamic-target-selection"),
        ("typescript", 'import { x } from "../solution";', "parent-relative-binding"),
        ("typescript", 'import test from "node:test"; import { x } from "./solution";', "typescript-node-typing"),
        (
            "typescript",
            'import { x } from "./solution"; let release: (() => void) | undefined; release();',
            "typescript-strict-null-call",
        ),
        ("python", "from ..solution import x", "parent-relative-binding"),
        ("rust", 'include!(concat!(env!("CARGO_MANIFEST_DIR"), "/solution.rs"));', "cargo-only-binding"),
        ("rust", '#[path = "../solution.rs"] mod solution;', "rust-binding"),
    ],
)
def test_lane_interface_negative_signatures_are_explicit(
    lane: str, content: str, expected: str,
) -> None:
    assert expected in {row["code"] for row in validate_lane_interface(lane, content)}


@pytest.mark.parametrize(
    ("lane", "content"),
    [
        ("go", "package solution\nfunc TestX(t *testing.T) {}"),
        ("java", "class SolutionTest { public static void main(String[] args) {} }"),
        ("javascript", "const s = require('./solution.js');"),
        ("typescript", 'import { x } from "./solution"; void x;'),
        ("python", "from solution import x\nassert x"),
        ("rust", '#[path = "solution.rs"] mod solution;'),
    ],
)
def test_lane_interface_accepts_canonical_binding_shapes(lane: str, content: str) -> None:
    assert validate_lane_interface(lane, content) == []


def test_offline_v5_raw_regression_accounts_exact_historical_mechanisms() -> None:
    report = run_offline_v5_raw_regression(
        (V5_ROOT / "codex-runs").glob("*.test_author.json"),
        V5_ROOT / "terminal-artifacts.jsonl",
    )
    assert report["status"] == "passed"
    assert report["historical_only"] is True
    assert report["coverage"] == {
        "raw_responses": 60,
        "heuristic_false_positives_not_syntax_adjudicated": 10,
        "java_role_path_collisions_eliminated": 4,
        "binding_failure_identities_explicitly_detected": 17,
    }
    assert len(V5_HEURISTIC_FALSE_POSITIVE_IDS) == 10
    assert len(V5_JAVA_ROLE_PATH_COLLISION_IDS) == 4
    assert len(V5_BINDING_FAILURE_IDS) == 17
    assert all(row["distinct_logical_role_paths"] for row in report["rows"])
    rows = {row["candidate_id"]: row for row in report["rows"]}
    assert all(rows[item]["structural_finding_codes"] for item in V5_BINDING_FAILURE_IDS)
    body = dict(report); claimed = body.pop("report_sha256")
    assert claimed == canonical_sha256(body)
    assert report["evaluation_artifacts_read"] == 0


def _component(name: str) -> dict:
    body = {"name": name, "status": "passed", "evaluation_artifacts_read": 0}
    body["report_sha256"] = canonical_sha256(body)
    return body


def test_composite_readiness_binds_all_components_and_hashes() -> None:
    components = {name: _component(name) for name in REQUIRED_READINESS_COMPONENTS}
    report = build_composite_readiness_report(
        plan_sha256=PLAN_SHA256, components=components,
        implementation_hashes={"v6_readiness": "1" * 64},
        input_hashes={"v5_terminal": "2" * 64},
    )
    assert report["status"] == "passed"
    assert [row["name"] for row in report["components"]] == list(REQUIRED_READINESS_COMPONENTS)
    assert report["evaluation_artifacts_read"] == 0
    body = dict(report); claimed = body.pop("report_sha256")
    assert claimed == canonical_sha256(body)


def test_composite_readiness_rejects_failed_or_reordered_components() -> None:
    components = {name: _component(name) for name in REQUIRED_READINESS_COMPONENTS}
    failed = copy.deepcopy(components)
    failed["training_only_canaries"]["status"] = "failed"
    with pytest.raises(ValueError, match="did not pass"):
        build_composite_readiness_report(
            plan_sha256=PLAN_SHA256, components=failed,
            implementation_hashes={"impl": "1" * 64}, input_hashes={"input": "2" * 64},
        )
    reordered = dict(reversed(components.items()))
    with pytest.raises(ValueError, match="canonical order"):
        build_composite_readiness_report(
            plan_sha256=PLAN_SHA256, components=reordered,
            implementation_hashes={"impl": "1" * 64}, input_hashes={"input": "2" * 64},
        )
