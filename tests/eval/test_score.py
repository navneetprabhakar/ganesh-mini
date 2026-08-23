from __future__ import annotations

import copy
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.eval.contracts import ContractError, load_json, sha256_object, sha256_text, validate_task
from scripts.eval.run_task import build_result
from scripts.eval.score import compare, load_results
from scripts.verify.sandbox import SANDBOX_CONTRACT


ZERO = "0" * 64


def assert_comparison_contract(test: unittest.TestCase, report: dict) -> None:
    """Check the frozen comparison schema without adding a runtime dependency."""
    schema = load_json(Path("schemas/eval/comparison.schema.json"))
    test.assertEqual(set(schema["required"]), set(report))
    test.assertEqual(schema["properties"]["schema_version"]["const"], report["schema_version"])

    cohort_keys = set(schema["$defs"]["cohort"]["required"])
    for cohort_name in ("base", "candidate"):
        test.assertEqual(cohort_keys, set(report[cohort_name]))

    paired_keys = set(schema["properties"]["paired"]["required"])
    test.assertEqual(paired_keys, set(report["paired"]))
    lane_keys = set(schema["properties"]["paired"]["properties"]["lanes"]["required"])
    test.assertEqual(lane_keys, set(report["paired"]["lanes"]))

    fraction_keys = set(schema["$defs"]["fraction"]["required"])
    for fraction in (
        report["base"]["five_family_macro"],
        report["candidate"]["five_family_macro"],
        report["five_family_macro_delta"],
    ):
        test.assertEqual(fraction_keys, set(fraction))
        test.assertGreaterEqual(fraction["denominator"], 1)


def result_for(language: str, passed: bool, model_id: str) -> dict:
    task = validate_task(load_json(Path(f"eval/fixtures/synthetic_harness/{language}.task.json")))
    code = task["validation"]["reference"]["code"]
    commands = [["synthetic-verifier"]]
    verifier = {
        "runtime_id": task["runtime_id"], "image": "synthetic.invalid/runtime@sha256:" + "1" * 64,
        "image_id": "sha256:" + "1" * 64, "commands": commands,
        "exit_codes": [0 if passed else 1], "timed_out": False,
        "stdout": "", "stdout_sha256": sha256_text(""), "stderr": "", "stderr_sha256": sha256_text(""),
        "duration_ms": 1, "sandbox_contract_sha256": sha256_object(SANDBOX_CONTRACT),
    }
    now = datetime.now(timezone.utc).isoformat()
    return build_result(
        task, code, code, "synthetic-extractor-v1",
        {"model_id": model_id, "revision": "test", "artifact_sha256": ZERO, "serving_contract_sha256": ZERO},
        {"parameters": {"temperature": 0}, "started_at": now, "completed_at": now}, verifier,
    )


class ScoreTests(unittest.TestCase):
    def test_v2_task_evidence_preserves_frozen_source_task_identity(self) -> None:
        source=load_json(Path("measurement/inference/synthetic/qwen3.5-2b-base-v1/tasks/synthetic-python-add.json"))
        source["schema_version"]="ganesh-mini-task-evidence/v2"; source.pop("evidence_sha256")
        source["evidence_sha256"]=sha256_object(source)
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            path=Path(directory)/"task.json"; path.write_text(json.dumps(source))
            result=load_results(path)[0]
        self.assertEqual(source["task"]["task_sha256"],result["_source_task_sha256"])

    def test_javascript_and_typescript_are_half_weighted_in_five_family_macro(self) -> None:
        base = [result_for(language, False, "base") for language in ("go", "java", "javascript", "typescript", "python", "rust")]
        candidate = [result_for(language, language == "javascript", "candidate") for language in ("go", "java", "javascript", "typescript", "python", "rust")]
        report = compare(base, candidate)
        assert_comparison_contract(self, report)
        self.assertEqual("1/2", report["candidate"]["families"]["javascript_typescript"]["fraction"])
        self.assertEqual("1/10", report["candidate"]["five_family_macro"]["fraction"])
        self.assertEqual({"wins": 1, "losses": 0, "ties": 5, "denominator": 6}, report["paired"]["aggregate"])

    def test_pairing_rejects_evidence_mismatch(self) -> None:
        languages = ("go", "java", "javascript", "typescript", "python", "rust")
        base = [result_for(language, False, "base") for language in languages]
        candidate = [result_for(language, True, "candidate") for language in languages]
        candidate[0] = copy.deepcopy(candidate[0])
        candidate[0]["task_sha256"] = "f" * 64
        candidate[0]["result_sha256"] = sha256_object({key: value for key, value in candidate[0].items() if key != "result_sha256"})
        with self.assertRaisesRegex(ContractError, "evidence mismatch"):
            compare(base, candidate)

    def test_cross_template_pairing_uses_frozen_source_task_identity(self) -> None:
        languages = ("go", "java", "javascript", "typescript", "python", "rust")
        base = [result_for(language, False, "base") for language in languages]
        candidate = [result_for(language, True, "candidate") for language in languages]
        for base_result,candidate_result in zip(base,candidate):
            source_sha=base_result["task_sha256"]
            base_result["_source_task_sha256"]=source_sha
            candidate_result["_source_task_sha256"]=source_sha
            candidate_result["task_sha256"]="f"*64
        report=compare(base,candidate)
        self.assertEqual({"wins":6,"losses":0,"ties":0,"denominator":6},report["paired"]["aggregate"])


if __name__ == "__main__":
    unittest.main()
