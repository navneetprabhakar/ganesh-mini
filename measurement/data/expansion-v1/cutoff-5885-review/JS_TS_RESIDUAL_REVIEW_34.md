# JavaScript/TypeScript residual review, batch 34

Positions 496–510 of 587. Full prompts, reference/corrected source and original
tests read; supplied known-bad source compared against reference via complete
diffs. Three new holds: 1058 additive plus historical three = **1061**;
**2,853** unique outside-sample inspections. Not admission, final rejection or
seven-criterion approval. 2026-09-07 IST.

| Position | ID suffix | Scoped finding |
| --- | --- | --- |
| 496 | javascript-generation-0363 | Hold: sum overflow makes average infinite for two identical finite MAX_VALUE readings. Numeric range and first-seen ordering of integer-like object keys need disposition. Explicit defineProperty preserves __proto__. |
| 497 | typescript-generation-0290 | Safe nonnegative validation, clamping and unchanged invalid-call state agree. Sum may exceed safe range only above the safe limit, where clamping resolves it. No new hold; low-complexity threshold pending. |
| 498 | typescript-generation-0291 | Loader called once after location validation; fresh decisions and identity reference retained as required. encodeURIComponent lone-surrogate domain needs clarity. No new hold. |
| 499 | typescript-generation-0293 | Row-major placement and zero/capacity cases agree. Large requested output requires runtime envelope; no unbounded allocation probe. No new hold. |
| 500 | typescript-repair-0195 | Inclusive threshold repair, greatest qualifying fixed band and fresh copies agree. Boundary tests kill supplied strict-comparison mutation. No new hold. |
| 501 | typescript-repair-0196 | Hold: valid non-enumerable token omitted on ordinary failure. Ordinary 2xx and revocation branches match tests; priority of success versus SESSION_REVOKED wording needs clarity. |
| 502 | typescript-generation-0289 | Typed/value errors, trimmed strings, exact contact rule and empty-note fallback agree. Multi-invalid error priority unspecified; no new hold. |
| 503 | typescript-repair-0193 | Hold: explicit UTF-16 four-unit contract contradicted by reference surrogate adjustment and original emoji test. Probe returns six-unit output for five-unit input. |
| 504 | javascript-generation-0368 | Exact tracking pattern, inclusive mass limit, optional own checks and error order agree. Meaning of present for inherited optionals needs clarity; no new hold. |
| 505 | javascript-generation-0370 | Own required fields, finite numeric validation, null-versus-zero target and detached output agree. No new hold. |
| 506 | javascript-repair-0246 | Nested Maps avoid delimiter collisions and preserve earliest route; Reflect.ownKeys checks exact own shape. Duplicate object shapes wording actually implemented/tested as repeated identity; clarity pending. No new hold. |
| 507 | javascript-generation-0376 | Explicit primitive copies, duplicate guards and descending sequence/ascending UTF-16 ordering agree. No runtime private-field bypass; no new hold. |
| 508 | javascript-generation-0378 | Optional undefined accepted explicitly, strings stay text, empty optionals omitted and nodes fresh. No new hold. |
| 509 | javascript-repair-0251 | OR primary modifiers repaired; strict booleans, Alt suppression and case folding agree. No new hold; simple repair nontriviality pending. |
| 510 | javascript-repair-0252 | Left-minus-right repaired; postfix stack, finite operation guards and documented errors agree. No new hold. |

Three isolated pinned, network-disabled, resource-limited probes failed without
timeout: sensors_0363_average [1], 452 ms; reply_0196_hidden_state [0,0,1],
2833 ms; mask_0193_utf16 [0,0,1], 2951 ms. Matching probe sources and JSON
receipts preserved. Original tests read, not rerun by these probes.
Candidate/sample/partition unchanged; candidate SHA
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
97 data tooling tests passed during batch32. GCS currently through residual480;
batches33–34 await backup. Continue511; criteria/dispositions pending.

