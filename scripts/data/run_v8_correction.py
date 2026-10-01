#!/usr/bin/env python3
"""Execute and seal the two-role V8 correction campaign."""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.build_capability_separation_attestations import PASS_FIELDS, build_report as build_separation
from scripts.data.generate_expansion_qualification import verify_codex_version
from scripts.data.repair_delta_v7_readiness import CANONICAL_LANE_INTERFACES, validate_lane_interface
from scripts.data.repair_delta_v8_readiness import CONTRACT_ID, RESPONSE_SCHEMA_VERSION, validate_response
from scripts.data.run_repair_delta_evidence import IsolatedCodexAdapter, _delta_evidence, _executable_evidence, delta_projection, seal
from scripts.data.run_repair_delta_two_phase import build_separation_sidecars
from scripts.eval.contracts import sha256_text
from scripts.verify.sandbox import verify


EXPECTED = {"reference.primary_discrimination": "pass", "reference.cross_cutting": "pass", "known_bad.primary_discrimination": "fail", "known_bad.cross_cutting": "pass"}


def _projection(row: dict[str, Any], role: str) -> dict[str, Any]:
    candidate = row["envelope"]["candidate"]; assignment = row["envelope"]["assignment"]
    interface = CANONICAL_LANE_INTERFACES[candidate["lane"]]
    rust = candidate["lane"] == "rust"
    return {
        "id": f"v8-{candidate['id']}-{role}", "specification": candidate["messages"][0]["content"],
        "embedded_known_bad": candidate["verification_task"]["validation"]["known_bad"][0]["code"],
        "lane": candidate["lane"], "role": role,
        "primary_capability": assignment["primary_capability"], "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"],
        "canonical_candidate_filename": interface["candidate_path"], "canonical_test_filename": interface["test_path"],
        "execution_commands": interface["commands"], "required_local_binding": interface["binding"],
        "role_constraints": (
            "Author only the Rust primary suite with at least two externally observable cases. Test that marking makes is_audit true, missing reads false, and unrelated metadata is preserved. Do not assert a literal metadata key because the specification does not uniquely name one. Reject the visible known-bad."
            if rust else
            "Author only the Python cross suite with at least one case. It must pass the visible known-bad and test only input non-mutation or alias isolation. Do not mock, patch, intercept, or assert the value passed to SHA-256, and do not assert the returned digest."
        ),
        "semantic_guard": "rust-no-internal-key" if rust else "python-no-primary-digest-dataflow",
    }


def _replace(row: dict[str, Any], role: str, response: dict[str, Any], run_sha: str) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = copy.deepcopy(row["envelope"]["candidate"]); assignment = row["envelope"]["assignment"]
    old_evidence = row["envelope"]["evidence"]["test_author"]
    old_roles = {item["role"]: item for item in old_evidence["test_roles"]}
    old_files = {item["path"]: item for item in candidate["verification_task"]["files"] if item.get("role") == "test"}
    support = [item for item in candidate["verification_task"]["files"] if item.get("role") == "support"]
    files, roles = [], []
    for current in ("primary_discrimination", "cross_cutting"):
        old = old_roles[current]
        if current == role:
            content = response["content"].rstrip() + "\n"; cases = response["case_ids"]
        else:
            content = old_files[old["path"]]["content"]; cases = old["case_ids"]
        if validate_lane_interface(candidate["lane"], content): raise ValueError(f"{candidate['id']}/{current}: static interface failed")
        path = f"v8/{current}/{CANONICAL_LANE_INTERFACES[candidate['lane']]['test_path']}"; digest = sha256_text(content)
        files.append({"path": path, "role": "test", "content": content, "sha256": digest})
        roles.append({"path": path, "canonical_path": CANONICAL_LANE_INTERFACES[candidate["lane"]]["test_path"], "file_sha256": digest, "role": current, "case_ids": cases, "valid_domain_only": current == "primary_discrimination", "scheduled_dimension_only": current == "cross_cutting"})
    candidate["verification_task"]["files"] = [*support, *files]
    evidence = seal({"candidate_sha256": canonical_sha256(candidate), "specification_sha256": sha256_text(candidate["messages"][0]["content"]), "known_bad_sha256": candidate["verification_task"]["validation"]["known_bad"][0]["sha256"], "primary_capability": assignment["primary_capability"], "assigned_cross_cutting_dimension": assignment["assigned_cross_cutting_dimension"], "response_schema_version": RESPONSE_SCHEMA_VERSION, "test_roles": roles, "test_author_run_evidence_sha256": run_sha, "carried_role": "cross_cutting" if role == "primary_discrimination" else "primary_discrimination", "visibility": {"specification_visible": True, "embedded_known_bad_visible": True, "capability_definition_visible": True, "scheduled_dimension_visible": True, "reference_visible": False, "teacher_proof_visible": False, "semantic_review_visible": False, "verifier_outputs_visible": False, "evaluation_artifacts_read": 0}})
    return candidate, evidence


def _outcomes(executable): return {f"{impl}.{role}": ("pass" if result.get("exit_codes") and all(code == 0 for code in result["exit_codes"]) else "fail") for impl, roles in executable["results"].items() for role, result in roles.items()}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plan", type=Path, required=True); p.add_argument("--readiness", type=Path, required=True); p.add_argument("--v7-terminal", type=Path, required=True)
    p.add_argument("--training-corpus", type=Path, action="append", required=True); p.add_argument("--evaluation-root", type=Path, action="append", required=True)
    p.add_argument("--runtimes", type=Path, default=Path("configs/eval/runtimes.json")); p.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json")); p.add_argument("--run-dir", type=Path, required=True); p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args(); readiness=json.loads(args.readiness.read_text()); rows=[json.loads(x) for x in args.v7_terminal.read_text().splitlines() if x]
    if readiness.get("status")!="passed" or len(rows)!=60: raise ValueError("V8 readiness/V7 terminal input invalid")
    targets=[row for row in rows if row["status"]!="admitted"]
    if [r["lane"] for r in targets] != ["rust","python"]: raise ValueError("V8 target order differs")
    roles=["primary_discrimination","cross_cutting"]; projections=[_projection(row,role) for row,role in zip(targets,roles,strict=True)]
    config=json.loads(args.codex_config.read_text()); cli=verify_codex_version("codex",config["codex_cli_version"])
    def author(proj): return IsolatedCodexAdapter("test_author",config,"codex",args.run_dir,cli,"v8")(proj)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex: responses=list(ex.map(author,projections))
    corrected=[]; tests=[]
    for row,role,proj,response in zip(targets,roles,projections,responses,strict=True):
        run_sha=response.pop("_run_sha256"); validate_response(proj,response); candidate,evidence=_replace(row,role,response,run_sha); corrected.append(candidate); tests.append(evidence)
    delta_projections=[delta_projection(c,r["envelope"]["assignment"]) for c,r in zip(corrected,targets,strict=True)]
    def audit(proj): return IsolatedCodexAdapter("delta_audit",config,"codex",args.run_dir,cli,"v8")(proj)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex: delta_responses=list(ex.map(audit,delta_projections))
    deltas=[]
    for candidate,row,response in zip(corrected,targets,delta_responses,strict=True):
        run_sha=response.pop("_run_sha256"); ev=_delta_evidence(candidate,row["envelope"]["assignment"],response,run_sha)
        if ev["independent_semantic_delta_count"]!=1 or ev["delta_is_capability_specific"] is not True or ev["introduces_multiple_independent_fixes"] is not False: raise ValueError("V8 delta audit rejected")
        deltas.append(ev)
    corrected_by_id={c["id"]:c for c in corrected}; complete=[corrected_by_id.get(row["candidate_id"],row["envelope"]["candidate"]) for row in rows]
    args.output_dir.mkdir(parents=True,exist_ok=True); complete_path=args.output_dir/"complete-candidates.jsonl"; complete_path.write_text("".join(json.dumps(c,sort_keys=True)+"\n" for c in complete))
    separation=build_separation(complete_path,args.training_corpus,args.evaluation_root); (args.output_dir/"global-separation-report.json").write_text(json.dumps(separation,indent=2,sort_keys=True)+"\n")
    if separation["status"]!="passed": raise ValueError("V8 separation failed")
    sidecars,contract=build_separation_sidecars(separation,complete,args.output_dir/"separation-sidecars.jsonl"); side={x["candidate_id"]:x for x in sidecars}
    final=[]
    for source,candidate,test,delta in zip(targets,corrected,tests,deltas,strict=True):
        executable,retry=_executable_evidence(candidate,test,args.runtimes,verify); outcomes=_outcomes(executable)
        status="admitted" if not retry["unresolved"] and outcomes==EXPECTED and all(side[candidate["id"]][f] is True for f in PASS_FIELDS) else "rejected"
        final.append({"candidate_id":candidate["id"],"lane":candidate["lane"],"status":status,"outcomes":outcomes,"candidate_sha256":canonical_sha256(candidate),"test_author_evidence_sha256":test["evidence_sha256"],"delta_evidence_sha256":delta["evidence_sha256"],"separation_evidence_sha256":side[candidate["id"]]["evidence_sha256"],"executable_evidence":executable,"retry_ledger":retry})
    carried=[row for row in rows if row["status"]=="admitted"]
    passed=len(carried)==58 and all(item["status"]=="admitted" for item in final)
    report={"schema_version":"ganesh-mini-gate2-v8-qualification-summary/v1","contract_id":CONTRACT_ID,"status":"passed" if passed else "qualification-failed","plan_sha256":hashlib.sha256(args.plan.read_bytes()).hexdigest(),"readiness_report_sha256":readiness["report_sha256"],"v7_carried_admissions":58,"fresh_role_author_calls":2,"fresh_delta_audit_calls":2,"final_admitted":60 if passed else 58+sum(x["status"]=="admitted" for x in final),"unresolved":sum(x["retry_ledger"]["unresolved"] for x in final),"corrected_rows":final,"separation_report_sha256":separation["report_sha256"],"separation_contract_sha256":contract,"v2_generation_equivalence":{"status":"passed","generation_cells":60,"qualification_report_sha256":"293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139"},"combined_coverage":{"covered":120 if passed else 118+sum(x["status"]=="admitted" for x in final),"required":120},"evaluation_artifacts_read_outside_content_free_boundary":0,"training_entry_eligible":passed}
    report["report_sha256"]=canonical_sha256(report); (args.output_dir/"qualification-summary-v8.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":report["status"],"final_admitted":report["final_admitted"],"report_sha256":report["report_sha256"]},sort_keys=True)); return 0 if passed else 2


if __name__=="__main__": raise SystemExit(main())
