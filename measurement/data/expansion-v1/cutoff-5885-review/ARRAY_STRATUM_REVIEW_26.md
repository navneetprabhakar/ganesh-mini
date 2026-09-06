# Array-validation follow-up, batch 26

Positions 376–390: 15 new / 398 unique outside-sample inspections. Three new
holds: **276 additive / 279 including historical three**. Full prompts,
references and original tests inspected; no duplicate holds added.

| Position | Candidate | Scoped finding |
| --- | --- | --- |
| 376 | JS repair0196 | Indexed own-element validation explicitly rejects holes before strict comparison. No new hold. |
| 377 | TS generation0243 | Dense required counts, safe-integer checks, explicit optional strings and escaping. No new hold; undefined follows optional absence semantics. |
| 378 | TS repair0161 | Object.is filtering preserves required identities; no malformed-record policy. No new hold. |
| 379 | TS repair0163 | Fixed jump/crouch/announce ordering, for-of plugin checks, primitive events. Repeated-action multiplicity is underspecified, not promoted to a hold. |
| 380 | TS repair0164 | Filters empty trimmed names before cycling; valid-name requirement applies even at count zero. No new hold. |
| 381 | TS generation0242 | Identity-index serialization and bounds-checked reconstruction reviewed. Original test's a.members.push(a) is suspicious: Avatar adds an unnecessary members field to support it. Requires oracle adjudication; no new reproduced contract violation claimed here. |
| 382 | TS generation0246 | Dense numeric checks; endpoint clipping and Set prevent duplicate pages. No new hold; no infeasible huge-output probe executed. |
| 383 | JS generation0295 | JSON-compatible own __proto__ key lost during deep clone. revision-update-proto-data-result.json, 340 ms. |
| 384 | JS generation0298 | Matching note loses required title when non-enumerable. search-note-required-title-result.json, 366 ms. Explicit shallow extra-metadata identity remains allowed. |
| 385 | JS generation0299 | Singleton missing option accepted. choice-model-missing-option-result.json, 350 ms. |
| 386 | JS generation0300 | Descriptor-aware JSON cloning preserves own prototype-named keys and rejects missing array slots; cycle tracking is ancestry-scoped. No new hold. |
| 387 | TS generation0252 | Explicit normalized fields, per-kind Maps, cascade removal, fresh outputs. Lexicographic/locale-order wording left for oracle review, not automatically rejected. |
| 388 | TS repair0165 | Trims and compares exact paths, explicitly reconstructs output fields. Missing-record behavior not specified. No new hold. |
| 389 | TS repair0167 | Trims before Set; missing destination becomes undefined then throws; fresh per-task asset fields. No new hold. |
| 390 | TS generation0249 | Explicit bookmark/member field copies, rank checks and code-unit tie breaker. No new hold from scoped inspection. |

Three probes failed without timeout in pinned network-disabled/resource-limited
sandboxes. Negative findings are not seven-criterion approvals. In particular,
the Arena test issue remains open despite no new additive runtime hold here.
Frozen data/sample/partition unchanged; no training seal. Scope v6 unchanged.
GCS verified through 276 holds / batch 25; batch 26 awaits backup. Continue 391.
