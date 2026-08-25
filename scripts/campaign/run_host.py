#!/usr/bin/env python3
"""Run the approved Gate 1 through Gate 3 campaign on one Linux/L4 host.

The host is an evidence orchestrator. Model processes run in separate offline
containers: evaluation containers can see development tasks but not training
data; training containers can see seed data and sealed gate reports but not
evaluation tasks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from decimal import Decimal
from pathlib import Path
from typing import Any

# The evaluation and training roots are sealed, read-only logical inputs even
# while they are mounted from writable host directories.  Linux otherwise
# creates in-tree __pycache__ files when campaign phases import workspace
# modules, which mutates the file set before the downstream identity check.
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
MODEL_RELATIVE = Path("models/qwen3.5-2b-15852e8")
BASE_OUTPUT_RELATIVE = Path("measurement/inference/development/qwen3.5-2b-base-v1")
CONTAINER_MODEL = Path("/input/model")
CONTAINER_TRAINING = Path("/training")
CONTAINER_ADAPTER = CONTAINER_TRAINING / "adapter-final"
CONTAINER_OUTPUT = Path("/output")
CONTAINER_CONTROL = Path("/control")
CUDA_IMAGE_ID = "sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860"
LR_CANDIDATES = (("lr-1e-4", 0.0001), ("lr-2e-4", 0.0002))


def docker_container_name(name: str) -> str:
    """Return a Docker-safe name without changing the canonical campaign ID."""
    normalized = name.lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9_.-]*", normalized):
        raise ValueError(f"invalid Docker container name: {name}")
    return normalized


def external_mount(source: Path, destination: Path, *, readonly: bool = False) -> str:
    """Build a bind whose target cannot depend on a read-only workspace path."""
    if not destination.is_absolute():
        raise ValueError("container mount destination must be absolute")
    if destination == Path("/workspace") or destination.is_relative_to(Path("/workspace")):
        raise ValueError("external state cannot be mounted beneath /workspace")
    suffix = ",readonly" if readonly else ""
    return f"type=bind,src={source.resolve()},dst={destination}{suffix}"


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def load_sealed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop(field, None)
    if claimed != canonical_sha256(value):
        raise ValueError(f"invalid {field}: {path}")
    value[field] = claimed
    return value


def verify_workspace(root: Path, manifest_path: Path, archive_path: Path, schema: str) -> dict[str, Any]:
    manifest = load_sealed(manifest_path, "manifest_sha256")
    if manifest.get("schema_version") != schema or manifest.get("status") != "sealed":
        raise ValueError(f"workspace contract mismatch: {manifest_path}")
    archive = manifest.get("archive", {})
    expected_size = archive.get("size_bytes", manifest.get("archive_size"))
    expected_sha = archive.get("sha256", manifest.get("archive_sha256"))
    if archive_path.stat().st_size != expected_size or file_sha256(archive_path) != expected_sha:
        raise ValueError(f"workspace archive identity mismatch: {archive_path}")
    expected = {row["path"]: (row.get("size_bytes", row.get("size")), row["sha256"]) for row in manifest["files"]}
    observed = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
    if observed != set(expected):
        raise ValueError(f"workspace file set mismatch: missing={sorted(set(expected)-observed)[:5]} extra={sorted(observed-set(expected))[:5]}")
    for relative, (size, digest) in expected.items():
        path = root / relative
        if path.stat().st_size != size or file_sha256(path) != digest:
            raise ValueError(f"workspace file identity mismatch: {relative}")
    return manifest


class Campaign:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.started = time.monotonic()
        self.output = args.output.resolve()
        self.output.mkdir(parents=True, exist_ok=True)
        self.ledger_path = self.output / "phase-ledger.json"
        self.phases: list[dict[str, Any]] = []
        self.docker = shutil.which("docker") or ""

    def remaining(self, reserve: int = 0) -> int:
        remaining = self.args.max_seconds - int(time.monotonic() - self.started) - reserve
        if remaining < 600:
            raise RuntimeError("campaign has insufficient bounded time remaining")
        return remaining

    def prior_cost(self) -> Decimal:
        return self.args.hourly_cost_usd * Decimal(str(time.monotonic() - self.started)) / Decimal(3600)

    def record(self, name: str, status: str, **evidence: Any) -> None:
        row = {"name": name, "status": status, "elapsed_seconds": round(time.monotonic() - self.started, 3), "evidence": evidence}
        self.phases.append(row)
        ledger = {"schema_version": "ganesh-mini-staged-campaign-ledger/v1", "attempt_id": self.args.attempt_id, "status": "running" if status == "passed" else status, "phases": self.phases}
        ledger["evidence_sha256"] = canonical_sha256(ledger)
        atomic_json(self.ledger_path, ledger)

    def run(self, command: list[str], *, log_name: str, timeout: int, env: dict[str, str] | None = None) -> None:
        stdout = self.output / f"{log_name}.stdout.log"
        stderr = self.output / f"{log_name}.stderr.log"
        try:
            with stdout.open("ab") as out, stderr.open("ab") as err:
                result = subprocess.run(command, stdout=out, stderr=err, timeout=timeout, env=env, check=False)
        except subprocess.TimeoutExpired:
            if self.docker:
                listed=subprocess.run([self.docker,"ps","-aq","--filter",f"label=ganesh.campaign={self.args.attempt_id}"],capture_output=True,text=True,check=False,timeout=30)
                ids=[row for row in listed.stdout.splitlines() if row]
                if ids: subprocess.run([self.docker,"rm","-f",*ids],capture_output=True,check=False,timeout=60)
            raise
        if result.returncode != 0:
            raise RuntimeError(f"{log_name} exited {result.returncode}")

    def docker_base(self, name: str, workspace: Path) -> list[str]:
        container_name = docker_container_name(name)
        return [
            self.docker, "run", "--pull=never", "--rm", "--name", container_name,
            "--label", f"ganesh.campaign={self.args.attempt_id}",
            "--gpus", "device=0", "--network", "none", "--cpus", "12", "--memory", "46g",
            "--pids-limit", "4096", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=8g",
            "--tmpfs", "/var/cache/triton:rw,exec,nosuid,nodev,size=1g",
            "--mount", f"type=bind,src={workspace},dst=/workspace,readonly",
            "--mount", external_mount(self.args.model, CONTAINER_MODEL, readonly=True),
            "--env", "HF_HUB_OFFLINE=1", "--env", "TRANSFORMERS_OFFLINE=1",
            "--env", "PYTHONPATH=/workspace", "--env", "TRITON_CACHE_DIR=/var/cache/triton",
            "--workdir", "/workspace",
        ]

    def baseline(self) -> None:
        from scripts.inference.run_development_baseline_host import execute
        namespace = argparse.Namespace(
            workspace=self.args.eval_workspace, workspace_manifest=self.args.eval_manifest,
            workspace_archive=self.args.eval_archive, model=self.args.model,
            verifier_bundle=self.args.verifier_manifest, verifier_archive=self.args.verifier_archive,
            output=self.output / "baseline", shared_tmp=self.args.shared_tmp,
            docker_socket=Path("/var/run/docker.sock"), cuda_image=self.args.cuda_image,
            cuda_image_id=self.args.cuda_image_id, attempt_id=self.args.attempt_id,
            max_seconds=min(self.remaining(self.args.finalization_reserve_seconds), 21600),
        )
        evidence = execute(namespace)
        self.record("gate1-base-baseline", "passed", host_execution_sha256=evidence["evidence_sha256"], run_sha256=evidence["run"]["run_sha256"])

    def build_gate1(self) -> Path:
        baseline_target = self.args.eval_workspace / BASE_OUTPUT_RELATIVE
        baseline_target.parent.mkdir(parents=True, exist_ok=True)
        if baseline_target.exists():
            raise RuntimeError("evaluation workspace baseline target is not fresh")
        shutil.copytree(self.output / "baseline", baseline_target)
        report = self.output / "gate1-readiness.json"
        env = {**os.environ, "PYTHONPATH": str(self.args.eval_workspace)}
        self.run([
            sys.executable, str(self.args.eval_workspace / "scripts/eval/build_gate1_readiness.py"),
            "--root", str(self.args.eval_workspace), "--baseline", str(baseline_target / "run.json"),
            "--training-workspace-manifest", str(self.args.train_manifest),
            "--output", str(report),
        ], log_name="gate1-readiness", timeout=min(self.remaining(), 600), env=env)
        gate1 = load_sealed(report, "evidence_sha256")
        if gate1.get("status") != "ready":
            raise RuntimeError(f"Gate 1 did not open: {gate1.get('failed_checks')}")
        self.record("gate1-admission", "passed", evidence_sha256=gate1["evidence_sha256"])
        return report

    def training_card(self, gate1: Path) -> Path:
        for source, relative in (
            (self.args.gate0_report, "measurement/gate0/readiness.json"),
            (gate1, "measurement/gate1/readiness.json"),
            (self.args.gate2_report, "measurement/gate2/readiness.json"),
        ):
            target = self.args.train_workspace / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        card = self.output / "training-execution-card.json"
        env = {**os.environ, "PYTHONPATH": str(self.args.train_workspace)}
        self.run([
            sys.executable, str(self.args.train_workspace / "scripts/train/pilot.py"), "preflight",
            "--root", str(self.args.train_workspace),
            "--config", str(self.args.train_workspace / "configs/train/seed_pilot.json"),
            "--system", "Linux", "--output", str(card),
        ], log_name="training-preflight", timeout=min(self.remaining(), 600), env=env)
        value = load_sealed(card, "card_sha256")
        if value.get("status") != "ready":
            raise RuntimeError(f"training card is not ready: {value.get('failed_checks')}")
        self.record("gate3-training-admission", "passed", card_sha256=value["card_sha256"])
        return card

    def train(self, label: str, learning_rate: float, maximum_tokens: int, card: Path, selection: Path | None = None) -> Path:
        destination = self.output / "training" / label
        destination.mkdir(parents=True, exist_ok=False)
        phase = "main" if label == "main" else "lr-candidate"
        command = self.docker_base(f"ganesh-train-{self.args.attempt_id}-{label}", self.args.train_workspace)
        command += [
            "--mount", external_mount(destination, Path("/outputs")),
            "--mount", external_mount(self.output, CONTAINER_CONTROL, readonly=True),
        ]
        command += ["--entrypoint", "python", self.args.cuda_image,
            "/workspace/scripts/train/run_sft.py", "--phase", phase,
            "--card", str(CONTAINER_CONTROL / card.name), "--model-dir", str(CONTAINER_MODEL),
            "--output", "/outputs", "--learning-rate", str(learning_rate),
            "--maximum-seen-tokens", str(maximum_tokens), "--hourly-cost-usd", str(self.args.hourly_cost_usd),
            "--prior-cost-usd", str(self.prior_cost()), "--cost-ceiling-usd", str(self.args.training_cost_ceiling_usd),
        ]
        if selection:
            command += ["--lr-selection-evidence", str(CONTAINER_CONTROL / selection.name)]
        self.run(command, log_name=f"train-{label}", timeout=min(self.remaining(self.args.finalization_reserve_seconds), 21600))
        evidence = load_sealed(destination / "run-evidence.json", "evidence_sha256")
        if evidence.get("status") != "complete":
            raise RuntimeError(f"{label} training did not complete")
        self.record(f"train-{label}", "passed", evidence_sha256=evidence["evidence_sha256"], seen_tokens=evidence["state"]["seen_tokens"])
        return destination

    def candidate_config(self, label: str, training: Path) -> Path:
        base = json.loads((self.args.eval_workspace / "configs/inference/qwen_base_development.json").read_text())
        base.update({
            "run_id": f"ganesh-mini-1.0-{label}-development-v1",
            "classification": "private_candidate_development",
            "output_dir": f"measurement/inference/development/{label}",
            "adapter": {"dir": f"artifacts/campaign/{label}/adapter-final", "run_evidence": f"artifacts/campaign/{label}/run-evidence.json", "served_model_id": f"ganesh-mini-1.0-{label}"},
        })
        path = self.output / "configs" / f"{label}.json"
        atomic_json(path, base)
        return path

    def evaluate(self, label: str, training: Path) -> Path:
        destination = self.output / "evaluation" / label
        destination.mkdir(parents=True, exist_ok=False)
        config = self.candidate_config(label, training)
        command = self.docker_base(f"ganesh-eval-{self.args.attempt_id}-{label}", self.args.eval_workspace)
        command += [
            "--mount", external_mount(training, CONTAINER_TRAINING, readonly=True),
            "--mount", external_mount(destination, CONTAINER_OUTPUT),
            "--mount", external_mount(self.output, CONTAINER_CONTROL, readonly=True),
            "--mount", external_mount(self.args.shared_tmp, self.args.shared_tmp.resolve()),
            "--mount", "type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock",
            "--mount", f"type=bind,src={self.docker},dst=/usr/local/bin/docker,readonly",
            "--env", f"TMPDIR={self.args.shared_tmp.resolve()}",
            "--entrypoint", "python", self.args.cuda_image,
            "/workspace/scripts/inference/run_evaluation.py", "--config", str(CONTAINER_CONTROL / "configs" / config.name),
            "--model-dir", str(CONTAINER_MODEL), "--adapter-dir", str(CONTAINER_ADAPTER),
            "--output-dir", str(CONTAINER_OUTPUT),
        ]
        self.run(command, log_name=f"evaluate-{label}", timeout=min(self.remaining(self.args.finalization_reserve_seconds), 21600))
        run = load_sealed(destination / "run.json", "run_sha256")
        accounting = run.get("task_accounting", {})
        if accounting.get("completed") != 180 or accounting.get("pending") != 0:
            raise RuntimeError(f"{label} evaluation is incomplete")
        self.record(f"evaluate-{label}", "passed", run_sha256=run["run_sha256"], passed=accounting["passed"])
        return destination

    def select_lr(self, runs: dict[str, Path], evaluations: dict[str, Path]) -> Path:
        output = self.output / "lr-selection.json"
        if str(self.args.eval_workspace) not in sys.path:
            sys.path.insert(0,str(self.args.eval_workspace))
        from scripts.eval.score import load_results
        low=load_results(evaluations["lr-1e-4"] / "tasks"); high=load_results(evaluations["lr-2e-4"] / "tasks")
        low_run=load_sealed(runs["lr-1e-4"] / "run-evidence.json","evidence_sha256"); high_run=load_sealed(runs["lr-2e-4"] / "run-evidence.json","evidence_sha256")
        for run,expected in ((low_run,"0.0001"),(high_run,"0.0002")):
            if run.get("status")!="complete" or run.get("identities",{}).get("phase")!="lr-candidate" or run.get("identities",{}).get("learning_rate")!=expected or run.get("state",{}).get("seen_tokens",0)<400000: raise RuntimeError("LR selection requires two complete 400k-token candidates")
        if len(low)!=180 or {row["task_id"] for row in low}!={row["task_id"] for row in high}: raise RuntimeError("LR candidates do not cover the same 180 tasks")
        lanes=("go","java","javascript","typescript","python","rust")
        low_lane={lane:sum(row["passed"] for row in low if row["language"]==lane) for lane in lanes}; high_lane={lane:sum(row["passed"] for row in high if row["language"]==lane) for lane in lanes}
        choose_high=sum(high_lane.values())>=sum(low_lane.values())+1 and all(high_lane[lane]>=low_lane[lane] for lane in lanes)
        collection=lambda rows:canonical_sha256([row["result_sha256"] for row in sorted(rows,key=lambda item:item["task_id"])])
        selected={"schema_version":"ganesh-mini-lr-selection/v1","status":"selected","rule":"select_0.0002_only_if_development_macro_improves_by_at_least_one_task_equivalent_with_no_lane_regression_else_0.0001","candidates":{"0.0001":{"run_evidence_sha256":low_run["evidence_sha256"],"result_collection_sha256":collection(low),"passed":sum(low_lane.values()),"lanes":low_lane},"0.0002":{"run_evidence_sha256":high_run["evidence_sha256"],"result_collection_sha256":collection(high),"passed":sum(high_lane.values()),"lanes":high_lane}},"selected_learning_rate":0.0002 if choose_high else 0.0001,"decision":"higher_lr_improved_without_lane_regression" if choose_high else "conservative_lower_lr_default"}
        selected["evidence_sha256"]=canonical_sha256(selected); atomic_json(output,selected)
        self.record("lr-selection", "passed", evidence_sha256=selected["evidence_sha256"], selected_learning_rate=selected["selected_learning_rate"])
        return output

    def adjudicate(self, main_run: Path, main_eval: Path) -> None:
        comparison = self.output / "main-vs-base.json"
        promotion = self.output / "pilot-promotion.json"
        if str(self.args.eval_workspace) not in sys.path: sys.path.insert(0,str(self.args.eval_workspace))
        from scripts.eval.score import compare,load_results
        base=load_results(self.output/"baseline/tasks"); candidate=load_results(main_eval/"tasks"); scored=compare(base,candidate); atomic_json(comparison,scored)
        families=("go","java","javascript_typescript","python","rust"); lanes=("go","java","javascript","typescript","python","rust")
        improved=[family for family in families if scored["candidate"]["families"][family]["decimal"]>scored["base"]["families"][family]["decimal"]]
        lane_deltas={lane:scored["candidate"]["lanes"][lane]["passed"]-scored["base"]["lanes"][lane]["passed"] for lane in lanes}
        base_quality=scored["base"]["quality_failures"]; candidate_quality=scored["candidate"]["quality_failures"]
        retention=load_sealed(self.args.eval_workspace/"manifests/evaluation/private/retention-slice.json","manifest_sha256"); ids={row["task_id"] for row in retention["tasks"]}; base_by={row["task_id"]:row for row in base}; candidate_by={row["task_id"]:row for row in candidate}
        if not ids<=set(base_by) or not ids<=set(candidate_by): raise RuntimeError("retention slice absent from development results")
        wins=sum(candidate_by[item]["passed"] and not base_by[item]["passed"] for item in ids); losses=sum(base_by[item]["passed"] and not candidate_by[item]["passed"] for item in ids); sft=load_sealed(main_run/"run-evidence.json","evidence_sha256")
        checks=[{"name":"four_of_five_families_improve","passed":len(improved)>=4,"evidence":{"improved":improved}},{"name":"no_lane_regression","passed":all(delta>=0 for delta in lane_deltas.values()),"evidence":{"lane_deltas":lane_deltas}},{"name":"quality_failures_do_not_increase","passed":all(candidate_quality[key]<=base_quality[key] for key in base_quality),"evidence":{"base":base_quality,"candidate":candidate_quality}},{"name":"retention_slice","passed":losses<=1 and wins-losses>=-1,"evidence":{"wins":wins,"losses":losses,"tasks":len(ids)}},{"name":"sft_complete_and_reload_reproduced","passed":sft.get("status")=="complete" and sft.get("save_reload",{}).get("passed") is True,"evidence":{"run_evidence_sha256":sft.get("evidence_sha256")}}]
        passed=all(row["passed"] for row in checks); result={"schema_version":"ganesh-mini-pilot-promotion/v1","status":"promote" if passed else "reject","checks":checks,"failed_checks":[row["name"] for row in checks if not row["passed"]],"decision":"promote_directly_or_admit_one_frozen_pass_a_expansion" if passed else "change_data_or_mechanism_before_scaling"}; result["evidence_sha256"]=canonical_sha256(result); atomic_json(promotion,result)
        self.record("gate3-promotion", "passed" if result.get("status") == "promote" else "rejected", evidence_sha256=result["evidence_sha256"], failed_checks=result.get("failed_checks"))
        if result.get("status") != "promote":
            raise RuntimeError(f"pilot rejected: {result.get('failed_checks')}")

    def execute(self) -> None:
        if platform.system() != "Linux" or platform.machine() not in {"x86_64", "amd64"}:
            raise RuntimeError("campaign host must be Linux/AMD64")
        if not self.docker or not Path("/var/run/docker.sock").is_socket():
            raise RuntimeError("Docker host runtime is unavailable")
        if self.args.cuda_image_id != CUDA_IMAGE_ID:
            raise RuntimeError("campaign escaped the qualified CUDA image")
        verify_workspace(self.args.eval_workspace, self.args.eval_manifest, self.args.eval_archive, "ganesh-mini-development-evaluation-workspace/v1")
        verify_workspace(self.args.train_workspace, self.args.train_manifest, self.args.train_archive, "ganesh-mini-training-workspace/v1")
        if str(self.args.eval_workspace) not in sys.path:
            sys.path.insert(0, str(self.args.eval_workspace))
        self.record("workspace-isolation", "passed", evaluation_root=str(self.args.eval_workspace), training_root=str(self.args.train_workspace))
        self.baseline()
        gate1 = self.build_gate1()
        card = self.training_card(gate1)
        runs: dict[str, Path] = {}
        evaluations: dict[str, Path] = {}
        for label, learning_rate in LR_CANDIDATES:
            runs[label] = self.train(label, learning_rate, 400000, card)
            evaluations[label] = self.evaluate(label, runs[label])
        selection = self.select_lr(runs, evaluations)
        selected = float(load_sealed(selection, "evidence_sha256")["selected_learning_rate"])
        main = self.train("main", selected, 636093, card, selection)
        main_eval = self.evaluate("main", main)
        self.adjudicate(main, main_eval)
        final = {"schema_version": "ganesh-mini-staged-campaign-result/v1", "status": "passed", "attempt_id": self.args.attempt_id, "elapsed_seconds": round(time.monotonic()-self.started, 3), "phases": self.phases, "projected_compute_cost_usd": str(self.prior_cost())}
        final["evidence_sha256"] = canonical_sha256(final)
        atomic_json(self.output / "campaign-result.json", final)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-workspace", type=Path, required=True)
    parser.add_argument("--eval-manifest", type=Path, required=True)
    parser.add_argument("--eval-archive", type=Path, required=True)
    parser.add_argument("--train-workspace", type=Path, required=True)
    parser.add_argument("--train-manifest", type=Path, required=True)
    parser.add_argument("--train-archive", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--verifier-manifest", type=Path, required=True)
    parser.add_argument("--verifier-archive", type=Path, required=True)
    parser.add_argument("--gate0-report", type=Path, required=True)
    parser.add_argument("--gate2-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shared-tmp", type=Path, required=True)
    parser.add_argument("--cuda-image", required=True)
    parser.add_argument("--cuda-image-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--max-seconds", type=int, required=True)
    parser.add_argument("--finalization-reserve-seconds", type=int, default=1800)
    parser.add_argument("--hourly-cost-usd", type=Decimal, required=True)
    parser.add_argument("--training-cost-ceiling-usd", type=Decimal, required=True)
    args = parser.parse_args()
    if not 3600 <= args.max_seconds <= 64800 or not 1200 <= args.finalization_reserve_seconds < args.max_seconds:
        parser.error("invalid campaign time envelope")
    if args.hourly_cost_usd <= 0 or args.training_cost_ceiling_usd <= 0:
        parser.error("invalid campaign cost envelope")
    return args


def main() -> int:
    try:
        Campaign(parse_args()).execute()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        print(f"staged campaign failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
