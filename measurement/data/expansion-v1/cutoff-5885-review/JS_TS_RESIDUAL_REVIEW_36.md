# JavaScript/TypeScript residual review, batch 36

Positions 526–540 of 587. Full prompts, reference/corrected source and original
tests read; supplied known-bad source compared via complete reference diffs.
Three new holds: 1065 additive plus historical three = **1068**;
**2,883** unique outside-sample inspections. Not admission, final rejection or
seven-criterion approval. 2026-09-07 IST.

| Position | ID suffix | Scoped finding |
| --- | --- | --- |
| 526 | typescript-generation-0309 | Correct false/empty distinction, typed-kind validation, canonical keys and copied snapshots. No method returns mutable storage; no private-field bypass. No new hold. |
| 527 | typescript-generation-0310 | No-op identity preserved before overflow guard; exact actions and safe increments agree. Readonly initial constant not required runtime frozen. No new hold. |
| 528 | typescript-generation-0312 | Explicit initial primitive copies, own-only relevant patch values, prevalidation and detached returns agree. Unknown fields versus all supplied wording needs clarity; no new hold. |
| 529 | typescript-repair-0206 | Hold: public return type changed and unsound assertion added. Runtime lookup comparison repaired, category copy correct. Test compares structurally non-overlapping input and output directly, suggesting harness pressure; causal inference only. |
| 530 | typescript-generation-0314 | Trimmed exact request, own catalog lookup, typed entries and specific status errors agree. No new hold. |
| 531 | typescript-generation-0317 | Captured per-stage functions, repeated execution and wrapped ordinary causes agree. Throws during String conversion of unusual thrown objects and action receiver domain unspecified; no invented conversion fallback. No new hold. |
| 532 | typescript-repair-0210 | Medium/large order repaired; exact styles, finite-integer guards and independent rows agree. Low-complexity table repair criterion pending; no new hold. |
| 533 | typescript-repair-0211 | Hold: old unsubscribe is not inert after first use if same callback later resubscribed. Required-answer OR repaired. Listener exception, mutation and duplicate-registration policy need clarity. |
| 534 | typescript-repair-0212 | Explicit blank label guard repaired; omitted function-name fallback and raw content contract agree. No invented HTML escaping requirement; no new hold. |
| 535 | typescript-generation-0322 | Preserved strings, JavaScript whitespace token count and exact prefixes agree. Four lines means four sections with embedded newlines explicitly allowed. No new hold. |
| 536 | typescript-generation-0320 | Hold: global Array.push void overload breaks unrelated consumer typing. Runtime snapshot logic otherwise agrees; ordinary token lifetime bound pending. |
| 537 | typescript-generation-0321 | Explicit loaded/saved primitive copies, initialization guard, validated merged settings and notification ordering agree. Unknown/present undefined/inherited patch policy needs clarity; no new hold. |
| 538 | typescript-repair-0214 | Reset fully clears value; complete rejects boundary whitespace as explicitly required by final prompt sentence. Problem retained verbatim intentionally, not a copy defect. No new hold. |
| 539 | typescript-generation-0325 | Trimmed values, first position with last replacement and detached entries agree. Unicode case-insensitivity versus en-US lowercase semantics needs clarity; no new hold. |
| 540 | typescript-repair-0217 | Clear delegates to set, subscriber snapshot and active-guard unsubscribe agree. Duplicate subscription/reentrant value semantics unspecified; no new hold. |

Static hold detail for position529: requested return annotation is
PreparedSurveyEntry. Reference changes it to PreparedSurveyEntry & SurveyInput,
constructs only prompt/details/state/category, then asserts the intersection.
The added required categoryId is absent. This is an API/idiomatic quality
finding from frozen source, not an executed metric.

Pinned isolated network-disabled, resource-limited survey_0211_unsubscribe
probe failed at runtime [0,0,1], 2222 ms, calls 0 instead of 1. The
channel_0320_global_push probe failed compilation [0,2], 1788 ms, TS2322:
void not assignable to number. Its runtime assertions did not execute.
Neither timed out. Sources and full JSON receipts retained.
Original tests read, not rerun by probes. Candidate/sample/partition unchanged;
candidate SHA
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
97 data tooling tests passed during batch35. GCS verified through residual510;
batches35–36 await backup. Continue541; criteria/dispositions pending.

