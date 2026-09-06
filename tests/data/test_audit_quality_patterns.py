import hashlib
import json

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


def test_followup_reopens_without_changing_sample_count(monkeypatch):
    monkeypatch.setattr(audit, 'GROUPS', {})
    row = candidate()
    followup = {'new': [{'id': 'x', 'candidate_sha256': hashlib.sha256(audit.canonical_json(row)).hexdigest()}]}
    result = audit.build([row, candidate('y')], {'records': []}, followup)
    assert result['sample_inspected'] == 0
    assert result['reopened_population'] == 2
    assert not any(r['semantically_inspected_in_frozen_sample'] for r in result['records'])
    followup['new'][0]['candidate_sha256'] = 'wrong'
    with pytest.raises(ValueError, match='candidate hash mismatch'):
        audit.build([row], {'records': []}, followup)


@pytest.mark.parametrize('codes,timed_out,valid', [([0, 0, 1], False, True),
                                                  ([0, 1], True, False),
                                                  ([1, 1], False, False),
                                                  ([0], False, False)])
def test_followup_diagnostic_binding(tmp_path, codes, timed_out, valid):
    row = candidate()
    result = {'id': 'x', 'candidate_sha256': hashlib.sha256(audit.canonical_json(row)).hexdigest(),
              'original_task': row['verification_task'],
              'result': {'exit_codes': codes, 'timed_out': timed_out}}
    evidence = tmp_path / 'evidence.json'
    evidence.write_text(json.dumps(result))
    path = tmp_path / 'groups.json'
    path.write_text(json.dumps({'groups': {'new': [{'id': 'x', 'evidence': str(evidence)}]}}))
    if valid:
        bound = audit.load_followup_groups(path, [row])
        assert bound['new'][0]['evidence_sha256'] == hashlib.sha256(evidence.read_bytes()).hexdigest()
        result['id'] = 'different'
        evidence.write_text(json.dumps(result))
        with pytest.raises(ValueError, match='candidate mismatch'):
            audit.load_followup_groups(path, [row])
    else:
        with pytest.raises(ValueError, match='behavioral failure'):
            audit.load_followup_groups(path, [row])
