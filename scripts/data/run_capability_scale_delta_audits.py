#!/usr/bin/env python3
"""Run resumable blind delta audits for capability-scale candidates.

This is a prospective Gate 3 controller.  It deliberately does not extend the
historical Gate 2 adapters: the scale campaign has its own input binding,
per-candidate artifacts, response schema, prompt, and aggregate report.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import json
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import (
    CodexInvocationFailure,
    invoke_codex,
    verify_codex_version,
)
from scripts.data.repair_delta_v7_readiness import (
    CANONICAL_LANE_INTERFACES,
    ROLES,
    validate_lane_interface,
)
from scripts.data.run_repair_delta_evidence import _delta_evidence, delta_projection
from scripts.eval.contracts import sha256_text


ARTIFACT_SCHEMA = "ganesh-mini-capability-scale-delta-audit-artifact/v1"
REPORT_SCHEMA = "ganesh-mini-capability-scale-delta-audit-report/v1"
RESPONSE_SCHEMA_ID = "ganesh-mini-capability-scale-delta-audit-response/v1"
InvokeFn = Callable[[dict[str, Any]], tuple[dict[str, Any], dict[str, Any]]]


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sealed(value: dict[str, Any], field: str, label: str) -> dict[str, Any]:
    body = dict(value)
    claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{label}: invalid {field}")
    return value


def _write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent,
        prefix=f".{path.name}.", suffix=".tmp", delete=False,
    ) as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        temporary = Path(handle.name)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _write_jsonl_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent,
        prefix=f".{path.name}.", suffix=".tmp", delete=False,
    ) as handle:
        handle.write("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
        temporary = Path(handle.name)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def response_schema() -> dict[str, Any]:
    boolean = {"type": "boolean"}
    properties = {
        "independent_semantic_delta_count": {"type": "integer", "minimum": 0},
        "delta_is_capability_specific": boolean,
        "introduces_multiple_independent_fixes": boolean,
        "delta_description": {"type": "string", "minLength": 1},
    }
    return {
        "$id": RESPONSE_SCHEMA_ID,
        "type": "object",
        "additionalProperties": False,
        "required": list(properties),
        "properties": properties,
    }


def delta_prompt(projection: dict[str, Any]) -> str:
    instruction = (
        "Blindly audit the known-bad/reference semantic delta using only this specification, "
        "the two implementations, and the assigned primary and cross-cutting labels. Determine "
        "the number of independent semantic fixes, whether the sole fix is specific to the "
        "assigned primary capability, and whether multiple independent fixes were introduced. "
        "You have not seen authored tests, teacher evidence, verifier output, source stimulus, "
        "training outcomes, or evaluation material. Do not use tools or inspect the filesystem. "
        "Return only the schema-constrained object."
    )
    return f"{instruction}\nInput: {json.dumps(projection, separators=(',', ':'), ensure_ascii=False)}"


def attach_tests(
    candidate: dict[str, Any], test_artifact: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate a canonical V7/V9 test-author artifact and attach both roles."""
    _sealed(test_artifact, "artifact_sha256", f"{candidate.get('id')}/test-author")
    identifier = candidate.get("id")
    candidate_sha = canonical_sha256(candidate)
    if (
        test_artifact.get("candidate_id") != identifier
        or test_artifact.get("status") != "structurally-valid"
        or test_artifact.get("evaluation_artifacts_read") != 0
        or test_artifact.get("candidate_sha256") != candidate_sha
    ):
        raise ValueError(f"{identifier}: test-author artifact does not bind the pre-test candidate")
    injection = test_artifact.get("injection")
    if not isinstance(injection, dict):
        raise ValueError(f"{identifier}: missing controller injection")
    injection_body = dict(injection)
    injection_claimed = injection_body.pop("injection_sha256", None)
    if injection_claimed != canonical_sha256(injection_body):
        raise ValueError(f"{identifier}: invalid injection seal")
    lane = candidate.get("lane")
    interface = CANONICAL_LANE_INTERFACES.get(str(lane))
    roles = injection.get("roles")
    if (
        injection.get("lane") != lane
        or injection.get("interface") != interface
        or not isinstance(roles, list)
        or [row.get("role") for row in roles] != list(ROLES)
    ):
        raise ValueError(f"{identifier}: canonical lane/role injection drift")

    attached = copy.deepcopy(candidate)
    support = [row for row in attached["verification_task"]["files"] if row.get("role") == "support"]
    files: list[dict[str, Any]] = []
    test_roles: list[dict[str, Any]] = []
    for ordinal, row in enumerate(roles, start=1):
        role = ROLES[ordinal - 1]
        required = {
            "role", "logical_path", "canonical_execution_path", "candidate_path",
            "commands", "content", "case_ids", "raw_role_sha256", "injected_path_sha256",
        }
        if not isinstance(row, dict) or set(row) != required:
            raise ValueError(f"{identifier}/{role}: injected role shape drift")
        expected_logical = f"roles/{ordinal:02d}-{role}/{interface['test_path']}"
        if (
            row["logical_path"] != expected_logical
            or row["canonical_execution_path"] != interface["test_path"]
            or row["candidate_path"] != interface["candidate_path"]
            or row["commands"] != interface["commands"]
            or validate_lane_interface(str(lane), row["content"])
        ):
            raise ValueError(f"{identifier}/{role}: canonical interface validation failed")
        minimum = 2 if role == "primary_discrimination" else 1
        cases = row["case_ids"]
        if (
            not isinstance(cases, list) or len(cases) < minimum
            or len(set(cases)) != len(cases)
            or any(not isinstance(case, str) or not case.strip() for case in cases)
        ):
            raise ValueError(f"{identifier}/{role}: invalid case IDs")
        content = row["content"].rstrip() + "\n"
        role_payload = {"content": row["content"], "case_ids": row["case_ids"]}
        path_payload = {
            "role": role, "logical_path": expected_logical,
            "canonical_execution_path": interface["test_path"],
            "candidate_path": interface["candidate_path"],
        }
        if (
            row["raw_role_sha256"] != canonical_sha256(role_payload)
            or row["injected_path_sha256"] != canonical_sha256(path_payload)
        ):
            raise ValueError(f"{identifier}/{role}: injected role hash drift")
        digest = sha256_text(content)
        files.append({"path": expected_logical, "role": "test", "content": content, "sha256": digest})
        test_roles.append({
            "path": expected_logical, "canonical_path": interface["test_path"],
            "file_sha256": digest, "role": role, "case_ids": list(cases),
            "valid_domain_only": role == "primary_discrimination",
            "scheduled_dimension_only": role == "cross_cutting",
        })
    attached["verification_task"]["files"] = [*support, *files]
    evidence = {
        "schema_version": "ganesh-mini-capability-scale-test-attachment/v1",
        "candidate_id": identifier,
        "pre_test_candidate_sha256": candidate_sha,
        "candidate_sha256": canonical_sha256(attached),
        "test_author_artifact_sha256": test_artifact["artifact_sha256"],
        "injection_sha256": injection_claimed,
        "test_roles": test_roles,
        "evaluation_artifacts_read": 0,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return attached, evidence


def _lineage(candidate: dict[str, Any]) -> dict[str, Any]:
    assignment = candidate.get("qualification_assignment", {})
    source = candidate.get("source", {})
    required = (
        "cell_id", "source_queue_id", "source_record_sha256",
        "queue_row_sha256", "assignment_sha256",
    )
    if any(not isinstance(assignment.get(field), str) or not assignment[field] for field in required):
        raise ValueError(f"{candidate.get('id')}: incomplete sealed queue lineage")
    if source.get("source_record_sha256") != assignment["source_record_sha256"]:
        raise ValueError(f"{candidate.get('id')}: source record hash drift")
    return {field: assignment[field] for field in required}


def run_one(
    candidate: dict[str, Any], test_artifact: dict[str, Any], artifact_dir: Path,
    invocation_identity: dict[str, Any], invoke: InvokeFn,
) -> tuple[dict[str, Any], bool, dict[str, Any]]:
    attached, attachment = attach_tests(candidate, test_artifact)
    assignment = attached.get("qualification_assignment")
    if not isinstance(assignment, dict):
        raise ValueError(f"{candidate.get('id')}: missing qualification assignment")
    lineage = _lineage(attached)
    projection = delta_projection(attached, assignment)
    prompt = delta_prompt(projection)
    binding = {
        "candidate_sha256": canonical_sha256(attached),
        "test_attachment_evidence_sha256": attachment["evidence_sha256"],
        "projection": projection,
        "prompt_sha256": sha256_text(prompt),
        "response_schema_sha256": canonical_sha256(response_schema()),
        "invocation_identity": invocation_identity,
        "lineage": lineage,
        "evaluation_artifacts_read": 0,
    }
    input_sha = canonical_sha256(binding)
    identifier = str(attached["id"])
    path = artifact_dir / f"{identifier}.delta-audit.json"
    if path.exists():
        artifact = _sealed(json.loads(path.read_text(encoding="utf-8")), "artifact_sha256", str(path))
        if artifact.get("input_sha256") != input_sha:
            raise ValueError(f"{identifier}: sealed delta-audit input drift")
        return artifact, False, attached

    base = {
        "schema_version": ARTIFACT_SCHEMA,
        "candidate_id": identifier,
        "cell_id": assignment["cell_id"],
        "input_sha256": input_sha,
        "input_binding": binding,
        "lineage": lineage,
        "test_attachment": attachment,
        "evaluation_artifacts_read": 0,
    }
    try:
        response, run = invoke(projection)
    except CodexInvocationFailure as exc:
        failure = copy.deepcopy(exc.evidence)
        artifact = {
            **base, "status": "invocation-failed", "reason": str(exc),
            "failure": failure, "failure_sha256": canonical_sha256(failure),
        }
    except (TypeError, ValueError) as exc:
        artifact = {
            **base, "status": "response-contract-rejected",
            "reason": f"provider-output-contract: {exc}",
        }
    else:
        response = copy.deepcopy(response)
        run = copy.deepcopy(run)
        run_sha = canonical_sha256(run)
        try:
            evidence = _delta_evidence(attached, assignment, response, run_sha)
        except (TypeError, ValueError) as exc:
            artifact = {
                **base, "status": "response-contract-rejected", "reason": str(exc),
                "response": response, "response_sha256": canonical_sha256(response),
                "run": run, "run_evidence_sha256": run_sha,
            }
        else:
            passed = (
                evidence["independent_semantic_delta_count"] == 1
                and evidence["delta_is_capability_specific"] is True
                and evidence["introduces_multiple_independent_fixes"] is False
            )
            artifact = {
                **base,
                "status": "passed" if passed else "semantic-rejected",
                "response": response,
                "response_sha256": canonical_sha256(response),
                "run": run,
                "run_evidence_sha256": run_sha,
                "delta_evidence": evidence,
            }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    _write_json_atomic(path, artifact)
    return artifact, True, attached


def run(args: argparse.Namespace, invoke_factory: Callable[[dict[str, Any], str], InvokeFn] | None = None) -> dict[str, Any]:
    candidates = _jsonl(args.candidates)
    test_rows = _jsonl(args.test_author_artifacts)
    selection_report_path = getattr(args, "test_author_selection_report", None)
    selection_binding: dict[str, Any] | None = None
    if selection_report_path is not None:
        selection = _sealed(
            json.loads(selection_report_path.read_text(encoding="utf-8")),
            "report_sha256", str(selection_report_path),
        )
        if (
            selection.get("schema_version") != "ganesh-mini-capability-scale-stage-selection/v1"
            or selection.get("selected_rows_sha256") != canonical_sha256(test_rows)
            or selection.get("selected_ids") != [row.get("candidate_id") for row in test_rows]
            or selection.get("selected_artifact_sha256s")
            != [row.get("artifact_sha256") for row in test_rows]
            or selection.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError("test-author selection report does not bind selected artifacts")
        candidate_by_id = {candidate.get("id"): candidate for candidate in candidates}
        if any(identifier not in candidate_by_id for identifier in selection["selected_ids"]):
            raise ValueError("test-author selection differs from candidate input")
        candidates = [candidate_by_id[identifier] for identifier in selection["selected_ids"]]
        selection_binding = {
            "test_author_selection_report_sha256": selection["report_sha256"],
            "test_author_parent_report_sha256": selection["parent_report_sha256"],
        }
    tests_by_id = {row.get("candidate_id"): row for row in test_rows}
    candidate_ids = [candidate.get("id") for candidate in candidates]
    if (
        not candidates or len(tests_by_id) != len(test_rows)
        or len(set(candidate_ids)) != len(candidate_ids)
        or any(
            not isinstance(identifier, str) or not identifier
            or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in identifier)
            for identifier in candidate_ids
        )
        or set(tests_by_id) != set(candidate_ids)
    ):
        raise ValueError("teacher candidates and test-author artifacts are not a one-to-one cohort")
    upstream_report_binding: dict[str, Any] | None = None
    if args.test_author_report is not None:
        test_report = _sealed(
            json.loads(args.test_author_report.read_text(encoding="utf-8")),
            "report_sha256", str(args.test_author_report),
        )
        if (
            test_report.get("status") != "passed"
            or test_report.get("evaluation_artifacts_read") != 0
            or test_report.get("ordered_candidate_ids") != candidate_ids
            or test_report.get("terminal_rows_sha256") != canonical_sha256(test_rows)
        ):
            raise ValueError("test-author report is not a passing zero-evaluation-read seal")
        report_artifacts = test_report.get("terminal_artifact_sha256s")
        if report_artifacts != [tests_by_id[candidate["id"]]["artifact_sha256"] for candidate in candidates]:
            raise ValueError("test-author report artifact ordering/hash drift")
        upstream_report_binding = {
            "test_author_report_sha256": test_report["report_sha256"],
            "teacher_report_sha256": test_report.get("teacher_report_sha256"),
        }
    elif selection_binding is not None:
        upstream_report_binding = selection_binding

    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"]) if invoke_factory is None else "test-cli"
    schema = response_schema()
    invocation_identity = {
        "cli_identity": cli_identity,
        "config_sha256": canonical_sha256(config),
        "response_schema_sha256": canonical_sha256(schema),
    }
    args.run_dir.mkdir(parents=True, exist_ok=True)

    if invoke_factory is None:
        def invoke_factory(projection: dict[str, Any], prompt: str) -> InvokeFn:
            def call(_: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
                with tempfile.TemporaryDirectory(prefix="ganesh-scale-delta-") as temp_name:
                    schema_path = Path(temp_name) / "schema.json"
                    schema_path.write_text(json.dumps(schema, sort_keys=True) + "\n", encoding="utf-8")
                    return invoke_codex(
                        args.codex_bin, config, schema_path, prompt,
                        "capability-scale-delta-audit", str(projection["lane"]),
                    )
            return call

    results: list[tuple[dict[str, Any], bool, dict[str, Any]] | None] = [None] * len(candidates)

    def execute(index: int) -> tuple[int, tuple[dict[str, Any], bool, dict[str, Any]]]:
        candidate = candidates[index]
        projection = delta_projection(candidate, candidate["qualification_assignment"])
        prompt = delta_prompt(projection)
        invoke = invoke_factory(projection, prompt)
        return index, run_one(
            candidate, tests_by_id[candidate["id"]], args.run_dir,
            invocation_identity, invoke,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        for index, result in executor.map(execute, range(len(candidates))):
            results[index] = result
    completed = [row for row in results if row is not None]
    artifacts = [row[0] for row in completed]
    attached = [row[2] for row in completed]
    lineage_bindings = [row["lineage"] for row in artifacts]
    counts = dict(sorted(Counter(row["status"] for row in artifacts).items()))
    report = {
        "schema_version": REPORT_SCHEMA,
        "status": "passed" if counts == {"passed": len(candidates)} else "failed",
        "requested": len(candidates),
        "new_calls": sum(1 for row in completed if row[1]),
        "resumed": sum(1 for row in completed if not row[1]),
        "counts": counts,
        "candidate_sha256s": [canonical_sha256(row) for row in candidates],
        "test_author_artifact_sha256s": [tests_by_id[row["id"]]["artifact_sha256"] for row in candidates],
        "terminal_artifact_sha256s": [row["artifact_sha256"] for row in artifacts],
        "lineage_bindings": lineage_bindings,
        "lineage_bindings_sha256": canonical_sha256(lineage_bindings),
        "attached_candidates_sha256": canonical_sha256(attached),
        "rows_sha256": canonical_sha256(artifacts),
        "invocation_identity": invocation_identity,
        "upstream_report_binding": upstream_report_binding,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_jsonl_atomic(args.output_dir / "attached-candidates.jsonl", attached)
    _write_jsonl_atomic(args.output_dir / "delta-terminal-artifacts.jsonl", artifacts)
    _write_json_atomic(args.output_dir / "delta-audit-report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--test-author-artifacts", type=Path, required=True)
    parser.add_argument("--test-author-report", type=Path)
    parser.add_argument("--test-author-selection-report", type=Path)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = run(args)
    print(json.dumps({
        "status": report["status"], "counts": report["counts"],
        "new_calls": report["new_calls"], "resumed": report["resumed"],
        "report_sha256": report["report_sha256"],
    }, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
