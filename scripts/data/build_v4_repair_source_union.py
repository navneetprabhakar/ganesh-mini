#!/usr/bin/env python3
"""Seal the exact v3 classified source parent plus the fixed v4 extension."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256


SCHEMA_VERSION = "ganesh-mini-gate2-v4-repair-source-union-manifest/v1"
PLAN_SHA256 = "79849d2f8b70ba69572b4c3fa1761bdb413562c6f6d9a12537d93a1724812ef6"
PARENT_SHA256 = "db2df5395914fd0395296b65a69ff589537ef9150458dc5a507dbb7332bb27b6"
EXTENSION_MANIFEST_SCHEMA = "ganesh-mini-gate2-v4-commitpackft-source-extension-manifest/v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def source_identity(row: dict[str, Any]) -> tuple[Any, ...]:
    source = row.get("source", {})
    return tuple(source.get(key) for key in (
        "dataset", "revision", "record_id", "source_record_sha256",
    ))


def build(
    parent_path: Path, extension_path: Path, extension_manifest_path: Path,
) -> tuple[bytes, dict[str, Any]]:
    parent_bytes = parent_path.read_bytes()
    extension_bytes = extension_path.read_bytes()
    if file_sha256(parent_path) != PARENT_SHA256 or not parent_bytes.endswith(b"\n"):
        raise ValueError("v3 terminal source parent differs from its frozen binding")
    manifest = json.loads(extension_manifest_path.read_text(encoding="utf-8"))
    body = dict(manifest)
    claimed = body.pop("manifest_sha256", None)
    if (
        manifest.get("schema_version") != EXTENSION_MANIFEST_SCHEMA
        or manifest.get("status") != "sealed-inactive-source-extension"
        or manifest.get("plan_sha256") != PLAN_SHA256
        or claimed != canonical_sha256(body)
        or manifest.get("extension", {}).get("sha256") != file_sha256(extension_path)
        or manifest.get("extension", {}).get("bytes") != len(extension_bytes)
        or manifest.get("extension", {}).get("records") != 3000
        or not extension_bytes.endswith(b"\n")
    ):
        raise ValueError("v4 source extension differs from its sealed manifest")
    parent_rows = read_jsonl(parent_path)
    extension_rows = read_jsonl(extension_path)
    rows = [*parent_rows, *extension_rows]
    identifiers = [row.get("id") for row in rows]
    identities = [source_identity(row) for row in rows]
    parent_identities = {source_identity(row) for row in parent_rows}
    extension_identities = [source_identity(row) for row in extension_rows]
    if (
        any(not isinstance(identifier, str) or not identifier for identifier in identifiers)
        or len(set(identifiers)) != len(identifiers)
        or any(None in identity for identity in identities)
        or len(set(extension_identities)) != len(extension_identities)
        or set(extension_identities) & parent_identities
    ):
        raise ValueError("v4 source extension overlaps or source union identities are incomplete")
    payload = parent_bytes + extension_bytes
    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": "sealed-classification-eligible",
        "plan_sha256": PLAN_SHA256,
        "parent": {
            "path": str(parent_path), "sha256": PARENT_SHA256,
            "bytes": len(parent_bytes), "records": len(parent_rows),
            "unique_source_lineages": len(parent_identities),
        },
        "extension": {
            "path": str(extension_path), "sha256": file_sha256(extension_path),
            "bytes": len(extension_bytes), "records": 3000,
            "manifest_sha256": manifest["manifest_sha256"],
            "unique_source_lineages": len(set(extension_identities)),
        },
        "union": {
            "bytes": len(payload), "records": len(rows),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "parent_is_exact_byte_prefix": True,
            "unique_source_ids": len(set(identifiers)),
            "unique_source_lineages": len(set(identities)),
        },
        "evaluation_artifacts_read": 0,
    }
    report["manifest_sha256"] = canonical_sha256(report)
    return payload, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--extension", type=Path, required=True)
    parser.add_argument("--extension-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    payload, manifest = build(args.parent, args.extension, args.extension_manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": manifest["status"], "records": manifest["union"]["records"],
        "union_sha256": manifest["union"]["sha256"],
        "manifest_sha256": manifest["manifest_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
