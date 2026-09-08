"""Preserve serial sandbox diagnostics for recovery candidates; never admit data."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from scripts.data.admit_expansion import configure_verifier_temp_root, validate_candidate
from scripts.data.generate_versioned_recovery import ROOT, persist, validate_inputs
from scripts.data.plan_versioned_recovery import digest
from scripts.data.admit_expansion import canonical_json
from scripts.verify.sandbox import infrastructure_failure, verify


def race_runtime(config: dict) -> dict:
    derived = copy.deepcopy(config)
    runtime = derived["runtimes"]["go-1.22.12"]
    if runtime["commands"] != [["go", "test", "./..."]]:
        raise ValueError("unexpected Go command contract")
    runtime["commands"] = [["go", "test", "-race", "./..."]]
    return derived


def outcome(result: dict) -> str:
    if infrastructure_failure(result):
        return "infrastructure-failure"
    if result["timed_out"]:
        return "timeout-not-semantic-proof"
    codes = result["exit_codes"]
    if codes and all(code == 0 for code in codes):
        return "passed"
    # A compiler/loader failure is not proof that a behavioral regression is caught.
    text = (result.get("stdout", "") + result.get("stderr", "")).lower()
    if len(codes) < len(result.get("commands", codes)) or any(
        marker in text for marker in ("syntaxerror", "indentationerror", "[build failed]", "[setup failed]")
    ):
        return "compile-or-load-failure-not-semantic-proof"
    return "behavioral-failure-requires-review"


def execute_record(candidate: dict, parent: dict, runtime: Path, directory: Path,
                   verifier=verify) -> dict:
    task = copy.deepcopy(candidate["verification_task"])
    task["surface"] = "synthetic_harness"
    programs = [("reference", candidate["messages"][1]["content"])]
    programs += [(f"known-bad-{i}", item["code"]) for i, item in enumerate(task["validation"]["known_bad"])]
    programs.append(("original-parent-reference", parent["messages"][1]["content"]))
    results = []
    for label, code in programs:
        evidence = {"label": label, "code": code, "code_sha256": digest(code.encode()),
                    "candidate_sha256": digest(canonical_json(candidate)),
                    "parent_candidate_sha256": digest(canonical_json(parent))}
        try:
            evidence["result"] = verifier(task, code, runtime)
            evidence["outcome"] = outcome(evidence["result"])
        except Exception as exc:
            evidence.update(outcome="verifier-exception-not-behavioral-proof",
                            error={"type": type(exc).__name__, "message": str(exc)})
        evidence["evidence_sha256"] = digest(canonical_json(evidence))
        persist(directory / f"{candidate['id']}-{label}.json", evidence)
        results.append({"label": label, "outcome": evidence["outcome"],
                        "evidence_sha256": evidence["evidence_sha256"]})
    directions = results[0]["outcome"] == "passed" and all(
        row["outcome"] == "behavioral-failure-requires-review" for row in results[1:]
    )
    summary = {"id": candidate["id"], "results": results, "directionality_passed": directions,
               "status": "diagnostic-only-not-admitted", "quality_and_separation": "pending"}
    persist(directory / f"{candidate['id']}-summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--input", type=Path, default=ROOT / "datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl")
    parser.add_argument("--holds", type=Path, default=ROOT / "measurement/data/expansion-v1/cutoff-5885-review/additional-holds.json")
    parser.add_argument("--config", type=Path, default=ROOT / "configs/data/expansion_v1.json")
    parser.add_argument("--runtime", type=Path, default=ROOT / "configs/eval/runtimes.json")
    parser.add_argument("--id", action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--go-race", action="store_true", help="additional qualification; keep image and resource limits pinned")
    args = parser.parse_args()
    plan = json.loads((args.run / "plan.json").read_text())
    contract = json.loads((args.run / "run-contract.json").read_text())
    parents = validate_inputs(plan, contract["quality_closure"], args.input.read_bytes(), args.holds.read_bytes(), ROOT)
    planned = {row["id"]: row for row in plan["records"]}
    if len(set(args.id)) != len(args.id) or any(id not in planned for id in args.id):
        raise ValueError("select unique planned IDs")
    config = json.loads(args.config.read_text())
    candidates = []
    for id in args.id:
        candidate = json.loads((args.run / f"{id}.candidate.json").read_text())
        validate_candidate(candidate, config)
        if candidate["id"] != id or candidate["rights"] != planned[id]["parent_rights"]:
            raise ValueError("candidate identity or rights mismatch")
        expected_source = copy.deepcopy(planned[id]["parent_source"])
        expected_source["transformation"] += f"; versioned recovery {id} from {planned[id]['parent_id']} sha256={planned[id]['parent_candidate_sha256']}"
        if candidate["source"] != expected_source:
            raise ValueError("candidate lineage mismatch")
        candidates.append(candidate)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    runtime = args.runtime
    if args.go_race:
        if any(row["lane"] != "go" for row in candidates):
            raise ValueError("race qualification is Go-only")
        runtime = args.output_dir / "race-runtimes.json"
        persist(runtime, race_runtime(json.loads(args.runtime.read_text())))
    persist(args.output_dir / "manifest.json", {"status": "diagnostics-not-admission",
        "plan_sha256": plan["plan_sha256"], "runtime_sha256": digest(runtime.read_bytes()),
        "parent_runtime_sha256": digest(args.runtime.read_bytes()), "go_race": args.go_race,
        "config_sha256": digest(args.config.read_bytes()),
        "candidates": {row["id"]: digest(canonical_json(row)) for row in candidates}})
    configure_verifier_temp_root()
    summaries = []
    for candidate in candidates:
        summary = execute_record(candidate, parents[planned[candidate["id"]]["parent_id"]], runtime, args.output_dir)
        summaries.append(summary)
        print(json.dumps({"id": summary["id"], "directionality_passed": summary["directionality_passed"],
                          "outcomes": [row["outcome"] for row in summary["results"]]}), flush=True)
    persist(args.output_dir / "summary.json", {"status": "diagnostics-not-admission", "records": summaries})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
