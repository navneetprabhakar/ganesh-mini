# Rust generation review, batch 26

Positions 376–390 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; two static holds and one sandbox
hold. Total 939 unique outside-sample inspections; 444 additive plus historical
three = 447 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 376 | 0436 | Static hold: Node variants and Edit::Replace field declaration required by tests are omitted. |
| 377 | 0438 | Token acquisition/use consumption, one unauthorized retry and retained failure consumption agree. Constructor/metadata signatures partly omitted; no new concrete hold. |
| 378 | 0439 | Nonfinite input rejection, horizontal sliding and original navigation examples agree. Pitch direction convention and finite-input arithmetic overflow policy incompletely stated; no fabricated finite-output requirement. No new hold. |
| 379 | 0440 | Full Unicode alphabetic validation precedes first-scalar uppercase expansion. No new hold; elementary scope pending. |
| 380 | 0441 | Static hold: trait method signatures, receiver shape and serializer/reducer argument order required by tests are absent. |
| 381 | 0442 | Three-token Unicode-whitespace parsing and checked signed operations agree. Combined parse/operator precedence not fully specified; no new hold. |
| 382 | 0444 | Six i32 values fit exactly in i64 and f64 before multiplication; scale validation and flags agree. No new hold; elementary scope pending. |
| 383 | 0443 | Lexer byte positions, precedence/associativity and checked unary/binary arithmetic agree. Literal MIN rejection is explicitly specified. Deep recursion and combined syntax/arithmetic errors remain pending; no new hold. |
| 384 | 0445 | Required recursive pop/sort/reinsert algorithm is stable and insert goes after equals. Large recursion envelope pending; no new hold. |
| 385 | 0446 | Exact append-only event formatting and silent no-op agree. No new hold; elementary scope pending. |
| 386 | 0448 | Interning and catalog-wide fresh counter agree for reachable inspected examples. Private u64 exhaustion not executed or promoted to a demonstrated reachable defect. No new hold. |
| 387 | 0449 | Sandbox hold: sum overflow masks later allocation error despite explicit allocation-error precedence. |
| 388 | 0451 | Saturating multiplication before division and ordered projection agree with explicit tests. Final subtraction saturation is unstated; no alternate overflow oracle invented. No new hold. |
| 389 | 0452 | Ordered prefix lookup and canonical u64 LEB128 termination/overflow/minimality checks agree. No new hold. |
| 390 | 0453 | Bounded runs, repeated XOR, exact FNV tag and one-suffix removal agree. This is the stipulated codec, not authenticated encryption; no security claim inferred. No new hold. |

0436 gives objects as ordered pairs but never declares Node's variants or the
struct-style Edit::Replace { path, value } used in exact original assertions.
The fixed root-replacement algorithm itself agrees with the reference/tests.

0441 names IntoContextRow, RowSerializer and ContextCellReducer but provides
no trait signatures. Tests require unit-value serializer/reducer method calls
with borrowed Handle first and borrowed Context second. Those choices are not
defined by a semantic instruction to serialize a handle through a context.

0449: `allocation_validation_priority_probe.rs` and
`allocation-validation-priority-result.json` preserve the isolated pinned
network-disabled/resource-limited sandbox diagnostic. An allocation sequence
with units [u64::MAX, 1, 1] and an empty recipient in the final record returns
ArithmeticOverflow before reaching EmptyRecipient. The oracle follows explicit
allocation errors before arithmetic errors. Original tests put invalid
allocations first and miss this ordering. No original test was changed.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 391. No new VM or training seal.
