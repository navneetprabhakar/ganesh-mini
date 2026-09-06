# Array-validation follow-up, batch 5

2026-09-06. Array-hit positions 61–75 outside the frozen sample inspected for
prompt/reference/original-test consistency: **15 new / 84 unique outside-sample
targeted inspections**. Frozen sample remains 300; this is not seven-criterion
approval. Five diagnostic failures on four records, plus one passing control.
All executed in pinned network-disabled resource-limited sandboxes, no timeout.

| ID suffix | Finding | Result file | ms |
| --- | --- | --- | ---: |
| javascript-repair-0032 | sparse priority records bypass validation | priority-sparse-result.json | 386 |
| javascript-repair-0030 | __proto__ string key is not stored | observable-parameter-key-result.json | 362 |
| typescript-repair-0033 | mean of identical finite MAX_VALUE numbers overflows | bucket-finite-mean-result.json | 2466 |
| typescript-repair-0033 | sparse numeric array bypasses finite validation | bucket-sparse-result.json | 2957 |
| typescript-repair-0039 | sparse routes bypass validation | route-sparse-result.json | 3003 |

JS failures exit `[1]`; TS failures compile then exit `[0,0,1]`. Original tests
do not cover these counterexamples. The mean is representable and exactly
known; this is not a demand to represent an overflowing mathematical result.
Four new holds bring totals to **86 additive / 89 including historical three**.

## Scoped negative findings and unresolved boundaries

- JS generation0047 buildSpeakerCard maps dense split words/fixed field names;
  no external sparse array. Unicode title-casing outside BMP remains unprobed.
- JS repair0029 extractFiniteMeasurements intentionally filters invalid values;
  skipping holes is consistent, not a hold. Non-triviality remains open.
- JS generation0046 resolveScreen maps a fixed dense delimiter list. Earliest
  query/fragment cut and literal routing agree with ordinary tests; non-triviality
  remains open.
- JS repair0030 uses per-entry subscription identity and callback snapshots;
  no duplicate-unsubscribe defect inferred. Held for dictionary storage only.
- TS generation0048 rewriteLatestAgentDirective maps dense parsed entries.
  Validation checks URI decodability but canonical encoding requirements are
  not fully explicit; retain API-clarity review instead of inventing rejection.
- JS generation0052 resolveChecklist validates items with for-of before map.
  Non-enumerable answer properties are read although validation visits enumerable
  keys; the treatment of such properties needs contract adjudication, not an
  unsupported automatic failure label.
- TS generation0049 buildFeaturePanel maps public input and can preserve holes,
  but only empty trimmed fields are expressly invalidated. Sparse-input scope
  is not sufficiently explicit here for a new rejection diagnostic/hold.
- TS generation0050 activateHints splits a string into a dense array, reads
  preference once, and guards activation. No sparse issue found.
- TS generation0059 MessageDrop validates constructor elements with spread plus
  for-of; message arrays are private push-built dense arrays and copied on read.
  No sparse acceptance found. Sequence exhaustion is not practically probed.
- TS repair0038 ExtensionRegistry maps private dense entries, replaces in place,
  and copies records. Empty get-key versus registration-only name rejection is
  an API wording question; no broad failure inferred.
- TS repair0039 rejects final-newline route segments in the pinned runtime:
  `route-terminal-newline-result.json` **passes `[0,0,0]`, 3207 ms**. This exact
  regex hypothesis is disproved. Its hold is solely the sparse-array result.
- TS generation0055 AdaptiveMenu maps fixed internal definitions and correctly
  copies snapshots. Fractional widths between 639 and 640 are an unresolved
  wording boundary, not a manufactured rejection.
- TS generation0057 rootReducer copies supplied records and changed branches,
  retains unaffected branch identity, and validates import counts. Sparse record
  validation is not specified; no hold invented. Public interface field details
  and mutable exported initial-state semantics remain API-clarity questions.

Continue at array-hit position 76 in the immutable inventory. No candidate
changes, new VM, generation restart, revised partition or training seal.
