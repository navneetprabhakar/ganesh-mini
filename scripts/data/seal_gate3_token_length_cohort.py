#!/usr/bin/env python3
"""Seal the corrected 720-row capability cohort after one approved replacement."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256
from scripts.data.build_capability_scale_queue import PLAN_SHA256
from scripts.data.select_capability_broad_replay import _capability_rows
from scripts.data.seal_capability_720 import PASS_FIELDS


REPLACEMENT_PLAN_SHA256 = "1844d190adcdc47496fc18fa9ec94babaeb469931985b384ac0c575726d4b13c"
AFFECTED = "binary_and_bitwise"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sealed(path: Path, key: str = "report_sha256") -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    if body.pop(key, None) != canonical_sha256(body):
        raise ValueError(f"invalid seal: {path}")
    return value


def seal(capability_path: Path, assembly_path: Path, scale_separation_path: Path,
         old_quality_dir: Path, new_quality_dir: Path, approved_plan: Path) -> dict:
    if file_sha(approved_plan) != REPLACEMENT_PLAN_SHA256:
        raise ValueError("approved replacement plan hash drift")
    rows = [json.loads(line) for line in capability_path.read_text(encoding="utf-8").splitlines()]
    assembly = sealed(assembly_path)
    separation = sealed(scale_separation_path)
    old_quality = sealed(old_quality_dir / "quality-review-report.json")
    new_quality = sealed(new_quality_dir / "quality-review-report.json")
    if (len(rows) != 720 or assembly.get("capability_rows_sha256") != canonical_sha256(rows) or
        assembly.get("status") != "provisional-separation-and-quality-pending" or
        separation.get("status") != "passed" or len(separation.get("records", [])) != 546 or
        old_quality.get("status") != "passed" or new_quality.get("status") != "passed" or
        new_quality.get("assembly_report_sha256") != assembly["report_sha256"] or
        new_quality.get("scale_separation_report_sha256") != separation["report_sha256"] or
        new_quality.get("historical_quality_report_sha256") != old_quality["report_sha256"]):
        raise ValueError("assembly, separation, or quality evidence differs")
    by_id = {row["id"]: row for row in rows}
    scale_ids = {row["id"] for row in rows if row["id"].startswith("cap-scale-")}
    if len(by_id) != 720 or len(scale_ids) != 546:
        raise ValueError("corrected cohort ID shape differs")
    if {item.get("id") for item in separation["records"]} != scale_ids or any(
        any(item.get(field) is not True for field in PASS_FIELDS) for item in separation["records"]
    ):
        raise ValueError("scale separation does not pass exact corrected rows")
    reviews = []
    for kind in ("generation", "repair"):
        artifact = sealed(old_quality_dir / f"{kind}-review.json", "artifact_sha256")
        if artifact.get("reviewer_kind") != "independent-codex-cli" or artifact.get("evaluation_artifacts_read") != 0:
            raise ValueError("historical reviewer metadata differs")
        for item in artifact.get("items", []):
            identifier = item["id"]
            row = by_id.get(identifier)
            if row is None:
                raise ValueError("historical reviewed row no longer exists")
            cap = row["qualification_assignment"]["primary_capability"]
            if cap == AFFECTED:
                continue
            index = artifact["candidate_ids"].index(identifier)
            if artifact["candidate_sha256s"][index] != canonical_sha256(row) or item.get("verdict") != "pass" or not all(item["checks"].values()):
                raise ValueError("historical quality review does not bind passing row")
            reviews.append((cap, identifier, artifact["reviewer_id"]))
    for kind in ("generation", "repair"):
        artifact = sealed(new_quality_dir / f"{kind}-review.json", "artifact_sha256")
        identifier = artifact.get("candidate_id")
        row = by_id.get(identifier)
        if (row is None or row["qualification_assignment"]["primary_capability"] != AFFECTED or
            row.get("task_type") != kind or artifact.get("candidate_sha256") != canonical_sha256(row) or
            artifact.get("reviewer_kind") != "independent-codex-cli" or artifact.get("evaluation_artifacts_read") != 0 or
            len(artifact.get("items", [])) != 1 or artifact["items"][0].get("verdict") != "pass" or
            not all(artifact["items"][0]["checks"].values())):
            raise ValueError("replacement quality review does not bind passing row")
        reviews.append((AFFECTED, identifier, artifact["reviewer_id"]))
    by_cap = defaultdict(list)
    for cap, identifier, reviewer in reviews:
        by_cap[cap].append((identifier, reviewer))
    if set(by_cap) != set(CAPABILITIES) or any(len(items) != 2 or len({i for i, _ in items}) != 2 or
                                                  len({r for _, r in items}) != 2 for items in by_cap.values()):
        raise ValueError("two blind reviews per primary capability absent")
    manifest = {
        "schema_version": "ganesh-mini-gate3-capability-720-seal/v1",
        "status": "passed",
        "plan_sha256": PLAN_SHA256,
        "prospective_replacement_plan_sha256": REPLACEMENT_PLAN_SHA256,
        "records": 720,
        "capability_rows_sha256": file_sha(capability_path),
        "unique_record_ids": 720,
        "unique_source_identities": 720,
        "assembly_report_sha256": assembly["report_sha256"],
        "scale_separation_report_sha256": separation["report_sha256"],
        "historical_quality_report_sha256": old_quality["report_sha256"],
        "replacement_quality_report_sha256": new_quality["report_sha256"],
        "quality_reviewers": "two independent blind AI content reviewers per capability; no human sign-off claimed",
        "evaluation_artifacts_read": 0,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    _capability_rows(capability_path.read_bytes(), manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("capability", "assembly_report", "scale_separation", "historical_quality_dir", "replacement_quality_dir", "approved_plan", "output"):
        parser.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("output already exists")
    manifest = seal(args.capability, args.assembly_report, args.scale_separation,
                    args.historical_quality_dir, args.replacement_quality_dir, args.approved_plan)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": "passed", "records": 720, "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
