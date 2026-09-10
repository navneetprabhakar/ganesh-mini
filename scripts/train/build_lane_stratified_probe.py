#!/usr/bin/env python3
"""Build a deterministic six-lane-stratified Gate 4 probe dataset."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
TARGETS = {"go": 0.2, "java": 0.2, "javascript": 0.1, "typescript": 0.1, "python": 0.2, "rust": 0.2}
GROUP_COUNTS = {"go": 2, "java": 2, "javascript": 1, "typescript": 1, "python": 2, "rust": 2}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def keyed_hash(seed: int, purpose: str, source_id: str) -> str:
    return hashlib.sha256(f"{seed}:{purpose}:{source_id}".encode()).hexdigest()


def response_tokens(row: dict[str, Any]) -> int:
    return int(row.get("response_token_count", sum(label != -100 for label in row["labels"])))


def load_source(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    ids = [row["source_id"] for row in rows]
    if not rows or len(ids) != len(set(ids)) or set(row["lane"] for row in rows) != set(LANES):
        raise ValueError("source must contain unique rows across all six lanes")
    if any(len(row["input_ids"]) != len(row["labels"]) or response_tokens(row) <= 0 for row in rows):
        raise ValueError("source contains invalid response-only encodings")
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")


def path_label(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def build(
    source_path: Path,
    train_path: Path,
    retention_path: Path,
    manifest_path: Path,
    *,
    optimizer_groups: int = 64,
    retention_per_lane: int = 10,
    seed: int = 3502,
) -> dict[str, Any]:
    if optimizer_groups <= 0 or retention_per_lane <= 0:
        raise ValueError("positive group and retention sizes are required")
    source = load_source(source_path)
    by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in source:
        by_lane[row["lane"]].append(row)

    retention: list[dict[str, Any]] = []
    available: dict[str, list[dict[str, Any]]] = {}
    for lane in LANES:
        ordered = sorted(by_lane[lane], key=lambda row: (keyed_hash(seed, "retention", row["source_id"]), row["source_id"]))
        if len(ordered) < retention_per_lane + optimizer_groups * GROUP_COUNTS[lane]:
            raise ValueError(f"insufficient unique rows for {lane}")
        held_out_ids = {row["source_id"] for row in ordered[:retention_per_lane]}
        for row in ordered[:retention_per_lane]:
            item = dict(row)
            item.pop("objective_weight", None)
            item["response_token_count"] = response_tokens(item)
            retention.append(item)
        available[lane] = sorted(
            (row for row in by_lane[lane] if row["source_id"] not in held_out_ids),
            key=lambda row: (keyed_hash(seed, "training", row["source_id"]), row["source_id"]),
        )

    cursors = Counter()
    training: list[dict[str, Any]] = []
    group_summaries: list[dict[str, Any]] = []
    for group_index in range(optimizer_groups):
        selected: list[dict[str, Any]] = []
        for lane in LANES:
            start = cursors[lane]
            end = start + GROUP_COUNTS[lane]
            selected.extend(available[lane][start:end])
            cursors[lane] = end
        random.Random(seed + group_index).shuffle(selected)

        lane_response_tokens = Counter()
        for row in selected:
            lane_response_tokens[row["lane"]] += response_tokens(row)
        weighted_group: list[dict[str, Any]] = []
        mass = Counter()
        for row in selected:
            item = dict(row)
            count = response_tokens(item)
            item["response_token_count"] = count
            item["objective_weight"] = TARGETS[item["lane"]] * count / lane_response_tokens[item["lane"]]
            item["optimizer_group"] = group_index
            mass[item["lane"]] += item["objective_weight"]
            weighted_group.append(item)
        if any(abs(mass[lane] - TARGETS[lane]) > 1e-12 for lane in LANES) or abs(sum(mass.values()) - 1.0) > 1e-12:
            raise RuntimeError("optimizer group objective is not exactly lane-stratified")
        training.extend(weighted_group)
        group_summaries.append({
            "optimizer_group": group_index,
            "records_by_lane": dict(Counter(row["lane"] for row in weighted_group)),
            "input_tokens": sum(sum(row["attention_mask"]) for row in weighted_group),
            "response_tokens_by_lane": dict(lane_response_tokens),
            "objective_mass_by_lane": dict(mass),
        })

    retention.sort(key=lambda row: (LANES.index(row["lane"]), keyed_hash(seed, "retention-order", row["source_id"])))
    train_ids = {row["source_id"] for row in training}
    retention_ids = {row["source_id"] for row in retention}
    if len(train_ids) != len(training) or len(retention_ids) != len(retention) or train_ids & retention_ids:
        raise RuntimeError("training and retention selection is not unique and disjoint")
    write_jsonl(train_path, training)
    write_jsonl(retention_path, retention)

    train_counts = Counter(row["lane"] for row in training)
    retention_counts = Counter(row["lane"] for row in retention)
    objective_mass = Counter()
    for row in training:
        objective_mass[row["lane"]] += row["objective_weight"]
    total_mass = sum(objective_mass.values())
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-lane-stratified-probe-data/v1",
        "status": "ready",
        "source": {"path": path_label(source_path), "sha256": file_sha256(source_path), "records": len(source)},
        "selection": {
            "method": "seeded-hash-disjoint-retention-and-lane-queues-v1",
            "seed": seed,
            "optimizer_groups": optimizer_groups,
            "gradient_accumulation_steps": sum(GROUP_COUNTS.values()),
            "records_per_optimizer_group_by_lane": GROUP_COUNTS,
            "objective_target_by_lane_per_optimizer_group": TARGETS,
            "retention_per_lane": retention_per_lane,
        },
        "prepared_train": {
            "path": path_label(train_path),
            "sha256": file_sha256(train_path),
            "records": len(training),
            "input_tokens": sum(sum(row["attention_mask"]) for row in training),
            "response_tokens_by_lane": dict(Counter({lane: sum(response_tokens(row) for row in training if row["lane"] == lane) for lane in LANES})),
            "records_by_lane": dict(train_counts),
            "realized_normalized_objective_mass_by_lane": {lane: objective_mass[lane] / total_mass for lane in LANES},
        },
        "prepared_validation": {
            "purpose": "non-evaluation authorized-training-corpus retention diagnostic",
            "path": path_label(retention_path),
            "sha256": file_sha256(retention_path),
            "records": len(retention),
            "records_by_lane": dict(retention_counts),
            "disjoint_from_training": not bool(train_ids & retention_ids),
        },
        "group_contract": {
            "every_group_contains_all_six_lanes": all(set(group["records_by_lane"]) == set(LANES) for group in group_summaries),
            "every_group_matches_record_target": all(group["records_by_lane"] == GROUP_COUNTS for group in group_summaries),
            "every_group_matches_objective_target": all(all(abs(group["objective_mass_by_lane"][lane] - TARGETS[lane]) <= 1e-12 for lane in LANES) for group in group_summaries),
            "group_input_tokens_min": min(group["input_tokens"] for group in group_summaries),
            "group_input_tokens_max": max(group["input_tokens"] for group in group_summaries),
        },
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "artifacts/train/expansion-pilot-v1/prepared-train.jsonl")
    parser.add_argument("--train", type=Path, default=ROOT / "artifacts/train/expansion-lane-stratified-probe-v3/prepared-train.jsonl")
    parser.add_argument("--retention", type=Path, default=ROOT / "artifacts/train/expansion-lane-stratified-probe-v3/prepared-retention.jsonl")
    parser.add_argument("--manifest", type=Path, default=ROOT / "artifacts/train/expansion-lane-stratified-probe-v3/prepared-dataset-manifest.json")
    parser.add_argument("--optimizer-groups", type=int, default=64)
    parser.add_argument("--retention-per-lane", type=int, default=10)
    parser.add_argument("--seed", type=int, default=3502)
    args = parser.parse_args()
    report = build(args.source.resolve(), args.train.resolve(), args.retention.resolve(), args.manifest.resolve(), optimizer_groups=args.optimizer_groups, retention_per_lane=args.retention_per_lane, seed=args.seed)
    print(json.dumps({"status": report["status"], "records": report["prepared_train"]["records"], "input_tokens": report["prepared_train"]["input_tokens"], "manifest_sha256": report["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
