# Cutoff quality review — in progress

Population: 5,885; deterministic sample: 300. Cutoff corpus SHA-256:
`3ca9209b51d36b9137d65f6f0424bfc369a662bd5af7f99666f4ecc60ee24e92`.
Prepared manifest SHA-256:
`0a58d3d30f98202bd6fd87fafb1c7ddb415a2fabbfa21f6378da0399e72b6623`.

This is a partial review, not a passed sample. Thirteen candidate specifications,
reference implementations, original tests, and known-bad implementations have
been read: the first twelve in frozen sample order and Go repair 0465, selected
for follow-up on atomicity. The remaining 287 have not had semantic review.
Archived test-origin checks matched 295/300 samples to exact specification-only
test-author prompts and unchanged test outputs; five need additional provenance
tracing. This automated trace is not 295 semantic reviews or a quality seal.
See `test-origin-all300.json` and `FIRST_BATCH_REVIEW.md`.

## Confirmed gap: exp-v1-go-generation-0165

The ticket registry's Consume deletes any existing ticket, including one whose
start tick is in the future. The specification allows deletion for currently
valid and expired tickets; a not-yet-valid ticket is neither. Existing tests
cover Check before start, Consume while valid, and Consume when expired, but
omit Consume before start followed by Check at start.

`probe_test.go` was executed as `cutoff_review_test.go` with the original
reference code and original go.mod in the pinned network-disabled Go sandbox.
It failed normally with exit 1, no timeout, in 28,132 ms. `probe-result.json`
preserves the actual result. The original candidate is unchanged and is bound
through the cutoff manifest's candidate origins and task hash.

Disposition: blocks passing this sample. Correct and independently re-admit,
or exclude with an explicit derived-corpus manifest. Audit temporal lifecycle
tasks for the same test gap before deciding whether the defect is systematic.
Passing original tests in final re-execution cannot waive this finding.

## Other inspected rows

- `exp-v1-go-generation-0251`: alias directory. Static inspection found the
  advertised validation, atomic batch, insertion order, copied slices, and
  mutex protection implemented. Tests exercise these properties and reject
  the missing-prefix-separator mutation. No defect identified in this read.
- `exp-v1-go-generation-0491`: attempt policy. Static inspection found total
  attempt bounds, halt-before-repeat precedence, original error identity,
  nil validation, and wrapping implemented. Tests cover the principal paths;
  the strict-upper-bound mutation is a plausible failure. No defect identified
  in this read. Neither row has a completed seven-criterion sign-off yet.

Final VM re-execution is complete. Training remains blocked by incomplete
review. The original ticket finding is held out in review-partition-v1; the
additional stock-ledger finding below must also be held out before sealing.

## Confirmed nondeterministic directionality: exp-v1-go-generation-0058

The stock-ledger known-bad implementation commits changes while iterating an
unordered map. The original atomicity tests can miss the defect when invalid
entries happen to be visited first. A pinned, network-disabled sandbox probe
ran the unmodified original suite in 64 fresh child processes for each code:
the reference passed 64/64; the known-bad passed 2/64 and failed 62/64.
Neither outer execution timed out. This is a test reliability defect, not a
newly demonstrated reference-code defect. Do not treat 2/64 as a population
estimate or alter the original VM report.

A second diagnostic retained the combined output and exit status of every
child trial: reference 64/64 passed, known-bad 0/64 passed. All 128 trial
records are present and neither run timed out. This does not negate the first
run's observed false accepts; the variation is consistent with the map-order
dependence. Keep both runs rather than selecting the more convenient result.
The full-output run is `stock-repeatability-trial-output-result.json`; each
result embeds its own exact diagnostic task, including the test version.

`stock_repeatability_test.go`, `stock-repeatability-result.json`, and
`scripts/data/probe_stock_repeatability.py` preserve the diagnostic and exact
inputs. The outer diagnostic deliberately reports nonzero to expose counts;
interpret its child counts, not the outer exit as reference failure.

Disposition: additional hold, separate from the three original held records.
The historical 5,882-row v1 partition is unchanged and must not be sealed as-is;
it still contains this row. Excluding it leaves 5,881 before any further review
exclusions. Audit map-order-dependent atomicity tests before signing off the
affected stratum. Go repair 0465 uses ordered slice changes and explicit
valid-then-invalid sequences; static review found it does not share this gap.
That single follow-up is not a corpus-wide systematic-defect clearance.
