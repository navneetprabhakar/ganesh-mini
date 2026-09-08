import json

import pytest

from scripts.data.prepare_recovery_admission import check_overlap, prior_recoveries
from scripts.data.admit_expansion import canonical_json
from scripts.data.plan_versioned_recovery import digest


def row(id, prompt):
    return {"id": id, "messages": [{"content": prompt}]}


def test_retained_and_selected_overlap_are_not_ignored():
    candidates = [row("new1", "Same prompt"), row("new2", "Other prompt"), row("new3", "Other prompt")]
    results = check_overlap(candidates, [row("original", "same PROMPT")])
    assert results == [{"id": "new1", "overlap_id": "original", "exact": True},
                       {"id": "new3", "overlap_id": "new2", "exact": True}]


def test_disjoint_short_prompts_do_not_fuzzy_collide():
    assert check_overlap([row("new", "Alpha")], [row("old", "Beta")]) == []


def test_prior_admission_is_bound_and_compared(tmp_path):
    registry = tmp_path / "registry"
    batch = registry / "first"
    batch.mkdir(parents=True)
    output = batch / "admitted.jsonl"
    old = row("old-recovery", "Prior recovery prompt")
    data = canonical_json(old) + b"\n"
    output.write_bytes(data)
    report = {"schema_version": "ganesh-mini-expansion-admission/v1", "accepted": 1,
              "output": {"path": str(output.relative_to(tmp_path)), "bytes": len(data), "sha256": digest(data)}}
    report["report_sha256"] = digest(canonical_json(report))
    (batch / "admission.json").write_text(json.dumps(report))
    rows, bindings = prior_recoveries(tmp_path, registry)
    assert rows == [old] and len(bindings) == 1
    assert check_overlap([row("new", "prior RECOVERY prompt")], rows)[0]["overlap_id"] == "old-recovery"
    output.write_bytes(data + b"\n")
    with pytest.raises(ValueError, match="output changed"):
        prior_recoveries(tmp_path, registry)


def test_unsealed_prior_output_fails_closed(tmp_path):
    batch = tmp_path / "batch"
    batch.mkdir()
    (batch / "admitted.jsonl").write_text("")
    with pytest.raises(FileNotFoundError):
        prior_recoveries(tmp_path, tmp_path)
