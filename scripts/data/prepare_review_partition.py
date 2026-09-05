"""Preserve executed results while separating records awaiting issue review."""
import hashlib
import json
from pathlib import Path
from scripts.data.admit_expansion import read_jsonl, canonical_json


def main():
    source = Path('artifacts/verification/cutoff-5885-vm/remote')
    output = Path('datasets/cache/expansion-v1/review-partition-v1')
    if output.exists():
        raise ValueError('partition already exists; preserve evidence')
    report = json.loads((source/'final.admission.json').read_text())
    payload = (source/'final.admitted.jsonl').read_bytes()
    if hashlib.sha256(payload).hexdigest() != report['output_sha256']:
        raise ValueError('executed output hash mismatch')
    rows = read_jsonl(source/'final.admitted.jsonl')
    flagged = {r['id']:r['reason'] for r in report['rejected']}
    flagged['exp-v1-go-generation-0165'] = 'Independent quality probe: Consume before start deletes future ticket'
    candidate_path = Path('datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl')
    if hashlib.sha256(candidate_path.read_bytes()).hexdigest() != report['input_sha256']:
        raise ValueError('executed candidate hash mismatch')
    candidates = read_jsonl(candidate_path)
    for collection in (rows, candidates):
        if len({r['id'] for r in collection}) != len(collection):
            raise ValueError('duplicate record IDs')
    held = [r for r in candidates if r['id'] in flagged]
    eligible = [r for r in rows if r['id'] not in flagged]
    if len(rows) != 5883 or len(held) != 3 or len(eligible) != 5882:
        raise ValueError('unexpected partition counts')
    files = {'review-eligible.jsonl': b''.join(canonical_json(r)+b'\n' for r in eligible),
             'flagged.candidates.jsonl': b''.join(canonical_json(r)+b'\n' for r in held)}
    manifest = {'status':'pending-quality-review-not-training-ready',
        'executed_passed':5883, 'review_eligible':5882, 'flagged':flagged,
        'source_report_sha256':hashlib.sha256((source/'final.admission.json').read_bytes()).hexdigest(),
        'source_output_sha256':report['output_sha256'],
        'files':{k:hashlib.sha256(v).hexdigest() for k,v in files.items()},
        'policy':'Review flagged records separately; preserve original VM report and original 300-row sample, including flagged rows.'}
    output.mkdir()
    for name,data in files.items():
        (output/name).write_bytes(data)
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps(manifest))


if __name__ == '__main__':
    main()
