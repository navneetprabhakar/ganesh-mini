# Array-validation follow-up, batch 32

Positions 466–480: fifteen new inspections and thirteen new holds. Total 486 unique
outside-sample inspections; 331 additive holds plus three historical = 334.
Full prompts, references and original tests inspected.

| Position | Candidate | Reproduced finding |
| --- | --- | --- |
| 466 | TS generation0298 | Required non-enumerable owner is dropped during copying, so owner lookup loses the reservation. reservation-required-owner-result.json; 2335 ms. |
| 467 | TS generation0299 | Singleton missing service bypasses text validation and becomes undefined. manifest-missing-service-result.json; 2819 ms. |
| 468 | TS generation0300 | Valid 0099-01-01 rejected because Date.UTC remaps years below 100. charges-early-year-result.json; 2564 ms. |

| 469 | TS repair0197 | Required destination lost; valid search throws. parcel-required-destination-result.json; 2542 ms. |
| 470 | TS generation0302 | Missing unit accepted. frame-missing-unit-result.json; 2805 ms. |
| 471 | TS generation0304 | Missing candidate accepted and prior selection replaced with undefined. selection-missing-candidate-result.json; 2425 ms. |
| 472 | TS generation0305 | Private dense catalog, safe page-start guard and fresh primitive records. No hold on typed string inputs; broader non-string runtime policy not adjudicated. |
| 473 | TS generation0306 | Audit callback reenters issuance: two successful calls return same ID, inner record overwritten. pass-reentrant-id-result.json; 2022 ms. |
| 474 | TS repair0202 | Fresh state/arrays, trim/deduplicate/case-sensitive behavior correct for supplied string SKUs. Missing-entry policy not specified; no hold. |
| 475 | TS repair0203 | Required quantityA lost from returned blend. blend-required-quantity-result.json; 2447 ms. Exact arithmetic formula does not require inventing overflow rejection. |
| 476 | TS repair0204 | Required action label lost in reduction. dock-required-label-result.json; 2601 ms. |
| 477 | JS generation0381 | Plain record with exactly four required fields rejected when givenName non-enumerable. access-hidden-required-field-result.json; 384 ms. |
| 478 | JS generation0382 | Extra hidden event field accepted despite explicit rejection contract. item-load-hidden-extra-result.json; 347 ms. Shallow item copy scope not broadened. |
| 479 | JS generation0383 | Missing item accepted. strip-missing-item-result.json; 338 ms. |
| 480 | JS generation0385 | Existing empty message text accepted despite explicit nonempty state-message fields. chat-empty-existing-text-result.json; 338 ms. RECEIVE empty-text policy not used as oracle. |

All thirteen probes failed at runtime (TS [0,0,1], JS [1]), without timeout in
pinned network-disabled/resource-limited sandboxes. Frozen artifacts unchanged.
GCS verified through 321 holds / batch 31; this batch awaits backup.
No training seal or new VM. Continue position 481 of 544.
Scoped no-hold findings are not seven-criterion approvals. Scope v6 unchanged.
