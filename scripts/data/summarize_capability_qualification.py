#!/usr/bin/env python3
"""Build a deterministic, fail-closed Gate 2 qualification progress report."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


EXPECTED_DRAFTS = 240
EXPECTED_CELLS = 120
MINIMUM_ADMITTED = 120
ENVELOPE_SCHEMA = "ganesh-mini-capability-qualification-envelope/v1"


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode()


def canonical_sha256(value: dict[str, Any], seal_field: str = "report_sha256") -> str:
    unsealed = {key: item for key, item in value.items() if key != seal_field}
    return hashlib.sha256(canonical_json(unsealed)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").split("\n") if line.strip()]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{path}: every JSONL row must be an object")
    return rows


def read_record_artifact(path: Path) -> list[dict[str, Any]]:
    """Read either JSONL or the rejected-output JSON array used by admission."""
    text = path.read_text(encoding="utf-8")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return read_jsonl(path)
    if isinstance(value, list) and all(isinstance(row, dict) for row in value):
        return value
    if isinstance(value, dict):
        return [value]
    raise ValueError(f"{path}: record artifact must contain objects")


def _rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _candidate_binding(row: dict[str, Any], original_ids: set[str], cells: set[str]) -> tuple[str, str, str | None]:
    identifier = row.get("id")
    if not isinstance(identifier, str) or not identifier:
        raise ValueError("generated candidate has no ID")
    for key in ("qualification_draft_id", "draft_id", "queue_id"):
        value = row.get(key)
        if isinstance(value, str) and value in original_ids:
            return identifier, "original", value
    if identifier in original_ids:
        return identifier, "original", identifier
    cell_id = row.get("replacement_for_cell_id")
    if cell_id is not None:
        if cell_id not in cells or row.get("cell_id") != cell_id or row.get("replacement_attempt") != 1:
            raise ValueError(f"{identifier}: invalid bounded replacement declaration")
        return identifier, "replacement", None
    raise ValueError(f"{identifier}: candidate is not bound to a qualification draft or replacement")


def _candidate_view(row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    if row.get("schema_version") != ENVELOPE_SCHEMA:
        return row, None
    candidate = row.get("candidate", row.get("training_candidate"))
    qualification = row.get("qualification")
    if not isinstance(candidate, dict) or not isinstance(qualification, dict):
        raise ValueError("qualification envelope lacks candidate or qualification metadata")
    if qualification.get("queue_id") != candidate.get("id"):
        raise ValueError(f"{candidate.get('id')}: qualification envelope queue binding mismatch")
    return candidate, qualification


def _sealed_report(path: Path) -> dict[str, Any]:
    report = json.loads(path.read_text(encoding="utf-8"))
    claimed = report.get("report_sha256")
    if not isinstance(claimed, str) or claimed != canonical_sha256(report):
        raise ValueError(f"{path}: invalid admission report seal")
    if report.get("schema_version") not in {
        "ganesh-mini-expansion-admission/v1",
        "ganesh-mini-capability-qualification-admission/v1",
    }:
        raise ValueError(f"{path}: unsupported admission report schema")
    return report


def _bound_artifact(path_value: Any, evidence: Any, label: str) -> tuple[Path, list[dict[str, Any]]]:
    if not isinstance(evidence, dict) or evidence.get("path") != path_value:
        raise ValueError(f"{label}: artifact path binding is incomplete")
    path = Path(path_value) if isinstance(path_value, str) else None
    if path is None or not path.is_file():
        raise ValueError(f"{label}: bound artifact does not exist")
    payload = path.read_bytes()
    if evidence.get("sha256") != hashlib.sha256(payload).hexdigest():
        raise ValueError(f"{label}: artifact hash mismatch")
    if "bytes" in evidence and evidence["bytes"] != len(payload):
        raise ValueError(f"{label}: artifact byte count mismatch")
    return path, read_record_artifact(path)


def _admitted_id(row: dict[str, Any], capability_report: bool) -> str:
    if capability_report:
        record = row.get("record")
        qualification = row.get("qualification")
        if not isinstance(record, dict) or not isinstance(qualification, dict):
            raise ValueError("capability admitted row lacks record or qualification evidence")
        identifier = record.get("id")
        if qualification.get("queue_id") != identifier:
            raise ValueError(f"{identifier}: admitted qualification queue binding mismatch")
    else:
        identifier = row.get("id")
    if not isinstance(identifier, str) or not identifier:
        raise ValueError("admitted artifact contains a row without an ID")
    return identifier


def _dimension_rows(
    dimensions: Iterable[str], cells: dict[str, dict[str, Any]], generated: set[str],
    original_generated_ids: set[str], corrected_ids: set[str], disposition: dict[str, str],
    identity_cell: dict[str, str],
) -> dict[str, dict[str, int | float | None]]:
    result: dict[str, dict[str, int | float | None]] = {}
    dimension_names = tuple(dimensions)
    keys = sorted({"/".join(str(cell[name]) for name in dimension_names) for cell in cells.values()})
    for key in keys:
        matching_cells = {
            cell_id for cell_id, cell in cells.items()
            if "/".join(str(cell[name]) for name in dimension_names) == key
        }
        drafted = 2 * len(matching_cells)
        generated_count = sum(1 for item in generated if identity_cell[item] in matching_cells)
        original_generated = sum(1 for item in original_generated_ids if identity_cell[item] in matching_cells)
        corrected = sum(1 for item in corrected_ids if identity_cell[item] in matching_cells)
        admitted = sum(1 for item, state in disposition.items() if state == "admitted" and identity_cell[item] in matching_cells)
        rejected = sum(1 for item, state in disposition.items() if state == "rejected" and identity_cell[item] in matching_cells)
        disposed = admitted + rejected
        result[key] = {
            "drafted": drafted,
            "generated": generated_count,
            "original_generated": original_generated,
            "replacement_generated": generated_count - original_generated,
            "corrected": corrected,
            "dispositioned": disposed,
            "admitted": admitted,
            "rejected": rejected,
            "generation_yield": _rate(original_generated, drafted),
            "admission_yield_from_generated": _rate(admitted, generated_count),
            "admission_yield_from_dispositioned": _rate(admitted, disposed),
        }
    return result


def _combine_metric_rows(rows: Iterable[dict[str, int | float | None]]) -> dict[str, int | float | None]:
    count_fields = (
        "drafted", "generated", "original_generated", "replacement_generated",
        "corrected", "dispositioned", "admitted", "rejected",
    )
    values = list(rows)
    result: dict[str, int | float | None] = {
        field: sum(int(row[field]) for row in values) for field in count_fields
    }
    result.update({
        "generation_yield": _rate(int(result["original_generated"]), int(result["drafted"])),
        "admission_yield_from_generated": _rate(int(result["admitted"]), int(result["generated"])),
        "admission_yield_from_dispositioned": _rate(int(result["admitted"]), int(result["dispositioned"])),
    })
    return result


def _five_families(by_lane: dict[str, dict[str, int | float | None]]) -> dict[str, dict[str, int | float | None]]:
    return {
        "go": _combine_metric_rows((by_lane["go"],)),
        "java": _combine_metric_rows((by_lane["java"],)),
        "javascript_typescript": _combine_metric_rows((by_lane["javascript"], by_lane["typescript"])),
        "python": _combine_metric_rows((by_lane["python"],)),
        "rust": _combine_metric_rows((by_lane["rust"],)),
    }


def summarize(
    queue_path: Path, candidate_paths: list[Path], admission_report_paths: list[Path],
) -> dict[str, Any]:
    queue = read_jsonl(queue_path)
    if len(queue) != EXPECTED_DRAFTS:
        raise ValueError(f"qualification queue must contain exactly {EXPECTED_DRAFTS} drafts")
    queue_ids = [row.get("id") for row in queue]
    if not all(isinstance(item, str) and item for item in queue_ids) or len(set(queue_ids)) != len(queue_ids):
        raise ValueError("qualification queue IDs must be non-empty and unique")
    required = ("cell_id", "primary_capability", "lane", "task_type")
    cells: dict[str, dict[str, Any]] = {}
    original_by_cell: dict[str, list[str]] = defaultdict(list)
    for row in queue:
        if not all(isinstance(row.get(key), str) and row[key] for key in required):
            raise ValueError(f"{row.get('id')}: incomplete qualification cell metadata")
        cell = {key: row[key] for key in required}
        existing = cells.setdefault(row["cell_id"], cell)
        if existing != cell:
            raise ValueError(f"{row['cell_id']}: inconsistent cell metadata")
        original_by_cell[row["cell_id"]].append(row["id"])
    if len(cells) != EXPECTED_CELLS or set(map(len, original_by_cell.values())) != {2}:
        raise ValueError("qualification queue must contain exactly two drafts in each of 120 cells")

    original_ids = set(queue_ids)
    queue_by_id = {row["id"]: row for row in queue}
    identity_cell = {row["id"]: row["cell_id"] for row in queue}
    generated: set[str] = set()
    original_generated_refs: set[str] = set()
    candidate_original_ref: dict[str, str] = {}
    corrected_ids: set[str] = set()
    replacements: dict[str, str] = {}
    candidate_inputs: list[dict[str, Any]] = []
    candidate_sha_to_ids: dict[str, tuple[Path, list[str]]] = {}
    for path in candidate_paths:
        rows = read_jsonl(path)
        identifiers: list[str] = []
        for row in rows:
            candidate, envelope_qualification = _candidate_view(row)
            identifier, role, original_ref = _candidate_binding(candidate, original_ids, set(cells))
            if identifier in generated:
                raise ValueError(f"{identifier}: duplicate generated candidate")
            if role == "original":
                assert original_ref is not None
                if original_ref in original_generated_refs:
                    raise ValueError(f"{original_ref}: qualification draft generated more than once")
                original_generated_refs.add(original_ref)
                candidate_original_ref[identifier] = original_ref
                identity_cell[identifier] = identity_cell[original_ref]
                expected = cells[identity_cell[original_ref]]
                for key in ("cell_id", "primary_capability", "lane", "task_type"):
                    if key in candidate and candidate[key] != expected[key]:
                        raise ValueError(f"{identifier}: generated candidate conflicts with queue field {key}")
                assignment = candidate.get("qualification_assignment")
                if assignment is not None:
                    if not isinstance(assignment, dict):
                        raise ValueError(f"{identifier}: qualification_assignment must be an object")
                    for key in ("cell_id", "primary_capability"):
                        if assignment.get(key) != expected[key]:
                            raise ValueError(f"{identifier}: qualification_assignment conflicts with queue field {key}")
                    expected_queue_hash = hashlib.sha256(canonical_json(queue_by_id[original_ref])).hexdigest()
                    if assignment.get("queue_row_sha256") != expected_queue_hash:
                        raise ValueError(f"{identifier}: qualification_assignment queue hash mismatch")
                    body = dict(assignment)
                    claimed_assignment = body.pop("assignment_sha256", None)
                    if claimed_assignment != hashlib.sha256(canonical_json(body)).hexdigest():
                        raise ValueError(f"{identifier}: qualification_assignment seal mismatch")
                if envelope_qualification is not None:
                    if (
                        envelope_qualification.get("cell_id") != expected["cell_id"]
                        or envelope_qualification.get("primary_capability") != expected["primary_capability"]
                    ):
                        raise ValueError(f"{identifier}: qualification envelope conflicts with queue cell")
                    correction_passes = envelope_qualification.get("correction_passes")
                    if type(correction_passes) is not int or correction_passes not in (0, 1):
                        raise ValueError(f"{identifier}: correction passes exceed the qualification contract")
                    if correction_passes == 1:
                        correction = envelope_qualification.get("correction")
                        if not isinstance(correction, dict):
                            raise ValueError(f"{identifier}: corrected envelope lacks correction evidence")
                        correction_body = dict(correction)
                        correction_seal = correction_body.pop("evidence_sha256", None)
                        if correction_seal != hashlib.sha256(canonical_json(correction_body)).hexdigest():
                            raise ValueError(f"{identifier}: correction evidence seal mismatch")
                        corrected_ids.add(identifier)
                    elif envelope_qualification.get("correction") is not None:
                        raise ValueError(f"{identifier}: uncorrected envelope carries correction evidence")
            else:
                cell_id = candidate["cell_id"]
                if cell_id in replacements:
                    raise ValueError(f"{cell_id}: more than one bounded replacement")
                replacements[cell_id] = identifier
                identity_cell[identifier] = cell_id
            generated.add(identifier)
            identifiers.append(identifier)
        digest = file_sha256(path)
        if digest in candidate_sha_to_ids:
            raise ValueError(f"{path}: duplicate candidate input content")
        candidate_sha_to_ids[digest] = (path, identifiers)
        candidate_inputs.append({"path": str(path), "sha256": digest, "records": len(rows)})

    disposition: dict[str, str] = {}
    admission_inputs: list[dict[str, Any]] = []
    for path in admission_report_paths:
        report = _sealed_report(path)
        capability_report = report["schema_version"] == "ganesh-mini-capability-qualification-admission/v1"
        input_evidence = report.get("input") if capability_report else {
            "path": report.get("input"), "sha256": report.get("input_sha256"),
        }
        if not isinstance(input_evidence, dict):
            raise ValueError(f"{path}: admission input binding is incomplete")
        input_sha = input_evidence.get("sha256")
        if input_sha not in candidate_sha_to_ids:
            raise ValueError(f"{path}: admission input is not one of the supplied candidate files")
        bound_input, _ = _bound_artifact(
            input_evidence.get("path"), input_evidence, f"{path}: input",
        )
        candidate_path, input_ids = candidate_sha_to_ids[input_sha]
        if bound_input.resolve() != candidate_path.resolve():
            raise ValueError(f"{path}: admission input path does not match the supplied candidate file")
        if capability_report:
            outputs = report.get("outputs")
            if not isinstance(outputs, dict):
                raise ValueError(f"{path}: capability admission outputs are incomplete")
            admitted_evidence = outputs.get("admitted")
            rejected_evidence = outputs.get("rejected")
            admitted_path, admitted_rows = _bound_artifact(
                admitted_evidence.get("path") if isinstance(admitted_evidence, dict) else None,
                admitted_evidence, f"{path}: admitted",
            )
            rejected_path, rejected_rows = _bound_artifact(
                rejected_evidence.get("path") if isinstance(rejected_evidence, dict) else None,
                rejected_evidence, f"{path}: rejected",
            )
        else:
            output_evidence = report.get("output")
            admitted_path, admitted_rows = _bound_artifact(
                output_evidence.get("path") if isinstance(output_evidence, dict) else None,
                output_evidence, f"{path}: admitted",
            )
            rejected_path = None
            rejected_rows = report.get("rejected", [])
            if not isinstance(rejected_rows, list) or not all(isinstance(row, dict) for row in rejected_rows):
                raise ValueError(f"{path}: legacy rejection evidence is malformed")
        accepted_ids = [_admitted_id(row, capability_report) for row in admitted_rows]
        rejected_ids = [row.get("id") for row in rejected_rows]
        if len(set(accepted_ids)) != len(accepted_ids):
            raise ValueError(f"{path}: admitted IDs are duplicated")
        if not all(isinstance(item, str) and item for item in rejected_ids) or len(set(rejected_ids)) != len(rejected_ids):
            raise ValueError(f"{path}: rejection IDs are incomplete or duplicated")
        if set(accepted_ids) & set(rejected_ids) or set(accepted_ids) | set(rejected_ids) != set(input_ids):
            raise ValueError(f"{path}: admitted and rejected artifacts do not partition the bound input")
        rejected_count = report.get("rejected") if capability_report else len(rejected_rows)
        if report.get("accepted") != len(accepted_ids) or rejected_count != len(rejected_ids):
            raise ValueError(f"{path}: admission counts do not reconcile with output artifacts")
        if capability_report:
            counts = Counter(
                row["qualification"].get("cell_id") for row in admitted_rows
            )
            if report.get("counts_by_cell") != dict(sorted(counts.items())):
                raise ValueError(f"{path}: admitted cell counts do not reconcile")
            for row in admitted_rows:
                identifier = row["record"]["id"]
                if row["qualification"].get("cell_id") != identity_cell.get(identifier):
                    raise ValueError(f"{identifier}: admitted cell conflicts with qualification queue")
        for identifier, state in [*((item, "accepted") for item in accepted_ids), *((item, "rejected") for item in rejected_ids)]:
            if identifier in disposition:
                raise ValueError(f"{identifier}: duplicate admission disposition")
            disposition[identifier] = "admitted" if state == "accepted" else state
        admission_inputs.append({
            "path": str(path), "sha256": file_sha256(path), "report_sha256": report["report_sha256"],
            "candidate_input_sha256": input_sha,
            "admitted_output": {"path": str(admitted_path), "sha256": file_sha256(admitted_path)},
            "rejected_output": (
                {"path": str(rejected_path), "sha256": file_sha256(rejected_path)}
                if rejected_path is not None else None
            ),
        })

    admitted_by_cell = Counter(identity_cell[item] for item, state in disposition.items() if state == "admitted")
    original_disposed_by_cell = Counter(
        identity_cell[item] for item in disposition if item in candidate_original_ref
    )
    empty_cells = sorted(cell_id for cell_id in cells if admitted_by_cell[cell_id] == 0)
    eligible: list[str] = []
    replacement_pending: list[str] = []
    exhausted: list[str] = []
    for cell_id in empty_cells:
        replacement_id = replacements.get(cell_id)
        if original_disposed_by_cell[cell_id] < 2:
            continue
        if replacement_id is None:
            eligible.append(cell_id)
        elif replacement_id not in disposition:
            replacement_pending.append(cell_id)
        else:
            exhausted.append(cell_id)

    original_generated = len(original_generated_refs)
    original_dispositioned_refs = {
        candidate_original_ref[item] for item in disposition if item in candidate_original_ref
    }
    original_dispositioned = len(original_dispositioned_refs)
    all_generated_dispositioned = generated.issubset(disposition)
    all_corrections_dispositioned = corrected_ids.issubset(disposition)
    all_replacements_dispositioned = set(replacements.values()).issubset(disposition)
    admitted = sum(state == "admitted" for state in disposition.values())
    complete = (
        original_generated == EXPECTED_DRAFTS
        and original_dispositioned == EXPECTED_DRAFTS
        and all_generated_dispositioned
        and all_corrections_dispositioned
        and all_replacements_dispositioned
    )
    passed = complete and admitted >= MINIMUM_ADMITTED and not empty_cells
    failed = bool(exhausted) or (complete and bool(empty_cells) and not eligible and not replacement_pending)
    status = "qualification-passed" if passed else "qualification-failed" if failed else "qualification-in-progress"

    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-qualification-summary/v1",
        "status": status,
        "gate_passed": passed,
        "contract": {
            "drafts": EXPECTED_DRAFTS, "cells": EXPECTED_CELLS,
            "minimum_admitted": MINIMUM_ADMITTED, "maximum_replacements_per_empty_cell": 1,
        },
        "inputs": {
            "queue": {"path": str(queue_path), "sha256": file_sha256(queue_path), "records": len(queue)},
            "candidates": candidate_inputs,
            "admission_reports": admission_inputs,
            "evaluation_surfaces_read": 0,
        },
        "totals": {
            "drafted": len(queue), "generated": len(generated),
            "original_generated": original_generated, "replacement_generated": len(replacements),
            "corrected": len(corrected_ids),
            "dispositioned": len(disposition), "admitted": admitted,
            "rejected": sum(state == "rejected" for state in disposition.values()),
            "generation_yield": _rate(original_generated, len(queue)),
            "admission_yield_from_generated": _rate(admitted, len(generated)),
            "admission_yield_from_dispositioned": _rate(admitted, len(disposition)),
        },
        "coverage": {
            "admitted_cells": EXPECTED_CELLS - len(empty_cells), "empty_cells": empty_cells,
        },
        "bounded_replacements": {
            "eligible_cells": eligible, "pending_cells": replacement_pending,
            "exhausted_cells": exhausted, "generated_by_cell": dict(sorted(replacements.items())),
        },
        "by_primary_capability": _dimension_rows(("primary_capability",), cells, generated, set(candidate_original_ref), corrected_ids, disposition, identity_cell),
        "by_lane": _dimension_rows(("lane",), cells, generated, set(candidate_original_ref), corrected_ids, disposition, identity_cell),
        "by_task_type": _dimension_rows(("task_type",), cells, generated, set(candidate_original_ref), corrected_ids, disposition, identity_cell),
        "by_cell": _dimension_rows(("cell_id",), cells, generated, set(candidate_original_ref), corrected_ids, disposition, identity_cell),
        "pass_requirements": {
            "all_original_drafts_generated": original_generated == EXPECTED_DRAFTS,
            "all_original_drafts_dispositioned": original_dispositioned == EXPECTED_DRAFTS,
            "all_generated_candidates_dispositioned": all_generated_dispositioned,
            "all_corrections_dispositioned": all_corrections_dispositioned,
            "all_replacements_dispositioned": all_replacements_dispositioned,
            "minimum_admitted_met": admitted >= MINIMUM_ADMITTED,
            "every_cell_admitted": not empty_cells,
        },
    }
    report["by_family"] = _five_families(report["by_lane"])
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, action="append", default=[])
    parser.add_argument("--admission-report", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = summarize(args.queue, args.candidates, args.admission_report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "admitted": report["totals"]["admitted"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
