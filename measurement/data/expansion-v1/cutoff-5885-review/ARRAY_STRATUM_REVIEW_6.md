# Array-validation follow-up, batch 6

2026-09-06. Array-hit positions 76–90 outside the frozen sample inspected for
prompt/reference/original-test consistency: **15 new / 99 unique outside-sample
targeted inspections**. Frozen 300 unchanged; no seven-criterion approvals.
Eight reproduced diagnostic failures on seven newly held candidates, in pinned
network-disabled resource-limited sandboxes. All completed without timeouts.

| ID suffix | Finding | Result file | ms |
| --- | --- | --- | ---: |
| javascript-repair-0042 | mean of equal finite median values becomes Infinity | viewport-finite-median-result.json | 341 |
| javascript-repair-0042 | sparse measurements bypass validation | viewport-sparse-result.json | 402 |
| javascript-repair-0043 | __proto__ cache key lost | cache-proto-key-result.json | 357 |
| javascript-generation-0061 | sparse plural telemetry accepted by map | feed-sparse-result.json | 341 |
| typescript-generation-0061 | missing stage is appended without validation | stages-sparse-result.json | 2145 |
| typescript-repair-0042 | zero fade yields NaN red for finite channels | fade-zero-amount-result.json | 2375 |
| javascript-generation-0069 | pooled credits overflow before representable equal shares | loan-pool-overflow-result.json | 362 |
| javascript-repair-0045 | sparse alternatives accepted behind valid primary | asset-alternatives-sparse-result.json | 528 |

JS exits `[1]`; TS compiles then exits `[0,0,1]`. Telemetry `canHandle` correctly
returns false for the same sparse packet, but `map` yields undefined. Numeric
counterexamples have representable expected outputs: median(MAX,MAX)=MAX,
zero-amount RGB fade clamps the original channels, and two MAX balances divided
equally between two active zero-balance members each produce MAX. Original tests
omit these inputs. Total **93 additive / 96 holds including historical three**.

## Scoped negative findings and open boundaries

- JS generation0063 document views/removal: for-of validates every document
  before find/map; Gregorian month/leap checks and first-duplicate ownership
  agree with original tests. Year-zero convention is an API clarity question.
- JS generation0065 range puzzle: for-of validates history, including correct
  termination and status consistency; mapped copies follow validation. A hole
  triggers TypeError through property access, so no sparse acceptance hold.
- JS repair0044 fitRectangle maps a fixed dense argument list. Extreme ratios
  can exceed numeric representability; unlike held means, the requested scale
  itself may be unrepresentable. Keep numeric domain clarification open rather
  than asserting a representable-scale diagnostic that was not executed.
- JS generation0062 field model: both creation and event application use for-of
  validation before copies. `copyItems` is unused; its map is not an exposed
  bypass. Blur semantics for differing model/event values need wording review.
- TS generation0064 reservation store: constructor for-of validates elements;
  query maps use dense Map values. Object-spread update may accept extra fields
  (including an ID carried on a structurally assignable variable); typed patch
  scope versus runtime rejection/ignoring extras remains an API review item.
- TS generation0066 NavController: sparse arrays are not explicitly addressed
  by its empty-ID/label contract; retain clarity finding rather than automatically
  holding it. Ordinary copied entries, disabled checks and state-before-callback
  behavior agree with tests.
- JS generation0067 PermitLedger: map/filter operates on Map-derived dense data,
  integer boundaries and copies agree with tests. Equipment whitespace handling
  is not fully explicit. Public storage property is not itself a returned-array
  alias diagnostic; no unexecuted private-state claim.
- JS generation0070 route manifest: split-derived arrays are dense; malformed
  query/fragment/empty segments skipped and reserved findings preserve ordering.
  Root-only route cannot produce a reserved finding, so its omission is not an
  observable counterexample here.

Continue at array-hit position 91 in the immutable inventory. No candidate
rewrite, generation restart, revised partition, training seal, or new VM.
