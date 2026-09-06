# Array-validation follow-up, batch 8

2026-09-06. Array-hit positions 106–120 outside the frozen sample inspected for
prompt/reference/original-test consistency: **15 new / 129 unique outside-sample
targeted inspections**. Frozen 300 unchanged; not seven-criterion approval.
Seven diagnostic failures on six new held records in pinned network-disabled,
resource-limited sandboxes. No timeout; JS exits `[1]`, TS `[0,0,1]`.

| ID suffix | Finding | Result file | ms |
| --- | --- | --- | ---: |
| javascript-repair-0055 | equal finite central readings overflow | central-reading-finite-result.json | 353 |
| javascript-repair-0055 | sparse readings accepted | central-reading-sparse-result.json | 333 |
| javascript-generation-0081 | zero-time integration produces NaN | body-zero-dt-result.json | 341 |
| typescript-generation-0073 | safe-integer changes lose precision before cancellation | stock-safe-cancellation-result.json | 2309 |
| typescript-repair-0050 | valid hidden string field lost during no-transform copy | conversion-hidden-field-result.json | 2408 |
| typescript-repair-0052 | valid hidden ID lost and current() throws | member-hidden-id-result.json | 2393 |
| javascript-generation-0090 | unknown hidden patch field accepted | shelf-hidden-patch-result.json | 381 |

Original tests omit these counterexamples. Stock changes are MAX_SAFE_INTEGER,
2 and -MAX_SAFE_INTEGER, whose exact final balance is 2. Body mass is positive
MIN_VALUE and force finite, but force/mass overflows before multiplication by
zero duration. Required property preservation has no enumerable-only limitation
in the conversion/member contracts. Shelf patch explicitly allows only three
field names without an enumerability exception. Totals: **107 additive / 110
holds including historical three**.

## Scoped negative findings and unresolved boundaries

- JS repair0053 rankDocuments intentionally skips malformed documents. forEach
  skipping holes is consistent; dense ranked results preserve tie order. Its
  whitespace-only ID policy is inherited but not explicit in the prose.
- JS repair0056 isOriginAllowed intentionally ignores malformed/non-string
  rules, so some skipping holes is valid. Dot-count/host-label constraints are
  underspecified in prose but inherited source/tests reject single-label hosts.
- JS generation0082 queue validation spreads source arrays before every, so
  missing elements become undefined and are rejected. Copies/freeze and order
  agree with original tests; do not treat every occurrence as a sparse bypass.
- TS generation0074 renderDelimited specifies string rows, not runtime malformed
  element handling. Delimiter UTF-16-unit bounds and escaping match tests;
  sparse-row semantics remain an API question, not a new hold.
- TS generation0075 normalizeOutline filters unsupported tokens intentionally.
  Title removal versus summary adjacency is not fully explicit; original tests
  show unknown tokens do not separate groups. Preserve ambiguity separately.
- TS generation0078 shipment validator explicitly scopes unknown keys to own
  enumerable ones, and tests ignore hidden extras. Do not apply the shelf's
  stricter patch contract to this candidate. Required key enumerability and
  inherited Object.prototype values remain distinct unprobed questions.
- JS generation0087 memory ledger validates source with for-of, and original
  tests expressly reject sparse input. Internal entries are push-built dense.
- JS repair0059 encodeFields explicitly scopes enumerable string keys, ignores
  hidden/symbol properties, checks plain prototypes and unpaired surrogates;
  internal maps are dense. This is a static control supported by original tests.
- TS repair0055 agenda rows specifies exact UTF-16 truncation, preserves duplicate
  IDs and copies groups. Sparse item/group rejection is not specified; no hold.

Continue at array-hit position 121. No candidate rewrite, generation restart,
revised partition, training seal or new VM.
