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

    @patch("scripts.verify.sandbox._inspect_image", return_value="sha256:" + "1" * 64)
    @patch("scripts.verify.sandbox.subprocess.run")
    def test_timeout_normalizes_bytes_output_and_fails_closed(self, run, _inspect) -> None:
        run.side_effect = subprocess.TimeoutExpired(
            cmd=["docker", "run"], timeout=1, output=b"partial \xff", stderr=b"timed out \xfe"
        )
        task = load_json(Path("eval/fixtures/synthetic_harness/python.task.json"))
        evidence = verify(task, task["validation"]["reference"]["code"], Path("configs/eval/runtimes.json"))
        self.assertTrue(evidence["timed_out"])
        self.assertEqual([], evidence["exit_codes"])
        self.assertEqual("partial \ufffd", evidence["stdout"])
        self.assertEqual("timed out \ufffd", evidence["stderr"])


if __name__ == "__main__":
    unittest.main()
