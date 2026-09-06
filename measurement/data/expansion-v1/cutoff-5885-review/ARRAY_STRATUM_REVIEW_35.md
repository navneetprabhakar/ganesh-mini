# Array-validation follow-up, batch 35

Positions 511–525: fifteen new inspections / thirteen new holds. Total 531 unique outside-
sample inspections; 367 additive holds plus historical three = 370. Full prompts,
references and original tests inspected.

| Position | TS candidate | Scoped finding |
| --- | --- | --- |
| 512 | generation0354 | Private scalar state and normalized string labels; fresh snapshots. Missing-label policy not explicit, no new hold. |
| 511 | generation-0351 | Required shipment code lost in bulk stage change. shipment-required-code-result.json; 2359 ms. |
| 513 | repair-0236 | Required invoice owner lost in returned copy. invoice-required-owner-result.json; 2314 ms. |
| 514 | generation-0352 | Safe integer rotation loses prior offset through intermediate rounding. turn-order-large-step-result.json; 2584 ms. |
| 515 | generation-0356 | Finite 1e21 cost formatted in exponent notation instead of exactly two decimals. asset-large-fixed-decimal-result.json; 2796 ms. |
| 516 | generation-0357 | Missing visible paragraph throws TypeError instead of specified RangeError. case-missing-paragraph-error-result.json; 2432 ms. |

| 517 | generation-0359 | Missing route accepted by constructor. route-registry-missing-entry-result.json; 2310 ms. |
| 518 | generation-0360 | Missing measurement bypasses validation. measurements-missing-record-result.json; 2637 ms. |
| 519 | repair-0237 | Required note text lost during replacement. workspace-note-required-text-result.json; 2499 ms. |
| 520 | generation-0358 | Singleton array shorthand accepted despite two/four-member array contract. gaps-singleton-shorthand-result.json; 2127 ms. |
| 521 | generation-0362 | Null orientation silently defaulted instead of rejected. field-null-orientation-result.json; 2716 ms. |
| 522 | generation-0363 | Required member tier lost from query result. member-query-required-tier-result.json; 2402 ms. |
| 523 | repair-0242 | Numeric falsey index flag accepted despite malformed-input contract. view-tree-nonboolean-index-result.json; 2289 ms. |
| 524 | generation-0365 | Missing keyword bypasses string validation. directory-index-missing-keyword-result.json; 2411 ms. |
| 525 | repair0241 | Explicit primitive field copies into private dense storage; validated titles and fresh list/find copies. No new hold. |

All thirteen probes compiled and failed at runtime [0,0,1] without timeout in pinned
network-disabled/resource-limited sandboxes. 0236 original tests additionally
impose safe-integer pagination not stated in prose; that oracle discrepancy is
not separately adjudicated. No-hold findings are not approvals. Frozen artifacts
and scope v6 unchanged. GCS verified through 357 holds; this batch awaits
backup. No training seal or VM. Continue position 526 of 544.
0365 additionally narrows the declared readonly keyword-array API; compile-time
compatibility is noted but not separately executed or counted.
