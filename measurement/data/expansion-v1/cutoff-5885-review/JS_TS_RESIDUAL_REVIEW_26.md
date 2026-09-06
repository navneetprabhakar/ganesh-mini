# JavaScript/TypeScript residual review, batch 26

Positions 376–390 of 587. Full prompts, reference/corrected source, original
tests and supplied known-bad source read. Three new holds: 1033 additive plus
historical three = **1036**, **2,733** unique outside-sample inspections.
Not final rejection, admission or seven-criterion approval. 2026-09-07 IST.

| Position | ID suffix | Scoped finding |
| --- | --- | --- |
| 376 | javascript-repair-0181 | ASCII trim and first-occurrence own-key handling repaired. Name domain excludes numeric/prototype key pitfalls; malformed duplicate segments still validated. No new hold. |
| 377 | javascript-repair-0182 | Null-prototype definition/cache maps, cycle exposure and retry deletion agree. Enumerable symbol definition scope needs clarity; no new hold. |
| 378 | typescript-generation-0229 | Hold: locale ordering differs from code-unit lexicographic ordering for a,A. Prompt says lexicographic without defining collation; ordering disposition pending, not an unambiguous UTF-16 requirement. |
| 379 | typescript-generation-0232 | Update-before-listener snapshot, unchanged no-event and exception propagation agree. Duplicate subscriptions and explicit undefined default remain clarity items; no new hold. |
| 380 | typescript-generation-0233 | Three traversal orders and odd/even outside-in bounds agree. Safe-count versus array-capacity runtime envelope pending; no huge execution or new hold. |
| 381 | typescript-repair-0155 | Flip-current clears selection; duplicate/unknown keys and returned order copies agree. No new hold. |
| 382 | typescript-repair-0156 | Correct modulo repairs length-minus-one bug; empty RangeError, copied sequence and retained element identities agree. No new hold. |
| 383 | typescript-generation-0234 | Hold: sparse snapshot array bypasses string validation via forEach and becomes empty strings. Bounds and ordinary copy isolation agree; capacity envelope remains pending. |
| 384 | typescript-repair-0153 | Zero quantity and exact relational sorting repaired. Validation-before-mutation and fresh result records agree. No new hold. |
| 385 | javascript-generation-0278 | Finite integer checks, ranges, padded format and validation state agree. No custom property tampering assumed; no new hold. |
| 386 | javascript-generation-0280 | Plain context, every finished entry, active precedence and HTML escaping agree. No new hold. |
| 387 | javascript-generation-0282 | Exact ternary messages and strict types agree. Very low task complexity requires nontriviality disposition; no semantic hold. |
| 388 | javascript-repair-0185 | Hold: safe integer 999999999999999 falsely accepted as a power of ten due to log10 rounding. Positive guard fixes negative inputs but not exactness. |
| 389 | javascript-repair-0187 | Width advancement repaired; row maximum height and boundary placement agree. Extreme numeric arithmetic envelope remains clarity, not an executed finding. No new hold. |
| 390 | javascript-generation-0283 | Own sparse-index traversal and enumerable Object.keys order agree; accumulator identity and callback exceptions preserved. Callback mutation/inherited index semantics need clarity; no invented snapshot guarantee or new hold. |

Three isolated pinned, network-disabled, resource-limited probes failed without
timeout: directory_0229_order [0,0,1], 2300 ms; segment_0234_sparse [0,0,1],
2231 ms; power_ten_0185_rounding [1], 482 ms. Power probe stopped at its first
assertion, so no claim about the second value. Matching `_probe` sources and
`_probe-result.json` receipts retained. Original tests read, not rerun by probes.
Frozen candidate/sample/partition unchanged; candidate SHA
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
Latest tooling check: 97 passed at batch24. GCS verified through residual360
/1028 holds; batches25–26 await backup. Continue391; criteria/dispositions pending.
