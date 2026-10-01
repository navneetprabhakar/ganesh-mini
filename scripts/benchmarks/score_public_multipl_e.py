#!/usr/bin/env python3
"""Fail-closed paired scoring of network-isolated public benchmark outputs."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path


LANGUAGES = ("go", "java", "js", "ts", "rs", "py")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def read_side(
    root: Path, run_prefix: str, side: str, language: str, verifier_image_digest: str,
) -> tuple[dict, dict[str, dict], str]:
    path = root / f"{run_prefix}-{side}-{language}"
    verifier_log = path / "verification-controller.log"
    log_text = verifier_log.read_text()
    if "--network none" not in log_text or verifier_image_digest not in log_text:
        raise ValueError(f"verifier sandbox binding missing for {side} {language}")
    manifest = json.loads((path / "manifest.json").read_text())
    if manifest.get("status") != "completed" or manifest.get("task_count", 0) < 1:
        raise ValueError(f"incomplete {side} {language} generation")
    seal = manifest.pop("manifest_sha256", None)
    if seal != canonical_sha256(manifest):
        raise ValueError(f"invalid {side} {language} generation manifest seal")
    manifest["manifest_sha256"] = seal
    names = manifest["selected_task_names"]
    if len(names) != manifest["task_count"] or len(set(names)) != len(names):
        raise ValueError(f"invalid selected task list for {side} {language}")
    expected = {f"{name}.results.json.gz" for name in names}
    files = {file.name: file for file in (path / "verified").glob("*.results.json.gz")}
    if set(files) != expected:
        raise ValueError(f"missing or extra verifier outputs for {side} {language}")
    results = {}
    for name in names:
        file = files[f"{name}.results.json.gz"]
        with gzip.open(file, "rt") as stream:
            value = json.load(stream)
        with gzip.open(path / "completions" / f"{name}.json.gz", "rt") as stream:
            completion = json.load(stream)
        if value.get("name") != name or len(value.get("results", [])) != 1:
            raise ValueError(f"invalid verifier result for {side} {language} {name}")
        if completion.get("name") != name or len(completion.get("completions", [])) != 1:
            raise ValueError(f"invalid completion for {side} {language} {name}")
        result = value["results"][0]
        if not isinstance(result.get("status"), str):
            raise ValueError(f"missing verifier status for {side} {language} {name}")
        expected_program = (
            completion["prompt"] + completion["completions"][0]
            + "\n" + completion["tests"]
        )
        if result.get("program") != expected_program:
            raise ValueError(f"stale verifier output for {side} {language} {name}")
        results[name] = {
            "status": result["status"],
            "result_file_sha256": sha256_file(file),
        }
    return manifest, results, sha256_file(verifier_log)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--languages", nargs="+", choices=LANGUAGES,
                        default=list(LANGUAGES))
    parser.add_argument("--run-prefix", default="sha30-v2")
    parser.add_argument("--rust-run-prefix", default=None,
                        help="Versioned Rust reassembly run; other lanes use --run-prefix")
    parser.add_argument("--verifier-image-digest", required=True)
    args = parser.parse_args()
    report = {
        "schema_version": "ganesh-mini-public-multipl-e-paired/v1",
        "status": "executed",
        "benchmark_use": "evaluation only; benchmark prompts and tests are not redistributed",
        "verifier_image_digest": args.verifier_image_digest,
        "verifier_runtime": {
            "network": "none", "cpus": 2, "memory": "4g", "pids_limit": 128,
            "cap_drop": "ALL", "no_new_privileges": True,
            "platform": "linux/amd64", "max_workers": 1,
        },
        "languages": {},
    }
    for language in args.languages:
        run_prefix = args.rust_run_prefix if language == "rs" and args.rust_run_prefix else args.run_prefix
        upstream, upstream_results, upstream_verifier_log_sha = read_side(
            args.root, run_prefix, "upstream", language, args.verifier_image_digest,
        )
        candidate, candidate_results, candidate_verifier_log_sha = read_side(
            args.root, run_prefix, "candidate", language, args.verifier_image_digest,
        )
        fields = (
            "dataset_id", "dataset_revision", "dataset_config",
            "dataset_file_sha256", "selected_task_names", "selection",
            "context_length", "max_new_tokens", "temperature", "seed",
            "prompt_template", "postprocessing", "llama_cpp_revision",
            "llama_server_sha256", "device",
        )
        for field in fields:
            if upstream.get(field) != candidate.get(field):
                raise ValueError(f"unpaired {language} field: {field}")
        if set(upstream_results) != set(candidate_results):
            raise ValueError(f"unpaired {language} verifier tasks")
        names = candidate["selected_task_names"]
        for name in names:
            base_path = args.root / f"{run_prefix}-upstream-{language}" / "raw" / f"{name}.json"
            tuned_path = args.root / f"{run_prefix}-candidate-{language}" / "raw" / f"{name}.json"
            base_raw = json.loads(base_path.read_text())
            tuned_raw = json.loads(tuned_path.read_text())
            for field in (
                "source_prompt_sha256", "tests_sha256", "user_prompt",
                "rendered_prompt_sha256", "input_token_ids",
            ):
                if base_raw.get(field) != tuned_raw.get(field):
                    raise ValueError(f"unpaired {language} {name} prompt field {field}")
        upstream_pass = sum(upstream_results[name]["status"] == "OK" for name in names)
        candidate_pass = sum(candidate_results[name]["status"] == "OK" for name in names)
        wins = sum(
            candidate_results[name]["status"] == "OK" and upstream_results[name]["status"] != "OK"
            for name in names
        )
        losses = sum(
            candidate_results[name]["status"] != "OK" and upstream_results[name]["status"] == "OK"
            for name in names
        )
        report["languages"][language] = {
            "tasks": len(names),
            "upstream_pass": upstream_pass,
            "candidate_pass": candidate_pass,
            "paired_wins": wins,
            "paired_losses": losses,
            "paired_ties": len(names) - wins - losses,
            "run_prefix": run_prefix,
            "dataset_id": candidate["dataset_id"],
            "dataset_revision": candidate["dataset_revision"],
            "dataset_config": candidate["dataset_config"],
            "selection": candidate["selection"],
            "selected_task_names": names,
            "serving_settings": {
                key: candidate[key] for key in (
                    "context_length", "max_new_tokens", "temperature", "seed",
                    "prompt_template", "postprocessing", "device",
                    "llama_cpp_revision", "llama_server_sha256",
                )
            },
            "candidate_model_id": candidate["model_id"],
            "candidate_model_sha256": candidate["model_sha256"],
            "upstream_model_id": upstream["model_id"],
            "upstream_model_sha256": upstream["model_sha256"],
            "candidate_generation_manifest_sha256": candidate["manifest_sha256"],
            "upstream_generation_manifest_sha256": upstream["manifest_sha256"],
            "candidate_generation_derivation": candidate.get("derivation"),
            "upstream_generation_derivation": upstream.get("derivation"),
            "candidate_verifier_log_sha256": candidate_verifier_log_sha,
            "upstream_verifier_log_sha256": upstream_verifier_log_sha,
            "per_task": {
                name: {
                    "upstream": upstream_results[name],
                    "candidate": candidate_results[name],
                } for name in names
            },
        }
    report["report_sha256"] = canonical_sha256(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise FileExistsError(args.output)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: {key: value for key, value in item.items() if key in {
        "tasks", "upstream_pass", "candidate_pass", "paired_wins", "paired_losses", "paired_ties"
    }} for k, item in report["languages"].items()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
