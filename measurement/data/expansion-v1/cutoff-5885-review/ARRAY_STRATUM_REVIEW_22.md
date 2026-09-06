# Array-validation follow-up, batch 22

Positions 316–330: 15 new inspections / 338 unique outside-sample inspections.
12 distinct new holds: **241 additive / 244 including historical three**.
Full prompts, references and original tests inspected. No duplicate hold IDs.

| Position | Candidate | Scoped finding / result |
| --- | --- | --- |
| 316 | JS generation0245 | Inherited __proto__ mistaken for affinity entry; valid missing-entry case throws. device-inherited-affinity-result.json, 368 ms. |
| 317 | JS generation0246 | Missing disclosure record accepted. disclosure-missing-record-result.json, 432 ms. |
| 318 | JS repair0161 | Missing action accepted. policy-missing-action-result.json, 382 ms. |
| 319 | JS generation0242 | Exactly five required own values rejected when received is non-enumerable. shipment-required-hidden-value-result.json, 431 ms. |
| 320 | JS generation0244 | Internal dense entries, individual string validation, fresh results, standard crypto digest. No new hold from scoped inspection. |
| 321 | TS generation0206 | Internal dense queue, generated fields copied, normal state progression and fresh outputs. No new hold from scoped inspection. |
| 322 | TS generation0208 | Required notebook ID lost in refresh action. notebook-row-required-id-result.json, 2157 ms. |
| 323 | TS repair0137 | Required note ID lost in empty-query copy. find-notes-required-id-result.json, 2093 ms. |
| 324 | TS repair0138 | Required membership ID lost during refresh. membership-required-id-result.json, 2093 ms. |
| 325 | TS repair0139 | Required units lost before sort, changing output order. pending-transfer-required-units-result.json, 2176 ms. |
| 326 | TS repair0140 | Required retired flag lost, misclassifying document. shelf-required-retired-flag-result.json, 2228 ms. |
| 327 | JS generation0247 | Non-plain class-instance day accepted. day-nonplain-shape-result.json, 333 ms. |
| 328 | JS generation0248 | Internal dense packing list; individually validated inputs, fresh snapshots, separate state. No new hold from scoped inspection. |
| 329 | TS generation0211 | Required empty ID lost on select. widget-required-id-preservation-result.json, 2094 ms. |
| 330 | TS generation0212 | Missing publication accepted. publication-missing-record-result.json, 2425 ms. |

Every diagnostic failed at runtime without timeout in the pinned network-disabled,
resource-limited sandbox; TypeScript compilation passed. Property probes retain
valid required interface fields, merely changing enumerability. These are not
demands to deep-copy arbitrary extra metadata. Numeric sum overflow alone is not
a hold for shipment accounting because only input safe-integer bounds are given.
The packing-list original test explicitly assigns fractional-ID TypeError;
no opposite error-class oracle was imposed. Negative findings are not approvals.

Scope v6 unchanged: 11 groups / 14 strata / 3,085 records requiring review,
not rejections. No training seal or frozen-input changes. All 97 data-tooling
tests pass. GCS verified through 232 holds; batch 22 awaits backup. Continue 331.
