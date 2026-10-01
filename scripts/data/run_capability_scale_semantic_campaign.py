#!/usr/bin/env python3
"""Run a resumable blind semantic-review campaign for sealed scale candidates."""

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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(value)
    temporary.replace(path)


def load_teacher_candidates(candidates_path: Path, report_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    body = dict(report)
    claimed = body.pop("report_sha256", None)
    rows = load_candidates(candidates_path)
    selected = report.get("selected_request_sha256s")
    request_shas = [row.get("teacher_evidence", {}).get("request_sha256") for row in rows]
    if (
        claimed != canonical_sha256(body)
        or report.get("schema_version") != "ganesh-mini-capability-scale-teacher-report/v1"
        or report.get("status") != "passed"
        or report.get("requested") != len(rows)
        or report.get("counts") != {"generated": len(rows)}
        or report.get("candidates_sha256") != canonical_sha256(rows)
        or not isinstance(selected, list)
        or selected != request_shas
        or len(set(selected)) != len(rows)
        or report.get("evaluation_artifacts_read") != 0
        or any(row.get("teacher_evidence", {}).get("evaluation_artifacts_read") != 0 for row in rows)
    ):
        raise ValueError("teacher candidates/report differ from their sealed scale contract")
    return rows, report


def batch_descriptor(
    campaign_sha256: str, lane: str, batch_index: int, rows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "campaign_sha256": campaign_sha256,
        "lane": lane,
        "batch_index": batch_index,
        "batch_size": BATCH_SIZE,
        "ordered_candidate_ids": [row["id"] for row in rows],
    }


def batch_paths(semantic_dir: Path, lane: str, index: int) -> tuple[Path, Path]:
    stem = f"{lane}-{index:03d}"
    return semantic_dir / f"{stem}.semantic.jsonl", semantic_dir / f"{stem}.evidence.json"


def build_work(
    rows: list[dict[str, Any]], semantic_dir: Path, campaign_sha: str,
) -> list[tuple[str, int, Path, Path, list[dict[str, Any]], str]]:
    work: list[tuple[str, int, Path, Path, list[dict[str, Any]], str]] = []
    for lane in LANES:
        lane_rows = [row for row in rows if row["lane"] == lane]
        for start in range(0, len(lane_rows), BATCH_SIZE):
            index = start // BATCH_SIZE
            selected = lane_rows[start:start + BATCH_SIZE]
            output, evidence = batch_paths(semantic_dir, lane, index)
            descriptor = batch_descriptor(campaign_sha, lane, index, selected)
            work.append((lane, index, output, evidence, selected, canonical_sha256(descriptor)))
    if not work or sum(len(item[4]) for item in work) != len(rows):
        raise ValueError("semantic campaign does not exactly cover its candidates")
    return work


def verify_completed(
    output: Path, evidence_path: Path, expected_rows: list[dict[str, Any]],
    campaign_sha: str, batch_sha: str,
) -> dict[str, Any] | None:
    expected_ids = [row["id"] for row in expected_rows]
    outer = verify_review_batch(output, evidence_path, expected_ids, campaign_sha, batch_sha)
    if outer is None:
        return None
    semantic_rows = read_jsonl(output)
    expected_hashes = [candidate_sha256(row) for row in expected_rows]
    if (
        outer.get("schema_version") != "ganesh-mini-capability-semantic-review-batch/v1"
        or outer.get("reviewed") != len(expected_rows)
        or outer.get("evaluation_artifacts_read") != 0
        or outer.get("campaign", {}).get("campaign_sha256") != campaign_sha
        or canonical_sha256(outer.get("batch", {})) != batch_sha
        or [row.get("candidate_sha256") for row in semantic_rows] != expected_hashes
    ):
        raise ValueError(f"semantic-review batch fails campaign contract: {output}")
    for candidate, semantic in zip(expected_rows, semantic_rows, strict=True):
        assignment = candidate["qualification_assignment"]
        visibility = semantic.get("visibility", {})
        substantive = semantic.get("primary_capability_is_substantive")
        generic = semantic.get("generic_edge_case_boilerplate_is_primary")
        if (
            load_evidence(semantic) is None
            or semantic.get("specification_sha256") != sha256_text(candidate["messages"][0]["content"])
            or semantic.get("primary_capability") != assignment["primary_capability"]
            or semantic.get("assigned_cross_cutting_dimension")
            != assignment["assigned_cross_cutting_dimension"]
            or semantic.get("verdict") not in {"pass", "reject"}
            or (semantic.get("verdict") == "pass") != (substantive is True and generic is False)
            or visibility.get("specification_and_assigned_labels_only") is not True
            or visibility.get("evaluation_artifacts_read") != 0
        ):
            raise ValueError(f"{candidate['id']}: semantic evidence fails candidate binding")
    return {
        "reviewed": len(semantic_rows),
        "passed": sum(row["verdict"] == "pass" for row in semantic_rows),
        "rejected": sum(row["verdict"] == "reject" for row in semantic_rows),
        "evidence_sha256": outer["evidence_sha256"],
        "output_sha256": sha256_file(output),
    }


def review_command(
    candidates: Path, output: Path, evidence: Path, lane: str, index: int,
    review_workers: int, teacher_config: Path, codex_bin: str,
) -> list[str]:
    return [
        sys.executable, str(ROOT / "scripts/data/review_capability_qualification.py"),
        "--teacher-config", str(teacher_config), "--codex-bin", codex_bin,
        "--candidates", str(candidates), "--lane", lane,
        "--batch-index", str(index), "--batch-size", str(BATCH_SIZE),
        "--workers", str(review_workers), "--output", str(output),
        "--evidence", str(evidence),
    ]


def run_batch(
    argv: list[str], output: Path, evidence: Path, expected_rows: list[dict[str, Any]],
    campaign_sha: str, batch_sha: str,
) -> dict[str, Any]:
    completed = verify_completed(output, evidence, expected_rows, campaign_sha, batch_sha)
    if completed is not None:
        return completed
    output.parent.mkdir(parents=True, exist_ok=True)
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
    return completed


def combine(
    work: list[tuple[str, int, Path, Path, list[dict[str, Any]], str]],
    canonical_rows: list[dict[str, Any]], campaign_sha: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_candidate: dict[str, dict[str, Any]] = {}
    batches: list[dict[str, Any]] = []
    for lane, index, output, evidence, expected_rows, batch_sha in work:
        verified = verify_completed(output, evidence, expected_rows, campaign_sha, batch_sha)
        if verified is None:
            raise RuntimeError(f"completed semantic-review campaign is missing {lane}/{index}")
        batches.append({
            "lane": lane, "batch_index": index,
            "ordered_candidate_ids": [row["id"] for row in expected_rows],
            "batch_sha256": batch_sha, **verified,
        })
        for semantic in read_jsonl(output):
            key = semantic["candidate_sha256"]
            if key in by_candidate:
                raise ValueError("semantic campaign contains duplicate candidate evidence")
            by_candidate[key] = semantic
    expected = [candidate_sha256(row) for row in canonical_rows]
    if len(set(expected)) != len(expected) or set(by_candidate) != set(expected):
        raise ValueError("semantic campaign does not exactly cover its candidate input")
    return [by_candidate[key] for key in expected], batches


def build_terminal_artifacts(
    candidates: list[dict[str, Any]], semantic_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if len(candidates) != len(semantic_rows):
        raise ValueError("semantic terminal inputs differ in length")
    terminal: list[dict[str, Any]] = []
    for candidate, semantic in zip(candidates, semantic_rows, strict=True):
        if (
            semantic.get("candidate_sha256") != candidate_sha256(candidate)
            or load_evidence(semantic) is None
            or semantic.get("verdict") not in {"pass", "reject"}
            or semantic.get("visibility", {}).get("evaluation_artifacts_read") != 0
        ):
            raise ValueError(f"{candidate.get('id')}: cannot build terminal semantic artifact")
        artifact: dict[str, Any] = {
            "schema_version": "ganesh-mini-capability-scale-semantic-terminal/v1",
            "candidate_id": candidate["id"],
            "cell_id": candidate["qualification_assignment"]["cell_id"],
            "status": "passed" if semantic["verdict"] == "pass" else "semantic-rejected",
            "candidate_sha256": semantic["candidate_sha256"],
            "semantic_evidence": semantic,
            "semantic_evidence_sha256": semantic["evidence_sha256"],
            "evaluation_artifacts_read": 0,
        }
        artifact["artifact_sha256"] = canonical_sha256(artifact)
        terminal.append(artifact)
    return terminal


def build_report(
    candidates_path: Path, teacher_report: dict[str, Any], campaign: dict[str, Any],
    combined_rows: list[dict[str, Any]], terminal: list[dict[str, Any]],
    batches: list[dict[str, Any]], combined_sha: str,
) -> dict[str, Any]:
    if len(combined_rows) != len(terminal):
        raise ValueError("semantic report inputs differ in length")
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-scale-semantic-campaign/v1",
        "status": "complete",
        "requested": len(terminal),
        "teacher_report_sha256": teacher_report["report_sha256"],
        "candidate_input_sha256": sha256_file(candidates_path),
        "campaign_sha256": campaign["campaign_sha256"],
        "ordered_candidate_ids": campaign["ordered_candidate_ids"],
        "counts": {
            "reviewed": len(combined_rows),
            "passed": sum(row["verdict"] == "pass" for row in combined_rows),
            "rejected": sum(row["verdict"] == "reject" for row in combined_rows),
        },
        "combined_semantic_sha256": combined_sha,
        "ordered_semantic_evidence_sha256s": [row["evidence_sha256"] for row in combined_rows],
        "terminal_rows_sha256": canonical_sha256(terminal),
        "terminal_artifact_sha256s": [row["artifact_sha256"] for row in terminal],
        "batches": batches,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--teacher-report", type=Path, required=True)
    parser.add_argument("--semantic-dir", type=Path, required=True)
    parser.add_argument("--combined-output", type=Path, required=True)
    parser.add_argument(
        "--terminal-output", type=Path,
        help="sealed per-candidate terminal JSONL; defaults beside --report",
    )
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--teacher-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--review-workers", type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.workers <= 12 or not 1 <= args.review_workers <= 4 or args.workers * args.review_workers > 12:
        raise ValueError("workers must be 1..12, review-workers 1..4, and their product at most 12")

    rows, teacher_report = load_teacher_candidates(args.candidates, args.teacher_report)
    campaign = campaign_descriptor(args.candidates, rows)
    work = build_work(rows, args.semantic_dir, campaign["campaign_sha256"])
    expected_outputs = {item[2] for item in work} | {item[3] for item in work}
    if args.semantic_dir.exists():
        actual = set(args.semantic_dir.glob("*.semantic.jsonl")) | set(args.semantic_dir.glob("*.evidence.json"))
        if actual - expected_outputs:
            raise ValueError("semantic directory contains batches outside this sealed campaign")

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                run_batch,
                review_command(
                    args.candidates, output, evidence, lane, index, args.review_workers,
                    args.teacher_config, args.codex_bin,
                ),
                output, evidence, selected, campaign["campaign_sha256"], batch_sha,
            ): (lane, index)
            for lane, index, output, evidence, selected, batch_sha in work
        }
        for future in as_completed(futures):
            future.result()

    combined_rows, batches = combine(work, rows, campaign["campaign_sha256"])
    payload = b"".join(canonical_json(row) + b"\n" for row in combined_rows)
    atomic_bytes(args.combined_output, payload)
    terminal = build_terminal_artifacts(rows, combined_rows)
    terminal_payload = b"".join(canonical_json(row) + b"\n" for row in terminal)
    terminal_output = args.terminal_output or args.report.with_name("terminal-artifacts.jsonl")
    atomic_bytes(terminal_output, terminal_payload)
    report = build_report(
        args.candidates, teacher_report, campaign, combined_rows, terminal, batches,
        hashlib.sha256(payload).hexdigest(),
    )
    atomic_bytes(args.report, json.dumps(report, indent=2, sort_keys=True).encode() + b"\n")
    print(json.dumps({"status": report["status"], "counts": report["counts"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
