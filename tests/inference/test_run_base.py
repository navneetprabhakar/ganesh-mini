from __future__ import annotations

import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.eval.contracts import load_json, sha256_object
from scripts.inference.run_base import completed_evidence, run_task, validate_config


class FakeBackend:
    load_ms = 7
    identity = {"backend": "fake-test-only"}
    eos_token_id = 248046

    def render(self, prompt: str) -> tuple[str, list[int]]:
        rendered = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
        return rendered, list(rendered.encode())

    def generate(self, input_ids: list[int], max_new_tokens: int, use_cache: bool):
        del input_ids, max_new_tokens, use_cache
        return [1, 2, 3], "```python\ndef add(a: int, b: int) -> int:\n    return a + b\n```<|im_end|>", 3


class RunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[2]
        self.config = load_json(self.root / "configs/inference/qwen_base_synthetic.json")

    def test_checked_in_config_is_fail_closed(self) -> None:
        validate_config(self.config)
        altered = dict(self.config)
        altered["classification"] = "development"
        with self.assertRaisesRegex(ValueError, "synthetic"):
            validate_config(altered)

    @patch("scripts.inference.run_base.verify")
    def test_task_evidence_is_sealed_and_resume_validated(self, mocked_verify) -> None:
        fixture = self.root / "eval/fixtures/synthetic_harness/python.task.json"
        task = load_json(fixture)
        mocked_verify.return_value = {
            "runtime_id": task["runtime_id"],
            "image": "example.invalid/python@sha256:" + "a" * 64,
            "image_id": "sha256:" + "b" * 64,
            "commands": [["python", "test_solution.py"]], "exit_codes": [0], "timed_out": False,
            "stdout": "", "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "stderr": "", "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "duration_ms": 1, "sandbox_contract_sha256": "c" * 64,
        }
        config_sha = sha256_object(self.config)
        model = {
            "model_id": "Qwen/Qwen3.5-2B", "revision": "pinned", "artifact_sha256": "d" * 64,
            "serving_contract_sha256": "e" * 64, "inventory_sha256": "f" * 64,
        }
        evidence = run_task(
            task_path=fixture, task=task, config=self.config, config_sha256=config_sha,
            model=model, backend=FakeBackend(), runtimes=self.root / "configs/eval/runtimes.json",
        )
        self.assertEqual("synthetic_harness_non_benchmark", evidence["classification"])
        self.assertNotEqual(task["rendered_prompt"]["sha256"], evidence["prompt"]["rendered_sha256"])
        target = self.root / "measurement/inference/synthetic/.unit-resume.json"
        try:
            from scripts.inference.run_base import atomic_json
            atomic_json(target, evidence)
            loaded = completed_evidence(target, sha256_object(task), config_sha)
            self.assertEqual(evidence["evidence_sha256"], loaded["evidence_sha256"])
        finally:
            target.unlink(missing_ok=True)
            parent = target.parent
            if parent.exists() and not any(parent.iterdir()):
                shutil.rmtree(parent)


if __name__ == "__main__":
    unittest.main()
