import json
from pathlib import Path

from scripts.eval.adjudicate_expansion_canary import canonical_digest
from scripts.eval.summarize_checkpoint_sweep import build


def write_sealed(path: Path, value: dict, field: str) -> None:
    value[field] = canonical_digest(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def task(path: Path, task_id: str, lane: str, passed: bool) -> None:
    write_sealed(path, {
        "task": {"task_id": task_id, "language": lane},
        "generation": {"stopped_at_eos": True},
        "parameters": {"output_tokens": 10, "max_new_tokens": 100},
        "extraction": {"extracted_code": "code"},
        "verification": {"result": {"passed": passed}},
    }, "evidence_sha256")


def test_summarizes_all_checkpoints_without_promotion_authority(tmp_path: Path) -> None:
    labels = [f"tokens-{index:012d}" for index in range(1, 6)]
    manifest = {
        "status": "diagnostic-only",
        "promotion_authority": "none",
        "training_run_evidence_sha256": "a" * 64,
        "config_sha256": {label: str(index) * 64 for index, label in enumerate(labels, 1)},
        "unmeasured_checkpoint_count": 5,
        "measured_final_checkpoint": "tokens-000000000006",
    }
    write_sealed(tmp_path / "manifest.json", manifest, "manifest_sha256")
    lanes = ("go", "java", "javascript", "typescript", "python", "rust")
    for index, lane in enumerate(lanes):
        task_id = f"task-{index}"
        task(tmp_path / "base" / f"{task_id}.json", task_id, lane, False)
        task(tmp_path / "final" / f"{task_id}.json", task_id, lane, lane == "rust")
        for label in labels:
            task(tmp_path / "results" / label / "tasks" / f"{task_id}.json", task_id, lane, lane in {"go", "java"})

    report = build(tmp_path / "manifest.json", tmp_path / "base", tmp_path / "results", tmp_path / "final")

    assert report["status"] == "complete-diagnostic"
    assert report["promotion_authority"] == "none"
    assert len(report["checkpoints"]) == 6
    assert report["maximum_improved_product_families"] == 2
