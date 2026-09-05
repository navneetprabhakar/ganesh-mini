import hashlib
import json

import pytest

from scripts.data.prepare_review_partition import main


@pytest.fixture
def campaign(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / 'artifacts/verification/cutoff-5885-vm/remote'
    cutoff = tmp_path / 'datasets/cache/expansion-v1/cutoff-5885'
    source.mkdir(parents=True)
    cutoff.mkdir(parents=True)
    rows = [{'id': 'exp-v1-go-generation-0165'}] + [
        {'id': f'passing-{i}'} for i in range(5882)]
    candidates = rows + [{'id': 'rust-a'}, {'id': 'rust-b'}]
    def encoded(items):
        return ''.join(json.dumps(row) + '\n' for row in items).encode()
    payload, inputs = encoded(rows), encoded(candidates)
    (source / 'final.admitted.jsonl').write_bytes(payload)
    (cutoff / 'final.candidates.jsonl').write_bytes(inputs)
    (source / 'final.admission.json').write_text(json.dumps({
        'output_sha256': hashlib.sha256(payload).hexdigest(),
        'input_sha256': hashlib.sha256(inputs).hexdigest(),
        'rejected': [{'id': id, 'reason': 'timeout'} for id in ['rust-a', 'rust-b']],
    }))
    return source, cutoff, tmp_path / 'datasets/cache/expansion-v1/review-partition-v1'


def test_partition_preserves_originals_and_refuses_overwrite(campaign):
    source, cutoff, output = campaign
    before = (source / 'final.admitted.jsonl').read_bytes()
    main()
    manifest = json.loads((output / 'manifest.json').read_text())
    assert manifest['review_eligible'] == 5882
    assert len((output / 'flagged.candidates.jsonl').read_text().splitlines()) == 3
    assert (source / 'final.admitted.jsonl').read_bytes() == before
    with pytest.raises(ValueError, match='already exists'):
        main()


@pytest.mark.parametrize('target', ['output', 'input'])
def test_tampering_fails_closed(campaign, target):
    source, cutoff, output = campaign
    path = (source / 'final.admitted.jsonl' if target == 'output'
            else cutoff / 'final.candidates.jsonl')
    path.write_bytes(path.read_bytes() + b'\n')
    with pytest.raises(ValueError, match='hash mismatch'):
        main()
    assert not output.exists()
