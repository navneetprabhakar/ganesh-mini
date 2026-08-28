#!/usr/bin/env python3
"""Build the deterministic, oversampled expansion-v1 teacher drafting queue."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LANES = ("go", "java", "javascript", "typescript", "python", "rust")
FENCE_ALIASES = {
    "go": "go", "golang": "go", "java": "java", "javascript": "javascript", "js": "javascript",
    "typescript": "typescript", "ts": "typescript", "python": "python", "py": "python", "rust": "rust",
}
PROHIBITED_MARKERS = (
    "humaneval", "mbpp", "multi-p-l-e", "multipl-e", "codefuseeval", "codefuse eval",
    "livecodebench", "swe-bench", "swebench", "lbpp",
)


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def verify_snapshot(path: Path, source: dict[str, Any]) -> None:
    observed = sha256_bytes(path.read_bytes())
    if observed != source["sha256"]:
        raise ValueError(f"{source['dataset']}: expected {source['sha256']}, observed {observed}")


def clean_stimulus(value: str, maximum: int) -> str:
    value = value.strip()
    if len(value) <= maximum:
        return value
    boundary = value.rfind("\n", 0, maximum)
    return value[: boundary if boundary >= maximum // 2 else maximum].rstrip() + "\n[truncated at deterministic queue boundary]"


def prohibited(value: str) -> bool:
    folded = " ".join(value.casefold().split())
    return any(marker in folded for marker in PROHIBITED_MARKERS)


def stable_order(seed: str, source_key: str, record_id: str) -> str:
    return sha256_bytes(f"{seed}\0{source_key}\0{record_id}".encode())


def load_mceval(path: Path, source: dict[str, Any], maximum: int) -> dict[str, list[dict[str, Any]]]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, row in enumerate(rows):
        lane = str(row.get("language", "")).casefold()
        instruction = row.get("instruction")
        if lane not in LANES or not isinstance(instruction, str) or not instruction.strip() or prohibited(instruction):
            continue
        record_id = f"row-{index:05d}"
        result[lane].append({
            "source_key": "mceval", "record_id": record_id,
            "source_record_sha256": sha256_bytes(canonical_json(row)),
            "stimulus": clean_stimulus(instruction, maximum), "source": source,
        })
    return result


def infer_fence_lane(messages: list[dict[str, Any]]) -> str | None:
    text = "\n".join(str(message.get("content", "")) for message in messages)
    lanes = {
        FENCE_ALIASES[tag.casefold()]
        for tag in re.findall(r"```([A-Za-z]+)", text)
        if tag.casefold() in FENCE_ALIASES
    }
    return next(iter(lanes)) if len(lanes) == 1 else None


def load_mdeval(path: Path, source: dict[str, Any], maximum: int) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = defaultdict(list)
    # Iterate physical lines. str.splitlines() also splits Unicode U+2028/U+2029
    # embedded inside valid JSON strings in this pinned source snapshot.
    with path.open(encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            if not line.strip():
                continue
            row = json.loads(line)
            messages = row.get("messages")
            if not isinstance(messages, list):
                continue
            lane = infer_fence_lane(messages)
            user = next((message.get("content") for message in messages if message.get("role") == "user"), None)
            if lane not in LANES or not isinstance(user, str) or not user.strip() or prohibited(user):
                continue
            record_id = f"row-{index:05d}"
            result[lane].append({
                "source_key": "mdeval", "record_id": record_id,
                "source_record_sha256": sha256_bytes(canonical_json(row)),
                "stimulus": clean_stimulus(user, maximum), "source": source,
            })
    return result


def queue_record(item: dict[str, Any], lane: str, task_type: str, ordinal: int) -> dict[str, Any]:
    source = item["source"]
    return {
        "schema_version": "ganesh-mini-expansion-draft/v1",
        "id": f"exp-v1-{lane}-{task_type}-{ordinal:04d}",
        "lane": lane,
        "task_type": task_type,
        "stimulus": item["stimulus"],
        "source": {
            "dataset": source["dataset"], "uri": source["uri"], "revision": source["revision"],
            "record_id": item["record_id"], "license": source["license"],
            "license_uri": source["license_uri"], "source_record_sha256": item["source_record_sha256"],
            "transformation": (
                "Codex teacher creates a new self-contained task inspired by this drafting stimulus; "
                "source answers/tests are not trusted and independent tests see only the transformed specification"
            ),
        },
    }


def build_queue(config: dict[str, Any], mceval_path: Path, mdeval_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    maximum = config["stimulus_max_chars"]
    sources = config["sources"]
    verify_snapshot(mceval_path, sources["mceval"])
    verify_snapshot(mdeval_path, sources["mdeval"])
    mceval = load_mceval(mceval_path, sources["mceval"], maximum)
    mdeval = load_mdeval(mdeval_path, sources["mdeval"], maximum)
    seed = config["seed"]
    queue: list[dict[str, Any]] = []
    availability: dict[str, Any] = {}
    all_mceval = [item for source_lane in LANES for item in mceval[source_lane]]
    for lane in LANES:
        generation_primary = sorted(mceval[lane], key=lambda row: stable_order(seed, row["source_key"], row["record_id"]))
        primary_ids = {(item["source_key"], item["record_id"]) for item in mceval[lane]}
        fallback_items = [*mdeval[lane]]
        if config.get("cross_language_generation_fallback", False):
            fallback_items.extend(
                item for item in all_mceval if (item["source_key"], item["record_id"]) not in primary_ids
            )
        generation_fallback = sorted(
            fallback_items,
            key=lambda row: stable_order(seed + "-generation", row["source_key"], row["record_id"]),
        )
        repair_primary = sorted(mdeval[lane], key=lambda row: stable_order(seed, row["source_key"], row["record_id"]))
        repair_fallback = sorted(mceval[lane], key=lambda row: stable_order(seed + "-repair", row["source_key"], row["record_id"]))
        generation_target = config["candidate_targets"][lane]["generation"]
        repair_target = config["candidate_targets"][lane]["repair"]
        generation_pool = generation_primary[:generation_target]
        if len(generation_pool) < generation_target:
            generation_pool.extend(generation_fallback[: generation_target - len(generation_pool)])
        if len(generation_pool) < generation_target:
            raise ValueError(f"{lane}: only {len(generation_pool)} generation stimuli for {generation_target}")
        repair_pool = repair_primary[:repair_target]
        if len(repair_pool) < repair_target:
            repair_pool.extend(repair_fallback[: repair_target - len(repair_pool)])
        if len(repair_pool) < repair_target:
            raise ValueError(f"{lane}: only {len(repair_pool)} repair stimuli for {repair_target}")
        queue.extend(queue_record(item, lane, "generation", index + 1) for index, item in enumerate(generation_pool[:generation_target]))
        queue.extend(queue_record(item, lane, "repair", index + 1) for index, item in enumerate(repair_pool))
        availability[lane] = {
            "mceval_generation": len(generation_primary), "mdeval_repair": len(repair_primary),
            "generation_fallback_used": max(0, generation_target - len(generation_primary)),
            "repair_fallback_used": max(0, repair_target - len(repair_primary)),
        }
    ids = [row["id"] for row in queue]
    if len(ids) != len(set(ids)):
        raise ValueError("queue contains duplicate IDs")
    counts = Counter((row["lane"], row["task_type"]) for row in queue)
    report = {
        "schema_version": "ganesh-mini-expansion-source-queue-report/v1",
        "status": "passed", "records": len(queue),
        "counts": {lane: {kind: counts[(lane, kind)] for kind in ("generation", "repair")} for lane in LANES},
        "availability": availability,
        "source_files": {
            "mceval": {"path": str(mceval_path), "sha256": sources["mceval"]["sha256"]},
            "mdeval": {"path": str(mdeval_path), "sha256": sources["mdeval"]["sha256"]},
        },
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    return queue, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/data/expansion_queue_v1.json"))
    parser.add_argument("--mceval", type=Path, required=True)
    parser.add_argument("--mdeval", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    queue, report = build_queue(config, args.mceval, args.mdeval)
    payload = b"".join(canonical_json(row) + b"\n" for row in queue)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    report["output"] = {"path": str(args.output), "bytes": len(payload), "sha256": sha256_bytes(payload)}
    report["report_sha256"] = sha256_bytes(canonical_json(report))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "records": len(queue), "sha256": report["output"]["sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
