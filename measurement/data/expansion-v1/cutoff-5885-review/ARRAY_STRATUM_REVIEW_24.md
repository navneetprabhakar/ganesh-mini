# Array-validation follow-up, batch 24

Positions 346–360: 15 new / 368 unique outside-sample inspections. Eleven new
holds: **261 additive / 264 including historical three**. Full prompts,
references and original tests inspected; hold IDs deduplicated.

| Position | Candidate | Finding |
| --- | --- | --- |
| 346 | JS repair0175 | Missing radial device accepted. radial-missing-device-result.json, 369 ms. |
| 347 | JS generation0260 | Missing trip coordinate point accepted. trip-missing-point-result.json, 404 ms. |
| 348 | JS generation0261 | Reflect.ownKeys exact-field checks, explicit primitive copies, bounded arithmetic, real subclass inheritance. No new hold from scoped inspection. |
| 349 | JS generation0262 | Exact own-field checks and copied primitive state; callback error prevents removal commit; normal later calls guarded. No new hold from scoped inspection. |
| 350 | JS generation0263 | Missing album accepted. album-missing-record-result.json, 373 ms. |
| 351 | JS repair0177 | Required non-enumerable broadcastEnabled lost while only previewEnabled should change. operator-broadcast-preservation-result.json, 378 ms. |
| 352 | JS repair0179 | Missing token accepted. render-tokens-missing-token-result.json, 407 ms. |
| 353 | JS generation0266 | for-of catches missing entries; original tests explicitly include a sparse array. Escaping and fixed grid output reviewed. No new hold. |
| 354 | TS generation0224 | Public WorkItem fields lack promised readonly modifiers. work-item-readonly-api-result.json, 1948 ms, compile result [0,2]. |
| 355 | TS repair0152 | Missing nonblank image accepted into gallery. detail-dialog-missing-image-result.json, 2558 ms. |
| 356 | JS generation0274 | Singleton missing book survives validation before remove. update-shelf-missing-book-result.json, 354 ms. |
| 357 | JS generation0275 | Own enumerable __proto__ flag lost. normalized-flags-proto-key-result.json, 339 ms. |
| 358 | TS generation0230 | Missing keyed item accepted. membership-weights-missing-item-result.json, 2263 ms. |
| 359 | TS repair0154 | 150,000 valid samples hit function-argument limit at Math.min(...amounts). sample-summary-bounded-large-input-result.json, 3087 ms. |
| 360 | JS generation0277 | Internal dense normalized records, explicit required fields, exact code identity, fresh outputs. Plain-object null-prototype ambiguity is not automatically a hold. |

Ten diagnostics failed at runtime without timeout in pinned network-disabled,
resource-limited sandboxes. The readonly diagnostic instead failed type checking:
all three @ts-expect-error directives were unused (TS2578), proving assignments
are allowed by the exported interface. A correctly readonly interface would
consume those directives. Original tests directly assign title without a cast;
this is a prompt/API/test inconsistency, not a fabricated runtime failure.

The large-input diagnostic is bounded (150,000 finite unit amounts, distinct
safe positions) and the error is argument spreading, not timeout or memory kill.
No public input-size restriction was specified. Negative findings remain scoped,
not approvals. Scope v6 unchanged; no training seal or frozen input changes.
GCS verified through 253 holds / batch 23; batch 24 awaits backup. Continue 361.
