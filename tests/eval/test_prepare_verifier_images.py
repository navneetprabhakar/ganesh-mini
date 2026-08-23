from __future__ import annotations

import json
import subprocess
import tarfile
import hashlib
from io import BytesIO
from pathlib import Path

import pytest

from scripts.eval.prepare_verifier_images import IMAGE_SPECS, inspect_image, runtime_config, verify_saved_archive


def completed(value: object) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], 0, json.dumps(value), "")


def test_inspect_image_requires_linux_amd64_and_exact_id_shape() -> None:
    value = [{"Id": "sha256:" + "a" * 64, "Os": "linux", "Architecture": "amd64", "Size": 12, "RootFS": {"Layers": []}, "Config": {"Labels": {}}}]
    assert inspect_image("tag", lambda *_args, **_kwargs: completed(value))["image_id"] == value[0]["Id"]
    value[0]["Architecture"] = "arm64"
    with pytest.raises(RuntimeError, match="Linux/AMD64"):
        inspect_image("tag", lambda *_args, **_kwargs: completed(value))


def test_runtime_config_separates_resolvable_tag_from_exact_image_id() -> None:
    images = {
        runtime_id: {"tag": f"ganesh-mini-{slug}-verify:amd64-v1", "image_id": "sha256:" + str(index) * 64}
        for index, (runtime_id, (_language, slug, _probe)) in enumerate(IMAGE_SPECS.items(), 1)
    }
    config = runtime_config(images)
    assert config["schema_version"] == "2.0" and config["platform"] == "linux/amd64"
    assert len(config["runtimes"]) == 6
    for runtime in config["runtimes"].values():
        assert runtime["image"].endswith(":amd64-v1")
        assert runtime["image_id"].startswith("sha256:")
        assert runtime["platform"] == "linux/amd64"


def test_saved_archive_binds_tag_to_exact_config_and_layers(tmp_path: Path) -> None:
    descriptor_payload = b'{"schemaVersion":2}'
    image_id = "sha256:" + hashlib.sha256(descriptor_payload).hexdigest()
    images = {"python": {"tag": "ganesh-mini-python-verify:amd64-v1", "image_id": image_id}}
    rows = [{"Config": "blobs/sha256/config", "RepoTags": [images["python"]["tag"]], "Layers": ["blobs/sha256/layer"]}]
    index = {"manifests": [{"digest": image_id, "annotations": {"io.containerd.image.name": "docker.io/library/" + images["python"]["tag"]}}]}
    archive = tmp_path / "images.tar"
    with tarfile.open(archive, "w") as bundle:
        values = (
            ("manifest.json", json.dumps(rows).encode()), ("index.json", json.dumps(index).encode()),
            ("blobs/sha256/" + image_id.removeprefix("sha256:"), descriptor_payload),
            ("blobs/sha256/config", b"{}"), ("blobs/sha256/layer", b"layer"),
        )
        for name, payload in values:
            info = tarfile.TarInfo(name)
            info.size = len(payload)
            bundle.addfile(info, BytesIO(payload))
    assert verify_saved_archive(archive, images)["image_count"] == 1
