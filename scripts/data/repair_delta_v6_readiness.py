#!/usr/bin/env python3
"""Pure, offline readiness primitives for the V6 canonical-test replay.

This module deliberately does not execute suites or call a model.  It owns the
provider response contract, controller path injection, lane-interface checks,
the diagnostic V5 raw-output replay, and the final readiness-report envelope.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable, Mapping

from scripts.data.build_capability_corpus_plan import canonical_sha256


CONTRACT_ID = "capability-stratified-v6-canonical-test-replay/v1"
RESPONSE_SCHEMA_VERSION = "ganesh-mini-repair-delta-v6-test-author-response/v1"
REGRESSION_SCHEMA_VERSION = "ganesh-mini-repair-delta-v6-v5-regression/v1"
COMPOSITE_SCHEMA_VERSION = "ganesh-mini-repair-delta-v6-readiness-composite/v1"
ROLES = ("primary_discrimination", "cross_cutting")
LANES = ("go", "java", "javascript", "typescript", "python", "rust")

CROSS_CUTTING_DEFINITIONS = {
    "duplicate_handling": (
        "exercise only the specification's behavior for repeated equal inputs or keys; "
        "the visible known-bad must already satisfy this behavior"
    ),
    "stable_ordering": (
        "exercise only the specification's required deterministic or stable output order; "
        "the visible known-bad must already satisfy this behavior"
    ),
    "malformed_input": (
        "exercise only the specified rejection or handling of malformed, empty, or invalid input; "
        "the visible known-bad must already satisfy this behavior"
    ),
    "state_isolation": (
        "exercise only independence between separate calls, instances, or sessions; "
        "the visible known-bad must already satisfy this behavior"
    ),
    "immutability_and_aliasing": (
        "exercise only the specified non-mutation, copy, or aliasing behavior; "
        "the visible known-bad must already satisfy this behavior"
    ),
}

CANONICAL_LANE_INTERFACES: dict[str, dict[str, Any]] = {
    "go": {
        "candidate_path": "solution.go", "test_path": "solution_test.go",
        "commands": [["go", "test", "solution.go", "solution_test.go"]],
        "binding": "package solution",
    },
    "java": {
        "candidate_path": "Solution.java", "test_path": "SolutionTest.java",
        "commands": [["javac", "Solution.java", "SolutionTest.java"], ["java", "SolutionTest"]],
        "binding": "default package; SolutionTest.main",
    },
    "javascript": {
        "candidate_path": "solution.js", "test_path": "solution.test.js",
        "commands": [["node", "--test", "solution.test.js"]],
        "binding": "require('./solution.js') only",
    },
    "typescript": {
        "candidate_path": "solution.ts", "test_path": "solution.test.ts",
        "commands": [
            ["tsc", "--strict", "solution.ts", "solution.test.ts"],
            ["node", "solution.test.js"],
        ],
        "binding": "relative module ./solution; no Node typings",
    },
    "python": {
        "candidate_path": "solution.py", "test_path": "test_solution.py",
        "commands": [["python", "-m", "unittest", "test_solution.py"]],
        "binding": "import solution/from solution",
    },
    "rust": {
        "candidate_path": "solution.rs", "test_path": "solution_test.rs",
        "commands": [
            ["rustc", "--edition=2021", "--test", "solution_test.rs", "-o", "solution_test"],
            ["./solution_test"],
        ],
        "binding": '#[path = "solution.rs"] mod solution;',
    },
}

# These are historical identities, not V6 dispositions.  They make the
# diagnostic regression exact and prevent a later implementation from merely
# reporting whichever counts happen to appear in a changed directory.
V5_HEURISTIC_FALSE_POSITIVE_IDS = (
    "cap-v4-associative_aggregation-javascript-repair-primary",
    "cap-v4-associative_aggregation-rust-repair-primary",
    "cap-v4-callbacks_and_events-java-repair-primary",
    "cap-v4-graph_and_tree-go-repair-primary",
    "cap-v4-graph_and_tree-rust-repair-primary",
    "cap-v4-ordering_and_selection-javascript-repair-primary",
    "cap-v4-parsing_and_encoding-rust-repair-primary",
    "cap-v4-sequence_algorithms-rust-repair-primary",
    "cap-v4-stateful_workflows-go-repair-primary",
    "cap-v4-stateful_workflows-rust-repair-primary",
)
V5_JAVA_ROLE_PATH_COLLISION_IDS = (
    "cap-v4-associative_aggregation-java-repair-primary",
    "cap-v4-parsing_and_encoding-java-repair-primary",
    "cap-v4-stateful_workflows-java-repair-primary",
    "cap-v4-string_and_unicode-java-repair-primary",
)
V5_BINDING_FAILURE_IDS = (
    "cap-v4-associative_aggregation-typescript-repair-primary",
    "cap-v4-binary_and_bitwise-javascript-repair-primary",
    "cap-v4-binary_and_bitwise-typescript-repair-primary",
    "cap-v4-binary_and_bitwise-rust-repair-primary",
    "cap-v4-callbacks_and_events-rust-repair-primary",
    "cap-v4-graph_and_tree-javascript-repair-primary",
    "cap-v4-graph_and_tree-typescript-repair-primary",
    "cap-v4-numeric_reasoning-javascript-repair-primary",
    "cap-v5-numeric_reasoning-typescript-repair-primary",
    "cap-v4-ordering_and_selection-rust-repair-primary",
    "cap-v4-parsing_and_encoding-javascript-repair-primary",
    "cap-v4-sequence_algorithms-javascript-repair-primary",
    "cap-v4-stateful_workflows-javascript-repair-primary",
    "cap-v5-stateful_workflows-typescript-repair-primary",
    "cap-v4-string_and_unicode-javascript-repair-primary",
    "cap-v4-string_and_unicode-typescript-repair-primary",
    "cap-v4-string_and_unicode-rust-repair-primary",
)


def response_schema() -> dict[str, Any]:
    role = {
        "type": "object", "additionalProperties": False,
        "required": ["content", "case_ids"],
        "properties": {
            "content": {"type": "string", "minLength": 1},
            "case_ids": {
                "type": "array", "items": {"type": "string", "minLength": 1},
                "minItems": 1,
            },
        },
    }
    return {
        "$id": RESPONSE_SCHEMA_VERSION, "type": "object",
        "additionalProperties": False,
        "required": list(ROLES),
        "properties": {name: role for name in ROLES},
    }


def test_author_projection(candidate: Mapping[str, Any], assignment: Mapping[str, Any]) -> dict[str, Any]:
    lane = candidate.get("lane")
    dimension = assignment.get("assigned_cross_cutting_dimension")
    if lane not in CANONICAL_LANE_INTERFACES:
        raise ValueError("V6 projection has unsupported lane")
    if dimension not in CROSS_CUTTING_DEFINITIONS:
        raise ValueError("V6 projection has unsupported cross-cutting dimension")
    validation = candidate.get("verification_task", {}).get("validation", {})
    known_bad = validation.get("known_bad")
    if not isinstance(known_bad, list) or len(known_bad) != 1:
        raise ValueError("V6 projection requires exactly one embedded known-bad")
    interface = CANONICAL_LANE_INTERFACES[str(lane)]
    return {
        "id": candidate.get("id"),
        "specification": candidate.get("messages", [{}])[0].get("content"),
        "lane": lane,
        "embedded_known_bad": known_bad[0].get("code"),
        "primary_capability": assignment.get("primary_capability"),
        "primary_capability_definition": assignment.get("primary_capability_definition"),
        "assigned_cross_cutting_dimension": dimension,
        "cross_cutting_dimension_definition": CROSS_CUTTING_DEFINITIONS[str(dimension)],
        "canonical_candidate_filename": interface["candidate_path"],
        "canonical_test_filename": interface["test_path"],
        "execution_commands": interface["commands"],
        "required_local_binding": interface["binding"],
    }


def test_author_prompt(projection: Mapping[str, Any]) -> str:
    instruction = (
        "Author two independent deterministic standard-library test suites from only this input. "
        "Return exactly primary_discrimination and cross_cutting; each contains only content and "
        "case_ids. Primary needs at least two distinct valid-domain cases that reject the visible "
        "known-bad primary defect. Cross needs at least one case, asserts only the assigned secondary "
        "dimension, and must pass the visible known-bad. Use exactly the canonical filename, execution "
        "command, and local binding supplied; never use parent-relative paths, environment/argv target "
        "selection, Cargo-only macros, external processes, network access, or third-party packages. "
        "You have not seen the reference, teacher proof, semantic result, verifier output, source data, "
        "V5 outcomes, or evaluation material. Do not use tools or inspect the filesystem. Return only "
        "the schema-constrained object."
    )
    return f"{instruction}\nInput: {json.dumps(dict(projection), separators=(',', ':'), ensure_ascii=False)}"


# These production helpers are imported by tests; prevent pytest from
# collecting the imported callables as standalone test functions.
test_author_projection.__test__ = False
test_author_prompt.__test__ = False


def validate_response(response: Any) -> dict[str, Any]:
    if not isinstance(response, dict) or list(response) != list(ROLES):
        raise ValueError("V6 response must contain the two ordered role objects exactly")
    for role in ROLES:
        value = response.get(role)
        if not isinstance(value, dict) or set(value) != {"content", "case_ids"}:
            raise ValueError(f"{role} must contain only content and case_ids")
        content, case_ids = value.get("content"), value.get("case_ids")
        minimum = 2 if role == "primary_discrimination" else 1
        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"{role} content must be non-empty")
        if (
            not isinstance(case_ids, list) or len(case_ids) < minimum
            or any(not isinstance(item, str) or not item.strip() for item in case_ids)
            or len(set(case_ids)) != len(case_ids)
        ):
            raise ValueError(f"{role} case_ids violate minimum or local uniqueness")
    return response


def inject_controller_paths(lane: str, response: Any) -> dict[str, Any]:
    response = validate_response(response)
    if lane not in CANONICAL_LANE_INTERFACES:
        raise ValueError(f"unsupported V6 lane: {lane}")
    interface = CANONICAL_LANE_INTERFACES[lane]
    roles = []
    for ordinal, role in enumerate(ROLES):
        value = response[role]
        # Logical paths are deliberately distinct even where isolated canonical
        # execution requires the same filename (notably Java).
        logical_path = f"roles/{ordinal + 1:02d}-{role}/{interface['test_path']}"
        roles.append({
            "role": role, "logical_path": logical_path,
            "canonical_execution_path": interface["test_path"],
            "candidate_path": interface["candidate_path"],
            "commands": [list(command) for command in interface["commands"]],
            "content": value["content"],
            "case_ids": list(value["case_ids"]),
            "raw_role_sha256": canonical_sha256(value),
            "injected_path_sha256": canonical_sha256({
                "role": role, "logical_path": logical_path,
                "canonical_execution_path": interface["test_path"],
                "candidate_path": interface["candidate_path"],
            }),
        })
    if roles[0]["logical_path"] == roles[1]["logical_path"]:
        raise AssertionError("controller generated colliding logical role paths")
    result = {"lane": lane, "interface": interface, "roles": roles}
    result["injection_sha256"] = canonical_sha256(result)
    return result


def _local_specifiers(content: str) -> list[str]:
    patterns = (
        r"require\(\s*['\"]([^'\"]+)['\"]\s*\)",
        r"(?:from|import)\s*['\"]([^'\"]+)['\"]",
        r"from\s+['\"]([^'\"]+)['\"]",
    )
    return [match for pattern in patterns for match in re.findall(pattern, content)]


def validate_lane_interface(lane: str, content: str) -> list[dict[str, str]]:
    """Return deterministic structural violations; never judge test semantics."""
    if lane not in CANONICAL_LANE_INTERFACES:
        raise ValueError(f"unsupported V6 lane: {lane}")
    findings: list[dict[str, str]] = []

    def add(code: str, detail: str) -> None:
        if code not in {row["code"] for row in findings}:
            findings.append({"code": code, "detail": detail})

    if "../" in content or "..\\" in content or re.search(r"(?m)^\s*from\s+\.\.", content):
        add("parent-relative-binding", "parent-relative source/module binding is forbidden")
    dynamic_patterns = (
        r"process\.env\b", r"process\.argv\b", r"sys\.argv\b", r"os\.environ\b",
        r"System\.getenv\s*\(", r"std::env::args\s*\(",
    )
    if any(re.search(pattern, content) for pattern in dynamic_patterns):
        add("dynamic-target-selection", "environment/argv target selection is forbidden")
    if re.search(r"(?:CARGO_MANIFEST_DIR|env!\s*\(|include!\s*\()", content):
        add("cargo-only-binding", "Cargo-only compile-time source binding is forbidden")
    if re.search(
        r"(?:child_process|subprocess\b|ProcessBuilder\b|Command::new\s*\(|"
        r"\brequests\.|\burllib\.|\bfetch\s*\(|\bnet/http\b)", content,
    ):
        add("external-execution", "network or subprocess access is forbidden")

    if lane == "go" and not re.search(r"(?m)^\s*package\s+solution\s*$", content):
        add("go-package", "Go tests must use package solution")
    elif lane == "java":
        if re.search(r"(?m)^\s*package\s+", content):
            add("java-package", "Java tests must use the default package")
        if not re.search(r"\bclass\s+SolutionTest\b", content):
            add("java-entrypoint", "Java tests must define SolutionTest")
        if not re.search(r"public\s+static\s+void\s+main\s*\(", content):
            add("java-entrypoint", "Java tests must expose SolutionTest.main")
    elif lane == "javascript":
        local = [item for item in _local_specifiers(content) if item.startswith(".")]
        if "require('./solution.js')" not in content and 'require("./solution.js")' not in content:
            add("javascript-binding", "JavaScript must require('./solution.js')")
        if any(item != "./solution.js" for item in local):
            add("javascript-binding", "unexpected local JavaScript module")
    elif lane == "typescript":
        local = [item for item in _local_specifiers(content) if item.startswith(".")]
        if "./solution" not in local:
            add("typescript-binding", "TypeScript must import relative module ./solution")
        if any(item != "./solution" for item in local):
            add("typescript-binding", "unexpected local TypeScript module")
        if re.search(r"(?:from\s+['\"]node:|require\s*\(|\bprocess\b|\bBuffer\b)", content):
            add("typescript-node-typing", "TypeScript tests may not require Node typings")
        nullable_callbacks = re.findall(
            r"\blet\s+([A-Za-z_$][\w$]*)\s*:\s*\(\(\s*\)\s*=>\s*void\)\s*\|\s*undefined",
            content,
        )
        if any(re.search(rf"\b{re.escape(name)}\s*\(", content) for name in nullable_callbacks):
            add(
                "typescript-strict-null-call",
                "possibly undefined callback is invoked without a TypeScript-recognized guard",
            )
    elif lane == "python":
        if not re.search(r"(?m)^\s*(?:import\s+solution\b|from\s+solution\s+import\b)", content):
            add("python-binding", "Python tests must import solution")
        if re.search(r"(?m)^\s*from\s+\.+", content):
            add("python-binding", "relative Python parent/package imports are forbidden")
    elif lane == "rust":
        if not re.search(
            r"#\s*\[\s*path\s*=\s*['\"]solution\.rs['\"]\s*\]\s*mod\s+solution\s*;",
            content,
        ):
            add("rust-binding", '#[path = "solution.rs"] mod solution; is required')
    return findings


def _legacy_v5_projection(raw_response: Any) -> dict[str, Any]:
    """Project a historical path-bearing V5 response for diagnostics only."""
    if not isinstance(raw_response, dict) or set(raw_response) != set(ROLES):
        raise ValueError("historical V5 response does not contain both roles")
    return {
        role: {
            "content": raw_response[role].get("content"),
            "case_ids": raw_response[role].get("case_ids"),
        }
        for role in ROLES
    }


def run_offline_v5_raw_regression(
    raw_run_paths: Iterable[Path], terminal_artifact_path: Path,
) -> dict[str, Any]:
    paths = [Path(path) for path in raw_run_paths]
    if len(paths) != 60:
        raise ValueError(f"V6 offline regression requires exactly 60 V5 raw runs, got {len(paths)}")
    terminal_rows = [
        json.loads(line) for line in terminal_artifact_path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    terminal = {row["candidate_id"]: row for row in terminal_rows}
    if len(terminal) != 60:
        raise ValueError("V5 terminal accounting must contain exactly 60 unique candidates")
    raw_by_id: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in paths:
        raw = json.loads(path.read_text(encoding="utf-8"))
        candidate_id = raw.get("candidate_id")
        if not isinstance(candidate_id, str) or candidate_id in raw_by_id:
            raise ValueError("V5 raw regression contains missing or duplicate candidate identities")
        raw_by_id[candidate_id] = (path, raw)
    if set(raw_by_id) != set(terminal):
        raise ValueError("V5 raw responses do not exactly match terminal accounting")
    rows = []
    for terminal_row in terminal_rows:
        path, raw = raw_by_id[terminal_row["candidate_id"]]
        candidate_id = raw.get("candidate_id")
        cell_parts = terminal.get(candidate_id, {}).get("cell_id", "").split("/")
        lane = cell_parts[1] if len(cell_parts) == 3 else next(
            (item for item in sorted(LANES, key=len, reverse=True)
             if isinstance(candidate_id, str) and f"-{item}-repair-primary" in candidate_id),
            "",
        )
        if candidate_id not in terminal or lane not in LANES:
            raise ValueError(f"unbound V5 raw response: {path}")
        projected = _legacy_v5_projection(raw.get("response"))
        validate_response(projected)
        injected = inject_controller_paths(lane, projected)
        findings = {
            role: validate_lane_interface(lane, projected[role]["content"]) for role in ROLES
        }
        rows.append({
            "candidate_id": candidate_id, "lane": lane,
            "raw_run_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "projected_response_sha256": canonical_sha256(projected),
            "injection_sha256": injected["injection_sha256"],
            "distinct_logical_role_paths": (
                injected["roles"][0]["logical_path"] != injected["roles"][1]["logical_path"]
            ),
            "structural_findings": findings,
            "structural_finding_codes": sorted({
                finding["code"] for role_findings in findings.values() for finding in role_findings
            }),
            "historical_heuristic_false_positive": candidate_id in V5_HEURISTIC_FALSE_POSITIVE_IDS,
            "historical_java_path_collision": candidate_id in V5_JAVA_ROLE_PATH_COLLISION_IDS,
            "historical_binding_failure": candidate_id in V5_BINDING_FAILURE_IDS,
        })
    by_id = {row["candidate_id"]: row for row in rows}
    if len(by_id) != 60:
        raise ValueError("V5 raw regression contains duplicate candidate identities")
    if set(V5_HEURISTIC_FALSE_POSITIVE_IDS) - by_id.keys():
        raise ValueError("V5 heuristic false-positive fixture is missing")
    if any(
        not by_id[candidate_id]["distinct_logical_role_paths"]
        for candidate_id in V5_JAVA_ROLE_PATH_COLLISION_IDS
    ):
        raise ValueError("controller path injection did not eliminate Java role collision")
    if any(
        not by_id[candidate_id]["structural_finding_codes"]
        for candidate_id in V5_BINDING_FAILURE_IDS
    ):
        raise ValueError("an observed V5 binding failure was not explicitly detected")
    report = {
        "schema_version": REGRESSION_SCHEMA_VERSION, "contract_id": CONTRACT_ID,
        "status": "passed", "historical_only": True,
        "coverage": {
            "raw_responses": 60,
            "heuristic_false_positives_not_syntax_adjudicated": len(V5_HEURISTIC_FALSE_POSITIVE_IDS),
            "java_role_path_collisions_eliminated": len(V5_JAVA_ROLE_PATH_COLLISION_IDS),
            "binding_failure_identities_explicitly_detected": len(V5_BINDING_FAILURE_IDS),
        },
        "terminal_artifacts_sha256": hashlib.sha256(terminal_artifact_path.read_bytes()).hexdigest(),
        "rows": rows, "rows_sha256": canonical_sha256(rows),
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


REQUIRED_READINESS_COMPONENTS = (
    "offline_v5_raw_regression", "unit_fixtures", "canonical_staging_closure",
    "live_provider_schema_smoke", "training_only_canaries",
)


def build_composite_readiness_report(
    *, plan_sha256: str, components: Mapping[str, Mapping[str, Any]],
    implementation_hashes: Mapping[str, str], input_hashes: Mapping[str, str],
) -> dict[str, Any]:
    if tuple(components) != REQUIRED_READINESS_COMPONENTS:
        raise ValueError("V6 readiness components are missing or out of canonical order")
    component_rows = []
    for name in REQUIRED_READINESS_COMPONENTS:
        component = components[name]
        if component.get("status") != "passed" or component.get("evaluation_artifacts_read") != 0:
            raise ValueError(f"V6 readiness component did not pass cleanly: {name}")
        seal = component.get("report_sha256") or component.get("artifact_sha256")
        if not isinstance(seal, str) or not re.fullmatch(r"[0-9a-f]{64}", seal):
            raise ValueError(f"V6 readiness component is unsealed: {name}")
        component_rows.append({"name": name, "status": "passed", "sha256": seal})
    for label, values in (("implementation", implementation_hashes), ("input", input_hashes)):
        if not values or any(not re.fullmatch(r"[0-9a-f]{64}", value) for value in values.values()):
            raise ValueError(f"V6 {label} hashes are incomplete or malformed")
    report = {
        "schema_version": COMPOSITE_SCHEMA_VERSION, "contract_id": CONTRACT_ID,
        "plan_sha256": plan_sha256, "status": "passed",
        "components": component_rows,
        "components_sha256": canonical_sha256(component_rows),
        "implementation_hashes": dict(implementation_hashes),
        "input_hashes": dict(input_hashes), "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report
