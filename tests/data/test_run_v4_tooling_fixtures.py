from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v4_tooling_fixture_bundle import (
    FAMILY_BY_LANE, LANES, SEPARATION_CONTRACT_SHA256, build_fixture_bundle,
)
from scripts.data.repair_delta_v4_preflight import load_preflight_config
from scripts.data.run_v4_tooling_fixtures import (
    EXPECTED_SUITE_OUTCOMES, FAMILY_DATASETS, REPORT_SCHEMA,
    run_fixture_bundle, validate_tooling_readiness_report,
)
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import SANDBOX_CONTRACT, load_runtime


ROOT = Path(__file__).resolve().parents[2]
RUNTIMES = ROOT / "configs/eval/runtimes.json"
PREFLIGHT = ROOT / "configs/data/gate2_v4_post_teacher_preflight.json"
ADMISSION = ROOT / "configs/data/expansion_v1.json"
LANE_SHAPES = {
    "go": ("func ComputeTotal", "errors.New", "func TestKnownBadCrossWitness", "fmt.Println"),
    "java": ("static int computeTotal", "IllegalArgumentException", "class CrossWitness", "System.out.println"),
    "javascript": ("function computeTotal", "TypeError", 'require("./solution")', "console.log"),
    "typescript": ("function computeTotal", "TypeError", 'from "./solution"', "console.log"),
    "python": ("def compute_total", "ValueError", "from solution import compute_total", "print("),
    "rust": ("fn compute_total", "values.is_empty()", "mod solution", "println!"),
}


class InjectedExecutors:
    def __init__(self) -> None:
        self.preflight_calls = 0
        self.suite_calls = 0
        self.marker = load_preflight_config(PREFLIGHT)["success_marker"]

    def preflight(self, task: dict, code: str, runtime_path: Path, commands: list[list[str]]) -> dict:
        self.preflight_calls += 1
        runtime = load_runtime(runtime_path, task["runtime_id"], task["language"], task["candidate_path"])
        stdout = self.marker + "\n"
        return {
            "runtime_id": task["runtime_id"],
            "image": f"{runtime['image'].rsplit(':', 1)[0]}@{runtime['manifest_digest']}",
            "image_id": runtime["image_id"], "commands": commands,
            "exit_codes": [0] * len(commands), "timed_out": False,
            "stdout": stdout, "stdout_sha256": sha256_text(stdout),
            "stderr": "", "stderr_sha256": sha256_text(""), "duration_ms": 1,
            "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        }

    def suite(self, task: dict, code: str, runtime_path: Path) -> dict:
        self.suite_calls += 1
        runtime = load_runtime(runtime_path, task["runtime_id"], task["language"], task["candidate_path"])
        test_content = "\n".join(item["content"] for item in task["files"] if item["role"] == "test")
        known_bad = any(token in code for token in ("maximum", "Math.max", ".max()", "max(values)"))
        primary = any(token in test_content for token in ("Primary", "primary", "[2, 3]", "{2, 3}"))
        passed = not (known_bad and primary)
        return {
            "runtime_id": task["runtime_id"],
            "image": f"{runtime['image'].rsplit(':', 1)[0]}@{runtime['manifest_digest']}",
            "image_id": runtime["image_id"], "commands": runtime["commands"],
            "exit_codes": [0 if passed else 1], "timed_out": False,
            "stdout": "", "stdout_sha256": sha256_text(""),
            "stderr": "", "stderr_sha256": sha256_text(""), "duration_ms": 1,
            "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        }


def _run() -> tuple[dict, InjectedExecutors]:
    executors = InjectedExecutors()
    report = run_fixture_bundle(
        build_fixture_bundle(), ADMISSION, RUNTIMES, PREFLIGHT,
        SEPARATION_CONTRACT_SHA256, preflight_executor=executors.preflight,
        suite_executor=executors.suite,
    )
    return report, executors


def test_default_bundle_has_executable_six_lane_shapes() -> None:
    bundle = build_fixture_bundle()
    positives = [row for row in bundle["fixtures"] if row["expected"] == "admitted"]
    negatives = [row for row in bundle["fixtures"] if row["expected"] == "broken-staging-rejected"]
    assert len(positives) == 6 and len(negatives) == 1
    assert {row["envelope"]["candidate"]["lane"] for row in positives} == set(LANES)
    assert {row["provenance_family"] for row in positives} == set(FAMILY_DATASETS)
    marker = load_preflight_config(PREFLIGHT)["success_marker"]
    for row in positives:
        lane = row["envelope"]["candidate"]["lane"]
        assert row["provenance_family"] == FAMILY_BY_LANE[lane]
        task = row["envelope"]["candidate"]["verification_task"]
        assert task["limits"]["timeout_seconds"] == (120 if lane == "go" else 30)
        reference = task["validation"]["reference"]["code"]
        known_bad = task["validation"]["known_bad"][0]["code"]
        tests = [item for item in task["files"] if item["role"] == "test"]
        roles = row["envelope"]["evidence"]["test_author"]["test_roles"]
        witness = row["envelope"]["evidence"]["teacher_proof"]["known_bad_cross_witness"]
        assert reference.strip() and known_bad.strip() and reference != known_bad
        assert not any(placeholder in reference + known_bad + witness["content"] for placeholder in (
            "// REFERENCE", "// KNOWN_BAD", "fixture witness",
        ))
        assert any(token in reference for token in ("total +=", "reduce", ".sum()", "sum(values)", "iter().sum()"))
        assert any(token in known_bad for token in ("maximum", "Math.max", "max(values)", ".max()"))
        function_token, rejection_token, witness_entry_token, print_token = LANE_SHAPES[lane]
        assert function_token in reference and function_token in known_bad
        assert rejection_token in reference and rejection_token in known_bad
        assert witness_entry_token in witness["content"] and print_token in witness["content"]
        assert len(tests) == 2 and {item["path"] for item in tests} == {role["path"] for role in roles}
        primary = next(role for role in roles if role["role"] == "primary_discrimination")
        cross = next(role for role in roles if role["role"] == "cross_cutting")
        assert len(primary["case_ids"]) >= 2 and cross["case_ids"]
        assert marker in witness["content"] and witness["content"].count(marker) == 1
        assert "empty" in witness["content"].lower() or "[]" in witness["content"]
        if lane == "go":
            assert any(item["path"] == "go.mod" and item["role"] == "support" for item in task["files"])
        assert all(item["sha256"] == sha256_text(item["content"]) for item in task["files"])


def test_sealed_fixture_runner_covers_contract_and_terminal_summary() -> None:
    report, executors = _run()
    assert report["schema_version"] == REPORT_SCHEMA and report["status"] == "passed"
    assert report["coverage"]["lanes"] == list(LANES)
    assert set(report["coverage"]["provenance_families"]) == set(FAMILY_DATASETS)
    assert report["terminal_summary"] == {
        "terminal": True, "purpose": "production-tooling-fixture-validation-only",
        "qualification_candidates_admitted": 0, "training_records_emitted": 0,
        "publication_decision": "not-applicable",
    }
    assert executors.preflight_calls == 24 and executors.suite_calls == 24
    assert [row["status"] for row in report["results"]].count("admitted") == 6
    assert report["results"][-1]["status"] == "expected-staging-rejection"
    assert report["results"][-1]["execution_attempted"] is False
    assert all(row["suite_outcomes"] == EXPECTED_SUITE_OUTCOMES for row in report["results"][:6])
    body = dict(report); claimed = body.pop("report_sha256")
    assert claimed == canonical_sha256(body)
    assert report["bindings"]["output_records_sha256"] == canonical_sha256(report["results"])
    validate_tooling_readiness_report(report, ADMISSION, RUNTIMES, PREFLIGHT)


def test_fixture_runner_fails_closed_before_execution_on_coverage_error() -> None:
    bundle = build_fixture_bundle()
    bundle["fixtures"] = bundle["fixtures"][:-2] + [bundle["fixtures"][-1]]
    executors = InjectedExecutors()
    with pytest.raises(ValueError, match="six admitted fixtures"):
        run_fixture_bundle(
            bundle, ADMISSION, RUNTIMES, PREFLIGHT, SEPARATION_CONTRACT_SHA256,
            preflight_executor=executors.preflight, suite_executor=executors.suite,
        )
    assert executors.preflight_calls == executors.suite_calls == 0


def test_tooling_readiness_validator_rejects_tampered_hash_and_coverage() -> None:
    report, _ = _run()
    tampered = copy.deepcopy(report)
    tampered["coverage"]["admitted"] = 5
    tampered.pop("report_sha256")
    tampered["report_sha256"] = canonical_sha256(tampered)
    with pytest.raises(ValueError, match="coverage"):
        validate_tooling_readiness_report(tampered, ADMISSION, RUNTIMES, PREFLIGHT)

    tampered = copy.deepcopy(report)
    tampered["bindings"]["runtime_config_sha256"] = "0" * 64
    tampered.pop("report_sha256")
    tampered["report_sha256"] = canonical_sha256(tampered)
    with pytest.raises(ValueError, match="bound hashes"):
        validate_tooling_readiness_report(tampered, ADMISSION, RUNTIMES, PREFLIGHT)
