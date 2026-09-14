#!/usr/bin/env python3
"""Run and seal the 24 resumable capability semantic-review batches."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_capability_qualification import LANES
from scripts.data.review_capability_qualification import (
    campaign_descriptor,
    candidate_sha256,
    load_candidates,
    load_evidence,
    read_jsonl,
    verify_completed as verify_review_batch,
)
from scripts.eval.contracts import sha256_text


BATCH_SIZE = 10
LANE_RECORDS = 40
CAMPAIGN_BATCHES = 24


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def batch_paths(output_root: Path, evidence_root: Path, lane: str, index: int) -> tuple[Path, Path]:
    stem = f"{lane}-{index:03d}"
    return output_root / f"{stem}.semantic.jsonl", evidence_root / f"{stem}.evidence.json"


def batch_descriptor(campaign_sha256: str, lane: str, index: int, expected_ids: list[str]) -> dict[str, Any]:
    return {
        "campaign_sha256": campaign_sha256,
        "lane": lane,
        "batch_index": index,
        "batch_size": BATCH_SIZE,
        "ordered_candidate_ids": expected_ids,
    }


def command(
    candidates: Path, output: Path, evidence: Path, lane: str, index: int, review_workers: int,
) -> list[str]:
    return [
        sys.executable,
        str(ROOT / "scripts/data/review_capability_qualification.py"),
        "--candidates", str(candidates),
        "--lane", lane,
        "--batch-index", str(index),
        "--batch-size", str(BATCH_SIZE),
        "--workers", str(review_workers),
        "--output", str(output),
        "--evidence", str(evidence),
    ]


def verify_completed(
    output: Path, evidence_path: Path, expected_rows: list[dict[str, Any]],
    campaign_sha: str, batch_sha: str,
) -> dict[str, Any] | None:
    expected_ids = [row["id"] for row in expected_rows]
    outer = verify_review_batch(output, evidence_path, expected_ids, campaign_sha, batch_sha)
    if outer is None:
        return None
    rows = read_jsonl(output)
    expected_hashes = [candidate_sha256(row) for row in expected_rows]
    if (
        outer.get("schema_version") != "ganesh-mini-capability-semantic-review-batch/v1"
        or outer.get("reviewed") != len(expected_rows)
        or outer.get("evaluation_artifacts_read") != 0
        or outer.get("campaign", {}).get("campaign_sha256") != campaign_sha
        or canonical_sha256(outer.get("batch", {})) != batch_sha
        or [row.get("candidate_sha256") for row in rows] != expected_hashes
    ):
        raise ValueError(f"semantic-review batch fails campaign contract: {output}")
    for candidate, semantic in zip(expected_rows, rows):
        assignment = candidate["qualification_assignment"]
        visibility = semantic.get("visibility")
        substantive = semantic.get("primary_capability_is_substantive")
        generic = semantic.get("generic_edge_case_boilerplate_is_primary")
        if (
            load_evidence(semantic) is None
            or semantic.get("specification_sha256") != sha256_text(candidate["messages"][0]["content"])
            or semantic.get("primary_capability") != assignment["primary_capability"]
            or semantic.get("assigned_cross_cutting_dimension") != assignment["assigned_cross_cutting_dimension"]
            or semantic.get("verdict") not in {"pass", "reject"}
            or (semantic.get("verdict") == "pass") != (substantive is True and generic is False)
            or not isinstance(visibility, dict)
            or visibility.get("evaluation_artifacts_read") != 0
            or visibility.get("specification_and_assigned_labels_only") is not True
        ):
            raise ValueError(f"{candidate['id']}: semantic evidence fails its candidate binding")
    return {
        "reviewed": len(rows),
        "passed": sum(row["verdict"] == "pass" for row in rows),
        "rejected": sum(row["verdict"] == "reject" for row in rows),
        "evidence_sha256": outer["evidence_sha256"],
        "output_sha256": sha256_file(output),
    }


def run_batch(
    argv: list[str], output: Path, evidence: Path, expected_rows: list[dict[str, Any]],
    campaign_sha: str, batch_sha: str,
) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    completed = verify_completed(output, evidence, expected_rows, campaign_sha, batch_sha)
    if completed is not None:
        return {"status": "reused", **completed}
    result = subprocess.run(
        argv, cwd=ROOT, stdin=subprocess.DEVNULL, capture_output=True, text=True,
        timeout=7200, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"semantic-review batch failed ({result.returncode}): {' '.join(argv)}\n"
            f"stdout={result.stdout}\nstderr={result.stderr}"
        )
    completed = verify_completed(output, evidence, expected_rows, campaign_sha, batch_sha)
    if completed is None:
        raise RuntimeError("semantic-review batch succeeded without sealed artifacts")
    return {"status": "reviewed", **completed}


def build_work(
    rows: list[dict[str, Any]], output_root: Path, evidence_root: Path, campaign_sha: str,
) -> list[tuple[str, int, Path, Path, list[dict[str, Any]], str]]:
    work: list[tuple[str, int, Path, Path, list[dict[str, Any]], str]] = []
    for lane in LANES:
        lane_rows = [row for row in rows if row["lane"] == lane]
        if len(lane_rows) != LANE_RECORDS:
            raise ValueError(f"{lane}: expected exactly {LANE_RECORDS} candidates")
        for index in range(LANE_RECORDS // BATCH_SIZE):
            selected = lane_rows[index * BATCH_SIZE:(index + 1) * BATCH_SIZE]
            output, evidence = batch_paths(output_root, evidence_root, lane, index)
            descriptor = batch_descriptor(campaign_sha, lane, index, [row["id"] for row in selected])
            work.append((lane, index, output, evidence, selected, canonical_sha256(descriptor)))
    if len(work) != CAMPAIGN_BATCHES:
        raise ValueError("semantic-review campaign must contain exactly 24 batches")
    return work


def combine(
    work: list[tuple[str, int, Path, Path, list[dict[str, Any]], str]],
    canonical_rows: list[dict[str, Any]], campaign_sha: str,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    by_candidate_hash: dict[str, dict[str, Any]] = {}
    batches: dict[str, dict[str, Any]] = {}
    for lane, index, output, evidence, expected_rows, batch_sha in work:
        verified = verify_completed(output, evidence, expected_rows, campaign_sha, batch_sha)
        if verified is None:
            raise RuntimeError(f"completed semantic-review campaign is missing {lane}/{index}")
        batches[f"{lane}/{index}"] = verified
        for row in read_jsonl(output):
            key = row["candidate_sha256"]
            if key in by_candidate_hash:
                raise ValueError("semantic-review campaign contains duplicate candidate evidence")
            by_candidate_hash[key] = row
    expected_hashes = [candidate_sha256(row) for row in canonical_rows]
    if set(by_candidate_hash) != set(expected_hashes) or len(expected_hashes) != 240:
        raise ValueError("semantic-review campaign does not cover exactly 240 candidates")
    return [by_candidate_hash[key] for key in expected_hashes], dict(sorted(batches.items()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--combined-output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--review-workers", type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.workers <= 6 or not 1 <= args.review_workers <= 4 or args.workers * args.review_workers > 12:
        raise ValueError("workers must be 1..6, review-workers 1..4, and their product at most 12")

    rows = load_candidates(args.candidates)
    if len(rows) != 240:
        raise ValueError("semantic-review campaign requires exactly 240 candidates")
    campaign = campaign_descriptor(args.candidates, rows)
    campaign_sha = campaign["campaign_sha256"]
    work = build_work(rows, args.output_root, args.evidence_root, campaign_sha)
    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                run_batch,
                command(args.candidates, output, evidence, lane, index, args.review_workers),
                output, evidence, expected_rows, campaign_sha, batch_sha,
            ): (lane, index)
            for lane, index, output, evidence, expected_rows, batch_sha in work
        }
        for future in as_completed(futures):
            lane, index = futures[future]
            results[f"{lane}/{index}"] = future.result()

    combined_rows, batches = combine(work, rows, campaign_sha)
    payload = b"".join(canonical_json(row) + b"\n" for row in combined_rows)
    args.combined_output.parent.mkdir(parents=True, exist_ok=True)
    args.combined_output.write_bytes(payload)
    admission_records = [
        {
            "id": candidate["id"],
            "candidate_sha256": semantic["candidate_sha256"],
            "specification_sha256": semantic["specification_sha256"],
            "primary_capability": semantic["primary_capability"],
            "assigned_cross_cutting_dimension": semantic["assigned_cross_cutting_dimension"],
            "verdict": semantic["verdict"],
            "primary_capability_is_substantive": semantic["primary_capability_is_substantive"],
            "generic_edge_case_boilerplate_is_primary": semantic["generic_edge_case_boilerplate_is_primary"],
            "verifier_outputs_visible": False,
            "evaluation_artifacts_read": 0,
            "correction_passes": 0,
            "semantic_evidence_sha256": semantic["evidence_sha256"],
        }
        for candidate, semantic in zip(rows, combined_rows, strict=True)
    ]
    admission_report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-semantic-review-report/v1",
        "status": "complete",
        "visibility": "specification-and-assigned-labels-only",
        "evaluation_artifacts_read": 0,
        "candidate_input_sha256": sha256_file(args.candidates),
        "semantic_evidence_sha256": hashlib.sha256(payload).hexdigest(),
        "records": admission_records,
    }
    admission_report["report_sha256"] = canonical_sha256(admission_report)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(admission_report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    summary: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-semantic-review-campaign/v1",
        "status": "semantic-review-complete-not-admission",
        "campaign": campaign,
        "candidate_input": {
            "path": str(args.candidates), "records": len(rows), "sha256": sha256_file(args.candidates),
        },
        "batches": {
            key: {"execution_status": results[key]["status"], **value}
            for key, value in batches.items()
        },
        "reviewed": len(combined_rows),
        "passed": sum(row["verdict"] == "pass" for row in combined_rows),
        "rejected": sum(row["verdict"] == "reject" for row in combined_rows),
        "combined_output": {
            "path": str(args.combined_output), "records": len(combined_rows),
            "sha256": hashlib.sha256(payload).hexdigest(),
        },
        "admission_report": {
            "path": str(args.report), "records": len(admission_records),
            "sha256": sha256_file(args.report), "report_sha256": admission_report["report_sha256"],
        },
        "maximum_parallel_reviewers": args.workers * args.review_workers,
        "evaluation_artifacts_read": 0,
    }
    summary["summary_sha256"] = canonical_sha256(summary)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "reviewed": summary["reviewed"], "passed": summary["passed"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
