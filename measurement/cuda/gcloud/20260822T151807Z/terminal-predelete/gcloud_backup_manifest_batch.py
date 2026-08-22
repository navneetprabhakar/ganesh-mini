#!/usr/bin/env python3
"""Generation-pin, batch-download, SHA-256, and seal an immutable GCS prefix."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import defaultdict
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--download-dir", type=Path, required=True)
    args = parser.parse_args()
    listing = json.loads(
        subprocess.run(
            ["gcloud", "storage", "ls", "--json", f"{args.prefix}/**", f"--project={args.project}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )
    if not listing:
        raise SystemExit("refusing to seal an empty GCS prefix")
    prefix_path = args.prefix.split("/", 3)[3].rstrip("/")
    grouped: dict[str, list[tuple[dict, str]]] = defaultdict(list)
    for item in listing:
        metadata = item["metadata"]
        relative = metadata["name"].removeprefix(prefix_path + "/")
        grouped[str(Path(relative).parent)].append((metadata, relative))
    for parent, members in sorted(grouped.items()):
        destination = args.download_dir / parent
        destination.mkdir(parents=True, exist_ok=True)
        sources = [
            f"gs://{metadata['bucket']}/{metadata['name']}#{metadata['generation']}"
            for metadata, _ in members
        ]
        subprocess.run(
            ["gsutil", "-m", "-u", args.project, "cp", *sources, str(destination) + "/"],
            check=True,
        )
    entries = []
    for item in sorted(listing, key=lambda value: value["metadata"]["name"]):
        metadata = item["metadata"]
        relative = metadata["name"].removeprefix(prefix_path + "/")
        local = args.download_dir / relative
        size = local.stat().st_size
        digest = sha256(local)
        if size != int(metadata["size"]):
            raise SystemExit(f"size mismatch: {metadata['name']}")
        entries.append(
            {
                "object_uri": f"gs://{metadata['bucket']}/{metadata['name']}",
                "generation": metadata["generation"],
                "size": size,
                "downloaded_sha256": digest,
                "verified": True,
            }
        )
    evidence = {
        "schema_version": "ganesh-mini-gcs-backup-manifest/v1",
        "status": "verified",
        "project": args.project,
        "prefix": args.prefix,
        "object_count": len(entries),
        "objects": entries,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
