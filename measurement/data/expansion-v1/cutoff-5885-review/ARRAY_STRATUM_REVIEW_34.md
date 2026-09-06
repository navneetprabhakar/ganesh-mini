# Array-validation follow-up, batch 34

Positions 496–510: 15 new inspections / 11 new holds. Total 516 unique outside-
sample inspections, 354 additive holds plus three historical = 357. Full prompts,
references and original tests inspected.

| Position | TS candidate | Scoped finding |
| --- | --- | --- |
| 496 | repair0216 | Private dense members, explicit normalized fields; validated operations precede mutation. No new hold. Unreachable-scale ID exhaustion not executed. |
| 501 | repair0220 | For-of validates assignments before atomic map replacement; explicit internal parcel fields. No new hold. |
| 508 | generation0343 | Sequential await/catch and fresh outputs; missing guard becomes caught TypeError. Throwing String conversions lack specified fallback, left unadjudicated. No new hold. |
| 509 | generation0344 | Private dense queue and primitive inputs, validated before mutation and fresh output copies. No new hold. |
| 497 | generation-0326 | Per-line whitespace not trimmed before sentence extraction. digest-per-line-trim-result.json; 2550 ms. |
| 498 | generation-0327 | Missing memo bypasses required-field validation. memo-queue-missing-record-result.json; 2539 ms. |
| 499 | generation-0328 | Required item ID lost from query result. selected-inventory-required-id-result.json; 2486 ms. |
| 500 | generation-0329 | Required initiative name lost from snapshot. initiative-required-name-result.json; 2369 ms. |
| 502 | generation-0337 | Safe integer move offset loses selected origin through intermediate rounding. entry-book-large-offset-result.json; 2379 ms. |
| 503 | generation-0338 | Finite extreme endpoints produce NaN at zero blend fraction. numeric-blend-finite-endpoint-result.json; 2394 ms. |
| 504 | generation-0339 | Missing allowed suffix bypasses dot-prefix validation. cleanup-missing-suffix-result.json; 2148 ms. |
| 505 | generation-0341 | Missing color bypasses finite-channel validation. voxel-missing-color-result.json; 2314 ms. |
| 506 | repair-0227 | UTF-16 sort violates stated code-point order on supplementary characters. member-roles-codepoint-order-result.json; 2743 ms. |
| 507 | repair-0228 | Missing volume bypasses malformed-volume validation. volumes-missing-record-result.json; 2481 ms. |
| 510 | generation-0347 | Required guest lost from removed reservation copy. withdrawal-required-guest-result.json; 2070 ms. |

All eleven probes compiled and failed at runtime [0,0,1], without timeout, in
pinned network-disabled/resource-limited sandboxes. Numeric inputs are bounded;
no large allocation or long loops. Additional wrap/prototype-key issues in
0338 are static observations only; 0339 slash-root wording remains unadjudicated.
No-hold findings are not seven-criterion approvals. Scope v6 and frozen artifacts
unchanged. GCS verified through 346 holds; this batch awaits backup.
No training seal or new VM. Continue position 511 of 544.
