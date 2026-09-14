#!/usr/bin/env python3
"""Fail-closed admission for the Gate 2 capability qualification matrix.

This layer deliberately does not read evaluation artifacts.  It verifies a
sealed separation attestation produced by the independent comparison stage,
then delegates executable reference/known-bad checks and ordinary candidate
validation to :mod:`scripts.data.admit_expansion`.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import threading
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
from scripts.eval.contracts import sha256_object, sha256_text  # noqa: E402
from scripts.verify.sandbox import SANDBOX_CONTRACT, infrastructure_failure  # noqa: E402


SCHEMA_VERSION = "ganesh-mini-capability-qualification-envelope/v1"
OUTPUT_SCHEMA_VERSION = "ganesh-mini-capability-qualified-record/v1"
REPORT_SCHEMA_VERSION = "ganesh-mini-capability-qualification-admission/v1"
REUSE_LEDGER_SCHEMA_VERSION = "ganesh-mini-capability-executable-reuse-ledger/v1"
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


def file_binding(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"path": str(path), "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def execution_contract(config_path: Path, runtime_config_path: Path) -> dict[str, Any]:
    """Bind every non-candidate input capable of changing verifier meaning."""
    config = json.loads(config_path.read_text(encoding="utf-8"))
    runtimes = json.loads(runtime_config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or not isinstance(runtimes, dict):
        raise ValueError("admission config and runtime config must be objects")
    return {
        "admission_config": file_binding(config_path),
        "admission_config_sha256": canonical_sha256(config),
        "runtime_config": file_binding(runtime_config_path),
        "runtime_config_sha256": canonical_sha256(runtimes),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
    }


def _validate_execution_contract(contract: Any) -> dict[str, Any]:
    if not isinstance(contract, dict) or contract.get("sandbox_contract_sha256") != sha256_object(SANDBOX_CONTRACT):
        raise ValueError("execution contract does not bind the current sandbox contract")
    config_path = _verify_bound_artifact(contract.get("admission_config"), "admission config")
    runtime_path = _verify_bound_artifact(contract.get("runtime_config"), "runtime config")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    runtimes = json.loads(runtime_path.read_text(encoding="utf-8"))
    if (
        contract.get("admission_config_sha256") != canonical_sha256(config)
        or contract.get("runtime_config_sha256") != canonical_sha256(runtimes)
    ):
        raise ValueError("execution contract canonical config binding mismatch")
    return runtimes


def candidate_execution_fingerprint(candidate: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    task = candidate["verification_task"]
    runtime_document = _validate_execution_contract(contract)
    runtime = runtime_document.get("runtimes", {}).get(task.get("runtime_id"))
    if not isinstance(runtime, dict):
        raise AdmissionFailure("candidate runtime is absent from the bound runtime config")
    return {
        "candidate_sha256": canonical_sha256(candidate),
        "verification_task_sha256": sha256_object(task),
        "reference_sha256": task["validation"]["reference"]["sha256"],
        "known_bad": [
            {"label": item["label"], "sha256": item["sha256"]}
            for item in task["validation"]["known_bad"]
        ],
        "files": [
            {"path": item["path"], "role": item["role"], "sha256": item["sha256"]}
            for item in task["files"]
        ],
        "runtime": {
            "runtime_id": task["runtime_id"], "image": runtime.get("image"),
            "image_id": runtime.get("image_id"), "manifest_digest": runtime.get("manifest_digest"),
            "rootfs_layers": runtime.get("rootfs_layers"), "platform": runtime.get("platform"),
            "commands": runtime.get("commands"),
        },
        "limits": task["limits"],
        "admission_config_sha256": contract["admission_config_sha256"],
        "runtime_config_sha256": contract["runtime_config_sha256"],
        "sandbox_contract_sha256": contract["sandbox_contract_sha256"],
    }


def _verify_bound_artifact(binding: Any, where: str) -> Path:
    if not isinstance(binding, dict) or not isinstance(binding.get("path"), str):
        raise ValueError(f"{where}: artifact binding is absent")
    path = Path(binding["path"])
    payload = path.read_bytes()
    if (
        binding.get("sha256") != hashlib.sha256(payload).hexdigest()
        or ("bytes" in binding and binding.get("bytes") != len(payload))
    ):
        raise ValueError(f"{where}: artifact binding changed")
    return path


def _result_matches_contract(result: Any, fingerprint: dict[str, Any]) -> bool:
    runtime = fingerprint["runtime"]
    expected_image = f"{str(runtime['image']).rsplit(':', 1)[0]}@{runtime['manifest_digest']}"
    return (
        isinstance(result, dict)
        and result.get("timed_out") is False
        and result.get("runtime_id") == runtime["runtime_id"]
        and result.get("image") == expected_image
        and result.get("image_id") == runtime["image_id"]
        and result.get("commands") == runtime["commands"]
        and result.get("sandbox_contract_sha256") == fingerprint["sandbox_contract_sha256"]
        and isinstance(result.get("exit_codes"), list)
        and infrastructure_failure(result) is None
    )


def load_execution_reuse(
    prior_report_path: Path, current_contract: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """Load a sealed prior run and expose only complete, non-timeout verifier evidence."""
    _validate_execution_contract(current_contract)
    report = load_sealed(prior_report_path, "report_sha256")
    if (
        report.get("schema_version") != REPORT_SCHEMA_VERSION
        or report.get("mode") != "final"
        or report.get("evaluation_artifacts_read") != 0
        or report.get("execution_contract") != current_contract
    ):
        raise ValueError("prior admission report does not match the current execution contract")
    envelope_path = _verify_bound_artifact(report.get("input"), "prior admission input")
    admitted_path = _verify_bound_artifact(report.get("outputs", {}).get("admitted"), "prior admitted output")
    rejected_path = _verify_bound_artifact(report.get("outputs", {}).get("rejected"), "prior rejected output")
    envelopes = read_jsonl(envelope_path)
    candidates: dict[str, dict[str, Any]] = {}
    for envelope in envelopes:
        candidate, _ = _candidate_from_envelope(envelope)
        identifier = candidate.get("id")
        if not isinstance(identifier, str) or identifier in candidates:
            raise ValueError("prior admission envelopes have missing or duplicate candidate IDs")
        candidates[identifier] = candidate
    admitted = read_jsonl(admitted_path)
    rejected = json.loads(rejected_path.read_text(encoding="utf-8"))
    if (
        not isinstance(rejected, list)
        or report.get("accepted") != len(admitted)
        or report.get("rejected") != len(rejected)
    ):
        raise ValueError("prior admission artifact counts do not match the sealed report")

    outcome_by_id: dict[str, tuple[str, dict[str, Any]]] = {}
    disposition_ids: set[str] = set()
    for row in admitted:
        identifier = row.get("record", {}).get("id") if isinstance(row, dict) else None
        evidence = row.get("record", {}).get("verification") if isinstance(row, dict) else None
        if not isinstance(identifier, str) or not isinstance(evidence, dict) or identifier in outcome_by_id:
            raise ValueError("prior admitted artifact has invalid candidate identity or evidence")
        body = dict(evidence)
        claimed = body.pop("evidence_sha256", None)
        if claimed != sha256_object(body):
            raise ValueError("prior admitted executable evidence seal mismatch")
        outcome_by_id[identifier] = ("admitted", evidence)
        disposition_ids.add(identifier)
    for row in rejected:
        identifier = row.get("id") if isinstance(row, dict) else None
        if not isinstance(identifier, str) or identifier in disposition_ids:
            raise ValueError("prior rejection identities do not exactly partition outcomes")
        disposition_ids.add(identifier)
        evidence = row.get("evidence")
        if isinstance(evidence, dict):
            outcome_by_id[identifier] = ("rejected", evidence)
    if disposition_ids != set(candidates):
        raise ValueError("prior admission outcomes do not exactly partition prior envelopes")

    reusable: dict[str, dict[str, Any]] = {}
    for identifier, (outcome, evidence) in outcome_by_id.items():
        candidate = candidates.get(identifier)
        if candidate is None:
            raise ValueError("prior executable outcome is not bound to a prior envelope")
        fingerprint = candidate_execution_fingerprint(candidate, current_contract)
        task = candidate["verification_task"]
        if outcome == "admitted" and evidence.get("task_sha256") != fingerprint["verification_task_sha256"]:
            raise ValueError("prior admitted evidence has a mismatched verification task hash")
        reference = evidence.get("reference")
        known_bad_rows = evidence.get("known_bad")
        expected_bad = fingerprint["known_bad"]
        if (
            not _result_matches_contract(reference, fingerprint)
            or not isinstance(known_bad_rows, list)
            or [row.get("label") for row in known_bad_rows if isinstance(row, dict)]
               != [row["label"] for row in expected_bad]
            or any(
                not isinstance(row, dict) or not _result_matches_contract(row.get("result"), fingerprint)
                for row in known_bad_rows
            )
        ):
            continue
        results = {fingerprint["reference_sha256"]: copy.deepcopy(reference)}
        for expected, evidence_row in zip(expected_bad, known_bad_rows, strict=True):
            results[expected["sha256"]] = copy.deepcopy(evidence_row["result"])
        reusable[identifier] = {
            "fingerprint": fingerprint, "results": results, "prior_outcome": outcome,
        }
    binding = {
        "prior_report": file_binding(prior_report_path),
        "prior_report_sha256": report["report_sha256"],
        "eligible_candidate_ids": sorted(reusable),
    }
    return reusable, binding


def write_reuse_ledger(
    path: Path, source_binding: dict[str, Any], summary: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any]:
    ledger: dict[str, Any] = {
        "schema_version": REUSE_LEDGER_SCHEMA_VERSION,
        "status": "complete",
        "source": source_binding,
        "execution_contract_sha256": canonical_sha256(contract),
        "eligible_candidate_ids": summary.get("eligible_candidate_ids", []),
        "reused_candidate_ids": summary.get("reused_candidate_ids", []),
        "executed_candidate_ids": summary.get("executed_candidate_ids", []),
        "counts": {
            "eligible": summary.get("eligible", 0),
            "reused": summary.get("reused", 0),
            "executed": summary.get("executed", 0),
        },
        "evaluation_artifacts_read": 0,
    }
    ledger["ledger_sha256"] = canonical_sha256(ledger)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return ledger


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
    reuse_index: dict[str, dict[str, Any]] | None = None,
    reuse_contract: dict[str, Any] | None = None,
    reuse_ledger: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = list(envelopes)
    valid: list[dict[str, Any]] = []
    metadata: list[dict[str, Any]] = []
    input_lines: list[int] = []
    rejected: list[dict[str, Any]] = []
    seen_queue_ids: set[str] = set()
    selected_reuse: dict[str, dict[str, Any]] = {}
    for line, envelope in enumerate(rows, 1):
        record_id = f"line-{line}"
        if isinstance(envelope, dict):
            nested = envelope.get("candidate", envelope.get("training_candidate"))
            if isinstance(nested, dict) and isinstance(nested.get("id"), str) and nested["id"]:
                record_id = nested["id"]
            elif isinstance(envelope.get("id"), str) and envelope["id"]:
                record_id = envelope["id"]
        try:
            candidate, item_metadata, _ = validate_envelope(envelope, plan, queue_by_id, config)
            record_id = candidate.get("id", record_id)
            if item_metadata["queue_id"] in seen_queue_ids:
                raise AdmissionFailure("sealed queue assignment reused by multiple candidates")
            seen_queue_ids.add(item_metadata["queue_id"])
            prior = (reuse_index or {}).get(candidate["id"])
            replacement = queue_by_id[item_metadata["queue_id"]].get("replacement_attempt") is not None
            if prior is not None and item_metadata["correction_passes"] == 0 and not replacement:
                if reuse_contract is None:
                    raise AdmissionFailure("executable reuse contract is absent")
                current_fingerprint = candidate_execution_fingerprint(candidate, reuse_contract)
                if prior.get("fingerprint") != current_fingerprint:
                    raise AdmissionFailure("prior executable evidence fingerprint mismatch")
                selected_reuse[candidate["id"]] = prior
            valid.append(candidate)
            metadata.append(item_metadata)
            input_lines.append(line)
        except (AdmissionFailure, KeyError, TypeError, ValueError) as exc:
            rejected.append({"line": line, "id": record_id, "reason": str(exc)})

    reused_calls: dict[str, set[str]] = {}
    executed_ids: set[str] = set()
    reuse_lock = threading.Lock()

    def verifier_with_reuse(task: dict[str, Any], code: str, runtime: Path) -> dict[str, Any]:
        identifier = task.get("task_id")
        entry = selected_reuse.get(identifier)
        code_sha256 = sha256_text(code)
        if entry is not None:
            result = entry["results"].get(code_sha256)
            if result is None:
                raise AdmissionFailure(f"{identifier}: prior executable evidence lacks an exact code-hash result")
            with reuse_lock:
                reused_calls.setdefault(identifier, set()).add(code_sha256)
            return copy.deepcopy(result)
        with reuse_lock:
            if isinstance(identifier, str):
                executed_ids.add(identifier)
        return verifier(task, code, runtime)

    admitted_rows, execution_rejections = admit_records(
        valid, config, EMPTY_EVALUATION_INDEX, runtime_config, verifier_with_reuse,
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
    if reuse_ledger is not None:
        fully_reused = sorted(
            identifier for identifier, entry in selected_reuse.items()
            if reused_calls.get(identifier) == set(entry["results"])
        )
        reuse_ledger.update({
            "eligible_candidate_ids": sorted(selected_reuse),
            "reused_candidate_ids": fully_reused,
            "executed_candidate_ids": sorted(executed_ids),
            "eligible": len(selected_reuse), "reused": len(fully_reused),
            "executed": len(executed_ids),
        })
    return output, rejected


def build_report(
    *, mode: str, plan: dict[str, Any], queue_manifest: dict[str, Any],
    input_path: Path, output_path: Path, rejected_path: Path,
    admitted: list[dict[str, Any]], rejected: list[dict[str, Any]],
    verifier_workers: int, record_workers: int,
    queue_by_id: dict[str, dict[str, Any]] | None = None,
    execution_contract_value: dict[str, Any] | None = None,
    reuse_summary: dict[str, Any] | None = None,
    reuse_ledger_binding: dict[str, Any] | None = None,
) -> dict[str, Any]:
    counts = Counter(row["qualification"]["cell_id"] for row in admitted)
    all_cells = {row["cell_id"] for row in plan["matrix"]["cell_contracts"]}
    missing_cells = sorted(all_cells - set(counts))
    input_rows = read_jsonl(input_path)
    input_queue_ids: list[str] = []
    input_binding_failures: list[dict[str, Any]] = []
    for line, envelope in enumerate(input_rows, 1):
        qualification = envelope.get("qualification") if isinstance(envelope, dict) else None
        candidate = None
        if isinstance(envelope, dict) and envelope.get("schema_version") == SCHEMA_VERSION:
            candidate = envelope.get("candidate", envelope.get("training_candidate"))
        elif isinstance(envelope, dict):
            candidate = {key: value for key, value in envelope.items() if key != "qualification"}
        queue_id = qualification.get("queue_id") if isinstance(qualification, dict) else None
        if isinstance(queue_id, str) and queue_id:
            input_queue_ids.append(queue_id)
        else:
            input_binding_failures.append({"line": line, "reason": "missing qualification.queue_id"})
            continue
        queue_row = queue_by_id.get(queue_id) if queue_by_id is not None else None
        if not isinstance(queue_row, dict) or not isinstance(candidate, dict):
            input_binding_failures.append({"line": line, "queue_id": queue_id, "reason": "queue or candidate binding absent"})
            continue
        expected_qualification = {
            "cell_id": queue_row["cell_id"],
            "primary_capability": queue_row["primary_capability"],
            "assigned_cross_cutting_dimension": queue_row["assigned_cross_cutting_dimension"],
            "source_queue_id": queue_row["source_queue_id"],
        }
        expected_candidate = {
            "id": queue_row["id"], "lane": queue_row["lane"],
            "task_type": queue_row["task_type"], "source": queue_row["source"],
        }
        if (
            any(qualification.get(key) != value for key, value in expected_qualification.items())
            or any(candidate.get(key) != value for key, value in expected_candidate.items())
        ):
            input_binding_failures.append({"line": line, "queue_id": queue_id, "reason": "cell or source binding mismatch"})
    queue_id_counts = Counter(input_queue_ids)
    expected_queue_ids = set(queue_by_id or {})
    original_queue_ids = {
        identifier for identifier, row in (queue_by_id or {}).items()
        if row.get("replacement_attempt") is None
    }
    replacement_rows = [
        row for row in (queue_by_id or {}).values()
        if row.get("replacement_attempt") is not None
    ]
    replacement_cells = [row.get("replacement_for_cell_id") for row in replacement_rows]
    missing_queue_ids = sorted(expected_queue_ids - set(queue_id_counts))
    unexpected_queue_ids = sorted(set(queue_id_counts) - expected_queue_ids)
    duplicate_queue_ids = sorted(identifier for identifier, count in queue_id_counts.items() if count != 1)
    full_queue_dispositioned = (
        queue_by_id is not None
        and len(original_queue_ids) == plan["qualification"]["drafts"]
        and all(row.get("replacement_attempt") == 1 for row in replacement_rows)
        and len(replacement_cells) == len(set(replacement_cells))
        and len(input_rows) == len(expected_queue_ids)
        and not missing_queue_ids
        and not unexpected_queue_ids
        and not duplicate_queue_ids
        and not input_binding_failures
        and len(admitted) + len(rejected) == len(input_rows)
    )
    final_gate_passed = (
        len(admitted) >= plan["qualification"]["minimum_admitted"]
        and not missing_cells
        and full_queue_dispositioned
    )
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
        "input": file_binding(input_path),
        "accepted": len(admitted),
        "rejected": len(rejected),
        "counts_by_cell": dict(sorted(counts.items())),
        "missing_cells": missing_cells,
        "queue_disposition": {
            "expected_originals": len(original_queue_ids),
            "sealed_originals": len(original_queue_ids),
            "bounded_replacements": len(replacement_rows),
            "input_envelopes": len(input_rows),
            "unique_queue_ids": len(queue_id_counts),
            "missing_queue_ids": missing_queue_ids,
            "unexpected_queue_ids": unexpected_queue_ids,
            "duplicate_queue_ids": duplicate_queue_ids,
            "input_binding_failures": input_binding_failures,
            "all_originals_dispositioned": full_queue_dispositioned,
        },
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
        "execution_contract": execution_contract_value,
        "executable_evidence_reuse": {
            "requested": reuse_summary is not None,
            "eligible": (reuse_summary or {}).get("eligible", 0),
            "reused": (reuse_summary or {}).get("reused", 0),
            "executed": (reuse_summary or {}).get("executed", len(admitted) + len(rejected)),
            "ledger": reuse_ledger_binding,
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
    parser.add_argument("--reuse-admission-report", type=Path)
    parser.add_argument("--reuse-ledger", type=Path)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    plan = load_sealed(args.plan, "plan_sha256")
    if (
        plan.get("schema_version") != "ganesh-mini-capability-stratified-corpus-plan/v1"
        or plan.get("matrix", {}).get("cells") != 120
    ):
        raise ValueError("unsupported capability qualification plan")
    queue_by_id = load_queue(args.queue, args.queue_manifest, plan)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    contract = execution_contract(args.config, args.runtime_config)
    reuse_index: dict[str, dict[str, Any]] | None = None
    reuse_source: dict[str, Any] | None = None
    reuse_summary: dict[str, Any] | None = None
    if (args.reuse_admission_report is None) != (args.reuse_ledger is None):
        raise ValueError("reuse admission report and reuse ledger must be provided together")
    if args.reuse_admission_report is not None:
        reuse_index, reuse_source = load_execution_reuse(args.reuse_admission_report, contract)
        reuse_summary = {}
    admitted, rejected = admit_qualification(
        read_jsonl(args.input), plan, queue_by_id, config, args.runtime_config,
        verifier_workers=args.verifier_workers, record_workers=args.record_workers,
        reuse_index=reuse_index, reuse_contract=contract, reuse_ledger=reuse_summary,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(b"".join(canonical_json(row) + b"\n" for row in admitted))
    args.rejected_output.parent.mkdir(parents=True, exist_ok=True)
    args.rejected_output.write_text(json.dumps(rejected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    reuse_ledger_binding = None
    if reuse_summary is not None and reuse_source is not None and args.reuse_ledger is not None:
        write_reuse_ledger(args.reuse_ledger, reuse_source, reuse_summary, contract)
        reuse_ledger_binding = file_binding(args.reuse_ledger)
    queue_manifest = load_sealed(args.queue_manifest, "manifest_sha256")
    report = build_report(
        mode=args.mode, plan=plan, queue_manifest=queue_manifest,
        input_path=args.input, output_path=args.output, rejected_path=args.rejected_output,
        admitted=admitted, rejected=rejected,
        verifier_workers=args.verifier_workers, record_workers=args.record_workers,
        queue_by_id=queue_by_id,
        execution_contract_value=contract, reuse_summary=reuse_summary,
        reuse_ledger_binding=reuse_ledger_binding,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "accepted": len(admitted), "rejected": len(rejected), "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
