# Array-validation follow-up, batch 30

Positions 436–450: **14 new**, one repeated inspection / 457 unique outside-
sample inspections. Six new holds: **307 additive / 310 including historical
three**. Full prompts, references and original tests inspected.

| Position | Candidate | Scoped finding |
| --- | --- | --- |
| 436 | JS repair0233 | Object.is suffix symmetry search and primitive-only policy; undefined explicitly allowed, no distinct missing-slot rejection rule. No new hold. |
| 437 | JS repair0235 | Duplicate of initial targeted inspection; NOT counted again. Internal dense listeners copied before emission; first-occurrence removal correct. |
| 438 | JS repair0236 | Full breakpoint validation before callbacks; Set preserves execution order. Missing steps eventually throw, but pre-callback validation guarantee explicitly names breakpoints; leave broader malformed-step timing for oracle review. No new hold. |
| 439 | JS generation0352 | Bounded 150000-element encoder args overflow function argument spreading. encode-batch-bounded-large-args-result.json, 370 ms, RangeError, no timeout. Other helpers validate via for-of and use required intentional identities. |
| 440 | JS generation0355 | Required inventory name lost from copied record. inventory-required-name-result.json, 417 ms. |
| 441 | JS generation0358 | for-of path checks and dense split segments, exact zip/deps filtering, fresh arrays. Cross-platform drive-letter policy not imposed without specified path platform. No new hold. |
| 442 | JS repair0237 | Own-index density validation explicit; correct one-based third partition, preserved identities. No new hold. |
| 443 | JS repair0238 | Own-index density/string validation before trim/lowercase and Set. No new hold. |
| 444 | TS generation0283 | Promise.resolve assimilation and both handlers before Promise.all; malformed thenable exceptions captured. Missing array-slot semantics unspecified; no automatic hold. |
| 445 | TS generation0284 | Explicit normalized strings and new notes arrays; missing-note validation unspecified. No new hold. |
| 446 | TS generation0287 | Own-property Object.is filter preserves required identities and skips nullish entries. Broader runtime non-object handling not fully adjudicated. No new hold. |
| 447 | TS repair0189 | Missing stock row throws TypeError instead of required RangeError. stock-ledger-missing-row-error-result.json, 2050 ms. |
| 448 | TS repair0190 | Own enumerable __proto__ key not preserved. merged-preferences-proto-key-result.json, 2291 ms. |
| 449 | JS generation0361 | Missing permitted group accepted. gate-missing-permitted-group-result.json, 470 ms. |
| 450 | JS repair0241 | Missing legend entry accepted. legend-missing-entry-result.json, 431 ms. |

Six counterexamples failed without timeout in pinned network-disabled/resource-
limited sandboxes. No candidate or historical partition changed. Scoped negative
findings are not seven-criterion approvals. No training seal or new VM.
Scope v6 unchanged. GCS verified through 304 holds; batch 30 awaits backup.
Continue position 451 of 544 outside-sample array hits.
