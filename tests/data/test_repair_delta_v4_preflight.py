from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.admit_repair_delta import V4_ASSEMBLY_SCHEMA, validate_assembly_artifact
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v4_preflight import (
    CONTRACT_ID,
    EVIDENCE_SCHEMA,
    LANES,
    PLAN_SHA256,
    PROOF_SCHEMA,
    V4PreflightFailure,
    WITNESS_SCHEMA,
    build_post_teacher_preflight_evidence,
    execute_post_teacher_preflight,
    load_preflight_config,
    test_author_projection_v4 as author_projection,
    validate_post_teacher_preflight_evidence,
    validate_preflight_outcome_evidence,
)
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import SANDBOX_CONTRACT


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs/data/gate2_v4_post_teacher_preflight.json"


def candidate() -> dict:
    reference = "def normalize(value):\n    return value.strip().lower()\n"
    known_bad = "def normalize(value):\n    return value.strip()\n"
    prompt = "Repair normalization while preserving rejection of non-string input."
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1",
        "id": "v4-python-0",
        "lane": "python",
        "task_type": "repair",
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": reference},
        ],
        "verification_task": {
            "language": "python",
            "runtime_id": "python-fixture",
            "candidate_path": "solution.py",
            "files": [],
            "limits": {
                "timeout_seconds": 60, "memory_mb": 512, "cpus": 1,
                "pids": 64, "output_bytes": 65536,
            },
            "validation": {
                "reference": {"code": reference, "sha256": sha256_text(reference)},
                "known_bad": [
                    {"code": known_bad, "sha256": sha256_text(known_bad), "label": "case is not normalized"},
                ],
            },
        },
    }


def assignment() -> dict:
    return {
        "contract_id": CONTRACT_ID,
        "id": "v4-python-0",
        "cell_id": "normalization/python/repair",
        "primary_capability": "normalization",
        "primary_capability_definition": "Normalize valid text deterministically.",
        "assigned_cross_cutting_dimension": "malformed_input",
    }


def runtime_path(tmp_path: Path) -> Path:
    runtime = {
        "language": "python",
        "image": "python-fixture:locked",
        "image_id": "sha256:" + "1" * 64,
        "manifest_digest": "sha256:" + "2" * 64,
        "rootfs_layers": ["sha256:" + "3" * 64],
        "platform": "linux/amd64",
        "candidate_path": "solution.py",
        "commands": [["python3", "test_solution.py"]],
    }
    path = tmp_path / "runtimes.json"
    path.write_text(json.dumps({
        "schema_version": "3.0", "platform": "linux/amd64",
        "runtimes": {"python-fixture": runtime},
    }))
    return path


def witness() -> dict:
    marker = "GANESH_V4_KNOWN_BAD_CROSS_WITNESS_PASS"
    content = (
        "from solution import normalize\n"
        "try:\n    normalize(None)\nexcept (TypeError, ValueError):\n    pass\n"
        "else:\n    raise AssertionError('non-string input must be rejected')\n"
        f"print('{marker}')\n"
    )
    return {
        "schema_version": WITNESS_SCHEMA,
        "valid_domain_input": "None is outside text values but valid for the malformed-input clause",
        "scheduled_dimension_assertion": "normalize(None) raises TypeError or ValueError",
        "path": "cross_witness.py",
        "content": content,
        "content_sha256": sha256_text(content),
        "valid_domain": True,
        "scheduled_dimension_only": True,
    }


def teacher_proof(item: dict, assigned: dict) -> dict:
    value = {
        "schema_version": PROOF_SCHEMA,
        "candidate_id": item["id"],
        "teacher_candidate_sha256": canonical_sha256(item),
        "queue_record_sha256": "4" * 64,
        "primary_capability": assigned["primary_capability"],
        "assigned_cross_cutting_dimension": assigned["assigned_cross_cutting_dimension"],
        "capability_operation": "lowercase normalized text",
        "defective_intermediate_or_decision": "case conversion is omitted",
        "valid_domain_counterexample": "'A' returns 'A' instead of 'a'",
        "minimal_capability_specific_patch": "apply lowercase conversion",
        "scheduled_dimension_obligation": "reject non-string input",
        "known_bad_already_satisfies_scheduled_dimension": True,
        "cross_dimension_only_patch_cannot_solve": True,
        "capability_remains_substantive_without_cross_clause": True,
        "known_bad_cross_witness": witness(),
        "teacher_run_evidence_sha256": "5" * 64,
        "visibility": {
            "source_affinity_card": True,
            "source_lineage": True,
            "runtime_contract": True,
            "evaluation_artifacts_read": 0,
        },
    }
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def result(commands: list[list[str]], stdout: str = "") -> dict:
    return {
        "runtime_id": "python-fixture",
        "image": "python-fixture@sha256:" + "2" * 64,
        "image_id": "sha256:" + "1" * 64,
        "commands": commands,
        "exit_codes": [0] * len(commands),
        "timed_out": False,
        "stdout": stdout,
        "stdout_sha256": sha256_text(stdout),
        "stderr": "",
        "stderr_sha256": sha256_text(""),
        "duration_ms": 4,
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
    }


def evidence(tmp_path: Path) -> tuple[dict, dict, dict, dict, Path]:
    item = candidate()
    assigned = assignment()
    runtime = runtime_path(tmp_path)
    config = load_preflight_config(CONFIG_PATH)
    lane = config["lanes"]["python"]
    compile_result = result(lane["compile_commands"])
    witness_result = result(lane["witness_commands"], config["success_marker"] + "\n")
    value = build_post_teacher_preflight_evidence(
        item,
        assigned,
        teacher_proof(item, assigned),
        {"reference": deepcopy(compile_result), "known_bad": deepcopy(compile_result)},
        {"reference": deepcopy(witness_result), "known_bad": deepcopy(witness_result)},
        runtime,
        CONFIG_PATH,
    )
    return value, item, assigned, teacher_proof(item, assigned), runtime


def reseal(value: dict) -> None:
    value.pop("evidence_sha256", None)
    value["evidence_sha256"] = canonical_sha256(value)


def test_config_is_sealed_and_has_exact_six_lane_contract() -> None:
    config = load_preflight_config(CONFIG_PATH)
    assert config["plan_sha256"] == PLAN_SHA256
    assert set(config["lanes"]) == set(LANES)
    assert all(row["compile_commands"] and row["witness_commands"] for row in config["lanes"].values())
    assert config["lanes"]["python"]["witness_commands"] == [[
        "python3", "-I", "-c",
        "import runpy, sys; sys.path.insert(0, '/work'); "
        "runpy.run_path('cross_witness.py', run_name='__main__')",
    ]]


def test_accepts_compile_and_cross_witness_passes_for_both_implementations(tmp_path: Path) -> None:
    value, item, assigned, proof, runtime = evidence(tmp_path)

    validated = validate_post_teacher_preflight_evidence(
        item, assigned, proof, value, runtime, CONFIG_PATH,
    )

    assert validated["schema_version"] == EVIDENCE_SCHEMA
    assert set(validated["compile"]) == {"reference", "known_bad"}
    assert set(validated["known_bad_cross_witness"]["results"]) == {"reference", "known_bad"}
    assert validated["visibility"]["known_bad_cross_witness_visible_to_test_author"] is False


def test_executor_stages_witness_only_for_isolated_phase(tmp_path: Path) -> None:
    item = candidate()
    assigned = assignment()
    proof = teacher_proof(item, assigned)
    runtime = runtime_path(tmp_path)
    config = load_preflight_config(CONFIG_PATH)
    calls: list[tuple[list[dict], str, list[list[str]]]] = []

    def fake_executor(task, code, runtime_path_value, commands):
        assert runtime_path_value == runtime
        calls.append((deepcopy(task["files"]), code, deepcopy(commands)))
        stdout = (
            config["success_marker"] + "\n"
            if commands == config["lanes"]["python"]["witness_commands"] else ""
        )
        return result(commands, stdout)

    value = execute_post_teacher_preflight(
        item, assigned, proof, runtime, CONFIG_PATH, fake_executor,
    )

    assert value["schema_version"] == EVIDENCE_SCHEMA
    assert len(calls) == 4
    assert all(not files for files, _, commands in calls if commands == config["lanes"]["python"]["compile_commands"])
    witness_calls = [files for files, _, commands in calls if commands == config["lanes"]["python"]["witness_commands"]]
    assert len(witness_calls) == 2
    assert all([row["path"] for row in files] == ["cross_witness.py"] for files in witness_calls)


def test_preflight_replays_infrastructure_once_with_identical_inputs(tmp_path: Path) -> None:
    item = candidate(); assigned = assignment(); proof = teacher_proof(item, assigned)
    runtime = runtime_path(tmp_path); config = load_preflight_config(CONFIG_PATH)
    calls = []

    def flaky(task, code, runtime_value, commands):
        calls.append((deepcopy(task), code, runtime_value, deepcopy(commands)))
        if len(calls) == 1:
            value = result(commands)
            value.update(timed_out=True, exit_codes=[])
            return value
        stdout = config["success_marker"] + "\n" if commands == config["lanes"]["python"]["witness_commands"] else ""
        return result(commands, stdout)

    value = execute_post_teacher_preflight(
        item, assigned, proof, runtime, CONFIG_PATH, flaky,
    )

    assert len(calls) == 5
    assert calls[0] == calls[1]
    first = value["retry_ledger"]["executions"][0]
    assert [attempt["classification"] for attempt in first["attempts"]] == ["timeout", None]


def test_preflight_semantic_failure_does_not_replay_and_second_infra_is_unresolved(
    tmp_path: Path,
) -> None:
    item = candidate(); assigned = assignment(); proof = teacher_proof(item, assigned)
    runtime = runtime_path(tmp_path); config = load_preflight_config(CONFIG_PATH)
    calls = 0

    def semantic_failure(_task, _code, _runtime, commands):
        nonlocal calls
        calls += 1
        value = result(commands)
        value["exit_codes"] = [1]
        return value

    with pytest.raises(V4PreflightFailure) as semantic_exc:
        execute_post_teacher_preflight(
            item, assigned, proof, runtime, CONFIG_PATH, semantic_failure,
        )
    assert calls == 1
    assert semantic_exc.value.status == "terminal-rejected"
    assert validate_preflight_outcome_evidence(semantic_exc.value.evidence)["status"] == "terminal-rejected"

    calls = 0
    def infrastructure_failure(_task, _code, _runtime, commands):
        nonlocal calls
        calls += 1
        value = result(commands)
        value.update(timed_out=True, exit_codes=[])
        return value

    with pytest.raises(V4PreflightFailure) as infra_exc:
        execute_post_teacher_preflight(
            item, assigned, proof, runtime, CONFIG_PATH, infrastructure_failure,
        )
    assert calls == 2
    assert infra_exc.value.status == "unresolved"
    outcome = validate_preflight_outcome_evidence(infra_exc.value.evidence)
    assert outcome["status"] == "unresolved"
    assert len(outcome["retry_ledger"]["executions"][-1]["attempts"]) == 2
    artifact = {
        "schema_version": V4_ASSEMBLY_SCHEMA, "status": "unresolved",
        "input_sha256": "9" * 64, "candidate_id": item["id"],
        "cell_id": assigned["cell_id"], "terminal_stage": "post_teacher_preflight",
        "reason": str(infra_exc.value),
        "evidence": {"teacher_proof": proof, "post_teacher_preflight": outcome},
        "evaluation_artifacts_read": 0,
    }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    disposition, envelope, measured = validate_assembly_artifact(artifact, CONTRACT_ID)
    assert disposition == "unresolved" and envelope is None and measured["id"] == item["id"]


@pytest.mark.parametrize("implementation", ["reference", "known_bad"])
def test_compile_failure_is_terminal_for_either_implementation(
    tmp_path: Path, implementation: str,
) -> None:
    value, item, assigned, proof, runtime = evidence(tmp_path)
    value["compile"][implementation]["result"]["exit_codes"] = [1]
    reseal(value)

    with pytest.raises(V4PreflightFailure, match="compile_syntax.*did not pass"):
        validate_post_teacher_preflight_evidence(item, assigned, proof, value, runtime, CONFIG_PATH)


@pytest.mark.parametrize("implementation", ["reference", "known_bad"])
def test_witness_requires_both_implementations_to_reach_success_marker(
    tmp_path: Path, implementation: str,
) -> None:
    value, item, assigned, proof, runtime = evidence(tmp_path)
    execution = value["known_bad_cross_witness"]["results"][implementation]["result"]
    execution["stdout"] = ""
    execution["stdout_sha256"] = sha256_text("")
    reseal(value)

    with pytest.raises(V4PreflightFailure, match="known_bad_cross_witness.*did not pass"):
        validate_post_teacher_preflight_evidence(item, assigned, proof, value, runtime, CONFIG_PATH)


def test_witness_accepts_one_harness_prefixed_marker_but_rejects_duplicates(
    tmp_path: Path,
) -> None:
    value, item, assigned, proof, runtime = evidence(tmp_path)
    marker = load_preflight_config(CONFIG_PATH)["success_marker"]
    for implementation in ("reference", "known_bad"):
        execution = value["known_bad_cross_witness"]["results"][implementation]["result"]
        execution["stdout"] = f"test witness ... {marker}\nok\n"
        execution["stdout_sha256"] = sha256_text(execution["stdout"])
        retry_row = next(
            row for row in value["retry_ledger"]["executions"]
            if row["phase"] == "known_bad_cross_witness"
            and row["implementation"] == implementation
        )
        retry_row["attempts"][-1]["result"] = deepcopy(execution)
    value["retry_ledger"].pop("ledger_sha256")
    value["retry_ledger"]["ledger_sha256"] = canonical_sha256(value["retry_ledger"])
    reseal(value)
    assert validate_post_teacher_preflight_evidence(
        item, assigned, proof, value, runtime, CONFIG_PATH,
    ) is value

    execution = value["known_bad_cross_witness"]["results"]["reference"]["result"]
    execution["stdout"] += marker
    execution["stdout_sha256"] = sha256_text(execution["stdout"])
    retry_row = next(
        row for row in value["retry_ledger"]["executions"]
        if row["phase"] == "known_bad_cross_witness"
        and row["implementation"] == "reference"
    )
    retry_row["attempts"][-1]["result"] = deepcopy(execution)
    value["retry_ledger"].pop("ledger_sha256")
    value["retry_ledger"]["ledger_sha256"] = canonical_sha256(value["retry_ledger"])
    reseal(value)
    with pytest.raises(V4PreflightFailure, match="known_bad_cross_witness.*did not pass"):
        validate_post_teacher_preflight_evidence(
            item, assigned, proof, value, runtime, CONFIG_PATH,
        )


def test_command_runtime_candidate_and_unknown_key_drift_fail_closed(tmp_path: Path) -> None:
    value, item, assigned, proof, runtime = evidence(tmp_path)
    changed_command = deepcopy(value)
    changed_command["compile"]["reference"]["result"]["commands"] = [["python3", "solution.py"]]
    reseal(changed_command)
    with pytest.raises(V4PreflightFailure, match="compile_syntax"):
        validate_post_teacher_preflight_evidence(item, assigned, proof, changed_command, runtime, CONFIG_PATH)

    changed_runtime = json.loads(runtime.read_text())
    changed_runtime["runtimes"]["python-fixture"]["manifest_digest"] = "sha256:" + "9" * 64
    runtime.write_text(json.dumps(changed_runtime))
    with pytest.raises(V4PreflightFailure, match="runtime binding"):
        validate_post_teacher_preflight_evidence(item, assigned, proof, value, runtime, CONFIG_PATH)

    value["unexpected"] = True
    reseal(value)
    with pytest.raises(V4PreflightFailure, match="keys differ"):
        validate_post_teacher_preflight_evidence(item, assigned, proof, value, runtime, CONFIG_PATH)


def test_preflight_requires_pre_test_candidate_and_v4_assignment(tmp_path: Path) -> None:
    value, item, assigned, proof, runtime = evidence(tmp_path)
    item["verification_task"]["files"] = [
        {"path": "test_solution.py", "role": "test", "content": "pass\n", "sha256": sha256_text("pass\n")},
    ]
    with pytest.raises(V4PreflightFailure, match="no test files"):
        build_post_teacher_preflight_evidence(
            item, assigned, teacher_proof(item, assigned), {}, {}, runtime, CONFIG_PATH,
        )

    assigned["contract_id"] = "capability-stratified-v3-repair-delta/v1"
    with pytest.raises(V4PreflightFailure, match="V4"):
        validate_post_teacher_preflight_evidence(candidate(), assigned, proof, value, runtime, CONFIG_PATH)


def test_test_author_projection_cannot_expose_preflight_or_witness_material(tmp_path: Path) -> None:
    value, item, assigned, _, _ = evidence(tmp_path)
    projection = author_projection(item, assigned)

    assert set(projection) == {
        "id", "specification", "lane", "embedded_known_bad", "primary_capability",
        "assigned_cross_cutting_dimension", "primary_capability_definition",
    }
    serialized = json.dumps(projection, sort_keys=True)
    assert value["known_bad_cross_witness"]["witness"]["content"] not in serialized
    assert "compile" not in serialized
    assert "witness" not in serialized


def test_v3_proof_and_teacher_witness_drift_are_not_reinterpreted(tmp_path: Path) -> None:
    value, item, assigned, proof, runtime = evidence(tmp_path)
    v3_proof = deepcopy(proof)
    v3_proof["schema_version"] = "ganesh-mini-repair-delta-proof/v1"
    v3_proof.pop("evidence_sha256")
    v3_proof["evidence_sha256"] = canonical_sha256(v3_proof)
    with pytest.raises(V4PreflightFailure, match="V4 teacher proof"):
        validate_post_teacher_preflight_evidence(
            item, assigned, v3_proof, value, runtime, CONFIG_PATH,
        )

    changed_proof = deepcopy(proof)
    changed_proof["known_bad_cross_witness"]["scheduled_dimension_assertion"] = (
        "a different teacher assertion"
    )
    changed_proof.pop("evidence_sha256")
    changed_proof["evidence_sha256"] = canonical_sha256(changed_proof)
    value["teacher_proof_evidence_sha256"] = changed_proof["evidence_sha256"]
    reseal(value)
    with pytest.raises(V4PreflightFailure, match="witness seal mismatch"):
        validate_post_teacher_preflight_evidence(
            item, assigned, changed_proof, value, runtime, CONFIG_PATH,
        )
