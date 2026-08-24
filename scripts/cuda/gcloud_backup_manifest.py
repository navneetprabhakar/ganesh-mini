#!/usr/bin/env python3
"""Independently download and hash every object in a run-scoped GCS prefix."""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def run(*args: str) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def download(project: str, uri: str, destination: Path) -> None:
    subprocess.run(["gcloud", "storage", "cp", uri, str(destination), f"--project={project}"], check=True)


def generation_uri(metadata: dict[str, object]) -> str:
    return f"gs://{metadata['bucket']}/{metadata['name']}#{metadata['generation']}"


def stream_sha256(project: str, uri: str) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    process = subprocess.Popen(
        ["gcloud", "storage", "cat", uri, f"--project={project}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None
    for chunk in iter(lambda: process.stdout.read(1024 * 1024), b""):
        digest.update(chunk)
        size += len(chunk)
    stderr = process.stderr.read().decode(errors="replace") if process.stderr is not None else ""
    if process.wait() != 0:
        raise subprocess.CalledProcessError(process.returncode, process.args, stderr=stderr)
    return digest.hexdigest(), size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--prefix", required=True, help="gs:// bucket prefix without wildcard")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--download-dir", type=Path, required=True)
    parser.add_argument(
        "--stream",
        action="store_true",
        help="hash each object through two independent streams instead of storing downloads",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="maximum concurrent immutable-object verifications (default: 8)",
    )
    parser.add_argument("--map", action="append", default=[], metavar="REMOTE_SUBPREFIX=LOCAL_ROOT")
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 32:
        parser.error("--workers must be between 1 and 32")
    mappings = []
    for value in args.map:
        remote, local = value.split("=", 1)
        mappings.append((remote.strip("/"), Path(local).resolve()))
    listing = json.loads(run("gcloud", "storage", "ls", "--json", f"{args.prefix}/**", f"--project={args.project}"))
    if not listing:
        raise SystemExit("refusing to seal an empty GCS prefix")
    if not args.stream:
        args.download_dir.mkdir(parents=True, exist_ok=True)
    items = sorted(listing, key=lambda value: value["metadata"]["name"])
    prefix_path = args.prefix.split("/", 3)[3].rstrip("/")
    with tempfile.TemporaryDirectory(prefix="ganesh-gcs-verify-") as second_root:
        def verify(item: dict[str, object]) -> dict[str, object]:
            metadata = item["metadata"]
            relative = metadata["name"].removeprefix(prefix_path + "/")
            immutable_uri = generation_uri(metadata)
            if args.stream:
                downloaded_hash, downloaded_size = stream_sha256(args.project, immutable_uri)
                verified_hash, verified_size = stream_sha256(args.project, immutable_uri)
                local_path = None
                for remote, root in mappings:
                    if relative == remote or relative.startswith(remote + "/"):
                        local_path = root if relative == remote and root.is_file() else root / relative.removeprefix(remote).lstrip("/")
                        break
                if local_path is not None:
                    if not local_path.is_file():
                        raise SystemExit(f"mapped local source missing: {local_path}")
                    local_hash = sha256(local_path)
                else:
                    local_hash = downloaded_hash
                size = int(metadata["size"])
                local_size = local_path.stat().st_size if local_path is not None else size
                passed = (
                    local_hash == downloaded_hash == verified_hash
                    and local_size == downloaded_size == verified_size == size
                )
                if not passed:
                    raise SystemExit(f"backup verification failed for {immutable_uri}")
                return {
                    "object_uri": "gs://" + metadata["bucket"] + "/" + metadata["name"],
                    "generation": metadata["generation"], "size": size,
                    "local_sha256": local_hash, "downloaded_sha256": downloaded_hash,
                    "verified_download_sha256": verified_hash, "verified": True,
                }
            first = args.download_dir / relative
            first.parent.mkdir(parents=True, exist_ok=True)
            download(args.project, immutable_uri, first)
            downloaded_hash = sha256(first)
            local_path = None
            for remote, root in mappings:
                if relative == remote or relative.startswith(remote + "/"):
                    local_path = root if relative == remote and root.is_file() else root / relative.removeprefix(remote).lstrip("/")
                    break
            if local_path is not None:
                if not local_path.is_file():
                    raise SystemExit(f"mapped local source missing: {local_path}")
                local_hash = sha256(local_path)
                verified_hash = downloaded_hash
            else:
                second = Path(second_root) / relative
                second.parent.mkdir(parents=True, exist_ok=True)
                download(args.project, immutable_uri, second)
                local_hash = downloaded_hash
                verified_hash = sha256(second)
            size = first.stat().st_size
            passed = local_hash == downloaded_hash == verified_hash and size == int(metadata["size"])
            if not passed:
                raise SystemExit(f"backup verification failed for {immutable_uri}")
            return {
                "object_uri": "gs://" + metadata["bucket"] + "/" + metadata["name"],
                "generation": metadata["generation"], "size": size,
                "local_sha256": local_hash, "downloaded_sha256": downloaded_hash,
                "verified_download_sha256": verified_hash, "verified": True,
            }

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            entries = list(executor.map(verify, items))
    evidence = {
        "schema_version": "ganesh-mini-gcs-backup-manifest/v1", "status": "verified",
        "project": args.project, "prefix": args.prefix, "object_count": len(entries), "objects": entries,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
