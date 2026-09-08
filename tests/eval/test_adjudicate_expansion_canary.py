import json
from pathlib import Path

from scripts.eval.adjudicate_expansion_canary import adjudicate, canonical_digest


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


def setup(tmp_path: Path, improved: bool) -> tuple[Path, Path, Path, Path]:
    rule = {"minimum_improved_product_families": 4, "minimum_net_pass_gain": 1, "maximum_pass_regression_per_lane": 0, "maximum_increase_in_non_code_outputs": 0, "maximum_increase_in_truncated_outputs": 0, "save_reload_required": True, "rule_id": "expansion-pilot-canary-promotion-v1"}
    card = {"schema_version": "ganesh-mini-expansion-pilot-card/v1", "status": "ready", "failed_checks": [], "evaluation": {"canary_tasks": 30, "promotion_rule": rule}}
    card["card_sha256"] = canonical_digest(card)
    card_path = tmp_path / "card.json"; card_path.write_text(json.dumps(card))
    terminal = {"status": "passed", "card_sha256": card["card_sha256"]}; terminal["report_sha256"] = canonical_digest(terminal)
    terminal_path = tmp_path / "terminal.json"; terminal_path.write_text(json.dumps(terminal))
    base, candidate = tmp_path / "base", tmp_path / "candidate"
    lanes = ("go", "java", "javascript", "typescript", "python", "rust")
    for index in range(30):
        lane = lanes[index % 6]; task_id = f"task-{index:02d}"
        task(base / f"{task_id}.json", task_id, lane, False)
        candidate_pass = improved and lane != "typescript"
        task(candidate / f"{task_id}.json", task_id, lane, candidate_pass)
    return card_path, terminal_path, base, candidate


def test_canary_promotes_only_on_frozen_multifamily_gain(tmp_path: Path) -> None:
    report = adjudicate(*setup(tmp_path, True))
    assert report["status"] == "promote-to-full-development"
    assert report["failed_checks"] == []


def test_canary_rejects_no_gain(tmp_path: Path) -> None:
    report = adjudicate(*setup(tmp_path, False))
    assert report["status"] == "do-not-promote"
    assert "net_pass_gain" in report["failed_checks"]
