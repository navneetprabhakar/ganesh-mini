#!/usr/bin/env python3
"""Seal the 720-row Gate 3 capability cohort from immutable upstream evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256
from scripts.data.build_capability_scale_queue import PLAN_SHA256, source_key
from scripts.data.select_capability_broad_replay import _capability_rows


PASS_FIELDS = (
    "exact_training_passed", "normalized_training_passed", "fuzzy_training_passed",
    "exact_evaluation_passed", "normalized_evaluation_passed", "fuzzy_evaluation_passed",
)


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sealed(path: Path, seal_key: str = "report_sha256") -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    seal = body.pop(seal_key, None)
    if seal != canonical_sha256(body):
        raise ValueError(f"{path}: invalid {seal_key}")
    return value


def seal(
    capability_path: Path, provisional_path: Path, entry_path: Path,
    materialized_path: Path, separation_path: Path, review_dir: Path,
) -> dict:
    capability_bytes = capability_path.read_bytes()
    provisional = sealed(provisional_path)
    entry = sealed(entry_path, "manifest_sha256")
    materialized = sealed(materialized_path)
    separation = sealed(separation_path)
    selection = sealed(review_dir / "selection-report.json")
    quality = sealed(review_dir / "quality-review-report.json")
    if (provisional.get("records"), provisional.get("unique_record_ids"),
        provisional.get("unique_source_identities")) != (720, 720, 720):
        raise ValueError("provisional capability counts are not 720/720/720")
    rows = [json.loads(line) for line in capability_bytes.splitlines()]
    if provisional.get("capability_rows_sha256") != canonical_sha256(rows):
        raise ValueError("provisional cohort file binding differs")
    if entry.get("status") != "passed" or entry.get("records") != 174 or provisional.get("entry_manifest_sha256") != entry.get("manifest_sha256"):
        raise ValueError("retained training entry is not the sealed 174-row cohort")
    if materialized.get("status") != "verified-envelopes-separation-pending" or materialized.get("records") != 546:
        raise ValueError("materialized scale evidence is not passed for 546 rows")
    if provisional.get("scale_report_sha256") != materialized.get("report_sha256"):
        raise ValueError("provisional cohort does not bind materialized scale")
    if separation.get("status") != "passed" or separation.get("evaluation_artifacts_read_by_construction") != 0:
        raise ValueError("scale separation has not passed without construction evaluation reads")
    if quality.get("status") != "passed" or quality.get("reviewed") != 20 or quality.get("failed_ids"):
        raise ValueError("blind review did not pass 20 sampled rows")
    if quality.get("selection_report_sha256") != selection.get("report_sha256") or selection.get("population") != 546:
        raise ValueError("quality sample does not bind materialized scale")
    if selection.get("materialized_report_sha256") != materialized.get("report_sha256"):
        raise ValueError("quality selection does not bind materialized scale")
    if any(report.get("evaluation_artifacts_read", 0) != 0 for report in (entry, provisional, materialized, selection, quality)):
        raise ValueError("construction evidence reports evaluation reads")

    if len(rows) != 720:
        raise ValueError("capability cohort is not 720 rows")
    scale_ids = {row["id"] for row in rows if row["id"].startswith("cap-scale-")}
    if len(scale_ids) != 546:
        raise ValueError("capability cohort is not 174 retained plus 546 scale")
    sep_rows = separation.get("records")
    if not isinstance(sep_rows, list) or {item.get("id") for item in sep_rows} != scale_ids:
        raise ValueError("scale separation does not cover the exact 546 rows")
    if any(any(item.get(field) is not True for field in PASS_FIELDS) for item in sep_rows):
        raise ValueError("scale separation has a failed row")
    by_id = {row["id"]: row for row in rows}
    if len(by_id) != 720:
        raise ValueError("duplicate capability record ID")
    if len({source_key(row) for row in rows}) != 720:
        raise ValueError("duplicate capability source identity")

    reviews = []
    reviewer_ids = set()
    for task_type in ("generation", "repair"):
        artifact = sealed(review_dir / f"{task_type}-review.json", "artifact_sha256")
        if artifact.get("task_type") != task_type or artifact.get("reviewer_kind") != "independent-codex-cli" or artifact.get("evaluation_artifacts_read") != 0:
            raise ValueError(f"{task_type}: incorrect reviewer metadata")
        reviewer_id = artifact.get("reviewer_id")
        if not isinstance(reviewer_id, str) or reviewer_id in reviewer_ids:
            raise ValueError("reviewer identities are not distinct")
        reviewer_ids.add(reviewer_id)
        if artifact.get("selection_report_sha256") != selection["report_sha256"]:
            raise ValueError("review artifact selection binding differs")
        for item in artifact.get("items", []):
            record_id = item.get("id")
            row = by_id.get(record_id)
            if record_id not in scale_ids or row.get("task_type") != task_type:
                raise ValueError("review item is not a selected scale row")
            if item.get("verdict") != "pass" or not isinstance(item.get("checks"), dict) or not all(item["checks"].values()):
                raise ValueError("review item failed a quality check")
            cap = row.get("primary_capability") or row.get("qualification_assignment", {}).get("primary_capability")
            reviews.append((cap, record_id, reviewer_id))
    if len(reviews) != 20 or {record_id for _, record_id, _ in reviews} != set(selection.get("selected_ids", [])):
        raise ValueError("review records differ from frozen sample")
    by_cap = defaultdict(list)
    for cap, record_id, reviewer_id in reviews:
        by_cap[cap].append((record_id, reviewer_id))
    if set(by_cap) != set(CAPABILITIES) or any(len(items) != 2 or len({i[0] for i in items}) != 2 or len({i[1] for i in items}) != 2 for items in by_cap.values()):
        raise ValueError("two independent blind reviews per primary capability absent")

    manifest = {
        "schema_version": "ganesh-mini-gate3-capability-720-seal/v1",
        "status": "passed",
        "plan_sha256": PLAN_SHA256,
        "records": 720,
        "capability_rows_sha256": file_sha(capability_path),
        "unique_record_ids": 720,
        "unique_source_identities": 720,
        "entry_manifest_sha256": entry["manifest_sha256"],
        "provisional_report_sha256": provisional["report_sha256"],
        "materialized_report_sha256": materialized["report_sha256"],
        "separation_report_sha256": separation["report_sha256"],
        "quality_review_report_sha256": quality["report_sha256"],
        "quality_reviewers": "two independent blind AI content reviewers; no human sign-off claimed",
        "evaluation_artifacts_read": 0,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    _capability_rows(capability_bytes, manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("capability", "provisional", "entry", "materialized", "separation", "review_dir", "output"):
        parser.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("output already exists")
    manifest = seal(args.capability, args.provisional, args.entry, args.materialized, args.separation, args.review_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": "passed", "records": 720, "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
