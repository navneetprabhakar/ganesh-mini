# Array-validation follow-up, batch 12

2026-09-06. Positions 166–180 inspected against prompts, references and original
tests: 15 new / 189 unique outside-sample targeted inspections. Ten new held
records: **146 additive / 149 including historical three**. Frozen 300 unchanged;
inspection is not seven-criterion approval.

| ID suffix | Finding | Result |
| --- | --- | --- |
| typescript-generation-0112 | Malformed unrelated email field throws instead of being a nonmatch. | recovery-unrelated-malformed-email-result.json |
| typescript-repair-0075 | Missing contact link bypasses required validation. | contact-footer-sparse-result.json |
| typescript-repair-0076 | Missing stored track ID accepted as valid reducer state. | queue-stored-sparse-result.json |
| javascript-repair-0092 | Missing color channels accepted despite integer-channel requirement. | tint-color-sparse-result.json |
| javascript-generation-0135 | Malformed sparse saved loans retained instead of falling back to empty. | library-saved-sparse-result.json |
| typescript-repair-0077 | Required validated meteorite ID lost in constructor copy. | meteorite-hidden-id-result.json |
| typescript-repair-0080 | Missing messages accepted; safe-integer delta also wraps incorrectly due to intermediate rounding. | message-deck-sparse-result.json |
| javascript-repair-0093 | Missing resources bypass required object validation. | realm-resources-sparse-result.json |
| javascript-repair-0094 | Floating-point rounding falsely classifies [1, MAX_SAFE_INTEGER, MAX_SAFE_INTEGER] as a right triangle. | right-triangle-safe-rounding-result.json |
| javascript-generation-0140 | Positive decimal pick beyond safe-integer range classified invalid although it exceeds valid result count and should return No results. | lookup-large-positive-pick-result.json |

Eleven diagnostics failed in pinned network-disabled/resource-limited sandboxes,
with no timeout. TS compilation succeeded. The second MessageDeck result is
`message-deck-safe-delta-result.json`: start index 2, three messages, delta
MAX_SAFE_INTEGER should reach index 0 but reaches index 2 after rounded addition.
Triangle sides are all positive safe integers; equality of the two longest sides
precludes a right triangle with a positive third side. Neither probe is large.
Lookup permits a positive decimal integer without a safe-integer restriction;
the diagnostic requests index 9007199254740992 against zero results.

Recovery's prose explicitly says malformed unrelated email fields are nonmatches
and only booleans are already strongly typed. Null-email probe uses an explicit
cast to test that runtime clause; it is not a blanket assumption that every
typed input needs runtime rejection. Original tests only cover malformed strings.

Scoped negative findings and open questions:

- JS generation0137 ticket callbacks operate on reducer-built dense state;
  unchanged tickets are intentionally shared. Prose's malformed-action fallback
  versus recognized-action validation needs clarity; no automatic hold here.
- JS generation0134 WorkshopRoster maps internally built dense entries and
  copies explicit fields. Underscore-private fields are not a stated security
  boundary; no arbitrary direct-state-tampering counterexample is imposed.
- JS repair0091 stableSortedBy uses an indexed loop and invokes the selector on
  every slot. Sparse selector policy is not silently inferred from map presence.
- TS generation0118 seatReducer assumes typed boolean state; malformed/sparse
  initial state policy remains open rather than an automatic rejection.
- TS repair0079 OutlineStore copies explicit fields, detects cycles/duplicate IDs
  and commits replacement only after copying. Sparse forests and missing nodes
  are an open type-boundary question beyond the enumerated rejection clauses.
- JS repair0094's sparse input already returns false through NaN comparison,
  matching its explicit contract. Its hold concerns numeric correctness only.
- Meteorite label-whitespace rejection is stronger than literal nonempty prose
  but appears in original tests; retain that separate contract-clarity issue.

Continue at position 181. GCS verified through batch 11 / 139 holds; this batch
awaits backup. No revised partition, training seal, generation restart or new VM.
