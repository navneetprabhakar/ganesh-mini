#!/usr/bin/env python3
"""Seal a self-describing proof that exact run-scoped GCloud resources are absent."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RESOURCE_KINDS = {"instance", "disk", "network", "subnet", "router", "nat"}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    scope = json.loads(args.scope.read_text(encoding="utf-8"))
    if scope.get("schema_version") != "ganesh-mini-gcloud-absence-scope/v1":
        raise SystemExit("unsupported absence scope")
    if not all(isinstance(scope.get(key), str) and scope[key] for key in ("project", "region", "zone", "run_id")):
        raise SystemExit("absence scope must bind project, region, zone, and run_id")
    resources = scope.get("expected_resources")
    if not isinstance(resources, list) or not resources:
        raise SystemExit("absence scope has no expected resources")
    identities = set()
    for resource in resources:
        identity = (resource.get("kind"), resource.get("name"), str(resource.get("id", "")))
        if identity[0] not in RESOURCE_KINDS or not identity[1] or identity in identities:
            raise SystemExit(f"invalid or duplicate expected resource: {resource}")
        identities.add(identity)
    queries = scope.get("queries")
    if not isinstance(queries, list) or {row.get("kind") for row in queries} != {row[0] for row in identities}:
        raise SystemExit("queries must cover every expected resource kind exactly")
    sealed_queries = []
    for query in queries:
        path = Path(query.get("path", ""))
        if not path.is_file():
            raise SystemExit(f"absence query output is missing: {path}")
        result = json.loads(path.read_text(encoding="utf-8"))
        if result != []:
            raise SystemExit(f"resource query is not empty for {query.get('kind')}")
        command = query.get("command")
        if not isinstance(command, list) or not command or scope["project"] not in " ".join(command):
            raise SystemExit("query command does not bind the expected project")
        location = scope["region"] if query["kind"] in {"subnet", "router", "nat"} else scope["zone"] if query["kind"] in {"instance", "disk"} else None
        if location is not None and location not in " ".join(command):
            raise SystemExit("query command does not bind the expected location")
        sealed_queries.append({
            "kind": query["kind"],
            "command": command,
            "path": str(path),
            "sha256": file_sha256(path),
            "result_count": 0,
        })
    evidence = {
        "schema_version": "ganesh-mini-gcloud-absence-proof/v2",
        "status": "passed",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "project": scope["project"],
        "region": scope["region"],
        "zone": scope["zone"],
        "run_id": scope["run_id"],
        "expected_resources": resources,
        "queries": sealed_queries,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
