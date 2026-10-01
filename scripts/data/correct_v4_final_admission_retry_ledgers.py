#!/usr/bin/env python3
"""Recover omitted V4 retry ledgers from sealed pre-final candidate artifacts.

This is a narrow, post-run evidence correction.  It only amends terminal
``final_admission`` rejections whose exact pre-final ready artifact proves the
candidate, envelope evidence, phase-two input, and scheduler bindings.  It does
not execute candidate code or reinterpret a disposition.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.admit_expansion import canonical_json, read_jsonl
from scripts.data.admit_repair_delta import (
    AdmissionFailure,
    V4_ASSEMBLY_SCHEMA,
    V4_CONTRACT_ID,
    validate_assembly_artifact,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256


REPORT_SCHEMA = "ganesh-mini-v4-final-admission-retry-ledger-correction/v1"


def _file_binding(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "path": str(path), "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def _sealed(value: Any, field: str, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{where}: expected object")
    body = dict(value)
    claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{where}: invalid {field}")
    return value


def _candidate_evidence_path(root: Path, identifier: str) -> Path:
    if not identifier or Path(identifier).name != identifier:
        raise ValueError("candidate ID cannot safely name an evidence artifact")
    path = (root / f"{identifier}.evidence.json").resolve()
    if path.parent != root.resolve():
        raise ValueError("candidate evidence path escaped its directory")
    return path


def _validate_inventory(
    inventory: dict[str, Any], inventory_path: Path,
    terminal_path: Path, terminal_rows: list[dict[str, Any]],
) -> None:
    _sealed(inventory, "report_sha256", str(inventory_path))
    binding = inventory.get("terminal_artifacts")
    expected_hashes = {
        row.get("candidate_id"): row.get("artifact_sha256") for row in terminal_rows
    }
    if (
        inventory.get("schema_version")
        != "ganesh-mini-repair-delta-two-phase-campaign/v1"
        or inventory.get("contract_id") != V4_CONTRACT_ID
        or inventory.get("generated") != 60
        or inventory.get("evaluation_artifacts_read_outside_separation") != 0
        or not isinstance(binding, dict)
        or binding != {**_file_binding(terminal_path), "records": len(terminal_rows)}
        or len(expected_hashes) != len(terminal_rows)
        or inventory.get("artifact_sha256s") != expected_hashes
    ):
        raise ValueError("two-phase inventory does not bind the sealed terminal cohort")


def _recover_one(
    original: dict[str, Any], candidate_evidence_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    identifier = original["candidate_id"]
    source_path = _candidate_evidence_path(candidate_evidence_dir, identifier)
    if not source_path.is_file():
        raise ValueError(f"{identifier}: sealed pre-final candidate evidence is missing")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    disposition, envelope, _ = validate_assembly_artifact(source, V4_CONTRACT_ID)
    if disposition != "ready" or not isinstance(envelope, dict):
        raise ValueError(f"{identifier}: pre-final candidate evidence is not ready")
    candidate = envelope.get("candidate")
    assignment = envelope.get("assignment")
    source_evidence = envelope.get("evidence")
    executable = source_evidence.get("executable") if isinstance(source_evidence, dict) else None
    ledger = source.get("retry_ledger")
    if (
        not isinstance(candidate, dict) or candidate.get("id") != identifier
        or not isinstance(assignment, dict)
        or assignment.get("cell_id") != original.get("cell_id")
        or original.get("input_sha256") != source.get("input_sha256")
        or original.get("phase2_input_sha256") != source.get("phase2_input_sha256")
        or original.get("verifier_scheduler") != source.get("verifier_scheduler")
        or original.get("evidence") != source_evidence
        or not isinstance(executable, dict) or not isinstance(ledger, dict)
        or executable.get("candidate_sha256") != canonical_sha256(candidate)
        or executable.get("retry_ledger_sha256") != ledger.get("ledger_sha256")
    ):
        raise ValueError(f"{identifier}: final rejection differs from sealed pre-final evidence")

    corrected = copy.deepcopy(original)
    corrected["evidence"]["retry_ledger"] = copy.deepcopy(ledger)
    corrected.pop("artifact_sha256")
    corrected["artifact_sha256"] = canonical_sha256(corrected)
    validate_assembly_artifact(corrected, V4_CONTRACT_ID)
    return corrected, {
        "candidate_id": identifier,
        "original_artifact_sha256": original["artifact_sha256"],
        "corrected_artifact_sha256": corrected["artifact_sha256"],
        "retry_ledger_sha256": ledger["ledger_sha256"],
        "candidate_evidence": {
            **_file_binding(source_path),
            "artifact_sha256": source["artifact_sha256"],
        },
    }


def correct_terminal_artifacts(
    terminal_path: Path, inventory_path: Path, candidate_evidence_dir: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    original = read_jsonl(terminal_path)
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    _validate_inventory(inventory, inventory_path, terminal_path, original)
    if len(original) != 60:
        raise ValueError("retry-ledger correction requires the complete 60-record terminal cohort")

    corrected: list[dict[str, Any]] = []
    amendments: list[dict[str, Any]] = []
    for row in original:
        validate_assembly_artifact(row, V4_CONTRACT_ID)
        amend = row.get("status") == "terminal-rejected" and row.get("terminal_stage") == "final_admission"
        if not amend:
            corrected.append(copy.deepcopy(row))
            continue
        if "retry_ledger" in row.get("evidence", {}):
            raise ValueError(f"{row.get('candidate_id')}: final rejection already contains a retry ledger")
        replacement, amendment = _recover_one(row, candidate_evidence_dir)
        corrected.append(replacement)
        amendments.append(amendment)

    if not amendments:
        raise ValueError("terminal cohort contains no correctable final-admission rejection")
    if [row["candidate_id"] for row in corrected] != [row["candidate_id"] for row in original]:
        raise AssertionError("correction changed terminal cohort order")
    amended_ids = {row["candidate_id"] for row in amendments}
    for before, after in zip(original, corrected, strict=True):
        if before["candidate_id"] not in amended_ids and before != after:
            raise AssertionError("correction changed a non-target terminal artifact")
        validate_assembly_artifact(after, V4_CONTRACT_ID)

    report = {
        "schema_version": REPORT_SCHEMA,
        "contract_id": V4_CONTRACT_ID,
        "input_terminal_artifacts": _file_binding(terminal_path),
        "input_two_phase_inventory": {
            **_file_binding(inventory_path),
            "report_sha256": inventory["report_sha256"],
        },
        "candidate_evidence_directory": str(candidate_evidence_dir),
        "records": len(corrected),
        "amended": len(amendments),
        "amended_candidate_ids": [row["candidate_id"] for row in amendments],
        "amendments": amendments,
        "preserved_order": True,
        "non_target_rows_unchanged": True,
        "evaluation_artifacts_read": 0,
    }
    return corrected, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terminal-artifacts", type=Path, required=True)
    parser.add_argument("--two-phase-inventory", type=Path, required=True)
    parser.add_argument("--candidate-evidence-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output.resolve() == args.terminal_artifacts.resolve():
        parser.error("--output must preserve the original terminal artifacts")
    if args.output.exists() or args.report.exists():
        parser.error("correction output and report must not already exist")

    corrected, report = correct_terminal_artifacts(
        args.terminal_artifacts, args.two_phase_inventory, args.candidate_evidence_dir,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = b"".join(canonical_json(row) + b"\n" for row in corrected)
    args.output.write_bytes(payload)
    report["output_terminal_artifacts"] = {
        "path": str(args.output), "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(), "records": len(corrected),
    }
    report["report_sha256"] = canonical_sha256(report)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "corrected", "records": len(corrected),
        "amended": report["amended"], "report_sha256": report["report_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
