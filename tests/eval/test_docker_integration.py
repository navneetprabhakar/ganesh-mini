from __future__ import annotations

import os
import unittest
from pathlib import Path

from scripts.eval.contracts import load_json, validate_task
from scripts.verify.sandbox import verify


@unittest.skipUnless(os.environ.get("GANESH_RUN_DOCKER_TESTS") == "1", "set GANESH_RUN_DOCKER_TESTS=1")
class DockerIntegrationTests(unittest.TestCase):
    def test_reference_passes_and_known_bad_fails_for_all_six_lanes(self) -> None:
        for task_path in sorted(Path("eval/fixtures/synthetic_harness").glob("*.task.json")):
            with self.subTest(task=task_path.name):
                task = validate_task(load_json(task_path))
                reference = verify(task, task["validation"]["reference"]["code"], Path("configs/eval/runtimes.json"))
                known_bad = verify(task, task["validation"]["known_bad"][0]["code"], Path("configs/eval/runtimes.json"))
                self.assertFalse(reference["timed_out"])
                self.assertEqual(len(reference["commands"]), len(reference["exit_codes"]))
                self.assertTrue(all(code == 0 for code in reference["exit_codes"]), reference)
                self.assertFalse(all(code == 0 for code in known_bad["exit_codes"]), known_bad)


if __name__ == "__main__":
    unittest.main()
