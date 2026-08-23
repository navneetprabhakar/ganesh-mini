#!/usr/bin/env python3
"""Build, qualify, and archive the Linux/AMD64 evaluation verifier images."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tarfile
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
PLATFORM = "linux/amd64"
IMAGE_SPECS = {
    "go-1.22.12": ("go", "go", ["go", "version"]),
    "java-21.0.11": ("java", "java", ["java", "-version"]),
    "javascript-node-22.23.2": ("javascript", "javascript", ["node", "--version"]),
    "typescript-5.5.4-node-22": ("typescript", "typescript", ["tsc", "--version"]),
    "python-3.11.15": ("python", "python", ["python3", "--version"]),
    "rust-1.85.0": ("rust", "rust", ["rustc", "--version"]),
}
EXPECTED_PROBE_FRAGMENTS = {
    "go-1.22.12": "go version go1.22.12 linux/amd64",
    "java-21.0.11": 'openjdk version "21.0.11"',
    "javascript-node-22.23.2": "v22.23.2",
    "typescript-5.5.4-node-22": "Version 5.5.4",
    "python-3.11.15": "Python 3.11.15",
    "rust-1.85.0": "rustc 1.85.0",
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def run_checked(argv: list[str], *, timeout: int) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(argv, check=False, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stderr.strip()}")
    return result


def inspect_image(tag: str, runner: Callable[..., subprocess.CompletedProcess[str]] = run_checked) -> dict[str, Any]:
    result = runner(["docker", "image", "inspect", tag], timeout=30)
    rows = json.loads(result.stdout)
    if not isinstance(rows, list) or len(rows) != 1:
        raise RuntimeError(f"unexpected image inspection cardinality for {tag}")
    row = rows[0]
    image_id = row.get("Id")
    if not isinstance(image_id, str) or not image_id.startswith("sha256:") or len(image_id) != 71:
        raise RuntimeError(f"invalid image ID for {tag}")
    if row.get("Os") != "linux" or row.get("Architecture") != "amd64":
        raise RuntimeError(f"{tag} is not Linux/AMD64")
    return {
        "tag": tag,
        "image_id": image_id,
        "os": row["Os"],
        "architecture": row["Architecture"],
        "size_bytes": int(row["Size"]),
        "rootfs_layers": row.get("RootFS", {}).get("Layers", []),
        "labels": row.get("Config", {}).get("Labels") or {},
    }


def runtime_config(images: dict[str, dict[str, Any]]) -> dict[str, Any]:
    commands = {
        "go-1.22.12": [["go", "test", "./..."]],
        "java-21.0.11": [["javac", "Solution.java", "SolutionTest.java"], ["java", "-ea", "SolutionTest"]],
        "javascript-node-22.23.2": [["node", "solution.test.js"]],
        "typescript-5.5.4-node-22": [["tsc", "--strict", "--skipLibCheck", "--module", "commonjs", "--target", "es2022", "solution.ts", "solution.test.ts"], ["node", "solution.test.js"]],
        "python-3.11.15": [["python3", "-I", "-c", "import runpy,sys;sys.path.insert(0,'/work');runpy.run_path('test_solution.py',run_name='__main__')"]],
        "rust-1.85.0": [["rustc", "--edition=2021", "--test", "solution_test.rs", "-o", "ganesh-tests"], ["./ganesh-tests"]],
    }
    candidates = {
        "go-1.22.12": "solution.go", "java-21.0.11": "Solution.java",
        "javascript-node-22.23.2": "solution.js", "typescript-5.5.4-node-22": "solution.ts",
        "python-3.11.15": "solution.py", "rust-1.85.0": "solution.rs",
    }
    return {
        "schema_version": "2.0",
        "platform": PLATFORM,
        "runtimes": {
            runtime_id: {
                "language": IMAGE_SPECS[runtime_id][0],
                "image": images[runtime_id]["tag"],
                "image_id": images[runtime_id]["image_id"],
                "platform": PLATFORM,
                "candidate_path": candidates[runtime_id],
                "commands": commands[runtime_id],
            }
            for runtime_id in IMAGE_SPECS
        },
    }


def verify_saved_archive(archive: Path, images: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Verify that docker-save OCI metadata binds every tag to its exact image ID."""
    with tarfile.open(archive, mode="r") as bundle:
        members = {member.name for member in bundle.getmembers() if member.isfile()}
        manifest_file = bundle.extractfile("manifest.json")
        index_file = bundle.extractfile("index.json")
        if manifest_file is None:
            raise RuntimeError("verifier image archive has no manifest.json")
        if index_file is None:
            raise RuntimeError("verifier image archive has no index.json")
        rows = json.load(manifest_file)
        index = json.load(index_file)
    descriptors = index.get("manifests") if isinstance(index, dict) else None
    if not isinstance(rows, list) or not isinstance(descriptors, list):
        raise RuntimeError("verifier image archive manifest is not a list")
    verified: list[dict[str, str]] = []
    for runtime_id, image in images.items():
        matches = [row for row in rows if image["tag"] in (row.get("RepoTags") or [])]
        if len(matches) != 1:
            raise RuntimeError(f"archive tag cardinality mismatch for {image['tag']}")
        row = matches[0]
        descriptor_matches = [
            item for item in descriptors
            if item.get("digest") == image["image_id"]
            and (item.get("annotations") or {}).get("io.containerd.image.name", "").endswith(image["tag"])
        ]
        if len(descriptor_matches) != 1:
            raise RuntimeError(f"archive OCI descriptor mismatch for {image['tag']}")
        descriptor_path = f"blobs/sha256/{image['image_id'].removeprefix('sha256:')}"
        if descriptor_path not in members:
            raise RuntimeError(f"archive image manifest missing for {image['tag']}")
        expected_config = row.get("Config")
        if not isinstance(expected_config, str) or expected_config not in members:
            raise RuntimeError(f"archive config missing for {image['tag']}")
        layers = row.get("Layers")
        if not isinstance(layers, list) or not layers or any(layer not in members for layer in layers):
            raise RuntimeError(f"archive layers incomplete for {image['tag']}")
        verified.append({
            "runtime_id": runtime_id, "tag": image["tag"], "image_id": image["image_id"],
            "descriptor": descriptor_path, "config": expected_config,
        })
    return {"status": "verified", "image_count": len(verified), "entries": verified}
def prepare(root: Path, output: Path, manifest_path: Path | None = None) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    images: dict[str, dict[str, Any]] = {}
    builds: dict[str, dict[str, Any]] = {}
    for runtime_id, (_, slug, probe) in IMAGE_SPECS.items():
        dockerfile = root / "containers/eval" / f"{slug}.Dockerfile"
        if not dockerfile.is_file():
            raise RuntimeError(f"missing verifier Dockerfile: {dockerfile}")
        tag = f"ganesh-mini-{slug}-verify:amd64-v1"
        argv = [
            "docker", "buildx", "build", "--platform", PLATFORM,
            "--provenance=false", "--load", "--file", str(dockerfile),
            "--tag", tag, str(dockerfile.parent),
        ]
        result = run_checked(argv, timeout=1800)
        image = inspect_image(tag)
        probe_result = run_checked([
            "docker", "run", "--rm", "--pull=never", "--network", "none",
            "--platform", PLATFORM, "--entrypoint", probe[0], tag, *probe[1:],
        ], timeout=120)
        probe_output = "\n".join(part for part in (probe_result.stdout.strip(), probe_result.stderr.strip()) if part)
        if EXPECTED_PROBE_FRAGMENTS[runtime_id] not in probe_output:
            raise RuntimeError(
                f"{runtime_id} probe did not contain {EXPECTED_PROBE_FRAGMENTS[runtime_id]!r}: {probe_output!r}"
            )
        images[runtime_id] = image
        builds[runtime_id] = {
            "dockerfile": str(dockerfile.relative_to(root)),
            "dockerfile_sha256": file_sha256(dockerfile),
            "command": [
                str(dockerfile.relative_to(root)) if item == str(dockerfile)
                else str(dockerfile.parent.relative_to(root)) if item == str(dockerfile.parent)
                else item
                for item in argv
            ],
            "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
            "stderr_sha256": hashlib.sha256(result.stderr.encode()).hexdigest(),
            "probe_command": probe,
            "probe_stdout": probe_result.stdout.strip(),
            "probe_stderr": probe_result.stderr.strip(),
        }
    archive = output / "verifier-images-amd64-v1.tar"
    run_checked(["docker", "image", "save", "--output", str(archive), *[row["tag"] for row in images.values()]], timeout=1800)
    archive_verification = verify_saved_archive(archive, images)
    proposed = runtime_config(images)
    proposed_path = output / "runtimes.amd64-v1.json"
    proposed_path.write_text(json.dumps(proposed, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    adopted_path = root / "configs/eval/runtimes.json"
    if json.loads(adopted_path.read_text(encoding="utf-8")) != proposed:
        raise RuntimeError("adopted runtime config does not match the prepared verifier images")
    manifest: dict[str, Any] = {
        "schema_version": "ganesh-mini-verifier-image-bundle/v1",
        "status": "prepared-adopted",
        "platform": PLATFORM,
        "archive": {
            "path": str(archive.relative_to(root)), "size_bytes": archive.stat().st_size,
            "sha256": file_sha256(archive), "verification": archive_verification,
        },
        "proposed_runtime_config": {"path": str(proposed_path.relative_to(root)), "sha256": file_sha256(proposed_path)},
        "adopted_runtime_config": {
            "path": str(adopted_path.relative_to(root)), "sha256": file_sha256(adopted_path),
        },
        "images": images,
        "builds": builds,
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    manifest_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    (output / "manifest.json").write_text(manifest_text, encoding="utf-8")
    if manifest_path is not None:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(manifest_text, encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    manifest = prepare(
        args.root.resolve(), args.output.resolve(),
        args.manifest.resolve() if args.manifest else None,
    )
    print(json.dumps({"status": manifest["status"], "archive_sha256": manifest["archive"]["sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
