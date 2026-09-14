#!/usr/bin/env python3
"""Assemble sealed Gate 2 admission envelopes without reading evaluation data."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_capability_qualification import SCHEMA_VERSION  # noqa: E402
from scripts.data.admit_expansion import RECORD_KEYS, canonical_json, read_jsonl  # noqa: E402
from scripts.data.build_capability_corpus_plan import canonical_sha256, load_sealed  # noqa: E402
from scripts.data.generate_capability_qualification import (  # noqa: E402
    architect_prompt,
    build_candidate,
    load_queue,
    qualification_metadata,
    test_prompt,
)
from scripts.data.generate_expansion_qualification import parse_events  # noqa: E402
from scripts.eval.contracts import sha256_text  # noqa: E402


SEMANTIC_SCHEMA = "ganesh-mini-capability-semantic-review-report/v1"
SEPARATION_SCHEMA = "ganesh-mini-capability-separation-attestation/v1"
ASSEMBLY_SCHEMA = "ganesh-mini-capability-admission-envelope-assembly/v1"
PASS_FIELDS = (
    "exact_training_passed", "normalized_training_passed", "fuzzy_training_passed",
    "exact_evaluation_passed", "normalized_evaluation_passed", "fuzzy_evaluation_passed",
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha(value: Any, where: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{where}: expected lowercase SHA-256")
    return value


def seal(value: dict[str, Any]) -> dict[str, Any]:
    sealed = dict(value)
    sealed["evidence_sha256"] = canonical_sha256(sealed)
    return sealed


def load_report(path: Path, seal_field: str, schema: str) -> dict[str, Any]:
    report = load_sealed(path, seal_field)
    if report.get("schema_version") != schema:
        raise ValueError(f"{path}: unsupported schema")
    return report


def _verify_run(run: Any, evidence_path: Path) -> dict[str, Any]:
    if not isinstance(run, dict):
        raise ValueError(f"{evidence_path}: teacher run is not an object")
    body = dict(run)
    claimed = body.pop("run_evidence_sha256", None)
    if claimed != hashlib.sha256(canonical_json(body)).hexdigest():
        raise ValueError(f"{evidence_path}: teacher run seal mismatch")
    for field, hash_field in (
        ("prompt", "prompt_sha256"), ("stdout_jsonl", "stdout_sha256"),
        ("stderr", "stderr_sha256"), ("final_output", "final_output_sha256"),
    ):
        if not isinstance(run.get(field), str) or sha256_text(run[field]) != run.get(hash_field):
            raise ValueError(f"{evidence_path}: {field} hash mismatch")
    command = run.get("command_identity")
    if not isinstance(command, list) or not all(flag in command for flag in (
        "--ephemeral", "--ignore-user-config", "--ignore-rules", "--sandbox", "-C",
    )):
        raise ValueError(f"{evidence_path}: teacher isolation flags are incomplete")
    sandbox_index = command.index("--sandbox")
    if sandbox_index + 1 >= len(command) or command[sandbox_index + 1] != "read-only":
        raise ValueError(f"{evidence_path}: teacher sandbox was not read-only")
    if (
        run.get("returncode") != 0 or run.get("timed_out") is not False
        or run.get("event_parse_error") is not None
        or run.get("disallowed_tool_item_types") != []
        or not isinstance(run.get("usage"), dict)
    ):
        raise ValueError(f"{evidence_path}: teacher execution did not complete cleanly")
    try:
        payload = json.loads(run["final_output"])
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError(f"{evidence_path}: invalid teacher final output") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise ValueError(f"{evidence_path}: teacher final output lacks items")
    events, usage, disallowed = parse_events(run["stdout_jsonl"])
    if events != run["events"] or usage != run["usage"] or disallowed != run["disallowed_tool_item_types"]:
        raise ValueError(f"{evidence_path}: parsed execution events differ from archived evidence")
    return payload


def _items_by_id(payload: dict[str, Any], expected_fields: set[str], where: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for item in payload["items"]:
        if (
            not isinstance(item, dict) or set(item) != expected_fields
            or any(not isinstance(value, str) or not value.strip() for value in item.values())
            or item["id"] in result
        ):
            raise ValueError(f"{where}: malformed or duplicate structured item")
        result[item["id"]] = item
    if not result:
        raise ValueError(f"{where}: empty structured output")
    return result


def _base_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    if set(candidate) != RECORD_KEYS | {"qualification_assignment", "teacher_evidence"}:
        raise ValueError(f"{candidate.get('id')}: generated candidate keys differ from contract")
    return {key: candidate[key] for key in RECORD_KEYS}


def load_teacher_candidates(
    queue_by_id: dict[str, dict[str, Any]],
    candidate_paths: list[Path],
    teacher_evidence_paths: list[Path],
    queue_file_sha256: str | None = None,
    queue_manifest_sha256: str | None = None,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    if not candidate_paths or len(candidate_paths) != len(teacher_evidence_paths):
        raise ValueError("candidate and teacher-evidence paths must be nonempty one-to-one pairs")
    candidates: list[dict[str, Any]] = []
    derived: dict[str, dict[str, Any]] = {}
    inputs: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for candidate_path, evidence_path in zip(candidate_paths, teacher_evidence_paths, strict=True):
        evidence = load_sealed(evidence_path, "evidence_sha256")
        rows = read_jsonl(candidate_path)
        requested_ids = [row.get("id") for row in rows]
        requested_queue_rows = [queue_by_id.get(identifier) for identifier in requested_ids]
        if (
            evidence.get("schema_version") != "ganesh-mini-capability-qualification-teacher-run/v1"
            or evidence.get("candidate_output_sha256") != file_sha256(candidate_path)
            or evidence.get("generated") != len(rows)
            or evidence.get("failures") != []
            or evidence.get("selection", {}).get("evaluation_surfaces_read") != 0
            or evidence.get("selection", {}).get("requested_ids") != requested_ids
            or any(row is None for row in requested_queue_rows)
            or evidence.get("selection", {}).get("queue_row_sha256s")
            != [canonical_sha256(row) for row in requested_queue_rows]
            or evidence.get("selection", {}).get("batch_size") != len(rows)
            or evidence.get("selection", {}).get("lane")
            != (rows[0].get("lane") if rows else None)
        ):
            raise ValueError(f"{evidence_path}: teacher batch does not bind its candidates")
        if queue_file_sha256 is not None and (
            evidence.get("queue", {}).get("sha256") != queue_file_sha256
            or evidence.get("queue", {}).get("manifest_sha256") != queue_manifest_sha256
        ):
            raise ValueError(f"{evidence_path}: teacher batch does not bind the supplied queue")
        runs: dict[str, tuple[dict[str, Any], dict[str, dict[str, str]]]] = {}
        for run in evidence.get("runs", []):
            payload = _verify_run(run, evidence_path)
            kind = run.get("run_kind")
            fields = (
                {"id", "problem", "reference_code", "known_bad_code", "known_bad_label"}
                if kind == "capability-source-architect" else {"id", "test_code"}
                if kind == "capability-independent-test-author" else None
            )
            if fields is None:
                raise ValueError(f"{evidence_path}: unexpected teacher run kind")
            run_hash = run["run_evidence_sha256"]
            if run_hash in runs:
                raise ValueError(f"{evidence_path}: duplicate teacher run seal")
            runs[run_hash] = (run, _items_by_id(payload, fields, str(evidence_path)))

        for generated in rows:
            identifier = generated.get("id")
            if not isinstance(identifier, str) or identifier in seen_ids or identifier not in queue_by_id:
                raise ValueError(f"{identifier}: missing, duplicate, or unknown queue identity")
            queue_row = queue_by_id[identifier]
            if generated.get("qualification_assignment") != qualification_metadata(queue_row):
                raise ValueError(f"{identifier}: assignment or source lineage changed")
            refs = generated.get("teacher_evidence")
            if not isinstance(refs, dict) or set(refs) != {
                "architect_run_evidence_sha256", "test_author_run_evidence_sha256",
            }:
                raise ValueError(f"{identifier}: teacher run bindings are incomplete")
            architect_bundle = runs.get(refs["architect_run_evidence_sha256"])
            test_bundle = runs.get(refs["test_author_run_evidence_sha256"])
            if architect_bundle is None or test_bundle is None:
                raise ValueError(f"{identifier}: referenced teacher run is absent")
            architect_run, architect_items = architect_bundle
            test_run, test_items = test_bundle
            architecture = architect_items.get(identifier)
            test_item = test_items.get(identifier)
            if architecture is None or test_item is None:
                raise ValueError(f"{identifier}: teacher outputs do not contain candidate")
            shard_ids = list(architect_items)
            if set(shard_ids) != set(test_items):
                raise ValueError(f"{identifier}: architect/test-author shard identities differ")
            shard_rows = [queue_by_id[item_id] for item_id in shard_ids]
            if architect_run.get("lane") != queue_row["lane"] or architect_run.get("prompt") != architect_prompt(queue_row["lane"], shard_rows):
                raise ValueError(f"{identifier}: architect prompt or lane differs from isolated contract")
            architecture_list = [architect_items[item_id] for item_id in shard_ids]
            if test_run.get("lane") != queue_row["lane"] or test_run.get("prompt") != test_prompt(queue_row["lane"], architecture_list):
                raise ValueError(f"{identifier}: test-author prompt is not specification-only")
            expected = build_candidate(
                queue_row["lane"], identifier, queue_row["task_type"], architecture,
                test_item["test_code"], source=queue_row["source"],
            )
            base = _base_candidate(generated)
            if base != expected:
                raise ValueError(f"{identifier}: candidate differs from bound teacher outputs")
            base_sha = canonical_sha256(base)
            derived[identifier] = {
                "candidate": base,
                "candidate_sha256": base_sha,
                "queue_row": queue_row,
                "queue_record_sha256": canonical_sha256(queue_row),
                "architect_run": architect_run,
                "test_author_run": test_run,
            }
            candidates.append(base)
            seen_ids.add(identifier)
        inputs.append({
            "candidates": {"path": str(candidate_path), "sha256": file_sha256(candidate_path), "records": len(rows)},
            "teacher_evidence": {"path": str(evidence_path), "sha256": file_sha256(evidence_path), "evidence_sha256": evidence["evidence_sha256"]},
        })
    return candidates, derived, inputs


def _indexed_records(report: dict[str, Any], where: str) -> dict[str, dict[str, Any]]:
    rows = report.get("records")
    if not isinstance(rows, list):
        raise ValueError(f"{where}: records must be a list")
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        identifier = row.get("id") if isinstance(row, dict) else None
        if not isinstance(identifier, str) or not identifier or identifier in indexed:
            raise ValueError(f"{where}: record IDs are missing or duplicated")
        indexed[identifier] = row
    return indexed


def build_envelopes(
    queue_by_id: dict[str, dict[str, Any]],
    candidates: list[dict[str, Any]],
    derived: dict[str, dict[str, Any]],
    semantic_report: dict[str, Any],
    separation_report: dict[str, Any],
) -> list[dict[str, Any]]:
    if (
        semantic_report.get("status") != "complete"
        or semantic_report.get("evaluation_artifacts_read") != 0
        or semantic_report.get("visibility") != "specification-and-assigned-labels-only"
    ):
        raise ValueError("semantic review report violates its isolation contract")
    if (
        separation_report.get("status") != "passed"
        or separation_report.get("evaluation_artifacts_read_by_construction") != 0
    ):
        raise ValueError("separation attestation is incomplete or failed")
    comparison_manifest_sha256 = _sha(
        separation_report.get("comparison_manifest_sha256"),
        "separation_report.comparison_manifest_sha256",
    )
    semantic_by_id = _indexed_records(semantic_report, "semantic report")
    separation_by_id = _indexed_records(separation_report, "separation report")
    candidate_ids = [candidate["id"] for candidate in candidates]
    if set(semantic_by_id) != set(candidate_ids) or set(separation_by_id) != set(candidate_ids):
        raise ValueError("candidate, semantic-review, and separation identities differ")

    envelopes: list[dict[str, Any]] = []
    for candidate in candidates:
        identifier = candidate["id"]
        context = derived[identifier]
        queue_row = context["queue_row"]
        candidate_sha = context["candidate_sha256"]
        specification_sha = sha256_text(candidate["messages"][0]["content"])
        tests = [item["sha256"] for item in candidate["verification_task"]["files"] if item.get("role") == "test"]

        semantic_input = semantic_by_id[identifier]
        if (
            semantic_input.get("candidate_sha256") != candidate_sha
            or semantic_input.get("specification_sha256") != specification_sha
            or semantic_input.get("primary_capability") != queue_row["primary_capability"]
            or semantic_input.get("assigned_cross_cutting_dimension") != queue_row["assigned_cross_cutting_dimension"]
            or semantic_input.get("verdict") != "pass"
            or semantic_input.get("primary_capability_is_substantive") is not True
            or semantic_input.get("generic_edge_case_boilerplate_is_primary") is not False
            or semantic_input.get("verifier_outputs_visible") is not False
            or semantic_input.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError(f"{identifier}: semantic review binding or verdict failed")

        separation_input = separation_by_id[identifier]
        if separation_input.get("candidate_sha256") != candidate_sha or any(separation_input.get(field) is not True for field in PASS_FIELDS):
            raise ValueError(f"{identifier}: separation binding or comparison failed")

        teacher = seal({
            "candidate_sha256": candidate_sha,
            "queue_record_sha256": context["queue_record_sha256"],
            "source_queue_id": queue_row["source_queue_id"],
            "source_record_sha256": queue_row["source"]["source_record_sha256"],
            "assistant_sha256": sha256_text(candidate["messages"][1]["content"]),
            "rendered_prompt_sha256": context["architect_run"]["prompt_sha256"],
            "architect_run_evidence_sha256": context["architect_run"]["run_evidence_sha256"],
            "visibility": {
                "training_stimulus": True, "assigned_ontology": True,
                "runtime_contract": True, "evaluation_artifacts_read": 0,
            },
        })
        test_author = seal({
            "candidate_sha256": candidate_sha,
            "specification_sha256": specification_sha,
            "test_sha256s": tests,
            "origin": candidate["test_origin"],
            "test_author_run_evidence_sha256": context["test_author_run"]["run_evidence_sha256"],
            "visibility": {
                "specification_only": True, "independent_of_teacher": True,
                "reference_visible": False, "known_bad_visible": False,
                "teacher_context_visible": False, "evaluation_artifacts_read": 0,
            },
        })
        semantic = seal({
            "candidate_sha256": candidate_sha, "specification_sha256": specification_sha,
            "primary_capability": queue_row["primary_capability"],
            "assigned_cross_cutting_dimension": queue_row["assigned_cross_cutting_dimension"],
            "verdict": "pass",
            "primary_capability_is_substantive": True,
            "generic_edge_case_boilerplate_is_primary": False,
            "review_record_sha256": canonical_sha256(semantic_input),
            "visibility": {
                "specification_and_assigned_labels_only": True,
                "verifier_outputs_visible": False, "evaluation_artifacts_read": 0,
            },
        })
        separation = seal({
            "candidate_sha256": candidate_sha,
            **{field: True for field in PASS_FIELDS},
            "comparison_manifest_sha256": comparison_manifest_sha256,
            "attestation_record_sha256": canonical_sha256(separation_input),
            "evaluation_artifacts_read_by_construction": 0,
        })
        lineage = seal({
            "candidate_sha256": candidate_sha,
            "queue_record_sha256": context["queue_record_sha256"],
            "source_identity": {key: candidate["source"][key] for key in ("dataset", "revision", "record_id")},
            "source_record_sha256": candidate["source"]["source_record_sha256"],
            "complete": True,
            "teacher_evidence_sha256": teacher["evidence_sha256"],
            "test_author_evidence_sha256": test_author["evidence_sha256"],
            "semantic_review_evidence_sha256": semantic["evidence_sha256"],
            "separation_evidence_sha256": separation["evidence_sha256"],
        })
        correction_passes = semantic_input.get("correction_passes", 0)
        if type(correction_passes) is not int or correction_passes not in (0, 1):
            raise ValueError(f"{identifier}: correction passes exceed the contract")
        correction = None
        if correction_passes == 1:
            parent_sha = _sha(semantic_input.get("parent_candidate_sha256"), f"{identifier}.parent_candidate_sha256")
            correction = seal({"candidate_sha256": candidate_sha, "parent_candidate_sha256": parent_sha})
        qualification = {
            "queue_id": identifier, "cell_id": queue_row["cell_id"],
            "primary_capability": queue_row["primary_capability"],
            "assigned_cross_cutting_dimension": queue_row["assigned_cross_cutting_dimension"],
            "source_queue_id": queue_row["source_queue_id"],
            "correction_passes": correction_passes, "correction": correction,
            "evidence": {
                "teacher": teacher, "test_author": test_author,
                "semantic_review": semantic, "separation": separation, "lineage": lineage,
            },
        }
        envelopes.append({"schema_version": SCHEMA_VERSION, "candidate": candidate, "qualification": qualification})
    return envelopes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, action="append", required=True)
    parser.add_argument("--teacher-evidence", type=Path, action="append", required=True)
    parser.add_argument("--semantic-review", type=Path, required=True)
    parser.add_argument("--separation-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    queue, queue_manifest = load_queue(args.queue, args.queue_manifest)
    queue_by_id = {row["id"]: row for row in queue}
    candidates, derived, teacher_inputs = load_teacher_candidates(
        queue_by_id, args.candidates, args.teacher_evidence,
        queue_file_sha256=file_sha256(args.queue),
        queue_manifest_sha256=queue_manifest["manifest_sha256"],
    )
    semantic = load_report(args.semantic_review, "report_sha256", SEMANTIC_SCHEMA)
    separation = load_report(args.separation_report, "report_sha256", SEPARATION_SCHEMA)
    envelopes = build_envelopes(queue_by_id, candidates, derived, semantic, separation)
    payload = b"".join(canonical_json(row) + b"\n" for row in envelopes)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    report: dict[str, Any] = {
        "schema_version": ASSEMBLY_SCHEMA, "status": "ready-for-executable-admission",
        "records": len(envelopes), "evaluation_artifacts_read": 0,
        "inputs": {
            "queue": {"path": str(args.queue), "sha256": file_sha256(args.queue), "manifest_sha256": queue_manifest["manifest_sha256"]},
            "teacher_batches": teacher_inputs,
            "semantic_review": {"path": str(args.semantic_review), "sha256": file_sha256(args.semantic_review), "report_sha256": semantic["report_sha256"]},
            "separation": {"path": str(args.separation_report), "sha256": file_sha256(args.separation_report), "report_sha256": separation["report_sha256"]},
        },
        "output": {"path": str(args.output), "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()},
    }
    report["report_sha256"] = canonical_sha256(report)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "records": len(envelopes), "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
