#!/usr/bin/env python3
"""Fail-closed admission for the Gate 2 capability qualification matrix.

This layer deliberately does not read evaluation artifacts.  It verifies a
sealed separation attestation produced by the independent comparison stage,
then delegates executable reference/known-bad checks and ordinary candidate
validation to :mod:`scripts.data.admit_expansion`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_expansion import (  # noqa: E402
    AdmissionFailure,
    admit_records,
    canonical_json,
    read_jsonl,
    verify,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256, load_sealed  # noqa: E402
from scripts.eval.contracts import sha256_text  # noqa: E402


SCHEMA_VERSION = "ganesh-mini-capability-qualification-envelope/v1"
OUTPUT_SCHEMA_VERSION = "ganesh-mini-capability-qualified-record/v1"
REPORT_SCHEMA_VERSION = "ganesh-mini-capability-qualification-admission/v1"
EMPTY_EVALUATION_INDEX = {
    "prompts": {}, "prompt_simhashes": [], "code_hashes": {}, "inspected": [],
}


def _sha(value: Any, where: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise AdmissionFailure(f"{where}: expected lowercase SHA-256")
    return value


def _sealed(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AdmissionFailure(f"{where}: expected object")
    body = dict(value)
    claimed = body.pop("evidence_sha256", None)
    if claimed != canonical_sha256(body):
        raise AdmissionFailure(f"{where}: evidence seal mismatch")
    return value


def _required_true(value: dict[str, Any], fields: Iterable[str], where: str) -> None:
    for field in fields:
        if value.get(field) is not True:
            raise AdmissionFailure(f"{where}.{field}: must be explicitly true")


def _required_zero(value: dict[str, Any], field: str, where: str) -> None:
    if value.get(field) != 0:
        raise AdmissionFailure(f"{where}.{field}: must be exactly zero")


def load_queue(queue_path: Path, manifest_path: Path, plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    manifest = load_sealed(manifest_path, "manifest_sha256")
    payload = queue_path.read_bytes()
    if (
        manifest.get("schema_version") != "ganesh-mini-capability-qualification-queue-manifest/v1"
        or manifest.get("status") != "ready-for-isolated-teacher-qualification"
        or manifest.get("plan_sha256") != plan["plan_sha256"]
        or manifest.get("queue_sha256") != hashlib.sha256(payload).hexdigest()
    ):
        raise ValueError("qualification queue manifest does not bind the plan and queue")
    rows = read_jsonl(queue_path)
    if len(rows) != manifest.get("records") or len(rows) < 240:
        raise ValueError("qualification queue record count mismatch")
    by_id: dict[str, dict[str, Any]] = {}
    source_identities: set[tuple[Any, Any, Any]] = set()
    source_queue_ids: set[str] = set()
    cell_counts: Counter[str] = Counter()
    cell_contracts = {row["cell_id"]: row for row in plan["matrix"]["cell_contracts"]}
    for row in rows:
        required = {
            "id", "cell_id", "primary_capability", "assigned_cross_cutting_dimension",
            "lane", "task_type", "source_queue_id", "source",
        }
        if not isinstance(row, dict) or not required.issubset(row):
            raise ValueError("qualification queue row is incomplete")
        if row["id"] in by_id:
            raise ValueError("qualification queue IDs are not unique")
        contract = cell_contracts.get(row["cell_id"])
        if contract is None or any(
            row[field] != contract[field]
            for field in ("primary_capability", "lane", "task_type", "assigned_cross_cutting_dimension")
        ):
            raise ValueError("qualification queue row does not match its plan cell")
        source = row["source"]
        identity = (source.get("dataset"), source.get("revision"), source.get("record_id"))
        if (
            not all(isinstance(part, str) and part for part in identity)
            or identity in source_identities
            or not isinstance(row["source_queue_id"], str)
            or not row["source_queue_id"]
            or row["source_queue_id"] in source_queue_ids
        ):
            raise ValueError("qualification queue source identities are incomplete or reused")
        by_id[row["id"]] = row
        source_identities.add(identity)
        source_queue_ids.add(row["source_queue_id"])
        cell_counts[row["cell_id"]] += 1
    allowed_cells = {row["cell_id"] for row in plan["matrix"]["cell_contracts"]}
    if set(cell_counts) != allowed_cells or any(count < 2 for count in cell_counts.values()):
        raise ValueError("qualification queue does not cover every plan cell")
    if (
        manifest.get("unique_source_identities") != len(source_identities)
        or manifest.get("cells") != len(cell_counts)
        or manifest.get("records_per_cell") != dict(sorted(cell_counts.items()))
    ):
        raise ValueError("qualification queue manifest summary mismatch")
    return by_id


def _candidate_from_envelope(envelope: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Accept a wrapper or a training-admission candidate with qualification metadata."""
    if envelope.get("schema_version") == SCHEMA_VERSION:
        candidate = envelope.get("candidate", envelope.get("training_candidate"))
        qualification = envelope.get("qualification")
    else:
        candidate = {key: value for key, value in envelope.items() if key != "qualification"}
        qualification = envelope.get("qualification")
    if not isinstance(candidate, dict) or not isinstance(qualification, dict):
        raise AdmissionFailure("candidate and qualification metadata are required")
    return candidate, qualification


def validate_envelope(
    envelope: Any,
    plan: dict[str, Any],
    queue_by_id: dict[str, dict[str, Any]],
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if not isinstance(envelope, dict):
        raise AdmissionFailure("qualification envelope must be an object")
    candidate, qualification = _candidate_from_envelope(envelope)
    candidate_sha256 = canonical_sha256(candidate)
    queue_id = qualification.get("queue_id")
    if not isinstance(queue_id, str) or queue_id not in queue_by_id:
        raise AdmissionFailure("qualification.queue_id is not in the sealed queue")
    queue_row = queue_by_id[queue_id]
    queue_sha256 = canonical_sha256(queue_row)

    bindings = {
        "id": candidate.get("id"),
        "lane": candidate.get("lane"),
        "task_type": candidate.get("task_type"),
    }
    for field, expected in (
        ("id", queue_row["id"]),
        ("lane", queue_row["lane"]),
        ("task_type", queue_row["task_type"]),
    ):
        if bindings[field] != expected:
            raise AdmissionFailure(f"candidate {field} does not match its queue cell")
    for field in ("cell_id", "primary_capability", "assigned_cross_cutting_dimension", "source_queue_id"):
        if qualification.get(field) != queue_row[field]:
            raise AdmissionFailure(f"qualification.{field} does not match the sealed queue")
    if candidate.get("source") != queue_row["source"]:
        raise AdmissionFailure("candidate source lineage does not match the sealed queue")

    evidence = qualification.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != {
        "teacher", "test_author", "semantic_review", "separation", "lineage",
    }:
        raise AdmissionFailure("qualification evidence set is incomplete")
    teacher = _sealed(evidence["teacher"], "teacher")
    test_author = _sealed(evidence["test_author"], "test_author")
    semantic = _sealed(evidence["semantic_review"], "semantic_review")
    separation = _sealed(evidence["separation"], "separation")
    lineage = _sealed(evidence["lineage"], "lineage")

    for name, item in (
        ("teacher", teacher), ("test_author", test_author),
        ("semantic_review", semantic), ("separation", separation), ("lineage", lineage),
    ):
        if item.get("candidate_sha256") != candidate_sha256:
            raise AdmissionFailure(f"{name}: candidate binding mismatch")

    if (
        teacher.get("queue_record_sha256") != queue_sha256
        or teacher.get("source_queue_id") != queue_row["source_queue_id"]
        or teacher.get("source_record_sha256") != candidate["source"].get("source_record_sha256")
        or teacher.get("assistant_sha256") != sha256_text(candidate["messages"][1]["content"])
    ):
        raise AdmissionFailure("teacher evidence does not bind candidate, source, and queue")
    _sha(teacher.get("rendered_prompt_sha256"), "teacher.rendered_prompt_sha256")
    teacher_visibility = teacher.get("visibility")
    if not isinstance(teacher_visibility, dict):
        raise AdmissionFailure("teacher.visibility is required")
    _required_true(teacher_visibility, ("training_stimulus", "assigned_ontology", "runtime_contract"), "teacher.visibility")
    _required_zero(teacher_visibility, "evaluation_artifacts_read", "teacher.visibility")

    specification_sha256 = sha256_text(candidate["messages"][0]["content"])
    tests = [item["sha256"] for item in candidate["verification_task"]["files"] if item.get("role") == "test"]
    if not tests:
        raise AdmissionFailure("candidate must contain at least one executable test file")
    if (
        test_author.get("specification_sha256") != specification_sha256
        or test_author.get("test_sha256s") != tests
        or test_author.get("origin") != candidate.get("test_origin")
        or test_author.get("origin") not in config.get("allowed_test_origins", [])
    ):
        raise AdmissionFailure("test-author evidence does not bind independent candidate tests")
    test_visibility = test_author.get("visibility")
    if not isinstance(test_visibility, dict):
        raise AdmissionFailure("test_author.visibility is required")
    _required_true(test_visibility, ("specification_only", "independent_of_teacher"), "test_author.visibility")
    for forbidden in ("reference_visible", "known_bad_visible", "teacher_context_visible"):
        if test_visibility.get(forbidden) is not False:
            raise AdmissionFailure(f"test_author.visibility.{forbidden}: must be explicitly false")
    _required_zero(test_visibility, "evaluation_artifacts_read", "test_author.visibility")

    if (
        semantic.get("specification_sha256") != specification_sha256
        or semantic.get("primary_capability") != queue_row["primary_capability"]
        or semantic.get("assigned_cross_cutting_dimension") != queue_row["assigned_cross_cutting_dimension"]
        or semantic.get("verdict") != "pass"
    ):
        raise AdmissionFailure("semantic review does not confirm the assigned ontology")
    _required_true(semantic, ("primary_capability_is_substantive",), "semantic_review")
    if semantic.get("generic_edge_case_boilerplate_is_primary") is not False:
        raise AdmissionFailure("semantic review accepted generic edge-case boilerplate as primary")
    semantic_visibility = semantic.get("visibility")
    if not isinstance(semantic_visibility, dict):
        raise AdmissionFailure("semantic_review.visibility is required")
    _required_true(semantic_visibility, ("specification_and_assigned_labels_only",), "semantic_review.visibility")
    if semantic_visibility.get("verifier_outputs_visible") is not False:
        raise AdmissionFailure("semantic reviewer saw verifier outputs")
    _required_zero(semantic_visibility, "evaluation_artifacts_read", "semantic_review.visibility")

    _required_true(
        separation,
        (
            "exact_training_passed", "normalized_training_passed", "fuzzy_training_passed",
            "exact_evaluation_passed", "normalized_evaluation_passed", "fuzzy_evaluation_passed",
        ),
        "separation",
    )
    _sha(separation.get("comparison_manifest_sha256"), "separation.comparison_manifest_sha256")
    _required_zero(separation, "evaluation_artifacts_read_by_construction", "separation")

    source = candidate["source"]
    source_identity = {key: source.get(key) for key in ("dataset", "revision", "record_id")}
    if (
        lineage.get("queue_record_sha256") != queue_sha256
        or lineage.get("source_identity") != source_identity
        or lineage.get("source_record_sha256") != source.get("source_record_sha256")
        or lineage.get("teacher_evidence_sha256") != teacher["evidence_sha256"]
        or lineage.get("test_author_evidence_sha256") != test_author["evidence_sha256"]
        or lineage.get("semantic_review_evidence_sha256") != semantic["evidence_sha256"]
        or lineage.get("separation_evidence_sha256") != separation["evidence_sha256"]
    ):
        raise AdmissionFailure("lineage evidence chain is incomplete or mismatched")
    _required_true(lineage, ("complete",), "lineage")

    correction_passes = qualification.get("correction_passes")
    if type(correction_passes) is not int or correction_passes not in (0, 1):
        raise AdmissionFailure("correction_passes must be zero or one")
    if correction_passes == 1:
        correction = _sealed(qualification.get("correction"), "correction")
        if (
            correction.get("candidate_sha256") != candidate_sha256
            or not isinstance(correction.get("parent_candidate_sha256"), str)
        ):
            raise AdmissionFailure("correction evidence does not bind candidate and parent")
        _sha(correction["parent_candidate_sha256"], "correction.parent_candidate_sha256")
    elif qualification.get("correction") is not None:
        raise AdmissionFailure("uncorrected candidate must not carry correction evidence")

    metadata = {
        "queue_id": queue_id,
        "queue_record_sha256": queue_sha256,
        "cell_id": queue_row["cell_id"],
        "primary_capability": queue_row["primary_capability"],
        "assigned_cross_cutting_dimension": queue_row["assigned_cross_cutting_dimension"],
        "source_queue_id": queue_row["source_queue_id"],
        "candidate_sha256": candidate_sha256,
        "correction_passes": correction_passes,
        "evidence_sha256s": {name: item["evidence_sha256"] for name, item in evidence.items()},
    }
    return candidate, metadata, qualification


def admit_qualification(
    envelopes: Iterable[Any],
    plan: dict[str, Any],
    queue_by_id: dict[str, dict[str, Any]],
    config: dict[str, Any],
    runtime_config: Path,
    verifier: Callable[[dict[str, Any], str, Path], dict[str, Any]] = verify,
    verifier_workers: int = 1,
    record_workers: int = 1,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = list(envelopes)
    valid: list[dict[str, Any]] = []
    metadata: list[dict[str, Any]] = []
    input_lines: list[int] = []
    rejected: list[dict[str, Any]] = []
    seen_queue_ids: set[str] = set()
    for line, envelope in enumerate(rows, 1):
        record_id = envelope.get("id", f"line-{line}") if isinstance(envelope, dict) else f"line-{line}"
        try:
            candidate, item_metadata, _ = validate_envelope(envelope, plan, queue_by_id, config)
            record_id = candidate.get("id", record_id)
            if item_metadata["queue_id"] in seen_queue_ids:
                raise AdmissionFailure("sealed queue assignment reused by multiple candidates")
            seen_queue_ids.add(item_metadata["queue_id"])
            valid.append(candidate)
            metadata.append(item_metadata)
            input_lines.append(line)
        except (AdmissionFailure, KeyError, TypeError, ValueError) as exc:
            rejected.append({"line": line, "id": record_id, "reason": str(exc)})

    admitted_rows, execution_rejections = admit_records(
        valid, config, EMPTY_EVALUATION_INDEX, runtime_config, verifier,
        verifier_workers=verifier_workers, record_workers=record_workers,
    )
    admitted_by_id = {row["id"]: row for row in admitted_rows}
    execution_rejected_by_id = {row["id"]: row for row in execution_rejections}
    output: list[dict[str, Any]] = []
    for candidate, item_metadata, line in zip(valid, metadata, input_lines, strict=True):
        record_id = candidate["id"]
        if record_id in execution_rejected_by_id:
            rejection = dict(execution_rejected_by_id[record_id])
            rejection["line"] = line
            rejected.append(rejection)
            continue
        admitted = admitted_by_id.get(record_id)
        if admitted is None:
            raise RuntimeError(f"{record_id}: executable admission result missing")
        output.append({
            "schema_version": OUTPUT_SCHEMA_VERSION,
            "qualification": item_metadata,
            "record": admitted,
        })
    rejected.sort(key=lambda item: item["line"])
    return output, rejected


def build_report(
    *, mode: str, plan: dict[str, Any], queue_manifest: dict[str, Any],
    input_path: Path, output_path: Path, rejected_path: Path,
    admitted: list[dict[str, Any]], rejected: list[dict[str, Any]],
    verifier_workers: int, record_workers: int,
) -> dict[str, Any]:
    counts = Counter(row["qualification"]["cell_id"] for row in admitted)
    all_cells = {row["cell_id"] for row in plan["matrix"]["cell_contracts"]}
    missing_cells = sorted(all_cells - set(counts))
    final_gate_passed = len(admitted) >= plan["qualification"]["minimum_admitted"] and not missing_cells
    status = (
        "passed" if mode == "final" and final_gate_passed
        else "failed" if mode == "final"
        else "candidate-admission-complete"
    )
    output_payload = output_path.read_bytes()
    rejected_payload = rejected_path.read_bytes()
    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "status": status,
        "mode": mode,
        "plan_sha256": plan["plan_sha256"],
        "queue_manifest_sha256": queue_manifest["manifest_sha256"],
        "input": {"path": str(input_path), "sha256": hashlib.sha256(input_path.read_bytes()).hexdigest()},
        "accepted": len(admitted),
        "rejected": len(rejected),
        "counts_by_cell": dict(sorted(counts.items())),
        "missing_cells": missing_cells,
        "final_gate": {
            "minimum_admitted": plan["qualification"]["minimum_admitted"],
            "minimum_per_cell": plan["qualification"]["minimum_admitted_per_cell"],
            "passed": final_gate_passed,
        },
        "evaluation_artifacts_read": 0,
        "execution": {
            "record_workers": record_workers,
            "verifier_workers_per_record": verifier_workers,
            "maximum_parallel_verifiers": record_workers * verifier_workers,
        },
        "outputs": {
            "admitted": {"path": str(output_path), "bytes": len(output_payload), "sha256": hashlib.sha256(output_payload).hexdigest()},
            "rejected": {"path": str(rejected_path), "bytes": len(rejected_payload), "sha256": hashlib.sha256(rejected_payload).hexdigest()},
        },
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("configs/data/expansion_v1.json"))
    parser.add_argument("--runtime-config", type=Path, default=Path("configs/eval/runtimes.json"))
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rejected-output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--mode", choices=("candidate", "final"), default="candidate")
    parser.add_argument("--verifier-workers", type=int, default=1)
    parser.add_argument("--record-workers", type=int, default=1)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    plan = load_sealed(args.plan, "plan_sha256")
    if (
        plan.get("schema_version") != "ganesh-mini-capability-stratified-corpus-plan/v1"
        or plan.get("matrix", {}).get("cells") != 120
    ):
        raise ValueError("unsupported capability qualification plan")
    queue_by_id = load_queue(args.queue, args.queue_manifest, plan)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    admitted, rejected = admit_qualification(
        read_jsonl(args.input), plan, queue_by_id, config, args.runtime_config,
        verifier_workers=args.verifier_workers, record_workers=args.record_workers,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(b"".join(canonical_json(row) + b"\n" for row in admitted))
    args.rejected_output.parent.mkdir(parents=True, exist_ok=True)
    args.rejected_output.write_text(json.dumps(rejected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    queue_manifest = load_sealed(args.queue_manifest, "manifest_sha256")
    report = build_report(
        mode=args.mode, plan=plan, queue_manifest=queue_manifest,
        input_path=args.input, output_path=args.output, rejected_path=args.rejected_output,
        admitted=admitted, rejected=rejected,
        verifier_workers=args.verifier_workers, record_workers=args.record_workers,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "accepted": len(admitted), "rejected": len(rejected), "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
