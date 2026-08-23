from __future__ import annotations

import subprocess
import unittest
import json
from pathlib import Path
from unittest.mock import patch

from scripts.eval.contracts import load_json
from scripts.eval.contracts import ContractError
from scripts.verify.sandbox import _inspect_image, verify


class SandboxTests(unittest.TestCase):
    @patch("scripts.verify.sandbox.subprocess.run")
    def test_image_identity_accepts_containerd_and_classic_stores(self, run) -> None:
        config = "sha256:" + "a" * 64
        manifest = "sha256:" + "b" * 64
        layers = ["sha256:" + "c" * 64]
        base = {"Os": "linux", "Architecture": "amd64", "RootFS": {"Layers": layers}}
        containerd = dict(base, Id=manifest, Descriptor={"digest": manifest, "annotations": {"config.digest": config}})
        run.return_value = subprocess.CompletedProcess([], 0, json.dumps(containerd), "")
        self.assertEqual(config, _inspect_image("tag", config, manifest, layers, "linux/amd64"))
        classic = dict(base, Id=config)
        run.return_value = subprocess.CompletedProcess([], 0, json.dumps(classic), "")
        self.assertEqual(config, _inspect_image("tag", config, manifest, layers, "linux/amd64"))

    @patch("scripts.verify.sandbox.subprocess.run")
    def test_image_identity_rejects_layer_drift(self, run) -> None:
        config = "sha256:" + "a" * 64
        manifest = "sha256:" + "b" * 64
        inspected = {"Id": config, "Os": "linux", "Architecture": "amd64", "RootFS": {"Layers": []}}
        run.return_value = subprocess.CompletedProcess([], 0, json.dumps(inspected), "")
        with self.assertRaisesRegex(ContractError, "rootfs layers"):
            _inspect_image("tag", config, manifest, ["sha256:" + "c" * 64], "linux/amd64")

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
