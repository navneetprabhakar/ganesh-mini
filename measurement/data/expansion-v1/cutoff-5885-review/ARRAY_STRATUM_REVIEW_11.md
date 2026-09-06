# Array-validation follow-up, batch 11 (in progress)

2026-09-06. Positions 151–155: five new / 164 unique outside-sample targeted
inspections, against prompt, reference and original tests. Frozen 300 unchanged.
Two new holds: 128 additive / 131 including historical three. Not training-ready.

- TS generation0103 DispatchRegistry: map/some operate on internal dense parcel
  storage, built field-by-field. No sparse-input or required-field-copy defect.
- TS generation0107 RecipeStore: normalizes input field-by-field before any
  state mutation; callbacks operate on internal dense records. No new hold.
- TS generation0108 compilePlan: missing sparse step emits step:undefined despite
  malformed-value rejection. `automation-steps-sparse-result.json`, 2022 ms.
- TS repair0069 SensorArchive: missing sparse constructor reading accepted despite
  invalid-constructor-input rejection. `sensor-readings-sparse-result.json`, 2022 ms.
  Finite-value validation is present in original tests but not explicit in prose;
  retain that separate contract-clarity question.
- TS repair0070 SettingsCatalog: field-by-field copy preserves required fields.
  Sparse-array rejection is not explicitly prescribed in its typed constructor
  contract; do not automatically turn the callback match into a quality hold.

Both probes compiled and then failed assertions `[0,0,1]` in pinned network-
disabled/resource-limited sandboxes, with no timeouts. Original tests omit holes.
Continue at position 156. These five inspections postdate the 129-hold GCS archive.
