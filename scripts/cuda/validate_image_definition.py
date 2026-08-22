#!/usr/bin/env python3
"""Validate the pinned CUDA image definition without claiming GPU qualification."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.cuda.qualify import canonical_sha256, file_sha256


def run(command: list[str], cwd: Path) -> str:
    return subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True, timeout=120).stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    root = ROOT
    parser.add_argument("--output", type=Path, default=root / "measurement/cuda/image_definition.json")
    args = parser.parse_args()
    config_path = root / "configs/cuda/qwen3_5_2b_gate0.json"
    dockerfile = root / "containers/cuda/Dockerfile"
    config = json.loads(config_path.read_text())
    inspect = run(["docker", "buildx", "imagetools", "inspect", config["container"]["base_image"]], root)
    expected_list = config["container"]["base_image"].rsplit("@sha256:", 1)[1]
    expected_amd64 = config["container"]["base_image_amd64_manifest_sha256"]
    manifest_ok = f"Digest:    sha256:{expected_list}" in inspect and f"sha256:{expected_amd64}" in inspect
    check = run(["docker", "build", "--check", "--platform", "linux/amd64", "-f", str(dockerfile), "."], root)
    evidence = {
        "schema_version": "ganesh-mini-cuda-image-definition/v1",
        "status": "validated" if manifest_ok and "no warnings found" in check else "failed",
        "scope": "Dockerfile syntax and pinned upstream manifest only; image build and CUDA execution are not claimed",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "host": {"platform": platform.platform(), "machine": platform.machine()},
        "config_sha256": file_sha256(config_path),
        "dockerfile_sha256": file_sha256(dockerfile),
        "base_manifest_list_sha256": expected_list,
        "base_manifest_amd64_sha256": expected_amd64,
        "manifest_resolved": manifest_ok,
        "dockerfile_check_passed": "no warnings found" in check,
        "image_built": False,
        "cuda_qualification_executed": False,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    return 0 if evidence["status"] == "validated" else 2


if __name__ == "__main__":
    raise SystemExit(main())
