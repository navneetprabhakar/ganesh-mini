from __future__ import annotations

import json
import threading
import time
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.admit_repair_delta import teacher_candidate_sha256, validate_envelope
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_separation_attestations import PASS_FIELDS, SCHEMA_VERSION
from scripts.data.run_repair_delta_two_phase import (
    PREPARATION_SCHEMA,
    _envelope_assignment,
    build_separation_sidecars,
    canonicalize_v4_terminal_order,
    prepare_candidate,
    prepare_candidate_v4,
    run_preparation_resumable,
    run_resume_resumable,
    run_resume_resumable_v4,
    resume_candidate,
    V4_VERIFIER_SCHEDULER_CONTRACT,
    V4_VERIFIER_SCHEDULER_SHA256,
    write_terminal_artifacts,
)
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import SANDBOX_CONTRACT


def fixture_candidate() -> dict:
    prompt = "Repair compute_total so signed integers are summed while malformed input remains rejected."
    reference = "def compute_total(values):\n    if values is None: raise TypeError()\n    return sum(values)\n"
    known_bad = "def compute_total(values):\n    if values is None: raise TypeError()\n    return max(values)\n"
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1",
        "id": "repair-0", "lane": "python", "task_type": "repair",
        "messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": reference}],
        "source": {
            "dataset": "fixture", "uri": "https://example.invalid/source",
            "revision": "r1", "record_id": "source-0", "license": "MIT",
            "license_uri": "https://example.invalid/license",
            "source_record_sha256": "a" * 64, "transformation": "repair-delta construction",
        },
        "rights": {name: True for name in ("prompt", "answer", "tests", "redistribution", "model_training")},
        "test_origin": "independent_author",
        "verification_task": {
            "schema_version": "1.0", "task_id": "repair-0", "surface": "training_admission",
            "language": "python", "family": "python", "task_type": "repair",
            "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
            "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
            "candidate_path": "solution.py", "files": [], "runtime_id": "python-locked",
            "limits": {"timeout_seconds": 30, "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536},
            "validation": {
                "reference": {"label": "reference", "code": reference, "sha256": sha256_text(reference)},
                "known_bad": [{"label": "maximum", "code": known_bad, "sha256": sha256_text(known_bad)}],
            },
        },
    }


def generated_and_assignment() -> tuple[dict, dict]:
    candidate = fixture_candidate()
    assignment = {
        "id": candidate["id"], "contract_id": "capability-stratified-v3-repair-delta/v1",
        "cell_id": "numeric_reasoning/python/repair", "primary_capability": "numeric_reasoning",
        "primary_capability_definition": "perform exact numeric aggregation",
        "assigned_cross_cutting_dimension": "malformed_input",
    }
    proof = {
        "candidate_id": candidate["id"], "teacher_candidate_sha256": teacher_candidate_sha256(candidate),
        "primary_capability": "numeric_reasoning", "assigned_cross_cutting_dimension": "malformed_input",
        "capability_operation": "sum signed integers",
        "defective_intermediate_or_decision": "maximum instead of sum",
        "valid_domain_counterexample": "[2, 3] is 5, not 3",
        "minimal_capability_specific_patch": "replace maximum with sum",
        "scheduled_dimension_obligation": "reject None",
        "known_bad_already_satisfies_scheduled_dimension": True,
        "cross_dimension_only_patch_cannot_solve": True,
        "capability_remains_substantive_without_cross_clause": True,
    }
    proof["evidence_sha256"] = canonical_sha256(proof)
    return {"candidate": candidate, "repair_delta_proof": proof}, assignment


def semantic(_projection: dict) -> dict:
    return {
        "repair_delta_requires_primary_capability": True,
        "scheduled_dimension_is_concrete_and_secondary": True,
        "known_bad_already_satisfies_scheduled_dimension": True,
        "cross_dimension_only_patch_cannot_solve": True,
        "capability_remains_substantive_without_cross_clause": True,
        "generic_boilerplate_is_not_primary": True,
        "rationale": "the known bad selects a maximum but already rejects None",
        "_run_sha256": "1" * 64,
    }


def author_stage(_projection: dict) -> dict:
    return {
        "files": [
            {
                "path": "test_primary.py",
                "content": "from solution import compute_total\nassert compute_total([2,3]) == 5\nassert compute_total([-2,3]) == 1\n",
                "role": "primary_discrimination", "case_ids": ["positive", "signed"],
            },
            {
                "path": "test_cross.py",
                "content": "from solution import compute_total\ntry:\n compute_total(None)\nexcept TypeError:\n pass\n",
                "role": "cross_cutting", "case_ids": ["none"],
            },
        ],
        "_run_sha256": "2" * 64,
    }


def delta(_projection: dict) -> dict:
    return {
        "independent_semantic_delta_count": 1,
        "delta_is_capability_specific": True,
        "introduces_multiple_independent_fixes": False,
        "delta_description": "maximum is replaced by signed summation",
        "_run_sha256": "3" * 64,
    }


def separation_report(candidate: dict, passed: bool = True) -> dict:
    policy = {
        "exact": "fixture exact", "normalized": "fixture normalized", "fuzzy": "fixture fuzzy",
        "prompt_simhash_max_hamming": 3, "minimum_fuzzy_tokens": 12,
        "peer_candidate_comparison": True, "fail_closed": True,
    }
    manifest = {"policy": policy}
    report = {
        "schema_version": SCHEMA_VERSION,
        "status": "passed" if passed else "failed",
        "evaluation_artifacts_read_by_construction": 0,
        "comparison_stage_evaluation_artifacts_read": 1,
        "comparison_manifest": manifest,
        "comparison_manifest_sha256": canonical_sha256(manifest),
        "records": [{
            "id": candidate["id"], "candidate_sha256": canonical_sha256(candidate),
            **{field: passed for field in PASS_FIELDS},
        }],
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def runtime_file(tmp_path: Path) -> tuple[Path, dict]:
    runtime = {
        "language": "python", "image": "python-fixture:locked",
        "image_id": "sha256:" + "1" * 64, "manifest_digest": "sha256:" + "2" * 64,
        "rootfs_layers": ["sha256:" + "3" * 64], "platform": "linux/amd64",
        "candidate_path": "solution.py", "commands": [["python", "test_solution.py"]],
    }
    companions = {
        "go-fixture": {"language": "go", "candidate_path": "solution.go", "commands": [["go", "test", "./..."]]},
        "java-fixture": {"language": "java", "candidate_path": "Solution.java", "commands": [["javac", "SolutionTest.java"]]},
        "javascript-fixture": {"language": "javascript", "candidate_path": "solution.js", "commands": [["node", "solution.test.js"]]},
        "typescript-fixture": {"language": "typescript", "candidate_path": "solution.ts", "commands": [["node", "solution.test.ts"]]},
        "rust-fixture": {"language": "rust", "candidate_path": "solution.rs", "commands": [["rustc", "--test", "solution_test.rs"]]},
    }
    for value in companions.values():
        value["platform"] = "linux/amd64"
    path = tmp_path / "runtimes.json"
    path.write_text(json.dumps({
        "schema_version": "3.0", "platform": "linux/amd64",
        "runtimes": {"python-locked": runtime, **companions},
    }))
    return path, runtime


def test_preparation_never_executes_and_resume_uses_sealed_global_sidecar(tmp_path: Path) -> None:
    generated, assignment = generated_and_assignment()
    prepared = prepare_candidate(generated, assignment, semantic, author_stage, delta)
    assert prepared["schema_version"] == PREPARATION_SCHEMA
    assert prepared["status"] == "awaiting-separation"
    assert prepared["execution_performed"] is False
    assert "executable" not in prepared["evidence"]


    sidecars, contract = build_separation_sidecars(
        separation_report(prepared["candidate"]), [prepared["candidate"]], tmp_path / "sidecars.jsonl",
    )
    assert len(contract) == 64
    calls = []
    staged_tasks = []
    runtime_path, runtime = runtime_file(tmp_path)

    def verifier(_task: dict, code: str, _runtime: Path) -> dict:
        calls.append(code)
        staged_tasks.append(deepcopy(_task))
        should_pass = "sum(values)" in code or "raise TypeError" in code
        # Known-bad is expected to pass the cross-cutting suite. The fixture
        # verifier does not see the logical role, so distinguish by call order.
        if "max(values)" in code:
            should_pass = len(calls) == 4
        return {
            "runtime_id": "python-locked",
            "image": f"python-fixture@{runtime['manifest_digest']}",
            "image_id": runtime["image_id"], "manifest_digest": runtime["manifest_digest"],
            "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
            "timed_out": False, "exit_codes": [0 if should_pass else 1],
        }

    artifact = resume_candidate(prepared, sidecars[0], runtime_path, verifier)
    assert artifact["status"] == "ready-for-admission"
    assert len(calls) == 4
    assert all(
        [item["path"] for item in task["files"] if item.get("role") == "test"] == ["test_solution.py"]
        for task in staged_tasks
    )
    assert all(
        item["sha256"] == sha256_text(item["content"])
        for task in staged_tasks for item in task["files"] if item.get("role") == "test"
    )
    assert artifact["envelope"]["evidence"]["separation"]["comparison_contract_sha256"] == contract
    admitted = validate_envelope(artifact["envelope"], {
        "allowed_licenses": ["MIT"],
        "required_rights": ["prompt", "answer", "tests", "redistribution", "model_training"],
        "allowed_test_origins": ["independent_author"],
        "sources": {"fixture": {"revision": "r1", "license": "MIT"}},
    }, runtime_path, contract)
    assert admitted["id"] == "repair-0"


def test_v4_malformed_test_author_response_is_candidate_local_terminal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    generated, assignment = generated_and_assignment()
    assignment["contract_id"] = "capability-stratified-v4-repair-delta/v1"
    generated["repair_delta_proof"]["schema_version"] = (
        "ganesh-mini-repair-delta-v4-proof/v1"
    )
    generated["repair_delta_proof"]["evidence_sha256"] = canonical_sha256({
        key: value for key, value in generated["repair_delta_proof"].items()
        if key != "evidence_sha256"
    })
    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.validate_teacher_proof_v4",
        lambda _candidate, _assignment, proof: proof,
    )
    monkeypatch.setattr(
        "scripts.data.run_repair_delta_two_phase.execute_post_teacher_preflight",
        lambda *_args, **_kwargs: {"evidence_sha256": "4" * 64},
    )

    def malformed_author(_projection: dict) -> dict:
        return {
            "files": [{
                "path": "only.py", "content": "pass\n",
                "role": "primary_discrimination", "case_ids": ["one"],
            }],
            "_run_sha256": "2" * 64,
        }

    artifact = prepare_candidate_v4(
        generated, assignment, semantic, malformed_author, delta,
        tmp_path / "runtime.json", tmp_path / "preflight.json",
    )
    assert artifact["status"] == "terminal-rejected"
    assert artifact["terminal_stage"] == "test_author_contract"
    failure = artifact["evidence"]["stage_contract_failure"]
    assert failure["stage"] == "test_author"
    assert failure["run_evidence_sha256"] == "2" * 64
    assert failure["evidence_sha256"] == canonical_sha256({
        key: value for key, value in failure.items() if key != "evidence_sha256"
    })


def test_v4_concurrent_results_are_reconstructed_in_primary_queue_order() -> None:
    expected = [f"candidate-{index}" for index in range(60)]
    binding = {"ordered_primary_candidate_ids": expected}
    rows = [
        {"candidate_id": identifier, "marker": index}
        for index, identifier in enumerate(reversed(expected))
    ]
    ordered = canonicalize_v4_terminal_order(rows, binding)
    assert [row["candidate_id"] for row in ordered] == expected
    with pytest.raises(ValueError, match="exact primary cohort"):
        canonicalize_v4_terminal_order(rows[:-1], binding)


def test_v4_envelope_preserves_exact_full_assignment_while_v3_projects() -> None:
    assignment = {
        "contract_id": "capability-stratified-v4-repair-delta/v1",
        "id": "candidate", "cell_id": "numeric_reasoning/python/repair",
        "primary_capability": "numeric_reasoning",
        "primary_capability_definition": "perform arithmetic",
        "assigned_cross_cutting_dimension": "malformed_input",
        "source_queue_id": "source", "generation_eligible": True,
    }
    assert _envelope_assignment(
        assignment, "capability-stratified-v4-repair-delta/v1",
    ) == assignment
    projected = _envelope_assignment(
        assignment, "capability-stratified-v3-repair-delta/v1",
    )
    assert set(projected) == {
        "contract_id", "cell_id", "primary_capability",
        "assigned_cross_cutting_dimension",
    }


def test_failed_global_separation_is_terminal_without_execution(tmp_path: Path) -> None:
    generated, assignment = generated_and_assignment()
    prepared = prepare_candidate(generated, assignment, semantic, author_stage, delta)
    sidecars, _ = build_separation_sidecars(
        separation_report(prepared["candidate"], passed=False),
        [prepared["candidate"]], tmp_path / "sidecars.jsonl",
    )
    runtime_path, _ = runtime_file(tmp_path)
    calls = []

    def verifier(*args):
        calls.append(args)
        raise AssertionError("separation failures must not execute")

    artifact = resume_candidate(prepared, sidecars[0], runtime_path, verifier)
    assert artifact["status"] == "terminal-rejected"
    assert artifact["terminal_stage"] == "separation"
    assert calls == []


def preparation_inputs(count: int) -> tuple[list[dict], dict[str, dict]]:
    generated, assignment = generated_and_assignment()
    rows = []
    assignments = {}
    for ordinal in range(count):
        row = deepcopy(generated)
        candidate = row["candidate"]
        identifier = f"repair-{ordinal}"
        candidate["id"] = identifier
        candidate["source"]["record_id"] = f"source-{ordinal}"
        candidate["verification_task"]["task_id"] = identifier
        proof = row["repair_delta_proof"]
        proof["candidate_id"] = identifier
        proof["teacher_candidate_sha256"] = teacher_candidate_sha256(candidate)
        proof.pop("evidence_sha256")
        proof["evidence_sha256"] = canonical_sha256(proof)
        assigned = deepcopy(assignment)
        assigned["id"] = identifier
        rows.append(row)
        assignments[identifier] = assigned
    return rows, assignments


def test_parallel_preparation_preserves_order_and_deterministic_artifacts(tmp_path: Path) -> None:
    generated, assignments = preparation_inputs(6)
    active = 0
    maximum_active = 0
    lock = threading.Lock()

    def concurrent_semantic(projection: dict) -> dict:
        nonlocal active, maximum_active
        with lock:
            active += 1
            maximum_active = max(maximum_active, active)
        time.sleep(0.02)
        with lock:
            active -= 1
        return semantic(projection)

    parallel = run_preparation_resumable(
        generated, assignments, tmp_path / "parallel",
        concurrent_semantic, author_stage, delta, workers=4,
    )
    sequential = run_preparation_resumable(
        generated, assignments, tmp_path / "sequential",
        semantic, author_stage, delta, workers=1,
    )

    assert maximum_active > 1
    assert [row["candidate_id"] for row in parallel] == [
        row["candidate"]["id"] for row in generated
    ]
    assert parallel == sequential
    assert all("verifier_scheduler" not in row for row in parallel)
    assert len(list((tmp_path / "parallel").glob("*.pre-separation.json"))) == 6
    assert list((tmp_path / "parallel").glob("*.tmp")) == []


def test_parallel_preparation_resume_skips_completed_candidates(tmp_path: Path) -> None:
    generated, assignments = preparation_inputs(4)
    output_dir = tmp_path / "prepared"
    first = run_preparation_resumable(
        generated, assignments, output_dir, semantic, author_stage, delta, workers=4,
    )
    calls = []

    def forbidden_stage(projection: dict) -> dict:
        calls.append(projection["id"])
        raise AssertionError("sealed prepared candidates must resume without rerunning stages")

    resumed = run_preparation_resumable(
        generated, assignments, output_dir,
        forbidden_stage, forbidden_stage, forbidden_stage, workers=4,
    )

    assert resumed == first
    assert calls == []


def test_parallel_preparation_resume_rebuilds_only_missing_candidate(tmp_path: Path) -> None:
    generated, assignments = preparation_inputs(4)
    output_dir = tmp_path / "prepared"
    first = run_preparation_resumable(
        generated, assignments, output_dir, semantic, author_stage, delta, workers=4,
    )
    missing_id = generated[2]["candidate"]["id"]
    (output_dir / f"{missing_id}.pre-separation.json").unlink()
    calls = []

    def resumed_semantic(projection: dict) -> dict:
        calls.append(("semantic", projection["id"]))
        return semantic(projection)

    def resumed_author(projection: dict) -> dict:
        calls.append(("author", projection["id"]))
        return author_stage(projection)

    def resumed_delta(projection: dict) -> dict:
        calls.append(("delta", projection["id"]))
        return delta(projection)

    resumed = run_preparation_resumable(
        generated, assignments, output_dir,
        resumed_semantic, resumed_author, resumed_delta, workers=4,
    )

    assert resumed == first
    assert calls == [
        ("semantic", missing_id), ("author", missing_id), ("delta", missing_id),
    ]


@pytest.mark.parametrize("workers", [0, 13, True])
def test_preparation_rejects_invalid_worker_counts(tmp_path: Path, workers: int) -> None:
    with pytest.raises(ValueError, match="workers"):
        run_preparation_resumable([], {}, tmp_path, semantic, author_stage, delta, workers=workers)


def test_parallel_preparation_rejects_duplicate_candidate_ids_before_stage_calls(tmp_path: Path) -> None:
    generated, assignments = preparation_inputs(1)
    calls = []

    def recording_semantic(projection: dict) -> dict:
        calls.append(projection["id"])
        return semantic(projection)

    with pytest.raises(ValueError, match="identities are duplicated"):
        run_preparation_resumable(
            [generated[0], deepcopy(generated[0])], assignments, tmp_path,
            recording_semantic, author_stage, delta, workers=2,
        )
    assert calls == []


def separation_report_for_candidates(candidates: list[dict]) -> dict:
    report = separation_report(candidates[0])
    report["records"] = [{
        "id": candidate["id"], "candidate_sha256": canonical_sha256(candidate),
        **{field: True for field in PASS_FIELDS},
    } for candidate in candidates]
    report.pop("report_sha256")
    report["report_sha256"] = canonical_sha256(report)
    return report


def deterministic_verifier(runtime: dict, delay: float = 0.0, activity=None):
    def verifier(task: dict, code: str, _runtime_path: Path) -> dict:
        if activity is not None:
            lock, state = activity
            with lock:
                state["active"] += 1
                state["maximum"] = max(state["maximum"], state["active"])
        if delay:
            time.sleep(delay)
        if activity is not None:
            with lock:
                state["active"] -= 1
                state["task_ids"].append(task["task_id"])
        primary_suite = any("compute_total([2,3])" in row.get("content", "") for row in task["files"])
        should_pass = not ("max(values)" in code and primary_suite)
        return {
            "runtime_id": "python-locked",
            "image": f"python-fixture@{runtime['manifest_digest']}",
            "image_id": runtime["image_id"], "manifest_digest": runtime["manifest_digest"],
            "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
            "timed_out": False, "exit_codes": [0 if should_pass else 1],
        }
    return verifier


def prepared_cohort(tmp_path: Path, count: int):
    generated, assignments = preparation_inputs(count)
    prepared = run_preparation_resumable(
        generated, assignments, tmp_path / "preparation",
        semantic, author_stage, delta, workers=min(count, 4),
    )
    candidates = [row["candidate"] for row in prepared]
    sidecars, _ = build_separation_sidecars(
        separation_report_for_candidates(candidates), candidates, tmp_path / "sidecars.jsonl",
    )
    runtime_path, runtime = runtime_file(tmp_path)
    return prepared, sidecars, runtime_path, runtime


def test_parallel_phase_two_preserves_order_and_deterministic_artifacts(tmp_path: Path) -> None:
    prepared, sidecars, runtime_path, runtime = prepared_cohort(tmp_path, 5)
    lock = threading.Lock()
    activity = (lock, {"active": 0, "maximum": 0, "task_ids": []})
    parallel = run_resume_resumable(
        prepared, sidecars, tmp_path / "parallel", runtime_path,
        deterministic_verifier(runtime, delay=0.01, activity=activity), workers=4,
    )
    sequential = run_resume_resumable(
        prepared, sidecars, tmp_path / "sequential", runtime_path,
        deterministic_verifier(runtime), workers=1,
    )

    assert activity[1]["maximum"] > 1
    assert [row["candidate_id"] for row in parallel] == [row["candidate_id"] for row in prepared]
    assert parallel == sequential
    assert len({row["artifact_sha256"] for row in parallel}) == len(prepared)
    assert len(list((tmp_path / "parallel").glob("*.evidence.json"))) == len(prepared)


def test_parallel_phase_two_resume_skips_completed_and_rebuilds_only_missing(tmp_path: Path) -> None:
    prepared, sidecars, runtime_path, runtime = prepared_cohort(tmp_path, 4)
    output_dir = tmp_path / "evidence"
    first = run_resume_resumable(
        prepared, sidecars, output_dir, runtime_path,
        deterministic_verifier(runtime), workers=4,
    )

    def forbidden_verifier(*_args):
        raise AssertionError("sealed phase-two artifacts must resume without verification")

    assert run_resume_resumable(
        prepared, sidecars, output_dir, runtime_path, forbidden_verifier, workers=4,
    ) == first

    missing_id = prepared[1]["candidate_id"]
    (output_dir / f"{missing_id}.evidence.json").unlink()
    activity = (threading.Lock(), {"active": 0, "maximum": 0, "task_ids": []})
    resumed = run_resume_resumable(
        prepared, sidecars, output_dir, runtime_path,
        deterministic_verifier(runtime, activity=activity), workers=4,
    )
    assert resumed == first
    assert activity[1]["task_ids"] == [missing_id] * 4


@pytest.mark.parametrize("workers", [0, 13, True])
def test_phase_two_rejects_invalid_worker_counts(tmp_path: Path, workers: int) -> None:
    runtime_path, _ = runtime_file(tmp_path)
    with pytest.raises(ValueError, match="workers"):
        run_resume_resumable([], [], tmp_path / "out", runtime_path, workers=workers)


def test_parallel_phase_two_rejects_duplicate_prepared_ids_before_verification(tmp_path: Path) -> None:
    prepared, sidecars, runtime_path, runtime = prepared_cohort(tmp_path, 1)
    calls = []

    def verifier(*args):
        calls.append(args)
        return deterministic_verifier(runtime)(*args)

    with pytest.raises(ValueError, match="identities are malformed or duplicated"):
        run_resume_resumable(
            [prepared[0], deepcopy(prepared[0])], sidecars,
            tmp_path / "evidence", runtime_path, verifier, workers=2,
        )
    assert calls == []


def test_terminal_artifacts_preserve_complete_ordered_cohort(tmp_path: Path) -> None:
    prepared, sidecars, runtime_path, runtime = prepared_cohort(tmp_path, 3)
    final = run_resume_resumable(
        prepared, sidecars, tmp_path / "evidence", runtime_path,
        deterministic_verifier(runtime), workers=2,
    )
    final[1]["status"] = "terminal-rejected"
    final[1].pop("envelope")
    final[1]["cell_id"] = prepared[1]["assignment"]["cell_id"]
    final[1]["terminal_stage"] = "fixture"
    final[1]["reason"] = "fixture terminal outcome"
    final[1].pop("artifact_sha256")
    final[1]["artifact_sha256"] = canonical_sha256(final[1])

    path = tmp_path / "terminal-artifacts.jsonl"
    write_terminal_artifacts(final, path)
    rows = [json.loads(line) for line in path.read_text().splitlines()]

    assert [row["candidate_id"] for row in rows] == [
        row["candidate_id"] for row in final
    ]
    assert [row["status"] for row in rows] == [
        "ready-for-admission", "terminal-rejected", "ready-for-admission",
    ]


def test_terminal_artifacts_reject_duplicate_ids(tmp_path: Path) -> None:
    prepared, sidecars, runtime_path, runtime = prepared_cohort(tmp_path, 1)
    final = run_resume_resumable(
        prepared, sidecars, tmp_path / "evidence", runtime_path,
        deterministic_verifier(runtime), workers=1,
    )

    with pytest.raises(ValueError, match="duplicate candidate IDs"):
        write_terminal_artifacts([final[0], deepcopy(final[0])], tmp_path / "terminal.jsonl")


def test_v4_scheduler_enforces_global_and_lane_caps_and_seals_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    lanes = ["go"] * 4 + ["typescript"] * 4 + [
        "python", "java", "javascript", "rust", "python", "java",
    ]
    prepared = []
    sidecars = []
    for index, lane in enumerate(lanes):
        identifier = f"v4-{index}"
        prepared.append({
            "status": "awaiting-separation", "candidate_id": identifier,
            "candidate": {"id": identifier, "lane": lane},
            "input_sha256": f"{index:064x}", "artifact_sha256": f"{index + 100:064x}",
        })
        sidecars.append({"candidate_id": identifier, "evidence_sha256": f"{index + 200:064x}"})
    runtime_path = tmp_path / "runtimes.json"
    runtime_path.write_text("fixture runtime bytes")
    lock = threading.Lock()
    state = {
        "global": 0, "global_max": 0, "lanes": {}, "lane_max": {}, "calls": [],
    }

    def fake_resume(row, _sidecar, _runtime_path, _verifier):
        lane = row["candidate"]["lane"]
        with lock:
            state["global"] += 1
            state["global_max"] = max(state["global_max"], state["global"])
            state["lanes"][lane] = state["lanes"].get(lane, 0) + 1
            state["lane_max"][lane] = max(
                state["lane_max"].get(lane, 0), state["lanes"][lane],
            )
            state["calls"].append(row["candidate_id"])
        time.sleep(0.02)
        with lock:
            state["global"] -= 1
            state["lanes"][lane] -= 1
        value = {
            "candidate_id": row["candidate_id"], "input_sha256": row["input_sha256"],
            "phase2_input_sha256": "legacy", "status": "ready-for-admission",
        }
        value["artifact_sha256"] = canonical_sha256(value)
        return value

    monkeypatch.setattr("scripts.data.run_repair_delta_two_phase.resume_candidate", fake_resume)
    output = run_resume_resumable_v4(
        prepared, sidecars, tmp_path / "v4-evidence", runtime_path,
    )

    assert state["global_max"] == 6
    assert state["lane_max"]["go"] == 1
    assert state["lane_max"]["typescript"] == 2
    assert sorted(state["calls"]) == sorted(row["candidate_id"] for row in prepared)
    assert len(state["calls"]) == len(set(state["calls"]))
    assert [row["candidate_id"] for row in output] == [row["candidate_id"] for row in prepared]
    assert V4_VERIFIER_SCHEDULER_CONTRACT["per_candidate_suites_sequential"] is True
    assert all(row["verifier_scheduler"] == {
        "contract": V4_VERIFIER_SCHEDULER_CONTRACT,
        "contract_sha256": V4_VERIFIER_SCHEDULER_SHA256,
    } for row in output)

    def forbidden_resume(*_args):
        raise AssertionError("sealed V4 artifacts must resume without verification")

    monkeypatch.setattr("scripts.data.run_repair_delta_two_phase.resume_candidate", forbidden_resume)
    assert run_resume_resumable_v4(
        prepared, sidecars, tmp_path / "v4-evidence", runtime_path,
    ) == output
