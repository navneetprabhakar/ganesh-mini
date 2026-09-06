import hashlib
import json
import sys

import pytest

from scripts.data import run_review_probe


@pytest.mark.parametrize('lane,test_path', [('go', 'solution_test.go'), ('java', 'SolutionTest.java'),
                                         ('javascript', 'solution.test.js'), ('python', 'test_solution.py'),
                                         ('rust', 'solution_test.rs'), ('typescript', 'solution.test.ts')])
def test_probe_preserves_original_and_uses_verifier(tmp_path, monkeypatch, lane, test_path):
    monkeypatch.chdir(tmp_path)
    root = tmp_path / 'datasets/cache/expansion-v1/cutoff-5885'
    root.mkdir(parents=True)
    original = {'surface': 'training_admission', 'files': [
        {'path': test_path, 'role': 'test', 'content': 'original'}],
        'validation': {'reference': {'code': 'reference'}}}
    row = {'id': 'x', 'lane': lane, 'verification_task': original}
    sample = root / 'quality-sample.candidates.jsonl'
    sample.write_text(json.dumps(row) + '\n')
    (root / 'manifest.json').write_text(json.dumps({'files': {sample.name: {
        'sha256': hashlib.sha256(sample.read_bytes()).hexdigest()}}}))
    runtime = tmp_path / 'configs/eval/runtimes.json'
    runtime.parent.mkdir(parents=True)
    runtime.write_text('{}')
    probe = tmp_path / 'probe'
    probe.write_text('diagnostic')
    output = tmp_path / 'result.json'
    calls = []

    def verify(task, code, config):
        calls.append((task, code, config))
        return {'exit_codes': [1], 'timed_out': False}

    monkeypatch.setattr(run_review_probe, 'verify', verify)
    monkeypatch.setattr(sys, 'argv', ['probe', '--id', 'x', '--probe', str(probe), '--output', str(output)])
    run_review_probe.main()
    result = json.loads(output.read_text())
    assert result['original_task'] == original
    assert len(calls) == 1 and calls[0][1] == 'reference'
    assert result['task']['surface'] == 'synthetic_harness'
    assert result['task']['files'][-1]['content'] == 'diagnostic'
    assert len(result['task']['files']) == (2 if lane == 'go' else 1)
    assert json.loads(sample.read_text()) == row
    before = output.read_bytes()
    with pytest.raises(ValueError, match='preserve existing evidence'):
        run_review_probe.main()
    assert output.read_bytes() == before
