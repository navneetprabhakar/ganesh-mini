# Array-validation follow-up, batch 21

Partial: positions 301–305 inspected; five new / 313 unique outside-sample
inspections. Three new holds: **223 additive / 226 including historical three**.

- TS repair0131 loses a valid required non-enumerable ID during copying, so get
  cannot find the record: operator-required-id-copy-result.json.
- JS generation0231 accepts a missing provider item: bin-snapshot-missing-item-result.json.
- JS generation0232 loses a valid required non-enumerable job ID on enqueue:
  queue-required-job-id-copy-result.json.

All three runtime checks failed without timeout in pinned network-disabled,
resource-limited sandboxes; TypeScript compilation succeeded. No duplicate hold
IDs were present before these probes. TS generation0198 builds dense class tokens
and explicitly merges style records; JS generation0229 stores only individually
validated points. No new holds for those scoped observations, not approvals.
Continue position 306. GCS verified through 223 holds / completed batch 20 / v6;
these five inspections postdate that backup.
