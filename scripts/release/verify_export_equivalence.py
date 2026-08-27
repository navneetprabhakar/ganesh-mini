#!/usr/bin/env python3
"""Verify a frozen six-lane BF16/F16/Q8 export-equivalence sample."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.eval.score import load_results


LANES = ("go", "java", "javascript", "typescript", "python", "rust")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def load_cohort(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    run = load_sealed(root / "run.json", "run_sha256")
    accounting = run.get("task_accounting", {})
    if (
        run.get("schema_version") != "ganesh-mini-inference-run/v2"
        or accounting.get("expected") != 6
        or accounting.get("completed") != 6
        or accounting.get("pending") != 0
        or len(run.get("tasks", [])) != 6
    ):
        raise ValueError("export-equivalence run is incomplete")
    results = load_results(root / "tasks")
    if len(results) != 6 or {row["task_id"] for row in results} != {row["task_id"] for row in run["tasks"]}:
        raise ValueError("export-equivalence task evidence does not bind its run")
    return run, results


def verify(
    artifact_manifest: dict[str, Any],
    cohorts: dict[str, tuple[dict[str, Any], list[dict[str, Any]]]],
) -> dict[str, Any]:
    manifest = dict(artifact_manifest)
    claimed = manifest.pop("manifest_sha256", None)
    if (
        claimed != canonical_sha256(manifest)
        or manifest.get("schema_version") != "ganesh-mini-release-artifacts/v1"
        or manifest.get("status") != "built"
    ):
        raise ValueError("release artifact manifest is invalid")
    expected = {
        "merged_bf16_hf": manifest["artifacts"]["merged_bf16_hf"]["sha256"],
        "gguf_f16": manifest["artifacts"]["gguf_f16"]["sha256"],
        "gguf_q8": manifest["artifacts"]["gguf_q8"]["sha256"],
    }
    if set(cohorts) != set(expected):
        raise ValueError("export-equivalence requires exact BF16, F16, and Q8 cohorts")
    ids = []
    source_tasks = []
    rendered_prompts = []
    pass_vectors = {}
    evidence = {}
    for name in expected:
        run, results = cohorts[name]
        model = run.get("model", {})
        if model.get("artifact_sha256") != expected[name]:
            raise ValueError(f"{name} run does not bind its release artifact")
        by_id = {row["task_id"]: row for row in results}
        if len(by_id) != 6 or {row["language"] for row in results} != set(LANES):
            raise ValueError(f"{name} does not cover exactly one task per lane")
        ids.append(frozenset(by_id))
        source_tasks.append({task_id: by_id[task_id]["_source_task_sha256"] for task_id in sorted(by_id)})
        rendered_prompts.append({task_id: by_id[task_id]["rendered_prompt_sha256"] for task_id in sorted(by_id)})
        pass_vectors[name] = {task_id: by_id[task_id]["passed"] for task_id in sorted(by_id)}
        evidence[name] = {
            "run_sha256": run["run_sha256"],
            "artifact_sha256": model["artifact_sha256"],
            "passed": sum(row["passed"] is True for row in results),
            "result_set_sha256": canonical_sha256([
                {key: row[key] for key in ("task_id", "result_sha256")}
                for row in sorted(results, key=lambda item: item["task_id"])
            ]),
        }
    if len(set(ids)) != 1:
        raise ValueError("export-equivalence cohorts do not cover the same frozen tasks")
    if any(value != source_tasks[0] for value in source_tasks[1:]):
        raise ValueError("export-equivalence cohorts do not bind the same frozen source tasks")
    if any(value != rendered_prompts[0] for value in rendered_prompts[1:]):
        raise ValueError("export-equivalence cohorts do not use the same rendered prompts")
    reference = pass_vectors["merged_bf16_hf"]
    exact = {
        name: vector == reference
        for name, vector in pass_vectors.items()
        if name != "merged_bf16_hf"
    }
    report = {
        "schema_version": "ganesh-mini-export-equivalence/v1",
        "status": "passed" if all(exact.values()) else "failed",
        "artifact_manifest_sha256": claimed,
        "task_count": 6,
        "lanes": list(LANES),
        "cohorts": evidence,
        "source_task_set_sha256": canonical_sha256(source_tasks[0]),
        "rendered_prompt_set_sha256": canonical_sha256(rendered_prompts[0]),
        "pass_vector_equivalence": exact,
    }
    report["evidence_sha256"] = canonical_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-manifest", type=Path, required=True)
    parser.add_argument("--merged-run", type=Path, required=True)
    parser.add_argument("--f16-run", type=Path, required=True)
    parser.add_argument("--q8-run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cohorts = {
        "merged_bf16_hf": load_cohort(args.merged_run),
        "gguf_f16": load_cohort(args.f16_run),
        "gguf_q8": load_cohort(args.q8_run),
    }
    report = verify(json.loads(args.artifact_manifest.read_text(encoding="utf-8")), cohorts)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
