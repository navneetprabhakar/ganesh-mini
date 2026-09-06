#!/usr/bin/env python3
"""Reconcile frozen cutoff review queues; never grants quality admission."""

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


REVIEW = Path('measurement/data/expansion-v1/cutoff-5885-review')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reconcile(root=REVIEW):
    if not __debug__:
        raise RuntimeError('This audit requires assertions; do not run Python with -O.')
    inputs = {}

    def read(name):
        path = root / name
        inputs[str(path)] = digest(path)
        return json.loads(path.read_text())

    v1 = read('stratum-followup-inventory-v1.json')
    v6 = read('stratum-followup-inventory-v6.json')
    origin = read('test-origin-all300-chains.json')
    holds = read('additional-holds.json')
    frozen = Path('datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl')
    assert digest(frozen) == v6['frozen_inputs']['final.candidates.jsonl']['sha256']
    inputs[str(frozen)] = digest(frozen)
    candidates = [json.loads(line) for line in frozen.read_text().splitlines()]
    candidate_ids = {row['id'] for row in candidates}
    assert len(candidates) == len(candidate_ids) == 5885
    tagged = {r['id'] for r in v1['records'] if r['heuristic_tags']}
    outside = lambda r: not r['semantically_inspected_in_frozen_sample']
    queues = {
        'array': [r['id'] for r in v1['records'] if outside(r) and
                  'js_array_callbacks_require_sparse_scope_review' in r['heuristic_tags']],
        'targeted': [r['id'] for r in v1['records'] if outside(r) and any(
            t != 'js_array_callbacks_require_sparse_scope_review' for t in r['heuristic_tags'])],
    }
    for name, lane, kind in [('rust_generation', 'rust', 'generation'),
                             ('python_generation', 'python', 'generation'),
                             ('python_repair', 'python', 'repair')]:
        queues[name] = [r['id'] for r in v6['records'] if outside(r) and
                        r['stratum']['lane'] == lane and r['stratum']['task_type'] == kind]
    queues['js_ts_residual'] = [r['id'] for r in v6['records'] if outside(r) and
        r['in_reopened_stratum'] and r['stratum']['lane'] in ('javascript', 'typescript')
        and r['id'] not in tagged]
    assert [len(q) for q in queues.values()] == [544, 10, 684, 684, 426, 587]
    inspected = set().union(*map(set, queues.values()))
    expected = {r['id'] for r in v6['records'] if r['in_reopened_stratum'] and outside(r)}
    assert inspected == expected and len(inspected) == 2930
    sampled = {r['id'] for r in origin['records']}
    assert len(sampled) == 300 and not sampled & inspected
    scope = {r['id'] for r in v6['records'] if r['in_reopened_stratum']}
    assert len(scope) == 3085 and len(scope & sampled) == 155
    assert scope <= inspected | sampled

    notes = {}
    unresolved_note_mentions = []
    stems = {'array': 'ARRAY_STRATUM_REVIEW', 'rust_generation': 'RUST_STRATUM_REVIEW',
             'python_generation': 'PYTHON_GENERATION_REVIEW',
             'python_repair': 'PYTHON_REPAIR_REVIEW', 'js_ts_residual': 'JS_TS_RESIDUAL_REVIEW'}
    for queue_name, ids in queues.items():
        for position, record_id in enumerate(ids, 1):
            if queue_name == 'targeted':
                name = 'TARGETED_STRATUM_REVIEW.md'
            else:
                batch = (position - 1) // 15 + 1
                if queue_name == 'array':
                    batch = min(batch, 36)  # Last documented batch contains 19 rows.
                stem = stems[queue_name]
                name = f'{stem}.md' if queue_name == 'array' and batch == 1 else f'{stem}_{batch}.md'
            path = root / name
            content = path.read_text()
            inputs[str(path)] = digest(path)
            compact = re.sub(r'[^a-z0-9]', '', content.lower())
            lane, kind, number = record_id.removeprefix('exp-v1-').split('-')
            # Early notes use prose identifiers, later ones position/ID tables.
            found = kind + number in compact or bool(re.search(
                rf'^\|\s*{position}\s*\|\s*{number}\s*\|', content, re.M))
            if not found:
                unresolved_note_mentions.append({'id': record_id, 'note': str(path), 'position': position})
            notes.setdefault(record_id, []).append({'queue': queue_name, 'position': position, 'note': str(path)})
    hold_ids = [h['id'] for h in holds['holds']]
    assert len(hold_ids) == len(set(hold_ids))
    assert set(hold_ids) <= candidate_ids
    for h in holds['holds']:
        path = Path(h['evidence'])
        inputs[str(path)] = digest(path)
    assert not unresolved_note_mentions, unresolved_note_mentions
    return {
        'status': 'inspection-coverage-reconciled-not-quality-admission',
        'candidate_count': len(candidates), 'reopened_scope_count': len(scope),
        'frozen_sample_count': len(sampled), 'sample_in_scope_count': len(sampled & scope),
        'unique_outside_sample_count': len(inspected), 'missing_scope_ids': sorted(scope - inspected - sampled),
        'outside_scope_ids': sorted(inspected - scope),
        'queue_counts': {k: len(v) for k, v in queues.items()},
        'overlap_ids': sorted(k for k, n in Counter(x for q in queues.values() for x in q).items() if n > 1),
        'test_origin_status_counts': dict(Counter(r['status'] for r in origin['records'])),
        'additive_holds': len(hold_ids), 'historical_holds': 3,
        'limitations': ['Inspections are documented scoped reviews, not seven-criterion passes.',
                       'No new candidate execution, no changed corpus, no training seal.',
                       'Record mentions and queue coverage do not independently certify semantic judgments.'],
        'records': [{'id': k, 'review_notes': v} for k, v in sorted(notes.items())],
        'input_sha256': inputs,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = reconcile()
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('records', 'input_sha256')}))


if __name__ == '__main__':
    main()
