import json
from pathlib import Path

import pytest

from scripts.inference.run_gguf_evaluation import (
    LlamaCppServerBackend,
    canonical_sha256,
    load_artifact,
    metal_device_name,
)


def test_load_artifact_requires_sealed_matching_file(tmp_path: Path) -> None:
    artifact = tmp_path / "model.gguf"
    artifact.write_bytes(b"gguf")
    import hashlib

    digest = hashlib.sha256(b"gguf").hexdigest()
    manifest = {
        "schema_version": "ganesh-mini-release-artifacts/v1",
        "status": "built",
        "model_name": "ganesh-mini-1.0",
        "artifacts": {"gguf_q8": {"path": str(artifact), "bytes": 4, "sha256": digest}},
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    _, observed = load_artifact(path, "gguf_q8")
    assert observed == artifact
    artifact.write_bytes(b"drift")
    with pytest.raises(ValueError, match="does not match"):
        load_artifact(path, "gguf_q8")


def test_backend_renders_and_generates_with_exact_server_contract() -> None:
    backend = object.__new__(LlamaCppServerBackend)
    backend.eos_token_id = 99
    calls = []

    def post(path: str, payload: dict) -> dict:
        calls.append((path, payload))
        if path == "/apply-template":
            return {"prompt": "rendered"}
        if path == "/tokenize":
            return {"tokens": [1, 2]}
        if path == "/detokenize":
            return {"content": "answer<eos>"}
        raise AssertionError(path)

    backend._post = post
    rendered, input_ids = backend.render("write code")
    assert (rendered, input_ids) == ("rendered", [1, 2])

    backend._request = lambda path, payload: {
        "tokens": [7], "content": "answer", "stop_type": "eos"
    }
    assert backend.generate_batch([[1, 2]], 8, True) == [([7, 99], "answer<eos>", pytest.approx(0, abs=1000))]
    completion = calls[-1]
    assert completion == ("/detokenize", {"tokens": [7, 99]})


def test_backend_rejects_disabled_kv_cache() -> None:
    backend = object.__new__(LlamaCppServerBackend)
    with pytest.raises(ValueError, match="KV cache"):
        backend.generate_batch([[1]], 1, False)


def test_metal_device_name_uses_exposed_llama_cpp_identifier(monkeypatch: pytest.MonkeyPatch) -> None:
    class Result:
        stdout = "Available devices:\n  MTL0: Apple M4 (18186 MiB)\n"

    monkeypatch.setattr(
        "scripts.inference.run_gguf_evaluation.subprocess.run",
        lambda *args, **kwargs: Result(),
    )
    assert metal_device_name(Path("llama-server")) == "MTL0"
