from __future__ import annotations

import json
import subprocess
from unittest.mock import patch

from scripts.eval.authoring.run_native_directionality import native_host


def completed(value: dict) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], 0, json.dumps(value), "")


@patch("scripts.eval.authoring.run_native_directionality.platform.release", return_value="test-kernel")
@patch("scripts.eval.authoring.run_native_directionality.platform.machine", return_value="x86_64")
@patch("scripts.eval.authoring.run_native_directionality.platform.system", return_value="Linux")
@patch("scripts.eval.authoring.run_native_directionality.checked")
def test_native_host_uses_portable_docker_json(
    checked, _system, _machine, _release,
) -> None:
    checked.side_effect = [
        completed({"Os": "linux", "Arch": "amd64", "Version": "test"}),
        completed({"OSType": "linux", "Architecture": "x86_64", "Driver": "overlay2", "DockerRootDir": "/var/lib/docker"}),
    ]
    value = native_host()
    assert value["docker_server"]["Arch"] == "amd64"
    assert value["docker_info"] == {
        "OSType": "linux", "Architecture": "x86_64",
        "Driver": "overlay2", "DockerRootDir": "/var/lib/docker",
    }
    assert checked.call_args_list[1].args[0] == ["docker", "info", "--format", "{{json .}}"]
