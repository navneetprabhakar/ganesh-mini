#!/usr/bin/env python3
"""Fail closed unless every runtime image has the frozen ID and platform."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def inspect(tag: str) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            ["docker", "image", "inspect", tag, "--format", "{{json .}}"],
            check=False, capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return 127, "", str(error)
    return result.returncode, result.stdout, result.stderr


def audit(config_path: Path, inspector: Callable[[str], tuple[int, str, str]] = inspect) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    rows: list[dict[str, Any]] = []
    if set(config) != {"schema_version", "platform", "runtimes"} or config.get("schema_version") != "2.0":
        raise ValueError("runtime image readiness requires schema 2.0")
    if config.get("platform") != "linux/amd64":
        raise ValueError("runtime image readiness requires linux/amd64")
    for runtime_id, runtime in sorted(config["runtimes"].items()):
        code, stdout, stderr = inspector(runtime["image"])
        observed: dict[str, Any] = {}
        if code == 0:
            try:
                observed = json.loads(stdout)
            except json.JSONDecodeError:
                failures.append(f"{runtime_id}: malformed Docker inspection")
        else:
            failures.append(f"{runtime_id}: image unavailable: {stderr.strip()}")
        expected_id = runtime["image_id"]
        observed_id = observed.get("Id")
        observed_platform = f"{observed.get('Os')}/{observed.get('Architecture')}" if observed else None
        if observed and observed_id != expected_id:
            failures.append(f"{runtime_id}: image ID mismatch")
        if observed and observed_platform != runtime["platform"]:
            failures.append(f"{runtime_id}: platform mismatch")
        rows.append({
            "runtime_id": runtime_id, "tag": runtime["image"], "expected_image_id": expected_id,
            "observed_image_id": observed_id, "expected_platform": runtime["platform"],
            "observed_platform": observed_platform, "ready": bool(observed_id == expected_id and observed_platform == runtime["platform"]),
        })
    value: dict[str, Any] = {
        "schema_version": "ganesh-mini-runtime-image-readiness/v1",
        "status": "ready" if not failures else "blocked",
        "runtime_config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
        "expected": len(config["runtimes"]),
        "ready": sum(row["ready"] for row in rows),
        "failures": failures,
        "images": rows,
    }
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/eval/runtimes.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    value = audit(args.config.resolve())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": value["status"], "ready": value["ready"], "expected": value["expected"]}, sort_keys=True))
    return 0 if value["status"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
