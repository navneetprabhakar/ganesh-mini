#!/usr/bin/env python3
"""Run V5 generated-shape interface fixtures through the production preflight."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_v5_interface_fixture_bundle import LANES, SCHEMA
from scripts.data.repair_delta_v5_preflight import (
    CONTRACT_ID, JAVA_CWD_INFRASTRUCTURE_SIGNATURE, PLAN_SHA256,
    CommandExecutor, execute_v5_interface_preflight,
)
from scripts.eval.contracts import sha256_object, sha256_text
from scripts.verify.sandbox import SANDBOX_CONTRACT, verify_commands


REPORT_SCHEMA = "ganesh-mini-v5-interface-fixture-report/v1"
ROOT = Path(__file__).resolve().parents[2]


class ProductionFixtureExecutor:
    """Exercise the Java infrastructure replay once, then use the real sandbox."""

    def __init__(self) -> None:
        self.java_cwd_injected = False

    def __call__(
        self, task: dict[str, Any], code: str, runtime_path: Path,
        commands: list[list[str]],
    ) -> dict[str, Any]:
        if task.get("language") == "java" and not self.java_cwd_injected:
            self.java_cwd_injected = True
            stdout = JAVA_CWD_INFRASTRUCTURE_SIGNATURE + "\n"
            return {
                "commands": copy.deepcopy(commands),
                "exit_codes": [1], "timed_out": False,
                "stdout": stdout, "stdout_sha256": sha256_text(stdout),
                "stderr": "", "stderr_sha256": sha256_text(""),
                "duration_ms": 1,
                "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
            }
        return verify_commands(task, code, runtime_path, commands)


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_v5_interface_fixture_bundle(
    bundle: dict[str, Any], runtime_path: Path, config_path: Path, v4_config_path: Path,
    executor: CommandExecutor,
) -> dict[str, Any]:
    body = dict(bundle); claimed = body.pop("bundle_sha256", None)
    fixtures = bundle.get("fixtures")
    if (
        claimed != canonical_sha256(body)
        or bundle.get("schema_version") != SCHEMA
        or bundle.get("contract_id") != CONTRACT_ID
        or bundle.get("plan_sha256") != PLAN_SHA256
        or not isinstance(fixtures, list) or len(fixtures) != len(LANES)
        or [row.get("lane") for row in fixtures] != list(LANES)
    ):
        raise ValueError("V5 interface fixture bundle is malformed or unsealed")
    results = []
    for row in fixtures:
        evidence = execute_v5_interface_preflight(
            copy.deepcopy(row["candidate"]), copy.deepcopy(row["assignment"]),
            copy.deepcopy(row["teacher_proof"]), runtime_path, config_path,
            v4_config_path, executor,
        )
        retry_rows = evidence["retry_ledger"]["executions"]
        results.append({
            "fixture_id": row["fixture_id"], "lane": row["lane"],
            "status": "passed", "witness_mode": evidence["witness_mode"],
            "attempt_contract": evidence["attempt_contract"],
            "preflight_evidence_sha256": evidence["evidence_sha256"],
            "infrastructure_replays": sum(len(item["attempts"]) == 2 for item in retry_rows),
        })
    report = {
        "schema_version": REPORT_SCHEMA, "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256, "status": "passed",
        "coverage": {
            "lanes": list(LANES), "javascript_dual_artifact": True,
            "rust_binary_main": True, "java_cwd_identical_replay": (
                next(row for row in results if row["lane"] == "java")["infrastructure_replays"] == 1
            ),
            "go_attempt_metadata": next(
                row["attempt_contract"] for row in results if row["lane"] == "go"
            ),
            "negative_contracts": copy.deepcopy(bundle["negative_contracts"]),
        },
        "bindings": {
            "fixture_bundle_sha256": bundle["bundle_sha256"],
            "fixture_builder_sha256": _file_sha256(
                ROOT / "scripts/data/build_v5_interface_fixture_bundle.py"
            ),
            "fixture_runner_sha256": _file_sha256(Path(__file__)),
            "preflight_implementation_sha256": _file_sha256(
                ROOT / "scripts/data/repair_delta_v5_preflight.py"
            ),
            "preflight_config_sha256": _file_sha256(config_path),
            "v4_proof_config_sha256": _file_sha256(v4_config_path),
            "runtime_config_sha256": _file_sha256(runtime_path),
            "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
            "results_sha256": canonical_sha256(results),
        },
        "results": results, "evaluation_artifacts_read": 0,
    }
    if not report["coverage"]["java_cwd_identical_replay"]:
        raise ValueError("V5 Java cwd fixture did not exercise one identical replay")
    report["report_sha256"] = canonical_sha256(report)
    return report


def validate_v5_interface_readiness_report(
    report: Any, bundle: dict[str, Any], runtime_path: Path,
    config_path: Path, v4_config_path: Path,
) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("V5 interface readiness report is missing")
    body = dict(report); claimed = body.pop("report_sha256", None)
    results = report.get("results")
    coverage = report.get("coverage")
    bindings = report.get("bindings")
    expected_bindings = {
        "fixture_bundle_sha256": bundle.get("bundle_sha256"),
        "fixture_builder_sha256": _file_sha256(
            ROOT / "scripts/data/build_v5_interface_fixture_bundle.py"
        ),
        "fixture_runner_sha256": _file_sha256(Path(__file__)),
        "preflight_implementation_sha256": _file_sha256(
            ROOT / "scripts/data/repair_delta_v5_preflight.py"
        ),
        "preflight_config_sha256": _file_sha256(config_path),
        "v4_proof_config_sha256": _file_sha256(v4_config_path),
        "runtime_config_sha256": _file_sha256(runtime_path),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        "results_sha256": canonical_sha256(results),
    }
    if (
        claimed != canonical_sha256(body)
        or report.get("schema_version") != REPORT_SCHEMA
        or report.get("contract_id") != CONTRACT_ID
        or report.get("plan_sha256") != PLAN_SHA256
        or report.get("status") != "passed"
        or report.get("evaluation_artifacts_read") != 0
        or not isinstance(results, list) or len(results) != len(LANES)
        or [row.get("lane") for row in results] != list(LANES)
        or any(row.get("status") != "passed" for row in results)
        or not isinstance(coverage, dict)
        or coverage.get("lanes") != list(LANES)
        or coverage.get("javascript_dual_artifact") is not True
        or coverage.get("rust_binary_main") is not True
        or coverage.get("java_cwd_identical_replay") is not True
        or not isinstance(bindings, dict) or bindings != expected_bindings
    ):
        raise ValueError("V5 interface readiness report is invalid or unbound")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--preflight-config", type=Path, required=True)
    parser.add_argument("--v4-preflight-config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
    report = run_v5_interface_fixture_bundle(
        bundle, args.runtime_config, args.preflight_config,
        args.v4_preflight_config, ProductionFixtureExecutor(),
    )
    validate_v5_interface_readiness_report(
        report, bundle, args.runtime_config, args.preflight_config,
        args.v4_preflight_config,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
