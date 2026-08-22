from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.eval.contracts import load_json
from scripts.verify.sandbox import verify


class SandboxTests(unittest.TestCase):
    @patch("scripts.verify.sandbox._inspect_image", return_value="sha256:" + "1" * 64)
    @patch("scripts.verify.sandbox.subprocess.run")
    def test_docker_contract_is_networkless_limited_and_shell_free(self, run, _inspect) -> None:
        run.return_value = subprocess.CompletedProcess([], 0, "ok", "")
        task = load_json(Path("eval/fixtures/synthetic_harness/python.task.json"))
        evidence = verify(task, task["validation"]["reference"]["code"], Path("configs/eval/runtimes.json"))
        argv = run.call_args.args[0]
        self.assertEqual("docker", argv[0])
        self.assertIn("none", argv)
        self.assertIn("--read-only", argv)
        self.assertIn("--cap-drop", argv)
        self.assertIn("--memory", argv)
        self.assertIn("--cpus", argv)
        self.assertIn("--pids-limit", argv)
        self.assertNotIn("sh", argv)
        self.assertFalse(evidence["timed_out"])
        self.assertEqual([0], evidence["exit_codes"])


if __name__ == "__main__":
    unittest.main()
