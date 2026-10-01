#!/usr/bin/env python3
"""Assemble and validate the corrected 900-row Gate 3 package evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from scripts.data.build_capability_corpus_plan import CAPABILITIES, canonical_sha256
from scripts.data.validate_gate3_final_package import validate


AFFECTED = "binary_and_bitwise"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict]:
    data = path.read_bytes()
    if not data or not data.endswith(b"\n"):
        raise ValueError(f"incomplete JSONL input: {path}")
    return [json.loads(line) for line in data.splitlines()]


def sealed(path: Path, key: str) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value)
    if body.pop(key, None) != canonical_sha256(body):
        raise ValueError(f"invalid sealed evidence: {path}")
    return value


def report(value: dict) -> dict:
    value["report_sha256"] = canonical_sha256(value)
    return value


def binding(path: Path, base: Path) -> dict:
    return {"path": os.path.relpath(path.resolve(), base.resolve()), "sha256": file_sha(path)}


def build(capability_path: Path, capability_manifest_path: Path, replay_path: Path,
          replay_manifest_path: Path, old_quality_dir: Path, new_quality_dir: Path,
          separation_path: Path, tokenization_path: Path) -> tuple[list[dict], dict[str, dict]]:
    capability, replay = rows(capability_path), rows(replay_path)
    package = capability + replay
    if len(capability) != 720 or len(replay) != 180 or len({row["id"] for row in package}) != 900:
        raise ValueError("package row counts or IDs differ")
    cap_manifest = sealed(capability_manifest_path, "manifest_sha256")
    replay_manifest = sealed(replay_manifest_path, "manifest_sha256")
    old_quality = sealed(old_quality_dir / "quality-review-report.json", "report_sha256")
    new_quality = sealed(new_quality_dir / "quality-review-report.json", "report_sha256")
    separation = sealed(separation_path, "report_sha256")
    tokenization = sealed(tokenization_path, "report_sha256")
    if (cap_manifest.get("status") != "passed" or cap_manifest.get("capability_rows_sha256") != file_sha(capability_path) or
        replay_manifest.get("capability_manifest_sha256") != cap_manifest["manifest_sha256"] or
        replay_manifest.get("replay_jsonl_sha256") != file_sha(replay_path) or
        old_quality.get("status") != "passed" or new_quality.get("status") != "passed" or
        separation.get("status") != "passed" or tokenization.get("status") != "passed" or
        separation.get("package_rows_sha256") != canonical_sha256(package) or
        tokenization.get("package_rows_sha256") != canonical_sha256(package) or
        tokenization.get("separation_report_sha256") != separation["report_sha256"]):
        raise ValueError("final package upstream evidence does not bind exact rows")
    cap_by_id = {row["id"]: row for row in capability}
    reviews = []
    for kind in ("generation", "repair"):
        artifact = sealed(old_quality_dir / f"{kind}-review.json", "artifact_sha256")
        for item in artifact["items"]:
            identifier = item["id"]
            row = cap_by_id.get(identifier)
            if row is None:
                raise ValueError("historical reviewed row absent")
            cap = row["qualification_assignment"]["primary_capability"]
            if cap == AFFECTED:
                continue
            index = artifact["candidate_ids"].index(identifier)
            if artifact["candidate_sha256s"][index] != canonical_sha256(row) or item["verdict"] != "pass":
                raise ValueError("historical quality review does not bind row")
            reviews.append({"record_id": identifier, "primary_capability": cap, "reviewer_id": artifact["reviewer_id"],
                            "reviewer_kind": "independent-codex-cli", "blind": True, "verdict": "pass",
                            "row_sha256": canonical_sha256(row), "review_artifact_sha256": artifact["artifact_sha256"]})
    for kind in ("generation", "repair"):
        artifact = sealed(new_quality_dir / f"{kind}-review.json", "artifact_sha256")
        identifier = artifact["candidate_id"]
        row = cap_by_id.get(identifier)
        if (row is None or row["qualification_assignment"]["primary_capability"] != AFFECTED or
            artifact["candidate_sha256"] != canonical_sha256(row) or artifact["items"][0]["verdict"] != "pass"):
            raise ValueError("replacement quality review does not bind row")
        reviews.append({"record_id": identifier, "primary_capability": AFFECTED,
                        "reviewer_id": artifact["reviewer_id"], "reviewer_kind": "independent-codex-cli",
                        "blind": True, "verdict": "pass", "row_sha256": canonical_sha256(row),
                        "review_artifact_sha256": artifact["artifact_sha256"]})
    if len(reviews) != 20 or {item["primary_capability"] for item in reviews} != set(CAPABILITIES):
        raise ValueError("quality report does not cover exact 20 reviews")
    common = {"status": "passed", "evaluation_artifacts_read_by_construction": 0}
    reports = {
        "admission": report({"schema_version": "ganesh-mini-gate3-package-admission/v1", **common,
                             "records": 720, "rows_sha256": canonical_sha256(capability),
                             "capability_manifest_sha256": cap_manifest["manifest_sha256"],
                             "qualified_source_rows": 720}),
        "replay_selection": report({"schema_version": "ganesh-mini-gate3-package-replay-selection/v1", **common,
                                    "records": 180, "rows_sha256": canonical_sha256(replay),
                                    "replay_manifest_sha256": replay_manifest["manifest_sha256"],
                                    "byte_preserved": True}),
        "manual_review": report({"schema_version": "ganesh-mini-gate3-package-blind-quality/v1", **common,
                                 "package_rows_sha256": canonical_sha256(package), "reviews": reviews,
                                 "reviewer_disclosure": "independent blind AI reviewers; no human sign-off claimed",
                                 "historical_quality_report_sha256": old_quality["report_sha256"],
                                 "replacement_quality_report_sha256": new_quality["report_sha256"]}),
    }
    return package, reports


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("capability", "capability_manifest", "replay", "replay_manifest", "historical_quality_dir", "replacement_quality_dir", "separation", "tokenization", "output_dir"):
        parser.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    args = parser.parse_args()
    output_dir = args.output_dir
    names = ("admission", "replay_selection", "manual_review")
    planned = [output_dir / f"{name}.json" for name in names] + [output_dir / "train-900.jsonl", output_dir / "manifest.json"]
    if any(path.exists() for path in planned):
        raise ValueError("final package output already exists")
    package, reports = build(args.capability, args.capability_manifest, args.replay, args.replay_manifest,
                             args.historical_quality_dir, args.replacement_quality_dir, args.separation, args.tokenization)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, value in reports.items():
        with (output_dir / f"{name}.json").open("x", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
    training_file = output_dir / "train-900.jsonl"
    with training_file.open("x", encoding="utf-8") as handle:
        handle.write("".join(json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n" for row in package))
    manifest = {
        "schema_version": "ganesh-mini-gate3-final-package/v1",
        "evaluation_artifacts_read_by_construction": 0,
        "capability": binding(args.capability, output_dir),
        "replay": binding(args.replay, output_dir),
        "admission": binding(output_dir / "admission.json", output_dir),
        "replay_selection": binding(output_dir / "replay_selection.json", output_dir),
        "manual_review": binding(output_dir / "manual_review.json", output_dir),
        "separation": binding(args.separation, output_dir),
        "tokenization": binding(args.tokenization, output_dir),
        "canonical_training_jsonl": binding(training_file, output_dir),
        "canonical_training_rows_sha256": canonical_sha256(package),
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_path = output_dir / "manifest.json"
    with manifest_path.open("x", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    result = validate(manifest_path)
    print(json.dumps({**result, "manifest_sha256": manifest["manifest_sha256"], "training_file_sha256": file_sha(training_file)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
