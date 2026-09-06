# Go frozen-sample criterion dispositions — 2026-09-07

Scope: all 56 original Go sample records, unchanged selection. These decisions
use FIRST_BATCH_REVIEW.md, SECOND_BATCH_REVIEW.md, the original REVIEW.md and
the all-300 test-origin chain audit. The open cases below were reread against
the full frozen prompt/reference; no new candidate execution is claimed.
Candidate SHA: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

Seven criteria mean prompt clarity, API consistency, independent test origin,
non-triviality, idiomatic code, dependency isolation and realistic known-bad
failure. A small patch is not itself trivial: an ordering, ownership, numeric
boundary or validation interaction in a substantive complete program can pass.
Conversely, a literal change in an otherwise elementary loop does not become
substantive merely by surrounding it with tests or boilerplate. This is reviewer
judgment under the existing criterion, not a measured model-learning result.

All 56 have verified archived specification-only test lineage and inspected
standard-library dependencies. Those two criteria do not establish behavioral
correctness. Positive decisions below cover all seven criteria, not corpus
admission: unresolved systematic strata and existing execution holds still bind.

## Positive sample decisions (39)

IDs below have prefix `exp-v1-go-`. Record-specific original review notes retain
the known-bad mutation and test checks; these are not newly executed results.

| ID suffix | Basis for retaining all-seven-criterion approval |
| --- | --- |
| generation-0251 | Alias-directory semantics, detached state and realistic lookup mutation; prior full review retained. |
| generation-0491 | Attempt limits, halt-before-repeat ordering and original error identity; prior full review retained. |
| generation-0549 | Byte grammar, length boundary, exact handler call and error masking interact. |
| generation-0715 | Ordered budgeted handlers, independent buffers, retained error identities and partial execution. |
| generation-0052 | Specific verbatim-label format governs content; one serialized record/write is not an added ban on label newlines. Mutex protects destination and complete writes. No prompt edit or added escaping. |
| generation-0124 | Archive state, credential precedence and copied related records. |
| generation-0128 | Transition validation, identifiers and atomic failed acceptance/finish. |
| generation-0138 | Deterministic authenticated encoding and strict decoding; educational contract, not production security certification. |
| generation-0208 | Pool ownership, reset on both boundaries and concurrency without required object reuse. |
| generation-0302 | Invalid enum handling, inclusive severity boundary and stable filtering. |
| generation-0351 | Exact scoped matching, ambiguity precedence and validating only the uniquely selected row. |
| generation-0354 | Full validation, copied overrides and nil-receiver behavior. |
| generation-0388 | CSV parsing, byte grammar, duplicate detection and deterministic sorting. |
| generation-0397 | Scoped keys, presence-based lookup, duplicate collapse and sorted independent results. |
| generation-0405 | Finite decimal validation, unit grammar and distinct zero/NaN behavior. |
| generation-0560 | Reverse precedence, map membership rather than truthiness, and no partial output. |
| generation-0680 | Exact structured parse, selective case folding and canonical rendering. |
| generation-0690 | Nested defensive copies, scoped identity, locked CRUD and concurrency tests. |
| generation-0780 | ASCII tokenization, distinct-term scoring, ties and stable multi-key ordering. |
| generation-0827 | Generation tracking, scoped length-prefixed keys and observer snapshot semantics. |
| generation-0834 | Framing, numeric limits, byte decoding, uniqueness and atomic malformed input. |
| repair-0545 | Exact source enumerates eight errors and all required checks identify them; introductory count 'six' is a copyediting defect, not an unresolved symbol/signature choice. Error identity and validation-order repair remain substantive. |
| repair-0552 | Hierarchical boundary matching, bitmasks and nested copy isolation. |
| repair-0360 | Zero-value catalog, duplicate removal, category cleanup and independent sorted snapshots. |
| repair-0392 | Strict JSON document boundary, wrapped errors, copied ordered artifacts. |
| repair-0456 | Inclusive capacity limits, nil precedence, locking and copied snapshots. |
| repair-0465 | Ordered transactional changes and rollback checks not dependent on random map iteration. |
| repair-0500 | Locked allocation, immutable assigned IDs, validation and sorted CRUD. |
| repair-0504 | Fleet state transitions, default selection, defensive copies and failure atomicity. |
| repair-0523 | Bounded Gregorian arithmetic, direction and leap-century boundaries. |
| repair-0190 | Supplied source distinguishes named query arguments from order elements; preserve existing empty-query validation. Boundary correction must still handle duplicates, reversed/equal queries and detached slices. No new empty-order-element restriction. |
| repair-0055 | Full int64 inclusive domain, singleton safety, signed truncation and binary rendering. Extra bounded big.Int operations and compact inherited formatting are not enough to fail idiomatic code. |
| repair-0056 | Copy-before-sort plus endpoint parity, duplicates and empty-result isolation. |
| repair-0115 | Full supplied source explicitly rejects empty keys; retaining that validation is compatible with this targeted value/revision comparison repair. Ordered change classification is substantive. |
| repair-0125 | Unicode rune selection, empty/singleton semantics and palindrome boundaries. |
| repair-0245 | Complete rule validation, ordered matching, wildcards and conjunction semantics. |
| repair-0269 | Segment validation and exact/descendant boundary matching. |
| repair-0280 | Normalized uniqueness, port bounds, duplicate rejection and atomic result. |
| repair-0324 | Arbitrary-precision accumulation, rune counting, tie stability and copied storage. |

## Held sample decisions (17)

Hold is exclusion from current training admission, not deletion, a final rejection
or a claim that an entire VM campaign failed. Other criteria cannot rescue a
blocking result. Unlisted criteria on newly held rows are not automatically
granted a pass; the original detailed notes remain the evidence.

| ID suffix | Blocking criterion / disposition |
| --- | --- |
| generation-0165 | Existing historical behavioral hold: premature ticket consumption. |
| generation-0058 | Existing known-bad rejection reliability hold: preserved repeatability runs differ. Independence and realistic mutation do not waive intermittent false acceptance. |
| generation-0330 | Existing API/behavior hold: empty-valued labels with different keys compare equal. |
| generation-0720 | Existing API/behavior hold: ready-step priority after newly unblocked work. |
| generation-0791 | Existing API/behavior hold: case-inexact JSON keys accepted. |
| generation-0137 | Non-triviality not met: fixed-character repetition plus two independent guards; no substantive interaction beyond elementary library operations. |
| generation-0416 | Non-triviality not met: fixed marker concatenation or identity, with inert immutable fields and empty-marker guard. |
| generation-0270 | API consistency not met: explicit prohibition on global mutable state versus package-level mutable map recorderLevels. Static evidence, not a new race or mutation execution. |
| generation-0361 | Prompt clarity unresolved: unrestricted int64 epoch input versus YYYY date rendering, with no supported year-width/range policy. Do not silently add a timestamp limit or claim an executed overflow. |
| generation-0366 | API/test consistency unresolved: tests require zero result on error, while only successful result is specified. A conventional Go choice is not an explicit required return contract. |
| generation-0767 | Prompt clarity/API conflict: mandatory consume-on-validly-formed Enter versus overflow-without-changing-state. Reference deletes challenge before exhaustion check. No feasible counter-exhaustion execution claimed. |
| repair-0025 | Non-triviality not met: prompt identifies wrong start position in a single elementary stride sum. |
| repair-0034 | Non-triviality not met: supplied element formula directly identifies the sole index-expression correction in an elementary allocation loop. |
| repair-0097 | Non-triviality not met: elementary truth-table inversion; guard/byte-format checks do not make this target substantive. |
| repair-0099 | Non-triviality not met; unrestricted recursive domain versus tests through 1000 also leaves a resource-envelope question. |
| repair-0143 | Non-triviality not met: remove a normalization call to preserve a literal token comparison. |
| repair-0259 | Non-triviality not met: reverse explicitly named substring operands in otherwise direct nested selection. |

Twelve new quality holds join five existing Go sample holds. Repeated elementary
targets reopen Go first-pass generation and repair for this criterion; their
combined population is 798 (526 generation, 272 repair), including 41 frozen
sample records. This requires 757 additional outside-sample checks, not 798
automatic rejections. Repair scope here is MdEval-Instruct: seven other Go
first-pass repair sample rows come from McEval-Instruct and are outside this
new group. Do not close admission from the completed v6 inventory:
record a new scope version preserving v6 as historical coverage evidence.

These decisions do not approve any non-sample Go row. No data edits, altered
sample, new generation, training seal or VM are authorized by this report.
