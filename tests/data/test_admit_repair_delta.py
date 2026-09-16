from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.admit_repair_delta import admit, suite_sha256, teacher_candidate_sha256, validate_envelope
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import SANDBOX_CONTRACT


SEPARATION_CONTRACT = "9" * 64


def seal(value: dict) -> dict:
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def admission_config() -> dict:
    return {
        "allowed_licenses": ["MIT"],
        "required_rights": ["prompt", "answer", "tests", "redistribution", "model_training"],
        "allowed_test_origins": ["independent_author"],
        "sources": {"fixture": {"revision": "r1", "license": "MIT"}},
    }


def candidate() -> dict:
    prompt = "Repair compute_total so it sums signed integers and rejects malformed input. Return only source."
    reference = "def compute_total(values):\n    return sum(values)\n"
    bad = "def compute_total(values):\n    return max(values)\n"
    primary_test = "from solution import compute_total\nassert compute_total([2,3]) == 5\nassert compute_total([-2,3]) == 1\n"
    cross_test = "from solution import compute_total\ntry:\n compute_total(None)\nexcept (TypeError, ValueError):\n pass\n"
    files = [
        {"path": "test_primary.py", "role": "test", "content": primary_test, "sha256": sha256_text(primary_test)},
        {"path": "test_cross.py", "role": "test", "content": cross_test, "sha256": sha256_text(cross_test)},
    ]
    task = {
        "schema_version": "1.0", "task_id": "repair-0", "surface": "training_admission",
        "language": "python", "family": "python", "task_type": "repair",
        "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "candidate_path": "solution.py", "files": files, "runtime_id": "python-locked",
        "limits": {"timeout_seconds": 30, "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536},
        "validation": {
            "reference": {"label": "reference", "code": reference, "sha256": sha256_text(reference)},
            "known_bad": [{"label": "uses maximum instead of aggregation", "code": bad, "sha256": sha256_text(bad)}],
        },
    }
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1", "id": "repair-0",
        "lane": "python", "task_type": "repair",
        "messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": reference}],
        "source": {
            "dataset": "fixture", "uri": "https://example.invalid/source", "revision": "r1",
            "record_id": "source-0", "license": "MIT", "license_uri": "https://example.invalid/license",
            "source_record_sha256": "a" * 64, "transformation": "repair-delta construction",
        },
        "rights": {name: True for name in ("prompt", "answer", "tests", "redistribution", "model_training")},
        "verification_task": task, "test_origin": "independent_author",
    }


def runtime_file(tmp_path: Path) -> tuple[Path, dict]:
    runtime = {
        "language": "python", "image": "python-fixture:locked",
        "image_id": "sha256:" + "1" * 64, "manifest_digest": "sha256:" + "2" * 64,
        "rootfs_layers": ["sha256:" + "3" * 64], "platform": "linux/amd64",
        "candidate_path": "solution.py", "commands": [["python", "test_primary.py"]],
    }
    path = tmp_path / "runtimes.json"
    path.write_text(json.dumps({"schema_version": "3.0", "platform": "linux/amd64", "runtimes": {"python-locked": runtime}}))
    return path, runtime


def envelope(tmp_path: Path) -> tuple[dict, Path]:
    item = candidate()
    runtime_path, runtime = runtime_file(tmp_path)
    candidate_sha = canonical_sha256(item)
    task = item["verification_task"]
    specification_sha = sha256_text(item["messages"][0]["content"])
    reference_sha = task["validation"]["reference"]["sha256"]
    known_bad_sha = task["validation"]["known_bad"][0]["sha256"]
    proof = seal({
        "candidate_id": item["id"], "teacher_candidate_sha256": teacher_candidate_sha256(item),
        "primary_capability": "numeric_reasoning", "assigned_cross_cutting_dimension": "malformed_input",
        "capability_operation": "sum all signed integer elements",
        "defective_intermediate_or_decision": "selects a maximum instead of accumulating",
        "valid_domain_counterexample": "[2, 3] must produce 5, not 3",
        "minimal_capability_specific_patch": "replace maximum selection with addition",
        "scheduled_dimension_obligation": "reject a non-iterable malformed input",
        "known_bad_already_satisfies_scheduled_dimension": True,
        "cross_dimension_only_patch_cannot_solve": True,
        "capability_remains_substantive_without_cross_clause": True,
    })
    semantic = seal({
        "candidate_sha256": candidate_sha, "specification_sha256": specification_sha,
        "known_bad_sha256": known_bad_sha, "primary_capability": "numeric_reasoning",
        "assigned_cross_cutting_dimension": "malformed_input",
        "repair_delta_requires_primary_capability": True,
        "scheduled_dimension_is_concrete_and_secondary": True,
        "known_bad_already_satisfies_scheduled_dimension": True,
        "cross_dimension_only_patch_cannot_solve": True,
        "capability_remains_substantive_without_cross_clause": True,
        "generic_boilerplate_is_not_primary": True,
        "visibility": {
            "specification_visible": True, "embedded_known_bad_visible": True,
            "assigned_labels_visible": True, "teacher_proof_visible": False,
            "reference_visible": False, "tests_visible": False, "verifier_outputs_visible": False,
            "training_stimulus_visible": False, "source_dataset_visible": False,
            "v2_outcomes_visible": False, "evaluation_artifacts_read": 0,
        },
    })
    roles = [
        {"path": "test_primary.py", "file_sha256": task["files"][0]["sha256"],
         "role": "primary_discrimination", "case_ids": ["positive", "signed"],
         "valid_domain_only": True, "scheduled_dimension_only": False},
        {"path": "test_cross.py", "file_sha256": task["files"][1]["sha256"],
         "role": "cross_cutting", "case_ids": ["malformed-none"],
         "valid_domain_only": False, "scheduled_dimension_only": True},
    ]
    test_author = seal({
        "candidate_sha256": candidate_sha, "specification_sha256": specification_sha,
        "known_bad_sha256": known_bad_sha, "test_roles": roles,
        "primary_capability": "numeric_reasoning", "assigned_cross_cutting_dimension": "malformed_input",
        "visibility": {
            "specification_visible": True, "embedded_known_bad_visible": True,
            "capability_definition_visible": True, "scheduled_dimension_visible": True,
            "reference_visible": False, "teacher_proof_visible": False,
            "semantic_review_visible": False, "verifier_outputs_visible": False,
            "evaluation_artifacts_read": 0,
        },
    })
    delta = seal({
        "candidate_sha256": candidate_sha, "specification_sha256": specification_sha,
        "reference_sha256": reference_sha, "known_bad_sha256": known_bad_sha,
        "primary_capability": "numeric_reasoning", "assigned_cross_cutting_dimension": "malformed_input",
        "independent_semantic_delta_count": 1, "delta_is_capability_specific": True,
        "introduces_multiple_independent_fixes": False,
        "delta_description": "maximum selection is replaced by signed accumulation",
        "visibility": {
            "specification_visible": True, "embedded_known_bad_visible": True,
            "reference_visible": True, "assigned_labels_visible": True,
            "tests_visible": False, "verifier_outputs_visible": False,
            "teacher_proof_visible": False, "training_stimulus_visible": False,
            "v2_outcomes_visible": False, "evaluation_artifacts_read": 0,
        },
    })
    separation = seal({
        "candidate_sha256": candidate_sha, "comparison_contract_sha256": SEPARATION_CONTRACT,
        "comparison_manifest_sha256": "8" * 64,
        "exact_training_passed": True, "normalized_training_passed": True, "fuzzy_training_passed": True,
        "exact_evaluation_passed": True, "normalized_evaluation_passed": True, "fuzzy_evaluation_passed": True,
        "evaluation_artifacts_read_by_construction": 0,
    })
    limits_sha = canonical_sha256(task["limits"])
    image = f"python-fixture@{runtime['manifest_digest']}"
    def result(role: str, passed: bool) -> dict:
        return {
            "suite_sha256": suite_sha256(item, [row for row in roles if row["role"] == role]),
            "runtime_id": task["runtime_id"], "image": image, "image_id": runtime["image_id"],
            "manifest_digest": runtime["manifest_digest"],
            "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
            "limits_sha256": limits_sha, "timed_out": False, "exit_codes": [0 if passed else 1],
        }
    executable = seal({
        "candidate_sha256": candidate_sha,
        "runtime_config_sha256": hashlib.sha256(runtime_path.read_bytes()).hexdigest(),
        "reference_sha256": reference_sha, "known_bad_sha256": known_bad_sha,
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        "results": {
            "reference": {
                "primary_discrimination": result("primary_discrimination", True),
                "cross_cutting": result("cross_cutting", True),
            },
            "known_bad": {
                "primary_discrimination": result("primary_discrimination", False),
                "cross_cutting": result("cross_cutting", True),
            },
        },
    })
    lineage = seal({
        "candidate_sha256": candidate_sha,
        "contract_id": "capability-stratified-v3-repair-delta/v1",
        "cell_id": "numeric_reasoning/python/repair",
        "source_identity": {"dataset": "fixture", "revision": "r1", "record_id": "source-0"},
        "source_record_sha256": "a" * 64, "complete": True,
        "teacher_proof_evidence_sha256": proof["evidence_sha256"],
        "semantic_review_evidence_sha256": semantic["evidence_sha256"],
        "test_author_evidence_sha256": test_author["evidence_sha256"],
        "delta_audit_evidence_sha256": delta["evidence_sha256"],
        "separation_evidence_sha256": separation["evidence_sha256"],
        "executable_evidence_sha256": executable["evidence_sha256"],
    })
    return {
        "schema_version": "ganesh-mini-repair-delta-envelope/v1", "candidate": item,
        "assignment": {
            "contract_id": "capability-stratified-v3-repair-delta/v1",
            "cell_id": "numeric_reasoning/python/repair", "primary_capability": "numeric_reasoning",
            "assigned_cross_cutting_dimension": "malformed_input",
        },
        "evidence": {
            "teacher_proof": proof, "semantic_review": semantic, "test_author": test_author,
            "delta_audit": delta, "separation": separation, "executable": executable, "lineage": lineage,
        },
    }, runtime_path


def reseal_evidence(value: dict, name: str) -> None:
    evidence = value["evidence"][name]
    evidence.pop("evidence_sha256")
    seal(evidence)


def retry_ledger(candidate_sha: str, unresolved: bool) -> dict:
    rows = []
    for implementation in ("reference", "known_bad"):
        for role in ("primary_discrimination", "cross_cutting"):
            attempts = [{"attempt": 1, "classification": None, "result": {"exit_codes": [0]}}]
            if unresolved and implementation == "reference" and role == "primary_discrimination":
                attempts = [
                    {"attempt": 1, "classification": "timeout", "result": {"timed_out": True}},
                    {"attempt": 2, "classification": "timeout", "result": {"timed_out": True}},
                ]
            rows.append({"implementation": implementation, "role": role, "attempts": attempts})
    value = {
        "schema_version": "ganesh-mini-repair-delta-retry-ledger/v1",
        "candidate_sha256": candidate_sha, "maximum_attempts": 2,
        "attempts": rows, "unresolved": unresolved, "evaluation_artifacts_read": 0,
    }
    value["ledger_sha256"] = canonical_sha256(value)
    return value


def ready_artifact(value: dict) -> dict:
    candidate_sha = canonical_sha256(value["candidate"])
    ledger = retry_ledger(candidate_sha, False)
    executable = value["evidence"]["executable"]
    executable["retry_ledger_sha256"] = ledger["ledger_sha256"]
    reseal_evidence(value, "executable")
    value["evidence"]["lineage"]["executable_evidence_sha256"] = executable["evidence_sha256"]
    reseal_evidence(value, "lineage")
    artifact = {
        "schema_version": "ganesh-mini-repair-delta-evidence-assembly/v1",
        "status": "ready-for-admission", "input_sha256": "5" * 64,
        "candidate_id": value["candidate"]["id"], "envelope": value,
        "retry_ledger": ledger, "evaluation_artifacts_read": 0,
    }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    return artifact


def unresolved_artifact(value: dict) -> dict:
    candidate_sha = canonical_sha256(value["candidate"])
    ledger = retry_ledger(candidate_sha, True)
    executable = seal({
        "candidate_sha256": candidate_sha, "retry_ledger_sha256": ledger["ledger_sha256"],
    })
    artifact = {
        "schema_version": "ganesh-mini-repair-delta-evidence-assembly/v1",
        "status": "unresolved", "input_sha256": "6" * 64,
        "candidate_id": value["candidate"]["id"],
        "cell_id": value["assignment"]["cell_id"], "terminal_stage": "executable",
        "reason": "unresolved infrastructure after one identical replay",
        "evidence": {"executable": executable, "retry_ledger": ledger},
        "evaluation_artifacts_read": 0,
    }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    return artifact


def test_accepts_exact_repair_delta_contract(tmp_path: Path) -> None:
    value, runtime_path = envelope(tmp_path)
    admitted = validate_envelope(value, admission_config(), runtime_path, SEPARATION_CONTRACT)
    assert admitted["cell_id"] == "numeric_reasoning/python/repair"
    assert len(admitted["proof_consistency_sha256"]) == 64
    output, rejected = admit([value], admission_config(), runtime_path, SEPARATION_CONTRACT)
    assert len(output) == 1 and rejected == []


def test_admits_ready_assembly_and_keeps_timeout_unresolved(tmp_path: Path) -> None:
    value, runtime_path = envelope(tmp_path)
    ready = ready_artifact(deepcopy(value))
    unresolved_value = deepcopy(value)
    unresolved_value["candidate"]["id"] = "repair-timeout"
    unresolved = unresolved_artifact(unresolved_value)
    unresolved_rows: list[dict] = []

    output, rejected = admit(
        [ready, unresolved], admission_config(), runtime_path, SEPARATION_CONTRACT,
        unresolved_rows,
    )

    assert [row["id"] for row in output] == ["repair-0"]
    assert rejected == []
    assert unresolved_rows == [{
        "line": 2, "id": "repair-timeout", "cell_id": "numeric_reasoning/python/repair",
        "terminal_stage": "executable",
        "reason": "unresolved infrastructure after one identical replay",
    }]


def test_retry_ledger_must_bind_candidate_and_executable(tmp_path: Path) -> None:
    value, runtime_path = envelope(tmp_path)
    artifact = ready_artifact(value)
    artifact["retry_ledger"]["candidate_sha256"] = "0" * 64
    artifact["retry_ledger"].pop("ledger_sha256")
    artifact["retry_ledger"]["ledger_sha256"] = canonical_sha256(artifact["retry_ledger"])
    artifact.pop("artifact_sha256")
    artifact["artifact_sha256"] = canonical_sha256(artifact)

    output, rejected = admit([artifact], admission_config(), runtime_path, SEPARATION_CONTRACT)

    assert output == []
    assert "retry ledger" in rejected[0]["reason"]


@pytest.mark.parametrize(
    ("mutate", "reason"),
    [
        (lambda value: value["evidence"]["semantic_review"]["visibility"].update(teacher_proof_visible=True), "visibility"),
        (lambda value: value["evidence"]["semantic_review"].update(cross_dimension_only_patch_cannot_solve=False), "independently pass"),
        (lambda value: value["evidence"]["teacher_proof"].update(cross_dimension_only_patch_cannot_solve=False), "proof-consistency"),
        (lambda value: value["evidence"]["test_author"]["test_roles"][0].update(case_ids=["only-one"]), "at least two"),
        (lambda value: value["evidence"]["delta_audit"].update(independent_semantic_delta_count=2), "exactly one"),
        (lambda value: value["evidence"]["executable"]["results"]["known_bad"]["cross_cutting"].update(exit_codes=[1]), "must pass"),
        (lambda value: value["evidence"]["separation"].update(fuzzy_evaluation_passed=False), "separation"),
    ],
)
def test_fails_closed_on_blinding_proof_roles_delta_execution_and_separation(tmp_path: Path, mutate, reason: str) -> None:
    value, runtime_path = envelope(tmp_path)
    mutate(value)
    # Identify and reseal the first evidence object whose seal changed.
    for name, evidence in value["evidence"].items():
        body = dict(evidence); claimed = body.pop("evidence_sha256")
        if claimed != canonical_sha256(body):
            reseal_evidence(value, name)
            break
    with pytest.raises(ValueError, match=reason):
        validate_envelope(value, admission_config(), runtime_path, SEPARATION_CONTRACT)


def test_rejects_timeout_and_runtime_or_lineage_drift(tmp_path: Path) -> None:
    value, runtime_path = envelope(tmp_path)
    value["evidence"]["executable"]["results"]["reference"]["primary_discrimination"]["timed_out"] = True
    reseal_evidence(value, "executable")
    with pytest.raises(ValueError, match="unresolved verifier infrastructure evidence"):
        validate_envelope(value, admission_config(), runtime_path, SEPARATION_CONTRACT)
    unresolved: list[dict] = []
    admitted, rejected = admit(
        [value], admission_config(), runtime_path, SEPARATION_CONTRACT, unresolved,
    )
    assert admitted == [] and rejected == []
    assert unresolved[0]["id"] == "repair-0"
    assert "unresolved verifier infrastructure" in unresolved[0]["reason"]

    value, runtime_path = envelope(tmp_path)
    runtime_document = json.loads(runtime_path.read_text())
    runtime_document["runtimes"]["python-locked"]["manifest_digest"] = "sha256:" + "4" * 64
    runtime_path.write_text(json.dumps(runtime_document))
    with pytest.raises(ValueError, match="unchanged runtime"):
        validate_envelope(value, admission_config(), runtime_path, SEPARATION_CONTRACT)

    value, runtime_path = envelope(tmp_path)
    value["evidence"]["lineage"]["source_record_sha256"] = "b" * 64
    reseal_evidence(value, "lineage")
    with pytest.raises(ValueError, match="lineage"):
        validate_envelope(value, admission_config(), runtime_path, SEPARATION_CONTRACT)


def test_candidate_or_suite_hash_drift_is_rejected(tmp_path: Path) -> None:
    value, runtime_path = envelope(tmp_path)
    drifted = deepcopy(value)
    drifted["candidate"]["verification_task"]["files"][0]["content"] += "# changed\n"
    with pytest.raises(ValueError, match="content hash mismatch"):
        validate_envelope(drifted, admission_config(), runtime_path, SEPARATION_CONTRACT)

    value["evidence"]["executable"]["results"]["reference"]["primary_discrimination"]["suite_sha256"] = "0" * 64
    reseal_evidence(value, "executable")
    with pytest.raises(ValueError, match="binding mismatch"):
        validate_envelope(value, admission_config(), runtime_path, SEPARATION_CONTRACT)
