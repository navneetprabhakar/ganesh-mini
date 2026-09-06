# Array-validation follow-up, batch 19

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
