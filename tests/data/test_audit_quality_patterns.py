import pytest

from scripts.data import audit_quality_patterns as audit


def candidate(identifier='x', code='', lane='typescript', transformation='draft'):
    return {'id': identifier, 'lane': lane, 'task_type': 'generation',
            'source': {'dataset': 'source', 'transformation': transformation},
            'verification_task': {'validation': {'reference': {'code': code}}}}


def test_patterns_are_inventory_not_approval():
    row = candidate(code='rows.every(valid); listeners.indexOf(listener)')
    assert len(audit.hits(row)) == 2
    assert audit.hits(candidate(code='return 1')) == []
    assert audit.stratum(candidate(transformation='reference corrected against independent tests'))[-1] == 'corrected'


def test_reopens_whole_stratum_and_preserves_uninspected_status(monkeypatch):
    monkeypatch.setattr(audit, 'GROUPS', {'finding': ['x']})
    rows = [candidate('x'), candidate('y'), candidate('z', lane='rust')]
    review = {'records': [dict(zip(audit.KEYS, audit.stratum(rows[0])), id='x')]}
    result = audit.build(rows, review)
    assert result['reopened_population'] == 2
    assert result['reopened_strata_count'] == 1
    assert [r['id'] for r in result['records']] == ['x', 'y']
    assert result['records'][0]['semantically_inspected_in_frozen_sample']
    assert not result['records'][1]['semantically_inspected_in_frozen_sample']
    assert result['status'] == 'requires-stratum-resolution-not-training-ready'


def test_requires_sample_bound_findings(monkeypatch):
    monkeypatch.setattr(audit, 'GROUPS', {'finding': ['missing']})
    with pytest.raises(ValueError, match='bind to frozen sample'):
        audit.build([candidate()], {'records': []})


def test_detects_inconsistent_sample_stratum(monkeypatch):
    monkeypatch.setattr(audit, 'GROUPS', {'finding': ['x']})
    row = candidate()
    sampled = dict(zip(audit.KEYS, audit.stratum(row)), id='x')
    sampled['rejection_history'] = 'corrected'
    with pytest.raises(ValueError, match='stratum mismatch'):
        audit.build([row], {'records': [sampled]})
