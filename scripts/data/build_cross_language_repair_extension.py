#!/usr/bin/env python3
"""Freeze content-blind McEval cross-language repair fallback source pools."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "ganesh-mini-cross-language-repair-extension/v1"
MANIFEST_SCHEMA_VERSION = "ganesh-mini-cross-language-repair-extension-manifest/v1"
SEED = "ganesh-mini-gate2-v3-cross-language-repair-fallback-v1"
DERIVATION_KIND = "cross_language_repair_fallback"
DATASET = "Multilingual-Multimodal-NLP/McEval-Instruct"
POOL_SPECS = (("javascript", "typescript"), ("java", "javascript"))


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{number}: expected an object")
            rows.append(value)
    return rows


def source_identity(value: Any) -> tuple[str, str, str, str] | None:
    if not isinstance(value, dict):
        return None
    fields = tuple(value.get(key) for key in ("dataset", "revision", "record_id", "source_record_sha256"))
    if all(isinstance(item, str) and item for item in fields):
        return fields  # type: ignore[return-value]
    return None


def walk(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def load_structured(path: Path) -> Any:
    if path.suffix == ".jsonl":
        return read_jsonl(path)
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(candidate for candidate in path.rglob("*") if candidate.suffix in {".json", ".jsonl"}))
        elif path.suffix in {".json", ".jsonl"}:
            files.append(path)
        else:
            raise ValueError(f"unsupported evidence path: {path}")
    return sorted(set(files), key=lambda item: str(item))


def collect_exclusions(
    prior_corpus: Path,
    v2_artifacts: list[Path],
    current_queue_rows: list[dict[str, Any]],
    evidence_paths: list[Path],
) -> tuple[set[tuple[str, str, str, str]], set[str], dict[str, Any]]:
    """Collect lineages and queue IDs without inspecting any evaluation artifact."""
    excluded: set[tuple[str, str, str, str]] = set()
    excluded_ids: set[str] = set()
    by_id = {row.get("id"): row for row in current_queue_rows if isinstance(row.get("id"), str)}
    inputs = [prior_corpus, *v2_artifacts]
    for path in inputs:
        for node in walk(load_structured(path)):
            identity = source_identity(node)
            if identity:
                excluded.add(identity)

    # All current repair rows are excluded, even if no classifier evidence exists.
    for row in current_queue_rows:
        if row.get("task_type") != "repair":
            continue
        identifier = row.get("id")
        if isinstance(identifier, str):
            excluded_ids.add(identifier)
        identity = source_identity(row.get("source"))
        if not identity:
            raise ValueError(f"repair queue row has incomplete lineage: {identifier!r}")
        excluded.add(identity)

    files = evidence_files(evidence_paths)
    evidence_inventory = [
        {"path": str(path), "bytes": path.stat().st_size, "sha256": file_sha256(path)}
        for path in files
    ]
    for path in files:
        for node in walk(load_structured(path)):
            identity = source_identity(node)
            if identity:
                excluded.add(identity)
            if not isinstance(node, dict):
                continue
            for key in ("source_queue_id",):
                if isinstance(node.get(key), str):
                    excluded_ids.add(node[key])
            for key in ("source_queue_ids", "batch_source_queue_ids"):
                values = node.get(key)
                if isinstance(values, list):
                    excluded_ids.update(value for value in values if isinstance(value, str))

    unresolved_ids = sorted(identifier for identifier in excluded_ids if identifier not in by_id)
    # IDs outside the current queue can legitimately belong to earlier snapshots. Their
    # embedded lineage must be supplied by a prior/v2 artifact or evidence record.
    for identifier in sorted(excluded_ids & by_id.keys()):
        identity = source_identity(by_id[identifier].get("source"))
        if not identity:
            raise ValueError(f"evidence queue ID resolves to incomplete lineage: {identifier}")
        excluded.add(identity)
    return excluded, excluded_ids, {
        "prior_and_v2_artifact_count": len(inputs),
        "repair_evidence_file_count": len(files),
        "repair_evidence_total_bytes": sum(item["bytes"] for item in evidence_inventory),
        "repair_evidence_inventory_sha256": sha256_bytes(canonical_json(evidence_inventory)),
        "referenced_source_queue_id_count": len(excluded_ids),
        "unresolved_historical_source_queue_id_count": len(unresolved_ids),
        "unresolved_historical_source_queue_ids_sha256": sha256_bytes(canonical_json(unresolved_ids)),
    }


def stable_order(source_language: str, target_lane: str, identity: tuple[str, str, str, str]) -> str:
    return sha256_bytes("\0".join((SEED, source_language, target_lane, *identity)).encode())


def load_mceval_roots(path: Path, metadata: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    if metadata.get("dataset") != DATASET:
        raise ValueError("config McEval dataset identity is not pinned to the approved dataset")
    if file_sha256(path) != metadata.get("sha256"):
        raise ValueError("pinned McEval snapshot hash mismatch")
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("McEval snapshot must be a JSON array")
    pools = {source_language: [] for source_language, _ in POOL_SPECS}
    for index, row in enumerate(raw):
        if not isinstance(row, dict):
            raise ValueError(f"McEval row {index} is not an object")
        language = row.get("language")
        instruction = row.get("instruction")
        source_language = language.casefold() if isinstance(language, str) else ""
        if source_language not in pools or not isinstance(instruction, str) or not instruction.strip():
            continue
        record_id = f"row-{index:05d}"
        source = {
            "dataset": metadata["dataset"],
            "uri": metadata["uri"],
            "revision": metadata["revision"],
            "record_id": record_id,
            "license": metadata["license"],
            "license_uri": metadata["license_uri"],
            "source_record_sha256": sha256_bytes(canonical_json(row)),
        }
        pools[source_language].append({"source": source, "stimulus": instruction})
    return pools


def transformation(source_language: str, target_lane: str) -> str:
    return (
        f"Content-blind cross-language repair fallback from {source_language} to {target_lane}: preserve the "
        "pinned McEval instruction verbatim as a drafting stimulus; a later isolated teacher may derive one "
        f"self-contained {target_lane} repair task. Source answers and tests are not trusted, and neither "
        "capability labels nor evaluation content influenced this pool selection."
    )


def build(
    config_path: Path,
    mceval_path: Path,
    prior_corpus: Path,
    v2_artifacts: list[Path],
    current_queue_path: Path,
    repair_evidence: list[Path],
) -> tuple[list[dict[str, Any]], dict[str, Any], bytes]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    metadata = config.get("sources", {}).get("mceval")
    if not isinstance(metadata, dict):
        raise ValueError("config has no pinned McEval source metadata")
    current_bytes = current_queue_path.read_bytes()
    if current_bytes and not current_bytes.endswith(b"\n"):
        raise ValueError("current full queue must end with LF for a byte-preserving JSONL union")
    current_rows = read_jsonl(current_queue_path)
    current_ids = [row.get("id") for row in current_rows]
    if any(not isinstance(identifier, str) or not identifier for identifier in current_ids):
        raise ValueError("current queue contains a missing or invalid ID")
    if len(current_ids) != len(set(current_ids)):
        raise ValueError("current queue contains duplicate IDs")
    existing_repair = [source_identity(row.get("source")) for row in current_rows if row.get("task_type") == "repair"]
    if any(identity is None for identity in existing_repair) or len(existing_repair) != len(set(existing_repair)):
        raise ValueError("current queue repair lineages are incomplete or not globally unique")

    exclusions, excluded_ids, exclusion_report = collect_exclusions(
        prior_corpus, v2_artifacts, current_rows, repair_evidence,
    )
    pools = load_mceval_roots(mceval_path, metadata)
    extension: list[dict[str, Any]] = []
    pool_counts: dict[str, Any] = {}
    for source_language, target_lane in POOL_SPECS:
        eligible = []
        for item in pools[source_language]:
            identity = source_identity(item["source"])
            assert identity is not None
            if identity not in exclusions:
                eligible.append(item)
        eligible.sort(key=lambda item: stable_order(source_language, target_lane, source_identity(item["source"])))
        for ordinal, item in enumerate(eligible, 1):
            source = dict(item["source"])
            source["transformation"] = transformation(source_language, target_lane)
            extension.append({
                "schema_version": SCHEMA_VERSION,
                "id": f"gate2-v3-xlang-{source_language}-to-{target_lane}-repair-{ordinal:04d}",
                "lane": target_lane,
                "task_type": "repair",
                "source_language": source_language,
                "target_lane": target_lane,
                "original_role": "generation",
                "derivation_kind": DERIVATION_KIND,
                "stimulus": item["stimulus"],
                "source": source,
            })
        pool_counts[f"{source_language}_to_{target_lane}"] = {
            "snapshot_roots": len(pools[source_language]),
            "excluded_roots": len(pools[source_language]) - len(eligible),
            "frozen_roots": len(eligible),
        }

    extension_ids = [row["id"] for row in extension]
    if len(extension_ids) != len(set(extension_ids)) or set(extension_ids) & set(current_ids):
        raise ValueError("extension IDs are not globally unique")
    extension_lineages = [source_identity(row["source"]) for row in extension]
    if len(extension_lineages) != len(set(extension_lineages)):
        raise ValueError("extension repair lineages are not globally unique")
    if set(extension_lineages) & set(existing_repair):
        raise ValueError("extension collides with a current repair lineage")

    extension_bytes = b"".join(canonical_json(row) + b"\n" for row in extension)
    union_bytes = current_bytes + extension_bytes
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "status": "passed",
        "selection_contract": {
            "seed": SEED,
            "ordering": "sha256(seed\\0source_language\\0target_lane\\0dataset\\0revision\\0record_id\\0source_record_sha256)",
            "content_blind": True,
            "capability_keywords_used": False,
            "evaluation_content_read": False,
            "retries": 0,
            "pool_specs": [
                {"source_language": source, "target_lane": target, "derivation_kind": DERIVATION_KIND}
                for source, target in POOL_SPECS
            ],
        },
        "inputs": {
            "config": {"path": str(config_path), "sha256": file_sha256(config_path)},
            "mceval_snapshot": {"path": str(mceval_path), "sha256": file_sha256(mceval_path)},
            "prior_corpus": {"path": str(prior_corpus), "sha256": file_sha256(prior_corpus)},
            "v2_artifacts": [{"path": str(path), "sha256": file_sha256(path)} for path in v2_artifacts],
            "current_full_queue": {"path": str(current_queue_path), "bytes": len(current_bytes), "sha256": sha256_bytes(current_bytes)},
            "repair_evidence": {
                "paths": [str(path) for path in repair_evidence],
                "inventory_sha256": exclusion_report["repair_evidence_inventory_sha256"],
                "files": exclusion_report["repair_evidence_file_count"],
                "bytes": exclusion_report["repair_evidence_total_bytes"],
            },
        },
        "exclusions": {
            **exclusion_report,
            "source_identity_count": len(exclusions),
            "source_id_count": len(excluded_ids),
            "source_identity_set_sha256": sha256_bytes(canonical_json(sorted(exclusions))),
        },
        "pools": pool_counts,
        "extension": {"records": len(extension), "bytes": len(extension_bytes), "sha256": sha256_bytes(extension_bytes)},
        "union": {
            "records": len(current_rows) + len(extension), "bytes": len(union_bytes),
            "sha256": sha256_bytes(union_bytes), "current_queue_is_exact_byte_prefix": True,
        },
        "counts_by_target_lane": dict(sorted(Counter(row["target_lane"] for row in extension).items())),
    }
    manifest["manifest_sha256"] = sha256_bytes(canonical_json(manifest))
    return extension, manifest, union_bytes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--mceval", type=Path, required=True)
    parser.add_argument("--prior-corpus", type=Path, required=True)
    parser.add_argument("--v2-artifact", type=Path, action="append", required=True)
    parser.add_argument("--current-full-queue", type=Path, required=True)
    parser.add_argument("--repair-evidence", type=Path, action="append", default=[])
    parser.add_argument("--extension-output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    parser.add_argument("--union-output", type=Path, required=True)
    args = parser.parse_args()
    rows, manifest, union_bytes = build(
        args.config, args.mceval, args.prior_corpus, args.v2_artifact,
        args.current_full_queue, args.repair_evidence,
    )
    extension_bytes = b"".join(canonical_json(row) + b"\n" for row in rows)
    for path in (args.extension_output, args.manifest_output, args.union_output):
        path.parent.mkdir(parents=True, exist_ok=True)
    args.extension_output.write_bytes(extension_bytes)
    args.union_output.write_bytes(union_bytes)
    args.manifest_output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "passed", "extension_records": len(rows),
        "extension_sha256": manifest["extension"]["sha256"],
        "union_sha256": manifest["union"]["sha256"],
        "manifest_sha256": manifest["manifest_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
