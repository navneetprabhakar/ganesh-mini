#!/usr/bin/env python3
"""Package the frozen development workspace plus checkpoint-sweep controllers."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BASE_MANIFEST = ROOT / "artifacts/eval/workspaces/development-v5.manifest.json"
ADDITIONS = (
    "scripts/campaign/run_checkpoint_sweep_host.py",
    "scripts/eval/build_checkpoint_sweep.py",
    "scripts/eval/summarize_checkpoint_sweep.py",
    "scripts/inference/build_checkpoint_sweep_gcloud_proposal.py",
    "scripts/inference/gcloud_checkpoint_sweep_metadata_wrapper.sh",
    "scripts/inference/gcloud_startup_checkpoint_sweep.sh",
    "measurement/gate4/checkpoint-sweep-20260909/configs/manifest.json",
    "measurement/gate4/checkpoint-sweep-20260909/configs/tokens-000000406491.json",
    "measurement/gate4/checkpoint-sweep-20260909/configs/tokens-000000814098.json",
    "measurement/gate4/checkpoint-sweep-20260909/configs/tokens-000001224637.json",
    "measurement/gate4/checkpoint-sweep-20260909/configs/tokens-000001629235.json",
    "measurement/gate4/checkpoint-sweep-20260909/configs/tokens-000002036559.json",
)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: Any) -> str:
    return digest_bytes(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    )


def build(output: Path, manifest_output: Path) -> dict[str, Any]:
    base = json.loads(BASE_MANIFEST.read_text(encoding="utf-8"))
    claimed = base.pop("manifest_sha256", None)
    if claimed != canonical_sha256(base):
        raise ValueError("development-v5 workspace manifest seal mismatch")
    paths = {row["path"] for row in base["files"]}
    paths.update(ADDITIONS)
    rows = []
    contents: dict[str, bytes] = {}
    for relative in sorted(paths):
        path = ROOT / relative
        if not path.is_file():
            raise ValueError(f"workspace source file is missing: {relative}")
        data = path.read_bytes()
        contents[relative] = data
        rows.append({"path": relative, "size_bytes": len(data), "sha256": digest_bytes(data)})
    output.parent.mkdir(parents=True, exist_ok=True)
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as bundle:
        for relative, data in contents.items():
            info = tarfile.TarInfo(relative)
            info.size = len(data); info.mtime = 0; info.uid = info.gid = 0; info.uname = info.gname = ""
            info.mode = 0o755 if relative.endswith(".sh") or relative.endswith(".py") else 0o644
            bundle.addfile(info, io.BytesIO(data))
    with output.open("wb") as target, gzip.GzipFile(filename="", mode="wb", fileobj=target, mtime=0) as compressed:
        compressed.write(raw.getvalue())
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-checkpoint-sweep-workspace/v1", "status": "sealed",
        "purpose": "evaluation-only Gate 4 checkpoint sweep", "promotion_authority": "none",
        "files": rows,
        "archive": {"size_bytes": output.stat().st_size, "sha256": digest_bytes(output.read_bytes())},
        "source_development_workspace_manifest_sha256": claimed,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_output.parent.mkdir(parents=True, exist_ok=True)
    manifest_output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    args = parser.parse_args()
    build(args.output, args.manifest_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
