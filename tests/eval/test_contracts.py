from __future__ import annotations

import copy
import unittest
from pathlib import Path

from scripts.eval.contracts import ContractError, load_json, validate_task


FIXTURES = Path("eval/fixtures/synthetic_harness")


class TaskContractTests(unittest.TestCase):
    def test_all_six_synthetic_lanes_validate(self) -> None:
        tasks = [load_json(path) for path in sorted(FIXTURES.glob("*.task.json"))]
        self.assertEqual(6, len(tasks))
        self.assertEqual(
            {"go", "java", "javascript", "typescript", "python", "rust"},
            {validate_task(task)["language"] for task in tasks},
        )

    def test_hash_tampering_fails_closed(self) -> None:
        task = load_json(FIXTURES / "python.task.json")
        task["prompt"]["text"] += " tampered"
        with self.assertRaisesRegex(ContractError, "hash mismatch"):
            validate_task(task)

    def test_candidate_overwrite_and_path_escape_fail_closed(self) -> None:
        task = load_json(FIXTURES / "python.task.json")
        overwrite = copy.deepcopy(task)
        overwrite["files"][0]["path"] = "solution.py"
        with self.assertRaisesRegex(ContractError, "overwrite candidate"):
            validate_task(overwrite)
        escaped = copy.deepcopy(task)
        escaped["files"][0]["path"] = "../test_solution.py"
        with self.assertRaisesRegex(ContractError, "remain under"):
            validate_task(escaped)

    def test_language_family_mismatch_fails_closed(self) -> None:
        task = load_json(FIXTURES / "typescript.task.json")
        task["family"] = "python"
        with self.assertRaisesRegex(ContractError, "does not match"):
            validate_task(task)


if __name__ == "__main__":
    unittest.main()
