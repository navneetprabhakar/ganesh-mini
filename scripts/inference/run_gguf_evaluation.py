#!/usr/bin/env python3
"""Run a sealed GGUF artifact through the production evaluation harness."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import socket
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from scripts.eval.contracts import load_json, sha256_object
from scripts.inference.run_evaluation import execute, file_sha256


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_KEYS = ("gguf_f16", "gguf_q8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def load_artifact(manifest_path: Path, key: str) -> tuple[dict[str, Any], Path]:
    manifest = load_json(manifest_path)
    unsigned = dict(manifest)
    claimed = unsigned.pop("manifest_sha256", None)
    if (
        claimed != canonical_sha256(unsigned)
        or manifest.get("schema_version") != "ganesh-mini-release-artifacts/v1"
        or manifest.get("status") != "built"
        or manifest.get("model_name") != "ganesh-mini-1.0"
    ):
        raise ValueError("invalid release artifact manifest")
    artifact = manifest.get("artifacts", {}).get(key)
    if not isinstance(artifact, dict):
        raise ValueError(f"release artifact manifest has no {key}")
    path = Path(artifact.get("path", ""))
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file() or file_sha256(path) != artifact.get("sha256"):
        raise ValueError(f"{key} file does not match the release artifact manifest")
    return manifest, path


def free_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handle:
        handle.bind(("127.0.0.1", 0))
        return int(handle.getsockname()[1])


def metal_device_name(server: Path) -> str:
    listed = subprocess.run(
        [str(server), "--list-devices"], check=True, capture_output=True, text=True,
    ).stdout
    match = re.search(r"^\s*(MTL\d+):", listed, re.MULTILINE)
    if match is None:
        raise RuntimeError("llama-server did not expose a Metal device")
    return match.group(1)


class LlamaCppServerBackend:
    """BatchBackend implementation backed by one pinned local llama-server."""

    def __init__(
        self,
        *,
        server: Path,
        model: Path,
        llama_revision: str,
        device: str,
        parallel: int,
        context_length: int,
        log_path: Path,
        startup_timeout_seconds: int,
    ) -> None:
        if device not in {"cpu", "mps"}:
            raise ValueError("GGUF evaluation device must be cpu or mps")
        if parallel < 1:
            raise ValueError("parallel must be positive")
        self._port = free_loopback_port()
        self._base_url = f"http://127.0.0.1:{self._port}"
        self._log_handle = None
        self._process: subprocess.Popen[bytes] | None = None
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log_handle = log_path.open("wb")
        command = [
            str(server), "--model", str(model), "--host", "127.0.0.1",
            "--port", str(self._port), "--ctx-size", str(context_length),
            "--parallel", str(parallel), "--reasoning", "off",
            "--no-webui", "--log-disable",
        ]
        if device == "cpu":
            command.extend(["--device", "none", "--gpu-layers", "0"])
        else:
            command.extend(["--device", metal_device_name(server), "--gpu-layers", "all"])
        started = time.perf_counter()
        self._process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=self._log_handle,
            stderr=subprocess.STDOUT,
        )
        try:
            self._wait_ready(startup_timeout_seconds)
            props = self._get("/props")
            eos_text = props.get("eos_token")
            if not isinstance(eos_text, str) or not eos_text:
                raise RuntimeError("llama-server did not expose an EOS token")
            eos_tokens = self._post(
                "/tokenize",
                {"content": eos_text, "add_special": False, "parse_special": True},
            ).get("tokens")
            if not isinstance(eos_tokens, list) or len(eos_tokens) != 1:
                raise RuntimeError("llama-server EOS token did not tokenize to one ID")
            self.eos_token_id = int(eos_tokens[0])
            self.load_ms = round((time.perf_counter() - started) * 1000)
            self.identity = {
                "backend": "llama.cpp-server",
                "device": device,
                "llama_cpp_revision": llama_revision,
                "llama_server_sha256": file_sha256(server),
                "model_file_sha256": file_sha256(model),
                "context_length": context_length,
                "parallel": parallel,
                "reasoning": "off",
            }
        except BaseException:
            self.close()
            raise

    def _request(self, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        data = None if payload is None else json.dumps(payload).encode()
        request = urllib.request.Request(
            self._base_url + path,
            data=data,
            headers={"Content-Type": "application/json"} if data is not None else {},
            method="POST" if data is not None else "GET",
        )
        with urllib.request.urlopen(request, timeout=600) as response:
            return json.loads(response.read().decode())

    def _get(self, path: str) -> dict[str, Any]:
        value = self._request(path)
        if not isinstance(value, dict):
            raise RuntimeError(f"llama-server {path} returned a non-object")
        return value

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        value = self._request(path, payload)
        if not isinstance(value, dict):
            raise RuntimeError(f"llama-server {path} returned a non-object")
        return value

    def _wait_ready(self, timeout_seconds: int) -> None:
        deadline = time.monotonic() + timeout_seconds
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            if self._process is not None and self._process.poll() is not None:
                raise RuntimeError(f"llama-server exited during startup: {self._process.returncode}")
            try:
                health = self._get("/health")
                if health.get("status") == "ok":
                    return
            except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
                last_error = error
            time.sleep(0.1)
        raise TimeoutError(f"llama-server did not become ready: {last_error}")

    def render(self, prompt: str) -> tuple[str, list[int]]:
        rendered = self._post(
            "/apply-template",
            {"messages": [{"role": "user", "content": prompt}]},
        ).get("prompt")
        if not isinstance(rendered, str):
            raise RuntimeError("llama-server did not render the chat prompt")
        tokens = self._post(
            "/tokenize",
            {"content": rendered, "add_special": False, "parse_special": True},
        ).get("tokens")
        if not isinstance(tokens, list) or not all(isinstance(token, int) for token in tokens):
            raise RuntimeError("llama-server returned invalid prompt tokens")
        return rendered, tokens

    def generate_batch(
        self,
        input_ids: list[list[int]],
        max_new_tokens: int,
        use_cache: bool,
    ) -> list[tuple[list[int], str, int]]:
        if not use_cache:
            raise ValueError("the frozen GGUF serving contract requires the KV cache")
        started = time.perf_counter()
        payload = {
            "prompt": input_ids[0] if len(input_ids) == 1 else input_ids,
            "n_predict": max_new_tokens,
            "temperature": 0.0,
            "samplers": ["temperature"],
            "seed": 0,
            "stream": False,
            "cache_prompt": False,
            "return_tokens": True,
        }
        raw = self._request("/completion", payload)
        rows = raw if isinstance(raw, list) else [raw]
        if len(rows) != len(input_ids) or not all(isinstance(row, dict) for row in rows):
            raise RuntimeError("llama-server completion cardinality mismatch")
        elapsed = round((time.perf_counter() - started) * 1000)
        result = []
        for row in rows:
            tokens = row.get("tokens")
            if not isinstance(tokens, list) or not all(isinstance(token, int) for token in tokens):
                raise RuntimeError("llama-server did not return generated token IDs")
            if row.get("stop_type") == "eos" and (not tokens or tokens[-1] != self.eos_token_id):
                tokens = [*tokens, self.eos_token_id]
            text = self._post("/detokenize", {"tokens": tokens}).get("content")
            if not isinstance(text, str):
                raise RuntimeError("llama-server did not detokenize generated IDs")
            result.append((tokens, text, elapsed))
        return result

    def close(self) -> None:
        process = self._process
        self._process = None
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
        if self._log_handle is not None:
            self._log_handle.close()
            self._log_handle = None

    def __enter__(self) -> "LlamaCppServerBackend":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--artifact-manifest", type=Path, required=True)
    parser.add_argument("--artifact-key", choices=ARTIFACT_KEYS, required=True)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--device", choices=("cpu", "mps"), required=True)
    parser.add_argument("--llama-cpp", type=Path, default=Path("models/llama.cpp"))
    parser.add_argument("--startup-timeout-seconds", type=int, default=300)
    args = parser.parse_args()

    manifest, model_path = load_artifact(args.artifact_manifest, args.artifact_key)
    llama_root = args.llama_cpp if args.llama_cpp.is_absolute() else ROOT / args.llama_cpp
    server = llama_root / "build/bin/llama-server"
    if not server.is_file():
        raise FileNotFoundError("pinned llama-server is not built")
    observed_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=llama_root, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    expected_revision = manifest.get("llama_cpp", {}).get("revision")
    if observed_revision != expected_revision:
        raise ValueError("llama.cpp revision does not match the artifact manifest")
    config = load_json(args.config)
    artifact = manifest["artifacts"][args.artifact_key]
    model_identity = {
        "model_id": args.model_id,
        "revision": args.model_revision,
        "artifact_sha256": artifact["sha256"],
        "serving_contract_sha256": sha256_object({
            **config["serving"],
            "chat_template_source": "gguf-metadata",
            "runtime": "llama.cpp-server",
            "llama_cpp_revision": observed_revision,
        }),
    }
    parallel = int(config["execution"]["batch_size"])
    log_path = args.output_dir / "llama-server.log"
    with LlamaCppServerBackend(
        server=server,
        model=model_path,
        llama_revision=observed_revision,
        device=args.device,
        parallel=parallel,
        context_length=int(config["serving"]["context_length"]),
        log_path=log_path,
        startup_timeout_seconds=args.startup_timeout_seconds,
    ) as backend:
        execute(
            args.config,
            backend=backend,
            model_override=model_identity,
            artifact_size_override=int(artifact["bytes"]),
            output_dir=args.output_dir,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
