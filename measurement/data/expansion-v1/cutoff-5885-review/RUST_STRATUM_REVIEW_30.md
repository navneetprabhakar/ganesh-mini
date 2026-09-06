# Rust generation review, batch 30

Positions 436–450 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; two new static contract/test holds.
Total 999 unique outside-sample inspections; 451 additive plus historical three
= 454 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 436 | 0500 | Checked stack operations and jump/end/halt rules agree. Invalid untaken target rejects in original test; no termination guarantee/fuel bound specified for cyclic programs. No new hold. |
| 437 | 0505 | Count/last-index sorting agrees. Distinct summaries cannot share a last index, so numeric tie-break is unreachable despite original-test comment; no new hold. |
| 438 | 0506 | Exact masked snapshot fields and immutable trait reads agree. No new hold; elementary scope pending. |
| 439 | 0507 | Required singletons, literal contents, selector order and missing-field line zero agree. CRLF/literal carriage-return interpretation remains pending; no new hold. |
| 440 | 0508 | Exact keys, strict ASCII u128 values and vacancy semantics agree. No new hold. |
| 441 | 0509 | Static hold: original test rejects dot-only suffix despite prompt allowing any nonempty combination of listed characters. |
| 442 | 0510 | Ordered firing/retargeting, initial dead counts and entire-tick escaping before next-tick stop agree. No new hold. |
| 443 | 0512 | Exact-key replacement, owned sorted reads and stated traits agree. No new hold. |
| 444 | 0514 | Present-empty required values, optional emptiness and duplicate detection before normalization agree. No new hold. |
| 445 | 0511 | Decimal ID and canonical paused codec agree with original tests. Absent value versus absent field wording and empty semicolon fields remain ambiguous; no new hold. |
| 446 | 0516 | Static hold: original duplicate-import assertion requires Catalog equality not included in exact API traits. Behavior including reachable maximum-ID creation agrees. |
| 447 | 0518 | Newline records, one terminal carriage-return removal and borrowed indexed lookup agree. No new hold. |
| 448 | 0520 | Widened fixed-point scaling and post-scale mirror follow exact point order at edge limits. No new hold. |
| 449 | 0521 | Exact route/method priority and literal request matching agree. No new hold; elementary scope pending. |
| 450 | 0522 | Component validation, syntax ordering, alias-free identity/hash and scoped display behavior agree. Combined malformed-component priority partly implicit; no new hold. |

0509: The prompt's domain is nonempty lowercase ASCII letters, digits, dots
or hyphens. The original rejects_invalid_rule_suffixes test includes ".",
which satisfies that declared grammar. The reference adds an unstated
requirement for at least one letter/digit. Preserve as a contract/test hold;
no new execution is claimed.

0516: The exact Catalog declaration requests Debug and Clone only. The
duplicate_import_is_rejected test calls assert_eq! on Result<Catalog,
CatalogError>, requiring Catalog: PartialEq even when comparing against Err.
The reference adds equality traits and therefore passes; an implementation
with precisely the requested traits cannot compile that assertion. This is
an unrequested test requirement, not a reference-runtime defect.

No new sandbox executions in this batch. Original tests/candidates unchanged.
Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 451. No new VM or training seal.
