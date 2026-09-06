# Array-validation follow-up, batch 19

Completed positions 271–285: 15 new / 294 unique outside-sample inspections.
Eight holds in batch: **214 additive / 217 including historical three**.
Later confirmed defects: TS generation0182 malformed lookup throws (explicit
runtime contract says undefined); generation0186 missing supported language;
repair0121 missing field ID; generation0183 missing choice value; JS generation
0211 snapshot drops a valid __proto__ SKU. Evidence prefixes: icon-malformed-lookup,
preference-missing-language, field-collection-missing-id, choice-model-missing-value,
inventory-proto-sku-snapshot (each suffixed -result.json).
All five runtime checks failed without timeout; TypeScript compilation passed.

Scoped negatives: TS generation0184 uses per-registration entries and snapshots
active listeners; inactive-entry retention is a scalability concern, not a tested
contract defect. TS repair0122 copies internally created toast and confirmation
objects. JS repair0143 and JS repair0142 validate with for-of and use internal dense records.
TS generation0188 materializes missing sequence entries with Array.from before
finite validation, so it does not share the skipped-hole defect. No approvals.
Continue position 286. Earlier partial checkpoint follows.

Partial: positions 271–275 inspected; five new / 284 unique outside-sample
inspections. Three new holds: **209 additive / 212 including historical three**.

- TS repair0119 skips a missing reading: station-missing-reading-result.json.
- JS repair0138 rejects two finite MAX_VALUE weights before trimming. Prose
  allows finite individual weights; original test explicitly imposes the extra
  aggregate-finiteness restriction. budget-finite-weights-result.json, 449 ms.
  This is a contract/test mismatch; the bounded diagnostic expects the right
  endpoint removed, leaving a representable total. Mathematical original-total
  tolerance does not bridge the huge excess.
- JS generation0205 loses a non-enumerable own data-count attribute despite the
  explicit own-key copy contract: toggle-own-hidden-attribute-result.json, 483 ms.

All diagnostics failed at runtime without timeout in pinned network-disabled,
resource-limited sandboxes; TypeScript compilation succeeded.
JS generation0209 copies validated profiles explicitly and maps internal dense
records. Its never-throws wording under throwing accessors remains unprobed.
JS generation0208 uses arrays produced by reducer operations and intentional
structural sharing for unchanged tickets; no new hold from this inspection.
No seven-criterion approvals. Continue position 276.
GCS verified through 209 holds / batch 18 / scope v5, not this partial batch.
