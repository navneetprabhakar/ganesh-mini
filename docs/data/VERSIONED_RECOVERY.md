# Versioned recovery planning

The original cutoff5885 corpus and historical review artifacts remain immutable.
Complete systematic criterion reconciliation before approving parent selections.
The planner is tooling only: it neither approves selections nor generates,
verifies, admits, or trains candidates.

`python -m scripts.data.plan_versioned_recovery --input <frozen-candidates.jsonl>
--holds <additional-holds.json> --requests <reviewed-requests.json>
--output-dir <new-directory>` creates a create-only `plan.json`. Existing output
directories, including incomplete runs, are rejected; use a new version/run.
The CLI accepts only the frozen5885 SHA256. Library tests use small fixtures.

The reviewed request contains `version` (r1, r2, ...), exact
`parent_corpus_sha256`, exact `hold_ledger_sha256`, and nonempty `selections`.
Each selection supplies `parent_id`, canonical `parent_candidate_sha256`,
`change_class`, a substantive `rationale`, `review_evidence` repository path,
and `review_evidence_sha256`. The CLI verifies the actual file content before
writing a plan; the execution path must verify it again.
Supported change classes: reference-fix, contract-clarification, oracle-rebuild.
Trivial prompt padding is not an accepted recovery class. Whether a held task
has enough substantive content to recover remains a human-reviewed decision;
the planner does not infer suitability from reason keywords.

New IDs use `exp-v1-recovery-rN-<lane>-<task-type>-<original-number>`.
Version names must be globally reserved at execution: fresh plan directories
alone do not prevent reusing an ID across two plans. The executor must enforce
one immutable plan per version and one generation attempt per derived ID.
Plans retain full parent source/rights/hold records and input hashes. These are
lineage manifests, not executable expansion candidates, and must not be supplied
directly to admission or training. The plan hash excludes its own hash field.

`python -m scripts.data.generate_versioned_recovery --plan <plan.json>
--quality-closure <closure.json> --input <frozen-candidates.jsonl>
--holds <additional-holds.json>` implements generation only. It validates input
hashes, closure and reviewed evidence, then reserves one immutable version under
`datasets/cache/expansion-v1/versioned-recovery/rN`. Never reuse interrupted
versions. Architect and independent-test phases preserve raw teacher evidence,
including partial timeout output. Test authors see only the derived specification.
Per-candidate outputs are preserved even if a subsequent lane fails.

Remaining admission work: execute reference and known-bad programs in
the pinned network-disabled sandbox; recheck evaluation separation and duplicate
overlap against both recovered and retained originals; perform independent quality
review and enforce corpus/task/family-token objectives before a new admission seal.
Generation is not verification, admission or training. Original parents and their
historical tests/results are never overwritten by a recovery.

## Bounded test correction and diagnostics

`scripts/data/correct_recovery_tests.py` performs one independently authored
test correction using a new globally reserved recovery version. A new reviewed
plan and exact intermediate-candidate hashes are mandatory. The critic sees
only the unchanged specification, proposed tests and specification-derived
feedback; no reference or mutant source. The run contract preserves that context
and the r1 file hashes. Specification/reference/known-bad bytes are unchanged.
Do not feed a correction run back into another automatic critic loop. An oracle
still failing after the bounded pass remains a documented exclusion.

`scripts/data/verify_versioned_recovery.py` preserves each reference, known-bad
and original-parent diagnostic separately. It is diagnostic-only and never
admits data. Compile failures, timeouts and infrastructure errors are not
semantic mutant proof. `--go-race` records a derived runtime-command contract
while retaining the exact Go image and all sandbox resource/network limits.

`scripts/data/prepare_recovery_admission.py` accepts an explicit main-reviewed
selection with candidate/review/diagnostic hashes and preserved parent lineage.
It checks exact/fuzzy overlap against retained originals and other selections.
Its prepared candidates still require `scripts/data/admit_expansion.py` for fresh
evaluation separation and executable candidate admission. Candidate admission
is not the final corpus seal: sufficiency, composition and family-token balance
remain mandatory before training.
