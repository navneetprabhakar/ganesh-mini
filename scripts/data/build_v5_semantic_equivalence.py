#!/usr/bin/env python3
"""Seal V5 carry-forward equivalence for the 37 completed blind reviews."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.data.build_v5_interface_replay_cohort import (  # noqa: E402
    BUDGET_CLARIFICATION_ADDENDUM_SHA256, CARRY_SCHEMA, COHORT_SCHEMA,
    CONTRACT_ID, PLAN_SHA256,
)
from scripts.data.run_repair_delta_evidence import (  # noqa: E402
    SEMANTIC_BOOLEANS, _semantic_evidence, _stage_prompt, semantic_projection,
)
from scripts.eval.contracts import sha256_text  # noqa: E402


SCHEMA_VERSION = "ganesh-mini-gate2-v5-semantic-equivalence-manifest/v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_sealed(path: Path, seal_field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    body = dict(value)
    claimed = body.pop(seal_field, None)
    if claimed != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {seal_field}")
    return value


def load_exact_teacher_row(carry: dict[str, Any]) -> dict[str, Any]:
    binding = carry.get("v4_teacher_artifact")
    if not isinstance(binding, dict):
        raise ValueError("carry row lacks its V4 teacher artifact binding")
    path = Path(binding.get("path", ""))
    raw_lines = [line for line in path.read_bytes().splitlines() if line.strip()]
    index = binding.get("row_index")
    if (
        file_sha256(path) != binding.get("file_sha256")
        or not isinstance(index, int) or not 0 <= index < len(raw_lines)
        or hashlib.sha256(raw_lines[index]).hexdigest() != binding.get("record_sha256")
    ):
        raise ValueError("V4 teacher artifact differs from its carry binding")
    value = json.loads(raw_lines[index])
    candidate = value.get("candidate")
    proof = value.get("repair_delta_proof")
    if (
        not isinstance(candidate, dict) or not isinstance(proof, dict)
        or candidate.get("id") != carry.get("v4_candidate_id")
        or canonical_sha256(candidate) != carry.get("candidate_sha256")
        or proof.get("evidence_sha256") != carry.get("teacher_proof_evidence_sha256")
    ):
        raise ValueError("carried teacher row differs from its immutable hashes")
    return value


def validate_stage_artifact(path: Path, expected_input_sha256: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    claimed = body.pop("artifact_sha256", None)
    run = value.get("run")
    if (
        claimed != canonical_sha256(body)
        or value.get("schema_version") != "ganesh-mini-repair-delta-codex-stage/v1"
        or value.get("stage") != "semantic_review"
        or value.get("input_sha256") != expected_input_sha256
        or value.get("evaluation_artifacts_read") != 0
        or not isinstance(run, dict)
    ):
        raise ValueError(f"{path}: semantic-review run is unsealed or input-drifted")
    run_body = dict(run)
    run_claimed = run_body.pop("run_evidence_sha256", None)
    if run_claimed != canonical_sha256(run_body):
        raise ValueError(f"{path}: semantic-review run evidence is unsealed")
    return value


def equivalence_row(
    carry: dict[str, Any], codex_run_dir: Path, pre_separation_dir: Path,
) -> dict[str, Any] | None:
    identifier = carry["v4_candidate_id"]
    run_path = codex_run_dir / f"{identifier}.semantic_review.json"
    if not run_path.exists():
        return None
    generated = load_exact_teacher_row(carry)
    candidate = generated["candidate"]
    assignment = carry["v4_assignment_projection"]
    projection = semantic_projection(candidate, assignment)
    prompt = _stage_prompt("semantic_review", projection, "v4")
    input_sha = canonical_sha256({
        "stage": "semantic_review", "projection": projection, "prompt": prompt,
    })
    run_artifact = validate_stage_artifact(run_path, input_sha)
    if (
        run_artifact.get("candidate_id") != identifier
        or run_artifact.get("prompt_sha256") != sha256_text(prompt)
    ):
        raise ValueError(f"{identifier}: semantic-review identity or prompt drift")
    semantic = _semantic_evidence(
        candidate, assignment, run_artifact["response"],
        run_artifact["run"]["run_evidence_sha256"],
    )
    if any(semantic.get(field) is not True for field in SEMANTIC_BOOLEANS):
        raise ValueError(f"{identifier}: prior semantic review was not a passing review")

    prepared_path = pre_separation_dir / f"{identifier}.pre-separation.json"
    prepared = json.loads(prepared_path.read_text(encoding="utf-8"))
    prepared_body = dict(prepared)
    prepared_claimed = prepared_body.pop("artifact_sha256", None)
    recorded = prepared.get("evidence", {}).get("semantic_review")
    if prepared_claimed != canonical_sha256(prepared_body) or not isinstance(recorded, dict):
        raise ValueError(f"{identifier}: V4 preparation artifact does not bind semantic evidence")
    if "pre_test_semantic_evidence_sha256" in recorded:
        if recorded["pre_test_semantic_evidence_sha256"] != semantic["evidence_sha256"]:
            raise ValueError(f"{identifier}: rebound semantic evidence does not bind the blind review")
    elif recorded != semantic:
        raise ValueError(f"{identifier}: recorded semantic evidence differs from reconstruction")

    row: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate2-v5-semantic-equivalence/v1",
        "disposition": "equivalent-v4-blind-semantic-review",
        "candidate_id": identifier,
        "cell_id": carry["cell_id"],
        "carry_row_sha256": carry["carry_row_sha256"],
        "candidate_sha256": carry["candidate_sha256"],
        "semantic_projection_sha256": canonical_sha256(projection),
        "semantic_evidence": semantic,
        "semantic_evidence_sha256": semantic["evidence_sha256"],
        "reviewer_run_evidence_sha256": run_artifact["run"]["run_evidence_sha256"],
        "v4_stage_artifact": {
            "path": str(run_path), "file_sha256": file_sha256(run_path),
            "artifact_sha256": run_artifact["artifact_sha256"],
        },
        "v4_preparation_artifact": {
            "path": str(prepared_path), "file_sha256": file_sha256(prepared_path),
            "artifact_sha256": prepared["artifact_sha256"],
        },
        "evaluation_artifacts_read": 0,
    }
    row["equivalence_row_sha256"] = canonical_sha256(row)
    return row


def build(
    carry_manifest_path: Path, cohort_manifest_path: Path,
    codex_run_dir: Path, pre_separation_dir: Path,
) -> dict[str, Any]:
    carry_manifest = load_sealed(carry_manifest_path, "manifest_sha256")
    cohort_manifest = load_sealed(cohort_manifest_path, "manifest_sha256")
    if (
        carry_manifest.get("schema_version") != CARRY_SCHEMA
        or cohort_manifest.get("schema_version") != COHORT_SCHEMA
        or carry_manifest.get("contract_id") != CONTRACT_ID
        or cohort_manifest.get("contract_id") != CONTRACT_ID
        or carry_manifest.get("plan_sha256") != PLAN_SHA256
        or cohort_manifest.get("plan_sha256") != PLAN_SHA256
        or carry_manifest.get("budget_clarification_addendum_sha256")
        != BUDGET_CLARIFICATION_ADDENDUM_SHA256
        or cohort_manifest.get("budget_clarification_addendum_sha256")
        != BUDGET_CLARIFICATION_ADDENDUM_SHA256
        or carry_manifest.get("records") != 58
        or cohort_manifest.get("records") != 60
        or cohort_manifest.get("carry_manifest_sha256") != carry_manifest["manifest_sha256"]
        or carry_manifest.get("evaluation_artifacts_read") != 0
        or cohort_manifest.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("V5 carry/cohort manifests are unsealed or inconsistent")
    carries = carry_manifest.get("rows")
    cohort = cohort_manifest.get("rows")
    if not isinstance(carries, list) or not isinstance(cohort, list):
        raise ValueError("V5 carry/cohort rows are missing")
    carry_by_hash = {row.get("carry_row_sha256"): row for row in carries}
    if len(carry_by_hash) != 58:
        raise ValueError("V5 carry rows are duplicated")

    equivalences: list[dict[str, Any]] = []
    review_required: list[dict[str, Any]] = []
    for cohort_row in cohort:
        if cohort_row.get("mode") == "immutable-v4-teacher-carry":
            carry = carry_by_hash.get(cohort_row.get("carry_row_sha256"))
            if carry is None or carry.get("cell_id") != cohort_row.get("cell_id"):
                raise ValueError("V5 cohort row does not bind its immutable carry")
            row = equivalence_row(carry, codex_run_dir, pre_separation_dir)
            if row is None:
                review_required.append({
                    "ordinal": cohort_row["ordinal"], "cell_id": cohort_row["cell_id"],
                    "candidate_id": cohort_row["candidate_id"], "reason": "no-equivalent-v4-review",
                })
            else:
                equivalences.append(row)
        elif cohort_row.get("mode") == "fresh-v5-teacher-primary":
            review_required.append({
                "ordinal": cohort_row["ordinal"], "cell_id": cohort_row["cell_id"],
                "candidate_id": cohort_row["candidate_id"], "reason": "fresh-v5-teacher-primary",
            })
        else:
            raise ValueError("V5 cohort contains an unknown mode")
    if len(equivalences) != 37 or len(review_required) != 23:
        raise ValueError("V5 semantic split must be exactly 37 equivalent and 23 new reviews")
    if [row["ordinal"] for row in review_required] != sorted(row["ordinal"] for row in review_required):
        raise ValueError("V5 semantic review-required rows lost cohort order")

    output: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION, "contract_id": CONTRACT_ID,
        "plan_sha256": PLAN_SHA256,
        "budget_clarification_addendum_sha256": BUDGET_CLARIFICATION_ADDENDUM_SHA256,
        "carry_manifest_sha256": carry_manifest["manifest_sha256"],
        "cohort_manifest_sha256": cohort_manifest["manifest_sha256"],
        "v4_codex_run_directory": str(codex_run_dir),
        "v4_pre_separation_directory": str(pre_separation_dir),
        "equivalences": equivalences,
        "equivalences_sha256": canonical_sha256(equivalences),
        "equivalent_reviews": 37,
        "review_required": review_required,
        "review_required_sha256": canonical_sha256(review_required),
        "new_reviews_required": 23,
        "evaluation_artifacts_read": 0,
    }
    output["manifest_sha256"] = canonical_sha256(output)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--carry-manifest", type=Path, required=True)
    parser.add_argument("--cohort-manifest", type=Path, required=True)
    parser.add_argument("--v4-codex-run-dir", type=Path, required=True)
    parser.add_argument("--v4-pre-separation-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    value = build(
        args.carry_manifest, args.cohort_manifest,
        args.v4_codex_run_dir, args.v4_pre_separation_dir,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "equivalent_reviews": value["equivalent_reviews"],
        "new_reviews_required": value["new_reviews_required"],
        "manifest_sha256": value["manifest_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
