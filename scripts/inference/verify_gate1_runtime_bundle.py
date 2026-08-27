#!/usr/bin/env python3
"""Rehearse the Gate 1 VM runtime boundary from the sealed archive itself."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ATTEMPT_ID = "20260825T061157Z"


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


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


def extract_verified(archive: Path, manifest: dict[str, Any], destination: Path) -> None:
    expected = {row["path"]: row for row in manifest["files"]}
    with tarfile.open(archive, "r:gz") as bundle:
        members = bundle.getmembers()
        observed = {member.name for member in members if member.isfile()}
        if observed != set(expected) or any(not member.isfile() for member in members):
            raise ValueError("runtime archive members differ from the sealed manifest")
        for member in members:
            if member.name.startswith("/") or ".." in Path(member.name).parts:
                raise ValueError(f"unsafe runtime archive member: {member.name}")
            source = bundle.extractfile(member)
            if source is None:
                raise ValueError(f"unreadable runtime archive member: {member.name}")
            target = destination / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("wb") as output:
                while chunk := source.read(1024 * 1024):
                    output.write(chunk)
            row = expected[member.name]
            if target.stat().st_size != row.get("size_bytes", row.get("size")) or file_sha256(target) != row["sha256"]:
                raise ValueError(f"extracted runtime file identity mismatch: {member.name}")


def rehearse(root: Path = ROOT) -> dict[str, Any]:
    archive = root / "artifacts/eval/workspaces/development-v2.tar.gz"
    manifest = load_sealed(root / "measurement/gate3/development_workspace_v2.json", "manifest_sha256")
    if archive.stat().st_size != manifest["archive"]["size_bytes"] or file_sha256(archive) != manifest["archive"]["sha256"]:
        raise ValueError("evaluation runtime archive differs from its sealed manifest")

    with (
        tempfile.TemporaryDirectory(prefix="ganesh-gate1-runtime-") as temporary,
        tempfile.TemporaryDirectory(prefix="ganesh-gate1-probe-host-") as probe_temporary,
    ):
        workspace = Path(temporary)
        extract_verified(archive, manifest, workspace)
        probe = r'''from pathlib import Path
from types import SimpleNamespace
from scripts.campaign.run_host import Campaign, CONTAINER_MODEL, docker_container_name, external_mount
from scripts.cuda.qualify import install_fla_recurrent_compatibility, kernel_identity
from scripts.inference.run_development_baseline_host import docker_attempt_id
from scripts.inference.run_evaluation import trim_at_eos
from scripts.verify.sandbox import _docker_argv, infrastructure_failure
attempt = "20260825T061157Z"
probe_host = Path(sys.argv[3])
assert callable(install_fla_recurrent_compatibility) and callable(kernel_identity)
assert not (Path(sys.argv[1]) / "scripts/train").exists()
assert docker_attempt_id(attempt) == "20260825t061157z"
assert trim_at_eos([1, 248046, 248044], 248046) == [1, 248046]
assert infrastructure_failure({"exit_codes":[1],"timed_out":False,"stderr":"fork/exec compile: resource temporarily unavailable"})
verifier_argv = _docker_argv("runtime", "linux/amd64", ["go", "test", "./..."], probe_host, {"pids":64,"cpus":1,"memory_mb":512})
assert "GOMAXPROCS=1" in verifier_argv and "GOFLAGS=-p=1" in verifier_argv and "CARGO_BUILD_JOBS=1" in verifier_argv
names = [
    docker_container_name("ganesh-train-" + attempt + "-lr-1e-5"),
    docker_container_name("ganesh-eval-" + attempt + "-lr-1e-5-canary"),
    docker_container_name("ganesh-train-" + attempt + "-lr-3e-5"),
    docker_container_name("ganesh-eval-" + attempt + "-lr-3e-5-canary"),
    docker_container_name("ganesh-eval-" + attempt + "-lr-1e-5-full"),
]
assert all(name == name.lower() for name in names)
campaign = Campaign(SimpleNamespace(
    output=probe_host/"campaign", max_seconds=12600, attempt_id=attempt,
    hourly_cost_usd=1, model=probe_host/"model",
))
campaign.docker = "/usr/bin/docker"
campaign_base = " ".join(map(str, campaign.docker_base(names[1], probe_host/"train")))
assert "dst=/workspace,readonly" in campaign_base
assert f"dst={CONTAINER_MODEL},readonly" in campaign_base
try:
    external_mount(probe_host/"model", Path("/workspace/models/base"), readonly=True)
except ValueError:
    pass
else:
    raise AssertionError("external mount guard accepted a nested workspace target")
print("\n".join(names))
print("MOUNT_TOPOLOGY_OK")
'''
        environment = {**os.environ, "PYTHONPATH": str(workspace)}
        result = subprocess.run(
            [
                sys.executable,
                "-I",
                "-c",
                "import sys; sys.pycache_prefix=None; sys.dont_write_bytecode=True; "
                "sys.path.insert(0, sys.argv[1]); exec(sys.argv[2])",
                str(workspace),
                probe,
                str(probe_temporary),
            ],
            cwd=workspace, env=environment, capture_output=True, text=True, check=False, timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(f"archived runtime attempt-ID rehearsal failed: {result.stderr.strip()}")
        probe_lines = result.stdout.splitlines()
        mount_topology_ok = probe_lines[-1:] == ["MOUNT_TOPOLOGY_OK"]
        container_names = probe_lines[:-1]
        observed_after_import = {
            str(path.relative_to(workspace))
            for path in workspace.rglob("*")
            if path.is_file()
        }
        expected_files = {row["path"] for row in manifest["files"]}
        if observed_after_import != expected_files:
            raise RuntimeError(
                "archived runtime imports mutated the sealed workspace: "
                f"missing={sorted(expected_files - observed_after_import)[:5]} "
                f"extra={sorted(observed_after_import - expected_files)[:5]}"
            )

    controller = (root / "scripts/inference/gcloud_startup_development_baseline.sh").read_text(encoding="utf-8")
    campaign_source = (root / "scripts/campaign/run_host.py").read_text(encoding="utf-8")
    launcher = (root / "scripts/inference/gcloud_launch_gate1.sh").read_text(encoding="utf-8")
    finalizer = (root / "scripts/inference/gcloud_finalize_gate1.sh").read_text(encoding="utf-8")
    finish = controller[controller.index("finish() {"):controller.index("trap finish EXIT")]
    checks = {
        "archived_attempt_id_is_docker_safe": len(container_names) == 5 and all(name == name.lower() for name in container_names),
        "external_mounts_avoid_read_only_workspace": mount_topology_ok,
        "cuda_serving_compatibility_imports_without_training_package": True,
        "batched_eos_padding_is_trimmed": True,
        "verifier_compiler_jobs_fit_pid_boundary": True,
        "verifier_infrastructure_failures_are_fail_closed": True,
        "archived_imports_preserve_sealed_file_set": observed_after_import == expected_files,
        "controller_disables_workspace_bytecode": 'python3 -B "$work_dir/workspace/scripts/campaign/run_host.py"' in controller,
        "controller_preserves_evidence_attempt_id": '--attempt-id "$GANESH_ATTEMPT_ID"' in controller,
        "controller_binds_canonical_gate1": '--gate1-report "$work_dir/gate1-readiness.json"' in controller,
        "campaign_loads_verifiers_before_training": (
            campaign_source.index("self.prepare_verifier_images()")
            < campaign_source.index("for label, learning_rate in candidates:")
        ),
        "controller_retains_outer_terminal_backup_reserve": '--finalization-reserve-seconds 300' in controller,
        "launcher_uploads_bindings_once": launcher.count("upload_bind bindings ") == 1,
        "provider_stops_before_independent_deletion": "--instance-termination-action=STOP" in launcher,
        "finalizer_preserves_on_terminal_failure": "preserve_finalizer_failure terminal-integrity" in finalizer and "preserve_finalizer_failure deletion-gate" in finalizer,
        "finalizer_uses_gate3_terminal_contract": "ganesh-mini-gate3-gcloud-finalization/v2" in finalizer and "gate3-campaign" in finalizer,
        "runtime_writers_stop_before_inventory": finish.index("stop_runtime_writers") < finish.index("capture_checkpoint_log") < finish.index("write_inventory") < finish.index("final_backup"),
    }
    if not all(checks.values()):
        raise ValueError(f"Gate 1 runtime bundle rehearsal failed: {[key for key, passed in checks.items() if not passed]}")
    evidence: dict[str, Any] = {
        "schema_version": "ganesh-mini-gate3-runtime-bundle-rehearsal/v2",
        "status": "passed",
        "attempt_id": ATTEMPT_ID,
        "workspace_manifest_sha256": manifest["manifest_sha256"],
        "workspace_archive_sha256": manifest["archive"]["sha256"],
        "container_names": container_names,
        "checks": checks,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    evidence = rehearse()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
