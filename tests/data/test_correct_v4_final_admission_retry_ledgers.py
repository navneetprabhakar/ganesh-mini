from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.admit_expansion import canonical_json
from scripts.data.admit_repair_delta import (
    AdmissionFailure, V4_ASSEMBLY_SCHEMA, V4_CONTRACT_ID, validate_assembly_artifact,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.correct_v4_final_admission_retry_ledgers import (
    REPORT_SCHEMA, correct_terminal_artifacts, main,
)
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import SANDBOX_CONTRACT


def seal(value: dict, field: str) -> dict:
    value[field] = canonical_sha256(value)
    return value


def assert_sealed(value: dict, field: str) -> None:
    body = dict(value)
    claimed = body.pop(field)
    assert claimed == canonical_sha256(body)


def attempt_binding(code: str, role: str) -> dict:
    files = [{"path": "test_solution.py", "sha256": sha256_text(role)}]
    value = {
        "schema_version": "ganesh-mini-repair-delta-execution-input/v1",
        "implementation_sha256": sha256_text(code),
        "staged_files": files, "staged_files_sha256": canonical_sha256(files),
        "staging_sha256": sha256_text(f"staging:{role}"),
        "runtime_config_sha256": "1" * 64, "runtime_id": "python-locked",
        "limits_sha256": "2" * 64,
        "image": "python@sha256:" + "3" * 64,
        "image_id": "sha256:" + "4" * 64,
        "manifest_digest": "sha256:" + "3" * 64,
        "commands": [["python", "test_solution.py"]],
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
    }
    return seal(value, "binding_sha256")


def ready_source(identifier: str) -> dict:
    candidate = {"id": identifier}
    bindings = {implementation: {
        role: attempt_binding(code, role)
        for role in ("primary_discrimination", "cross_cutting")
    } for implementation, code in (("reference", "good"), ("known_bad", "bad"))}
    attempts = []
    for implementation in ("reference", "known_bad"):
        for role in ("primary_discrimination", "cross_cutting"):
            binding = bindings[implementation][role]
            attempts.append({
                "implementation": implementation, "role": role,
                "attempts": [{
                    "attempt": 1, "classification": None,
                    "input_binding": deepcopy(binding),
                    "result": {
                        "runtime_id": binding["runtime_id"], "image": binding["image"],
                        "image_id": binding["image_id"],
                        "manifest_digest": binding["manifest_digest"],
                        "limits_sha256": binding["limits_sha256"],
                        "commands": deepcopy(binding["commands"]),
                        "sandbox_contract_sha256": binding["sandbox_contract_sha256"],
                        "staging": {"staging_sha256": binding["staging_sha256"]},
                        "timed_out": False, "exit_codes": [0],
                    },
                }],
            })
    ledger = seal({
        "schema_version": "ganesh-mini-repair-delta-retry-ledger/v1",
        "candidate_sha256": canonical_sha256(candidate), "maximum_attempts": 2,
        "attempts": attempts, "unresolved": False, "evaluation_artifacts_read": 0,
    }, "ledger_sha256")
    executable = seal({
        "candidate_sha256": canonical_sha256(candidate),
        "retry_ledger_sha256": ledger["ledger_sha256"],
        "attempt_bindings": bindings,
    }, "evidence_sha256")
    value = {
        "schema_version": V4_ASSEMBLY_SCHEMA, "status": "ready-for-admission",
        "input_sha256": "5" * 64, "candidate_id": identifier,
        "phase2_input_sha256": "6" * 64,
        "verifier_scheduler": {"contract_sha256": "7" * 64},
        "envelope": {
            "candidate": candidate, "assignment": {"cell_id": "cap/python/repair"},
            "evidence": {"executable": executable},
        },
        "retry_ledger": ledger, "evaluation_artifacts_read": 0,
    }
    return seal(value, "artifact_sha256")


def terminal_final(source: dict) -> dict:
    value = {
        "schema_version": V4_ASSEMBLY_SCHEMA, "status": "terminal-rejected",
        "input_sha256": source["input_sha256"], "candidate_id": source["candidate_id"],
        "cell_id": source["envelope"]["assignment"]["cell_id"],
        "terminal_stage": "final_admission", "reason": "fixture final rejection",
        "evidence": deepcopy(source["envelope"]["evidence"]),
        "phase2_input_sha256": source["phase2_input_sha256"],
        "verifier_scheduler": deepcopy(source["verifier_scheduler"]),
        "evaluation_artifacts_read": 0,
    }
    return seal(value, "artifact_sha256")


def ordinary_terminal(identifier: str) -> dict:
    evidence = seal({"candidate_sha256": "8" * 64}, "evidence_sha256")
    value = {
        "schema_version": V4_ASSEMBLY_SCHEMA, "status": "terminal-rejected",
        "input_sha256": "9" * 64, "candidate_id": identifier,
        "cell_id": f"cap/{identifier}/repair", "terminal_stage": "semantic_review",
        "reason": "fixture rejection", "evidence": {"semantic_review": evidence},
        "evaluation_artifacts_read": 0,
    }
    return seal(value, "artifact_sha256")


def fixture(tmp_path: Path) -> tuple[Path, Path, Path, list[dict], dict]:
    source = ready_source("candidate-00")
    evidence_dir = tmp_path / "candidate-evidence"
    evidence_dir.mkdir()
    source_path = evidence_dir / "candidate-00.evidence.json"
    source_path.write_text(json.dumps(source))
    terminal = [terminal_final(source)] + [ordinary_terminal(f"candidate-{index:02d}") for index in range(1, 60)]
    terminal_path = tmp_path / "terminal-artifacts.jsonl"
    terminal_path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in terminal))
    inventory = {
        "schema_version": "ganesh-mini-repair-delta-two-phase-campaign/v1",
        "contract_id": V4_CONTRACT_ID, "generated": 60,
        "evaluation_artifacts_read_outside_separation": 0,
        "terminal_artifacts": {
            "path": str(terminal_path), "bytes": terminal_path.stat().st_size,
            "sha256": hashlib.sha256(terminal_path.read_bytes()).hexdigest(), "records": 60,
        },
        "artifact_sha256s": {row["candidate_id"]: row["artifact_sha256"] for row in terminal},
    }
    seal(inventory, "report_sha256")
    inventory_path = tmp_path / "two-phase-inventory.json"
    inventory_path.write_text(json.dumps(inventory))
    return terminal_path, inventory_path, evidence_dir, terminal, source


def test_corrects_only_final_admission_reject_and_preserves_order(tmp_path: Path) -> None:
    terminal_path, inventory_path, evidence_dir, original, source = fixture(tmp_path)
    corrected, report = correct_terminal_artifacts(terminal_path, inventory_path, evidence_dir)

    assert [row["candidate_id"] for row in corrected] == [row["candidate_id"] for row in original]
    assert corrected[1:] == original[1:]
    assert corrected[0]["evidence"]["retry_ledger"] == source["retry_ledger"]
    assert report["schema_version"] == REPORT_SCHEMA
    assert report["amended_candidate_ids"] == ["candidate-00"]
    validate_assembly_artifact(corrected[0], V4_CONTRACT_ID)


@pytest.mark.parametrize("field", ["phase2_input_sha256", "verifier_scheduler", "evidence"])
def test_fails_closed_on_pre_final_binding_drift(tmp_path: Path, field: str) -> None:
    terminal_path, inventory_path, evidence_dir, _, source = fixture(tmp_path)
    if field == "evidence":
        source["envelope"]["evidence"] = {}
    else:
        source[field] = "drift"
    source.pop("artifact_sha256")
    source["artifact_sha256"] = canonical_sha256(source)
    (evidence_dir / "candidate-00.evidence.json").write_text(json.dumps(source))

    with pytest.raises((ValueError, AdmissionFailure)):
        correct_terminal_artifacts(terminal_path, inventory_path, evidence_dir)


def test_cli_emits_sealed_report_bound_to_corrected_output(tmp_path: Path) -> None:
    terminal_path, inventory_path, evidence_dir, _, _ = fixture(tmp_path)
    output = tmp_path / "terminal-artifacts-corrected.jsonl"
    report_path = tmp_path / "correction-report.json"

    assert main([
        "--terminal-artifacts", str(terminal_path),
        "--two-phase-inventory", str(inventory_path),
        "--candidate-evidence-dir", str(evidence_dir),
        "--output", str(output), "--report", str(report_path),
    ]) == 0
    report = json.loads(report_path.read_text())
    assert_sealed(report, "report_sha256")
    assert report["output_terminal_artifacts"] == {
        "path": str(output), "bytes": output.stat().st_size,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "records": 60,
    }
    assert len(output.read_text().splitlines()) == 60
