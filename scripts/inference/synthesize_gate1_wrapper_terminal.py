#!/usr/bin/env python3
"""Build a deletion-only Gate 1 terminal envelope from verified wrapper failure evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
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


def parse_inventory(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split(None, 1)
        relative = relative.lstrip("*").removeprefix("./")
        if len(digest) != 64 or relative in rows or not relative:
            raise ValueError("partial terminal inventory contains an invalid or duplicate row")
        rows[relative] = digest
    if not rows:
        raise ValueError("partial terminal inventory is empty")
    return rows


def recover_partial(
    partial_manifest_path: Path,
    partial_root: Path,
    wrapper_manifest_path: Path,
    wrapper_root: Path,
    card_path: Path,
    output_root: Path,
) -> None:
    partial_manifest = load_sealed(partial_manifest_path, "evidence_sha256")
    prefix = partial_manifest.get("prefix", "").rstrip("/") + "/"
    objects = partial_manifest.get("objects", [])
    rows = {
        row["object_uri"].removeprefix(prefix): row
        for row in objects
        if row.get("object_uri", "").startswith(prefix)
    }
    inventory_path = partial_root / "runtime-files.sha256"
    inventory = parse_inventory(inventory_path)
    if (
        partial_manifest.get("status") != "verified"
        or len(rows) != len(objects)
        or set(rows) != set(inventory) | {"runtime-files.sha256"}
        or not all(row.get("verified") is True for row in objects)
    ):
        raise ValueError("partial terminal backup is not the exact inventoried envelope")
    for name, row in rows.items():
        path = partial_root / name
        if not path.is_file() or file_sha256(path) != row.get("downloaded_sha256"):
            raise ValueError(f"partial terminal download is absent or mismatched: {name}")
    for name, digest in inventory.items():
        if file_sha256(partial_root / name) != digest:
            raise ValueError(f"partial terminal inventory mismatch: {name}")
    if "execution-card.json" in inventory or "controller-exit-code.txt" in inventory:
        raise ValueError("partial recovery is only valid before card/controller binding")
    startup_code = int((partial_root / "startup-exit-code.txt").read_text(encoding="utf-8").strip())
    if startup_code == 0 or not (partial_root / "startup.stderr.log").read_bytes():
        raise ValueError("partial terminal lacks a nonzero startup exit or diagnostic")

    with tempfile.TemporaryDirectory(prefix="ganesh-wrapper-terminal-") as temporary:
        minimal = Path(temporary) / "minimal"
        synthesize(wrapper_manifest_path, wrapper_root, card_path, minimal)
        controller_code = int((minimal / "controller-exit-code.txt").read_text(encoding="utf-8").strip())
        if startup_code != controller_code:
            raise ValueError("partial and wrapper exit codes disagree")
        output_root.mkdir(parents=True, exist_ok=False)
        for name in sorted(inventory):
            shutil.copy2(partial_root / name, output_root / name)
        shutil.copy2(inventory_path, output_root / "original-runtime-files.sha256")
        for name in (
            "bootstrap-files.sha256",
            "controller-exit-code.txt",
            "controller.stderr.log",
            "controller.stdout.log",
            "execution-card.json",
        ):
            shutil.copy2(minimal / name, output_root / name)
    files = sorted(path for path in output_root.iterdir() if path.is_file())
    recovered_inventory = "".join(f"{file_sha256(path)}  ./{path.name}\n" for path in files)
    (output_root / "runtime-files.sha256").write_text(recovered_inventory, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backup-manifest", type=Path, required=True)
    parser.add_argument("--download-root", type=Path, required=True)
    parser.add_argument("--execution-card", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--partial-backup-manifest", type=Path)
    parser.add_argument("--partial-download-root", type=Path)
    args = parser.parse_args()
    if (args.partial_backup_manifest is None) != (args.partial_download_root is None):
        parser.error("partial backup manifest and download root must be provided together")
    if args.partial_backup_manifest is None:
        synthesize(args.backup_manifest, args.download_root, args.execution_card, args.output_dir)
    else:
        recover_partial(
            args.partial_backup_manifest,
            args.partial_download_root,
            args.backup_manifest,
            args.download_root,
            args.execution_card,
            args.output_dir,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
