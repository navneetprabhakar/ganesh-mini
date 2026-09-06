# Array-validation follow-up, batch 7

2026-09-06. Array-hit positions 91–105 outside the frozen sample inspected for
prompt/reference/original-test consistency: **15 new / 114 unique outside-sample
targeted inspections**. Frozen 300 unchanged; not seven-criterion approval.
Nine diagnostic failures on eight new held records, all in pinned network-
disabled resource-limited sandboxes, no timeout.

| ID suffix | Finding | Result file | ms |
| --- | --- | --- | ---: |
| javascript-repair-0048 | sparse handlers bypass pre-invocation validation | dispatch-sparse-atomic-result.json | 395 |
| typescript-generation-0072 | valid non-enumerable required ID lost in copy | subscriber-hidden-id-result.json | 2039 |
| javascript-generation-0078 | sparse choices accepted | dependent-choices-sparse-result.json | 326 |
| javascript-generation-0078 | empty string code rejected despite unrestricted string code type | dependent-empty-code-result.json | 349 |
| javascript-repair-0049 | sparse invoice lines accepted | invoice-sparse-result.json | 408 |
| javascript-repair-0050 | sparse records accepted | detach-sparse-result.json | 425 |
| javascript-repair-0051 | earlier pipeline step runs before malformed hole rejected | pipeline-sparse-atomic-result.json | 378 |
| javascript-generation-0076 | nested successful open shares outer ticket ID | repair-desk-reentry-result.json | 330 |
| javascript-generation-0084 | sparse menu records accepted | menu-records-sparse-result.json | 457 |

JS exits `[1]`; TS compiles then exits `[0,0,1]`. Original tests omit these
inputs. Subscriber input retains all declared fields and types: only the ID
property's enumerability differs. Dependent options explicitly restrict labels
to non-empty strings, but do not impose that restriction on codes. The reentry
probe is bounded to one nested synchronous open, with no throw or side-channel
mutation; both opens return ID 1. Reference commit ordering overwrites the
nested ticket. Callback reentry needs an explicit contract/implementation policy
before this candidate can pass; do not silently rewrite original tests.

Totals: **101 additive / 104 holds including historical three**.

## Scoped negative findings and open boundaries

- JS repair0046 bounded scroll validates a fixed dense argument list. Overflow
  in start+delta is bounded by the following clamp, unlike the held averaging
  examples. No blanket overflow hold; ordinary boundary tests cover remainder.
- JS repair0047 channel matcher uses dense split arrays and checks final wildcard
  placement before matching. Zero-tail wildcard fix agrees with tests.
- TS generation0067 path utilities use for-of traversal and dense collected
  results. Sparse Scalar formatting scope is unspecified; functions as traversable
  objects need API wording review, not an invented failure label.
- TS generation0068 ModeClassManager normalizes with Set and owns copied arrays.
  Invalid typed mode/initial elements have no explicit runtime rejection policy.
  Disposal and restoration agree with original tests.
- TS repair0047 ProductInserter explicitly reads all required fields into a
  new object, so Object.values sees fixed dense fields. Sink failure is caught;
  fresh loadKinds arrays reflect current source. Missing-field runtime handling
  is not specified beyond the required interface.
- JS generation0073 stock book maps Map/private log data, no sparse input array.
  localeCompare versus unspecified lexicographic ordering and integer accumulation
  representability remain API/numeric review items, not executed defects here.
- JS generation0083 bag codec uses explicit enumerable-key scope, dense keys/
  split arrays and a null-prototype decode target. No __proto__ assignment loss
  inferred. Lone-surrogate encodeURIComponent limitations need domain clarity.
- JS repair0050 original tests additionally assume key trimming although the
  prose only says non-empty; retain this inherited-contract clarity question.
- JS repair0049 arbitrary-length decimal prices may exceed number range, but
  no finite representable-total overflow counterexample was executed here.

Continue at array-hit position 106 in the immutable inventory. No candidate
rewrite, generation restart, revised partition, training seal, or new VM.
