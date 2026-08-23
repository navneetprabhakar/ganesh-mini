#!/usr/bin/env python3
"""Seal the complete private decision surface and its comparison inputs."""

from __future__ import annotations

import json
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from scripts.eval.contracts import (
    load_json,
    sha256_bytes,
    sha256_object,
    sha256_text,
    validate_task,
    write_json,
)
from scripts.verify.sandbox import SANDBOX_CONTRACT

ROOT = Path(__file__).resolve().parents[3]
PRIVATE_MANIFESTS = ROOT / "manifests/evaluation/private"
SEED_PATHS = (
    "data/seed/ganesh_v01/train.jsonl",
    "data/seed/ganesh_v01/validation.jsonl",
)
DEVELOPMENT_MANIFESTS = tuple(
    f"manifests/evaluation/private/development-tranche{i}.json" for i in range(1, 7)
)
DECISION_MANIFESTS = tuple(
    f"manifests/evaluation/private/decision-tranche{i}.json" for i in range(1, 7)
)
OUTPUT = PRIVATE_MANIFESTS / "decision-global-separation.json"
RUNTIME_CONFIG = "configs/eval/runtimes.json"
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
KINDS = ("generation", "repair")


def normalized(text: str) -> str:
    """Return the declared comparison normalization."""
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def _without(value: dict[str, Any], key: str) -> dict[str, Any]:
    return {name: item for name, item in value.items() if name != key}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _duplicates(values: Iterable[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def _load_seed() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    inputs: list[dict[str, Any]] = []
    prompts: list[dict[str, str]] = []
    record_ids: list[str] = []
    for relative in SEED_PATHS:
        path = ROOT / relative
        raw = path.read_bytes()
        rows = 0
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                _require(bool(line.strip()), f"blank seed record: {relative}:{line_number}")
                row = json.loads(line)
                _require(
                    isinstance(row, dict),
                    f"invalid seed record: {relative}:{line_number}",
                )
                record_id = row.get("id")
                _require(
                    isinstance(record_id, str) and bool(record_id),
                    f"invalid seed id: {relative}:{line_number}",
                )
                messages = row.get("messages")
                _require(isinstance(messages, list) and bool(messages), f"invalid seed messages: {record_id}")
                user_messages = [item for item in messages if item.get("role") == "user"]
                _require(len(user_messages) == 1, f"seed must contain exactly one user prompt: {record_id}")
                text = user_messages[0].get("content")
                _require(isinstance(text, str) and bool(text), f"invalid seed prompt: {record_id}")
                hashes = row.get("content_hashes")
                _require(isinstance(hashes, dict), f"missing seed content hashes: {record_id}")
                _require(hashes.get("user_sha256") == sha256_text(text), f"seed prompt hash mismatch: {record_id}")
                _require(
                    hashes.get("user_normalized_sha256") == sha256_text(normalized(text)),
                    f"seed normalized prompt hash mismatch: {record_id}",
                )
                record_ids.append(record_id)
                prompts.append({"id": record_id, "text": text, "source": relative})
                rows += 1
        inputs.append(
            {"path": relative, "sha256": sha256_bytes(raw), "bytes": len(raw), "records": rows}
        )
    duplicates = _duplicates(record_ids)
    _require(not duplicates, f"duplicate seed record ids: {duplicates}")
    return prompts, inputs


def _load_surface(
    surface: str, manifest_paths: tuple[str, ...]
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    all_tasks: list[dict[str, str]] = []
    bindings: list[dict[str, Any]] = []
    expected_per_manifest = 30 if surface == "development" else 60
    expected_per_lane = 5 if surface == "development" else 10
    for index, relative in enumerate(manifest_paths, 1):
        manifest = load_json(ROOT / relative)
        claimed = manifest.get("manifest_sha256")
        _require(
            claimed == sha256_object(_without(manifest, "manifest_sha256")),
            f"manifest seal mismatch: {relative}",
        )
        _require(manifest.get("surface") == surface, f"surface mismatch: {relative}")
        _require(manifest.get("tranche") == f"tranche{index}", f"tranche mismatch: {relative}")
        _require(
            manifest.get("runtime_config") == RUNTIME_CONFIG,
            f"runtime config path mismatch: {relative}",
        )
        entries = manifest.get("tasks")
        _require(
            isinstance(entries, list) and len(entries) == expected_per_manifest,
            f"task count mismatch: {relative}",
        )
        _require(manifest.get("task_count") == len(entries), f"declared task count mismatch: {relative}")
        actual: Counter[tuple[str, str]] = Counter()
        task_bindings: list[dict[str, str]] = []
        for entry in entries:
            task = validate_task(load_json(ROOT / entry["path"]))
            task_hash = sha256_object(task)
            _require(task_hash == entry.get("sha256"), f"task seal mismatch: {entry.get('task_id')}")
            _require(task["surface"] == surface, f"task surface mismatch: {task['task_id']}")
            _require(task["task_id"] == entry.get("task_id"), f"task id mismatch: {entry.get('path')}")
            _require(
                task["language"] == entry.get("language"),
                f"task language mismatch: {task['task_id']}",
            )
            _require(task["task_type"] == entry.get("task_type"), f"task type mismatch: {task['task_id']}")
            _require(
                task["prompt"]["sha256"] == entry.get("prompt_sha256"),
                f"prompt seal mismatch: {task['task_id']}",
            )
            _require(
                task["rendered_prompt"]["sha256"] == entry.get("rendered_prompt_sha256"),
                f"rendered prompt seal mismatch: {task['task_id']}",
            )
            actual[(task["language"], task["task_type"])] += 1
            row = {
                "id": task["task_id"],
                "path": entry["path"],
                "text": task["prompt"]["text"],
                "manifest": relative,
            }
            all_tasks.append(row)
            task_bindings.append(
                {"path": entry["path"], "sha256": task_hash, "task_id": task["task_id"]}
            )
        recorded = manifest.get("counts_by_lane")
        computed = {
            lane: {kind: actual[(lane, kind)] for kind in KINDS}
            for lane in LANES
        }
        _require(recorded == computed, f"lane/type counts do not match tasks: {relative}")
        _require(
            all(sum(computed[lane].values()) == expected_per_lane for lane in LANES),
            f"lane imbalance: {relative}",
        )
        if surface == "decision":
            _require(
                all(computed[lane] == {"generation": 5, "repair": 5} for lane in LANES),
                f"decision lane/type imbalance: {relative}",
            )
        bindings.append(
            {
                "path": relative,
                "sha256": claimed,
                "task_count": len(entries),
                "tasks": task_bindings,
            }
        )
    duplicate_ids = _duplicates(task["id"] for task in all_tasks)
    duplicate_paths = _duplicates(task["path"] for task in all_tasks)
    _require(not duplicate_ids, f"duplicate {surface} task ids: {duplicate_ids}")
    _require(not duplicate_paths, f"duplicate {surface} task paths: {duplicate_paths}")
    expected_total = expected_per_manifest * len(manifest_paths)
    _require(len(all_tasks) == expected_total, f"global {surface} count mismatch")
    lane_counts = Counter(load_json(ROOT / task["path"])["language"] for task in all_tasks)
    _require(
        lane_counts == Counter({lane: expected_total // len(LANES) for lane in LANES}),
        f"global {surface} lane imbalance",
    )
    type_counts = Counter(load_json(ROOT / task["path"])["task_type"] for task in all_tasks)
    _require(type_counts == Counter({kind: expected_total // 2 for kind in KINDS}), f"global {surface} type imbalance")
    return all_tasks, bindings


def _load_runtime_config() -> tuple[dict[str, Any], dict[str, Any]]:
    path = ROOT / RUNTIME_CONFIG
    raw = path.read_bytes()
    config = json.loads(raw)
    _require(config.get("schema_version") == "3.0", "unsupported runtime config schema")
    _require(config.get("platform") == "linux/amd64", "unsupported verifier platform")
    runtimes = config.get("runtimes")
    _require(isinstance(runtimes, dict) and bool(runtimes), "invalid runtime config")
    for runtime_id, runtime in runtimes.items():
        _require(isinstance(runtime, dict), f"invalid runtime: {runtime_id}")
        _require(runtime.get("platform") == config["platform"], f"runtime platform mismatch: {runtime_id}")
        image_id = runtime.get("image_id")
        _require(
            isinstance(image_id, str) and image_id.startswith("sha256:") and len(image_id) == 71,
            f"invalid runtime image ID: {runtime_id}",
        )
        manifest_digest = runtime.get("manifest_digest")
        _require(
            isinstance(manifest_digest, str) and manifest_digest.startswith("sha256:")
            and len(manifest_digest) == 71,
            f"invalid runtime manifest digest: {runtime_id}",
        )
    binding = {"path": RUNTIME_CONFIG, "sha256": sha256_bytes(raw), "bytes": len(raw)}
    return runtimes, binding


def _bind_decision_evidence(
    manifest_bindings: list[dict[str, Any]], runtimes: dict[str, Any]
) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for index, manifest_binding in enumerate(manifest_bindings, 1):
        manifest_sha = manifest_binding["sha256"]
        row: dict[str, Any] = {"tranche": index}
        for suffix, seal_field in (("overlap", "report_sha256"), ("directionality", "evidence_sha256")):
            relative = f"manifests/evaluation/private/decision-tranche{index}-{suffix}.json"
            item = load_json(ROOT / relative)
            claimed = item.get(seal_field)
            _require(
                claimed == sha256_object(_without(item, seal_field)),
                f"{suffix} evidence seal mismatch: tranche{index}",
            )
            _require(item.get("status") == "passed", f"{suffix} evidence not passed: tranche{index}")
            _require(
                item.get("evaluation_manifest") == manifest_binding["path"],
                f"{suffix} manifest path mismatch: tranche{index}",
            )
            _require(
                item.get("evaluation_manifest_sha256") == manifest_sha,
                f"{suffix} manifest seal mismatch: tranche{index}",
            )
            if suffix == "overlap":
                for field in (
                    "exact_prompt_overlaps",
                    "normalized_prompt_overlaps",
                    "within_tranche_exact_overlaps",
                    "within_tranche_normalized_overlaps",
                ):
                    _require(item.get(field) == [], f"overlap evidence contains hits: tranche{index}:{field}")
                _require(item.get("evaluation_prompts_inspected") == 60, f"overlap task count mismatch: tranche{index}")
            else:
                _require(
                    item.get("runtime_config") == RUNTIME_CONFIG,
                    f"directionality runtime config path mismatch: tranche{index}",
                )
                _require(item.get("task_count") == 60, f"directionality task count mismatch: tranche{index}")
                _require(item.get("execution_count") == 120, f"directionality execution count mismatch: tranche{index}")
                _require(item.get("reference_passes") == 60, f"directionality reference count mismatch: tranche{index}")
                _require(
                    item.get("known_bad_rejections") == 60,
                    f"directionality rejection count mismatch: tranche{index}",
                )
                _require(item.get("failures") == [], f"directionality failures present: tranche{index}")
                tasks = {
                    task_binding["task_id"]: validate_task(load_json(ROOT / task_binding["path"]))
                    for task_binding in manifest_binding["tasks"]
                }
                execution_counts: Counter[tuple[str, str]] = Counter()
                verifier_sandbox_hashes: set[str] = set()
                for execution in item.get("executions", []):
                    task_id = execution.get("task_id")
                    _require(
                        task_id in tasks,
                        f"directionality execution has unknown task: tranche{index}:{task_id}",
                    )
                    task = tasks[task_id]
                    runtime = runtimes.get(task["runtime_id"])
                    _require(isinstance(runtime, dict), f"unbound task runtime: {task_id}")
                    artifact_kind = execution.get("artifact")
                    _require(artifact_kind in {"reference", "known_bad"}, f"invalid artifact kind: {task_id}")
                    selected = (
                        task["validation"]["reference"]
                        if artifact_kind == "reference"
                        else task["validation"]["known_bad"][0]
                    )
                    if artifact_kind == "known_bad":
                        _require(
                            len(task["validation"]["known_bad"]) == 1,
                            f"task does not have exactly one bound known-bad artifact: {task_id}",
                        )
                    _require(execution.get("language") == task["language"], f"execution language mismatch: {task_id}")
                    _require(
                        execution.get("artifact_label") == selected["label"],
                        f"artifact label mismatch: {task_id}",
                    )
                    _require(
                        execution.get("artifact_sha256") == selected["sha256"],
                        f"artifact seal mismatch: {task_id}",
                    )
                    expected_pass = artifact_kind == "reference"
                    _require(execution.get("expected_pass") is expected_pass, f"expected polarity mismatch: {task_id}")
                    _require(execution.get("observed_pass") is expected_pass, f"observed polarity mismatch: {task_id}")
                    verifier = execution.get("verifier")
                    _require(isinstance(verifier, dict), f"missing verifier: {task_id}")
                    _require(
                        verifier.get("runtime_id") == task["runtime_id"],
                        f"verifier runtime mismatch: {task_id}",
                    )
                    _require(
                        runtime.get("language") == task["language"]
                        and runtime.get("candidate_path") == task["candidate_path"],
                        f"runtime contract mismatch: {task_id}",
                    )
                    _require(
                        verifier.get("commands") == runtime.get("commands"),
                        f"verifier commands mismatch: {task_id}",
                    )
                    _require(
                        verifier.get("timed_out") is False,
                        f"timed-out directionality execution: {task_id}",
                    )
                    image = verifier.get("image")
                    expected_image = f"{runtime['image'].rsplit(':', 1)[0]}@{runtime['manifest_digest']}"
                    _require(image == expected_image, f"verifier image mismatch: {task_id}")
                    _require(
                        verifier.get("image_id") == runtime.get("image_id"),
                        f"verifier image identity mismatch: {task_id}",
                    )
                    for output_field in ("stdout", "stderr"):
                        output = verifier.get(output_field)
                        _require(isinstance(output, str), f"invalid verifier {output_field}: {task_id}")
                        _require(
                            verifier.get(f"{output_field}_sha256") == sha256_text(output),
                            f"verifier {output_field} seal mismatch: {task_id}",
                        )
                    exit_codes = verifier.get("exit_codes")
                    _require(
                        isinstance(exit_codes, list)
                        and bool(exit_codes)
                        and all(type(code) is int for code in exit_codes),
                        f"invalid verifier exit codes: {task_id}",
                    )
                    if artifact_kind == "reference":
                        _require(
                            len(exit_codes) == len(runtime["commands"])
                            and all(code == 0 for code in exit_codes),
                            f"reference verifier did not complete successfully: {task_id}",
                        )
                    else:
                        _require(
                            any(code != 0 for code in exit_codes),
                            f"known-bad verifier lacks a failing exit code: {task_id}",
                        )
                    sandbox_hash = verifier.get("sandbox_contract_sha256")
                    _require(
                        isinstance(sandbox_hash, str)
                        and len(sandbox_hash) == 64
                        and all(char in "0123456789abcdef" for char in sandbox_hash),
                        f"invalid verifier sandbox seal: {task_id}",
                    )
                    _require(
                        sandbox_hash == sha256_object(SANDBOX_CONTRACT),
                        f"verifier sandbox contract mismatch: {task_id}",
                    )
                    verifier_sandbox_hashes.add(sandbox_hash)
                    execution_counts[(task_id, artifact_kind)] += 1
                _require(len(verifier_sandbox_hashes) == 1, f"mixed verifier sandbox seals: tranche{index}")
                evidence_sandbox_hash = item.get("sandbox_contract_sha256")
                if evidence_sandbox_hash is not None:
                    _require(
                        verifier_sandbox_hashes == {evidence_sandbox_hash},
                        f"verifier/evidence sandbox seal mismatch: tranche{index}",
                    )
                for task_id in tasks:
                    _require(
                        execution_counts[(task_id, "reference")] == 1
                        and execution_counts[(task_id, "known_bad")] == 1,
                        f"directionality execution multiplicity mismatch: {task_id}",
                    )
                _require(sum(execution_counts.values()) == 120, f"unexpected directionality executions: tranche{index}")

                if index <= 2:
                    overlap_path = item.get("cross_tranche_overlap_report")
                    overlap_sha = item.get("cross_tranche_overlap_report_sha256")
                    expected_path = "manifests/evaluation/private/decision-tranches1-2-cross-overlap.json"
                    _require(overlap_path == expected_path, f"cross-overlap path mismatch: tranche{index}")
                    cross = load_json(ROOT / expected_path)
                    _require(
                        cross.get("report_sha256") == overlap_sha
                        == sha256_object(_without(cross, "report_sha256")),
                        f"cross-overlap seal mismatch: tranche{index}",
                    )
                    _require(cross.get("status") == "passed", "cross-overlap evidence not passed")
                    expected_manifests = [
                        {
                            "path": binding["path"],
                            "sha256": binding["sha256"],
                            "task_count": binding["task_count"],
                        }
                        for binding in manifest_bindings[:2]
                    ]
                    _require(
                        cross.get("manifests") == expected_manifests,
                        "cross-overlap manifest bindings mismatch",
                    )
                    row["cross_overlap"] = {"path": expected_path, "sha256": overlap_sha}
                else:
                    _require(
                        item.get("overlap_report") == row["overlap"]["path"]
                        and item.get("overlap_report_sha256") == row["overlap"]["sha256"],
                        f"directionality/overlap binding mismatch: tranche{index}",
                    )
                row["sandbox_contract_sha256"] = next(iter(verifier_sandbox_hashes))
            row[suffix] = {"path": relative, "sha256": claimed}
        evidence.append(row)
    return evidence


def build() -> dict[str, Any]:
    seed, seed_inputs = _load_seed()
    development, development_bindings = _load_surface("development", DEVELOPMENT_MANIFESTS)
    decision, decision_bindings = _load_surface("decision", DECISION_MANIFESTS)
    runtimes, runtime_binding = _load_runtime_config()
    evidence = _bind_decision_evidence(decision_bindings, runtimes)

    comparison = seed + development
    comparison_exact_hashes = [sha256_text(row["text"]) for row in comparison]
    comparison_normalized_hashes = [sha256_text(normalized(row["text"])) for row in comparison]
    duplicate_comparison_exact = _duplicates(comparison_exact_hashes)
    duplicate_comparison_normalized = _duplicates(comparison_normalized_hashes)
    _require(
        not duplicate_comparison_exact,
        "duplicate exact prompts in seed/development comparison surface",
    )
    _require(
        not duplicate_comparison_normalized,
        "duplicate normalized prompts in seed/development comparison surface",
    )
    comparison_exact = dict(zip(comparison_exact_hashes, (row["id"] for row in comparison)))
    comparison_normalized = dict(
        zip(comparison_normalized_hashes, (row["id"] for row in comparison))
    )
    decision_exact: dict[str, str] = {}
    decision_normalized: dict[str, str] = {}
    exact_comparison_hits: list[dict[str, str]] = []
    normalized_comparison_hits: list[dict[str, str]] = []
    exact_decision_hits: list[dict[str, str]] = []
    normalized_decision_hits: list[dict[str, str]] = []
    for row in decision:
        exact = sha256_text(row["text"])
        norm = sha256_text(normalized(row["text"]))
        if exact in comparison_exact:
            exact_comparison_hits.append({"decision_task_id": row["id"], "comparison_id": comparison_exact[exact]})
        if norm in comparison_normalized:
            normalized_comparison_hits.append(
                {"decision_task_id": row["id"], "comparison_id": comparison_normalized[norm]}
            )
        if exact in decision_exact:
            exact_decision_hits.append({"first_task_id": decision_exact[exact], "second_task_id": row["id"]})
        if norm in decision_normalized:
            normalized_decision_hits.append({"first_task_id": decision_normalized[norm], "second_task_id": row["id"]})
        decision_exact[exact] = row["id"]
        decision_normalized[norm] = row["id"]

    duplicate_ids = _duplicates(row["id"] for row in seed + development + decision)
    failures = exact_comparison_hits + normalized_comparison_hits + exact_decision_hits + normalized_decision_hits
    _require(not failures, "global decision prompt separation failed")
    _require(not duplicate_ids, f"duplicate ids across bound surfaces: {duplicate_ids}")

    report: dict[str, Any] = {
        "schema_version": "ganesh-mini-global-decision-separation/v1",
        "status": "passed",
        "normalization": "NFKC + Unicode casefold + whitespace collapse",
        "seed_inputs": seed_inputs,
        "development_manifests": development_bindings,
        "decision_manifests": decision_bindings,
        "decision_evidence": evidence,
        "runtime_config": runtime_binding,
        "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
        "counts": {
            "seed_records": len(seed),
            "development_tasks": len(development),
            "decision_tasks": len(decision),
            "comparison_prompts": len(comparison),
        },
        "exact_decision_vs_seed_development_overlaps": exact_comparison_hits,
        "normalized_decision_vs_seed_development_overlaps": normalized_comparison_hits,
        "exact_decision_prompt_overlaps": exact_decision_hits,
        "normalized_decision_prompt_overlaps": normalized_decision_hits,
        "duplicate_ids": duplicate_ids,
        "duplicate_seed_development_exact_prompts": duplicate_comparison_exact,
        "duplicate_seed_development_normalized_prompts": duplicate_comparison_normalized,
    }
    report["report_sha256"] = sha256_object(report)
    write_json(OUTPUT, report)
    return report


if __name__ == "__main__":
    result = build()
    print(
        json.dumps(
            {
                "status": result["status"],
                "counts": result["counts"],
                "report_sha256": result["report_sha256"],
            },
            sort_keys=True,
        )
    )
