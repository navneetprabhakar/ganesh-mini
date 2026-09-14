#!/usr/bin/env python3
"""Combine reviewed bounded replacements with the sealed original qualification."""

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

from scripts.data.admit_expansion import canonical_json, read_jsonl  # noqa: E402
from scripts.data.build_capability_corpus_plan import canonical_sha256, load_sealed  # noqa: E402
from scripts.data.generate_capability_replacements import MANIFEST_SCHEMA  # noqa: E402
from scripts.data.review_capability_qualification import candidate_sha256  # noqa: E402
from scripts.eval.contracts import sha256_text  # noqa: E402


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(
    original_candidates_path: Path, original_semantic: dict[str, Any],
    replacement_manifest: dict[str, Any], review_paths: list[Path],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    originals = read_jsonl(original_candidates_path)
    if (
        len(originals) != 240
        or original_semantic.get("schema_version") != "ganesh-mini-capability-semantic-review-report/v1"
        or original_semantic.get("status") != "complete"
        or original_semantic.get("candidate_input_sha256") != file_sha256(original_candidates_path)
        or replacement_manifest.get("schema_version") != MANIFEST_SCHEMA
        or replacement_manifest.get("semantic_report_sha256") != original_semantic.get("report_sha256")
        or replacement_manifest.get("replacement_attempt") != 1
    ):
        raise ValueError("original disposition or replacement manifest binding is invalid")
    batches = replacement_manifest.get("batches")
    if not isinstance(batches, list):
        raise ValueError("replacement batch inventory is absent")
    replacements: list[dict[str, Any]] = []
    for batch in batches:
        path = Path(batch["candidates"])
        rows = read_jsonl(path)
        if len(rows) != batch.get("records"):
            raise ValueError("replacement candidate batch count mismatch")
        replacements.extend(rows)
    expected_ids = replacement_manifest.get("candidate_ids")
    if [row.get("id") for row in replacements] != expected_ids or len(set(expected_ids)) != len(expected_ids):
        raise ValueError("replacement candidates differ from manifest")

    reviews: dict[str, dict[str, Any]] = {}
    for path in review_paths:
        for row in read_jsonl(path):
            body = dict(row); claimed = body.pop("evidence_sha256", None)
            identifier = row.get("id")
            if claimed != canonical_sha256(body) or not isinstance(identifier, str) or identifier in reviews:
                raise ValueError("replacement semantic evidence seal or identity is invalid")
            reviews[identifier] = row
    if set(reviews) != set(expected_ids):
        raise ValueError("replacement semantic review does not cover every replacement exactly once")

    records = list(original_semantic["records"])
    for candidate in replacements:
        identifier = candidate["id"]
        review = reviews[identifier]
        assignment = candidate.get("qualification_assignment", {})
        visibility = review.get("visibility", {})
        substantive = review.get("primary_capability_is_substantive")
        generic = review.get("generic_edge_case_boilerplate_is_primary")
        verdict = review.get("verdict")
        if (
            review.get("candidate_sha256") != candidate_sha256(candidate)
            or review.get("specification_sha256") != sha256_text(candidate["messages"][0]["content"])
            or review.get("primary_capability") != assignment.get("primary_capability")
            or review.get("assigned_cross_cutting_dimension") != assignment.get("assigned_cross_cutting_dimension")
            or (verdict == "pass") != (substantive is True and generic is False)
            or visibility.get("specification_and_assigned_labels_only") is not True
            or visibility.get("verifier_outputs_visible") is not False
            or visibility.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError(f"{identifier}: replacement semantic review binding is invalid")
        records.append({
            "id": identifier, "candidate_sha256": review["candidate_sha256"],
            "specification_sha256": review["specification_sha256"],
            "primary_capability": review["primary_capability"],
            "assigned_cross_cutting_dimension": review["assigned_cross_cutting_dimension"],
            "verdict": verdict, "primary_capability_is_substantive": substantive,
            "generic_edge_case_boilerplate_is_primary": generic,
            "verifier_outputs_visible": False, "evaluation_artifacts_read": 0,
            "correction_passes": 0, "semantic_evidence_sha256": review["evidence_sha256"],
        })
    if len({row["id"] for row in records}) != len(records):
        raise ValueError("augmented semantic disposition contains duplicate candidates")
    combined = [*originals, *replacements]
    payload = b"".join(canonical_json(row) + b"\n" for row in combined)
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-semantic-review-report/v1",
        "status": "complete", "visibility": "specification-and-assigned-labels-only",
        "evaluation_artifacts_read": 0, "candidate_input_sha256": hashlib.sha256(payload).hexdigest(),
        "semantic_evidence_sha256": hashlib.sha256(b"".join(canonical_json(row) + b"\n" for row in records)).hexdigest(),
        "original_semantic_report_sha256": original_semantic["report_sha256"],
        "replacement_manifest_sha256": replacement_manifest["manifest_sha256"],
        "records": records,
    }
    report["report_sha256"] = canonical_sha256(report)
    return combined, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original-candidates", type=Path, required=True)
    parser.add_argument("--original-semantic-report", type=Path, required=True)
    parser.add_argument("--replacement-manifest", type=Path, required=True)
    parser.add_argument("--replacement-semantic", type=Path, action="append", required=True)
    parser.add_argument("--output-candidates", type=Path, required=True)
    parser.add_argument("--output-semantic-report", type=Path, required=True)
    args = parser.parse_args()
    original_semantic = load_sealed(args.original_semantic_report, "report_sha256")
    replacement_manifest = load_sealed(args.replacement_manifest, "manifest_sha256")
    candidates, semantic = build(
        args.original_candidates, original_semantic, replacement_manifest, args.replacement_semantic,
    )
    args.output_candidates.parent.mkdir(parents=True, exist_ok=True)
    args.output_candidates.write_bytes(b"".join(canonical_json(row) + b"\n" for row in candidates))
    args.output_semantic_report.parent.mkdir(parents=True, exist_ok=True)
    args.output_semantic_report.write_text(json.dumps(semantic, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(candidates), "report_sha256": semantic["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
