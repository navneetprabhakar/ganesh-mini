#!/usr/bin/env python3
"""Run resumable independent test authors for Gate 3 capability-scale rows."""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_capability_qualification import qualification_metadata
from scripts.data.generate_expansion_qualification import (
    CodexInvocationFailure,
    invoke_codex,
    verify_codex_version,
)
from scripts.data.repair_delta_v7_readiness import (
    CONTRACT_ID as V7_CONTRACT_ID,
    inject_controller_paths,
    response_schema,
    test_author_projection,
    test_author_prompt,
    validate_lane_interface,
    validate_response as validate_v7_response,
)
from scripts.data.repair_delta_v9_readiness import (
    CONTRACT_ID as V9_CONTRACT_ID,
    validate_response as validate_v9_role,
)
from scripts.data.run_capability_scale_teacher import load_queue


CONTRACT_ID = "ganesh-mini-capability-scale-v9-canonical-test-author/v1"
ARTIFACT_SCHEMA = "ganesh-mini-capability-scale-test-author-artifact/v1"
REPORT_SCHEMA = "ganesh-mini-capability-scale-test-author-report/v1"


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {field}")
    return value


def _selection_ids(rows_path: Path, report_path: Path) -> list[str]:
    rows = _jsonl(rows_path)
    report = _sealed(report_path, "report_sha256")
    id_field = report.get("id_field", "candidate_id")
    seal_field = report.get("row_seal_field", "artifact_sha256")
    if (
        report.get("schema_version") != "ganesh-mini-capability-scale-stage-selection/v1"
        or report.get("selected_rows_sha256") != canonical_sha256(rows)
        or report.get("selected") != len(rows)
        or report.get("selected_ids") != [row.get(id_field) for row in rows]
        or report.get("selected_artifact_sha256s") != [row.get(seal_field) for row in rows]
        or report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("candidate selection does not bind selected artifacts")
    for row in rows:
        body = dict(row); claimed = body.pop(seal_field, None)
        if claimed != canonical_sha256(body) or row.get("evaluation_artifacts_read", 0) != 0:
            raise ValueError("candidate selection contains an unsealed artifact")
    return list(report["selected_ids"])


def load_teacher_inputs(
    queue_path: Path,
    queue_manifest_path: Path,
    candidates_path: Path,
    teacher_report_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Validate the sealed teacher aggregate and its exact queue lineage."""
    queue = load_queue(queue_path, queue_manifest_path)
    by_request = {row["request_sha256"]: row for row in queue}
    report = _sealed(teacher_report_path, "report_sha256")
    candidates = _jsonl(candidates_path)
    selected = report.get("selected_request_sha256s")
    if (
        report.get("schema_version") != "ganesh-mini-capability-scale-teacher-report/v1"
        or report.get("status") != "passed"
        or report.get("queue_manifest_sha256") != _sealed(queue_manifest_path, "manifest_sha256").get("manifest_sha256")
        or not isinstance(selected, list)
        or len(selected) != report.get("requested")
        or len(selected) != len(candidates)
        or len(set(selected)) != len(selected)
        or any(value not in by_request for value in selected)
        or report.get("candidates_sha256") != canonical_sha256(candidates)
        or report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("teacher output differs from its sealed aggregate")

    ordered_rows = [by_request[value] for value in selected]
    for candidate, row in zip(candidates, ordered_rows, strict=True):
        expected_assignment = qualification_metadata(row)
        files = candidate.get("verification_task", {}).get("files")
        if (
            candidate.get("id") != row["id"]
            or candidate.get("lane") != row["lane"]
            or candidate.get("task_type") != row["task_type"]
            or candidate.get("qualification_assignment") != expected_assignment
            or candidate.get("teacher_evidence", {}).get("request_sha256") != row["request_sha256"]
            or candidate.get("teacher_evidence", {}).get("evaluation_artifacts_read") != 0
            or candidate.get("test_origin") != "pending-v9-canonical-independent-author"
            or not isinstance(files, list)
            or any(item.get("role") != "support" for item in files)
        ):
            raise ValueError(f"{row['id']}: teacher candidate/queue binding drift")
    return candidates, report


def write_response_schema(path: Path) -> str:
    """Materialize the provider schema once and return its byte hash."""
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(response_schema(), indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") != encoded:
        raise ValueError(f"{path}: response schema drift")
    if not path.exists():
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(encoded, encoding="utf-8")
        temporary.replace(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_atomic(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _write_atomic_text(path: Path, value: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def _validate_and_inject(
    candidate: dict[str, Any], projection: dict[str, Any], response: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, list[dict[str, str]]]]:
    validate_v7_response(response)
    for role in ("primary_discrimination", "cross_cutting"):
        validate_v9_role({**projection, "role": role}, response[role])
    injection = inject_controller_paths(candidate["lane"], response)
    findings = {
        role["role"]: validate_lane_interface(candidate["lane"], role["content"])
        for role in injection["roles"]
    }
    if any(findings.values()):
        raise ValueError(f"lane-interface findings: {findings}")
    return injection, findings


def run_one(
    candidate: dict[str, Any],
    config: dict[str, Any],
    codex_bin: str,
    cli_identity: str,
    schema_path: Path,
    schema_sha256: str,
    run_dir: Path,
    correction: dict[str, Any] | None = None,
) -> dict[str, Any]:
    assignment = candidate["qualification_assignment"]
    projection = test_author_projection(candidate, assignment)
    prompt = test_author_prompt(projection)
    input_binding = {
        "candidate_sha256": canonical_sha256(candidate),
        "assignment_sha256": assignment["assignment_sha256"],
        "projection": projection,
        "prompt": prompt,
        "response_schema_sha256": schema_sha256,
        "config": config,
        "cli_identity": cli_identity,
        "upstream_contracts": [V7_CONTRACT_ID, V9_CONTRACT_ID],
    }
    if correction is not None:
        input_binding["correction_activation_sha256"] = correction["activation_sha256"]
        input_binding["correction_count"] = correction["correction_count"]
    input_sha256 = canonical_sha256(input_binding)
    path = run_dir / f"{candidate['id']}.test-author.json"
    if path.exists():
        artifact = json.loads(path.read_text(encoding="utf-8"))
        body = dict(artifact)
        claimed = body.pop("artifact_sha256", None)
        if claimed != canonical_sha256(body) or artifact.get("input_sha256") != input_sha256:
            raise ValueError(f"{candidate['id']}: sealed test-author artifact drift")
        return artifact

    base = {
        "schema_version": ARTIFACT_SCHEMA,
        "contract_id": CONTRACT_ID,
        "upstream_contract_ids": [V7_CONTRACT_ID, V9_CONTRACT_ID],
        "candidate_id": candidate["id"],
        "cell_id": assignment["cell_id"],
        "lane": candidate["lane"],
        "task_type": candidate["task_type"],
        "input_sha256": input_sha256,
        "candidate_sha256": canonical_sha256(candidate),
        "assignment_sha256": assignment["assignment_sha256"],
        "projection_sha256": canonical_sha256(projection),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "response_schema_sha256": schema_sha256,
        "evaluation_artifacts_read": 0,
    }
    if correction is not None:
        base["correction_count"] = correction["correction_count"]
        base["correction_activation_sha256"] = correction["activation_sha256"]
    try:
        response, run_evidence = invoke_codex(
            codex_bin,
            config,
            schema_path,
            prompt,
            "capability-scale-test-author",
            candidate["lane"],
        )
        run_copy = copy.deepcopy(run_evidence)
        run_sha256 = canonical_sha256(run_copy)
        try:
            injection, findings = _validate_and_inject(candidate, projection, response)
            artifact = {
                **base,
                "status": "structurally-valid",
                "response": response,
                "response_sha256": canonical_sha256(response),
                "injection": injection,
                "findings": findings,
                "finding_codes": [],
                "run": run_copy,
                "run_evidence_sha256": run_sha256,
            }
        except (TypeError, ValueError) as exc:
            artifact = {
                **base,
                "status": "structural-rejected",
                "reason": f"response-contract: {exc}",
                "response": response,
                "response_sha256": canonical_sha256(response),
                "run": run_copy,
                "run_evidence_sha256": run_sha256,
            }
    except CodexInvocationFailure as exc:
        failure = copy.deepcopy(exc.evidence)
        artifact = {
            **base,
            "status": "invocation-failed",
            "reason": str(exc),
            "failure": failure,
            "failure_evidence_sha256": canonical_sha256(failure),
        }
    except (TypeError, ValueError) as exc:
        # Provider output-shape failures can occur after a successful process
        # return but before invoke_codex can return its evidence tuple.  Seal
        # the candidate-local terminal outcome instead of aborting the cohort.
        artifact = {
            **base,
            "status": "invocation-failed",
            "reason": f"provider-output-contract: {exc}",
        }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    _write_atomic(path, artifact)
    return artifact


def run(args: argparse.Namespace) -> dict[str, Any]:
    candidates, teacher_report = load_teacher_inputs(
        args.queue,
        args.queue_manifest,
        args.teacher_candidates,
        args.teacher_report,
    )
    candidate_selection = getattr(args, "candidate_selection", None)
    candidate_selection_report = getattr(args, "candidate_selection_report", None)
    if candidate_selection is not None or candidate_selection_report is not None:
        if candidate_selection is None or candidate_selection_report is None:
            raise ValueError("candidate selection rows and report must be supplied together")
        selected_ids = _selection_ids(candidate_selection, candidate_selection_report)
        by_id = {candidate["id"]: candidate for candidate in candidates}
        if any(identifier not in by_id for identifier in selected_ids):
            raise ValueError("candidate selection differs from teacher candidates")
        candidates = [by_id[identifier] for identifier in selected_ids]
    corrections: dict[str, dict[str, Any]] = {}
    correction_activation = getattr(args, "correction_activation", None)
    correction_report_path = getattr(args, "correction_report", None)
    if correction_activation is not None or correction_report_path is not None:
        if correction_activation is None or correction_report_path is None:
            raise ValueError("correction activation and report must be supplied together")
        correction_report = _sealed(correction_report_path, "report_sha256")
        correction_rows = _jsonl(correction_activation)
        if (
            correction_report.get("status") != "activated"
            or correction_report.get("activated") != len(correction_rows)
            or correction_report.get("activation_rows_sha256") != canonical_sha256(correction_rows)
            or correction_report.get("maximum_correction_count") != 1
        ):
            raise ValueError("test-reauthor activation report is invalid")
        for row in correction_rows:
            body = dict(row); claimed = body.pop("activation_sha256", None)
            if (
                claimed != canonical_sha256(body) or row.get("correction_count") != 1
                or row.get("author_visibility") != {
                    "specification_and_controller_bindings_only": True,
                    "prior_tests_visible": False, "verifier_outputs_visible": False,
                    "reference_visible": False, "evaluation_artifacts_read": 0,
                }
            ):
                raise ValueError("test-reauthor activation row is invalid")
            corrections[row["candidate_id"]] = row
        if len(corrections) != len(correction_rows):
            raise ValueError("duplicate test-reauthor activation")
        candidates = [candidate for candidate in candidates if candidate["id"] in corrections]
        if len(candidates) != len(corrections):
            raise ValueError("test-reauthor activation differs from teacher candidates")
    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    args.run_dir.mkdir(parents=True, exist_ok=True)
    schema_path = args.run_dir / "v7-order-insensitive-test-author.schema.json"
    schema_sha256 = write_response_schema(schema_path)
    terminal: list[dict[str, Any] | None] = [None] * len(candidates)

    def invoke(index: int) -> tuple[int, dict[str, Any]]:
        return index, run_one(
            candidates[index], config, args.codex_bin, cli_identity,
            schema_path, schema_sha256, args.run_dir, corrections.get(candidates[index]["id"]),
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        for index, artifact in executor.map(invoke, range(len(candidates))):
            terminal[index] = artifact
    rows = [row for row in terminal if row is not None]
    counts = dict(sorted(Counter(row["status"] for row in rows).items()))
    report = {
        "schema_version": REPORT_SCHEMA,
        "contract_id": CONTRACT_ID,
        "upstream_contract_ids": [V7_CONTRACT_ID, V9_CONTRACT_ID],
        "status": "passed" if counts == {"structurally-valid": len(candidates)} else "failed",
        "requested": len(candidates),
        "counts": counts,
        "teacher_report_sha256": teacher_report["report_sha256"],
        "ordered_candidate_ids": [candidate["id"] for candidate in candidates],
        "terminal_artifact_sha256s": [row["artifact_sha256"] for row in rows],
        "terminal_rows_sha256": canonical_sha256(rows),
        "selected_candidates_sha256": canonical_sha256(candidates),
        "response_schema_sha256": schema_sha256,
        "cli_identity": cli_identity,
        "config_sha256": canonical_sha256(config),
        "evaluation_artifacts_read": 0,
    }
    if corrections:
        report["correction_count"] = 1
        report["correction_candidate_ids"] = [candidate["id"] for candidate in candidates]
    if candidate_selection_report is not None:
        report["candidate_selection_report_sha256"] = _sealed(
            candidate_selection_report, "report_sha256",
        )["report_sha256"]
    report["report_sha256"] = canonical_sha256(report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_atomic_text(
        args.output_dir / "terminal-artifacts.jsonl",
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
    )
    _write_atomic_text(
        args.output_dir / "selected-candidates.jsonl",
        "".join(json.dumps(candidate, sort_keys=True) + "\n" for candidate in candidates),
    )
    _write_atomic(args.output_dir / "test-author-report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--teacher-candidates", type=Path, required=True)
    parser.add_argument("--teacher-report", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--correction-activation", type=Path)
    parser.add_argument("--correction-report", type=Path)
    parser.add_argument("--candidate-selection", type=Path)
    parser.add_argument("--candidate-selection-report", type=Path)
    args = parser.parse_args()
    report = run(args)
    print(json.dumps({
        "status": report["status"],
        "counts": report["counts"],
        "report_sha256": report["report_sha256"],
    }, sort_keys=True))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
