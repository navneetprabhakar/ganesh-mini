# Array-validation follow-up, batch 16

Completed positions 226–240: 15 new / 249 unique outside-sample inspections.
Eleven new holds in this batch: **186 additive / 189 including historical three**.
The later five diagnostics all reproduced runtime assertion failures without
timeout: JS generation0183 accepts a duplicate trimmed topic label when an
existing label is padded; generation0184 skips missing passes; generation0185
skips missing playlist entries; generation0186 skips missing notes; repair0122
accepts a missing generated job. Result files respectively: topic-trimmed-duplicate,
member-passes-missing, playlist-missing-entry, note-collection-missing, and
flush-generated-missing (each suffixed -result.json).
Continue position 241. Earlier partial checkpoint follows.

Partial: positions 226–235 inspected, ten new / 244 unique outside-sample
inspections. Six confirmed new holds: 181 additive / 184 including historical
three. Original frozen sample and historical partition unchanged.

| ID suffix | Finding | Diagnostic result |
| --- | --- | --- |
| javascript-generation-0176 | Missing initial meter accepted | meter-bank-sparse-result.json |
| typescript-repair-0107 | Required layer ID lost in spread copy | compiled-layer-hidden-id-result.json |
| typescript-repair-0108 | Missing rule throws wrong exception class | recurrence-sparse-error-type-result.json |
| typescript-generation-0158 | Required note ID lost in spread copy | notebook-note-hidden-id-result.json |
| typescript-generation-0159 | Missing byte accepted | packing-missing-byte-result.json |
| typescript-generation-0160 | Required metric ID lost in spread copy | dashboard-metric-hidden-id-result.json |

All six runtime assertions failed in pinned network-disabled/resource-limited
sandboxes, without timeout. All TypeScript compilations succeeded. Required
property probes use valid typed objects whose own ID is non-enumerable; they do
not require preserving arbitrary metadata or property descriptors.

Scoped negative findings: JavaScript repair0119 uses dense date components and
own Gregorian validation; TypeScript repair0106 maps internal dense entries;
TypeScript generation0157 validates shortcuts using for-of; JavaScript
generation0182 validates cards using for-of and copies explicit fields.
These observations are not seven-criterion approvals. Dashboard existing-state
duplicate handling remains an unprobed contract question.

Continue position 236. GCS covers 178 holds / batch 15, not this partial batch.
No training seal, revised partition, generation restart, or new VM.
