#!/usr/bin/env python3
"""Verify and aggregate capability-scale blind semantic-review batches."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.review_capability_qualification import (
    campaign_descriptor, candidate_sha256, load_candidates, load_evidence,
    read_jsonl, verify_completed,
)
from scripts.eval.contracts import sha256_text


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def aggregate(candidates_path: Path, semantic_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    candidates = load_candidates(candidates_path)
    campaign = campaign_descriptor(candidates_path, candidates)
    expected = {candidate_sha256(row): row for row in candidates}
    if len(expected) != len(candidates):
        raise ValueError("candidate semantic identities are not unique")
    combined: dict[str, dict[str, Any]] = {}
    batches: list[dict[str, Any]] = []
    evidence_files = sorted(semantic_dir.glob("*.evidence.json"))
    if not evidence_files:
        raise ValueError("semantic-review evidence is absent")
    for evidence_path in evidence_files:
        outer = json.loads(evidence_path.read_text(encoding="utf-8"))
        batch = outer.get("batch")
        if not isinstance(batch, dict):
            raise ValueError(f"{evidence_path}: batch descriptor is absent")
        output = semantic_dir / evidence_path.name.replace(".evidence.json", ".semantic.jsonl")
        verified = verify_completed(
            output, evidence_path, batch.get("ordered_candidate_ids", []),
            campaign["campaign_sha256"], canonical_sha256(batch),
        )
        if verified is None:
            raise ValueError(f"{evidence_path}: batch is incomplete")
        for semantic in read_jsonl(output):
            key = semantic.get("candidate_sha256")
            candidate = expected.get(key)
            if (
                candidate is None or key in combined or load_evidence(semantic) is None
                or semantic.get("specification_sha256") != sha256_text(candidate["messages"][0]["content"])
                or semantic.get("primary_capability") != candidate["qualification_assignment"]["primary_capability"]
                or semantic.get("assigned_cross_cutting_dimension")
                != candidate["qualification_assignment"]["assigned_cross_cutting_dimension"]
                or semantic.get("visibility", {}).get("evaluation_artifacts_read") != 0
            ):
                raise ValueError(f"{evidence_path}: semantic row fails candidate binding")
            combined[key] = semantic
        batches.append({
            "evidence_path": str(evidence_path), "evidence_sha256": file_sha256(evidence_path),
            "output_path": str(output), "output_sha256": file_sha256(output),
        })
    if set(combined) != set(expected):
        raise ValueError("semantic-review batches do not exactly cover candidates")
    ordered = [combined[candidate_sha256(row)] for row in candidates]
    counts = {
        "reviewed": len(ordered),
        "passed": sum(row["verdict"] == "pass" for row in ordered),
        "rejected": sum(row["verdict"] == "reject" for row in ordered),
    }
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-semantic-report/v1",
        "status": "complete" if counts["reviewed"] == len(candidates) else "incomplete",
        "candidate_input_sha256": file_sha256(candidates_path),
        "campaign_sha256": campaign["campaign_sha256"],
        "counts": counts,
        "ordered_candidate_ids": [row["id"] for row in candidates],
        "semantic_evidence_sha256s": [row["evidence_sha256"] for row in ordered],
        "batches": batches,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return ordered, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--semantic-dir", type=Path, required=True)
    parser.add_argument("--combined-output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    rows, report = aggregate(args.candidates, args.semantic_dir)
    _atomic_text(args.combined_output, "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    _atomic_text(args.report, json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "counts": report["counts"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0 if report["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
