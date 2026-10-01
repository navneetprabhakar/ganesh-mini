from pathlib import Path

from scripts.data.resume_capability_scale_usage_failures import (
    is_usage_limit_without_draft, load_original,
)


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "measurement/gate3/capability-scale-v1"


def test_usage_failure_requires_no_completed_draft() -> None:
    failure = {"status": "invocation-failed", "failure": {
        "events": [{"type": "turn.failed", "error": {"message": "You've hit your usage limit"}}],
        "final_output": "", "usage": None,
    }}
    assert is_usage_limit_without_draft(failure)
    failure["failure"]["final_output"] = '{"items": []}'
    assert not is_usage_limit_without_draft(failure)


def test_original_381_153_census_is_sealed() -> None:
    import json
    from scripts.data.generate_expansion_qualification import verify_codex_version

    config = json.loads((ROOT / "configs/data/expansion_teacher.json").read_text())
    cli_identity = verify_codex_version("codex", config["codex_cli_version"])
    rows, artifacts, report = load_original(
        BASE / "source-queue.jsonl", BASE / "source-queue-manifest.json",
        BASE / "canary-v1/teacher/teacher-report.json",
        BASE / "first-pass-v2/teacher/teacher-report.json",
        BASE / "first-pass-v2/teacher/candidates.jsonl",
        BASE / "first-pass-v2/teacher-runs", config, cli_identity,
    )
    assert len(rows) == len(artifacts) == 534
    assert sum(item["status"] == "generated" for item in artifacts) == 381
    assert sum(item["status"] == "invocation-failed" for item in artifacts) == 153
    assert report["status"] == "failed"
