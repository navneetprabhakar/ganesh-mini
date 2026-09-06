# Array-validation follow-up, batch 15

Completed positions 211–225: 15 new / 234 unique outside-sample inspections.
Ten new holds in this batch: **175 additive / 178 including historical three**.
Earlier five-record checkpoint below retained as history.

| ID suffix | Finding | Result |
| --- | --- | --- |
| javascript-repair-0114 | Missing header bypasses string validation. | header-fields-sparse-result.json |
| javascript-generation-0169 | Quantity total changes with object key insertion order. | basket-count-key-order-result.json |
| javascript-repair-0113 | Reference overrides returned array map semantics to accommodate incorrect chunks.map(Array.from) tests. | chunk-array-map-contract-result.json |
| typescript-repair-0102 | Null text field throws instead of using required fallback. | assignment-null-text-result.json |
| javascript-generation-0175 | Missing selection record bypasses validation. | selection-model-sparse-result.json |
| javascript-generation-0178 | Missing secondary action bypasses validation. | alert-secondary-sparse-result.json |
| javascript-generation-0179 | Missing key is passed to collaborators instead of rejecting malformed input before calls. | clear-exit-sparse-prevalidation-result.json |

All seven later diagnostics reproduced failures without timeout. TS compilation
passed. ChunkBytes returns an array with an own map override that omits callback
index and array arguments. Original tests use chunks.map(Array.from), which is
not a valid ordinary-array callback use. The diagnostic tests ordinary map index
arguments; the hold also records explicit reference/test accommodation.
Basket counterexample has just three quantities (2**53, 1, 1); changing key order
changes total despite a specific order-independence promise. Assignment explicitly
requires fallbacks for null text fields; the type assertion tests that runtime
clause rather than imposing a general untyped-input policy.

Scoped negative findings: JS generation0170 parses dense string splits and uses
per-registration subscriber identity plus a publication snapshot. TS generation
0153 validates each active ID with for-of before filtering. TS generation0154
maps internal dense entries with bounded rates; huge argument-list limits remain
an unprobed scalability question. No automatic extra holds for those rows.

Continue position 226. Scope v4 adds candidate-bound JavaScript test accommodation:
10 groups, still 14 strata / 3,085 records of review scope, not rejection count.
No training seal, revised partition, generation restart or new VM.

2026-09-06. Positions 211–215 inspected against prompt, reference and original
tests: five new / 224 unique outside-sample inspections. Three new holds bring
the ledger to **168 additive / 171 including historical three**. Frozen 300
unchanged. This is not seven-criterion approval.

- JS generation0163 createQueue maps internally built dense entries; explicit
  primitive fields are copied. No new array-validation or copying defect found.
- TS generation0146 configuration helpers use null-prototype result maps and
  own-key checks. Filename localeCompare versus generic sorting wording and
  numeric-key enumeration remain open contract questions, not executed holds.
- TS generation0148 validateAccount inserts duplicate-email issue before a later
  accessLevel format issue; contract says append duplicate after format/required
  issues. `account-duplicate-issue-order-result.json`, 2170 ms, `[0,0,1]`.
- TS generation0149 PreferenceForm accepts a missing provider as undefined;
  `preference-providers-sparse-result.json`, 2123 ms, `[0,0,1]`. Notifier/navigation
  throwing behavior remains a separate callback-policy question.
- JS generation0174 timeline rejects valid date 0099-01-01 because Date.UTC maps
  years 0–99 into 1900–1999; `timeline-early-year-result.json`, 396 ms, `[1]`.

All probes ran in pinned network-disabled/resource-limited sandboxes, no timeout;
TS compilation succeeded. Original tests omit these cases. Continue position 216.
GCS verified through 168 holds / batch 14; these five inspections postdate it.
No training seal, revised partition, generation restart or new VM.
