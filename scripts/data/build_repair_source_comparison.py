#!/usr/bin/env python3
"""Build a content-free evaluation-separation result for v3 source stimuli.

This is the only v3 source-selection stage allowed to read frozen evaluation
tasks.  Its output contains source-queue IDs that must be excluded, aggregate
counts, and content hashes; it never serializes evaluation text, IDs, or paths.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_expansion import _tokens, canonical_json, normalized_sha256, simhash  # noqa: E402
from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.eval.contracts import sha256_text, validate_task  # noqa: E402


SCHEMA_VERSION = "ganesh-mini-content-free-source-comparison/v1"
MANIFEST_SCHEMA = "ganesh-mini-content-free-source-comparison-manifest/v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_source_queue(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = [row.get("id") for row in rows]
    if (
        not rows or any(not isinstance(identifier, str) or not identifier for identifier in ids)
        or len(set(ids)) != len(ids)
        or any(not isinstance(row.get("stimulus"), str) or not row["stimulus"] for row in rows)
    ):
        raise ValueError("source queue has malformed or duplicate records")
    return rows


def evaluation_files(roots: list[Path]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        files.extend(sorted(root.rglob("*.task.json")) if root.is_dir() else [root])
    if not files or len(set(files)) != len(files):
        raise ValueError("evaluation roots are empty or overlap")
    return files


def evaluation_surfaces(files: list[Path]) -> tuple[list[str], list[dict[str, Any]]]:
    surfaces: list[str] = []
    identities: list[dict[str, Any]] = []
    for path in files:
        task = json.loads(path.read_text(encoding="utf-8"))
        validate_task(task)
        surfaces.append(task["prompt"]["text"])
        surfaces.append(task["validation"]["reference"]["code"])
        surfaces.extend(item["code"] for item in task["validation"]["known_bad"])
        surfaces.extend(item["content"] for item in task["files"])
        identities.append({"sha256": file_sha256(path), "bytes": path.stat().st_size})
    return surfaces, identities


def build_comparison(
    source_queue: Path, evaluation_roots: list[Path], fuzzy_limit: int = 3,
    minimum_tokens: int = 12,
) -> dict[str, Any]:
    if fuzzy_limit < 0 or minimum_tokens <= 0:
        raise ValueError("invalid fuzzy comparison parameters")
    rows = read_source_queue(source_queue)
    files = evaluation_files(evaluation_roots)
    surfaces, identities = evaluation_surfaces(files)
    exact = {sha256_text(value) for value in surfaces}
    normalized = {normalized_sha256(value) for value in surfaces}
    fuzzy = [(simhash(value), len(_tokens(value))) for value in surfaces]
    excluded: list[str] = []
    failures: Counter[str] = Counter()
    for row in rows:
        stimulus = row["stimulus"]
        stimulus_tokens = len(_tokens(stimulus))
        stimulus_simhash = simhash(stimulus) if stimulus_tokens >= minimum_tokens else None
        checks = {
            "exact": sha256_text(stimulus) in exact,
            "normalized": normalized_sha256(stimulus) in normalized,
            "fuzzy": stimulus_simhash is not None and any(
                count >= minimum_tokens and (stimulus_simhash ^ fingerprint).bit_count() <= fuzzy_limit
                for fingerprint, count in fuzzy
            ),
        }
        if any(checks.values()):
            excluded.append(row["id"])
            failures.update(name for name, failed in checks.items() if failed)
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA,
        "source_queue": {
            "sha256": file_sha256(source_queue), "bytes": source_queue.stat().st_size,
            "records": len(rows),
        },
        "evaluation_inputs": sorted(identities, key=lambda item: (item["sha256"], item["bytes"])),
        "policy": {
            "exact": "raw SHA-256 equality against evaluation prompt and code surfaces",
            "normalized": "NFKC casefolded whitespace-normalized SHA-256 equality",
            "fuzzy": "SimHash over complete source stimulus and evaluation surfaces",
            "prompt_simhash_max_hamming": fuzzy_limit,
            "minimum_fuzzy_tokens": minimum_tokens,
            "fail_closed": True,
        },
        "counts": {
            "source_records": len(rows), "evaluation_tasks": len(files),
            "evaluation_surfaces": len(surfaces), "excluded_sources": len(excluded),
            "failed_by_check": {name: failures[name] for name in ("exact", "normalized", "fuzzy")},
        },
        "content_exposure": {
            "evaluation_content_serialized": 0,
            "evaluation_identifiers_serialized": 0,
            "evaluation_paths_serialized": 0,
            "collision_identities_serialized": 0,
        },
    }
    manifest_sha = canonical_sha256(manifest)
    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "source_queue_sha256": file_sha256(source_queue),
        "exact_normalized_fuzzy_comparison_complete": True,
        "comparison_manifest_sha256": manifest_sha,
        "excluded_source_queue_ids": sorted(excluded),
        "excluded_source_count": len(excluded),
        "visibility": {
            "evaluation_content_exposed_to_construction": False,
            "evaluation_identifiers_exposed_to_construction": False,
            "evaluation_paths_exposed_to_construction": False,
        },
    }
    report["comparison_sha256"] = canonical_sha256(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-queue", type=Path, required=True)
    parser.add_argument("--evaluation-root", type=Path, action="append", required=True)
    parser.add_argument("--prompt-simhash-max-hamming", type=int, default=3)
    parser.add_argument("--minimum-fuzzy-tokens", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    report = build_comparison(
        args.source_queue, args.evaluation_root,
        args.prompt_simhash_max_hamming, args.minimum_fuzzy_tokens,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"excluded": report["excluded_source_count"], "comparison_sha256": report["comparison_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
