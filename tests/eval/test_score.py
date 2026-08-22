from __future__ import annotations

import copy
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.eval.contracts import ContractError, load_json, sha256_object, sha256_text, validate_task
from scripts.eval.run_task import build_result
from scripts.eval.score import compare
from scripts.verify.sandbox import SANDBOX_CONTRACT


ZERO = "0" * 64


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
    def test_javascript_and_typescript_are_half_weighted_in_five_family_macro(self) -> None:
        base = [result_for(language, False, "base") for language in ("go", "java", "javascript", "typescript", "python", "rust")]
        candidate = [result_for(language, language == "javascript", "candidate") for language in ("go", "java", "javascript", "typescript", "python", "rust")]
        report = compare(base, candidate)
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


if __name__ == "__main__":
    unittest.main()
