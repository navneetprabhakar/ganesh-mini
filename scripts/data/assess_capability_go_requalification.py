#!/usr/bin/env python3
"""Fail-closed assessment and full-cohort merge of uniform Go requalification."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_capability_scale_delta_audits import _write_json_atomic, _write_jsonl_atomic
from scripts.data.run_capability_scale_final_matrix import _jsonl, _sealed


def assess(args: argparse.Namespace) -> dict[str, Any]:
    manifest = _sealed(json.loads(args.input_manifest.read_text(encoding="utf-8")),
                       "manifest_sha256", "Go input manifest")
    parent_report = _sealed(json.loads(args.parent_report.read_text(encoding="utf-8")),
                            "report_sha256", "parent matrix report")
    parent = _jsonl(args.parent_artifacts)
    new_report = _sealed(json.loads(args.go_report.read_text(encoding="utf-8")),
                         "report_sha256", "Go matrix report")
    new = _jsonl(args.go_artifacts)
    ids = manifest.get("ordered_candidate_ids")
    if (
        manifest.get("status") != "ready"
        or manifest.get("selected") != 89
        or manifest.get("workers") != 1
        or manifest.get("candidate_or_runtime_mutation") is not False
        or manifest.get("evaluation_artifacts_read") != 0
        or manifest.get("parent_report_sha256s", {}).get("matrix") != parent_report["report_sha256"]
        or len(parent) != 534
        or parent_report.get("requested") != 534
        or parent_report.get("terminal_rows_sha256") != canonical_sha256(parent)
        or len(new) != 89
        or new_report.get("requested") != 89
        or new_report.get("terminal_rows_sha256") != canonical_sha256(new)
        or new_report.get("ordered_candidate_ids") != ids
        or [row.get("candidate_id") for row in new] != ids
        or new_report.get("evaluation_artifacts_read") != 0
    ):
        raise ValueError("Go requalification is not bound to the exact parent and input cohort")
    for row in parent + new:
        _sealed(row, "artifact_sha256", str(row.get("candidate_id")))
        if row.get("evaluation_artifacts_read") != 0:
            raise ValueError("matrix artifact read evaluation data")
    parent_by_id = {row["candidate_id"]: row for row in parent}
    if len(parent_by_id) != 534:
        raise ValueError("duplicate parent candidate")
    original = [parent_by_id.get(identifier) for identifier in ids]
    if (
        any(row is None or row.get("lane") != "go" for row in original)
        or [row["input_sha256"] for row in original] != manifest.get("original_input_sha256s")
        or [row["artifact_sha256"] for row in original] != manifest.get("original_artifact_sha256s")
        or [row["status"] for row in original] != manifest.get("original_statuses")
        or [row["input_sha256"] for row in new] != manifest.get("original_input_sha256s")
        or new_report.get("terminal_artifact_sha256s") != [row["artifact_sha256"] for row in new]
    ):
        raise ValueError("new Go input or ordered artifact bindings drifted")
    unresolved = [row["candidate_id"] for row in new if row["status"] == "unresolved"]
    regressions = [old["candidate_id"] for old, row in zip(original, new, strict=True)
                   if old["status"] == "admitted" and row["status"] != "admitted"]
    status = "accepted" if not unresolved and not regressions else "failed"
    result: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-go-requalification-assessment/v1",
        "status": status,
        "input_manifest_sha256": manifest["manifest_sha256"],
        "parent_report_sha256": parent_report["report_sha256"],
        "go_report_sha256": new_report["report_sha256"],
        "go_counts": dict(sorted(Counter(row["status"] for row in new).items())),
        "original_go_counts": dict(sorted(Counter(row["status"] for row in original).items())),
        "unresolved_candidate_ids": unresolved,
        "regressed_original_admission_ids": regressions,
        "ordered_go_artifact_sha256s": [row["artifact_sha256"] for row in new],
        "admission_credit_from_diagnostic": 0,
        "evaluation_artifacts_read": 0,
    }
    if status == "accepted":
        replacement = {row["candidate_id"]: row for row in new}
        merged = [replacement.get(row["candidate_id"], row) for row in parent]
        counts = dict(sorted(Counter(row["status"] for row in merged).items()))
        combined = dict(parent_report)
        combined.pop("report_sha256")
        combined.update({
            "status": "passed" if counts == {"admitted": 534} else "failed",
            "counts": counts,
            "admitted_by_lane": dict(sorted(Counter(
                row["lane"] for row in merged if row["status"] == "admitted"
            ).items())),
            "terminal_artifact_sha256s": [row["artifact_sha256"] for row in merged],
            "terminal_rows_sha256": canonical_sha256(merged),
            "parent_report_sha256": parent_report["report_sha256"],
            "go_requalification_report_sha256": new_report["report_sha256"],
            "go_requalification_manifest_sha256": manifest["manifest_sha256"],
        })
        combined["report_sha256"] = canonical_sha256(combined)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        _write_jsonl_atomic(args.output_dir / "terminal-artifacts.jsonl", merged)
        _write_json_atomic(args.output_dir / "matrix-report.json", combined)
        result["combined_report_sha256"] = combined["report_sha256"]
        result["combined_counts"] = counts
    result["report_sha256"] = canonical_sha256(result)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_json_atomic(args.output_dir / "assessment-report.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-manifest", type=Path, required=True)
    parser.add_argument("--parent-report", type=Path, required=True)
    parser.add_argument("--parent-artifacts", type=Path, required=True)
    parser.add_argument("--go-report", type=Path, required=True)
    parser.add_argument("--go-artifacts", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    result = assess(parser.parse_args())
    print(json.dumps({"status": result["status"], "go_counts": result["go_counts"],
                      "report_sha256": result["report_sha256"]}, sort_keys=True))
    return 0 if result["status"] == "accepted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
