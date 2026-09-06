# Rust generation review, batch 35

Positions 511–525 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; two new sandbox-backed holds.
Total 1,074 unique outside-sample inspections; 463 additive plus historical
three = 466 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 511 | 0594 | Requested trait directions, field order, Rust decimal parsing and strict booleans agree. No new hold. |
| 512 | 0595 | Sandbox hold: JSON list renderer leaves raw control characters. Locator and graph/source ordering agree. |
| 513 | 0596 | Pre-call validation, single load/execute, phase selection and exact mismatches agree. No new hold. |
| 514 | 0597 | Key/separator/message byte order and eight-byte XOR accumulation agree. Explicitly educational, not cryptographic security; no new hold. |
| 515 | 0598 | Borrow/mutate/consume pattern matching and ordinary arithmetic follow explicit build-profile overflow rule. No new hold. |
| 516 | 0599 | Relative traversal, sibling uniqueness and atomic additions agree. Invalid parent-name precedence and public malformed trees/deep recursion remain pending; no new hold. |
| 517 | 0601 | Staged batch clone preserves logical atomicity and ordered dependencies. Empty batch replaces allocations but not logical contents; malformed externally built state and deep values remain pending. No new hold. |
| 518 | 0602 | Blanket unsized coordinates, finite-input validation and direct max absolute difference agree. Unrepresentable finite-coordinate differences can yield infinity; no finite-result requirement added. No new hold. |
| 519 | 0605 | Checked byte spans, failed-materialization atomicity, owned content and append spans agree. DefaultHasher exact algorithm unspecified by prompt and tests; no new hold. |
| 520 | 0606 | Sandbox hold: document cache JSON leaves raw controls in document names and values. Sorting and ID rules agree. |
| 521 | 0607 | Ordered matching, once removal and captured state agree. Callback unwind behavior and private ID exhaustion unspecified/unexecuted; no new hold. |
| 522 | 0610 | Required registration validation and atomic update agree. Registration session-key scope and exact six-line output with embedded newlines remain ambiguous; secret-display design is explicitly requested, not production endorsement. No new hold. |
| 523 | 0612 | Borrowed codebooks and every matching entry in insertion order agree. Built-in name strings unspecified but original expectations derive from name(), not hardcoded labels. No new hold. |
| 524 | 0611 | Maximal increasing-run sums, including all-negative runs, agree with widened accumulation. No new hold. |
| 525 | 0613 | Named renderers, closed dispatch and owned title copies agree. No new hold; elementary scope pending. |

0595: `json_control_render_probe.rs` ran against the unmodified reference in
the pinned network-disabled, resource-limited Rust 1.85.0 verifier. Compile
0/test 101, 1,690 ms, no timeout. A list string containing NUL, backspace and
form feed yielded raw bytes below 0x20 in the rendered output. Those bytes
must be escaped in JSON strings. The probe does not demand a particular
choice of legal escape spelling. Result: `json-control-render-result.json`.

0606: `document_json_control_probe.rs` used the same sandbox contract.
Compile 0/test 101, 1,771 ms, no timeout. A NUL in document name and backspace
in value remained raw in cache_json. The prompt requires a JSON object and
does not restrict these input characters. Original tests cover only the five
listed escape cases and miss other JSON control characters.
Result: `document-json-control-result.json`.

Original tests/candidates unchanged. Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 526. No new VM or training seal.
