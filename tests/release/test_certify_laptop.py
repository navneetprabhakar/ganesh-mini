import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from scripts.release.certify_laptop import canonical_sha256, peak_rss, validate_release_inputs


def test_peak_rss_parses_darwin_and_linux_time_formats() -> None:
    assert peak_rss("  12345  maximum resident set size\n","Darwin")==12345
    assert peak_rss("Maximum resident set size (kbytes): 12345\n","Linux")==12345*1024


def test_laptop_certification_inputs_bind_artifacts_and_llama_build(tmp_path: Path) -> None:
    llama = tmp_path / "llama.cpp"
    llama.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=llama, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=llama, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=llama, check=True)
    cli = llama / "llama-cli"
    cli.write_bytes(b"cli")
    subprocess.run(["git", "add", "llama-cli"], cwd=llama, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=llama, check=True)
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=llama, check=True, capture_output=True, text=True).stdout.strip()
    q8 = tmp_path / "q8.gguf"
    f16 = tmp_path / "f16.gguf"
    q8.write_bytes(b"q8")
    f16.write_bytes(b"f16")
    manifest = {
        "schema_version": "ganesh-mini-release-artifacts/v1",
        "status": "built",
        "model_name": "ganesh-mini-1.0",
        "llama_cpp": {
            "revision": revision,
            "llama_cli_sha256": hashlib.sha256(cli.read_bytes()).hexdigest(),
        },
        "artifacts": {
            "gguf_q8": {"bytes": q8.stat().st_size, "sha256": hashlib.sha256(q8.read_bytes()).hexdigest()},
            "gguf_f16": {"bytes": f16.stat().st_size, "sha256": hashlib.sha256(f16.read_bytes()).hexdigest()},
        },
    }
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest))

    observed, observed_revision = validate_release_inputs(path, llama, cli, q8, f16)
    assert observed["manifest_sha256"] == manifest["manifest_sha256"]
    assert observed_revision == revision

    cli.write_bytes(b"drift")
    with pytest.raises(ValueError, match="pinned llama.cpp"):
        validate_release_inputs(path, llama, cli, q8, f16)
