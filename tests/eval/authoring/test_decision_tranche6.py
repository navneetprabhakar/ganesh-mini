import pytest

from scripts.eval.authoring.build_decision_tranche6 import DEVELOPMENT_MANIFESTS, EXPECTED_TRANCHE5_SHA256, PRIOR_DECISION_MANIFESTS, ROOT, SEED_PATHS, SLUGS, artifact, build
from scripts.eval.contracts import load_json, sha256_object, validate_task
from scripts.verify.sandbox import SANDBOX_CONTRACT


def test_reference_generator_avoids_known_mechanical_defects() -> None:
    for slug in SLUGS:
        python_source, _, _ = artifact("python", slug)
        compile(python_source, "solution.py", "exec")

        typescript_source, _, _ = artifact("typescript", slug)
        assert "const nums=(s:string):number[]|null" in typescript_source
        assert "let m=" in typescript_source and "a:number[]=[]" in typescript_source
        assert ",a,k,lo,hi,q" not in typescript_source

        javascript_source, _, _ = artifact("javascript", slug)
        assert "number[]" not in javascript_source
        assert "const q=s.split(';')," in javascript_source

        go_source, _, _ = artifact("go", slug)
        assert go_source.count('"regexp"') == 1 and "regexp.MustCompile" in go_source
        assert go_source.count('"strconv"') == 1 and "strconv.Atoi" in go_source
        assert go_source.count('"strings"') == 1 and "strings.Split" in go_source


def test_decision_tranche6_contract_balance_hashes_and_separation() -> None:
    tranche5 = load_json(ROOT / PRIOR_DECISION_MANIFESTS[-1])
    assert tranche5["manifest_sha256"] == EXPECTED_TRANCHE5_SHA256
    manifest, overlap = build()
    assert manifest["surface"] == "decision" and manifest["status"] == "authored-unexecuted"
    assert manifest["task_count"] == 60
    assert all(counts == {"generation": 5, "repair": 5} for counts in manifest["counts_by_lane"].values())
    assert overlap["comparison_inputs"] == {"seed_jsonl": list(SEED_PATHS), "private_development_manifests": list(DEVELOPMENT_MANIFESTS), "prior_decision_manifests": list(PRIOR_DECISION_MANIFESTS)}
    assert overlap["seed_records_inspected"] == 1449
    assert overlap["private_development_prompts_inspected"] == 180
    assert overlap["prior_decision_prompts_inspected"] == 300
    assert overlap["comparison_prompts_inspected"] == 1929
    assert overlap["evaluation_prompts_inspected"] == 60
    assert overlap["exact_prompt_overlaps"] == overlap["normalized_prompt_overlaps"] == []
    assert overlap["within_tranche_exact_overlaps"] == overlap["within_tranche_normalized_overlaps"] == []
    assert overlap["evaluation_manifest_sha256"] == manifest["manifest_sha256"]
    assert sha256_object({k: v for k, v in overlap.items() if k != "report_sha256"}) == overlap["report_sha256"]
    assert len({entry["task_id"] for entry in manifest["tasks"]}) == 60
    assert all(any(slug in entry["task_id"] for slug in SLUGS) for entry in manifest["tasks"])
    for entry in manifest["tasks"]:
        task = validate_task(load_json(ROOT / entry["path"])); assert sha256_object(task) == entry["sha256"]
        assert task["limits"] == {"timeout_seconds": 60 if task["language"] in {"go", "java", "rust"} else 30, "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536}
        prompt = task["prompt"]["text"]
        assert all(label in prompt for label in ("File contract:", "Required API:", "Behavior:", "Visible example:", "Return only the complete source file"))
        assert task["prompt"]["sha256"] == task["rendered_prompt"]["sha256"]
        if task["task_type"] == "repair":
            assert "Buggy source to repair:" in prompt and task["validation"]["known_bad"][0]["code"] in prompt


def test_executed_directionality_evidence_is_complete_and_bound() -> None:
    evidence_path = ROOT / "manifests/evaluation/private/decision-tranche6-directionality.json"
    if not evidence_path.exists(): pytest.skip("directionality has not been executed")
    evidence = load_json(evidence_path); claimed = evidence.pop("evidence_sha256")
    assert sha256_object(evidence) == claimed and evidence["status"] == "passed"
    assert evidence["execution_mode"] == "sequential"
    assert evidence["evaluation_manifest_sha256"] == "f97eb03d1206cb7135a520f2fb069a44375b9332a4e36ddc9f78cbb0ca6d7c89"
    assert evidence["overlap_report"] == "manifests/evaluation/private/decision-tranche6-overlap.json"
    assert evidence["overlap_report_sha256"] == "80f4d7f340fc4994f97e8c332e9eea9a339c7eb4837f9d00595775b0ef1ba0ff"
    assert SANDBOX_CONTRACT["backend"] == "docker" and SANDBOX_CONTRACT["network"] == "none" and SANDBOX_CONTRACT["pull"] == "never"
    assert evidence["sandbox_contract_sha256"] == sha256_object(SANDBOX_CONTRACT)
    assert evidence["task_count"] == 60 and evidence["execution_count"] == 120
    assert evidence["reference_passes"] == 60 and evidence["known_bad_rejections"] == 60 and evidence["failures"] == []
    assert all("@sha256:" in row["verifier"]["image"] and row["verifier"]["sandbox_contract_sha256"] == evidence["sandbox_contract_sha256"] and not row["verifier"]["timed_out"] for row in evidence["executions"])
