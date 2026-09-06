# Array-validation follow-up, batch 14

2026-09-06. Positions 196–210 inspected against prompts, references and original
tests: 15 new / 219 unique outside-sample targeted inspections. Nine new holds:
**165 additive / 168 including historical three**. Frozen 300 unchanged;
inspection is not seven-criterion approval.

| ID suffix | Finding | Result |
| --- | --- | --- |
| typescript-repair-0085 | Required choice value lost during copying. | choice-deck-hidden-value-result.json |
| typescript-repair-0087 | Required gallery ID lost during copying. | gallery-hidden-id-result.json |
| typescript-generation-0139 | Missing provider label accepted as valid string data. | label-counter-sparse-result.json |
| typescript-repair-0094 | Required mount route lost during copying. | gateway-mount-hidden-route-result.json |
| typescript-repair-0095 | Inherited Object method is accepted as a supplied default translation table. | phrase-missing-prototype-locale-result.json |
| javascript-repair-0106 | Required validated card ID lost during copying. | hovered-card-hidden-id-result.json |
| javascript-repair-0108 | Missing label bypasses string validation. | shared-labels-sparse-result.json |
| javascript-repair-0109 | Sparse task list runs earlier callback before rejecting missing function, violating prevalidation. | run-steps-sparse-prevalidation-result.json |
| javascript-repair-0112 | Missing numeric value bypasses input validation. | lighter-sparse-result.json |

Nine reproduced behavioral failures, no timeouts. Pinned network-disabled,
resource-limited runtimes; TS compiled successfully before assertions failed.
PhraseBook probe uses an empty supplied map with default locale toString; the
inherited method is not a supplied translation table. runSteps eventually
rejects with TypeError, but only after running the preceding callback; the
diagnostic verifies both the rejection and the forbidden callback side effect.
Original tests do not cover these counterexamples.

Scoped negative findings and open questions:

- TS generation0133 splits strings into dense arrays. Its prose about dot-
  separated email segments is ambiguous against explicit original tests; no
  additional email-domain restriction is invented here.
- TS repair0092 MemoryLogger maps internal dense records. Quantity fractional
  unit boundary wording remains open; rounding after division avoids the simple
  finite-intermediate overflow pattern present in other candidates.
- TS generation0144 creates success objects field-by-field and validates entry
  order with for-of. Runtime malformed available-name policy beyond blank and
  duplicate typed strings remains open rather than a new hold.
- TS repair0093 renders typed input directly; no malformed-input policy stated.
- JS generation0162 validates a fixed dense field list and copies fields
  explicitly. What normalized day fields means beyond validation needs clarity.
- JS generation0165 copies a fixed four-action list and explicit operator fields.
  Non-string action-ID coercion policy is not specified; no new hold inferred.
- ChoiceDeck listener state changes occur before notification as required;
  its hold is required-field preservation, not listener timing.

Continue at position 211. No revised partition, training seal, generation restart
or new VM. GCS verified through 159 holds; batch 14 awaits backup.
