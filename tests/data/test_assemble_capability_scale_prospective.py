from __future__ import annotations

from argparse import Namespace
from pathlib import Path

import pytest

from scripts.data.assemble_capability_scale_provisional import assemble
from scripts.data.run_capability_scale_teacher import load_queue


ROOT = Path(__file__).resolve().parents[2]
SCALE = ROOT / "measurement/gate3/capability-scale-v1"
PROSPECTIVE = SCALE / "prospective-replacement-v1"


def _args(with_replacement: bool) -> Namespace:
    return Namespace(
        training_entry_manifest=ROOT / "measurement/gate3/training-entry-v1/manifest.json",
        canary_dir=SCALE / "canary-final",
        first_pass_root=SCALE / "first-pass-v2",
        prospective_queue=PROSPECTIVE / "queue.jsonl" if with_replacement else None,
        prospective_manifest=PROSPECTIVE / "manifest.json" if with_replacement else None,
        prospective_dir=PROSPECTIVE if with_replacement else None,
    )


def test_old_assembly_remains_failed() -> None:
    with pytest.raises(ValueError, match="546 candidate-unique"):
        assemble(_args(False))


def test_prospective_assembly_has_exact_unique_546() -> None:
    rows, report = assemble(_args(True))
    assert report["schema_version"] == "ganesh-mini-gate3-scale-provisional-assembly/v2"
    assert report["records"] == report["unique_record_ids"] == report["unique_source_identities"] == 546
    assert report["reserves"] == 15
    assert report["prospective_replacements"] == 1
    assert sum(report["cell_counts"].values()) == 546
    assert len(rows) == 546


def test_teacher_loader_accepts_only_sealed_one_row_queue() -> None:
    rows = load_queue(PROSPECTIVE / "queue.jsonl", PROSPECTIVE / "manifest.json")
    assert len(rows) == 1
    assert rows[0]["cohort"] == "prospective_replacement"
