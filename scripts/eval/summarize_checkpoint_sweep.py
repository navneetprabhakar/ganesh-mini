#!/usr/bin/env python3
"""Summarize a diagnostic checkpoint sweep without selecting a release candidate."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.eval.adjudicate_expansion_canary import FAMILY, LANES, canonical_digest, load_sealed, task_rows


def metrics(rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    lanes = Counter({lane: 0 for lane in LANES})
    families: Counter[str] = Counter()
    for row in rows.values():
        lanes[row["lane"]] += int(row["passed"])
        families[row["family"]] += int(row["passed"])
    return {"passes": sum(lanes.values()), "passes_by_lane": dict(lanes), "passes_by_family": dict(families)}


def build(manifest_path: Path, base_dir: Path, results_dir: Path, final_tasks: Path) -> dict[str, Any]:
    manifest = load_sealed(manifest_path, "manifest_sha256")
    if manifest.get("status") != "diagnostic-only" or manifest.get("promotion_authority") != "none":
        raise ValueError("checkpoint sweep manifest is not diagnostic-only")
    labels = sorted(manifest.get("config_sha256", {}))
    if len(labels) != manifest.get("unmeasured_checkpoint_count"):
        raise ValueError("checkpoint sweep config accounting mismatch")
    final = task_rows(final_tasks)
    base = task_rows(base_dir, set(final))
    baseline = metrics(base)
    rows = []
    for label in [*labels, manifest["measured_final_checkpoint"]]:
        candidate = final if label == manifest["measured_final_checkpoint"] else task_rows(results_dir / label / "tasks")
        if set(candidate) != set(base):
            raise ValueError(f"checkpoint task set mismatch: {label}")
        observed = metrics(candidate)
        improved = sum(observed["passes_by_family"].get(name, 0) > baseline["passes_by_family"].get(name, 0) for name in set(FAMILY.values()))
        rows.append({
            "checkpoint": label,
            **observed,
            "net_pass_gain": observed["passes"] - baseline["passes"],
            "improved_product_families": improved,
        })
    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-checkpoint-sweep-result/v1",
        "status": "complete-diagnostic",
        "sweep_manifest_sha256": manifest["manifest_sha256"],
        "training_run_evidence_sha256": manifest["training_run_evidence_sha256"],
        "task_count": len(base),
        "base": baseline,
        "checkpoints": rows,
        "maximum_improved_product_families": max(row["improved_product_families"] for row in rows),
        "promotion_authority": "none",
    }
    report["report_sha256"] = canonical_digest(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--base-tasks", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--final-tasks", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = build(args.manifest, args.base_tasks, args.results, args.final_tasks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "maximum_improved_product_families": report["maximum_improved_product_families"], "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
