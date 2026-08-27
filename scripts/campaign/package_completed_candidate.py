#!/usr/bin/env python3
"""Package one completed Gate 3 LR candidate for a later sealed continuation."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import tarfile
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ATTEMPT = "20260827T090603Z"
DEFAULT_SOURCE = ROOT / (
    "measurement/gate3/gcloud/20260827T090603Z/finalization/terminal-download/"
    "output/campaign/training/lr-1e-5"
)
DEFAULT_BACKUP = ROOT / (
    "measurement/gate3/gcloud/20260827T090603Z/finalization/terminal-backup-manifest.json"
)
DEFAULT_TERMINAL = ROOT / (
    "measurement/gate3/gcloud/20260827T090603Z/finalization/terminal-validation.json"
)
DEFAULT_CARD = ROOT / "measurement/gate3/gcloud/20260827T090603Z/execution-card.json"
DEFAULT_ARCHIVE = ROOT / "artifacts/gcloud-inputs/gate3/completed-lr-1e-5.tar.gz"
DEFAULT_MANIFEST = ROOT / "measurement/gate3/completed_candidate_lr_1e_5.json"
REQUIRED_FILES = (
    "adapter-final/README.md",
    "adapter-final/adapter_config.json",
    "adapter-final/adapter_model.safetensors",
    "run-evidence.json",
)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def _tar_info(path: Path, relative: str) -> tarfile.TarInfo:
    info = tarfile.TarInfo(relative)
    info.size = path.stat().st_size
    info.mode = 0o644
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    return info


def build(
    source: Path,
    backup_path: Path,
    terminal_path: Path,
    execution_card_path: Path,
    archive: Path,
    manifest_path: Path,
    *,
    attempt_id: str = DEFAULT_ATTEMPT,
) -> dict[str, Any]:
    source = source.resolve(strict=True)
    backup = load_sealed(backup_path.resolve(strict=True), "evidence_sha256")
    terminal = load_sealed(terminal_path.resolve(strict=True), "evidence_sha256")
    execution = load_sealed(execution_card_path.resolve(strict=True), "execution_sha256")
    run = load_sealed(source / "run-evidence.json", "evidence_sha256")

    expected_prefix = (
        "gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/"
        f"gate3/{attempt_id}/runtime-terminal-{attempt_id}"
    )
    if backup.get("status") != "verified" or backup.get("prefix") != expected_prefix:
        raise ValueError("source terminal backup is not the expected verified prefix")
    if (
        terminal.get("status") != "sealed-failure"
        or terminal.get("attempt_id") != attempt_id
        or terminal.get("backup_manifest_sha256") != backup["evidence_sha256"]
        or terminal.get("deletion_eligible") is not True
    ):
        raise ValueError("source terminal validation does not bind the verified backup")
    if (
        execution.get("execution", {}).get("attempt_id") != attempt_id
        or terminal.get("execution_sha256") != execution["execution_sha256"]
    ):
        raise ValueError("source execution card is not bound by terminal validation")
    if (
        run.get("schema_version") != "ganesh-mini-sft-run/v2"
        or run.get("status") != "complete"
        or run.get("identities", {}).get("phase") != "lr-candidate"
        or run.get("identities", {}).get("learning_rate") != "1e-05"
        or run.get("identities", {}).get("model_revision")
        != "15852e8c16360a2fea060d615a32b45270f8a8fc"
        or run.get("state", {}).get("seen_tokens") != 461235
        or run.get("planned_end_row") != 1399
        or run.get("save_reload", {}).get("passed") is not True
    ):
        raise ValueError("source candidate is not the completed frozen 1e-5 epoch")

    object_rows = {
        row["object_uri"].removeprefix(expected_prefix.rstrip("/") + "/"): row
        for row in backup.get("objects", [])
        if row.get("object_uri", "").startswith(expected_prefix.rstrip("/") + "/")
    }
    entries: list[dict[str, Any]] = []
    for relative in REQUIRED_FILES:
        path = source / relative
        if not path.is_file():
            raise ValueError(f"completed candidate file is missing: {relative}")
        digest = file_sha256(path)
        terminal_relative = f"output/campaign/training/lr-1e-5/{relative}"
        row = object_rows.get(terminal_relative)
        if row is None or row.get("verified") is not True or row.get("downloaded_sha256") != digest:
            raise ValueError(f"candidate file is not bound by terminal backup: {relative}")
        entries.append({"path": relative, "size_bytes": path.stat().st_size, "sha256": digest})

    adapter_hashes = run.get("adapter_files", {})
    for relative in REQUIRED_FILES:
        if relative.startswith("adapter-final/"):
            name = Path(relative).name
            if adapter_hashes.get(name) != next(row["sha256"] for row in entries if row["path"] == relative):
                raise ValueError(f"run evidence does not bind adapter file: {name}")

    archive.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=archive.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with temporary_path.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
                with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as bundle:
                    for relative in REQUIRED_FILES:
                        path = source / relative
                        with path.open("rb") as handle:
                            bundle.addfile(_tar_info(path, relative), handle)
        os.replace(temporary_path, archive)
    finally:
        temporary_path.unlink(missing_ok=True)

    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-completed-candidate/v1",
        "status": "sealed",
        "candidate": {
            "label": "lr-1e-5",
            "learning_rate": 0.00001,
            "run_evidence_sha256": run["evidence_sha256"],
            "seen_tokens": 461235,
            "unique_train_records": 1399,
            "adapter_model_sha256": adapter_hashes["adapter_model.safetensors"],
        },
        "model": {
            "model_id": "Qwen/Qwen3.5-2B",
            "revision": run["identities"]["model_revision"],
        },
        "training_inputs": {
            "card_sha256": run["identities"]["card_sha256"],
            "config_sha256": run["identities"]["config_sha256"],
            "prepared_data_sha256": run["identities"]["prepared_data_sha256"],
            "prepared_manifest_sha256": run["identities"]["prepared_manifest_sha256"],
            "recipe_sha256": run["identities"]["recipe_sha256"],
            "validation_data_sha256": run["identities"]["validation_data_sha256"],
        },
        "source": {
            "attempt_id": attempt_id,
            "gcs_terminal_prefix": expected_prefix,
            "execution_sha256": execution["execution_sha256"],
            "terminal_backup_sha256": backup["evidence_sha256"],
            "terminal_validation_sha256": terminal["evidence_sha256"],
        },
        "files": entries,
        "archive": {"path": str(archive.relative_to(ROOT)), "size_bytes": archive.stat().st_size, "sha256": file_sha256(archive)},
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--terminal-backup", type=Path, default=DEFAULT_BACKUP)
    parser.add_argument("--terminal-validation", type=Path, default=DEFAULT_TERMINAL)
    parser.add_argument("--execution-card", type=Path, default=DEFAULT_CARD)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--attempt-id", default=DEFAULT_ATTEMPT)
    args = parser.parse_args()
    result = build(
        args.source, args.terminal_backup, args.terminal_validation,
        args.execution_card, args.archive, args.manifest, attempt_id=args.attempt_id,
    )
    print(json.dumps({"status": result["status"], "manifest_sha256": result["manifest_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
