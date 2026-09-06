# Rust generation review, batch 34

Positions 496–510 of the 684-record outside-sample queue. Fifteen full prompt,
reference and original-test inspections; one new sandbox-backed hold.
Total 1,059 unique outside-sample inspections; 461 additive plus historical
three = 464 holds. Inspection is not seven-criterion approval.

| Position | Generation ID | Scoped finding |
| --- | --- | --- |
| 496 | 0574 | Raw escape preservation across two separator scans and decoded field validation agree. Supported escapes cannot yield a known alphabetic key from a differently escaped name; that requirement is vacuous. No new hold. |
| 497 | 0577 | Widened products and checked coefficient accumulation agree. Allocation failure/oversize-result envelope remains pending; no new hold. |
| 498 | 0578 | One-pass five-character escape, replacement mounting and independent clearing agree. No new hold. |
| 499 | 0579 | Trim validation with original string retention, borrowed reads and ordinary IDs agree. Private exhaustion not executed; no new hold. |
| 500 | 0580 | Canonical Tick codec, checked elapsed difference and nondecreasing journal agree. No new hold. |
| 501 | 0581 | Left-to-right shrink and ordinary widened placement agree. u64 sum can theoretically overflow above 4.29 billion MAX-width items; large-input/output representability envelope pending, not executed. No new hold. |
| 502 | 0582 | Exact header, ordered validation and tagged prefix agree. No new hold. |
| 503 | 0583 | Sorted per-stream counts and non-inserting reads agree. Saturation visible in code but private MAX counters not executed. Constructor free-versus-associated presentation pending; no new hold. |
| 504 | 0584 | Sandbox hold: byte length misclassified as character limit, masking first nonprintable byte below stated character limit. |
| 505 | 0585 | Missing-versus-empty data and exact ordered rendering agree. No new hold; elementary scope pending. |
| 506 | 0586 | Required-artifact priority, ordered models and sorted additional entries agree. Required names used as model names not excluded by prompt; no new hold. |
| 507 | 0590 | Unicode scalar palindrome DP and vector lexicographic tie-break agree. Repeated substring tests/cloning have high polynomial cost; resource envelope pending, no new hold. |
| 508 | 0591 | Register-before-label validation, second-pass unknown targets and exact rendering agree. No new hold. |
| 509 | 0592 | Incremental prime testing uses division to avoid square overflow. Full-u64 search/resource boundary is not executed; no new hold. |
| 510 | 0593 | Mask replacement, clear and zero-mask behavior agree. No new hold; elementary scope pending. |

0584: `banner_character_count_probe.rs` ran against the unmodified reference in
the pinned network-disabled, resource-limited Rust 1.85.0 verifier. Compile
0/test 101, 1,594 ms, no timeout. A string of 32,768 copies of é contains fewer
than u16::MAX characters but 65,536 UTF-8 bytes. Reference returns TooLong,
not NonPrintable at byte index zero. Prompt limits characters and explicitly
requests the first rejected UTF-8 byte for non-ASCII input. Preserve this
counterexample; no original test or candidate modified.
Result: `banner-character-count-result.json`.

Frozen candidates SHA-256:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Scope v6 unchanged. Continue 511. No new VM or training seal.
