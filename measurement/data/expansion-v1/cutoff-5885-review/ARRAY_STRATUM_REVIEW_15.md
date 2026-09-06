# Array-validation follow-up, batch 15 (in progress)

2026-09-06. Positions 211–215 inspected against prompt, reference and original
tests: five new / 224 unique outside-sample inspections. Three new holds bring
the ledger to **168 additive / 171 including historical three**. Frozen 300
unchanged. This is not seven-criterion approval.

- JS generation0163 createQueue maps internally built dense entries; explicit
  primitive fields are copied. No new array-validation or copying defect found.
- TS generation0146 configuration helpers use null-prototype result maps and
  own-key checks. Filename localeCompare versus generic sorting wording and
  numeric-key enumeration remain open contract questions, not executed holds.
- TS generation0148 validateAccount inserts duplicate-email issue before a later
  accessLevel format issue; contract says append duplicate after format/required
  issues. `account-duplicate-issue-order-result.json`, 2170 ms, `[0,0,1]`.
- TS generation0149 PreferenceForm accepts a missing provider as undefined;
  `preference-providers-sparse-result.json`, 2123 ms, `[0,0,1]`. Notifier/navigation
  throwing behavior remains a separate callback-policy question.
- JS generation0174 timeline rejects valid date 0099-01-01 because Date.UTC maps
  years 0–99 into 1900–1999; `timeline-early-year-result.json`, 396 ms, `[1]`.

All probes ran in pinned network-disabled/resource-limited sandboxes, no timeout;
TS compilation succeeded. Original tests omit these cases. Continue position 216.
GCS verified through 168 holds / batch 14; these five inspections postdate it.
No training seal, revised partition, generation restart or new VM.
