#!/usr/bin/env python3
"""Execute and seal the bounded V4 tooling-contract fixture suite.

The command-line path deliberately uses the production Docker-backed
executors.  ``run_fixture_bundle`` accepts executor arguments solely so unit
tests can exercise the complete evidence and admission path without Docker.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_expansion import AdmissionFailure, canonical_json  # noqa: E402
from scripts.data.admit_repair_delta import (  # noqa: E402
    V4_CONTRACT_ID,
    V4_ENVELOPE_SCHEMA,
    stage_role_suite,
    validate_envelope,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.data.repair_delta_v4_preflight import (  # noqa: E402
    PLAN_SHA256,
    V4PreflightFailure,
    execute_post_teacher_preflight,
)
from scripts.data.run_repair_delta_evidence import _executable_evidence, seal  # noqa: E402
from scripts.eval.contracts import sha256_object  # noqa: E402
from scripts.verify.sandbox import (  # noqa: E402
    SANDBOX_CONTRACT,
    load_runtime,
    verify,
    verify_commands,
)


SCHEMA = "ganesh-mini-v4-tooling-fixture-bundle/v1"
REPORT_SCHEMA = "ganesh-mini-v4-tooling-fixture-report/v1"
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
FAMILY_DATASETS = {
    "mceval": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "mdeval": "m-a-p/MdEval-Instruct",
    "commitpackft": "bigcode/commitpackft",
}
EXPECTED_SUITE_OUTCOMES = {
    "reference.primary_discrimination": "pass",
    "reference.cross_cutting": "pass",
    "known_bad.primary_discrimination": "fail",
    "known_bad.cross_cutting": "pass",
}

PreflightExecutor = Callable[[dict[str, Any], str, Path, list[list[str]]], dict[str, Any]]
SuiteExecutor = Callable[[dict[str, Any], str, Path], dict[str, Any]]


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path, where: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{where}: unreadable JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{where}: expected a JSON object")
    return value


def _family(candidate: dict[str, Any]) -> str:
    dataset = candidate.get("source", {}).get("dataset")
    matches = [name for name, expected in FAMILY_DATASETS.items() if dataset == expected]
    if len(matches) != 1:
        raise ValueError(f"candidate source dataset is not a frozen V4 provenance family: {dataset!r}")
    return matches[0]


def _suite_outcomes(executable: dict[str, Any]) -> dict[str, str]:
    outcomes: dict[str, str] = {}
    for implementation in ("reference", "known_bad"):
        for role in ("primary_discrimination", "cross_cutting"):
            result = executable["results"][implementation][role]
            exits = result.get("exit_codes")
            if not isinstance(exits, list) or not exits:
                raise ValueError(f"{implementation}.{role}: missing executable exit codes")
            outcomes[f"{implementation}.{role}"] = (
                "pass" if all(code == 0 for code in exits) else "fail"
            )
    if outcomes != EXPECTED_SUITE_OUTCOMES:
        raise ValueError(f"four-suite fixture outcome mismatch: {outcomes!r}")
    return outcomes


def _lineage(
    candidate: dict[str, Any], assignment: dict[str, Any], evidence: dict[str, Any],
) -> dict[str, Any]:
    source = candidate["source"]
    return seal({
        "candidate_sha256": canonical_sha256(candidate),
        "contract_id": V4_CONTRACT_ID,
        "cell_id": assignment["cell_id"],
        "source_identity": {
            key: source[key] for key in ("dataset", "revision", "record_id")
        },
        "source_record_sha256": source["source_record_sha256"],
        "complete": True,
        "teacher_proof_evidence_sha256": evidence["teacher_proof"]["evidence_sha256"],
        "post_teacher_preflight_evidence_sha256": evidence["post_teacher_preflight"]["evidence_sha256"],
        "semantic_review_evidence_sha256": evidence["semantic_review"]["evidence_sha256"],
        "test_author_evidence_sha256": evidence["test_author"]["evidence_sha256"],
        "delta_audit_evidence_sha256": evidence["delta_audit"]["evidence_sha256"],
        "separation_evidence_sha256": evidence["separation"]["evidence_sha256"],
        "executable_evidence_sha256": evidence["executable"]["evidence_sha256"],
    })


def _runtime_binding(runtime_path: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    task = candidate["verification_task"]
    runtime = load_runtime(runtime_path, task["runtime_id"], candidate["lane"], task["candidate_path"])
    return {
        "runtime_id": task["runtime_id"],
        "image": runtime["image"],
        "image_id": runtime["image_id"],
        "manifest_digest": runtime["manifest_digest"],
        "rootfs_layers_sha256": canonical_sha256(runtime["rootfs_layers"]),
        "commands_sha256": canonical_sha256(runtime["commands"]),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
    }


def _positive(
    fixture: dict[str, Any], admission_config: dict[str, Any], runtime_path: Path,
    preflight_path: Path, separation_contract_sha256: str,
    preflight_executor: PreflightExecutor, suite_executor: SuiteExecutor,
) -> dict[str, Any]:
    envelope = copy.deepcopy(fixture["envelope"])
    if envelope.get("schema_version") != V4_ENVELOPE_SCHEMA:
        raise ValueError("positive fixture must contain an exact V4 envelope")
    candidate = envelope["candidate"]
    assignment = envelope["assignment"]
    family = _family(candidate)
    if fixture.get("provenance_family") != family:
        raise ValueError("fixture provenance_family does not match source.dataset")

    evidence = envelope.get("evidence")
    required_core = {"teacher_proof", "semantic_review", "test_author", "delta_audit", "separation"}
    if not isinstance(evidence, dict) or set(evidence) != required_core:
        raise ValueError("fixture envelope must contain exactly the five pre-execution evidence objects")
    pretest = copy.deepcopy(candidate)
    pretest["verification_task"]["files"] = [
        item for item in pretest["verification_task"]["files"] if item.get("role") != "test"
    ]
    try:
        preflight = execute_post_teacher_preflight(
            pretest, assignment, evidence["teacher_proof"], runtime_path, preflight_path,
            executor=preflight_executor,
        )
    except V4PreflightFailure as exc:
        raise ValueError(
            f"{fixture['fixture_id']}: V4 preflight {exc.status}: {exc}; "
            f"evidence={json.dumps(exc.evidence, sort_keys=True)}"
        ) from exc
    executable, retry_ledger = _executable_evidence(
        candidate, evidence["test_author"], runtime_path, suite_executor,
    )
    if retry_ledger.get("unresolved") is not False:
        raise ValueError(
            f"{fixture['fixture_id']}: fixture executable evidence remained unresolved: "
            f"{json.dumps(retry_ledger, sort_keys=True)}"
        )
    outcomes = _suite_outcomes(executable)
    evidence["post_teacher_preflight"] = preflight
    evidence["executable"] = executable
    evidence["lineage"] = _lineage(candidate, assignment, evidence)
    admitted = validate_envelope(
        envelope, admission_config, runtime_path, separation_contract_sha256,
        contract_id=V4_CONTRACT_ID, v4_preflight_config=preflight_path,
    )
    return {
        "fixture_id": fixture["fixture_id"],
        "status": "admitted",
        "lane": candidate["lane"],
        "provenance_family": family,
        "candidate_sha256": canonical_sha256(candidate),
        "preflight_evidence_sha256": preflight["evidence_sha256"],
        "executable_evidence_sha256": executable["evidence_sha256"],
        "retry_ledger_sha256": retry_ledger["ledger_sha256"],
        "suite_outcomes": outcomes,
        "admitted_output_sha256": canonical_sha256(admitted),
        "runtime_binding": _runtime_binding(runtime_path, candidate),
    }


def _broken_staging(fixture: dict[str, Any], runtime_path: Path) -> dict[str, Any]:
    envelope = fixture.get("envelope")
    if not isinstance(envelope, dict):
        raise ValueError("broken-staging fixture lacks an envelope")
    candidate = envelope.get("candidate")
    evidence = envelope.get("evidence")
    roles = evidence.get("test_author", {}).get("test_roles") if isinstance(evidence, dict) else None
    mutation = fixture.get("broken_staging")
    if not isinstance(candidate, dict) or not isinstance(roles, list) or not isinstance(mutation, dict):
        raise ValueError("broken-staging fixture is malformed")
    if set(mutation) != {"role", "canonical_path"} or mutation["role"] not in {
        "primary_discrimination", "cross_cutting",
    }:
        raise ValueError("broken_staging mutation differs from the fixed contract")
    selected = [row for row in roles if row.get("role") == mutation["role"]]
    if len(selected) != 1:
        raise ValueError("broken-staging role is not unique")
    role = copy.deepcopy(selected[0])
    role["canonical_path"] = mutation["canonical_path"]
    task = candidate["verification_task"]
    runtime = load_runtime(runtime_path, task["runtime_id"], candidate["lane"], task["candidate_path"])
    family = _family(candidate)
    if fixture.get("provenance_family") != family:
        raise ValueError("fixture provenance_family does not match source.dataset")
    try:
        stage_role_suite(candidate, role, runtime)
    except AdmissionFailure as exc:
        reason = str(exc)
    else:
        raise ValueError("broken-staging fixture unexpectedly reached execution")
    if "canonical path" not in reason:
        raise ValueError(f"broken-staging fixture failed for the wrong reason: {reason}")
    return {
        "fixture_id": fixture["fixture_id"],
        "status": "expected-staging-rejection",
        "lane": candidate["lane"],
        "provenance_family": family,
        "reason": reason,
        "execution_attempted": False,
        "candidate_sha256": canonical_sha256(candidate),
        "runtime_binding": _runtime_binding(runtime_path, candidate),
    }


def run_fixture_bundle(
    bundle: dict[str, Any], admission_config_path: Path, runtime_path: Path,
    preflight_path: Path, separation_contract_sha256: str,
    *, preflight_executor: PreflightExecutor = verify_commands,
    suite_executor: SuiteExecutor = verify,
    fixture_input_sha256: str | None = None,
) -> dict[str, Any]:
    """Run the six-lane positive suite and one pre-execution staging negative."""
    if not isinstance(bundle, dict) or set(bundle) != {
        "schema_version", "contract_id", "plan_sha256", "fixtures",
    }:
        raise ValueError("fixture bundle keys differ from the sealed tooling contract")
    if (
        bundle["schema_version"] != SCHEMA
        or bundle["contract_id"] != V4_CONTRACT_ID
        or bundle["plan_sha256"] != PLAN_SHA256
        or not isinstance(bundle["fixtures"], list)
    ):
        raise ValueError("fixture bundle identity is invalid")
    fixtures = bundle["fixtures"]
    positives = [row for row in fixtures if row.get("expected") == "admitted"]
    negatives = [row for row in fixtures if row.get("expected") == "broken-staging-rejected"]
    if len(positives) != 6 or len(negatives) != 1 or len(fixtures) != 7:
        raise ValueError("fixture bundle requires six admitted fixtures and one broken-staging negative")
    if len({row.get("fixture_id") for row in fixtures}) != 7:
        raise ValueError("fixture IDs must be unique")
    for row in positives:
        if not isinstance(row, dict) or set(row) != {
            "fixture_id", "provenance_family", "expected", "envelope",
        }:
            raise ValueError("positive fixture keys differ from the fixed contract")
    if not isinstance(negatives[0], dict) or set(negatives[0]) != {
        "fixture_id", "provenance_family", "expected", "envelope", "broken_staging",
    }:
        raise ValueError("broken-staging fixture keys differ from the fixed contract")
    lanes = [row.get("envelope", {}).get("candidate", {}).get("lane") for row in positives]
    if set(lanes) != set(LANES) or len(lanes) != len(set(lanes)):
        raise ValueError("positive fixtures must cover every lane exactly once")
    families = {_family(row["envelope"]["candidate"]) for row in positives}
    if families != set(FAMILY_DATASETS):
        raise ValueError("positive fixtures must cover McEval, MdEval, and CommitPackFT")
    if any(row.get("provenance_family") != _family(row["envelope"]["candidate"]) for row in fixtures):
        raise ValueError("fixture provenance_family does not match source.dataset")

    admission_config = _load_json(admission_config_path, "admission config")
    results = [
        _positive(
            row, admission_config, runtime_path, preflight_path,
            separation_contract_sha256, preflight_executor, suite_executor,
        )
        for row in sorted(positives, key=lambda item: LANES.index(item["envelope"]["candidate"]["lane"]))
    ]
    results.append(_broken_staging(negatives[0], runtime_path))
    result_sha = canonical_sha256(results)
    bindings = {
        "runner_code_sha256": _file_sha256(Path(__file__)),
        "fixture_builder_sha256": _file_sha256(ROOT / "scripts/data/build_v4_tooling_fixture_bundle.py"),
        "fixture_input_sha256": fixture_input_sha256 or canonical_sha256(bundle),
        "admission_config_sha256": _file_sha256(admission_config_path),
        "runtime_config_sha256": _file_sha256(runtime_path),
        "preflight_config_sha256": _file_sha256(preflight_path),
        "preflight_validator_sha256": _file_sha256(ROOT / "scripts/data/repair_delta_v4_preflight.py"),
        "final_validator_sha256": _file_sha256(ROOT / "scripts/data/admit_repair_delta.py"),
        "evidence_builder_sha256": _file_sha256(ROOT / "scripts/data/run_repair_delta_evidence.py"),
        "two_phase_controller_sha256": _file_sha256(ROOT / "scripts/data/run_repair_delta_two_phase.py"),
        "sandbox_implementation_sha256": _file_sha256(ROOT / "scripts/verify/sandbox.py"),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        "output_records_sha256": result_sha,
    }
    report = {
        "schema_version": REPORT_SCHEMA,
        "contract_id": V4_CONTRACT_ID,
        "plan_sha256": PLAN_SHA256,
        "status": "passed",
        "coverage": {
            "lanes": list(LANES),
            "provenance_families": sorted(FAMILY_DATASETS),
            "admitted": 6,
            "expected_staging_rejections": 1,
            "four_suite_outcome_contract": dict(EXPECTED_SUITE_OUTCOMES),
        },
        "terminal_summary": {
            "terminal": True,
            "purpose": "production-tooling-fixture-validation-only",
            "qualification_candidates_admitted": 0,
            "training_records_emitted": 0,
            "publication_decision": "not-applicable",
        },
        "bindings": bindings,
        "results": results,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def validate_tooling_readiness_report(
    report: Any, admission_config_path: Path, runtime_path: Path,
    preflight_path: Path, fixture_path: Path | None = None,
) -> dict[str, Any]:
    """Fail closed unless a report proves the exact production tooling fixture gate.

    This is the generation-gate entry point.  With no ``fixture_path`` it binds
    the deterministic default builder output; callers using an explicit fixture
    file must provide that same path so its byte hash can be checked.
    """
    expected_top = {
        "schema_version", "contract_id", "plan_sha256", "status", "coverage",
        "terminal_summary", "bindings", "results", "evaluation_artifacts_read",
        "report_sha256",
    }
    if not isinstance(report, dict) or set(report) != expected_top:
        raise ValueError("tooling readiness report keys differ from the fixed contract")
    body = dict(report)
    claimed = body.pop("report_sha256")
    if claimed != canonical_sha256(body):
        raise ValueError("tooling readiness report seal mismatch")
    if (
        report["schema_version"] != REPORT_SCHEMA
        or report["contract_id"] != V4_CONTRACT_ID
        or report["plan_sha256"] != PLAN_SHA256
        or report["status"] != "passed"
        or report["evaluation_artifacts_read"] != 0
    ):
        raise ValueError("tooling readiness report identity or pass status mismatch")
    expected_coverage = {
        "lanes": list(LANES),
        "provenance_families": sorted(FAMILY_DATASETS),
        "admitted": 6,
        "expected_staging_rejections": 1,
        "four_suite_outcome_contract": dict(EXPECTED_SUITE_OUTCOMES),
    }
    if report["coverage"] != expected_coverage:
        raise ValueError("tooling readiness coverage differs from the fixed gate")
    expected_terminal = {
        "terminal": True,
        "purpose": "production-tooling-fixture-validation-only",
        "qualification_candidates_admitted": 0,
        "training_records_emitted": 0,
        "publication_decision": "not-applicable",
    }
    if report["terminal_summary"] != expected_terminal:
        raise ValueError("tooling readiness report is not a terminal fixture summary")

    if fixture_path is None:
        from scripts.data.build_v4_tooling_fixture_bundle import build_fixture_bundle
        fixture_bundle = build_fixture_bundle(admission_config_path, preflight_path)
        fixture_hash = canonical_sha256(fixture_bundle)
    else:
        fixture_bytes = fixture_path.read_bytes()
        fixture_hash = hashlib.sha256(fixture_bytes).hexdigest()
        fixture_bundle = json.loads(fixture_bytes)
    expected_bindings = {
        "runner_code_sha256": _file_sha256(Path(__file__)),
        "fixture_builder_sha256": _file_sha256(ROOT / "scripts/data/build_v4_tooling_fixture_bundle.py"),
        "fixture_input_sha256": fixture_hash,
        "admission_config_sha256": _file_sha256(admission_config_path),
        "runtime_config_sha256": _file_sha256(runtime_path),
        "preflight_config_sha256": _file_sha256(preflight_path),
        "preflight_validator_sha256": _file_sha256(ROOT / "scripts/data/repair_delta_v4_preflight.py"),
        "final_validator_sha256": _file_sha256(ROOT / "scripts/data/admit_repair_delta.py"),
        "evidence_builder_sha256": _file_sha256(ROOT / "scripts/data/run_repair_delta_evidence.py"),
        "two_phase_controller_sha256": _file_sha256(ROOT / "scripts/data/run_repair_delta_two_phase.py"),
        "sandbox_implementation_sha256": _file_sha256(ROOT / "scripts/verify/sandbox.py"),
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        "output_records_sha256": canonical_sha256(report["results"]),
    }
    if report["bindings"] != expected_bindings:
        raise ValueError("tooling readiness bound hashes differ from current code/config/runtime")

    results = report["results"]
    if not isinstance(results, list) or len(results) != 7:
        raise ValueError("tooling readiness result count differs from the fixed gate")
    positives = [row for row in results if row.get("status") == "admitted"]
    negatives = [row for row in results if row.get("status") == "expected-staging-rejection"]
    if (
        len(positives) != 6 or len(negatives) != 1
        or {row.get("lane") for row in positives} != set(LANES)
        or {row.get("provenance_family") for row in positives} != set(FAMILY_DATASETS)
        or any(row.get("suite_outcomes") != EXPECTED_SUITE_OUTCOMES for row in positives)
        or negatives[0].get("execution_attempted") is not False
    ):
        raise ValueError("tooling readiness result coverage or four-suite pass contract failed")
    fixture_rows = fixture_bundle.get("fixtures") if isinstance(fixture_bundle, dict) else None
    if not isinstance(fixture_rows, list) or len(fixture_rows) != 7:
        raise ValueError("tooling readiness fixture input no longer has exact coverage")
    fixture_by_id = {row.get("fixture_id"): row for row in fixture_rows if isinstance(row, dict)}
    if len(fixture_by_id) != 7 or {row.get("fixture_id") for row in results} != set(fixture_by_id):
        raise ValueError("tooling readiness results do not bind every fixture identity")
    for row in results:
        fixture = fixture_by_id[row["fixture_id"]]
        candidate = fixture.get("envelope", {}).get("candidate", {})
        expected_status = "admitted" if fixture.get("expected") == "admitted" else "expected-staging-rejection"
        if (
            row.get("status") != expected_status
            or row.get("lane") != candidate.get("lane")
            or row.get("provenance_family") != fixture.get("provenance_family")
            or row.get("candidate_sha256") != canonical_sha256(candidate)
        ):
            raise ValueError("tooling readiness result does not bind its fixture candidate")
    runtime_document = _load_json(runtime_path, "runtime config")
    for row in results:
        binding = row.get("runtime_binding")
        runtime = runtime_document.get("runtimes", {}).get(binding.get("runtime_id")) if isinstance(binding, dict) else None
        expected_runtime_binding = {
            "runtime_id": binding.get("runtime_id") if isinstance(binding, dict) else None,
            "image": runtime.get("image") if isinstance(runtime, dict) else None,
            "image_id": runtime.get("image_id") if isinstance(runtime, dict) else None,
            "manifest_digest": runtime.get("manifest_digest") if isinstance(runtime, dict) else None,
            "rootfs_layers_sha256": canonical_sha256(runtime.get("rootfs_layers")) if isinstance(runtime, dict) else None,
            "commands_sha256": canonical_sha256(runtime.get("commands")) if isinstance(runtime, dict) else None,
            "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        }
        if binding != expected_runtime_binding:
            raise ValueError("tooling readiness per-lane image/runtime binding mismatch")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixtures", type=Path,
        help="optional sealed fixture JSON; omission uses the deterministic default builder",
    )
    parser.add_argument("--admission-config", type=Path, required=True)
    parser.add_argument("--runtimes", type=Path, default=ROOT / "configs/eval/runtimes.json")
    parser.add_argument(
        "--preflight-config", type=Path,
        default=ROOT / "configs/data/gate2_v4_post_teacher_preflight.json",
    )
    parser.add_argument("--separation-contract-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    if args.fixtures is None:
        from scripts.data.build_v4_tooling_fixture_bundle import build_fixture_bundle
        bundle = build_fixture_bundle(args.admission_config, args.preflight_config)
        raw = canonical_json(bundle)
    else:
        raw = args.fixtures.read_bytes()
        bundle = json.loads(raw)
    report = run_fixture_bundle(
        bundle, args.admission_config, args.runtimes, args.preflight_config,
        args.separation_contract_sha256,
        fixture_input_sha256=hashlib.sha256(raw).hexdigest(),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_json(report) + b"\n")
    print(canonical_json({
        "status": report["status"], "output": str(args.output),
        "report_sha256": report["report_sha256"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
