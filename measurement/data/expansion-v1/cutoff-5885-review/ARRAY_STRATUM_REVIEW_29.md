# Array-validation follow-up, batch 29

Positions 421–435: 15 new / 443 unique outside-sample inspections. Nine new
holds: **301 additive / 304 including historical three**. Full prompts,
references and original tests inspected, including rereading initially
truncated ArticleUpdate content. No duplicate holds added.

| Position | Candidate | Scoped finding |
| --- | --- | --- |
| 421 | JS repair0225 | for-of validates individual Unicode markers; Array.from text preserves code points and original case. No new hold. |
| 422 | JS repair0226 | Complete for-of validation before Map reconciliation, Object.is and required identity reuse. Revision arithmetic explicitly uses oldRevision+1; no invented safe-integer policy. No new hold. |
| 423 | TS generation0276 | Explicit fields and copied tag arrays. Constructor trim versus snapshot wording needs oracle clarification; missing-tag policy not specified. No new hold. |
| 424 | TS repair0184 | Required initial text lost in snapshot. audit-trail-required-text-result.json, 2442 ms. Disposal guard precedes unsubscribe; ordering convention left for oracle review. |
| 425 | TS generation0274 | Required article ID lost on delta-zero text update. article-update-required-id-result.json, 1957 ms. Prompt says four string fields but reference/test use six: separate oracle issue. Unchanged-object sharing not automatically forbidden by immutable-update contract. |
| 426 | TS generation0275 | Required commandId lost on registration. action-shelf-required-command-result.json, 2293 ms. Opaque extra-metadata aliasing not used as this hold's evidence. |
| 427 | JS generation0344 | Explicit Infinity limit accepted. parcel-explicit-infinite-limit-result.json, 349 ms. Default internal Infinity sentinel does not authorize supplied non-integer limit. |
| 428 | JS repair0232 | Missing obstacle accepted. cursor-missing-obstacle-result.json, 478 ms. |
| 429 | TS generation0277 | Required destination lost in returned copy. dispatch-required-destination-result.json, 2006 ms. Complete for-of validation catches sparse records. |
| 430 | TS generation0280 | Missing color accepted. draft-shelf-missing-color-result.json, 2731 ms. |
| 431 | TS generation0282 | Code-point counts, fixed dense numeric-enum membership, text preservation and private dense records. No new hold. |
| 432 | TS repair0186 | Missing carrier accepted without required failure path. delivery-missing-carrier-result.json, 2620 ms. |
| 433 | TS repair0187 | String enum values avoid numeric reverse-mapping issue; internal dense records explicitly constructed and copies returned. No new hold. |
| 434 | TS repair0188 | Primitive inputs normalized into internal dense records; fresh results and exact settings. No new hold. |
| 435 | TS generation0279 | Missing label accepted. equipment-missing-label-result.json, 2063 ms. ID increment before normalization is an additional static observation; failed-ID-consumption rule not explicitly imposed here. |

All nine counterexamples failed without timeout in pinned network-disabled/
resource-limited sandboxes; TypeScript compilation succeeded. Scoped negative
findings are not seven-criterion approvals. Frozen data/sample/partition unchanged.
No training seal or new VM. Scope v6 unchanged. GCS verified through 295 holds;
this batch awaits backup. Continue position 436 of 544 outside-sample array hits.
