#!/usr/bin/env python3
"""Run the 24 resumable capability-qualification teacher batches in parallel."""

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

from scripts.data.build_capability_corpus_plan import canonical_sha256, load_sealed
from scripts.data.generate_capability_qualification import LANES, load_queue


BATCH_SIZE = 10


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def batch_paths(output_root: Path, evidence_root: Path, lane: str, index: int) -> tuple[Path, Path]:
    stem = f"{lane}-{index:03d}"
    return output_root / f"{stem}.candidates.jsonl", evidence_root / f"{stem}.evidence.json"


def verify_completed(output: Path, evidence_path: Path, expected_ids: list[str]) -> dict[str, Any] | None:
    if not output.exists() and not evidence_path.exists():
        return None
    if not output.is_file() or not evidence_path.is_file():
        raise ValueError(f"partial teacher artifacts: {output} / {evidence_path}")
    evidence = load_sealed(evidence_path, "evidence_sha256")
    rows = read_jsonl(output)
    if (
        evidence.get("candidate_output_sha256") != sha256_file(output)
        or evidence.get("generated") != len(expected_ids)
        or evidence.get("failures") != []
        or evidence.get("selection", {}).get("requested_ids") != expected_ids
        or evidence.get("selection", {}).get("evaluation_surfaces_read") != 0
        or [row.get("id") for row in rows] != expected_ids
    ):
        raise ValueError(f"existing teacher batch fails its sealed contract: {output}")
    return {"status": "reused", "generated": len(rows), "evidence_sha256": evidence["evidence_sha256"]}


def command(
    queue: Path,
    manifest: Path,
    output: Path,
    evidence: Path,
    lane: str,
    index: int,
    teacher_workers: int,
) -> list[str]:
    return [
        sys.executable,
        str(ROOT / "scripts/data/generate_capability_qualification.py"),
        "--queue", str(queue),
        "--queue-manifest", str(manifest),
        "--lane", lane,
        "--batch-index", str(index),
        "--batch-size", str(BATCH_SIZE),
        "--teacher-workers", str(teacher_workers),
        "--output", str(output),
        "--evidence", str(evidence),
    ]


def run_batch(argv: list[str], output: Path, evidence: Path, expected_ids: list[str]) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    completed = verify_completed(output, evidence, expected_ids)
    if completed is not None:
        return completed
    result = subprocess.run(
        argv,
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=7200,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"teacher batch failed ({result.returncode}): {' '.join(argv)}\n"
            f"stdout={result.stdout}\nstderr={result.stderr}"
        )
    sealed = verify_completed(output, evidence, expected_ids)
    if sealed is None:
        raise RuntimeError("teacher batch succeeded without sealed artifacts")
    sealed["status"] = "generated"
    return sealed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--combined-output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--teacher-workers", type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.workers <= 6 or not 1 <= args.teacher_workers <= 2:
        raise ValueError("workers must be 1..6 and teacher-workers must be 1..2")

    rows, manifest = load_queue(args.queue, args.queue_manifest)
    work: list[tuple[str, int, Path, Path, list[str]]] = []
    for lane in LANES:
        lane_rows = [row for row in rows if row["lane"] == lane]
        if len(lane_rows) != 40:
            raise ValueError(f"{lane}: expected exactly 40 queue rows")
        for index in range(4):
            selected = lane_rows[index * BATCH_SIZE:(index + 1) * BATCH_SIZE]
            output, evidence = batch_paths(args.output_root, args.evidence_root, lane, index)
            work.append((lane, index, output, evidence, [row["id"] for row in selected]))

    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                run_batch,
                command(args.queue, args.queue_manifest, output, evidence, lane, index, args.teacher_workers),
                output,
                evidence,
                expected_ids,
            ): (lane, index)
            for lane, index, output, evidence, expected_ids in work
        }
        for future in as_completed(futures):
            lane, index = futures[future]
            results[f"{lane}/{index}"] = future.result()

    combined_rows: list[dict[str, Any]] = []
    for lane, index, output, evidence, expected_ids in work:
        verified = verify_completed(output, evidence, expected_ids)
        if verified is None:
            raise RuntimeError(f"completed campaign is missing {lane}/{index}")
        combined_rows.extend(read_jsonl(output))
    combined_payload = b"".join(
        json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
        for row in combined_rows
    )
    args.combined_output.parent.mkdir(parents=True, exist_ok=True)
    args.combined_output.write_bytes(combined_payload)

    summary: dict[str, Any] = {
        "schema_version": "ganesh-mini-capability-qualification-teacher-campaign/v1",
        "status": "teacher-generation-complete-not-admission",
        "queue_manifest_sha256": manifest["manifest_sha256"],
        "batches": dict(sorted(results.items())),
        "generated": sum(item["generated"] for item in results.values()),
        "combined_output": {
            "path": str(args.combined_output),
            "records": len(combined_rows),
            "sha256": hashlib.sha256(combined_payload).hexdigest(),
        },
        "evaluation_surfaces_read": 0,
    }
    summary["summary_sha256"] = canonical_sha256(summary)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "generated": summary["generated"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
