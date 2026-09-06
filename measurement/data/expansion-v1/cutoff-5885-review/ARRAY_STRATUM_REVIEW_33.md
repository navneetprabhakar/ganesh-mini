# Array-validation follow-up, batch 33

Positions 481–495: 15 new inspections, 12 new holds; 501 unique outside-sample
inspections. 343 additive holds plus three historical = 346. Full prompts,
references and original tests inspected. No frozen artifacts changed.

| Position | Candidate | Scoped finding |
| --- | --- | --- |
| 481 | JS generation0386 | Dense private records and explicit scalar copies; value/patch shallow-copy contract honored. No new hold. Throwing accessors/reentrant accessors not adjudicated. |
| 484 | JS generation0395 | For-of validates every label before filter; locale casing and empty-query semantics match. No new hold. |
| 487 | TS repair0205 | Explicit entry/config copies and options snapshots; later for-of rejects missing entries. Selected return-type overload is compatible refinement. No new hold. |
| 482 | javascript-generation-0388 | Missing catalog entry accepted. catalog-missing-entry-result.json; 424 ms. |
| 483 | javascript-generation-0389 | Missing site-map entry accepted. sitemap-missing-entry-result.json; 350 ms. |
| 485 | typescript-generation-0311 | Missing review record bypasses field validation. review-page-missing-record-result.json; 2398 ms. |
| 486 | typescript-repair-0207 | Required SKU lost in quantity update. reservation-line-required-sku-result.json; 2355 ms. |
| 488 | typescript-generation-0315 | Missing tag stored as non-string. submission-missing-tag-result.json; 2246 ms. |
| 489 | typescript-generation-0316 | Missing replacement item bypasses ID validation. replica-missing-item-result.json; 2332 ms. |
| 490 | typescript-generation-0318 | Missing permit zone bypasses normalization. route-missing-permit-zone-result.json; 2600 ms. |
| 491 | typescript-repair-0209 | Missing coefficient accepted despite finite numeric requirement. polynomial-missing-coefficient-result.json; 2803 ms. |
| 492 | typescript-generation-0323 | Missing candidate accepted by constructor. candidate-list-missing-record-result.json; 2510 ms. |
| 493 | typescript-generation-0324 | Missing work entry accepted by constructor. work-ledger-missing-entry-result.json; 2648 ms. |
| 494 | typescript-repair-0213 | Required seed name lost, preventing valid save. chapter-required-name-result.json; 2945 ms. |
| 495 | typescript-repair-0215 | Required column name lost during catalog copy. audit-column-required-name-result.json; 2560 ms. |

All 12 probes failed at runtime (TS [0,0,1], JS [1]) without timeout in pinned
network-disabled/resource-limited sandboxes. No-hold findings are scoped, not
seven-criterion approvals. Scope v6 unchanged. GCS verified through 334 holds;
this batch awaits backup. No training seal or new VM. Continue position 496.
