# Array-validation follow-up, batch 25

Positions 361–375: 15 new / 383 unique outside-sample inspections. Twelve new
holds: **273 additive / 276 including historical three**. Full prompts,
references and original tests inspected; no duplicate hold IDs added.

| Position | Candidate | Finding |
| --- | --- | --- |
| 361 | JS generation0279 | Own __proto__ state key lost. control-board-proto-state-result.json, 381 ms. |
| 362 | JS generation0281 | Missing loaded journal entry accepted. journal-load-missing-entry-result.json, 360 ms. |
| 363 | JS repair0186 | Missing blocked tag accepted. log-policy-missing-tag-result.json, 380 ms. |
| 364 | JS repair0188 | Own non-enumerable false email override ignored. merge-alerts-hidden-override-result.json, 431 ms. |
| 365 | JS generation0286 | Dense two-name list, copies strings, code-point first-character uppercase, fresh JSON snapshots. No new hold. |
| 366 | JS generation0288 | Explicitly discards non-string values; missing slots need not be retained. Dense retained sequence and fresh state snapshots; no new hold. |
| 367 | TS generation0237 | Required quantity lost in line copy and arithmetic consumes undefined. reservation-required-quantity-result.json, 2055 ms. |
| 368 | TS generation0238 | Non-string roster ID accepted. roster-nonstring-id-result.json, 2183 ms. |
| 369 | TS generation0240 | Missing nonempty bullet accepted. organization-missing-bullet-result.json, 2559 ms. |
| 370 | TS repair0158 | Missing toString translation returns inherited function, not key. panel-inherited-translation-result.json, 2535 ms. |
| 371 | TS repair0159 | Dense required-value checks, global escaping and first-match selected flag; no malformed-option policy added. No new hold. |
| 372 | TS repair0160 | Valid required non-enumerable command field name lost. command-field-required-name-result.json, 2049 ms. |
| 373 | JS generation0289 | Missing author accepted. book-summary-missing-author-result.json, 463 ms. |
| 374 | JS generation0293 | Missing request group accepted despite required strings. access-missing-request-group-result.json, 419 ms. |
| 375 | JS repair0193 | Class-instance point accepted despite plain-object requirement. route-nonplain-point-result.json, 598 ms. |

All twelve diagnostics failed at runtime, not by timeout, in pinned network-
disabled/resource-limited sandboxes. All TypeScript compilation passed. Null-
prototype plain-object interpretation was not treated as a defect in isolation;
the log-policy original test explicitly permits it. Negative observations are
not approvals. Frozen corpus/sample/partition unchanged; no training seal.

All 97 data-tooling tests pass. Scope v6 unchanged. GCS verified through 264
holds / batch 24; batch 25 awaits backup. Continue position 376.
