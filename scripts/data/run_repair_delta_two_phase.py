#!/usr/bin/env python3
"""Run v3 repair-delta evidence across the content-free separation boundary.

Phase one performs only blind semantic review, independent split-test
authorship, and delta audit.  It emits the complete post-test candidate cohort
before any candidate code is executed.  The existing global separation
builder then compares that cohort as one immutable batch.  Phase two consumes
only content-free, sealed per-candidate sidecars and may execute the split
suites and assemble admission envelopes.

The orchestration functions accept stage/verifier callables so unit tests do
not invoke Codex, containers, or evaluation data.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_expansion import canonical_json  # noqa: E402
from scripts.data.admit_repair_delta import (  # noqa: E402
    CONTRACT_ID, ENVELOPE_SCHEMA, PROOF_BOOLEAN_OVERLAP, SEMANTIC_BOOLEANS,
    SEPARATION_PASSES, teacher_candidate_sha256,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.data.build_capability_separation_attestations import (  # noqa: E402
    PASS_FIELDS, SCHEMA_VERSION as SEPARATION_REPORT_SCHEMA, build_report,
)
from scripts.data.generate_expansion_qualification import verify_codex_version  # noqa: E402
from scripts.data.run_repair_delta_evidence import (  # noqa: E402
    ARTIFACT_SCHEMA, IsolatedCodexAdapter, StageFn, VerifierFn,
    _add_tests, _delta_evidence, _executable_evidence, _rebind_semantic,
    _semantic_evidence, _terminal, delta_projection, load_campaign_inputs,
    semantic_projection, seal, test_author_projection,
)
from scripts.verify.sandbox import verify  # noqa: E402


PREPARATION_SCHEMA = "ganesh-mini-repair-delta-pre-separation/v1"
SIDECAR_SCHEMA = "ganesh-mini-repair-delta-separation-sidecar/v1"
CAMPAIGN_SCHEMA = "ganesh-mini-repair-delta-two-phase-campaign/v1"


def _sealed(value: dict[str, Any], field: str) -> dict[str, Any]:
    body = dict(value)
    claimed = body.pop(field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"unsealed {field} artifact")
    return value


def _validate_teacher_binding(
    generated: dict[str, Any], assignment: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], str]:
    candidate = copy.deepcopy(generated["candidate"])
    proof = copy.deepcopy(generated["repair_delta_proof"])
    input_sha = canonical_sha256({"generated": generated, "assignment": assignment})
    proof_body = dict(proof)
    proof_claimed = proof_body.pop("evidence_sha256", None)
    if (
        proof_claimed != canonical_sha256(proof_body)
        or proof.get("candidate_id") != candidate.get("id")
        or proof.get("teacher_candidate_sha256") != teacher_candidate_sha256(candidate)
        or assignment.get("id") != candidate.get("id")
        or assignment.get("contract_id") != CONTRACT_ID
    ):
        raise ValueError("teacher proof, pre-test candidate, and sealed assignment do not bind")
    return candidate, proof, input_sha


def prepare_candidate(
    generated: dict[str, Any], assignment: dict[str, Any],
    semantic_fn: StageFn, test_fn: StageFn, delta_fn: StageFn,
) -> dict[str, Any]:
    """Author all pre-execution evidence and return a sealed post-test row."""
    candidate, proof, input_sha = _validate_teacher_binding(generated, assignment)

    semantic_response = semantic_fn(semantic_projection(candidate, assignment))
    semantic_run = semantic_response.pop("_run_sha256")
    semantic = _semantic_evidence(candidate, assignment, semantic_response, semantic_run)
    if any(semantic[field] is not True for field in SEMANTIC_BOOLEANS):
        return _terminal(candidate, assignment, "semantic_review", "blind semantic boolean failed", {
            "teacher_proof": proof, "semantic_review": semantic,
        }, input_sha)
    if any(semantic[field] is not proof[field] for field in PROOF_BOOLEAN_OVERLAP):
        return _terminal(candidate, assignment, "proof_consistency", "teacher proof disagrees with blind review", {
            "teacher_proof": proof, "semantic_review": semantic,
        }, input_sha)

    test_response = test_fn(test_author_projection(candidate, assignment))
    test_run = test_response.pop("_run_sha256")
    candidate, test_evidence = _add_tests(candidate, assignment, test_response, test_run)
    semantic = _rebind_semantic(semantic, candidate)

    delta_response = delta_fn(delta_projection(candidate, assignment))
    delta_run = delta_response.pop("_run_sha256")
    delta = _delta_evidence(candidate, assignment, delta_response, delta_run)
    if (
        delta["independent_semantic_delta_count"] != 1
        or delta["delta_is_capability_specific"] is not True
        or delta["introduces_multiple_independent_fixes"] is not False
    ):
        return _terminal(candidate, assignment, "delta_audit", "delta auditor rejected the repair", {
            "teacher_proof": proof, "semantic_review": semantic,
            "test_author": test_evidence, "delta_audit": delta,
        }, input_sha)

    artifact: dict[str, Any] = {
        "schema_version": PREPARATION_SCHEMA,
        "status": "awaiting-separation",
        "input_sha256": input_sha,
        "candidate_id": candidate["id"],
        "candidate_sha256": canonical_sha256(candidate),
        "cell_id": assignment["cell_id"],
        "candidate": candidate,
        "assignment": copy.deepcopy(assignment),
        "evidence": {
            "teacher_proof": proof, "semantic_review": semantic,
            "test_author": test_evidence, "delta_audit": delta,
        },
        "execution_performed": False,
        "evaluation_artifacts_read": 0,
    }
    artifact["artifact_sha256"] = canonical_sha256(artifact)
    return artifact


def run_preparation_resumable(
    generated_rows: list[dict[str, Any]], assignments: dict[str, dict[str, Any]],
    output_dir: Path, semantic_fn: StageFn, test_fn: StageFn, delta_fn: StageFn,
) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict[str, Any]] = []
    for generated in generated_rows:
        identifier = generated.get("candidate", {}).get("id")
        assignment = assignments.get(identifier)
        if not isinstance(identifier, str) or not isinstance(assignment, dict):
            raise ValueError("generated candidate lacks an exact assignment")
        path = output_dir / f"{identifier}.pre-separation.json"
        expected = canonical_sha256({"generated": generated, "assignment": assignment})
        if path.exists():
            artifact = json.loads(path.read_text(encoding="utf-8"))
            _sealed(artifact, "artifact_sha256")
            if artifact.get("input_sha256") != expected:
                raise ValueError(f"{identifier}: prepared artifact binds different input")
        else:
            artifact = prepare_candidate(generated, assignment, semantic_fn, test_fn, delta_fn)
            path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        artifacts.append(artifact)
    return artifacts


def write_post_test_candidates(artifacts: list[dict[str, Any]], path: Path) -> list[dict[str, Any]]:
    candidates = [row["candidate"] for row in artifacts if row.get("status") == "awaiting-separation"]
    identifiers = [row["id"] for row in candidates]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("post-test candidate identities are duplicated")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in candidates))
    return candidates


def separation_contract_sha256(report: dict[str, Any]) -> str:
    """Hash only the frozen comparator behavior, not observed candidate results."""
    return canonical_sha256({
        "schema_version": SEPARATION_REPORT_SCHEMA,
        "policy": report["comparison_manifest"]["policy"],
        "pass_fields": list(PASS_FIELDS),
        "sidecar_schema": SIDECAR_SCHEMA,
    })


def build_separation_sidecars(
    report: dict[str, Any], candidates: list[dict[str, Any]], output_path: Path,
) -> tuple[list[dict[str, Any]], str]:
    _sealed(report, "report_sha256")
    if (
        report.get("schema_version") != SEPARATION_REPORT_SCHEMA
        or report.get("evaluation_artifacts_read_by_construction") != 0
        or report.get("comparison_manifest_sha256")
        != canonical_sha256(report.get("comparison_manifest"))
    ):
        raise ValueError("global separation report is unsealed or not content-free")
    by_id = {row.get("id"): row for row in report.get("records", []) if isinstance(row, dict)}
    candidate_by_id = {row["id"]: row for row in candidates}
    if set(by_id) != set(candidate_by_id) or len(by_id) != len(report.get("records", [])):
        raise ValueError("global separation report does not cover the exact post-test cohort")
    contract_sha = separation_contract_sha256(report)
    sidecars: list[dict[str, Any]] = []
    for identifier in sorted(candidate_by_id):
        source = by_id[identifier]
        candidate_sha = canonical_sha256(candidate_by_id[identifier])
        if source.get("candidate_sha256") != candidate_sha or any(
            type(source.get(field)) is not bool for field in PASS_FIELDS
        ):
            raise ValueError(f"{identifier}: separation record is malformed or candidate-unbound")
        row = {
            "schema_version": SIDECAR_SCHEMA,
            "candidate_id": identifier,
            "candidate_sha256": candidate_sha,
            "comparison_contract_sha256": contract_sha,
            "comparison_manifest_sha256": report["comparison_manifest_sha256"],
            **{field: source[field] for field in PASS_FIELDS},
            "evaluation_artifacts_read_by_construction": 0,
        }
        row["evidence_sha256"] = canonical_sha256(row)
        sidecars.append(row)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in sidecars))
    return sidecars, contract_sha


def _validate_prepared(artifact: dict[str, Any]) -> None:
    _sealed(artifact, "artifact_sha256")
    candidate = artifact.get("candidate")
    evidence = artifact.get("evidence")
    if (
        artifact.get("schema_version") != PREPARATION_SCHEMA
        or artifact.get("status") != "awaiting-separation"
        or artifact.get("execution_performed") is not False
        or artifact.get("evaluation_artifacts_read") != 0
        or not isinstance(candidate, dict)
        or artifact.get("candidate_id") != candidate.get("id")
        or artifact.get("candidate_sha256") != canonical_sha256(candidate)
        or not isinstance(evidence, dict)
        or set(evidence) != {"teacher_proof", "semantic_review", "test_author", "delta_audit"}
    ):
        raise ValueError("prepared artifact is malformed or not pre-execution")
    for value in evidence.values():
        _sealed(value, "evidence_sha256")


def resume_candidate(
    prepared: dict[str, Any], separation: dict[str, Any], runtime_path: Path,
    verifier_fn: VerifierFn = verify,
) -> dict[str, Any]:
    """Consume a content-free sidecar, then and only then execute suites."""
    _validate_prepared(prepared)
    _sealed(separation, "evidence_sha256")
    candidate = copy.deepcopy(prepared["candidate"])
    assignment = copy.deepcopy(prepared["assignment"])
    if (
        separation.get("schema_version") != SIDECAR_SCHEMA
        or separation.get("candidate_id") != candidate["id"]
        or separation.get("candidate_sha256") != canonical_sha256(candidate)
        or separation.get("evaluation_artifacts_read_by_construction") != 0
    ):
        raise ValueError("separation sidecar does not bind the prepared candidate")
    evidence = copy.deepcopy(prepared["evidence"])
    evidence["separation"] = copy.deepcopy(separation)
    phase2_input_sha = canonical_sha256({
        "prepared_artifact_sha256": prepared["artifact_sha256"],
        "separation_evidence_sha256": separation["evidence_sha256"],
        "runtime_config_sha256": hashlib.sha256(runtime_path.read_bytes()).hexdigest(),
    })
    if any(separation.get(field) is not True for field in SEPARATION_PASSES):
        result = _terminal(
            candidate, assignment, "separation", "global content-free separation failed",
            evidence, prepared["input_sha256"],
        )
        result["phase2_input_sha256"] = phase2_input_sha
        result.pop("artifact_sha256")
        result["artifact_sha256"] = canonical_sha256(result)
        return result

    executable, retry_ledger = _executable_evidence(
        candidate, evidence["test_author"], runtime_path, verifier_fn,
    )
    evidence["executable"] = executable
    if retry_ledger["unresolved"]:
        value = _terminal(
            candidate, assignment, "executable",
            "unresolved infrastructure after one identical replay",
            {**evidence, "retry_ledger": retry_ledger}, prepared["input_sha256"],
        )
        value["status"] = "unresolved"
        value["phase2_input_sha256"] = phase2_input_sha
        value.pop("artifact_sha256")
        value["artifact_sha256"] = canonical_sha256(value)
        return value

    lineage = seal({
        "candidate_sha256": canonical_sha256(candidate), "contract_id": CONTRACT_ID,
        "cell_id": assignment["cell_id"],
        "source_identity": {key: candidate["source"].get(key) for key in ("dataset", "revision", "record_id")},
        "source_record_sha256": candidate["source"]["source_record_sha256"], "complete": True,
        "teacher_proof_evidence_sha256": evidence["teacher_proof"]["evidence_sha256"],
        "semantic_review_evidence_sha256": evidence["semantic_review"]["evidence_sha256"],
        "test_author_evidence_sha256": evidence["test_author"]["evidence_sha256"],
        "delta_audit_evidence_sha256": evidence["delta_audit"]["evidence_sha256"],
        "separation_evidence_sha256": separation["evidence_sha256"],
        "executable_evidence_sha256": executable["evidence_sha256"],
    })
    evidence["lineage"] = lineage
    envelope = {
        "schema_version": ENVELOPE_SCHEMA, "candidate": candidate,
        "assignment": {
            "contract_id": CONTRACT_ID, "cell_id": assignment["cell_id"],
            "primary_capability": assignment["primary_capability"],
            "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        },
        "evidence": evidence,
    }
    result = {
        "schema_version": ARTIFACT_SCHEMA, "status": "ready-for-admission",
        "input_sha256": prepared["input_sha256"], "candidate_id": candidate["id"],
        "phase2_input_sha256": phase2_input_sha,
        "envelope": envelope, "retry_ledger": retry_ledger,
        "evaluation_artifacts_read": 0,
    }
    result["artifact_sha256"] = canonical_sha256(result)
    return result


def run_resume_resumable(
    prepared_rows: list[dict[str, Any]], sidecars: list[dict[str, Any]],
    output_dir: Path, runtime_path: Path, verifier_fn: VerifierFn = verify,
) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    by_id = {row.get("candidate_id"): row for row in sidecars}
    awaiting = {row["candidate_id"] for row in prepared_rows if row.get("status") == "awaiting-separation"}
    if set(by_id) != awaiting or len(by_id) != len(sidecars):
        raise ValueError("separation sidecars do not exactly cover prepared post-test candidates")
    results: list[dict[str, Any]] = []
    for prepared in prepared_rows:
        if prepared.get("status") != "awaiting-separation":
            results.append(prepared)
            continue
        identifier = prepared["candidate_id"]
        path = output_dir / f"{identifier}.evidence.json"
        expected_phase2_input = canonical_sha256({
            "prepared_artifact_sha256": prepared["artifact_sha256"],
            "separation_evidence_sha256": by_id[identifier]["evidence_sha256"],
            "runtime_config_sha256": hashlib.sha256(runtime_path.read_bytes()).hexdigest(),
        })
        if path.exists():
            artifact = json.loads(path.read_text(encoding="utf-8"))
            _sealed(artifact, "artifact_sha256")
            if (
                artifact.get("input_sha256") != prepared["input_sha256"]
                or artifact.get("phase2_input_sha256") != expected_phase2_input
            ):
                raise ValueError(f"{identifier}: resumed artifact binds different phase-two input")
        else:
            artifact = resume_candidate(prepared, by_id[identifier], runtime_path, verifier_fn)
            path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        results.append(artifact)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--teacher-candidates", type=Path, action="append", required=True)
    parser.add_argument("--teacher-evidence", type=Path, action="append", required=True)
    parser.add_argument("--cohort", choices=("primary", "reserve"), required=True)
    parser.add_argument("--reserve-eligibility", type=Path)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--runtime-config", type=Path, required=True)
    parser.add_argument("--training-corpus", type=Path, action="append", required=True)
    parser.add_argument("--evaluation-root", type=Path, action="append", required=True)
    parser.add_argument("--prompt-simhash-max-hamming", type=int, default=3)
    parser.add_argument("--minimum-fuzzy-tokens", type=int, default=12)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    generated, assignments, manifest = load_campaign_inputs(
        args.queue, args.queue_manifest, args.teacher_candidates, args.teacher_evidence,
        args.cohort, args.reserve_eligibility,
    )
    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    adapters = {
        stage: IsolatedCodexAdapter(stage, config, args.codex_bin, args.output_root / "codex-runs", cli_identity)
        for stage in ("semantic_review", "test_author", "delta_audit")
    }
    prepared = run_preparation_resumable(
        generated, assignments, args.output_root / "pre-separation",
        adapters["semantic_review"], adapters["test_author"], adapters["delta_audit"],
    )
    candidate_path = args.output_root / "post-test-candidates.jsonl"
    candidates = write_post_test_candidates(prepared, candidate_path)
    if not candidates:
        raise ValueError("no post-test candidates remain for global separation")
    report = build_report(
        candidate_path, args.training_corpus, args.evaluation_root,
        args.prompt_simhash_max_hamming, args.minimum_fuzzy_tokens,
    )
    report_path = args.output_root / "global-separation-report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sidecar_path = args.output_root / "separation-sidecars.jsonl"
    sidecars, contract_sha = build_separation_sidecars(report, candidates, sidecar_path)
    final = run_resume_resumable(
        prepared, sidecars, args.output_root / "candidate-evidence", args.runtime_config,
    )
    envelope_path = args.output_root / "admission-envelopes.jsonl"
    ready = [row["envelope"] for row in final if row.get("status") == "ready-for-admission"]
    envelope_path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in ready))
    inventory = {
        "schema_version": CAMPAIGN_SCHEMA,
        "status": "ready-for-admission" if len(ready) == len(final) else "terminal-or-unresolved",
        "cohort": args.cohort, "queue_manifest_sha256": manifest["manifest_sha256"],
        "generated": len(generated), "post_test": len(candidates), "ready": len(ready),
        "terminal_rejected": sum(row.get("status") == "terminal-rejected" for row in final),
        "unresolved": sum(row.get("status") == "unresolved" for row in final),
        "post_test_candidates_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "separation_report_sha256": report["report_sha256"],
        "separation_contract_sha256": contract_sha,
        "separation_sidecars_sha256": hashlib.sha256(sidecar_path.read_bytes()).hexdigest(),
        "admission_envelopes_sha256": hashlib.sha256(envelope_path.read_bytes()).hexdigest(),
        "artifact_sha256s": {row["candidate_id"]: row["artifact_sha256"] for row in final},
        "cli_identity": cli_identity,
        "codex_config_sha256": hashlib.sha256(args.codex_config.read_bytes()).hexdigest(),
        "runtime_config_sha256": hashlib.sha256(args.runtime_config.read_bytes()).hexdigest(),
        "evaluation_artifacts_read_outside_separation": 0,
    }
    inventory["report_sha256"] = canonical_sha256(inventory)
    inventory_path = args.output_root / "two-phase-inventory.json"
    inventory_path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": inventory["status"], "ready": len(ready),
        "separation_contract_sha256": contract_sha,
        "report_sha256": inventory["report_sha256"],
    }, sort_keys=True))
    return 0 if inventory["status"] == "ready-for-admission" else 2


if __name__ == "__main__":
    raise SystemExit(main())
