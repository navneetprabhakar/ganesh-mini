from __future__ import annotations

import base64
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.eval.contracts import load_json
from scripts.eval.contracts import ContractError
from scripts.verify.sandbox import _inspect_image, infrastructure_failure, verify


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
        self.assertIn("--name", argv)
        self.assertTrue(argv[argv.index("--name") + 1].startswith("ganesh-verifier-"))
        self.assertIn("GOMAXPROCS=1", argv)
        self.assertIn("GOFLAGS=-p=1", argv)
        self.assertIn("CARGO_BUILD_JOBS=1", argv)
        self.assertNotIn("sh", argv)
        self.assertFalse(evidence["timed_out"])
        self.assertEqual([0], evidence["exit_codes"])

    @patch("scripts.verify.sandbox._inspect_image", return_value="sha256:" + "1" * 64)
    @patch("scripts.verify.sandbox.subprocess.run")
    def test_timeout_normalizes_bytes_output_and_fails_closed(self, run, _inspect) -> None:
        run.side_effect = [
            subprocess.TimeoutExpired(
                cmd=["docker", "run"], timeout=1, output=b"partial \xff", stderr=b"timed out \xfe"
            ),
            subprocess.CompletedProcess([], 0, "container-id", ""),
        ]
        task = load_json(Path("eval/fixtures/synthetic_harness/python.task.json"))
        evidence = verify(task, task["validation"]["reference"]["code"], Path("configs/eval/runtimes.json"))
        self.assertTrue(evidence["timed_out"])
        self.assertEqual([], evidence["exit_codes"])
        self.assertEqual("base64:" + base64.b64encode(b"partial \xff").decode(), evidence["stdout"])
        self.assertEqual("base64:" + base64.b64encode(b"timed out \xfe").decode(), evidence["stderr"])
        cleanup = run.call_args_list[1].args[0]
        self.assertEqual(["docker", "rm", "--force"], cleanup[:3])
        self.assertEqual(run.call_args_list[0].args[0][run.call_args_list[0].args[0].index("--name") + 1], cleanup[3])

    @patch("scripts.verify.sandbox._inspect_image", return_value="sha256:" + "1" * 64)
    @patch("scripts.verify.sandbox.subprocess.run")
    def test_completed_process_preserves_non_utf8_output(self, run, _inspect) -> None:
        run.return_value = subprocess.CompletedProcess([], 1, b"output \x81", b"error \xfe")
        task = load_json(Path("eval/fixtures/synthetic_harness/python.task.json"))
        evidence = verify(task, task["validation"]["reference"]["code"], Path("configs/eval/runtimes.json"))
        self.assertEqual("base64:" + base64.b64encode(b"output \x81").decode(), evidence["stdout"])
        self.assertEqual("base64:" + base64.b64encode(b"error \xfe").decode(), evidence["stderr"])
        self.assertEqual([1], evidence["exit_codes"])

    def test_resource_exhaustion_is_an_infrastructure_failure(self) -> None:
        verifier = {
            "exit_codes": [1], "timed_out": False,
            "stderr": "compile: fork/exec tool: resource temporarily unavailable",
        }
        self.assertIn("resource temporarily unavailable", infrastructure_failure(verifier) or "")

    def test_normal_compile_failure_is_not_an_infrastructure_failure(self) -> None:
        verifier = {"exit_codes": [1], "timed_out": False, "stderr": "solution.go: undefined: missing"}
        self.assertIsNone(infrastructure_failure(verifier))

    def test_known_bad_sigabrt_is_behavioral_evidence_not_infrastructure(self) -> None:
        verifier = {
            "exit_codes": [0, 134], "timed_out": False,
            "stderr": "unsafe precondition violated; thread caused non-unwinding panic. aborting.",
        }
        self.assertIsNone(infrastructure_failure(verifier))

    def test_docker_reserved_exit_codes_are_infrastructure_failures(self) -> None:
        for code in (125, 126, 127):
            verifier = {"exit_codes": [code], "timed_out": False, "stderr": ""}
            self.assertIn("container runtime exit code", infrastructure_failure(verifier) or "")


if __name__ == "__main__":
    unittest.main()
