from pathlib import Path

import pytest

from scripts.data import reconcile_cutoff_review as audit


@pytest.fixture
def corpus_available():
    if not Path('datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl').exists():
        pytest.skip('Local immutable cutoff integration fixture is not present')


def test_frozen_coverage_reconciles_without_granting_admission(corpus_available):
    report = audit.reconcile()
    assert report['status'] == 'inspection-coverage-reconciled-not-quality-admission'
    assert report['unique_outside_sample_count'] == 2930
    assert report['sample_in_scope_count'] == 155
    assert report['missing_scope_ids'] == report['outside_scope_ids'] == []
    assert len(report['records']) == 2930
    assert len(report['overlap_ids']) == 5


def test_missing_record_mention_fails_closed(corpus_available, monkeypatch):
    original = Path.read_text

    def read(path, *args, **kwargs):
        text = original(path, *args, **kwargs)
        if path.name == 'JS_TS_RESIDUAL_REVIEW_40.md':
            return text.replace('typescript-generation-0395', 'removed-identifier')
        return text

    monkeypatch.setattr(Path, 'read_text', read)
    with pytest.raises(AssertionError, match='typescript-generation-0395'):
        audit.reconcile()


def test_candidate_hash_change_fails_closed(corpus_available, monkeypatch):
    original = audit.digest
    monkeypatch.setattr(audit, 'digest', lambda path:
                        '0' * 64 if path.name == 'final.candidates.jsonl' else original(path))
    with pytest.raises(AssertionError):
        audit.reconcile()
