import hashlib
import tarfile
from pathlib import Path

import pytest

from scripts.inference.build_checkpoint_sweep_recovery import build


def fixture(tmp_path: Path) -> Path:
    terminal = tmp_path / "source"
    (terminal / "output").mkdir(parents=True)
    files = {"exit.txt": b"0\n", "output/result.json": b"{}\n"}
    for relative, data in files.items():
        (terminal / relative).write_bytes(data)
    inventory = "".join(
        f"{hashlib.sha256(data).hexdigest()}  ./{relative}\n"
        for relative, data in sorted(files.items())
    )
    (terminal / "runtime-files.sha256").write_text(inventory)
    return terminal


def test_recovery_archive_is_deterministic_and_terminal_rooted(tmp_path: Path) -> None:
    source = fixture(tmp_path)
    first, second = tmp_path / "first.tar.gz", tmp_path / "second.tar.gz"
    one = build(source, first, tmp_path / "first.json")
    two = build(source, second, tmp_path / "second.json")

    assert first.read_bytes() == second.read_bytes()
    assert one["archive"] == two["archive"]
    assert one["promotion_authority"] == "none"
    with tarfile.open(first, "r:gz") as archive:
        assert set(archive.getnames()) == {
            "terminal",
            "terminal/exit.txt",
            "terminal/output/result.json",
            "terminal/runtime-files.sha256",
        }


def test_recovery_archive_rejects_inventory_mismatch(tmp_path: Path) -> None:
    source = fixture(tmp_path)
    (source / "exit.txt").write_text("1\n")

    with pytest.raises(ValueError, match="identity mismatch"):
        build(source, tmp_path / "bad.tar.gz", tmp_path / "bad.json")
