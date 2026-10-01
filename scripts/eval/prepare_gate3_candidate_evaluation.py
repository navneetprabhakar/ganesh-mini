#!/usr/bin/env python3
"""Prepare local, evaluation-only Gate 3 candidate inputs and run cards.

This module does not start compute or access GCloud.  Its output is a staged
input, not evidence that an evaluator, verifier image, or quality gate passed.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import tarfile
from pathlib import Path
from typing import Any

from scripts.eval.contracts import load_json, sha256_object
from scripts.eval.package_workspace import file_sha256
from scripts.inference.run_evaluation import validate_config


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_SEAL = "8ed2f45d87b3b867a59c6eca03be6e9d991bd1070037bd52311ed63a07585edc"
CANARY_TASK_GLOB = "eval/private/development/tranche1/*.task.json"
DEVELOPMENT_TASK_GLOB = "eval/private/development/**/*.task.json"
EXPECTED_RUNS = {"1e-5": "1e-05", "3e-5": "3e-05"}
EXPECTED_TOKENS = 651639
EXPECTED_ROWS = 900


def sealed_json(path: Path, field: str) -> dict[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict):
        raise ValueError(f"not a JSON object: {path}")
    claim = value.pop(field, None)
    if claim != sha256_object(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claim
    return value


def verify_workspace(path: Path) -> dict[str, Any]:
    value = sealed_json(path, "manifest_sha256")
    if (value.get("schema_version") != "ganesh-mini-development-evaluation-workspace/v1"
        or value.get("status") != "sealed" or value.get("surface") != "development"
        or value.get("task_count") != 180 or value["manifest_sha256"] != WORKSPACE_SEAL):
        raise ValueError("evaluation workspace is not the frozen development-only workspace")
    archive = ROOT / value["archive"]["path"]
    if not archive.is_file() or file_sha256(archive) != value["archive"]["sha256"]:
        raise ValueError("evaluation workspace archive hash differs")
    files = value.get("files")
    if not isinstance(files, list) or len(files) != 587:
        raise ValueError("evaluation workspace file count differs")
    names = [row["path"] for row in files]
    if len(names) != len(set(names)) or any("decision" in Path(name).parts for name in names):
        raise ValueError("decision material or duplicate workspace path found")
    if sum(name.endswith(".task.json") for name in names) != 180:
        raise ValueError("evaluation workspace task inventory differs")
    return value


def verify_canary(path: Path, workspace: dict[str, Any]) -> dict[str, Any]:
    value = sealed_json(path, "manifest_sha256")
    if (value.get("schema_version") != "ganesh-mini-gate3-canary/v1"
        or value.get("status") != "frozen" or value.get("surface") != "development"
        or value.get("records") != 30 or value.get("training_admission_allowed") is not False):
        raise ValueError("not the frozen 30-task development canary")
    entries = {row["path"]: row["sha256"] for row in workspace["files"]}
    task_ids: set[str] = set()
    for task in value["tasks"]:
        name = task["path"]
        if not name.startswith("eval/private/development/tranche1/") or not name.endswith(".task.json"):
            raise ValueError("canary task escaped tranche 1")
        if task["task_file_sha256"] != entries.get(name):
            raise ValueError("canary task differs from evaluation workspace")
        task_ids.add(task["task_id"])
    if len(value["tasks"]) != 30 or len(task_ids) != 30:
        raise ValueError("canary task IDs differ")
    return value


def verify_candidate(run_path: Path, lr: str) -> dict[str, Any]:
    run = sealed_json(run_path, "evidence_sha256")
    identities = run.get("identities", {})
    state = run.get("state", {})
    if (run.get("schema_version") != "ganesh-mini-sft-run/v2"
        or run.get("status") != "complete" or identities.get("learning_rate") != EXPECTED_RUNS[lr]
        or run.get("planned_end_row") != EXPECTED_ROWS or state.get("next_row") != EXPECTED_ROWS
        or state.get("seen_tokens") != EXPECTED_TOKENS or state.get("optimizer_steps") != 113
        or run.get("save_reload", {}).get("passed") is not True):
        raise ValueError(f"{lr} is not a completed, save/reload-passed frozen epoch")
    training = run_path.parent
    adapter_dir = training / "adapter-final"
    expected = run.get("adapter_files")
    observed = {str(path.relative_to(adapter_dir)): file_sha256(path)
                for path in sorted(adapter_dir.rglob("*")) if path.is_file()}
    if not expected or observed != expected:
        raise ValueError(f"{lr} adapter bytes differ from sealed run")
    attempt = run_path.parents[3]
    final = load_json(attempt / "finalization.json")
    backup = sealed_json(attempt / "terminal-backup-verification.json", "evidence_sha256")
    if (final.get("status") != "terminal-backup-verified-and-exact-resources-absent-twice"
        or final.get("training_exit_code") != 0 or backup.get("status") != "verified"
        or backup.get("schema_version") != "ganesh-mini-gcs-backup-manifest/v1"
        or backup.get("object_count") != 54):
        raise ValueError(f"{lr} terminal backup or resource teardown is incomplete")
    objects = backup.get("objects", [])
    if len(objects) != 54 or not all(row.get("verified") is True for row in objects):
        raise ValueError(f"{lr} terminal object verification is incomplete")
    for source in (run_path, *sorted(path for path in adapter_dir.iterdir() if path.is_file())):
        relative = source.relative_to(attempt / "terminal-roundtrip")
        matching = [row for row in objects if row.get("object_uri", "").endswith(f"/terminal/{relative}")]
        if len(matching) != 1 or matching[0].get("verified_download_sha256") != file_sha256(source):
            raise ValueError(f"{lr} evaluation input differs from independently verified GCS backup: {relative}")
    return {"run": run, "run_path": run_path, "adapter_dir": adapter_dir}


def _config(lr: str, phase: str, run: dict[str, Any]) -> dict[str, Any]:
    canary = phase == "canary"
    config = {
        "schema_version": "ganesh-mini-production-inference/v1",
        "run_id": f"ganesh-mini-gate3-{lr}-{phase}-v1",
        "classification": "private_candidate_development",
        "task_globs": [CANARY_TASK_GLOB if canary else DEVELOPMENT_TASK_GLOB],
        "allowed_surface": "development",
        "expected_task_count": 30 if canary else 180,
        "model_contract": "configs/model/qwen3_5_2b.contract.json",
        "model_inventory": "configs/model/qwen3_5_2b.inventory.json",
        "model_dir": "models/qwen3.5-2b-15852e8",
        "auto_model_class": "image-text-to-text",
        "runtimes": "configs/eval/runtimes.json",
        "output_dir": f"measurement/inference/development/ganesh-mini-gate3-{lr}-{phase}-v1",
        "serving": {"modality": "text-only", "enable_thinking": False, "context_length": 8192, "add_generation_prompt": True},
        "generation": {"do_sample": False, "max_new_tokens": 4096, "use_cache": True},
        "execution": {"batch_size": 4, "verifier_workers": 12, "length_bucket_width": 256, "required_device": "cuda"},
        "extractor_id": "ganesh-code-fence-v1",
        "adapter": {
            "served_model_id": f"ganesh-mini-gate3-{lr}",
            "dir": f"candidate-inputs/{lr}/adapter-final",
            "run_evidence": f"candidate-inputs/{lr}/run-evidence.json",
        },
    }
    validate_config(config)
    if run["identities"].get("model_revision") != load_json(ROOT / config["model_contract"])["revision"]:
        raise ValueError("candidate upstream revision differs from serving contract")
    return config


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def prepare(workspace_path: Path, canary_path: Path, first_run: Path, second_run: Path,
            output: Path, selection_path: Path | None = None) -> dict[str, Any]:
    if output.exists():
        raise ValueError("output already exists; preserve prior staging evidence")
    workspace = verify_workspace(workspace_path)
    canary = verify_canary(canary_path, workspace)
    candidates = {"1e-5": verify_candidate(first_run, "1e-5"),
                  "3e-5": verify_candidate(second_run, "3e-5")}
    first_ids = candidates["1e-5"]["run"]["identities"]
    second_ids = candidates["3e-5"]["run"]["identities"]
    for field in ("prepared_data_sha256", "prepared_manifest_sha256", "recipe_sha256",
                  "validation_data_sha256", "model_revision"):
        if first_ids.get(field) != second_ids.get(field):
            raise ValueError(f"candidate training identity differs: {field}")
    selected_lr = None
    selection = None
    if selection_path is not None:
        selection = sealed_json(selection_path, "report_sha256")
        selected_lr = selection.get("selected_learning_rate")
        selected = selection.get("selected_candidate", {})
        summaries = selection.get("candidates", {})
        base_artifact = selection.get("base", {}).get("model", {}).get("artifact_sha256")
        expected_artifact = sha256_object({
            "base": base_artifact,
            "adapter": candidates[selected_lr]["run"]["adapter_files"],
            "run_evidence_sha256": candidates[selected_lr]["run"]["evidence_sha256"],
        }) if selected_lr in candidates and isinstance(base_artifact, str) else None
        expected_task_ids = {row["task_id"] for row in canary["tasks"]}
        if (selection.get("schema_version") != "ganesh-mini-capability-canary-selection/v1"
            or selection.get("status") != "selected" or selected_lr not in candidates
            or selection.get("authority") != "selected-candidate-180-task-development-evaluation-only"
            or selection.get("gate3_quality_passed") is not False
            or selection.get("decision_tasks_opened") != 0
            or selection.get("evaluation_workspace_manifest_sha256") != workspace["manifest_sha256"]
            or selection.get("canary_manifest_sha256") != canary["manifest_sha256"]
            or selected.get("run_evidence_sha256") != candidates[selected_lr]["run"]["evidence_sha256"]
            or selected.get("adapter_files") != candidates[selected_lr]["run"]["adapter_files"]
            or selected.get("model") != summaries.get(selected_lr, {}).get("model")
            or selected.get("model", {}).get("artifact_sha256") != expected_artifact
            or selected.get("model", {}).get("revision") != first_ids["model_revision"]
            or len(selection.get("task_ids", [])) != 30
            or set(selection.get("task_ids", [])) != expected_task_ids
            or set(summaries) != set(candidates)
            or any(summaries[lr].get("run_evidence_sha256") != candidates[lr]["run"]["evidence_sha256"]
                   or summaries[lr].get("adapter_files") != candidates[lr]["run"]["adapter_files"]
                   or set(summaries[lr].get("task_evidence", {})) != expected_task_ids
                   for lr in candidates)
            or selected.get("result_collection_sha256") != summaries[selected_lr].get("result_collection_sha256")
            or selected.get("task_evidence") != summaries[selected_lr].get("task_evidence")):
            raise ValueError("development stage lacks exact sealed canary selection")
    output.mkdir(parents=True)
    files: list[tuple[Path, str]] = []
    for lr, candidate in candidates.items():
        files.append((candidate["run_path"], f"candidate-inputs/{lr}/run-evidence.json"))
        for path in sorted(candidate["adapter_dir"].iterdir()):
            if path.is_file():
                files.append((path, f"candidate-inputs/{lr}/adapter-final/{path.name}"))
    bundle = output / "candidate-inputs.tar.gz"
    with bundle.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for source, name in files:
                    info = archive.gettarinfo(str(source), arcname=name)
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    info.mtime = 0
                    with source.open("rb") as handle:
                        archive.addfile(info, handle)
    phases = [(lr, "canary") for lr in candidates]
    if selected_lr is not None:
        phases.append((selected_lr, "development"))
    configs = {}
    for lr, phase in phases:
        config = _config(lr, phase, candidates[lr]["run"])
        name = f"{phase}-{lr}.json"
        _write_json(output / name, config)
        configs[name] = {"sha256": file_sha256(output / name), "config_sha256": sha256_object(config)}
    selection_artifact = None
    if selection_path is not None:
        selection_copy = output / "selection-report.json"
        selection_copy.write_bytes(selection_path.read_bytes())
        if sealed_json(selection_copy, "report_sha256") != selection:
            raise ValueError("copied canary selection differs")
        selection_artifact = {"path": selection_copy.name, "sha256": file_sha256(selection_copy),
                              "report_sha256": selection["report_sha256"]}
    card = {
        "schema_version": "ganesh-mini-gate3-evaluation-staging/v1",
        "status": "prepared-only",
        "evaluation_workspace_manifest_sha256": workspace["manifest_sha256"],
        "evaluation_workspace_archive_sha256": workspace["archive"]["sha256"],
        "canary_manifest_sha256": canary["manifest_sha256"],
        "canary_task_ids": sorted(row["task_id"] for row in canary["tasks"]),
        "candidate_runs": {lr: {"run_evidence_sha256": candidate["run"]["evidence_sha256"],
                                "adapter_files": candidate["run"]["adapter_files"]}
                           for lr, candidate in candidates.items()},
        "candidate_input_bundle": {"sha256": file_sha256(bundle), "files":
                                   [{"path": name, "sha256": file_sha256(source)} for source, name in files]},
        "configs": configs,
        "selected_learning_rate": selected_lr,
        "selection_report_sha256": selection["report_sha256"] if selection else None,
        "selection_report_artifact": selection_artifact,
        "requires_before_execution": ["qualified CUDA evaluator", "separate offline evaluation workspace",
                                      "pinned model materialization", "network-disabled resource-limited verifier images",
                                      "single allocation and watcher", "terminal GCS backup before exact resource teardown"],
        "decision_tasks_opened": 0,
    }
    card["card_sha256"] = sha256_object(card)
    _write_json(output / "evaluation-card.json", card)
    return card


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-manifest", type=Path, required=True)
    parser.add_argument("--canary-manifest", type=Path, required=True)
    parser.add_argument("--first-run", type=Path, required=True)
    parser.add_argument("--second-run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--selection", type=Path)
    args = parser.parse_args()
    card = prepare(args.workspace_manifest.resolve(), args.canary_manifest.resolve(),
                   args.first_run.resolve(), args.second_run.resolve(), args.output.resolve(),
                   args.selection.resolve() if args.selection else None)
    print(json.dumps({"status": card["status"], "card_sha256": card["card_sha256"],
                      "configs": sorted(card["configs"])}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
