import gzip
import json

from scripts.benchmarks.serve_public_progress import summarize


def test_progress_counts_only_public_artifact_files(tmp_path) -> None:
    run = tmp_path / "full-humaneval-v1-candidate-js"
    (run / "raw").mkdir(parents=True)
    (run / "completions").mkdir()
    (run / "verified").mkdir()
    (run / "raw" / "HumanEval_0.json").write_text('{"secret":"not exposed"}')
    (run / "completions" / "HumanEval_0.json.gz").write_bytes(b"test")
    with gzip.open(run / "verified" / "HumanEval_0.results.json.gz", "wt") as stream:
        json.dump({"name": "HumanEval_0", "results": [{"status": "OK"}]}, stream)
    (run / "manifest.json").write_text(json.dumps({"status": "in_progress", "task_count": 161}))
    result = summarize(tmp_path, "full-humaneval-v1", True)
    assert result["status"] == "running"
    assert result["generated"] == 1
    assert result["verified"] == 1
    assert result["passed"] == 1
    assert result["lanes"][0]["sides"]["candidate"]["passed"] == 1
    assert result["lanes"][0]["sides"]["candidate"]["pass_count_final"] is False
    assert result["expected"] == 1904
    assert result["current_stage"] == "Generating JavaScript · candidate"
    assert "secret" not in json.dumps(result)


def test_progress_marks_stopped_controller_without_claiming_failure(tmp_path) -> None:
    result = summarize(tmp_path, "full-humaneval-v1", False)
    assert result["status"] == "stopped"
    assert result["current_stage"].startswith("Controller stopped")


def test_incomplete_verifier_file_is_not_counted_as_pass(tmp_path) -> None:
    run = tmp_path / "full-humaneval-v1-candidate-js"
    (run / "verified").mkdir(parents=True)
    (run / "verified" / "HumanEval_0.results.json.gz").write_bytes(b"partial")
    result = summarize(tmp_path, "full-humaneval-v1", True)
    assert result["verified"] == 0
    assert result["passed"] == 0
    assert result["lanes"][0]["sides"]["candidate"]["passed"] is None
