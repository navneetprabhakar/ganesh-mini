# Rust generation review, batch 37

Positions 541–555 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; two sandbox-confirmed holds.
Total 1,104 unique outside-sample inspections; 466 additive plus historical
three = 469 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 541 | 0634 | Sandbox hold: unknown option in command position returns UnknownCommand rather than Unexpected. Ordinary commands/options agree; option-looking operands remain pending. |
| 542 | 0635 | Sandbox hold: forbidden explicit null is deferred past later invalid tracing, contradicting left-to-right first-error rule. Ordinary settings/defaults agree. |
| 543 | 0636 | Viewport, winding, validation and interpolation agree on inspected paths. Outside-edge tolerance remains pending; no new hold. |
| 544 | 0631 | Six bitfields validate widths and preserve unrelated bits. No new hold. |
| 545 | 0637 | Educational envelope roundtrip and tamper tests agree; algorithm deliberately not pinned. Not a production cryptography claim. Capacity envelope pending; no new hold. |
| 546 | 0641 | Reservations, capacity, overwrite, commit and interrupt behavior agree. Commit versus reservation order wording and private token exhaustion remain pending; no new hold. |
| 547 | 0642 | Explicit crate::alpha path matches original crate-root import and saturating metrics. No new hold. |
| 548 | 0643 | Shape/output length and each i64 multiplication/addition checked. Huge zero-column loop and allocation envelope remain unexecuted; no new hold. |
| 549 | 0645 | Async zone parsing, exact separators, parse-before-bounds and signed minimum handling agree. No new hold. |
| 550 | 0646 | Glyph strings, conversions and standard hashing agree. No new hold. |
| 551 | 0648 | Stable in-place retain is constant auxiliary space and leaves reversed intervals unchanged. No new hold. |
| 552 | 0649 | Destructuring returns disjoint borrows in requested 0,2,1,3 order without copy or mutation. No new hold. |
| 553 | 0650 | Ordered byte conversion, bounded chunks and first sink error agree. Up-front chunk_size allocation even for empty input remains a resource-boundary concern, not newly executed. No new hold. |
| 554 | 0651 | Canonical maximum-count splitting, little-endian encoding and checked combined length agree. Allocation beyond isize bounds remains unexecuted; no new hold. |
| 555 | 0652 | Exact badge styles, toggling and original-character escaping agree. No new hold. |

0634: invocation_unknown_option_probe.rs supplies ["--unknown"]. Reference
returns UnknownCommand("--unknown") instead of the specified Unexpected.
invocation-unknown-option-result.json records compile 0, test 101, 1,943 ms,
no timeout.

0635: profile_null_priority_probe.rs supplies endpoint=null;tracing=bad with
reject_null_required true. Reference reports InvalidValue for tracing rather
than NullEndpoint for the first segment. profile-null-priority-result.json
records compile 0, test 101, 1,764 ms, no timeout.

Both probes ran in the pinned Rust 1.85.0 network-disabled, resource-limited
sandbox. Original tests and candidates remain unchanged. Frozen SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 556. No new VM or training seal.
