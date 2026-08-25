#!/usr/bin/env python3
"""Build a deletion-only Gate 1 terminal envelope from verified wrapper failure evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


EXPECTED_WRAPPER_FILES = {
    "bootstrap-files.sha256",
    "controller-exit-code.txt",
    "controller.stderr.log",
    "controller.stdout.log",
}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def synthesize(manifest_path: Path, wrapper_root: Path, card_path: Path, output_root: Path) -> None:
    manifest = load_sealed(manifest_path, "evidence_sha256")
    card = load_sealed(card_path, "execution_sha256")
    prefix = manifest.get("prefix", "").rstrip("/") + "/"
    objects = manifest.get("objects", [])
    rows = {
        row["object_uri"].removeprefix(prefix): row
        for row in objects
        if row.get("object_uri", "").startswith(prefix)
    }
    if (
        manifest.get("status") != "verified"
        or len(rows) != len(objects)
        or set(rows) != EXPECTED_WRAPPER_FILES
        or not all(row.get("verified") is True for row in objects)
    ):
        raise ValueError("wrapper failure backup is not the exact verified envelope")
    for name, row in rows.items():
        path = wrapper_root / name
        if not path.is_file() or file_sha256(path) != row.get("downloaded_sha256"):
            raise ValueError(f"wrapper download is absent or mismatched: {name}")

    code_text = (wrapper_root / "controller-exit-code.txt").read_text(encoding="utf-8").strip()
    try:
        code = int(code_text)
    except ValueError as error:
        raise ValueError("wrapper controller exit code is not an integer") from error
    if code == 0 or not (wrapper_root / "controller.stderr.log").read_bytes():
        raise ValueError("wrapper failure lacks a nonzero exit or diagnostic")

    bootstrap: list[tuple[str, str]] = []
    for line in (wrapper_root / "bootstrap-files.sha256").read_text(encoding="utf-8").splitlines():
        digest, name = line.split(None, 1)
        bootstrap.append((digest, name.lstrip("*")))
    expected_hashes = {
        card["launch"]["metadata_wrapper"]["sha256"],
        card["launch"]["controller"]["sha256"],
    }
    if len(bootstrap) != 2 or {row[0] for row in bootstrap} != expected_hashes:
        raise ValueError("wrapper bootstrap inventory does not bind the executable card")

    output_root.mkdir(parents=True, exist_ok=False)
    for name in sorted(EXPECTED_WRAPPER_FILES):
        shutil.copy2(wrapper_root / name, output_root / name)
    shutil.copy2(card_path, output_root / "execution-card.json")
    (output_root / "startup-exit-code.txt").write_text(f"{code}\n", encoding="utf-8")
    files = sorted(path for path in output_root.iterdir() if path.is_file())
    inventory = "".join(f"{file_sha256(path)}  ./{path.name}\n" for path in files)
    (output_root / "runtime-files.sha256").write_text(inventory, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backup-manifest", type=Path, required=True)
    parser.add_argument("--download-root", type=Path, required=True)
    parser.add_argument("--execution-card", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    synthesize(args.backup_manifest, args.download_root, args.execution_card, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
