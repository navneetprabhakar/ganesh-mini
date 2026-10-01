#!/usr/bin/env python3
"""Seal V8 58+2 accounting, live schema smoke, and two executable canaries."""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import verify_codex_version
from scripts.data.repair_delta_v7_readiness import CANONICAL_LANE_INTERFACES, validate_lane_interface
from scripts.data.repair_delta_v8_readiness import CONTRACT_ID, response_schema, validate_response
from scripts.data.run_repair_delta_evidence import IsolatedCodexAdapter, _executable_evidence, seal
from scripts.eval.contracts import sha256_text
from scripts.verify.sandbox import verify


EXPECTED = {"reference.primary_discrimination": "pass", "reference.cross_cutting": "pass", "known_bad.primary_discrimination": "fail", "known_bad.cross_cutting": "pass"}


def _projection(identifier: str, candidate: dict[str, Any], assignment: dict[str, Any], role: str, constraints: str, guard: str | None = None) -> dict[str, Any]:
    interface = CANONICAL_LANE_INTERFACES[candidate["lane"]]
    return {
        "id": identifier, "specification": candidate["messages"][0]["content"],
        "embedded_known_bad": candidate["verification_task"]["validation"]["known_bad"][0]["code"],
        "lane": candidate["lane"], "role": role,
        "primary_capability": assignment["primary_capability"],
        "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        "canonical_candidate_filename": interface["candidate_path"],
        "canonical_test_filename": interface["test_path"], "execution_commands": interface["commands"],
        "required_local_binding": interface["binding"], "role_constraints": constraints,
        "semantic_guard": guard,
    }


def _canonical(lane: str, content: str) -> str:
    if lane == "rust" and '#[path = "solution.rs"] mod solution;' not in content:
        content = content.replace("mod solution;", '#[path = "solution.rs"] mod solution;')
    return content.rstrip() + "\n"


def _replace_role(fixture: dict[str, Any], role: str, response: dict[str, Any], run_sha: str) -> tuple[dict[str, Any], dict[str, Any]]:
    envelope = fixture["envelope"]
    candidate = copy.deepcopy(envelope["candidate"])
    source_roles = {row["role"]: row for row in envelope["evidence"]["test_author"]["test_roles"]}
    source_files = {row["path"]: row for row in candidate["verification_task"]["files"] if row.get("role") == "test"}
    support = [row for row in candidate["verification_task"]["files"] if row.get("role") == "support"]
    files, roles = [], []
    for current in ("primary_discrimination", "cross_cutting"):
        if current == role:
            content = _canonical(candidate["lane"], response["content"])
            cases = response["case_ids"]
            path = f"v8-{current}-{candidate['lane']}.test"
        else:
            source = source_roles[current]
            content = _canonical(candidate["lane"], source_files[source["path"]]["content"])
            cases = source["case_ids"]
            path = f"carried-{current}-{candidate['lane']}.test"
        findings = validate_lane_interface(candidate["lane"], content)
        if findings:
            raise ValueError(f"{candidate['lane']}/{current}: canary interface findings: {findings}")
        digest = sha256_text(content)
        files.append({"path": path, "role": "test", "content": content, "sha256": digest})
        roles.append({"path": path, "canonical_path": CANONICAL_LANE_INTERFACES[candidate["lane"]]["test_path"], "file_sha256": digest, "role": current, "case_ids": cases})
    candidate["verification_task"]["files"] = [*support, *files]
    evidence = seal({"candidate_sha256": canonical_sha256(candidate), "test_roles": roles, "test_author_run_evidence_sha256": run_sha, "evaluation_artifacts_read": 0})
    return candidate, evidence


def _outcomes(executable: dict[str, Any]) -> dict[str, str]:
    return {f"{impl}.{role}": ("pass" if result.get("exit_codes") and all(code == 0 for code in result["exit_codes"]) else "fail") for impl, roles in executable["results"].items() for role, result in roles.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--v7-terminal", type=Path, required=True)
    parser.add_argument("--v7-qualification", type=Path, required=True)
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--runtimes", type=Path, default=Path("configs/eval/runtimes.json"))
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    terminal = [json.loads(line) for line in args.v7_terminal.read_text(encoding="utf-8").splitlines() if line]
    qualification = json.loads(args.v7_qualification.read_text(encoding="utf-8"))
    rejected = [row for row in terminal if row["status"] != "admitted"]
    if len(terminal) != 60 or len(rejected) != 2 or qualification.get("report_sha256") != "1bbdd82b8558542547f0476e8b753089a0c93e73221f4db4c6b6b9787dde3f06":
        raise ValueError("V8 accounting does not bind terminal V7")
    manifest = {"schema_version": "ganesh-mini-gate2-v8-correction-manifest/v1", "contract_id": CONTRACT_ID, "status": "sealed", "v7_qualification_report_sha256": qualification["report_sha256"], "carried_complete_admissions": 58, "corrections": [{"candidate_id": rejected[0]["candidate_id"], "replace_role": "primary_discrimination", "carry_role": "cross_cutting"}, {"candidate_id": rejected[1]["candidate_id"], "replace_role": "cross_cutting", "carry_role": "primary_discrimination"}], "model_call_budget": {"readiness_schema_smoke": 1, "readiness_canaries": 2, "qualification_role_authors": 2, "qualification_delta_audits": 2}, "evaluation_artifacts_read": 0}
    manifest["manifest_sha256"] = canonical_sha256(manifest)

    bundle = json.loads(args.fixtures.read_text(encoding="utf-8"))
    by_lane = {row["envelope"]["candidate"]["lane"]: row for row in bundle["fixtures"] if row.get("expected") == "admitted"}
    rust, python = by_lane["rust"], by_lane["python"]
    smoke = _projection("v8-live-schema-smoke", rust["envelope"]["candidate"], rust["envelope"]["assignment"], "primary_discrimination", "Author at least two externally observable primary cases that reject the visible known-bad.")
    rust_p = _projection("v8-readiness-canary-rust", rust["envelope"]["candidate"], rust["envelope"]["assignment"], "primary_discrimination", "Author at least two compute_total result cases that reject maximum-selection; do not assert internal representation.")
    py_p = _projection("v8-readiness-canary-python", python["envelope"]["candidate"], python["envelope"]["assignment"], "cross_cutting", "Author only the malformed-empty-input behavior already satisfied by the visible known-bad; do not assert summation results.")
    config = json.loads(args.codex_config.read_text(encoding="utf-8")); cli = verify_codex_version("codex", config["codex_cli_version"])
    projections = [smoke, rust_p, py_p]
    def call(projection): return IsolatedCodexAdapter("test_author", config, "codex", args.run_dir, cli, "v8")(projection)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor: responses = list(executor.map(call, projections))
    for projection, response in zip(projections, responses, strict=True):
        run_sha = response.pop("_run_sha256"); validate_response(projection, response); response["_run_sha256"] = run_sha
    canary_rows = []
    for fixture, role, projection, response in ((rust, "primary_discrimination", rust_p, responses[1]), (python, "cross_cutting", py_p, responses[2])):
        run_sha = response.pop("_run_sha256"); candidate, evidence = _replace_role(fixture, role, response, run_sha)
        executable, retry = _executable_evidence(candidate, evidence, args.runtimes, verify); outcomes = _outcomes(executable)
        if retry["unresolved"] or outcomes != EXPECTED: raise ValueError(f"V8 readiness canary failed: {candidate['lane']} {outcomes}")
        canary_rows.append({"lane": candidate["lane"], "role": role, "response_sha256": canonical_sha256(response), "executable_evidence_sha256": executable["evidence_sha256"], "outcomes": outcomes})
    report = {"schema_version": "ganesh-mini-gate2-v8-readiness-composite/v1", "contract_id": CONTRACT_ID, "plan_sha256": hashlib.sha256(args.plan.read_bytes()).hexdigest(), "status": "passed", "correction_manifest_sha256": manifest["manifest_sha256"], "provider_schema_sha256": canonical_sha256(response_schema()), "live_schema_smoke_run_sha256": responses[0]["_run_sha256"], "canaries": canary_rows, "canaries_sha256": canonical_sha256(canary_rows), "evaluation_artifacts_read": 0}
    report["report_sha256"] = canonical_sha256(report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "correction-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
    (args.output_dir / "readiness-composite.json").write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"status": "passed", "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__": raise SystemExit(main())
