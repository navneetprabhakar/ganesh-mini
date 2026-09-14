from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.admit_capability_qualification import (
    admit_qualification,
    build_report,
    candidate_execution_fingerprint,
    execution_contract,
    load_execution_reuse,
    validate_envelope,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import SANDBOX_CONTRACT


def plan() -> dict:
    cells = []
    for index in range(120):
        cells.append({
            "cell_id": f"cap-{index}/python/generation",
            "primary_capability": f"cap-{index}",
            "lane": "python",
            "task_type": "generation",
            "assigned_cross_cutting_dimension": "malformed_input",
        })
    value = {
        "schema_version": "ganesh-mini-capability-stratified-corpus-plan/v1",
        "matrix": {"cells": 120, "cell_contracts": cells},
        "qualification": {"drafts": 240, "minimum_admitted": 120, "minimum_admitted_per_cell": 1},
    }
    value["plan_sha256"] = canonical_sha256(value)
    return value


def candidate() -> dict:
    prompt = "Implement add_one(value: int) -> int and return only the complete Python source file."
    reference = "def add_one(value: int) -> int:\n    return value + 1\n"
    bad = "def add_one(value: int) -> int:\n    return value\n"
    tests = "from solution import add_one\nassert add_one(0) == 1\n"
    task = {
        "schema_version": "1.0", "task_id": "queue-0", "surface": "training_admission",
        "language": "python", "family": "python", "task_type": "generation",
        "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "candidate_path": "solution.py",
        "files": [{"path": "test_solution.py", "role": "test", "content": tests, "sha256": sha256_text(tests)}],
        "runtime_id": "python-3.11.15",
        "limits": {"timeout_seconds": 30, "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536},
        "validation": {
            "reference": {"label": "reference", "code": reference, "sha256": sha256_text(reference)},
            "known_bad": [{"label": "missing-add", "code": bad, "sha256": sha256_text(bad)}],
        },
    }
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1", "id": "queue-0",
        "lane": "python", "task_type": "generation",
        "messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": reference}],
        "source": {
            "dataset": "fixture", "uri": "https://example.invalid/source", "revision": "abc123",
            "record_id": "record-0", "license": "MIT", "license_uri": "https://example.invalid/license",
            "source_record_sha256": "a" * 64, "transformation": "capability-specific construction",
        },
        "rights": {key: True for key in ("prompt", "answer", "tests", "redistribution", "model_training")},
        "verification_task": task, "test_origin": "independent_author",
    }


def config() -> dict:
    return {
        "allowed_licenses": ["MIT"],
        "required_rights": ["prompt", "answer", "tests", "redistribution", "model_training"],
        "allowed_test_origins": ["independent_author"],
        "sources": {"fixture": {"revision": "abc123", "license": "MIT"}},
        "deduplication": {"prompt_simhash_max_hamming": 3, "minimum_fuzzy_tokens": 12},
    }


def queue_row(index: int = 0) -> dict:
    row = {
        "schema_version": "ganesh-mini-capability-qualification-draft/v1",
        "id": f"queue-{index}", "cell_id": f"cap-{index}/python/generation",
        "primary_capability": f"cap-{index}",
        "assigned_cross_cutting_dimension": "malformed_input",
        "lane": "python", "task_type": "generation", "source_queue_id": f"source-{index}",
        "source": candidate()["source"], "stimulus": {"problem": "fixture"},
    }
    row["source"]["record_id"] = f"record-{index}"
    return row


def seal(value: dict) -> dict:
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def envelope(*, direct: bool = False) -> dict:
    item = candidate()
    queue = queue_row()
    candidate_sha = canonical_sha256(item)
    queue_sha = canonical_sha256(queue)
    spec_sha = sha256_text(item["messages"][0]["content"])
    teacher = seal({
        "candidate_sha256": candidate_sha, "queue_record_sha256": queue_sha,
        "source_queue_id": queue["source_queue_id"], "source_record_sha256": "a" * 64,
        "assistant_sha256": sha256_text(item["messages"][1]["content"]),
        "rendered_prompt_sha256": "b" * 64,
        "visibility": {"training_stimulus": True, "assigned_ontology": True, "runtime_contract": True, "evaluation_artifacts_read": 0},
    })
    test_author = seal({
        "candidate_sha256": candidate_sha, "specification_sha256": spec_sha,
        "test_sha256s": [item["verification_task"]["files"][0]["sha256"]],
        "origin": "independent_author",
        "visibility": {
            "specification_only": True, "independent_of_teacher": True,
            "reference_visible": False, "known_bad_visible": False, "teacher_context_visible": False,
            "evaluation_artifacts_read": 0,
        },
    })
    semantic = seal({
        "candidate_sha256": candidate_sha, "specification_sha256": spec_sha,
        "primary_capability": "cap-0", "assigned_cross_cutting_dimension": "malformed_input",
        "verdict": "pass", "primary_capability_is_substantive": True,
        "generic_edge_case_boilerplate_is_primary": False,
        "visibility": {"specification_and_assigned_labels_only": True, "verifier_outputs_visible": False, "evaluation_artifacts_read": 0},
    })
    separation = seal({
        "candidate_sha256": candidate_sha,
        "exact_training_passed": True, "normalized_training_passed": True, "fuzzy_training_passed": True,
        "exact_evaluation_passed": True, "normalized_evaluation_passed": True, "fuzzy_evaluation_passed": True,
        "comparison_manifest_sha256": "c" * 64, "evaluation_artifacts_read_by_construction": 0,
    })
    lineage = seal({
        "candidate_sha256": candidate_sha, "queue_record_sha256": queue_sha,
        "source_identity": {"dataset": "fixture", "revision": "abc123", "record_id": "record-0"},
        "source_record_sha256": "a" * 64, "complete": True,
        "teacher_evidence_sha256": teacher["evidence_sha256"],
        "test_author_evidence_sha256": test_author["evidence_sha256"],
        "semantic_review_evidence_sha256": semantic["evidence_sha256"],
        "separation_evidence_sha256": separation["evidence_sha256"],
    })
    qualification = {
        "queue_id": "queue-0", "cell_id": "cap-0/python/generation",
        "primary_capability": "cap-0", "assigned_cross_cutting_dimension": "malformed_input",
        "source_queue_id": "source-0", "correction_passes": 0, "correction": None,
        "evidence": {"teacher": teacher, "test_author": test_author, "semantic_review": semantic, "separation": separation, "lineage": lineage},
    }
    if direct:
        return {**item, "qualification": qualification}
    return {"schema_version": "ganesh-mini-capability-qualification-envelope/v1", "candidate": item, "qualification": qualification}


def verifier(task: dict, code: str, runtime: Path) -> dict:
    passed = code == task["validation"]["reference"]["code"]
    return {"exit_codes": [0 if passed else 1], "timed_out": False, "stderr": "", "stdout": ""}


def reuse_files(tmp_path: Path) -> tuple[Path, Path, dict]:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config()) + "\n", encoding="utf-8")
    runtime = {
        "language": "python", "image": "fixture-python:locked",
        "image_id": "sha256:" + "1" * 64, "manifest_digest": "sha256:" + "2" * 64,
        "rootfs_layers": ["sha256:" + "3" * 64], "platform": "linux/amd64",
        "candidate_path": "solution.py", "commands": [["python", "test_solution.py"]],
    }
    runtime_path = tmp_path / "runtime.json"
    runtime_path.write_text(json.dumps({
        "schema_version": "3.0", "platform": "linux/amd64",
        "runtimes": {"python-3.11.15": runtime},
    }) + "\n", encoding="utf-8")
    return config_path, runtime_path, runtime


def reusable_result(task: dict, code: str, runtime: dict) -> dict:
    passed = code == task["validation"]["reference"]["code"]
    return {
        "runtime_id": task["runtime_id"],
        "image": f"fixture-python@{runtime['manifest_digest']}",
        "image_id": runtime["image_id"], "commands": runtime["commands"],
        "exit_codes": [0 if passed else 1], "timed_out": False,
        "stdout": "", "stdout_sha256": sha256_text(""),
        "stderr": "", "stderr_sha256": sha256_text(""), "duration_ms": 1,
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
    }


def test_accepts_wrapped_existing_candidate_and_executes_contract() -> None:
    output, rejected = admit_qualification(
        [envelope()], plan(), {"queue-0": queue_row()}, config(), Path("runtime.json"), verifier,
    )
    assert rejected == []
    assert output[0]["qualification"]["cell_id"] == "cap-0/python/generation"
    assert output[0]["record"]["verification"]["known_bad"][0]["result"]["exit_codes"] == [1]


def test_accepts_direct_training_candidate_with_qualification_metadata() -> None:
    candidate_value, metadata, _ = validate_envelope(
        envelope(direct=True), plan(), {"queue-0": queue_row()}, config(),
    )
    assert candidate_value["schema_version"] == "ganesh-mini-expansion-candidate/v1"
    assert metadata["queue_record_sha256"] == canonical_sha256(queue_row())


def test_terminal_no_change_correction_is_rejected_without_execution() -> None:
    value = envelope()
    candidate_sha = canonical_sha256(value["candidate"])
    value["qualification"]["correction_passes"] = 1
    value["qualification"]["correction"] = seal({
        "candidate_sha256": candidate_sha,
        "parent_candidate_sha256": candidate_sha,
        "outcome": "terminal-no-change",
    })

    def must_not_execute(*_args):
        raise AssertionError("terminal no-change must not execute")

    admitted, rejected = admit_qualification(
        [value], plan(), {"queue-0": queue_row()}, config(), Path("runtime.json"), must_not_execute,
    )
    assert admitted == []
    assert rejected[0]["reason"] == "terminal no-change correction attempt is not admissible"


def test_exact_non_timeout_evidence_is_reused_but_corrected_candidate_executes(tmp_path: Path) -> None:
    config_path, runtime_path, runtime = reuse_files(tmp_path)
    contract = execution_contract(config_path, runtime_path)
    item = candidate()
    task = item["verification_task"]
    reference = task["validation"]["reference"]
    known_bad = task["validation"]["known_bad"][0]
    reuse_index = {
        item["id"]: {
            "fingerprint": candidate_execution_fingerprint(item, contract),
            "results": {
                reference["sha256"]: reusable_result(task, reference["code"], runtime),
                known_bad["sha256"]: reusable_result(task, known_bad["code"], runtime),
            },
            "prior_outcome": "admitted",
        },
    }
    ledger: dict = {}

    def must_not_execute(task_value: dict, code: str, runtime_value: Path) -> dict:
        raise AssertionError("exact prior evidence should be reused")

    admitted, rejected = admit_qualification(
        [envelope()], plan(), {"queue-0": queue_row()}, config(), runtime_path,
        must_not_execute, reuse_index=reuse_index, reuse_contract=contract, reuse_ledger=ledger,
    )
    assert len(admitted) == 1 and rejected == []
    assert ledger["reused_candidate_ids"] == ["queue-0"]
    assert ledger["executed"] == 0

    stale_semantics = envelope()
    semantic = stale_semantics["qualification"]["evidence"]["semantic_review"]
    semantic.pop("evidence_sha256")
    semantic["verdict"] = "reject"
    seal(semantic)
    ledger = {}
    admitted, rejected = admit_qualification(
        [stale_semantics], plan(), {"queue-0": queue_row()}, config(), runtime_path,
        must_not_execute, reuse_index=reuse_index, reuse_contract=contract, reuse_ledger=ledger,
    )
    assert admitted == [] and "semantic review" in rejected[0]["reason"]
    assert ledger["reused"] == 0

    corrected = envelope()
    corrected["qualification"]["correction_passes"] = 1
    corrected["qualification"]["correction"] = seal({
        "candidate_sha256": canonical_sha256(corrected["candidate"]),
        "parent_candidate_sha256": "f" * 64,
        "outcome": "changed",
    })
    calls: list[str] = []

    def execute(task_value: dict, code: str, runtime_value: Path) -> dict:
        calls.append(sha256_text(code))
        return reusable_result(task_value, code, runtime)

    ledger = {}
    admitted, rejected = admit_qualification(
        [corrected], plan(), {"queue-0": queue_row()}, config(), runtime_path,
        execute, reuse_index=reuse_index, reuse_contract=contract, reuse_ledger=ledger,
    )
    assert len(admitted) == 1 and rejected == []
    assert set(calls) == {reference["sha256"], known_bad["sha256"]}
    assert ledger["reused"] == 0 and ledger["executed_candidate_ids"] == ["queue-0"]

    replacement_queue = queue_row()
    replacement_queue.update(
        replacement_attempt=1,
        replacement_for_cell_id=replacement_queue["cell_id"],
    )
    replacement_envelope = envelope()
    replacement_evidence = replacement_envelope["qualification"]["evidence"]
    replacement_teacher = replacement_evidence["teacher"]
    replacement_teacher.pop("evidence_sha256")
    replacement_teacher["queue_record_sha256"] = canonical_sha256(replacement_queue)
    seal(replacement_teacher)
    replacement_lineage = replacement_evidence["lineage"]
    replacement_lineage.pop("evidence_sha256")
    replacement_lineage["queue_record_sha256"] = canonical_sha256(replacement_queue)
    replacement_lineage["teacher_evidence_sha256"] = replacement_teacher["evidence_sha256"]
    seal(replacement_lineage)
    calls.clear()
    ledger = {}
    admitted, rejected = admit_qualification(
        [replacement_envelope], plan(), {"queue-0": replacement_queue}, config(), runtime_path,
        execute, reuse_index=reuse_index, reuse_contract=contract, reuse_ledger=ledger,
    )
    assert len(admitted) == 1 and rejected == []
    assert set(calls) == {reference["sha256"], known_bad["sha256"]}
    assert ledger["reused"] == 0 and ledger["executed_candidate_ids"] == ["queue-0"]


def test_loads_only_sealed_exact_prior_execution_evidence(tmp_path: Path) -> None:
    config_path, runtime_path, runtime = reuse_files(tmp_path)
    contract = execution_contract(config_path, runtime_path)
    envelope_path = tmp_path / "prior-envelopes.jsonl"
    envelope_path.write_text(json.dumps(envelope()) + "\n", encoding="utf-8")
    admitted, rejected = admit_qualification(
        [envelope()], plan(), {"queue-0": queue_row()}, config(), runtime_path,
        lambda task, code, _: reusable_result(task, code, runtime),
    )
    admitted_path = tmp_path / "prior-admitted.jsonl"
    admitted_path.write_text("".join(json.dumps(row) + "\n" for row in admitted), encoding="utf-8")
    rejected_path = tmp_path / "prior-rejected.json"
    rejected_path.write_text(json.dumps(rejected) + "\n", encoding="utf-8")
    report = build_report(
        mode="final", plan=plan(), queue_manifest={"manifest_sha256": "d" * 64},
        input_path=envelope_path, output_path=admitted_path, rejected_path=rejected_path,
        admitted=admitted, rejected=rejected, verifier_workers=1, record_workers=1,
        queue_by_id={"queue-0": queue_row()}, execution_contract_value=contract,
    )
    report_path = tmp_path / "prior-report.json"
    report_path.write_text(json.dumps(report) + "\n", encoding="utf-8")
    reuse, source = load_execution_reuse(report_path, contract)
    assert list(reuse) == ["queue-0"]
    assert source["eligible_candidate_ids"] == ["queue-0"]

    mismatched = dict(contract)
    mismatched["sandbox_contract_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="execution contract"):
        load_execution_reuse(report_path, mismatched)

    admitted[0]["record"]["verification"]["reference"]["timed_out"] = True
    admitted_path.write_text("".join(json.dumps(row) + "\n" for row in admitted), encoding="utf-8")
    with pytest.raises(ValueError, match="artifact binding changed"):
        load_execution_reuse(report_path, contract)

    verification = admitted[0]["record"]["verification"]
    verification.pop("evidence_sha256")
    verification["evidence_sha256"] = sha256_object(verification)
    admitted_path.write_text("".join(json.dumps(row) + "\n" for row in admitted), encoding="utf-8")
    report["outputs"]["admitted"] = {
        "path": str(admitted_path), "bytes": admitted_path.stat().st_size,
        "sha256": hashlib.sha256(admitted_path.read_bytes()).hexdigest(),
    }
    report.pop("report_sha256")
    report["report_sha256"] = canonical_sha256(report)
    report_path.write_text(json.dumps(report) + "\n", encoding="utf-8")
    reuse, _ = load_execution_reuse(report_path, contract)
    assert reuse == {}


@pytest.mark.parametrize(
    ("evidence_name", "mutate", "reason"),
    [
        (None, lambda value: value["qualification"].update(cell_id="wrong"), "sealed queue"),
        ("teacher", lambda item: item["visibility"].update(evaluation_artifacts_read=1), "exactly zero"),
        ("test_author", lambda item: item["visibility"].update(reference_visible=True), "explicitly false"),
        ("semantic_review", lambda item: item.update(verdict="reject"), "does not confirm"),
        ("separation", lambda item: item.update(fuzzy_evaluation_passed=False), "explicitly true"),
        ("lineage", lambda item: item.update(complete=False), "explicitly true"),
        (None, lambda value: value["qualification"].update(correction_passes=2), "zero or one"),
    ],
)
def test_fails_closed_on_binding_isolation_review_separation_and_corrections(evidence_name, mutate, reason: str) -> None:
    value = envelope()
    if evidence_name is None:
        mutate(value)
    else:
        evidence = value["qualification"]["evidence"][evidence_name]
        evidence.pop("evidence_sha256")
        mutate(evidence)
        seal(evidence)
    with pytest.raises(ValueError, match=reason):
        validate_envelope(value, plan(), {"queue-0": queue_row()}, config())


def test_rejects_reference_that_fails_executable_admission() -> None:
    def always_fail(task: dict, code: str, runtime: Path) -> dict:
        return {"exit_codes": [1], "timed_out": False, "stderr": "failure", "stdout": ""}

    output, rejected = admit_qualification(
        [envelope()], plan(), {"queue-0": queue_row()}, config(), Path("runtime.json"), always_fail,
    )
    assert output == []
    assert "reference solution failed" in rejected[0]["reason"]


def test_preverifier_envelope_rejection_preserves_nested_candidate_id() -> None:
    value = envelope()
    semantic = value["qualification"]["evidence"]["semantic_review"]
    semantic.pop("evidence_sha256")
    semantic["verdict"] = "reject"
    semantic["primary_capability_is_substantive"] = False
    seal(semantic)
    output, rejected = admit_qualification(
        [value], plan(), {"queue-0": queue_row()}, config(), Path("runtime.json"), verifier,
    )
    assert output == []
    assert rejected[0]["id"] == "queue-0"
    assert not rejected[0]["id"].startswith("line-")


def test_final_mode_alone_enforces_overall_and_every_cell(tmp_path: Path) -> None:
    admitted_path = tmp_path / "admitted.jsonl"
    rejected_path = tmp_path / "rejected.json"
    input_path = tmp_path / "input.jsonl"
    admitted_path.write_text("", encoding="utf-8")
    rejected_path.write_text("[]\n", encoding="utf-8")
    input_path.write_text("{}\n", encoding="utf-8")
    queue_manifest = {"manifest_sha256": "d" * 64}
    candidate_report = build_report(
        mode="candidate", plan=plan(), queue_manifest=queue_manifest,
        input_path=input_path, output_path=admitted_path, rejected_path=rejected_path,
        admitted=[], rejected=[], verifier_workers=1, record_workers=1,
    )
    final_report = build_report(
        mode="final", plan=plan(), queue_manifest=queue_manifest,
        input_path=input_path, output_path=admitted_path, rejected_path=rejected_path,
        admitted=[], rejected=[], verifier_workers=1, record_workers=1,
    )
    assert candidate_report["status"] == "candidate-admission-complete"
    assert final_report["status"] == "failed"
    assert len(final_report["missing_cells"]) == 120
    body = dict(final_report); seal_value = body.pop("report_sha256")
    assert canonical_sha256(body) == seal_value

    complete = []
    queue = {}
    envelopes = []
    for index in range(120):
        for ordinal in range(2):
            identifier = f"queue-{index}-{ordinal}"
            source = {"dataset": "fixture", "revision": "abc", "record_id": identifier}
            queue[identifier] = {
                "id": identifier, "cell_id": f"cap-{index}/python/generation",
                "primary_capability": f"cap-{index}",
                "assigned_cross_cutting_dimension": "malformed_input",
                "source_queue_id": f"source-{index}-{ordinal}",
                "lane": "python", "task_type": "generation", "source": source,
            }
            envelopes.append({
                "schema_version": "ganesh-mini-capability-qualification-envelope/v1",
                "candidate": {"id": identifier, "lane": "python", "task_type": "generation", "source": source},
                "qualification": {
                    "queue_id": identifier, "cell_id": f"cap-{index}/python/generation",
                    "primary_capability": f"cap-{index}",
                    "assigned_cross_cutting_dimension": "malformed_input",
                    "source_queue_id": f"source-{index}-{ordinal}",
                },
            })
        complete.append({"qualification": {"cell_id": f"cap-{index}/python/generation"}})
    input_path.write_text("".join(json.dumps(row) + "\n" for row in envelopes), encoding="utf-8")
    disposition_rejections = [
        {"line": index + 121, "id": f"queue-{index}-1", "reason": "not admitted"}
        for index in range(120)
    ]
    passing_report = build_report(
        mode="final", plan=plan(), queue_manifest=queue_manifest,
        input_path=input_path, output_path=admitted_path, rejected_path=rejected_path,
        admitted=complete, rejected=disposition_rejections, verifier_workers=1, record_workers=1,
        queue_by_id=queue,
    )
    assert passing_report["status"] == "passed"
    assert passing_report["final_gate"]["passed"] is True
    assert passing_report["queue_disposition"]["all_originals_dispositioned"] is True

    one_per_cell = envelopes[::2]
    input_path.write_text("".join(json.dumps(row) + "\n" for row in one_per_cell), encoding="utf-8")
    subset_report = build_report(
        mode="final", plan=plan(), queue_manifest=queue_manifest,
        input_path=input_path, output_path=admitted_path, rejected_path=rejected_path,
        admitted=complete, rejected=[], verifier_workers=1, record_workers=1,
        queue_by_id=queue,
    )
    assert subset_report["status"] == "failed"
    assert len(subset_report["queue_disposition"]["missing_queue_ids"]) == 120

    corrupt = deepcopy(envelopes)
    corrupt[0]["candidate"]["source"] = {"dataset": "fixture", "revision": "abc", "record_id": "wrong"}
    input_path.write_text("".join(json.dumps(row) + "\n" for row in corrupt), encoding="utf-8")
    corrupt_report = build_report(
        mode="final", plan=plan(), queue_manifest=queue_manifest,
        input_path=input_path, output_path=admitted_path, rejected_path=rejected_path,
        admitted=complete, rejected=disposition_rejections, verifier_workers=1, record_workers=1,
        queue_by_id=queue,
    )
    assert corrupt_report["status"] == "failed"
    assert corrupt_report["queue_disposition"]["input_binding_failures"][0]["reason"] == "cell or source binding mismatch"

    replacement_id = "replacement-cell-0"
    replacement_source = {"dataset": "fixture", "revision": "abc", "record_id": replacement_id}
    replacement_row = {
        "id": replacement_id, "cell_id": "cap-0/python/generation", "primary_capability": "cap-0",
        "assigned_cross_cutting_dimension": "malformed_input", "source_queue_id": "replacement-source-0",
        "lane": "python", "task_type": "generation", "source": replacement_source,
        "replacement_attempt": 1, "replacement_for_cell_id": "cap-0/python/generation",
    }
    replacement_envelope = {
        "schema_version": "ganesh-mini-capability-qualification-envelope/v1",
        "candidate": {"id": replacement_id, "lane": "python", "task_type": "generation", "source": replacement_source},
        "qualification": {
            "queue_id": replacement_id, "cell_id": replacement_row["cell_id"], "primary_capability": "cap-0",
            "assigned_cross_cutting_dimension": "malformed_input", "source_queue_id": "replacement-source-0",
        },
    }
    augmented_queue = {**queue, replacement_id: replacement_row}
    augmented_envelopes = [*envelopes, replacement_envelope]
    input_path.write_text("".join(json.dumps(row) + "\n" for row in augmented_envelopes), encoding="utf-8")
    replacement_rejections = [*disposition_rejections, {"line": 241, "id": replacement_id, "reason": "not admitted"}]
    replacement_report = build_report(
        mode="final", plan=plan(), queue_manifest=queue_manifest,
        input_path=input_path, output_path=admitted_path, rejected_path=rejected_path,
        admitted=complete, rejected=replacement_rejections, verifier_workers=1, record_workers=1,
        queue_by_id=augmented_queue,
    )
    assert replacement_report["status"] == "passed"
    assert replacement_report["queue_disposition"]["bounded_replacements"] == 1

    second = deepcopy(replacement_row); second["id"] = "replacement-cell-0-again"
    second["source_queue_id"] = "replacement-source-0-again"
    second["source"] = {"dataset": "fixture", "revision": "abc", "record_id": second["id"]}
    second_envelope = deepcopy(replacement_envelope)
    second_envelope["candidate"].update(id=second["id"], source=second["source"])
    second_envelope["qualification"].update(queue_id=second["id"], source_queue_id=second["source_queue_id"])
    input_path.write_text("".join(json.dumps(row) + "\n" for row in [*augmented_envelopes, second_envelope]), encoding="utf-8")
    second_report = build_report(
        mode="final", plan=plan(), queue_manifest=queue_manifest,
        input_path=input_path, output_path=admitted_path, rejected_path=rejected_path,
        admitted=complete, rejected=[*replacement_rejections, {"line": 242, "id": second["id"], "reason": "not admitted"}],
        verifier_workers=1, record_workers=1, queue_by_id={**augmented_queue, second["id"]: second},
    )
    assert second_report["status"] == "failed"
