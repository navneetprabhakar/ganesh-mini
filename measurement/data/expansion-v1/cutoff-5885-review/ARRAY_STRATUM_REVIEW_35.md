# Array-validation follow-up, batch 35 — partial

Positions 511–516: six new inspections / five new holds. Total 522 unique outside-
sample inspections; 359 additive holds plus historical three = 362. Full prompts,
references and original tests inspected.

| Position | TS candidate | Scoped finding |
| --- | --- | --- |
| 512 | generation0354 | Private scalar state and normalized string labels; fresh snapshots. Missing-label policy not explicit, no new hold. |
| 511 | generation-0351 | Required shipment code lost in bulk stage change. shipment-required-code-result.json; 2359 ms. |
| 513 | repair-0236 | Required invoice owner lost in returned copy. invoice-required-owner-result.json; 2314 ms. |
| 514 | generation-0352 | Safe integer rotation loses prior offset through intermediate rounding. turn-order-large-step-result.json; 2584 ms. |
| 515 | generation-0356 | Finite 1e21 cost formatted in exponent notation instead of exactly two decimals. asset-large-fixed-decimal-result.json; 2796 ms. |
| 516 | generation-0357 | Missing visible paragraph throws TypeError instead of specified RangeError. case-missing-paragraph-error-result.json; 2432 ms. |

All five probes compiled and failed at runtime [0,0,1] without timeout in pinned
network-disabled/resource-limited sandboxes. 0236 original tests additionally
impose safe-integer pagination not stated in prose; that oracle discrepancy is
not separately adjudicated. No-hold findings are not approvals. Frozen artifacts
and scope v6 unchanged. GCS verified through 357 holds; this partial batch awaits
backup. No training seal or VM. Continue position 517 of 544.
