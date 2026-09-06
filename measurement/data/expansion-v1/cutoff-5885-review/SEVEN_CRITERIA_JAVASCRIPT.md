# JavaScript frozen-sample criterion dispositions — 2026-09-07

All 30 frozen JavaScript sample records: 10 positive seven-criterion decisions,
20 holds (15 existing, five new). Initial complete prompt/reference/test/mutant
inspections are in THIRD_BATCH_REVIEW.md; open contracts and elementary repairs
were reread for this adjudication. No new execution is claimed here.
Candidate SHA: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
Criteria and patch-size policy follow SEVEN_CRITERIA_GO.md. All 30 have archived
independent test lineage and standard-library-only dependencies. Positive review
is not training admission. Holds are reversible, not final rejection.

## Positive decisions (10)

Prefix: exp-v1-javascript-.

| ID suffix | Basis / resolved concern |
| --- | --- |
| generation-0006 | Ordered per-job steps, synchronous callback validation, detached state and idempotent approval. No fabricated rollback guarantee for user callback exceptions. |
| generation-0124 | Map equality, recency and least-recent eviction with explicitly shared element references. TypeError is a permissible rejection of invalid capacity; the meaningful mutant changes eviction, not an unspecified error class. |
| generation-0196 | Division-based bounded integer square-root search and exact safe-integer boundary handling. |
| generation-0230 | Canonical decimal grammar and exact field ordering with primitive-string validation. |
| generation-0374 | Complete line validation, quantities and explicit JavaScript arithmetic; extent grammar and canonical Number rendering. Neither finite output nor arbitrary-precision arithmetic is promised. No invented overflow failure. |
| repair-0054 | Own-property-safe JSON cloning, sparse rejection, ancestor-cycle detection and retained independent header normalization. No unspecified symbol-header guarantee. |
| repair-0096 | Explicit ready-state transition, queue detachment, reentrant registration and exception/no-replay behavior. |
| repair-0144 | Indexed sequence semantics, complete sparse-aware validation and independent returned objects. |
| repair-0147 | Stateful GET-only cache, validation-before-POST return and input/output copies. Supplied source explicitly defines trim-based request validation; preserve that repair context. |
| repair-0249 | Explicit immediate-predecessor rule governs matching, including a possible suffix after a dot. No additional maximal-token parser was promised. Source supplies the right boundary; repaired left boundary distinguishes identifier suffixes. |

## Held decisions (20)

| ID suffix | Blocking evidence / criterion |
| --- | --- |
| generation-0160 | Existing mutant differs only in an unspecified return value demanded by tests. |
| generation-0233 | Existing sparse validation gap and additional async-function identity/API constraints. |
| generation-0241 | Existing explicit default argument versus no-argument rejection contradiction. |
| generation-0292 | Existing executed boxed-command acceptance. |
| generation-0173 | Existing sparse media validation gap. |
| generation-0206 | Existing sparse record validation gap. |
| generation-0218 | New static contract hold: nonempty address/account/selection strings are narrowed to trimmed-nonblank by reference and original tests, without source context or specification for that restriction. |
| generation-0254 | Existing executed same-unit finite value becoming Infinity. |
| generation-0296 | Existing executed own-__proto__ copy/state alias defect. |
| generation-0319 | Existing sparse topic validation gap. |
| generation-0335 | Existing executed safe-integer page arithmetic defect. |
| generation-0339 | Existing executed omitted-handler acceptance. |
| generation-0394 | Existing executed hidden own patch property accepted. |
| repair-0111 | Existing sparse validation failure; elementary missing declaration is an additional non-triviality concern. |
| repair-0132 | Existing sparse cell validation failure. |
| repair-0227 | New non-triviality hold: explicitly disclosed two-characters-per-byte factor in a direct pairwise decode loop. Correctness/tests are not the reason for this qualitative hold. |
| repair-0229 | New non-triviality hold: remove an expressly identified falsy-zero guard in a validation-and-format wrapper. |
| repair-0231 | New non-triviality hold: replace one returned array reference with an empty literal, beside two identical empty literals, in an elementary spread wrapper. |
| repair-0239 | New non-triviality hold: reverse a direct source/target computed-property assignment in a shallow-copy wrapper. No non-enumerable-copy failure claimed. |
| repair-0240 | Existing executed sparse route construction failure. |

Repeated elementary repair targets reopen their full lane/source/task/history
stratum for focused non-triviality checks. Prior sparse/semantic inspections
do not automatically satisfy this newly adjudicated criterion.
