#!/usr/bin/env python3
"""Run resumable adaptive expansion-v1 construction with bounded parallel lane workers."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from scripts.data.admit_expansion import _tokens, canonical_json, normalized_sha256, simhash


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
PILOT_BATCHES = {
    "go": ("000",), "java": ("000",), "javascript": ("000",),
    "typescript": ("000", "001"), "python": ("000",), "rust": ("000", "001"),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> str:
    payload = b"".join(canonical_json(row) + b"\n" for row in rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)
    return sha256_bytes(payload)


def write_state(path: Path, state: dict[str, Any]) -> None:
    payload = json.dumps(state, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(path)


def run(command: list[str], root: Path, timeout: int = 7200, allowed: set[int] | None = None) -> str:
    result = subprocess.run(
        command, cwd=root, stdin=subprocess.DEVNULL, capture_output=True, text=True,
        timeout=timeout, check=False,
    )
    if result.returncode not in (allowed or {0}):
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(command)}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    return result.stdout.strip()


class Corpus:
    def __init__(self, rows: list[dict[str, Any]], targets: dict[str, dict[str, int]]) -> None:
        existing = list(rows)
        self.rows: list[dict[str, Any]] = []
        self.targets = targets
        self.ids: set[str] = set()
        self.prompts: dict[str, str] = {}
        self.conversations: set[str] = set()
        self.fuzzy: list[tuple[int, str, int]] = []
        self.counts: Counter[tuple[str, str]] = Counter()
        for row in existing:
            reason = self.add(row, enforce_target=False)
            if reason is not None:
                raise ValueError(f"existing corpus row {row.get('id')}: {reason}")

    def add(self, row: dict[str, Any], enforce_target: bool = True) -> str | None:
        lane, task_type = row["lane"], row["task_type"]
        if enforce_target and self.counts[(lane, task_type)] >= self.targets[lane][task_type]:
            return "quota already met"
        prompt = row["messages"][0]["content"]
        prompt_hash = normalized_sha256(prompt)
        conversation_hash = row["content_hashes"]["conversation_sha256"]
        if row["id"] in self.ids:
            return "duplicate id"
        if prompt_hash in self.prompts:
            return f"exact prompt duplicate of {self.prompts[prompt_hash]}"
        if conversation_hash in self.conversations:
            return "exact conversation duplicate"
        token_count = len(_tokens(prompt))
        candidate_hash = simhash(prompt) if token_count >= 12 else None
        if candidate_hash is not None:
            for other_hash, other_id, other_tokens in self.fuzzy:
                if other_tokens >= 12 and (candidate_hash ^ other_hash).bit_count() <= 3:
                    return f"fuzzy prompt duplicate of {other_id}"
        self.rows.append(row)
        self.ids.add(row["id"]); self.prompts[prompt_hash] = row["id"]
        self.conversations.add(conversation_hash); self.counts[(lane, task_type)] += 1
        if candidate_hash is not None:
            self.fuzzy.append((candidate_hash, row["id"], token_count))
        return None

    def deficit(self, lane: str, task_type: str) -> int:
        return self.targets[lane][task_type] - self.counts[(lane, task_type)]

    def lane_complete(self, lane: str) -> bool:
        return all(self.deficit(lane, task_type) == 0 for task_type in ("generation", "repair"))


def frozen_targets(config: dict[str, Any]) -> dict[str, dict[str, int]]:
    return {
        lane: {
            "generation": int(config["lane_targets"][lane] * 0.6),
            "repair": int(config["lane_targets"][lane] * 0.4),
        }
        for lane in LANES
    }


def initial_pilot(root: Path, targets: dict[str, dict[str, int]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cache = root / "datasets/cache/expansion-v1"
    measurement = root / "measurement/data/expansion-v1"
    corpus = Corpus([], targets)
    batches: list[dict[str, Any]] = []
    consumed = {lane: {"generation": 0, "repair": 0} for lane in LANES}
    for lane in LANES:
        for index in PILOT_BATCHES[lane]:
            admitted_path = cache / f"source-pilot-{lane}-{index}-lineage.admitted.jsonl"
            report = json.loads((measurement / f"source-pilot-{lane}-{index}-lineage.admission.json").read_text(encoding="utf-8"))
            for row in read_jsonl(admitted_path):
                reason = corpus.add(row)
                if reason is not None:
                    raise ValueError(f"pilot row {row['id']}: {reason}")
            consumed[lane]["generation"] += 6
            consumed[lane]["repair"] += 4
            batches.append({
                "kind": "pilot", "lane": lane, "index": index,
                "accepted": report["accepted"], "rejected": len(report["rejected"]),
                "admission_report_sha256": report["report_sha256"],
            })
    return corpus.rows, {"consumed": consumed, "batches": batches}


def selection(corpus: Corpus, lane: str, consumed: dict[str, int], limits: dict[str, int]) -> dict[str, int]:
    generation_deficit = corpus.deficit(lane, "generation")
    repair_deficit = corpus.deficit(lane, "repair")
    generation_available = limits["generation"] - consumed["generation"]
    repair_available = limits["repair"] - consumed["repair"]
    if generation_deficit and generation_available <= 0:
        raise RuntimeError(f"{lane}: generation reserve exhausted with deficit {generation_deficit}")
    if repair_deficit and repair_available <= 0:
        raise RuntimeError(f"{lane}: repair reserve exhausted with deficit {repair_deficit}")
    if generation_deficit and repair_deficit:
        generation_count = min(6, generation_available, generation_deficit)
        repair_count = min(4, repair_available, repair_deficit)
    elif generation_deficit:
        generation_count = min(10, generation_available, generation_deficit)
        repair_count = 0
    else:
        generation_count = 0
        repair_count = min(10, repair_available, repair_deficit)
    return {
        "generation_start": consumed["generation"], "generation_count": generation_count,
        "repair_start": consumed["repair"], "repair_count": repair_count,
    }


def verify_reusable_candidates(candidate: Path, evidence_path: Path, lane: str, plan: dict[str, int]) -> None:
    if not candidate.is_file() or not evidence_path.is_file():
        raise ValueError("recoverable batch is missing sealed candidate or teacher evidence")
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    if evidence.get("candidate_output_sha256") != sha256_bytes(candidate.read_bytes()):
        raise ValueError("recoverable batch candidate hash differs from teacher evidence")
    expected = {"lane": lane, **plan}
    if evidence.get("selection") != expected:
        raise ValueError("recoverable batch selection differs from teacher evidence")


def unfinished_batch(state: dict[str, Any], lane: str) -> dict[str, Any] | None:
    rows = [
        item for item in state["batches"]
        if item.get("kind") == "production" and item.get("lane") == lane
        and item.get("status") in {"failed", "running"}
    ]
    if len(rows) > 1:
        raise ValueError(f"{lane}: multiple unfinished production batches")
    return rows[0] if rows else None


def verifier_infrastructure_rejections(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        row for row in report.get("rejected", [])
        if "verifier infrastructure failure:" in str(row.get("reason", ""))
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--queue", type=Path, default=Path("datasets/cache/expansion-v1/source-reserve-queue-v1.jsonl"))
    parser.add_argument("--workers", type=int, default=len(LANES))
    parser.add_argument("--max-new-batches", type=int, help="bounded controller qualification/resume run")
    parser.add_argument("--recover-only", action="store_true", help="finish existing failed/running batches without starting new ones")
    parser.add_argument("--state", type=Path, default=Path("datasets/cache/expansion-v1/production/state.json"))
    parser.add_argument("--corpus", type=Path, default=Path("datasets/cache/expansion-v1/production/admitted.jsonl"))
    parser.add_argument("--lock-file", type=Path, default=Path("datasets/cache/expansion-v1/production/controller.lock"))
    args = parser.parse_args()
    root = args.root.resolve()
    queue = (root / args.queue).resolve()
    state_path = (root / args.state).resolve()
    corpus_path = (root / args.corpus).resolve()
    lock_path = (root / args.lock_file).resolve()
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    controller_lock = lock_path.open("a+", encoding="utf-8")
    try:
        fcntl.flock(controller_lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        raise RuntimeError(f"another expansion production controller holds {lock_path}") from exc
    controller_lock.seek(0); controller_lock.truncate()
    controller_lock.write(f"{os.getpid()}\n"); controller_lock.flush()
    expansion_config = json.loads((root / "configs/data/expansion_v1.json").read_text(encoding="utf-8"))
    reserve_config = json.loads((root / "configs/data/expansion_queue_v1.json").read_text(encoding="utf-8"))
    targets = frozen_targets(expansion_config)
    queue_sha = sha256_bytes(queue.read_bytes())
    reserve_report = json.loads((root / "measurement/data/expansion-v1/source-reserve-queue-v1-report.json").read_text(encoding="utf-8"))
    if reserve_report["output"]["sha256"] != queue_sha:
        raise ValueError("reserve queue does not match sealed report")
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state["queue_sha256"] != queue_sha or state["targets"] != targets:
            raise ValueError("production state queue/targets mismatch")
        rows = read_jsonl(corpus_path)
        if state["corpus_sha256"] != sha256_bytes(corpus_path.read_bytes()):
            raise ValueError("production corpus hash differs from state")
    else:
        rows, pilot = initial_pilot(root, targets)
        corpus_sha = write_jsonl(corpus_path, rows)
        state = {
            "schema_version": "ganesh-mini-expansion-production-state/v1", "status": "running",
            "queue_sha256": queue_sha, "targets": targets, "consumed": pilot["consumed"],
            "batches": pilot["batches"], "aggregation_rejections": [],
            "corpus_path": str(corpus_path.relative_to(root)), "corpus_sha256": corpus_sha,
        }
        write_state(state_path, state)
    corpus = Corpus([], targets)
    for row in rows:
        reason = corpus.add(row)
        if reason is not None:
            raise ValueError(f"existing corpus row {row['id']}: {reason}")
    state_lock = threading.Lock()
    stop = threading.Event()
    new_batches_started = 0

    def persist() -> None:
        state["corpus_sha256"] = write_jsonl(corpus_path, corpus.rows)
        state["counts"] = {
            lane: {kind: corpus.counts[(lane, kind)] for kind in ("generation", "repair")} for lane in LANES
        }
        write_state(state_path, state)

    def lane_worker(lane: str) -> None:
        nonlocal new_batches_started
        limits = reserve_config["candidate_targets"][lane]
        while not stop.is_set():
            with state_lock:
                if corpus.lane_complete(lane):
                    return
                entry = unfinished_batch(state, lane)
                recovering = entry is not None
                if recovering:
                    plan = entry["selection"]
                    name = entry["name"]
                    if entry["status"] == "failed":
                        entry.setdefault("attempt_errors", []).append({
                            "attempt": entry.get("attempts", 1), "error": entry.pop("error"),
                        })
                    entry["attempts"] = entry.get("attempts", 1) + 1
                    entry["status"] = "running"
                else:
                    if args.recover_only:
                        return
                    if args.max_new_batches is not None and new_batches_started >= args.max_new_batches:
                        return
                    plan = selection(corpus, lane, state["consumed"][lane], limits)
                    sequence = sum(1 for item in state["batches"] if item["kind"] == "production" and item["lane"] == lane)
                    name = (
                        f"{lane}-{sequence:04d}-g{plan['generation_start']:04d}n{plan['generation_count']}"
                        f"-r{plan['repair_start']:04d}n{plan['repair_count']}"
                    )
                    state["consumed"][lane]["generation"] += plan["generation_count"]
                    state["consumed"][lane]["repair"] += plan["repair_count"]
                    new_batches_started += 1
                    entry = {"kind": "production", "lane": lane, "name": name, "status": "running", "selection": plan, "attempts": 1}
                    state["batches"].append(entry)
                state["status"] = "running"
                persist()
            batch_dir = root / "datasets/cache/expansion-v1/production/batches" / name
            batch_dir.mkdir(parents=True, exist_ok=True)
            candidate = batch_dir / "candidates.jsonl"
            teacher = batch_dir / "teacher-evidence.json"
            try:
                if recovering:
                    verify_reusable_candidates(candidate, teacher, lane, plan)
                else:
                    run([
                        sys.executable, "scripts/data/generate_expansion_source_batch.py", "--queue", str(queue),
                        "--lane", lane, "--generation-start", str(plan["generation_start"]),
                        "--generation-count", str(plan["generation_count"]), "--repair-start", str(plan["repair_start"]),
                        "--repair-count", str(plan["repair_count"]), "--output", str(candidate), "--evidence", str(teacher),
                    ], root)
                admitted = batch_dir / "admitted.jsonl"
                report_path = batch_dir / "admission.json"
                run([
                    sys.executable, "scripts/data/admit_expansion.py", "--input", str(candidate),
                    "--output", str(admitted), "--report", str(report_path),
                ], root, allowed={0, 2})
                report = json.loads(report_path.read_text(encoding="utf-8"))
                final_rows = read_jsonl(admitted)
                final_report = report_path
                remaining_rejections = report["rejected"]
                infrastructure_rejections = verifier_infrastructure_rejections(report)
                if infrastructure_rejections:
                    identifiers = ", ".join(str(row.get("id")) for row in infrastructure_rejections)
                    raise RuntimeError(
                        f"verifier infrastructure retries exhausted for {identifiers}; batch preserved for exact recovery"
                    )
                if report["rejected"]:
                    repaired = batch_dir / "repaired.candidates.jsonl"
                    repair_evidence = batch_dir / "repair.teacher-evidence.json"
                    run([
                        sys.executable, "scripts/data/repair_expansion_rejections.py", "--input", str(candidate),
                        "--admission-report", str(report_path), "--output", str(repaired),
                        "--evidence", str(repair_evidence),
                    ], root)
                    original_rows = read_jsonl(candidate)
                    repaired_rows = read_jsonl(repaired)
                    if len(original_rows) != len(repaired_rows):
                        raise ValueError("repair changed batch row count")
                    rejected_ids = {item["id"] for item in report["rejected"]}
                    repair_only: list[dict[str, Any]] = []
                    for before, after in zip(original_rows, repaired_rows, strict=True):
                        if before["id"] != after["id"]:
                            raise ValueError("repair changed batch row order or IDs")
                        if before["id"] in rejected_ids:
                            repair_only.append(after)
                        elif canonical_json(before) != canonical_json(after):
                            raise ValueError(f"repair changed accepted row {before['id']}")
                    repair_only_path = batch_dir / "repair-only.candidates.jsonl"
                    write_jsonl(repair_only_path, repair_only)
                    repaired_admitted = batch_dir / "repair-only.admitted.jsonl"
                    final_report = batch_dir / "repair-only.admission.json"
                    run([
                        sys.executable, "scripts/data/admit_expansion.py", "--input", str(repair_only_path),
                        "--output", str(repaired_admitted), "--report", str(final_report),
                    ], root, allowed={0, 2})
                    final_rows.extend(read_jsonl(repaired_admitted))
                final = json.loads(final_report.read_text(encoding="utf-8"))
                remaining_rejections = final["rejected"]
                with state_lock:
                    accepted_now = 0
                    for row in final_rows:
                        reason = corpus.add(row)
                        if reason is None:
                            accepted_now += 1
                        else:
                            state["aggregation_rejections"].append({"id": row["id"], "batch": name, "reason": reason})
                    entry = next(item for item in state["batches"] if item.get("name") == name)
                    entry.update({
                        "status": "complete", "admitted": accepted_now,
                        "batch_accepted": len(final_rows), "batch_rejected": len(remaining_rejections),
                        "first_report": str(report_path.relative_to(root)),
                        "first_report_sha256": report["report_sha256"],
                        "final_report": str(final_report.relative_to(root)),
                        "final_report_sha256": final["report_sha256"],
                    })
                    persist()
            except Exception as exc:
                with state_lock:
                    entry = next(item for item in state["batches"] if item.get("name") == name)
                    entry.update({"status": "failed", "error": str(exc)})
                    state["status"] = "failed"
                    persist()
                    stop.set()
                return

    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, len(LANES)))) as executor:
        futures = [executor.submit(lane_worker, lane) for lane in LANES]
        for future in as_completed(futures):
            future.result()
    with state_lock:
        complete = all(corpus.lane_complete(lane) for lane in LANES)
        if state.get("status") != "failed":
            state["status"] = "complete" if complete else "paused"
        persist()
    print(json.dumps({"status": state["status"], "counts": state["counts"], "new_batches": new_batches_started}, sort_keys=True))
    return 0 if state["status"] in {"complete", "paused"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
