from __future__ import annotations

import json
from pathlib import Path

from scripts.data.admit_repair_delta import teacher_candidate_sha256, validate_envelope
from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_separation_attestations import PASS_FIELDS, SCHEMA_VERSION
from scripts.data.run_repair_delta_two_phase import (
    PREPARATION_SCHEMA,
    build_separation_sidecars,
    prepare_candidate,
    resume_candidate,
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
        "candidate_path": "solution.py", "commands": [["python", "test_primary.py"]],
    }
    path = tmp_path / "runtimes.json"
    path.write_text(json.dumps({
        "schema_version": "3.0", "platform": "linux/amd64",
        "runtimes": {"python-locked": runtime},
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
    runtime_path, runtime = runtime_file(tmp_path)

    def verifier(_task: dict, code: str, _runtime: Path) -> dict:
        calls.append(code)
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
    assert artifact["envelope"]["evidence"]["separation"]["comparison_contract_sha256"] == contract
    admitted = validate_envelope(artifact["envelope"], {
        "allowed_licenses": ["MIT"],
        "required_rights": ["prompt", "answer", "tests", "redistribution", "model_training"],
        "allowed_test_origins": ["independent_author"],
        "sources": {"fixture": {"revision": "r1", "license": "MIT"}},
    }, runtime_path, contract)
    assert admitted["id"] == "repair-0"


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
