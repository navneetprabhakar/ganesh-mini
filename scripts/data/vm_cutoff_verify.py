"""CPU-only cutoff verification runner; executed inside the sealed VM workspace."""
import hashlib
import json
import threading
import time
from collections import Counter
from pathlib import Path

from scripts.data import admit_expansion as admission
from scripts.eval.contracts import sha256_object
from scripts.verify.sandbox import verify


def write(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main():
    admission.configure_verifier_temp_root()
    output = Path("results")
    output.mkdir(exist_ok=True)
    config = json.loads(Path("cutoff.config.json").read_text())
    rows = admission.read_jsonl(Path("final.candidates.jsonl"))
    index = admission.evaluation_index([Path("eval")])
    runtime = Path("configs/eval/runtimes.json")
    sample = []
    for lane in sorted(config["lane_targets"]):
        for task_type in ("generation", "repair"):
            sample.append(next(r for r in rows if r["lane"] == lane and r["task_type"] == task_type))
    baseline = None
    trials = []
    for workers in (1, 4, 8):
        start = time.monotonic()
        accepted, rejected = admission.admit_records(sample, config, index, runtime, record_workers=workers)
        trial = {"workers": workers, "seconds": time.monotonic()-start,
                 "accepted": [r["id"] for r in accepted], "rejected": rejected}
        write(output / f"qualification-{workers}.json", {**trial, "evidence": accepted})
        if rejected or len(accepted) != len(sample):
            raise RuntimeError(f"qualification failed at {workers} workers")
        identity = [r["id"] for r in accepted]
        if baseline is not None and identity != baseline:
            raise RuntimeError("concurrent qualification changed admission outcome")
        baseline = identity
        trials.append(trial)
    chosen = min(trials, key=lambda trial: trial["seconds"])["workers"]
    write(output / "qualification.json", {"status": "passed", "selected_workers": chosen, "trials": trials})
    lock = threading.Lock()
    executed = 0
    started = time.monotonic()

    def logged_verify(task, code, runtime_config):
        nonlocal executed
        result = verify(task, code, runtime_config)
        with lock:
            executed += 1
            record = {"task_id": task["task_id"], "code_sha256": hashlib.sha256(code.encode()).hexdigest(), "result": result}
            with (output / "executions.jsonl").open("a") as stream:
                stream.write(json.dumps(record, sort_keys=True) + "\n")
            write(output / "progress.json", {"status": "running", "executions": executed,
                  "elapsed_seconds": time.monotonic()-started, "last_task_id": task["task_id"], "workers": chosen})
        return result

    accepted, rejected = admission.admit_records(rows, config, index, runtime, verifier=logged_verify, record_workers=chosen)
    lanes = dict(Counter(r["lane"] for r in accepted))
    types = dict(Counter(r["task_type"] for r in accepted))
    balanced = len(accepted) == config["target_records"] and lanes == config["lane_targets"] and types == config["task_type_targets"]
    payload = b"".join(admission.canonical_json(r)+b"\n" for r in accepted)
    (output / "final.admitted.jsonl").write_bytes(payload)
    report = {"schema_version": "ganesh-mini-expansion-vm-admission/v1", "mode": "sealed",
              "status": "passed" if not rejected and balanced else "failed", "balance_passed": balanced,
              "accepted": len(accepted), "rejected": rejected, "counts_by_lane": lanes,
              "counts_by_task_type": types, "evaluation_files_inspected": len(index["inspected"]),
              "input_sha256": hashlib.sha256(Path("final.candidates.jsonl").read_bytes()).hexdigest(),
              "config_sha256": hashlib.sha256(Path("cutoff.config.json").read_bytes()).hexdigest(),
              "output_sha256": hashlib.sha256(payload).hexdigest(), "workers": chosen,
              "elapsed_seconds": time.monotonic()-started,
              "quality_review": "separate and incomplete; execution pass is not training authorization"}
    report["report_sha256"] = sha256_object(report)
    write(output / "final.admission.json", report)
    write(output / "progress.json", {"status": report["status"], "executions": executed})
    if report["status"] != "passed":
        raise RuntimeError("final admission rejected records; see preserved evidence")


if __name__ == "__main__":
    main()
