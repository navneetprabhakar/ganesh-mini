from copy import deepcopy
from pathlib import Path

import pytest

from scripts.data.admit_expansion import admit_records, canonical_json
from scripts.data.prepare_expansion_cutoff import assemble, matches
from tests.data.test_admit_expansion import config, empty_index, record, verifier


def admitted(candidate):
    return admit_records([candidate], config(), empty_index(), Path("runtime.json"), verifier)[0][0]


def test_exact_candidate_restored_with_original_tests(tmp_path):
    candidate = record()
    row = admitted(candidate)
    path = tmp_path / "candidates.jsonl"
    path.write_bytes(canonical_json(candidate) + b"\n")
    restored, origins = assemble([row], [path], config())
    assert restored == [candidate]
    assert origins[0]["line"] == 1


@pytest.mark.parametrize("field", ["messages", "source", "verification_task", "rights"])
def test_changed_candidate_cannot_replace_admitted_version(field, tmp_path):
    candidate = record()
    row = admitted(candidate)
    altered = deepcopy(candidate)
    if field == "messages":
        altered[field][1]["content"] += "# changed\n"
    else:
        altered[field]["tampered"] = True
    assert not matches(row, altered)
    path = tmp_path / "candidates.jsonl"
    path.write_bytes(canonical_json(altered) + b"\n")
    with pytest.raises(ValueError, match="missing exact"):
        assemble([row], [path], config())


def test_duplicate_corpus_ids_fail_closed(tmp_path):
    row = admitted(record())
    with pytest.raises(ValueError, match="duplicate corpus"):
        assemble([row, row], [], config())
