#!/usr/bin/env python3
"""Fail-closed admission for the v3 repair-delta qualification lane.

The program consumes already-authored and already-executed training-only
evidence.  It never reads evaluation artifacts and never executes candidate
code.  Semantic evidence is independently sealed and explicitly proves that
the reviewer could not see the teacher proof or executable evidence.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_expansion import AdmissionFailure, canonical_json, read_jsonl, validate_candidate  # noqa: E402
from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.eval.contracts import sha256_object, sha256_text  # noqa: E402
from scripts.verify.sandbox import SANDBOX_CONTRACT  # noqa: E402
from scripts.data.repair_delta_v5_contract import (  # noqa: E402
    CONTRACT_ID as V5_CONTRACT_ID,
    cohort_binding as make_v5_cohort_binding,
    load_v5_contract,
    validate_terminal_order as validate_v5_terminal_order,
)


CONTRACT_ID = "capability-stratified-v3-repair-delta/v1"
V4_CONTRACT_ID = "capability-stratified-v4-repair-delta/v1"
ENVELOPE_SCHEMA = "ganesh-mini-repair-delta-envelope/v1"
V4_ENVELOPE_SCHEMA = "ganesh-mini-repair-delta-v4-envelope/v1"
OUTPUT_SCHEMA = "ganesh-mini-repair-delta-admitted/v1"
V4_OUTPUT_SCHEMA = "ganesh-mini-repair-delta-v4-admitted/v1"
REPORT_SCHEMA = "ganesh-mini-repair-delta-admission-report/v1"
V4_REPORT_SCHEMA = "ganesh-mini-repair-delta-v4-admission-report/v1"
ASSEMBLY_SCHEMA = "ganesh-mini-repair-delta-evidence-assembly/v1"
V4_ASSEMBLY_SCHEMA = "ganesh-mini-repair-delta-v4-evidence-assembly/v1"
V5_ENVELOPE_SCHEMA = "ganesh-mini-repair-delta-v5-envelope/v1"
V5_OUTPUT_SCHEMA = "ganesh-mini-repair-delta-v5-admitted/v1"
V5_REPORT_SCHEMA = "ganesh-mini-repair-delta-v5-admission-report/v1"
V5_ASSEMBLY_SCHEMA = "ganesh-mini-repair-delta-v5-evidence-assembly/v1"
V4_QUEUE_MANIFEST_SCHEMA = "ganesh-mini-repair-delta-v4-queue-manifest/v1"
EVIDENCE_NAMES = {
    "teacher_proof", "semantic_review", "test_author", "delta_audit",
    "separation", "executable", "lineage",
}
V4_EVIDENCE_NAMES = EVIDENCE_NAMES | {"post_teacher_preflight"}
V5_EVIDENCE_NAMES = EVIDENCE_NAMES | {"interface_preflight"}
SEMANTIC_BOOLEANS = (
    "repair_delta_requires_primary_capability",
    "scheduled_dimension_is_concrete_and_secondary",
    "known_bad_already_satisfies_scheduled_dimension",
    "cross_dimension_only_patch_cannot_solve",
    "capability_remains_substantive_without_cross_clause",
    "generic_boilerplate_is_not_primary",
)
PROOF_BOOLEAN_OVERLAP = (
    "known_bad_already_satisfies_scheduled_dimension",
    "cross_dimension_only_patch_cannot_solve",
    "capability_remains_substantive_without_cross_clause",
)
SEPARATION_PASSES = (
    "exact_training_passed", "normalized_training_passed", "fuzzy_training_passed",
    "exact_evaluation_passed", "normalized_evaluation_passed", "fuzzy_evaluation_passed",
)
CANONICAL_TEST_PATHS = {
    "go": "solution_test.go",
    "java": "SolutionTest.java",
    "javascript": "solution.test.js",
    "typescript": "solution.test.ts",
    "python": "test_solution.py",
    "rust": "solution_test.rs",
}
STAGING_SCHEMA = "ganesh-mini-repair-delta-test-staging/v1"


class UnresolvedEvidence(AdmissionFailure):
    """Infrastructure evidence that requires the one allowed identical replay."""


def load_v4_primary_cohort_binding(
    queue_path: Path, manifest_path: Path, cohort: str,
) -> dict[str, Any]:
    """Load the sealed V4 queue and bind final accounting to its ordered primaries."""
    if cohort != "primary":
        raise AdmissionFailure("V4 final admission requires the primary cohort")
    queue_payload = queue_path.read_bytes()
    rows = [
        json.loads(line) for line in queue_payload.decode("utf-8").splitlines()
        if line.strip()
    ]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise AdmissionFailure("V4 queue manifest is malformed")
    body = dict(manifest)
    claimed = body.pop("manifest_sha256", None)
    if (
        claimed != canonical_sha256(body)
        or manifest.get("schema_version") != V4_QUEUE_MANIFEST_SCHEMA
        or manifest.get("contract_version") != "v4"
        or manifest.get("contract_id") != V4_CONTRACT_ID
        or manifest.get("queue_sha256") != hashlib.sha256(queue_payload).hexdigest()
        or manifest.get("assignments") != 120
        or manifest.get("primary_assignments") != 60
        or manifest.get("initial_generation_eligible") != 60
        or len(rows) != 120
    ):
        raise AdmissionFailure("V4 queue or manifest is unsealed or inconsistent")
    identifiers = [row.get("id") for row in rows if isinstance(row, dict)]
    if (
        len(identifiers) != 120
        or any(not isinstance(identifier, str) or not identifier for identifier in identifiers)
        or len(set(identifiers)) != 120
    ):
        raise AdmissionFailure("V4 queue identities are malformed or duplicated")
    primary_rows = [row for row in rows if row.get("role") == "primary"]
    primary_ids = [row["id"] for row in primary_rows]
    if (
        len(primary_rows) != 60
        or any(
            row.get("cohort") != "first_pass"
            or row.get("generation_eligible") is not True
            or row.get("contract_id") != V4_CONTRACT_ID
            for row in primary_rows
        )
        or any(row.get("role") not in {"primary", "reserve"} for row in rows)
    ):
        raise AdmissionFailure("V4 queue does not contain the exact ordered 60-primary cohort")
    binding: dict[str, Any] = {
        "schema_version": "ganesh-mini-repair-delta-v4-primary-cohort-binding/v1",
        "cohort": "primary",
        "queue_sha256": manifest["queue_sha256"],
        "queue_manifest_sha256": manifest["manifest_sha256"],
        "ordered_primary_candidate_ids": primary_ids,
        "ordered_primary_candidate_ids_sha256": canonical_sha256(primary_ids),
        "records": 60,
    }
    binding["binding_sha256"] = canonical_sha256(binding)
    return binding


def validate_v4_terminal_accounting(
    rows: list[Any], binding: dict[str, Any],
) -> None:
    """Require the canonical terminal input to partition all ordered primaries."""
    body = dict(binding) if isinstance(binding, dict) else {}
    claimed = body.pop("binding_sha256", None)
    expected = binding.get("ordered_primary_candidate_ids") if isinstance(binding, dict) else None
    if (
        claimed != canonical_sha256(body)
        or binding.get("schema_version")
        != "ganesh-mini-repair-delta-v4-primary-cohort-binding/v1"
        or binding.get("cohort") != "primary"
        or binding.get("records") != 60
        or not isinstance(expected, list) or len(expected) != 60
        or binding.get("ordered_primary_candidate_ids_sha256") != canonical_sha256(expected)
    ):
        raise AdmissionFailure("V4 primary cohort binding is malformed or unsealed")
    actual: list[Any] = []
    for row in rows:
        if (
            not isinstance(row, dict)
            or row.get("schema_version") != V4_ASSEMBLY_SCHEMA
            or row.get("status") not in {
                "ready-for-admission", "terminal-rejected", "unresolved",
            }
        ):
            raise AdmissionFailure("V4 final accounting requires canonical terminal artifacts")
        actual.append(row.get("candidate_id"))
    if actual != expected:
        if len(actual) != 60 or set(actual) != set(expected):
            raise AdmissionFailure("V4 terminal artifacts do not cover the exact 60-primary cohort")
        raise AdmissionFailure("V4 terminal artifacts do not preserve primary cohort order")


def validate_retry_ledger(
    value: Any, candidate_sha256: str, unresolved: bool,
    expected_bindings: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Validate the bounded identical-replay ledger emitted by evidence assembly."""
    if not isinstance(value, dict):
        raise AdmissionFailure("retry ledger is missing")
    body = dict(value)
    claimed = body.pop("ledger_sha256", None)
    attempts = value.get("attempts")
    if (
        claimed != canonical_sha256(body)
        or value.get("schema_version") != "ganesh-mini-repair-delta-retry-ledger/v1"
        or value.get("candidate_sha256") != candidate_sha256
        or value.get("maximum_attempts") != 2
        or value.get("unresolved") is not unresolved
        or value.get("evaluation_artifacts_read") != 0
        or not isinstance(attempts, list) or len(attempts) != 4
    ):
        raise AdmissionFailure("retry ledger is unsealed or unbound")
    expected = {
        (implementation, role)
        for implementation in ("reference", "known_bad")
        for role in ("primary_discrimination", "cross_cutting")
    }
    if expected_bindings is not None and (
        not isinstance(expected_bindings, dict)
        or set(expected_bindings) != {"reference", "known_bad"}
        or any(
            not isinstance(rows, dict)
            or set(rows) != {"primary_discrimination", "cross_cutting"}
            for rows in expected_bindings.values()
        )
    ):
        raise AdmissionFailure("retry ledger expected execution bindings are incomplete")
    observed: set[tuple[str, str]] = set()
    unresolved_rows = 0
    for row in attempts:
        if not isinstance(row, dict):
            raise AdmissionFailure("retry ledger attempt row is malformed")
        key = (row.get("implementation"), row.get("role"))
        runs = row.get("attempts")
        if key not in expected or key in observed or not isinstance(runs, list) or not 1 <= len(runs) <= 2:
            raise AdmissionFailure("retry ledger attempt coverage is malformed")
        observed.add(key)
        expected_binding = None
        if expected_bindings is not None:
            expected_binding = expected_bindings.get(str(key[0]), {}).get(str(key[1]))
            _validate_attempt_binding(expected_binding, f"retry ledger {key[0]}.{key[1]}")
        for index, run in enumerate(runs, 1):
            if (
                not isinstance(run, dict) or run.get("attempt") != index
                or not isinstance(run.get("result"), dict)
                or run.get("classification") is not None
                and not isinstance(run.get("classification"), str)
            ):
                raise AdmissionFailure("retry ledger run is malformed")
            if expected_binding is not None:
                binding = run.get("input_binding")
                _validate_attempt_binding(binding, f"retry ledger {key[0]}.{key[1]} attempt {index}")
                if binding != expected_binding:
                    raise AdmissionFailure("retry ledger replay input binding drifted")
                result = run["result"]
                if (
                    result.get("runtime_id") != binding["runtime_id"]
                    or result.get("image") != binding["image"]
                    or result.get("image_id") != binding["image_id"]
                    or result.get("manifest_digest") != binding["manifest_digest"]
                    or result.get("limits_sha256") != binding["limits_sha256"]
                    or result.get("commands") != binding["commands"]
                    or result.get("sandbox_contract_sha256") != binding["sandbox_contract_sha256"]
                    or result.get("staging", {}).get("staging_sha256") != binding["staging_sha256"]
                ):
                    raise AdmissionFailure("retry ledger result differs from its pinned execution input")
        final_unresolved = runs[-1].get("classification") is not None
        if final_unresolved and len(runs) != 2:
            raise AdmissionFailure("unresolved execution lacks its one identical replay")
        unresolved_rows += int(final_unresolved)
    if observed != expected or bool(unresolved_rows) is not unresolved:
        raise AdmissionFailure("retry ledger unresolved state is inconsistent")
    return value


def _validate_attempt_binding(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AdmissionFailure(f"{where}: execution input binding is missing")
    body = dict(value)
    claimed = body.pop("binding_sha256", None)
    required = {
        "schema_version", "implementation_sha256", "staged_files", "staged_files_sha256",
        "staging_sha256", "runtime_config_sha256", "runtime_id", "limits_sha256",
        "image", "image_id", "manifest_digest", "commands", "sandbox_contract_sha256",
    }
    if (
        set(body) != required
        or value.get("schema_version") != "ganesh-mini-repair-delta-execution-input/v1"
        or claimed != canonical_sha256(body)
        or value.get("staged_files_sha256") != canonical_sha256(value.get("staged_files"))
        or value.get("sandbox_contract_sha256") != sha256_object(SANDBOX_CONTRACT)
        or not isinstance(value.get("staged_files"), list)
        or not value["staged_files"]
        or any(
            not isinstance(item, dict)
            or set(item) != {"path", "sha256"}
            or not isinstance(item.get("path"), str) or not item["path"]
            for item in value["staged_files"]
        )
        or not isinstance(value.get("commands"), list) or not value["commands"]
    ):
        raise AdmissionFailure(f"{where}: execution input binding is malformed or unsealed")
    for field in (
        "implementation_sha256", "staged_files_sha256", "staging_sha256",
        "runtime_config_sha256", "limits_sha256",
    ):
        _sha(value.get(field), f"{where}.{field}")
    return value


def validate_assembly_artifact(
    value: Any, contract_id: str = CONTRACT_ID,
) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
    """Return disposition, optional envelope, and a content-free disposition row."""
    expected_schema = {
        V4_CONTRACT_ID: V4_ASSEMBLY_SCHEMA,
        V5_CONTRACT_ID: V5_ASSEMBLY_SCHEMA,
    }.get(contract_id, ASSEMBLY_SCHEMA)
    if not isinstance(value, dict) or value.get("schema_version") != expected_schema:
        raise AdmissionFailure("unsupported repair-delta evidence assembly artifact")
    body = dict(value)
    claimed = body.pop("artifact_sha256", None)
    status = value.get("status")
    identifier = value.get("candidate_id")
    if (
        claimed != canonical_sha256(body) or status not in {
            "ready-for-admission", "terminal-rejected", "unresolved",
        }
        or not isinstance(identifier, str) or not identifier
        or value.get("evaluation_artifacts_read") != 0
        or _sha(value.get("input_sha256"), "assembly input") != value.get("input_sha256")
    ):
        raise AdmissionFailure("evidence assembly artifact is unsealed or malformed")
    if status == "ready-for-admission":
        envelope = value.get("envelope")
        if not isinstance(envelope, dict) or envelope.get("candidate", {}).get("id") != identifier:
            raise AdmissionFailure("ready artifact does not bind its candidate envelope")
        candidate_sha = canonical_sha256(envelope["candidate"])
        executable = envelope.get("evidence", {}).get("executable", {})
        bindings = executable.get("attempt_bindings") if contract_id in {V4_CONTRACT_ID, V5_CONTRACT_ID} else None
        ledger = validate_retry_ledger(
            value.get("retry_ledger"), candidate_sha, False, bindings,
        )
        if executable.get("retry_ledger_sha256") != ledger["ledger_sha256"]:
            raise AdmissionFailure("executable evidence does not bind the retry ledger")
        return "ready", envelope, {"id": identifier}
    evidence = value.get("evidence")
    cell = value.get("cell_id")
    stage = value.get("terminal_stage")
    reason = value.get("reason")
    if (
        not isinstance(evidence, dict) or not evidence
        or not isinstance(cell, str) or not cell
        or not isinstance(stage, str) or not stage
        or not isinstance(reason, str) or not reason
    ):
        raise AdmissionFailure("terminal artifact lacks its bound disposition evidence")
    for name, item in evidence.items():
        if name != "retry_ledger":
            _sealed(item, name)
    if status == "unresolved":
        if contract_id == V4_CONTRACT_ID and stage == "post_teacher_preflight":
            from scripts.data.repair_delta_v4_preflight import (  # noqa: PLC0415
                validate_preflight_outcome_evidence,
            )
            outcome = evidence.get("post_teacher_preflight")
            validate_preflight_outcome_evidence(outcome)
            if outcome.get("status") != "unresolved":
                raise AdmissionFailure("V4 preflight unresolved artifact has inconsistent evidence")
            return status, None, {
                "id": identifier, "cell_id": cell, "terminal_stage": stage, "reason": reason,
            }
        if contract_id == V5_CONTRACT_ID and stage == "interface_preflight":
            outcome = evidence.get("interface_preflight")
            if not isinstance(outcome, dict) or outcome.get("status") != "unresolved":
                raise AdmissionFailure("V5 interface preflight unresolved artifact has inconsistent evidence")
            return status, None, {
                "id": identifier, "cell_id": cell, "terminal_stage": stage, "reason": reason,
            }
        executable = evidence.get("executable")
        if not isinstance(executable, dict):
            raise AdmissionFailure("unresolved artifact lacks executable evidence")
        bindings = executable.get("attempt_bindings") if contract_id in {V4_CONTRACT_ID, V5_CONTRACT_ID} else None
        ledger = validate_retry_ledger(
            evidence.get("retry_ledger"), executable.get("candidate_sha256"), True, bindings,
        )
        if executable.get("retry_ledger_sha256") != ledger["ledger_sha256"]:
            raise AdmissionFailure("unresolved executable does not bind the retry ledger")
    elif "retry_ledger" in evidence:
        if contract_id not in {V4_CONTRACT_ID, V5_CONTRACT_ID} or stage != "final_admission":
            raise AdmissionFailure("terminal semantic rejection unexpectedly contains a retry ledger")
        executable = evidence.get("executable")
        if not isinstance(executable, dict):
            raise AdmissionFailure("final-admission rejection lacks executable evidence")
        bindings = executable.get("attempt_bindings")
        ledger = validate_retry_ledger(
            evidence.get("retry_ledger"), executable.get("candidate_sha256"), False, bindings,
        )
        if executable.get("retry_ledger_sha256") != ledger["ledger_sha256"]:
            raise AdmissionFailure("final-admission rejection does not bind the retry ledger")
    if contract_id == V4_CONTRACT_ID and stage == "post_teacher_preflight":
        from scripts.data.repair_delta_v4_preflight import (  # noqa: PLC0415
            validate_preflight_outcome_evidence,
        )
        outcome = evidence.get("post_teacher_preflight")
        validate_preflight_outcome_evidence(outcome)
        if outcome.get("status") != "terminal-rejected":
            raise AdmissionFailure("V4 preflight rejection has inconsistent evidence")
    if contract_id == V5_CONTRACT_ID and stage == "interface_preflight":
        outcome = evidence.get("interface_preflight")
        if not isinstance(outcome, dict) or outcome.get("status") != "terminal-rejected":
            raise AdmissionFailure("V5 interface preflight rejection has inconsistent evidence")
    return status, None, {"id": identifier, "cell_id": cell, "terminal_stage": stage, "reason": reason}


def _sha(value: Any, where: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise AdmissionFailure(f"{where}: expected lowercase SHA-256")
    return value


def _sealed(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AdmissionFailure(f"{where}: expected sealed object")
    body = dict(value)
    claimed = body.pop("evidence_sha256", None)
    if claimed != canonical_sha256(body):
        raise AdmissionFailure(f"{where}: evidence seal mismatch")
    return value


def _runtime(runtime_path: Path, candidate: dict[str, Any]) -> tuple[dict[str, Any], str]:
    payload = runtime_path.read_bytes()
    document = json.loads(payload)
    task = candidate["verification_task"]
    runtime = document.get("runtimes", {}).get(task["runtime_id"]) if isinstance(document, dict) else None
    if (
        document.get("schema_version") != "3.0"
        or document.get("platform") != "linux/amd64"
        or not isinstance(runtime, dict)
        or runtime.get("language") != candidate["lane"]
        or runtime.get("candidate_path") != task["candidate_path"]
        or runtime.get("platform") != "linux/amd64"
    ):
        raise AdmissionFailure("runtime config does not bind the candidate lane and path")
    return runtime, hashlib.sha256(payload).hexdigest()


def validate_runtime_harness_closure(runtime_path: Path) -> dict[str, str]:
    """Prove every qualification lane's pinned command consumes its staged test."""
    document = json.loads(runtime_path.read_text(encoding="utf-8"))
    runtimes = document.get("runtimes") if isinstance(document, dict) else None
    if (
        document.get("schema_version") != "3.0"
        or document.get("platform") != "linux/amd64"
        or not isinstance(runtimes, dict)
    ):
        raise AdmissionFailure("runtime harness closure requires the pinned linux/amd64 contract")
    lane_runtimes: dict[str, str] = {}
    for runtime_id, runtime in runtimes.items():
        if not isinstance(runtime, dict):
            raise AdmissionFailure("runtime harness closure contains a malformed runtime")
        lane = runtime.get("language")
        if lane not in CANONICAL_TEST_PATHS or lane in lane_runtimes:
            raise AdmissionFailure("runtime harness closure has an unknown or duplicate lane")
        if runtime.get("platform") != "linux/amd64" or not isinstance(runtime.get("candidate_path"), str):
            raise AdmissionFailure("runtime harness closure is not platform/path bound")
        commands = runtime.get("commands")
        if not isinstance(commands, list) or not commands or any(
            not isinstance(command, list) or not command or any(not isinstance(arg, str) for arg in command)
            for command in commands
        ):
            raise AdmissionFailure("runtime harness closure has malformed commands")
        canonical_path = CANONICAL_TEST_PATHS[lane]
        consumes_path = any(canonical_path in argument for command in commands for argument in command)
        if lane == "go":
            consumes_path = canonical_path.endswith("_test.go") and ["go", "test", "./..."] in commands
        if not consumes_path:
            raise AdmissionFailure(f"runtime harness does not consume canonical {lane} test path")
        lane_runtimes[lane] = runtime_id
    if set(lane_runtimes) != set(CANONICAL_TEST_PATHS):
        raise AdmissionFailure("runtime harness closure does not cover all six lanes")
    return lane_runtimes


def staging_contract(
    candidate: dict[str, Any], role_row: dict[str, Any], runtime: dict[str, Any],
) -> dict[str, Any]:
    """Build the admission-recomputable binding for a byte-preserving role stage."""
    lane = candidate.get("lane")
    task = candidate["verification_task"]
    canonical_path = CANONICAL_TEST_PATHS.get(lane)
    if canonical_path is None or role_row.get("canonical_path") != canonical_path:
        raise AdmissionFailure("test role canonical path does not match its lane")
    value = {
        "schema_version": STAGING_SCHEMA,
        "candidate_sha256": canonical_sha256(candidate),
        "role": role_row.get("role"),
        "authored_content_sha256": role_row.get("file_sha256"),
        "logical_path": role_row.get("path"),
        "canonical_path": canonical_path,
        "runtime_id": task.get("runtime_id"),
        "candidate_path": task.get("candidate_path"),
        "commands": runtime.get("commands"),
    }
    value["suite_sha256"] = canonical_sha256(value)
    value["staging_sha256"] = canonical_sha256(value)
    return value


def stage_role_suite(
    candidate: dict[str, Any], role_row: dict[str, Any], runtime: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Copy one logical role file byte-for-byte to the lane's canonical path."""
    task = candidate["verification_task"]
    matches = [
        item for item in task["files"]
        if item.get("role") == "test" and item.get("path") == role_row.get("path")
    ]
    if len(matches) != 1 or matches[0].get("sha256") != role_row.get("file_sha256"):
        raise AdmissionFailure("logical role does not bind exactly one authored test file")
    staging = staging_contract(candidate, role_row, runtime)
    canonical_path = staging["canonical_path"]
    support = [item for item in task["files"] if item.get("role") == "support"]
    if any(item.get("path") == canonical_path for item in support):
        raise AdmissionFailure("support file collides with canonical staged test path")
    authored = matches[0]
    staged = copy.deepcopy(authored)
    staged["path"] = canonical_path
    if staged.get("content") != authored.get("content") or staged.get("sha256") != authored.get("sha256"):
        raise AdmissionFailure("canonical staging changed authored test bytes")
    suite_task = copy.deepcopy(task)
    suite_task["surface"] = "synthetic_harness"
    suite_task["files"] = [*copy.deepcopy(support), staged]
    return suite_task, staging


def execution_attempt_binding(
    candidate: dict[str, Any], role_row: dict[str, Any], runtime: dict[str, Any],
    runtime_config_sha256: str, implementation_code: str,
) -> dict[str, Any]:
    """Build the immutable byte/runtime boundary shared by an execution replay."""
    suite_task, staging = stage_role_suite(candidate, role_row, runtime)
    staged_files = [
        {"path": item["path"], "sha256": sha256_text(item["content"])}
        for item in suite_task["files"]
    ]
    value = {
        "schema_version": "ganesh-mini-repair-delta-execution-input/v1",
        "implementation_sha256": sha256_text(implementation_code),
        "staged_files": staged_files,
        "staged_files_sha256": canonical_sha256(staged_files),
        "staging_sha256": staging["staging_sha256"],
        "runtime_config_sha256": runtime_config_sha256,
        "runtime_id": candidate["verification_task"]["runtime_id"],
        "limits_sha256": canonical_sha256(candidate["verification_task"]["limits"]),
        "image": f"{str(runtime['image']).rsplit(':', 1)[0]}@{runtime['manifest_digest']}",
        "image_id": runtime["image_id"],
        "manifest_digest": runtime["manifest_digest"],
        "commands": copy.deepcopy(runtime["commands"]),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
    }
    value["binding_sha256"] = canonical_sha256(value)
    return value


def _visibility(evidence: dict[str, Any], expected: dict[str, Any], where: str) -> None:
    visibility = evidence.get("visibility")
    if not isinstance(visibility, dict) or visibility != expected:
        raise AdmissionFailure(f"{where}: visibility contract mismatch")


def _test_roles(candidate: dict[str, Any], evidence: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    rows = evidence.get("test_roles")
    if not isinstance(rows, list):
        raise AdmissionFailure("test_author.test_roles must be an array")
    tests = {
        item["path"]: item for item in candidate["verification_task"]["files"]
        if item.get("role") == "test"
    }
    by_role: dict[str, list[dict[str, Any]]] = {"primary_discrimination": [], "cross_cutting": []}
    seen_paths: set[str] = set()
    seen_cases: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "path", "canonical_path", "file_sha256", "role", "case_ids",
            "valid_domain_only", "scheduled_dimension_only",
        }:
            raise AdmissionFailure("test role entry differs from the frozen contract")
        role = row.get("role")
        path = row.get("path")
        cases = row.get("case_ids")
        if (
            role not in by_role or path not in tests or path in seen_paths
            or row.get("canonical_path") != CANONICAL_TEST_PATHS.get(candidate.get("lane"))
            or row.get("file_sha256") != tests[path]["sha256"]
            or not isinstance(cases, list) or not cases
            or len(set(cases)) != len(cases)
            or any(not isinstance(case, str) or not case or case in seen_cases for case in cases)
        ):
            raise AdmissionFailure("test roles do not bind unique hashed test files and cases")
        if role == "primary_discrimination" and (
            row.get("valid_domain_only") is not True or row.get("scheduled_dimension_only") is not False
        ):
            raise AdmissionFailure("primary-discrimination cases must be valid-domain and capability-specific")
        if role == "cross_cutting" and (
            row.get("valid_domain_only") is not False or row.get("scheduled_dimension_only") is not True
        ):
            raise AdmissionFailure("cross-cutting cases must isolate the scheduled dimension")
        seen_paths.add(path)
        seen_cases.update(cases)
        by_role[role].append(row)
    if seen_paths != set(tests) or any(len(by_role[role]) != 1 for role in by_role):
        raise AdmissionFailure("each role must contain exactly one logical executable test file")
    if len(by_role["primary_discrimination"][0]["case_ids"]) < 2:
        raise AdmissionFailure("at least two primary-discrimination cases are required")
    if sum(len(row["case_ids"]) for row in by_role["cross_cutting"]) < 1:
        raise AdmissionFailure("at least one cross-cutting case is required")
    return by_role


def suite_sha256(candidate: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    task = candidate["verification_task"]
    return canonical_sha256({
        "candidate_id": candidate["id"], "runtime_id": task["runtime_id"],
        "candidate_path": task["candidate_path"], "limits": task["limits"],
        "files": [{"path": row["path"], "sha256": row["file_sha256"]} for row in rows],
    })


def teacher_candidate_sha256(candidate: dict[str, Any]) -> str:
    """Reconstruct the candidate boundary before independent tests were added."""
    pretest = copy.deepcopy(candidate)
    pretest["verification_task"]["files"] = [
        item for item in pretest["verification_task"]["files"] if item.get("role") != "test"
    ]
    return canonical_sha256(pretest)


def _execution_result(
    result: Any, expected_staging: dict[str, Any], runtime: dict[str, Any], limits_sha256: str,
    expected_runtime_id: str, should_pass: bool, where: str,
    require_pinned_commands: bool = False,
) -> None:
    expected_image = f"{str(runtime['image']).rsplit(':', 1)[0]}@{runtime['manifest_digest']}"
    if (
        not isinstance(result, dict)
        or result.get("staging") != expected_staging
        or result.get("suite_sha256") != expected_staging["suite_sha256"]
        or result.get("runtime_id") != expected_runtime_id
        or result.get("image") != expected_image
        or result.get("image_id") != runtime.get("image_id")
        or result.get("manifest_digest") != runtime.get("manifest_digest")
        or result.get("sandbox_contract_sha256") != sha256_object(SANDBOX_CONTRACT)
        or result.get("limits_sha256") != limits_sha256
        or require_pinned_commands and result.get("commands") != runtime.get("commands")
        or not isinstance(result.get("exit_codes"), list)
    ):
        raise AdmissionFailure(f"{where}: executable evidence binding mismatch or infrastructure failure")
    if result.get("timed_out") is True or not result["exit_codes"]:
        raise UnresolvedEvidence(f"{where}: unresolved verifier infrastructure evidence")
    if result.get("timed_out") is not False:
        raise AdmissionFailure(f"{where}: timed_out must be explicit")
    passed = all(code == 0 for code in result["exit_codes"])
    if passed is not should_pass:
        expectation = "pass" if should_pass else "fail"
        raise AdmissionFailure(f"{where}: suite must {expectation}")


def validate_envelope(
    envelope: Any, admission_config: dict[str, Any], runtime_path: Path,
    separation_contract_sha256: str, contract_id: str = CONTRACT_ID,
    v4_preflight_config: Path | None = None,
) -> dict[str, Any]:
    if contract_id not in {CONTRACT_ID, V4_CONTRACT_ID, V5_CONTRACT_ID}:
        raise AdmissionFailure("unknown repair-delta contract")
    expected_envelope_schema = {
        V4_CONTRACT_ID: V4_ENVELOPE_SCHEMA,
        V5_CONTRACT_ID: V5_ENVELOPE_SCHEMA,
    }.get(contract_id, ENVELOPE_SCHEMA)
    if not isinstance(envelope, dict) or envelope.get("schema_version") != expected_envelope_schema:
        raise AdmissionFailure("unsupported repair-delta envelope")
    candidate = envelope.get("candidate")
    assignment = envelope.get("assignment")
    if not isinstance(candidate, dict) or not isinstance(assignment, dict):
        raise AdmissionFailure("candidate and assignment are required")
    validate_candidate(candidate, admission_config)
    if candidate["task_type"] != "repair" or candidate["verification_task"]["task_type"] != "repair":
        raise AdmissionFailure("v3 repair-delta lane accepts repair candidates only")
    primary = assignment.get("primary_capability")
    dimension = assignment.get("assigned_cross_cutting_dimension")
    if (
        assignment.get("contract_id") != contract_id
        or assignment.get("cell_id") != f"{primary}/{candidate['lane']}/repair"
        or not isinstance(primary, str) or not primary
        or not isinstance(dimension, str) or not dimension
    ):
        raise AdmissionFailure("assignment does not bind the selected repair cell contract")
    candidate_sha = canonical_sha256(candidate)
    specification_sha = sha256_text(candidate["messages"][0]["content"])
    validation = candidate["verification_task"]["validation"]
    if len(validation["known_bad"]) != 1:
        raise AdmissionFailure("repair-delta candidate requires exactly one known-bad implementation")
    reference_sha = validation["reference"]["sha256"]
    known_bad_sha = validation["known_bad"][0]["sha256"]
    evidence = envelope.get("evidence")
    expected_evidence = {
        V4_CONTRACT_ID: V4_EVIDENCE_NAMES,
        V5_CONTRACT_ID: V5_EVIDENCE_NAMES,
    }.get(contract_id, EVIDENCE_NAMES)
    if not isinstance(evidence, dict) or set(evidence) != expected_evidence:
        raise AdmissionFailure("repair-delta evidence set is incomplete")
    sealed = {name: _sealed(evidence[name], name) for name in expected_evidence}
    for name, item in sealed.items():
        if name in {"teacher_proof", "post_teacher_preflight", "interface_preflight"}:
            continue
        if item.get("candidate_sha256") != candidate_sha:
            raise AdmissionFailure(f"{name}: candidate hash mismatch")

    proof = sealed["teacher_proof"]
    if (
        proof.get("candidate_id") != candidate["id"]
        or proof.get("teacher_candidate_sha256") != teacher_candidate_sha256(candidate)
        or proof.get("primary_capability") != primary
        or proof.get("assigned_cross_cutting_dimension") != dimension
    ):
        raise AdmissionFailure("teacher proof does not bind the assigned capability and dimension")
    for field in (
        "capability_operation", "defective_intermediate_or_decision", "valid_domain_counterexample",
        "minimal_capability_specific_patch", "scheduled_dimension_obligation",
    ):
        if not isinstance(proof.get(field), str) or not proof[field].strip():
            raise AdmissionFailure(f"teacher_proof.{field}: non-empty structural proof is required")
    for field in PROOF_BOOLEAN_OVERLAP:
        if type(proof.get(field)) is not bool:
            raise AdmissionFailure(f"teacher_proof.{field}: boolean required")

    if contract_id == V4_CONTRACT_ID:
        if v4_preflight_config is None:
            raise AdmissionFailure("V4 admission requires the sealed post-teacher preflight config")
        from scripts.data.repair_delta_v4_preflight import (  # noqa: PLC0415
            validate_post_teacher_preflight_evidence,
        )
        pretest_candidate = copy.deepcopy(candidate)
        pretest_candidate["verification_task"]["files"] = [
            item for item in pretest_candidate["verification_task"]["files"]
            if item.get("role") != "test"
        ]
        try:
            validate_post_teacher_preflight_evidence(
                pretest_candidate, assignment, proof, sealed["post_teacher_preflight"],
                runtime_path, v4_preflight_config,
            )
        except ValueError as exc:
            raise AdmissionFailure(f"post_teacher_preflight: {exc}") from exc
    elif contract_id == V5_CONTRACT_ID:
        if v4_preflight_config is None:
            raise AdmissionFailure("V5 admission requires the sealed interface preflight config")
        from scripts.data.repair_delta_v5_preflight import (  # noqa: PLC0415
            validate_v5_interface_preflight_evidence,
        )
        pretest_candidate = copy.deepcopy(candidate)
        pretest_candidate["verification_task"]["files"] = [
            item for item in pretest_candidate["verification_task"]["files"]
            if item.get("role") != "test"
        ]
        try:
            validate_v5_interface_preflight_evidence(
                sealed["interface_preflight"], pretest_candidate, assignment, v4_preflight_config,
            )
        except ValueError as exc:
            raise AdmissionFailure(f"interface_preflight: {exc}") from exc

    semantic = sealed["semantic_review"]
    if (
        semantic.get("specification_sha256") != specification_sha
        or semantic.get("known_bad_sha256") != known_bad_sha
        or semantic.get("primary_capability") != primary
        or semantic.get("assigned_cross_cutting_dimension") != dimension
        or any(semantic.get(field) is not True for field in SEMANTIC_BOOLEANS)
    ):
        raise AdmissionFailure("blind semantic review did not independently pass every measured boolean")
    _visibility(semantic, {
        "specification_visible": True, "embedded_known_bad_visible": True,
        "assigned_labels_visible": True, "teacher_proof_visible": False,
        "reference_visible": False, "tests_visible": False, "verifier_outputs_visible": False,
        "training_stimulus_visible": False, "source_dataset_visible": False,
        "v2_outcomes_visible": False, "evaluation_artifacts_read": 0,
    }, "semantic_review")
    if any(semantic[field] is not proof[field] for field in PROOF_BOOLEAN_OVERLAP):
        raise AdmissionFailure("deterministic proof-consistency check found a semantic/proof disagreement")

    test_author = sealed["test_author"]
    if (
        test_author.get("specification_sha256") != specification_sha
        or test_author.get("known_bad_sha256") != known_bad_sha
        or test_author.get("primary_capability") != primary
        or test_author.get("assigned_cross_cutting_dimension") != dimension
    ):
        raise AdmissionFailure("test-author evidence does not bind specification and embedded known-bad")
    _visibility(test_author, {
        "specification_visible": True, "embedded_known_bad_visible": True,
        "capability_definition_visible": True, "scheduled_dimension_visible": True,
        "reference_visible": False, "teacher_proof_visible": False,
        "semantic_review_visible": False, "verifier_outputs_visible": False,
        "evaluation_artifacts_read": 0,
    }, "test_author")
    roles = _test_roles(candidate, test_author)

    delta = sealed["delta_audit"]
    if (
        delta.get("specification_sha256") != specification_sha
        or delta.get("reference_sha256") != reference_sha
        or delta.get("known_bad_sha256") != known_bad_sha
        or delta.get("primary_capability") != primary
        or delta.get("assigned_cross_cutting_dimension") != dimension
        or delta.get("independent_semantic_delta_count") != 1
        or delta.get("delta_is_capability_specific") is not True
        or delta.get("introduces_multiple_independent_fixes") is not False
        or not isinstance(delta.get("delta_description"), str) or not delta["delta_description"].strip()
    ):
        raise AdmissionFailure("delta auditor did not confirm exactly one capability-specific bug")
    _visibility(delta, {
        "specification_visible": True, "embedded_known_bad_visible": True,
        "reference_visible": True, "assigned_labels_visible": True,
        "tests_visible": False, "verifier_outputs_visible": False,
        "teacher_proof_visible": False, "training_stimulus_visible": False,
        "v2_outcomes_visible": False, "evaluation_artifacts_read": 0,
    }, "delta_audit")

    separation = sealed["separation"]
    _sha(separation_contract_sha256, "separation contract")
    if (
        separation.get("comparison_contract_sha256") != separation_contract_sha256
        or not isinstance(separation.get("comparison_manifest_sha256"), str)
        or len(separation["comparison_manifest_sha256"]) != 64
        or any(char not in "0123456789abcdef" for char in separation["comparison_manifest_sha256"])
        or any(separation.get(field) is not True for field in SEPARATION_PASSES)
        or separation.get("evaluation_artifacts_read_by_construction") != 0
    ):
        raise AdmissionFailure("unchanged content-free separation contract did not pass")

    runtime, runtime_config_sha = _runtime(runtime_path, candidate)
    validate_runtime_harness_closure(runtime_path)
    executable = sealed["executable"]
    task = candidate["verification_task"]
    limits_sha = canonical_sha256(task["limits"])
    if (
        executable.get("runtime_config_sha256") != runtime_config_sha
        or executable.get("reference_sha256") != reference_sha
        or executable.get("known_bad_sha256") != known_bad_sha
        or executable.get("sandbox_contract_sha256") != sha256_object(SANDBOX_CONTRACT)
    ):
        raise AdmissionFailure("executable evidence does not bind the unchanged runtime and sandbox")
    if contract_id in {V4_CONTRACT_ID, V5_CONTRACT_ID}:
        expected_attempt_bindings: dict[str, dict[str, dict[str, Any]]] = {
            "reference": {}, "known_bad": {},
        }
        implementations = {
            "reference": validation["reference"]["code"],
            "known_bad": validation["known_bad"][0]["code"],
        }
        for implementation, code in implementations.items():
            for role in ("primary_discrimination", "cross_cutting"):
                expected_attempt_bindings[implementation][role] = execution_attempt_binding(
                    candidate, roles[role][0], runtime, runtime_config_sha, code,
                )
        if executable.get("attempt_bindings") != expected_attempt_bindings:
            raise AdmissionFailure("executable evidence does not bind the exact V4 replay inputs")
    results = executable.get("results")
    if not isinstance(results, dict) or set(results) != {"reference", "known_bad"}:
        raise AdmissionFailure("executable suite results are incomplete")
    for implementation, should_primary_pass, should_cross_pass in (
        ("reference", True, True), ("known_bad", False, True),
    ):
        suites = results.get(implementation)
        if not isinstance(suites, dict) or set(suites) != {"primary_discrimination", "cross_cutting"}:
            raise AdmissionFailure(f"{implementation}: split suite evidence is incomplete")
        _execution_result(
            suites["primary_discrimination"], staging_contract(candidate, roles["primary_discrimination"][0], runtime),
            runtime, limits_sha, task["runtime_id"], should_primary_pass, f"{implementation}.primary_discrimination",
            contract_id in {V4_CONTRACT_ID, V5_CONTRACT_ID},
        )
        _execution_result(
            suites["cross_cutting"], staging_contract(candidate, roles["cross_cutting"][0], runtime),
            runtime, limits_sha, task["runtime_id"], should_cross_pass, f"{implementation}.cross_cutting",
            contract_id in {V4_CONTRACT_ID, V5_CONTRACT_ID},
        )

    lineage = sealed["lineage"]
    source = candidate["source"]
    if (
        lineage.get("source_identity") != {key: source.get(key) for key in ("dataset", "revision", "record_id")}
        or lineage.get("contract_id") != contract_id
        or lineage.get("cell_id") != assignment["cell_id"]
        or lineage.get("source_record_sha256") != source.get("source_record_sha256")
        or lineage.get("complete") is not True
        or lineage.get("teacher_proof_evidence_sha256") != proof["evidence_sha256"]
        or lineage.get("semantic_review_evidence_sha256") != semantic["evidence_sha256"]
        or lineage.get("test_author_evidence_sha256") != test_author["evidence_sha256"]
        or lineage.get("delta_audit_evidence_sha256") != delta["evidence_sha256"]
        or lineage.get("separation_evidence_sha256") != separation["evidence_sha256"]
        or lineage.get("executable_evidence_sha256") != executable["evidence_sha256"]
        or (
            contract_id == V4_CONTRACT_ID
            and lineage.get("post_teacher_preflight_evidence_sha256")
            != sealed["post_teacher_preflight"]["evidence_sha256"]
        )
        or (
            contract_id == V5_CONTRACT_ID
            and lineage.get("interface_preflight_evidence_sha256")
            != sealed["interface_preflight"]["evidence_sha256"]
        )
    ):
        raise AdmissionFailure("lineage evidence chain is incomplete or mismatched")
    return {
        "schema_version": {
            V4_CONTRACT_ID: V4_OUTPUT_SCHEMA,
            V5_CONTRACT_ID: V5_OUTPUT_SCHEMA,
        }.get(contract_id, OUTPUT_SCHEMA),
        "id": candidate["id"], "cell_id": assignment["cell_id"],
        "lane": candidate["lane"], "primary_capability": primary,
        "assigned_cross_cutting_dimension": dimension, "candidate": candidate,
        "evidence_sha256s": {name: sealed[name]["evidence_sha256"] for name in sorted(sealed)},
        "proof_consistency_sha256": canonical_sha256({
            field: {"teacher": proof[field], "reviewer": semantic[field]}
            for field in PROOF_BOOLEAN_OVERLAP
        }),
    }


def admit(
    envelopes: list[Any], admission_config: dict[str, Any], runtime_path: Path,
    separation_contract_sha256: str, unresolved: list[dict[str, Any]] | None = None,
    contract_id: str = CONTRACT_ID, v4_preflight_config: Path | None = None,
    v4_cohort_binding: dict[str, Any] | None = None,
    v5_cohort_binding: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if contract_id == V4_CONTRACT_ID and v4_cohort_binding is not None:
        validate_v4_terminal_accounting(envelopes, v4_cohort_binding)
    if contract_id == V5_CONTRACT_ID:
        if v5_cohort_binding is None:
            raise AdmissionFailure("V5 admission requires a sealed cohort binding")
        try:
            validate_v5_terminal_order(
                envelopes, v5_cohort_binding["ordered_candidate_ids"], V5_ASSEMBLY_SCHEMA,
            )
        except (KeyError, ValueError) as exc:
            raise AdmissionFailure(str(exc)) from exc
    admitted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line, input_row in enumerate(envelopes, 1):
        identifier = input_row.get("candidate_id", input_row.get("candidate", {}).get("id", f"line-{line}")) if isinstance(input_row, dict) else f"line-{line}"
        try:
            envelope = input_row
            measured: dict[str, Any] | None = None
            assembly_schema = {
                V4_CONTRACT_ID: V4_ASSEMBLY_SCHEMA,
                V5_CONTRACT_ID: V5_ASSEMBLY_SCHEMA,
            }.get(contract_id, ASSEMBLY_SCHEMA)
            if isinstance(input_row, dict) and input_row.get("schema_version") == assembly_schema:
                disposition, envelope, measured = validate_assembly_artifact(input_row, contract_id)
                if identifier in seen:
                    raise AdmissionFailure("duplicate repair-delta candidate ID")
                seen.add(identifier)
                if disposition == "terminal-rejected":
                    rejected.append({"line": line, **measured})
                    continue
                if disposition == "unresolved":
                    if unresolved is None:
                        raise UnresolvedEvidence(measured["reason"])
                    unresolved.append({"line": line, **measured})
                    continue
                if envelope is None:
                    raise AdmissionFailure("ready evidence assembly artifact lacks an envelope")
            row = validate_envelope(
                envelope, admission_config, runtime_path, separation_contract_sha256,
                contract_id, v4_preflight_config,
            )
            if measured is None and row["id"] in seen:
                raise AdmissionFailure("duplicate repair-delta candidate ID")
            if measured is None:
                seen.add(row["id"])
            admitted.append(row)
        except UnresolvedEvidence as exc:
            if unresolved is None:
                raise
            unresolved.append({"line": line, "id": identifier, "reason": str(exc)})
        except (AdmissionFailure, KeyError, TypeError, ValueError) as exc:
            rejected.append({"line": line, "id": identifier, "reason": str(exc)})
    if contract_id == V4_CONTRACT_ID and v4_cohort_binding is not None:
        unresolved_count = len(unresolved) if unresolved is not None else 0
        if len(admitted) + len(rejected) + unresolved_count != 60:
            raise AdmissionFailure(
                "V4 admitted, rejected, and unresolved dispositions do not reconcile to 60"
            )
    if contract_id == V5_CONTRACT_ID and v5_cohort_binding is not None:
        expected = v5_cohort_binding["records"]
        unresolved_count = len(unresolved) if unresolved is not None else 0
        if len(admitted) + len(rejected) + unresolved_count != expected:
            raise AdmissionFailure(
                "V5 admitted, rejected, and unresolved dispositions do not reconcile to bound cohort"
            )
    return admitted, rejected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("configs/data/expansion_v1.json"))
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--separation-contract-sha256", required=True)
    parser.add_argument("--contract-version", choices=("v3", "v4", "v5"), default="v3")
    parser.add_argument("--v4-preflight-config", type=Path)
    parser.add_argument("--v5-preflight-config", type=Path)
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--queue-manifest", type=Path)
    parser.add_argument("--cohort", choices=("primary", "reserve"))
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--source-feasibility-addendum", type=Path)
    parser.add_argument("--budget-clarification-addendum", type=Path)
    parser.add_argument("--exclusion-ledger", type=Path)
    parser.add_argument("--carry-manifest", type=Path)
    parser.add_argument("--source-manifest", type=Path)
    parser.add_argument("--cohort-manifest", type=Path)
    parser.add_argument("--reserve-eligibility", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rejected-output", type=Path, required=True)
    parser.add_argument("--unresolved-output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    rows = read_jsonl(args.input)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    unresolved: list[dict[str, Any]] = []
    contract_id = {
        "v3": CONTRACT_ID, "v4": V4_CONTRACT_ID, "v5": V5_CONTRACT_ID,
    }[args.contract_version]
    if contract_id == V4_CONTRACT_ID and args.v4_preflight_config is None:
        parser.error("--v4-preflight-config is required for --contract-version v4")
    v4_cohort_binding = None
    v5_cohort_binding = None
    if contract_id == V4_CONTRACT_ID:
        if args.queue is None or args.queue_manifest is None or args.cohort is None:
            parser.error("--queue, --queue-manifest, and --cohort are required for --contract-version v4")
        try:
            v4_cohort_binding = load_v4_primary_cohort_binding(
                args.queue, args.queue_manifest, args.cohort,
            )
        except AdmissionFailure as exc:
            parser.error(str(exc))
    if contract_id == V5_CONTRACT_ID:
        required = {
            "--plan": args.plan,
            "--source-feasibility-addendum": args.source_feasibility_addendum,
            "--budget-clarification-addendum": args.budget_clarification_addendum,
            "--exclusion-ledger": args.exclusion_ledger,
            "--carry-manifest": args.carry_manifest,
            "--source-manifest": args.source_manifest,
            "--cohort-manifest": args.cohort_manifest,
            "--cohort": args.cohort,
            "--v5-preflight-config": args.v5_preflight_config,
        }
        missing = [name for name, value in required.items() if value is None]
        if missing:
            parser.error(f"V5 requires {', '.join(missing)}")
        try:
            v5_contract = load_v5_contract(
                plan_path=args.plan,
                source_addendum_path=args.source_feasibility_addendum,
                budget_addendum_path=args.budget_clarification_addendum,
                exclusion_path=args.exclusion_ledger,
                carry_path=args.carry_manifest,
                source_path=args.source_manifest,
                cohort_path=args.cohort_manifest,
            )
            v5_cohort_binding = make_v5_cohort_binding(
                v5_contract, args.cohort, args.reserve_eligibility,
            )
        except ValueError as exc:
            parser.error(str(exc))
    admitted, rejected = admit(
        rows, config, args.runtime_config, args.separation_contract_sha256, unresolved,
        contract_id,
        args.v5_preflight_config if contract_id == V5_CONTRACT_ID else args.v4_preflight_config,
        v4_cohort_binding, v5_cohort_binding,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(b"".join(canonical_json(row) + b"\n" for row in admitted))
    args.rejected_output.parent.mkdir(parents=True, exist_ok=True)
    args.rejected_output.write_text(json.dumps(rejected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.unresolved_output.parent.mkdir(parents=True, exist_ok=True)
    args.unresolved_output.write_text(json.dumps(unresolved, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report: dict[str, Any] = {
        "schema_version": {
            V4_CONTRACT_ID: V4_REPORT_SCHEMA,
            V5_CONTRACT_ID: V5_REPORT_SCHEMA,
        }.get(contract_id, REPORT_SCHEMA),
        "status": "admission-complete" if not rejected and not unresolved else "failed",
        "contract_id": contract_id,
        "input": {"path": str(args.input), "bytes": args.input.stat().st_size, "sha256": hashlib.sha256(args.input.read_bytes()).hexdigest()},
        "runtime_config_sha256": hashlib.sha256(args.runtime_config.read_bytes()).hexdigest(),
        "admission_config_sha256": hashlib.sha256(args.config.read_bytes()).hexdigest(),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        "separation_contract_sha256": args.separation_contract_sha256,
        "accepted": len(admitted), "rejected": len(rejected), "unresolved": len(unresolved),
        "counts_by_lane": dict(sorted(Counter(row["lane"] for row in admitted).items())),
        "evaluation_artifacts_read": 0,
        "outputs": {
            "admitted": {"path": str(args.output), "bytes": args.output.stat().st_size, "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()},
            "rejected": {"path": str(args.rejected_output), "bytes": args.rejected_output.stat().st_size, "sha256": hashlib.sha256(args.rejected_output.read_bytes()).hexdigest()},
            "unresolved": {"path": str(args.unresolved_output), "bytes": args.unresolved_output.stat().st_size, "sha256": hashlib.sha256(args.unresolved_output.read_bytes()).hexdigest()},
        },
    }
    if contract_id == V4_CONTRACT_ID:
        report["v4_primary_cohort_binding"] = v4_cohort_binding
    elif contract_id == V5_CONTRACT_ID:
        report["v5_cohort_binding"] = v5_cohort_binding
    report["report_sha256"] = canonical_sha256(report)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "accepted": len(admitted), "rejected": len(rejected), "unresolved": len(unresolved)}, sort_keys=True))
    return 0 if not rejected and not unresolved else 1


if __name__ == "__main__":
    raise SystemExit(main())
