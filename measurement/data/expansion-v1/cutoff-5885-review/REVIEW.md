# Cutoff quality review — in progress

Population: 5,885; deterministic sample: 300. Cutoff corpus SHA-256:
`3ca9209b51d36b9137d65f6f0424bfc369a662bd5af7f99666f4ecc60ee24e92`.
Prepared manifest SHA-256:
`0a58d3d30f98202bd6fd87fafb1c7ddb415a2fabbfa21f6378da0399e72b6623`.

This is a partial review, not a passed sample. Three candidate specifications,
reference implementations, original tests, and known-bad implementations were
read. Teacher isolation evidence has not yet been independently audited for
these rows. The remaining 297 sample records have not been reviewed.

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

Final re-execution continues separately. Training remains blocked by incomplete
review and the confirmed ticket-registry finding.
