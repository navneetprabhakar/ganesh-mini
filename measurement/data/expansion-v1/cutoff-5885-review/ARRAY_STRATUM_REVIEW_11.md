# Array-validation follow-up, batch 11

Completed positions 151–165: 15 new / 174 unique outside-sample inspections.
Ten new holds in this batch, **136 additive / 139 including historical three**.
The earlier five-record checkpoint below is retained as history.

| ID suffix | Finding | Result |
| --- | --- | --- |
| javascript-generation-0127 | Missing sparse player name is accepted. | token-names-sparse-result.json |
| javascript-generation-0128 | Missing detection is accepted and counted. | detections-sparse-result.json |
| javascript-generation-0129 | Safe-integer sum loses a unit during intermediate cancellation. | ledger-safe-cancellation-result.json |
| javascript-repair-0085 | Missing task bypasses required synchronous function validation. | concurrent-tasks-sparse-result.json |
| javascript-repair-0087 | Missing finite value bypasses whole-array validation. | stride-sparse-result.json |
| javascript-repair-0088 | Exact arithmetic tie-break conflicts with ordinary numeric addition and shortest-segment specification; original test encodes the conflicting outcome. | segment-numeric-tie-result.json |
| typescript-generation-0109 | Required ledger ID lost during valid entry copying. | ledger-report-hidden-id-result.json |
| typescript-generation-0111 | Required reading ID lost during valid item copying. | reading-page-hidden-id-result.json |

All eight later probes reproduced assertion failures without timeout. JS exits
`[1]`; TS compiles then exits `[0,0,1]`. JS repair0088 is a prompt/original-test/
reference inconsistency: original test expects the longer segment even though
the prescribed ordinary numeric sums tie. No hidden-test assumption is needed.
JS generation0129 uses only three safe integers, with exactly representable
final sum 2; it returns 1. This is not an infeasibly large input test.

TS repair0072 copies rows/header and validates every row length with for-of;
no sparse outer-array validation bypass. Cell-level runtime type policy is not
specified beyond the type alias. JS repair0086's every skips holes initially,
but for-of subsequently reads undefined.length and throws the required TypeError;
therefore the heuristic alone does not warrant a hold. JS repair0087 explicitly
requires ordinary addition order, so no exact-sum arithmetic rule is imposed.
TS generation0109 identifier collation and numeric-balance semantics remain
separate open review questions; neither is claimed as an executed defect here.

Next position 166. No training seal or revised partition. Latest evidence awaits
GCS backup; 129-hold archive is the last verified checkpoint.

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
