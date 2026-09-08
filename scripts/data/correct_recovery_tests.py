"""One immutable specification-only test correction, reusing reviewed recovery code."""

from __future__ import annotations

import argparse
import copy
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scripts.data.admit_expansion import canonical_json, validate_candidate
from scripts.data.generate_expansion_qualification import (
    TEST_SCHEMA, CodexInvocationFailure, critic_test_prompt, exact_items,
    invoke_codex, verify_codex_version,
)
from scripts.data.generate_versioned_recovery import ROOT, REGISTRY, persist, reserve_version, validate_inputs
from scripts.data.plan_versioned_recovery import digest


def correct(plan, previous, feedback, config, binary, directory, lane_workers=1):
    if not 1 <= lane_workers <= 3:
        raise ValueError("lane_workers must be between one and three")
    grouped = defaultdict(list)
    for row in plan["records"]:
        grouped[row["lane"]].append(row)
    def correct_lane(lane, rows):
        if len(rows) > config["execution"].get("batch_size", 10):
            raise ValueError("lane exceeds frozen teacher batch size")
        architecture, tests, notes, candidates = [], [], [], []
        for row in rows:
            source = previous[row["id"]]
            architecture.append({"id": row["id"], "problem": source["messages"][0]["content"]})
            test_files = [f for f in source["verification_task"]["files"] if f["role"] == "test"]
            if len(test_files) != 1:
                raise ValueError("correction requires one independently authored test file")
            tests.append({"id": row["id"], "test_code": test_files[0]["content"]})
            notes.append({"id": row["id"], "specification_review": feedback[row["id"]]["specification_review"]})
        prompt = critic_test_prompt(lane, architecture, tests)
        prompt += "\nSpecification-derived review (no reference or mutant code): " + json.dumps(notes, ensure_ascii=False)
        path = directory / f"{lane}-recovery-test-correction-evidence.json"
        try:
            payload, evidence = invoke_codex(binary, config, TEST_SCHEMA, prompt, "recovery-test-correction", lane)
        except CodexInvocationFailure as exc:
            persist(path, exc.evidence)
            raise
        persist(path, evidence)
        corrected = exact_items(payload, [row["id"] for row in rows], {"id", "test_code"})
        for row, test in zip(rows, corrected, strict=True):
            candidate = copy.deepcopy(previous[row["id"]])
            candidate["id"] = row["id"]
            candidate["verification_task"]["task_id"] = row["id"]
            candidate["source"] = copy.deepcopy(row["parent_source"])
            candidate["source"]["transformation"] += f"; versioned recovery {row['id']} from {row['parent_id']} sha256={row['parent_candidate_sha256']}"
            content = test["test_code"].strip() + "\n"
            for item in candidate["verification_task"]["files"]:
                if item["role"] == "test":
                    item.update(content=content, sha256=digest(content.encode()))
            persist(directory / f"{row['id']}.candidate.json", candidate)
            candidates.append(candidate)
        return candidates

    completed = {}
    failures = {}
    with ThreadPoolExecutor(max_workers=lane_workers) as executor:
        futures = {executor.submit(correct_lane, lane, rows): lane
                   for lane, rows in grouped.items()}
        for future in as_completed(futures):
            lane = futures[future]
            try:
                completed[lane] = future.result()
            except Exception as exc:
                failures[lane] = exc
                persist(directory / f"{lane}-failure.json", {
                    "status": "correction-failed-not-admitted", "lane": lane,
                    "type": type(exc).__name__, "reason": str(exc),
                })
    if failures:
        persist(directory / "lane-results.json", {
            "status": "partial-correction-not-verified-not-admitted",
            "completed_lanes": sorted(completed), "failed_lanes": sorted(failures),
        })
        raise failures[next(lane for lane in grouped if lane in failures)]
    by_id = {row["id"]: row for rows in completed.values() for row in rows}
    candidates = [by_id[row["id"]] for row in plan["records"]]
    with (directory / "candidates.jsonl").open("xb") as handle:
        for row in candidates:
            handle.write(canonical_json(row) + b"\n")
    return candidates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--prior-run", type=Path, required=True)
    parser.add_argument("--feedback", type=Path, required=True)
    parser.add_argument("--input", type=Path, default=ROOT / "datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl")
    parser.add_argument("--holds", type=Path, default=ROOT / "measurement/data/expansion-v1/cutoff-5885-review/additional-holds.json")
    parser.add_argument("--config", type=Path, default=ROOT / "configs/data/expansion_teacher.json")
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--lane-workers", type=int, choices=(1, 2, 3), default=1)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    prior_plan = json.loads((args.prior_run / "plan.json").read_text())
    contract = json.loads((args.prior_run / "run-contract.json").read_text())
    closure = contract["quality_closure"]
    for item in (plan, prior_plan):
        validate_inputs(item, closure, args.input.read_bytes(), args.holds.read_bytes(), ROOT)
    if contract.get("correction_attempt"):
        raise ValueError("one bounded correction only; no repeated critic loop")
    feedback = json.loads(args.feedback.read_text())
    if set(feedback) != {row["id"] for row in plan["records"]}:
        raise ValueError("feedback must bind exact planned IDs")
    prior_ids = {row["id"] for row in prior_plan["records"]}
    previous = {}
    source_hashes = {}
    candidate_config = json.loads((ROOT / "configs/data/expansion_v1.json").read_text())
    for row in plan["records"]:
        if row["change_class"] != "oracle-rebuild":
            raise ValueError("test correction must declare oracle-rebuild")
        id = row["parent_id"].replace("exp-v1-", f"exp-v1-recovery-{prior_plan['version']}-", 1)
        if id not in prior_ids:
            raise ValueError("previous candidate not planned")
        path = args.prior_run / f"{id}.candidate.json"
        source = json.loads(path.read_text())
        validate_candidate(source, candidate_config)
        if source["id"] != id or digest(canonical_json(source)) != feedback[row["id"]]["previous_candidate_sha256"]:
            raise ValueError("previous candidate hash mismatch")
        if source["rights"] != row["parent_rights"] or source["lane"] != row["lane"] or source["task_type"] != row["task_type"]:
            raise ValueError("previous candidate lane/type/rights mismatch")
        if not feedback[row["id"]].get("specification_review", "").strip():
            raise ValueError("explicit specification review required")
        previous[row["id"]] = source
        source_hashes[str(path)] = digest(path.read_bytes())
    config = json.loads(args.config.read_text())
    cli = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    directory = reserve_version(REGISTRY, plan)
    persist(directory / "run-contract.json", {"quality_closure": closure, "teacher": config,
        "cli_identity": cli, "correction_attempt": 1, "prior_plan_sha256": prior_plan["plan_sha256"],
        "lane_workers": args.lane_workers,
        "prior_candidate_files": source_hashes, "feedback": feedback,
        "feedback_file_sha256": digest(args.feedback.read_bytes()),
        "unchanged": ["specification", "reference", "known-bad"],
        "status": "test-correction-not-admitted"})
    try:
        rows = correct(plan, previous, feedback, config, args.codex_bin, directory, args.lane_workers)
    except Exception as exc:
        persist(directory / "failure.json", {"status": "correction-failed-not-admitted", "type": type(exc).__name__, "reason": str(exc)})
        raise
    persist(directory / "generation.json", {"status": "generated-not-verified-not-admitted", "count": len(rows),
        "candidate_sha256": digest((directory / "candidates.jsonl").read_bytes()), "plan_sha256": plan["plan_sha256"]})
    print(json.dumps({"generated": len(rows), "directory": str(directory), "admitted": False}))


if __name__ == "__main__":
    main()
