#!/usr/bin/env python3
"""Build a deterministic, verified terminal archive for a checkpoint sweep."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def verified_inventory(terminal: Path) -> list[dict[str, Any]]:
    inventory = terminal / "runtime-files.sha256"
    if not inventory.is_file():
        raise ValueError("terminal runtime inventory is missing")
    expected: dict[str, str] = {}
    for line in inventory.read_text(encoding="utf-8").splitlines():
        digest, marker, relative = line.partition("  ./")
        if marker != "  ./" or len(digest) != 64 or not relative:
            raise ValueError("terminal runtime inventory has an invalid row")
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts or relative in expected:
            raise ValueError("terminal runtime inventory has an unsafe or duplicate path")
        expected[relative] = digest
    observed = {
        str(path.relative_to(terminal))
        for path in terminal.rglob("*")
        if path.is_file() and path != inventory
    }
    if observed != set(expected):
        raise ValueError("terminal runtime inventory file set mismatch")
    rows = []
    for relative in sorted(expected):
        path = terminal / relative
        digest = file_sha256(path)
        if path.is_symlink() or digest != expected[relative]:
            raise ValueError(f"terminal runtime identity mismatch: {relative}")
        rows.append({"path": relative, "size_bytes": path.stat().st_size, "sha256": digest})
    return rows


def build(terminal: Path, output: Path, manifest_output: Path) -> dict[str, Any]:
    terminal = terminal.resolve()
    rows = verified_inventory(terminal)
    inventory = terminal / "runtime-files.sha256"
    inventory_row = {
        "path": "runtime-files.sha256",
        "size_bytes": inventory.stat().st_size,
        "sha256": file_sha256(inventory),
    }
    archive_rows = [*rows, inventory_row]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.PAX_FORMAT) as archive:
                directory = tarfile.TarInfo("terminal")
                directory.type = tarfile.DIRTYPE
                directory.mode = 0o755
                directory.mtime = directory.uid = directory.gid = 0
                directory.uname = directory.gname = ""
                archive.addfile(directory)
                for row in archive_rows:
                    source = terminal / row["path"]
                    info = tarfile.TarInfo(f"terminal/{row['path']}")
                    info.size = row["size_bytes"]
                    info.mode = 0o644
                    info.mtime = info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    with source.open("rb") as stream:
                        archive.addfile(info, stream)
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-checkpoint-sweep-recovery/v1",
        "status": "sealed",
        "purpose": "diagnostic-only checkpoint sweep recovery input",
        "promotion_authority": "none",
        "source_terminal_manifest_sha256": inventory_row["sha256"],
        "source_file_count": len(archive_rows),
        "source_bytes": sum(row["size_bytes"] for row in archive_rows),
        "files": archive_rows,
        "archive": {
            "size_bytes": output.stat().st_size,
            "sha256": file_sha256(output),
        },
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_output.parent.mkdir(parents=True, exist_ok=True)
    manifest_output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terminal", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    args = parser.parse_args()
    manifest = build(args.terminal, args.output, args.manifest_output)
    print(json.dumps({"archive": manifest["archive"], "manifest_sha256": manifest["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
