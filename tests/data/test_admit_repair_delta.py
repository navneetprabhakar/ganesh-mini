from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.admit_repair_delta import (
    AdmissionFailure, V4_ASSEMBLY_SCHEMA, V4_CONTRACT_ID, V4_ENVELOPE_SCHEMA,
    admit, execution_attempt_binding, load_v4_primary_cohort_binding, staging_contract,
    teacher_candidate_sha256, validate_assembly_artifact, validate_envelope, validate_retry_ledger,
    validate_v4_terminal_accounting,
)
from scripts.data.admit_expansion import canonical_json, validate_candidate
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v4_preflight import (
    PROOF_SCHEMA as V4_PROOF_SCHEMA,
    WITNESS_SCHEMA as V4_WITNESS_SCHEMA,
    build_post_teacher_preflight_evidence,
    load_preflight_config,
)
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import SANDBOX_CONTRACT


SEPARATION_CONTRACT = "9" * 64
V4_PREFLIGHT_CONFIG = Path(__file__).resolve().parents[2] / "configs/data/gate2_v4_post_teacher_preflight.json"


def seal(value: dict) -> dict:
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def v4_primary_cohort_binding(tmp_path: Path) -> dict:
    rows = []
    for index in range(120):
        primary = index < 60
        rows.append({
            "id": f"v4-{index}",
            "role": "primary" if primary else "reserve",
            "cohort": "first_pass" if primary else "reserve",
            "generation_eligible": primary,
            "contract_id": V4_CONTRACT_ID,
        })
    queue_path = tmp_path / "queue.jsonl"
    queue_path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))
    manifest = {
        "schema_version": "ganesh-mini-repair-delta-v4-queue-manifest/v1",
        "contract_version": "v4", "contract_id": V4_CONTRACT_ID,
        "queue_sha256": hashlib.sha256(queue_path.read_bytes()).hexdigest(),
        "assignments": 120, "primary_assignments": 60,
        "initial_generation_eligible": 60,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_path = tmp_path / "queue-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return load_v4_primary_cohort_binding(queue_path, manifest_path, "primary")


def test_v4_terminal_accounting_binds_exact_ordered_60_primary_cohort(tmp_path: Path) -> None:
    binding = v4_primary_cohort_binding(tmp_path)
    rows = [{
        "schema_version": V4_ASSEMBLY_SCHEMA,
        "candidate_id": identifier,
        "status": "terminal-rejected" if index % 3 == 0 else (
            "unresolved" if index % 3 == 1 else "ready-for-admission"
        ),
    } for index, identifier in enumerate(binding["ordered_primary_candidate_ids"])]
    validate_v4_terminal_accounting(rows, binding)

    with pytest.raises(AdmissionFailure, match="exact 60-primary"):
        validate_v4_terminal_accounting(rows[:-1], binding)
    reordered = deepcopy(rows)
    reordered[0], reordered[1] = reordered[1], reordered[0]
    with pytest.raises(AdmissionFailure, match="preserve primary cohort order"):
        validate_v4_terminal_accounting(reordered, binding)


def test_v4_primary_cohort_binding_rejects_reserve_final_admission(tmp_path: Path) -> None:
    binding = v4_primary_cohort_binding(tmp_path)
    assert binding["records"] == 60
    queue_path = tmp_path / "queue.jsonl"
    manifest_path = tmp_path / "queue-manifest.json"
    with pytest.raises(AdmissionFailure, match="requires the primary cohort"):
        load_v4_primary_cohort_binding(queue_path, manifest_path, "reserve")


def admission_config() -> dict:
    return {
        "allowed_licenses": ["MIT"],
        "required_rights": ["prompt", "answer", "tests", "redistribution", "model_training"],
        "allowed_test_origins": ["independent_author"],
        "sources": {"fixture": {"revision": "r1", "license": "MIT"}},
    }


def commitpack_source() -> dict:
    return {
        "dataset": "bigcode/commitpackft",
        "uri": "https://huggingface.co/datasets/bigcode/commitpackft",
        "revision": "fc56fe33c030c6daa414c2b112c932b8eed085e6",
        "record_id": "data/javascript/data.jsonl:line-00003647",
        "license": "MIT", "license_uri": "https://opensource.org/license/mit/",
        "source_record_sha256": "1" * 64,
        "transformation": "Native CommitPackFT repair stimulus; new_contents remains quarantined",
        "source_file": "data/javascript/data.jsonl",
        "source_file_sha256": "2" * 64, "source_file_bytes": 128001108,
        "raw_line_sha256": "3" * 64, "commit": "4" * 40,
        "old_file": "src/old.js", "new_file": "src/new.js",
        "repositories_raw": "owner/repo,fork/repo", "repositories": ["owner/repo", "fork/repo"],
        "subject_sha256": "5" * 64, "message_sha256": "6" * 64,
        "old_contents_sha256": "7" * 64,
    }


def commitpack_config() -> dict:
    value = admission_config()
    value["allowed_licenses"] = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0", "Unlicense"]
    value["sources"]["bigcode/commitpackft"] = {
        "revision": "fc56fe33c030c6daa414c2b112c932b8eed085e6",
        "uri": "https://huggingface.co/datasets/bigcode/commitpackft",
        "licenses": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0", "Unlicense"],
        "source_files": {
            "data/javascript/data.jsonl": {"bytes": 128001108, "sha256": "2" * 64},
            "data/typescript/data.jsonl": {"bytes": 14620423, "sha256": "8" * 64},
            "data/go/data.jsonl": {"bytes": 12417842, "sha256": "9" * 64},
            "data/python/data.jsonl": {"bytes": 135858935, "sha256": "a" * 64},
        },
    }
    return value


def commitpack_v4_native_source() -> dict:
    source = commitpack_source()
    source.update(
        record_id="data/python/data.jsonl:line-00003221",
        source_file="data/python/data.jsonl",
        source_file_sha256="a" * 64,
        source_file_bytes=135858935,
        old_file="lib/ratelimit.py",
        new_file="lib/ratelimit.py",
        quarantined_record_sha256="b" * 64,
        selection_rank=1,
    )
    return source


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
        "candidate_path": "solution.py", "commands": [["python", "test_solution.py"]],
    }
    companion_runtimes = {
        "go-fixture": {"language": "go", "candidate_path": "solution.go", "commands": [["go", "test", "./..."]]},
        "java-fixture": {"language": "java", "candidate_path": "Solution.java", "commands": [["javac", "Solution.java", "SolutionTest.java"], ["java", "SolutionTest"]]},
        "javascript-fixture": {"language": "javascript", "candidate_path": "solution.js", "commands": [["node", "solution.test.js"]]},
        "typescript-fixture": {"language": "typescript", "candidate_path": "solution.ts", "commands": [["node", "tsc", "solution.test.ts"], ["node", "solution.test.js"]]},
        "rust-fixture": {"language": "rust", "candidate_path": "solution.rs", "commands": [["rustc", "--test", "solution_test.rs"]]},
    }
    for value in companion_runtimes.values():
        value["platform"] = "linux/amd64"
    path = tmp_path / "runtimes.json"
    path.write_text(json.dumps({
        "schema_version": "3.0", "platform": "linux/amd64",
        "runtimes": {"python-locked": runtime, **companion_runtimes},
    }))
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
        {"path": "test_primary.py", "canonical_path": "test_solution.py", "file_sha256": task["files"][0]["sha256"],
         "role": "primary_discrimination", "case_ids": ["positive", "signed"],
         "valid_domain_only": True, "scheduled_dimension_only": False},
        {"path": "test_cross.py", "canonical_path": "test_solution.py", "file_sha256": task["files"][1]["sha256"],
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
        row = next(row for row in roles if row["role"] == role)
        staging = staging_contract(item, row, runtime)
        return {
            "staging": staging, "suite_sha256": staging["suite_sha256"],
            "runtime_id": task["runtime_id"], "image": image, "image_id": runtime["image_id"],
            "manifest_digest": runtime["manifest_digest"],
            "commands": runtime["commands"],
            "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
            "limits_sha256": limits_sha, "timed_out": False, "exit_codes": [0 if passed else 1],
        }
    runtime_config_sha = hashlib.sha256(runtime_path.read_bytes()).hexdigest()
    attempt_bindings = {
        implementation: {
            role: execution_attempt_binding(item, row, runtime, runtime_config_sha, code)
            for role, row in (
                ("primary_discrimination", roles[0]), ("cross_cutting", roles[1]),
            )
        }
        for implementation, code in (
            ("reference", task["validation"]["reference"]["code"]),
            ("known_bad", task["validation"]["known_bad"][0]["code"]),
        )
    }
    executable = seal({
        "candidate_sha256": candidate_sha,
        "runtime_config_sha256": runtime_config_sha,
        "reference_sha256": reference_sha, "known_bad_sha256": known_bad_sha,
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        "attempt_bindings": attempt_bindings,
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


def rebind_source(value: dict, source: dict) -> None:
    value["candidate"]["source"] = source
    candidate_sha = canonical_sha256(value["candidate"])
    for suites in value["evidence"]["executable"]["results"].values():
        for result in suites.values():
            staging = result["staging"]
            staging["candidate_sha256"] = candidate_sha
            staging.pop("suite_sha256"); staging.pop("staging_sha256")
            staging["suite_sha256"] = canonical_sha256(staging)
            staging["staging_sha256"] = canonical_sha256(staging)
            result["suite_sha256"] = staging["suite_sha256"]
    proof = value["evidence"]["teacher_proof"]
    proof["teacher_candidate_sha256"] = teacher_candidate_sha256(value["candidate"])
    proof.pop("evidence_sha256"); seal(proof)
    for name in ("semantic_review", "test_author", "delta_audit", "separation", "executable"):
        evidence = value["evidence"][name]
        evidence["candidate_sha256"] = candidate_sha
        evidence.pop("evidence_sha256"); seal(evidence)
    lineage = value["evidence"]["lineage"]
    lineage.update({
        "candidate_sha256": candidate_sha,
        "source_identity": {key: source[key] for key in ("dataset", "revision", "record_id")},
        "source_record_sha256": source["source_record_sha256"],
        "teacher_proof_evidence_sha256": proof["evidence_sha256"],
        "semantic_review_evidence_sha256": value["evidence"]["semantic_review"]["evidence_sha256"],
        "test_author_evidence_sha256": value["evidence"]["test_author"]["evidence_sha256"],
        "delta_audit_evidence_sha256": value["evidence"]["delta_audit"]["evidence_sha256"],
        "separation_evidence_sha256": value["evidence"]["separation"]["evidence_sha256"],
        "executable_evidence_sha256": value["evidence"]["executable"]["evidence_sha256"],
    })
    lineage.pop("evidence_sha256"); seal(lineage)


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


def test_v4_final_admission_rejection_preserves_and_validates_retry_ledger() -> None:
    candidate_sha = "a" * 64
    ledger = retry_ledger(candidate_sha, False)
    executable = seal({
        "candidate_sha256": candidate_sha,
        "retry_ledger_sha256": ledger["ledger_sha256"],
    })
    artifact = {
        "schema_version": V4_ASSEMBLY_SCHEMA,
        "status": "terminal-rejected",
        "input_sha256": "b" * 64,
        "candidate_id": "v4-final-reject",
        "cell_id": "numeric_reasoning/python/repair",
        "terminal_stage": "final_admission",
        "reason": "final validator rejected the ready envelope",
        "evidence": {"executable": executable, "retry_ledger": ledger},
        "evaluation_artifacts_read": 0,
    }
    artifact["artifact_sha256"] = canonical_sha256(artifact)

    disposition, envelope_value, summary = validate_assembly_artifact(
        artifact, V4_CONTRACT_ID,
    )

    assert disposition == "terminal-rejected"
    assert envelope_value is None
    assert summary["id"] == artifact["candidate_id"]


def test_accepts_exact_repair_delta_contract(tmp_path: Path) -> None:
    value, runtime_path = envelope(tmp_path)
    admitted = validate_envelope(value, admission_config(), runtime_path, SEPARATION_CONTRACT)
    assert admitted["cell_id"] == "numeric_reasoning/python/repair"
    assert len(admitted["proof_consistency_sha256"]) == 64
    output, rejected = admit([value], admission_config(), runtime_path, SEPARATION_CONTRACT)
    assert len(output) == 1 and rejected == []


def test_v4_retry_ledger_rejects_replay_input_drift(tmp_path: Path) -> None:
    value, _ = envelope(tmp_path)
    candidate_sha = canonical_sha256(value["candidate"])
    bindings = value["evidence"]["executable"]["attempt_bindings"]
    ledger = retry_ledger(candidate_sha, True)
    for row in ledger["attempts"]:
        binding = bindings[row["implementation"]][row["role"]]
        for run in row["attempts"]:
            run["input_binding"] = deepcopy(binding)
            run["result"].update({
                "runtime_id": binding["runtime_id"], "image": binding["image"],
                "image_id": binding["image_id"], "commands": deepcopy(binding["commands"]),
                "manifest_digest": binding["manifest_digest"],
                "limits_sha256": binding["limits_sha256"],
                "staging": {"staging_sha256": binding["staging_sha256"]},
                "sandbox_contract_sha256": binding["sandbox_contract_sha256"],
            })
    ledger.pop("ledger_sha256")
    ledger["ledger_sha256"] = canonical_sha256(ledger)
    assert validate_retry_ledger(ledger, candidate_sha, True, bindings) is ledger

    replay = ledger["attempts"][0]["attempts"][1]
    replay["input_binding"]["commands"] = [["python", "different.py"]]
    replay["input_binding"].pop("binding_sha256")
    replay["input_binding"]["binding_sha256"] = canonical_sha256(replay["input_binding"])
    ledger.pop("ledger_sha256")
    ledger["ledger_sha256"] = canonical_sha256(ledger)
    with pytest.raises(AdmissionFailure, match="replay input binding drifted"):
        validate_retry_ledger(ledger, candidate_sha, True, bindings)


def test_v4_final_admission_requires_and_validates_post_teacher_preflight(tmp_path: Path) -> None:
    value, runtime_path = envelope(tmp_path)
    value["schema_version"] = V4_ENVELOPE_SCHEMA
    item = value["candidate"]
    assigned = value["assignment"]
    assigned.update(
        contract_id=V4_CONTRACT_ID, id=item["id"],
        primary_capability_definition="Aggregate signed integer values deterministically.",
    )
    pretest = deepcopy(item)
    pretest["verification_task"]["files"] = []
    marker = load_preflight_config(V4_PREFLIGHT_CONFIG)["success_marker"]
    witness_content = (
        "from solution import compute_total\n"
        "try:\n    compute_total(None)\nexcept (TypeError, ValueError):\n    pass\n"
        "else:\n    raise AssertionError('malformed input must be rejected')\n"
        f"print('{marker}')\n"
    )
    proof = value["evidence"]["teacher_proof"]
    proof.update(
        schema_version=V4_PROOF_SCHEMA,
        queue_record_sha256="4" * 64,
        teacher_run_evidence_sha256="5" * 64,
        known_bad_cross_witness={
            "schema_version": V4_WITNESS_SCHEMA,
            "valid_domain_input": "None isolates malformed-input handling",
            "scheduled_dimension_assertion": "both implementations reject None",
            "path": "cross_witness.py", "content": witness_content,
            "content_sha256": sha256_text(witness_content),
            "valid_domain": True, "scheduled_dimension_only": True,
        },
        visibility={
            "source_affinity_card": True, "source_lineage": True,
            "runtime_contract": True, "evaluation_artifacts_read": 0,
        },
    )
    proof["teacher_candidate_sha256"] = canonical_sha256(pretest)
    proof.pop("evidence_sha256")
    seal(proof)
    lane_config = load_preflight_config(V4_PREFLIGHT_CONFIG)["lanes"]["python"]

    def preflight_result(commands, stdout=""):
        return {
            "runtime_id": "python-locked",
            "image": "python-fixture@sha256:" + "2" * 64,
            "image_id": "sha256:" + "1" * 64,
            "commands": commands, "exit_codes": [0] * len(commands),
            "timed_out": False, "stdout": stdout, "stdout_sha256": sha256_text(stdout),
            "stderr": "", "stderr_sha256": sha256_text(""), "duration_ms": 1,
            "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        }

    preflight = build_post_teacher_preflight_evidence(
        pretest, assigned, proof,
        {name: preflight_result(lane_config["compile_commands"]) for name in ("reference", "known_bad")},
        {name: preflight_result(lane_config["witness_commands"], marker + "\n") for name in ("reference", "known_bad")},
        runtime_path, V4_PREFLIGHT_CONFIG,
    )
    value["evidence"]["post_teacher_preflight"] = preflight
    lineage = value["evidence"]["lineage"]
    lineage["contract_id"] = V4_CONTRACT_ID
    lineage["teacher_proof_evidence_sha256"] = proof["evidence_sha256"]
    lineage["post_teacher_preflight_evidence_sha256"] = preflight["evidence_sha256"]
    lineage.pop("evidence_sha256")
    seal(lineage)

    admitted = validate_envelope(
        value, admission_config(), runtime_path, SEPARATION_CONTRACT,
        V4_CONTRACT_ID, V4_PREFLIGHT_CONFIG,
    )
    assert admitted["id"] == item["id"]
    assert admitted["schema_version"] == "ganesh-mini-repair-delta-v4-admitted/v1"
    command_drift = deepcopy(value)
    command_drift["evidence"]["executable"]["results"]["reference"][
        "primary_discrimination"
    ]["commands"] = [["python", "different.py"]]
    reseal_evidence(command_drift, "executable")
    with pytest.raises(AdmissionFailure, match="executable evidence binding mismatch"):
        validate_envelope(
            command_drift, admission_config(), runtime_path, SEPARATION_CONTRACT,
            V4_CONTRACT_ID, V4_PREFLIGHT_CONFIG,
        )
    outputs, rejected = admit(
        [value], admission_config(), runtime_path, SEPARATION_CONTRACT,
        contract_id=V4_CONTRACT_ID, v4_preflight_config=V4_PREFLIGHT_CONFIG,
    )
    assert [row["id"] for row in outputs] == [item["id"]]
    assert rejected == []

    del value["evidence"]["post_teacher_preflight"]
    with pytest.raises(ValueError, match="evidence set"):
        validate_envelope(
            value, admission_config(), runtime_path, SEPARATION_CONTRACT,
            V4_CONTRACT_ID, V4_PREFLIGHT_CONFIG,
        )


def test_accepts_exact_pinned_commitpackft_extended_provenance(tmp_path: Path) -> None:
    value, runtime_path = envelope(tmp_path)
    candidate_value = value["candidate"]
    candidate_value["lane"] = "javascript"
    task = candidate_value["verification_task"]
    task.update(language="javascript", family="javascript_typescript", candidate_path="solution.js")
    value["assignment"]["cell_id"] = "numeric_reasoning/javascript/repair"
    value["evidence"]["lineage"]["cell_id"] = "numeric_reasoning/javascript/repair"
    runtime_document = json.loads(runtime_path.read_text())
    runtime_document["runtimes"]["python-locked"].update(
        language="javascript", candidate_path="solution.js", commands=[["node", "solution.test.js"]]
    )
    runtime_document["runtimes"]["javascript-fixture"].update(
        language="python", candidate_path="solution.py", commands=[["python", "test_solution.py"]]
    )
    runtime_path.write_text(json.dumps(runtime_document))
    executable = value["evidence"]["executable"]
    executable["runtime_config_sha256"] = hashlib.sha256(runtime_path.read_bytes()).hexdigest()
    roles = value["evidence"]["test_author"]["test_roles"]
    for row in roles:
        row["canonical_path"] = "solution.test.js"
    for role in ("primary_discrimination", "cross_cutting"):
        row = next(row for row in roles if row["role"] == role)
        staging = staging_contract(candidate_value, row, runtime_document["runtimes"]["python-locked"])
        for implementation in ("reference", "known_bad"):
            executable["results"][implementation][role]["staging"] = staging
            executable["results"][implementation][role]["suite_sha256"] = staging["suite_sha256"]
    rebind_source(value, commitpack_source())

    admitted = validate_envelope(value, commitpack_config(), runtime_path, SEPARATION_CONTRACT)

    assert admitted["candidate"]["source"]["dataset"] == "bigcode/commitpackft"
    assert admitted["candidate"]["source"]["source_file_sha256"] == "2" * 64


def test_accepts_exact_v4_native_commitpackft_provenance() -> None:
    item = candidate()
    item["source"] = commitpack_v4_native_source()

    assert validate_candidate(item, commitpack_config()) is item


@pytest.mark.parametrize(
    "mutation",
    [
        lambda source: source.pop("selection_rank"),
        lambda source: source.update(selection_rank=0),
        lambda source: source.update(selection_rank=True),
        lambda source: source.pop("quarantined_record_sha256"),
        lambda source: source.update(quarantined_record_sha256="not-a-hash"),
    ],
)
def test_v4_native_commitpackft_provenance_fails_closed(mutation) -> None:
    item = candidate()
    item["source"] = commitpack_v4_native_source()
    mutation(item["source"])

    with pytest.raises(ValueError):
        validate_candidate(item, commitpack_config())


def test_legacy_commitpackft_rejects_v4_native_fields() -> None:
    item = candidate()
    item["lane"] = "javascript"
    item["verification_task"]["language"] = "javascript"
    item["source"] = commitpack_source()
    item["source"].update(quarantined_record_sha256="a" * 64, selection_rank=1)

    with pytest.raises(ValueError, match="source keys"):
        validate_candidate(item, commitpack_config())


@pytest.mark.parametrize(
    ("mutation", "reason"),
    [
        (lambda source: source.update(unexpected="not allowed"), "source keys"),
        (lambda source: source.pop("raw_line_sha256"), "source keys"),
        (lambda source: source.update(source_file_sha256="9" * 64), "pinned dataset-specific"),
        (lambda source: source.update(source_file_bytes="128001108"), "pinned dataset-specific"),
        (lambda source: source.update(license="GPL-3.0"), "pinned dataset-specific"),
        (lambda source: source.update(repositories=["different/repo"]), "pinned dataset-specific"),
        (lambda source: source.update(record_id="data/javascript/data.jsonl:line-12"), "pinned dataset-specific"),
    ],
)
def test_commitpackft_provenance_fails_closed_on_schema_or_pin_drift(mutation, reason: str) -> None:
    item = candidate()
    item["lane"] = "javascript"
    item["verification_task"]["language"] = "javascript"
    item["source"] = commitpack_source()
    mutation(item["source"])

    with pytest.raises(ValueError, match=reason):
        validate_candidate(item, commitpack_config())


@pytest.mark.parametrize("dataset", ["Multilingual-Multimodal-NLP/McEval-Instruct", "m-a-p/MdEval-Instruct"])
def test_native_source_contract_still_rejects_any_extra_key(dataset: str) -> None:
    item = candidate()
    item["source"].update(dataset=dataset, revision="native-revision", license="MIT")
    config = admission_config()
    config["sources"][dataset] = {"revision": "native-revision", "license": "MIT"}

    assert validate_candidate(item, config) is item
    item["source"]["unexpected"] = "no"

    with pytest.raises(ValueError, match="source keys"):
        validate_candidate(item, config)


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

    value, runtime_path = envelope(tmp_path)
    result = value["evidence"]["executable"]["results"]["known_bad"]["cross_cutting"]
    result["staging"]["canonical_path"] = "test_cross.py"
    reseal_evidence(value, "executable")
    with pytest.raises(ValueError, match="binding mismatch"):
        validate_envelope(value, admission_config(), runtime_path, SEPARATION_CONTRACT)
