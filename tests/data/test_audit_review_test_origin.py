import copy
import json

import pytest

from scripts.data.audit_review_test_origin import check_run, digest
from scripts.data.generate_expansion_qualification import test_prompt as make_test_prompt


def run_evidence():
    events = [{'type': 'turn.completed', 'usage': {'input_tokens': 1}}]
    run = {'lane': 'go', 'prompt': make_test_prompt('go', [{'id': 'x', 'problem': 'Implement X.'}]),
           'final_output': '{"items":[]}', 'stdout_jsonl': json.dumps(events[0]) + '\n',
           'stderr': '', 'events': events, 'returncode': 0,
           'command_identity': ['codex', 'exec', '--ephemeral', '--ignore-user-config',
                                '--ignore-rules', '--sandbox', 'read-only', '-C', '/isolated']}
    for field, h in [('prompt', 'prompt_sha256'), ('final_output', 'final_output_sha256'),
                     ('stdout_jsonl', 'stdout_sha256'), ('stderr', 'stderr_sha256')]:
        run[h] = digest(run[field].encode())
    return run


def test_specification_only_prompt_verified():
    assert check_run(run_evidence()) == {'x': {'id': 'x', 'problem': 'Implement X.'}}


def test_reference_appended_to_prompt_is_rejected_even_with_fresh_hash():
    run = run_evidence()
    run['prompt'] += '\nSecret reference: return 1'
    run['prompt_sha256'] = digest(run['prompt'].encode())
    with pytest.raises(ValueError, match='template'):
        check_run(run)


def test_tampered_output_rejected():
    run = run_evidence()
    run['final_output'] += 'changed'
    with pytest.raises(ValueError, match='hash mismatch'):
        check_run(run)


def test_tool_event_rejected():
    run = copy.deepcopy(run_evidence())
    run['events'].append({'type': 'item.completed', 'item': {'type': 'command_execution'}})
    run['stdout_jsonl'] = ''.join(json.dumps(x) + '\n' for x in run['events'])
    run['stdout_sha256'] = digest(run['stdout_jsonl'].encode())
    with pytest.raises(ValueError, match='execution events'):
        check_run(run)


def test_non_ephemeral_execution_rejected():
    run = run_evidence()
    run['command_identity'].remove('--ephemeral')
    with pytest.raises(ValueError, match='isolation flags'):
        check_run(run)
