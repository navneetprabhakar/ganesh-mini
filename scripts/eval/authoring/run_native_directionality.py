#!/usr/bin/env python3
"""Run every frozen verifier directionality check on native Linux/AMD64."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from scripts.eval.contracts import load_json, sha256_object, write_json
from scripts.eval.prepare_verifier_images import EXPECTED_PROBE_FRAGMENTS, IMAGE_SPECS
from scripts.eval.verify_runtime_images import audit as audit_images


ROOT = Path(__file__).resolve().parents[3]
RUNTIME_CONFIG = ROOT / "configs/eval/runtimes.json"
READINESS = ROOT / "measurement/gate1/native_amd64_runtime_readiness.json"
GLOBAL_REPORT = ROOT / "manifests/evaluation/private/decision-global-separation.json"
LOG_ROOT = ROOT / "measurement/gate1/native-directionality-logs"
JOBS = (
    ("development-tranche1", "scripts/eval/authoring/run_tranche1_directionality.py", ["--workers", "2"], "manifests/evaluation/private/development-tranche1-directionality.json"),
    ("development-tranche2", "scripts/eval/authoring/run_tranche2_directionality.py", [], "manifests/evaluation/private/development-tranche2-directionality.json"),
    ("development-tranche3", "scripts/eval/authoring/run_tranche3_directionality.py", [], "manifests/evaluation/private/development-tranche3-directionality.json"),
    ("development-tranche4", "scripts/eval/authoring/run_tranche4_directionality.py", [], "manifests/evaluation/private/development-tranche4-directionality.json"),
    ("development-tranche5", "scripts/eval/authoring/run_tranche5_directionality.py", [], "manifests/evaluation/private/development-tranche5-directionality.json"),
    ("development-tranche6", "scripts/eval/authoring/run_tranche6_directionality.py", [], "manifests/evaluation/private/development-tranche6-directionality.json"),
    ("decision-tranche1", "scripts/eval/authoring/run_decision_tranche1_directionality.py", [], "manifests/evaluation/private/decision-tranche1-directionality.json"),
    ("decision-tranche2", "scripts/eval/authoring/run_decision_tranche2_directionality.py", [], "manifests/evaluation/private/decision-tranche2-directionality.json"),
    ("decision-tranche3", "scripts/eval/authoring/run_decision_tranche3_directionality.py", [], "manifests/evaluation/private/decision-tranche3-directionality.json"),
    ("decision-tranche4", "scripts/eval/authoring/run_decision_tranche4_directionality.py", [], "manifests/evaluation/private/decision-tranche4-directionality.json"),
    ("decision-tranche5", "scripts/eval/authoring/run_decision_tranche5_directionality.py", [], "manifests/evaluation/private/decision-tranche5-directionality.json"),
    ("decision-tranche6", "scripts/eval/authoring/run_decision_tranche6_directionality.py", [], "manifests/evaluation/private/decision-tranche6-directionality.json"),
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(argv: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ, PYTHONPATH=str(ROOT))
    result = subprocess.run(
        argv, cwd=ROOT, check=False, capture_output=True, text=True,
        timeout=timeout, env=environment,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stderr.strip()}")
    return result


def native_host() -> dict[str, Any]:
    if platform.system() != "Linux" or platform.machine() not in {"x86_64", "amd64"}:
        raise RuntimeError("directionality qualification requires native Linux/AMD64")
    server = json.loads(checked(["docker", "version", "--format", "{{json .Server}}"], 30).stdout)
    info = json.loads(checked([
        "docker", "info", "--format",
        "{{json (dict \"OSType\" .OSType \"Architecture\" .Architecture \"Driver\" .Driver \"DockerRootDir\" .DockerRootDir)}}",
    ], 30).stdout)
    if server.get("Os") != "linux" or server.get("Arch") != "amd64":
        raise RuntimeError("Docker server is not native Linux/AMD64")
    return {
        "system": platform.system(), "machine": platform.machine(),
        "kernel": platform.release(), "docker_server": server, "docker_info": info,
    }


def probe_images(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for runtime_id, (_, _slug, probe) in IMAGE_SPECS.items():
        runtime = config["runtimes"][runtime_id]
        result = checked([
            "docker", "run", "--rm", "--pull", "never", "--network", "none",
            "--platform", "linux/amd64", "--entrypoint", probe[0], runtime["image"], *probe[1:],
        ])
        output = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part)
        expected = EXPECTED_PROBE_FRAGMENTS[runtime_id]
        if expected not in output:
            raise RuntimeError(f"toolchain probe mismatch for {runtime_id}: {output!r}")
        rows.append({
            "runtime_id": runtime_id, "image": runtime["image"],
            "manifest_digest": runtime["manifest_digest"], "image_id": runtime["image_id"],
            "probe": probe, "expected_fragment": expected,
            "stdout": result.stdout.strip(), "stderr": result.stderr.strip(),
        })
    return rows


def run_job(job: tuple[str, str, list[str], str]) -> dict[str, Any]:
    name, script, arguments, output = job
    started = time.monotonic()
    result = subprocess.run(
        [sys.executable, script, *arguments], cwd=ROOT, check=False,
        capture_output=True, text=True, timeout=7200,
        env=dict(os.environ, PYTHONPATH=str(ROOT)),
    )
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    stdout_path = LOG_ROOT / f"{name}.stdout.log"
    stderr_path = LOG_ROOT / f"{name}.stderr.log"
    stdout_path.write_text(result.stdout, encoding="utf-8")
    stderr_path.write_text(result.stderr, encoding="utf-8")
    output_path = ROOT / output
    row: dict[str, Any] = {
        "name": name, "script": script, "arguments": arguments, "returncode": result.returncode,
        "duration_ms": round((time.monotonic() - started) * 1000),
        "stdout": {"path": str(stdout_path.relative_to(ROOT)), "sha256": file_sha256(stdout_path)},
        "stderr": {"path": str(stderr_path.relative_to(ROOT)), "sha256": file_sha256(stderr_path)},
        "output": str(output_path.relative_to(ROOT)),
    }
    if result.returncode == 0 and output_path.is_file():
        evidence = load_json(output_path)
        claimed = evidence.get("evidence_sha256")
        row.update({
            "output_sha256": file_sha256(output_path), "evidence_sha256": claimed,
            "evidence_seal_valid": claimed == sha256_object({key: value for key, value in evidence.items() if key != "evidence_sha256"}),
            "status": evidence.get("status"),
        })
    else:
        row.update({"evidence_seal_valid": False, "status": "failed"})
    return row


def run(output: Path, workers: int) -> dict[str, Any]:
    host = native_host()
    config = load_json(RUNTIME_CONFIG)
    readiness = audit_images(RUNTIME_CONFIG)
    write_json(READINESS, readiness)
    if readiness["status"] != "ready":
        raise RuntimeError(f"runtime images are not ready: {readiness['failures']}")
    probes = probe_images(config)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        jobs = list(executor.map(run_job, JOBS))
    failures = [row["name"] for row in jobs if row["status"] != "passed" or not row["evidence_seal_valid"]]
    if not failures:
        checked([sys.executable, "scripts/eval/authoring/audit_global_decision_separation.py"], 600)
    global_report = load_json(GLOBAL_REPORT) if GLOBAL_REPORT.is_file() and not failures else None
    if global_report is not None:
        claimed = global_report.get("report_sha256")
        if claimed != sha256_object({key: value for key, value in global_report.items() if key != "report_sha256"}):
            failures.append("global-decision-separation-seal")
        elif global_report.get("status") != "passed":
            failures.append("global-decision-separation-status")
    evidence: dict[str, Any] = {
        "schema_version": "ganesh-mini-native-amd64-directionality/v1",
        "status": "passed" if not failures else "failed",
        "source_commit": checked(["git", "rev-parse", "HEAD"], 30).stdout.strip(),
        "host": host,
        "runtime_config": {"path": str(RUNTIME_CONFIG.relative_to(ROOT)), "sha256": file_sha256(RUNTIME_CONFIG)},
        "runtime_readiness": {"path": str(READINESS.relative_to(ROOT)), "evidence_sha256": readiness["evidence_sha256"]},
        "toolchain_probes": probes, "workers": workers, "jobs": jobs, "failures": failures,
        "global_decision_separation": None if global_report is None else {
            "path": str(GLOBAL_REPORT.relative_to(ROOT)), "report_sha256": global_report["report_sha256"],
        },
    }
    evidence["evidence_sha256"] = sha256_object(evidence)
    write_json(output, evidence)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "measurement/gate1/native_amd64_directionality.json")
    parser.add_argument("--workers", type=int, default=min(2, max(1, (os.cpu_count() or 2) // 2)))
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 4:
        raise ValueError("workers must be between 1 and 4")
    evidence = run(args.output.resolve(), args.workers)
    print(json.dumps({"status": evidence["status"], "evidence_sha256": evidence["evidence_sha256"]}, sort_keys=True))
    return 0 if evidence["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
