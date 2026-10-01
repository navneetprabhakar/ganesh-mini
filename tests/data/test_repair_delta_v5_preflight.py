from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v5_interface_fixture_bundle import build_v5_interface_fixture_bundle
from scripts.data.repair_delta_v5_preflight import (
    GO_ATTEMPT_CONTRACT, JAVA_CWD_INFRASTRUCTURE_SIGNATURE, PLAN_SHA256,
    V5PreflightFailure, execute_v5_interface_preflight, load_v5_preflight_config,
)
from scripts.data.run_v5_interface_fixtures import (
    run_v5_interface_fixture_bundle, validate_v5_interface_readiness_report,
)
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import SANDBOX_CONTRACT, load_runtime


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configs/data/gate2_v5_interface_preflight.json"
V4_CONFIG = ROOT / "configs/data/gate2_v4_post_teacher_preflight.json"
RUNTIMES = ROOT / "configs/eval/runtimes.json"


class FixtureExecutor:
    def __init__(self, *, omit_marker: bool = False) -> None:
        self.calls: list[dict] = []
        self.java_cwd_injected = False
        self.omit_marker = omit_marker
        self.marker = load_v5_preflight_config(CONFIG)["success_marker"]

    def __call__(self, task, code, runtime_path, commands):
        snapshot = {"task": copy.deepcopy(task), "code": code, "commands": copy.deepcopy(commands)}
        self.calls.append(snapshot)
        runtime = load_runtime(runtime_path, task["runtime_id"], task["language"], task["candidate_path"])
        witness = any(item.get("path", "").lower().startswith("crosswitness")
                      or "cross_witness" in item.get("path", "") for item in task["files"])
        stdout = ""
        exit_codes = [0] * len(commands)
        if task["language"] == "java" and witness and not self.java_cwd_injected:
            self.java_cwd_injected = True
            stdout = "Error occurred during initialization of VM\njava.lang.Error: " + JAVA_CWD_INFRASTRUCTURE_SIGNATURE
            exit_codes = [0, 1]
        elif witness and not self.omit_marker:
            stdout = self.marker + "\n"
        return {
            "runtime_id": task["runtime_id"],
            "image": f"{runtime['image'].rsplit(':', 1)[0]}@{runtime['manifest_digest']}",
            "image_id": runtime["image_id"], "commands": commands,
            "exit_codes": exit_codes, "timed_out": False,
            "stdout": stdout, "stdout_sha256": sha256_text(stdout),
            "stderr": "", "stderr_sha256": sha256_text(""), "duration_ms": 1,
            "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        }


def fixture(lane: str) -> dict:
    return next(row for row in build_v5_interface_fixture_bundle()["fixtures"] if row["lane"] == lane)


def test_v5_config_is_sealed_and_resolves_go_attempt_semantics() -> None:
    config = load_v5_preflight_config(CONFIG)
    assert config["plan_sha256"] == PLAN_SHA256
    assert config["go_attempt_contract"] == GO_ATTEMPT_CONTRACT
    assert GO_ATTEMPT_CONTRACT["aggregate_candidate_timeout_seconds"] is None
    assert GO_ATTEMPT_CONTRACT["final_matrix_seconds_without_replay"] == 480
    assert GO_ATTEMPT_CONTRACT["final_matrix_seconds_with_four_replays"] == 960
    assert config["lanes"]["javascript"]["witness_mode"] == "dual-immutable-artifact"
    assert config["lanes"]["rust"]["witness_mode"] == "binary-main-per-implementation"
    assert all("--test" not in command for command in config["lanes"]["rust"]["witness_commands"])


def test_javascript_dual_artifact_stages_both_immutable_sources_once() -> None:
    row = fixture("javascript"); executor = FixtureExecutor()
    evidence = execute_v5_interface_preflight(
        row["candidate"], row["assignment"], row["teacher_proof"],
        RUNTIMES, CONFIG, V4_CONFIG, executor,
    )
    witness_calls = [call for call in executor.calls if any(
        item["path"] == "cross_witness.js" for item in call["task"]["files"]
    )]
    assert len(witness_calls) == 1
    files = {item["path"]: item for item in witness_calls[0]["task"]["files"]}
    assert {"reference.js", "known_bad.js", "cross_witness.js"} <= set(files)
    validation = row["candidate"]["verification_task"]["validation"]
    assert files["reference.js"]["sha256"] == validation["reference"]["sha256"]
    assert files["known_bad.js"]["sha256"] == validation["known_bad"][0]["sha256"]
    assert set(evidence["witness_results"]) == {"reference+known_bad"}
    assert len(evidence["retry_ledger"]["executions"]) == 3


def test_rust_generated_fn_main_uses_binary_commands_for_each_implementation() -> None:
    row = fixture("rust"); executor = FixtureExecutor()
    evidence = execute_v5_interface_preflight(
        row["candidate"], row["assignment"], row["teacher_proof"],
        RUNTIMES, CONFIG, V4_CONFIG, executor,
    )
    witness_calls = [call for call in executor.calls if any(
        item["path"] == "cross_witness.rs" for item in call["task"]["files"]
    )]
    assert len(witness_calls) == 2
    assert all("--test" not in {part for command in call["commands"] for part in command}
               for call in witness_calls)
    assert "fn main()" in row["teacher_proof"]["known_bad_cross_witness"]["content"]
    assert set(evidence["witness_results"]) == {"reference", "known_bad"}


def test_java_cwd_signature_gets_one_byte_identical_replay() -> None:
    row = fixture("java"); executor = FixtureExecutor()
    evidence = execute_v5_interface_preflight(
        row["candidate"], row["assignment"], row["teacher_proof"],
        RUNTIMES, CONFIG, V4_CONFIG, executor,
    )
    replayed = [item for item in evidence["retry_ledger"]["executions"] if len(item["attempts"]) == 2]
    assert len(replayed) == 1
    attempts = replayed[0]["attempts"]
    assert [item["classification"] for item in attempts] == ["java-cwd-infrastructure", None]
    assert attempts[0]["input_binding"] == attempts[1]["input_binding"] == replayed[0]["input_binding"]


def test_go_wrong_attempt_limit_rejects_before_executor() -> None:
    row = fixture("go"); row["candidate"]["verification_task"]["limits"]["timeout_seconds"] = 119
    executor = FixtureExecutor()
    with pytest.raises(V5PreflightFailure, match="120 seconds"):
        execute_v5_interface_preflight(
            row["candidate"], row["assignment"], row["teacher_proof"],
            RUNTIMES, CONFIG, V4_CONFIG, executor,
        )
    assert executor.calls == []


def test_missing_marker_is_terminal_without_infrastructure_replay() -> None:
    row = fixture("rust"); executor = FixtureExecutor(omit_marker=True)
    with pytest.raises(V5PreflightFailure, match="execution did not pass") as caught:
        execute_v5_interface_preflight(
            row["candidate"], row["assignment"], row["teacher_proof"],
            RUNTIMES, CONFIG, V4_CONFIG, executor,
        )
    assert caught.value.status == "terminal-rejected"
    witness_calls = [call for call in executor.calls if any(
        item["path"] == "cross_witness.rs" for item in call["task"]["files"]
    )]
    assert len(witness_calls) == 1


def test_rust_test_harness_command_is_rejected_by_sealed_config(tmp_path: Path) -> None:
    value = json.loads(CONFIG.read_text())
    value["lanes"]["rust"]["witness_commands"][0].insert(1, "--test")
    value.pop("config_sha256")
    value["config_sha256"] = canonical_sha256(value)
    path = tmp_path / "bad.json"; path.write_text(json.dumps(value))
    with pytest.raises(V5PreflightFailure, match="must not use rustc --test"):
        load_v5_preflight_config(path)


def test_production_path_fixture_report_covers_modes_replay_and_go_metadata() -> None:
    bundle = build_v5_interface_fixture_bundle(); executor = FixtureExecutor()
    report = run_v5_interface_fixture_bundle(bundle, RUNTIMES, CONFIG, V4_CONFIG, executor)
    assert report["status"] == "passed"
    assert report["coverage"]["javascript_dual_artifact"] is True
    assert report["coverage"]["rust_binary_main"] is True
    assert report["coverage"]["java_cwd_identical_replay"] is True
    assert report["coverage"]["go_attempt_metadata"] == GO_ATTEMPT_CONTRACT
    body = dict(report); claimed = body.pop("report_sha256")
    assert claimed == canonical_sha256(body)
    assert validate_v5_interface_readiness_report(
        report, bundle, RUNTIMES, CONFIG, V4_CONFIG,
    ) is report

    tampered = copy.deepcopy(report)
    tampered["bindings"]["runtime_config_sha256"] = "0" * 64
    tampered.pop("report_sha256")
    tampered["report_sha256"] = canonical_sha256(tampered)
    with pytest.raises(ValueError, match="invalid or unbound"):
        validate_v5_interface_readiness_report(
            tampered, bundle, RUNTIMES, CONFIG, V4_CONFIG,
        )
