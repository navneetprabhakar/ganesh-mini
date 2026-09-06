import pytest

from scripts.data.reconcile_sample_criteria import parse_decisions, reconcile


def test_complete_frozen_sample():
    report = reconcile()
    assert report['sample_count'] == 300
    assert report['positive'] + report['held'] == 300
    assert len({r['id'] for r in report['records']}) == 300
    assert report['status'].endswith('not-training-admission')


def test_duplicate_disposition_rejected():
    text = ('## Positive decisions (1)\n| generation-0001 | first |\n'
            '## Held decisions (1)\n| generation-0001 | second |\n')
    with pytest.raises(ValueError, match='duplicate disposition'):
        parse_decisions(text, 'go')


def test_missing_count_rejected():
    with pytest.raises(ValueError, match='counts disagree'):
        parse_decisions('## Positive decisions (2)\n| generation-0001 | basis |\n'
                        '## Held decisions (0)\n', 'go')
