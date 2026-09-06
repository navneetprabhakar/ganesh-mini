"""Bind completed sample dispositions to frozen candidate and hold identities."""

import argparse
import hashlib
import json
import re
from pathlib import Path

from scripts.data.admit_expansion import canonical_json


REVIEW = Path('measurement/data/expansion-v1/cutoff-5885-review')
FROZEN = Path('datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl')
EXPECTED_SHA = '680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec'
LANES = ('go', 'java', 'javascript', 'python', 'rust', 'typescript')
HISTORICAL_HOLDS = {
    'exp-v1-go-generation-0165',
    'exp-v1-rust-generation-0161',
    'exp-v1-rust-generation-0224',
}


def parse_decisions(text, lane):
    current = None
    result = {}
    declared = {}
    counts = {'positive': 0, 'held': 0}
    for line in text.splitlines():
        if line.startswith('## '):
            match = re.fullmatch(r'## (Positive|Held)(?: sample)? decisions \((\d+)\)', line)
            current = match[1].lower() if match else None
            if current:
                if current in declared:
                    raise ValueError('duplicate decision section')
                declared[current] = int(match[2])
        match = re.match(r'^\| ((?:generation|repair)-\d+) \| (.+) \|$', line)
        if match:
            if current is None:
                raise ValueError('record outside a decision section')
            identifier = f'exp-v1-{lane}-{match[1]}'
            if identifier in result:
                raise ValueError('duplicate disposition: ' + identifier)
            result[identifier] = {'decision': current, 'basis': match[2]}
            counts[current] += 1
    if declared != counts:
        raise ValueError('declared decision counts disagree with rows')
    return result


def reconcile(root=REVIEW, frozen=FROZEN):
    candidate_bytes = frozen.read_bytes()
    if hashlib.sha256(candidate_bytes).hexdigest() != EXPECTED_SHA:
        raise ValueError('frozen candidate file changed')
    candidates = [json.loads(line) for line in candidate_bytes.splitlines()]
    by_id = {r['id']: r for r in candidates}
    if len(by_id) != len(candidates):
        raise ValueError('duplicate candidate identity')
    origin = json.loads((root / 'test-origin-all300-chains.json').read_text())
    sample = {r['id']: r for r in origin['records']}
    if len(sample) != 300 or len(sample) != len(origin['records']):
        raise ValueError('sample size/identity changed')
    holds = json.loads((root / 'additional-holds.json').read_text())['holds']
    held = {r['id'] for r in holds}
    if len(held) != len(holds) or held & HISTORICAL_HOLDS:
        raise ValueError('duplicate hold')
    held |= HISTORICAL_HOLDS
    rows = []
    counts = {}
    inputs = {}
    for lane in LANES:
        path = root / f'SEVEN_CRITERIA_{lane.upper()}.md'
        payload = path.read_bytes()
        inputs[str(path)] = hashlib.sha256(payload).hexdigest()
        decisions = parse_decisions(payload.decode(), lane)
        expected = {identifier for identifier in sample if identifier.startswith(f'exp-v1-{lane}-')}
        if set(decisions) != expected:
            raise ValueError('sample disposition coverage mismatch: ' + lane)
        counts[lane] = {'positive': 0, 'held': 0}
        for identifier, decision in decisions.items():
            if (identifier in held) != (decision['decision'] == 'held'):
                raise ValueError('hold/disposition disagreement: ' + identifier)
            candidate_sha = hashlib.sha256(canonical_json(by_id[identifier])).hexdigest()
            if candidate_sha != sample[identifier]['candidate_sha256']:
                raise ValueError('sample candidate binding changed: ' + identifier)
            counts[lane][decision['decision']] += 1
            rows.append({'id': identifier, 'candidate_sha256': candidate_sha,
                         'evidence': str(path), **decision})
    for name in ('additional-holds.json', 'test-origin-all300-chains.json'):
        path = root / name
        inputs[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {'status': 'sample-disposition-complete-not-training-admission',
            'candidate_sha256': EXPECTED_SHA, 'sample_count': len(rows),
            'by_lane': counts, 'positive': sum(v['positive'] for v in counts.values()),
            'held': sum(v['held'] for v in counts.values()), 'corpus_holds': len(held),
            'evidence_sha256': inputs, 'records': rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = reconcile()
    with args.output.open('x') as handle:
        json.dump(report, handle, indent=2)
        handle.write('\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('records', 'evidence_sha256')}))


if __name__ == '__main__':
    main()
