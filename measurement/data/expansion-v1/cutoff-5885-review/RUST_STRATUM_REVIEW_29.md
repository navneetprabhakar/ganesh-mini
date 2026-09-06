# Rust generation review, batch 29

Positions 421–435 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; one new static contract/test hold.
Total 984 unique outside-sample inspections; 449 additive plus historical three
= 452 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 421 | 0486 | Exact five fields, literal whitespace, unique ordered key/value pairs and dash sentinel agree. No new hold. |
| 422 | 0490 | Explicit wrapping operations and nested module API agree. No new hold; elementary scope pending. |
| 423 | 0491 | Ordered flags, include consumption, terminator, positional limit and final scan dependency agree. No new hold. |
| 424 | 0487 | Static hold: original tests require query arity rejection, but prompt constrains equal arity only for observations and otherwise specifies fallback for no exact feature match. |
| 425 | 0489 | Validated half-open extent ranges, checked ends and stable removals agree. Combined duplicate/overlap ordering not frozen; no new hold. |
| 426 | 0492 | Section parsing, exact character sets, duplicates and physical numbering agree with tests. Exact heading versus trimmed heading interpretation remains pending; no new hold. |
| 427 | 0493 | ASCII token parsing, checked left-to-right offset and owned identifier agree. Most-specific combined syntax-error policy partly implicit; no new hold. |
| 428 | 0494 | Exact reset request grammar, identifiers and nonmutating error replies agree. No new hold; elementary scope pending. |
| 429 | 0496 | Strict positive intersection and widened dimensions support full i32 valid coordinate range. No new hold. |
| 430 | 0497 | Reverse cumulative stanzas, oldest-item suffix and literal strings agree. No new hold; elementary scope pending. |
| 431 | 0499 | Ordered recursive paths and cloned atomic descendants preserve duplicate fields. Deep recursion envelope pending; no new hold. |
| 432 | 0501 | Explicit validation order, checked public counter and owned sessions agree. No new hold. |
| 433 | 0502 | Finite-input validation, dot-product formula and basic intersections agree. Finite intermediate/output handling and numerical robustness are unspecified; not promoted to a fabricated finite-output rule. No new hold. |
| 434 | 0503 | Exact key validation, strictly increasing revisions, owned reads and ordered keys agree. No new hold. |
| 435 | 0504 | Name/path checks, exact default contents, substitution and sorted owned files agree. Cross-platform drive-prefix/NUL path interpretation is unstated; this is an in-memory renderer, not an executed filesystem write. No new hold. |

0487: The prompt says every observation/query has at least one feature and
all observations for one model have the same feature count. It then specifies
an all-outcome fallback whenever no observation features exactly equal a query.
The original tests instead require ArityMismatch for a nonempty one-feature
query against a two-feature model, and the reference enforces that unstated
query restriction. The prompt should explicitly decide whether such queries
are invalid or use fallback. Update append-versus-replace semantics and the
scope of "derive ... where applicable" are additional unresolved questions.
This is a static contract/test comparison, not a new execution failure.

No new sandbox executions in this batch. Original tests/candidates unchanged.
Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 436. No new VM or training seal.
