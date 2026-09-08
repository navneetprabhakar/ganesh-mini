# Final systematic scope delta — 2026-09-08

## Result and boundary

Gate 2, read-only scope accounting. The six specified findings justify **three criterion-to-stratum membership additions**, not new unique inspection scope and not a blanket review restart. Proposed C membership grows 451 → 808; proposed J membership grows 116 → 389. No central files, holds, corpus, cloud resources, or candidate execution were changed. This note makes no new adverse candidate adjudications.

C = required_property_copy_loss. J = javascript_reference_test_accommodation. Strata are matched exactly on lane, source, task_type and rejection_history; population and heuristic tags are not join keys. The rule in docs/data/EXPANSION_V1.md is that a systematic defect reopens its affected stratum. A stratum's having been inspected for a different criterion does not remove this obligation.

## Findings mapped to exact strata

All six IDs below already have final scoped hold evidence. Their reuse as group evidence is bookkeeping, not six new holds.

| Evidence ID | Actual stratum (lane / source / task / history) | Proposed group action | Final evidence |
|---|---|---|---|
| exp-v1-javascript-generation-0113 | javascript / Multilingual-Multimodal-NLP/McEval-Instruct / generation / first_pass | Add this stratum to C: required own string-key data lost by spread | JS_TS_FINAL_CONTRACT_ADJUDICATION_20260908.md; prior JS_TS_RESIDUAL_REVIEW_12.md |
| exp-v1-javascript-generation-0270 | javascript / Multilingual-Multimodal-NLP/McEval-Instruct / generation / first_pass | Same C addition; do not duplicate its population | JS_TS_FINAL_CONTRACT_ADJUDICATION_20260908.md; prior JS_TS_RESIDUAL_REVIEW_25.md |
| exp-v1-typescript-generation-0029 | typescript / Multilingual-Multimodal-NLP/McEval-Instruct / generation / corrected | Add this stratum to C: required existing-locker fields lost by spread | JS_TS_FINAL_CONTRACT_ADJUDICATION_20260908.md |
| exp-v1-typescript-generation-0087 | typescript / Multilingual-Multimodal-NLP/McEval-Instruct / generation / corrected | Same C addition; supplied permitted patch field ignored | JS_TS_FINAL_CONTRACT_ADJUDICATION_20260908.md |
| exp-v1-typescript-generation-0064 | typescript / Multilingual-Multimodal-NLP/McEval-Instruct / generation / first_pass | Already in C under v14; append evidence only, membership delta zero | TS_PROPERTY_FINAL_ADJUDICATION_20260908.md |
| exp-v1-javascript-generation-0307 | javascript / Multilingual-Multimodal-NLP/McEval-Instruct / generation / first_pass | Add this stratum to J: explicit integer exception class conflicts with reference and supplied test | JS_TS_FINAL_CONTRACT_ADJUDICATION_20260908.md; prior JS_TS_RESIDUAL_REVIEW_29.md |

JS0307 concerns the mandated exception class, not an intermediate arithmetic overflow. It does **not** justify extending finite_intermediate_arithmetic. J is the existing JS-specific oracle/contract group; duplicating the same addition under the broader reference_accommodates_incorrect_test_or_api group would add redundant obligations without a distinct demonstrated mechanism. The two corrected TS records already belong to that broader API group; only C membership is missing there.

## Exact membership deltas

| Proposed addition | New criterion memberships | Frozen sample | Outside sample | Already held at pinned snapshot | Surviving memberships to reconcile |
|---|---:|---:|---:|---:|---:|
| C × JavaScript McEval generation first_pass | 273 | 14 | 259 | 128 | 145 |
| C × TypeScript McEval generation corrected | 84 | 4 | 80 | 48 | 36 |
| J × JavaScript McEval generation first_pass | 273 | 14 | 259 | 128 | 145 |
| Membership total, intentionally overlapping | 630 | 32 | 598 | 304 | 326 |
| Unique affected IDs | 357 | 18 | 339 | 176 | 181 |

Every one of these 357 records is already in v14's reopened union. Consequently the global reopened union remains **5,500**, its distinct stratum count remains **21**, and new unique-row inspection credit is **0**. C has two existing strata plus two additions; J has two existing strata plus one addition. Both appended strata are already known globally, not newly discovered populations. Existing groups and their frozen memberships must remain preserved in the next version, not silently rewritten in v14.

Suggested next version: append these group evidence IDs and three stratum objects in a successor to followup-systematic-groups-v7.json / stratum-followup-inventory-v14.json, with explicit parent hashes and this report as evidence. Recompute derived memberships; preserve v14 and its historical coverage claims.

## What needs reconciliation, not repeated full inspection

All 339 affected outside-sample IDs have at least one exact coverage-reconciliation-v1.json note/queue-position link; all 18 sample IDs have frozen seven-criterion evidence. There are zero IDs missing prior inspection evidence. JavaScript has 121 array-note and 138 residual-note links (259 IDs); TypeScript has 41 array, 39 residual and 2 targeted links covering 80 IDs, with overlap. These are evidence locations, not automatic C/J approvals.

The necessary narrow join is:

1. Retain current holds as exclusion evidence: the 176 held unique IDs need no new pass solely to exclude them. Preserve their original reasons; group membership does not mean every member exhibits the seed defect.
2. Reconcile C for the exact 181 surviving IDs in the appendix: whether any required caller-supplied property, dictionary entry, or supported patch value is lost through enumerable-only copying. Internally constructed records, explicit named-field reconstruction, scalar-only APIs and expressly enumerable-only contracts may resolve this from existing notes. Do not require preserving arbitrary descriptors, unknown extras or private storage mutation.
3. Reconcile J for the 145 surviving JavaScript IDs in the appendix: exact prescribed input domain, output API and exception semantics versus supplied reference/tests. An unspecified error class is not the JS0307 defect. A passing test is not evidence that an accommodating reference obeys prose.
4. Where the linked note answers the question, carry forward a reasoned scoped disposition. Only a specific unsupported contract point warrants a fresh full contract read, then a bounded probe if static reasoning cannot decide it. This report does not claim that all 326 obligations require fresh reads, nor that they are already closed.

The five surviving affected sample IDs are exp-v1-javascript-generation-0006, -0124, -0196, -0230 and -0374 (each prefix is exp-v1-javascript-generation). sample-criteria-reconciliation-v2.json already marks them positive with individual reasoning: ordered job callbacks/detached state; Map eviction with deliberately shared values and permissible TypeError; safe-integer square-root arithmetic; canonical decimal grammar; and explicit JavaScript-number line arithmetic. Reuse those substantive notes rather than treating their “sample” flag as sufficient. The four corrected TypeScript sample IDs are already held in the pinned current snapshot.

No additional generic pending list or new defects are asserted: the appendix is an exact *membership and evidence-location* ledger. “Surviving; reconcile” below means criterion accounting remains to be joined, not a diagnosis of failure or a mandate for duplicate inspection.

## Pinned inputs

Snapshot contains 2,745 additive holds; the three historical Go/Rust holds are outside these delta strata and do not change the counts above. Concurrent later hold changes require recomputing the held/surviving columns, not changing membership.

| Input | SHA-256 |
|---|---|
| stratum-followup-inventory-v14.json | `4c0e0f9e0d32057f0738a1d57a16146619f6f355b0d686d04e0df0ffd1f44bce` |
| coverage-reconciliation-v1.json | `4d9484ef4012f02e8eb3269f2c57083aa6ddb05b40532c0426b2ecbc351db329` |
| additional-holds.json | `19e0c0705e31461c7b9e77142f3a336a3eaaf60363372e075665462107e20fd2` |
| JS_TS_FINAL_CONTRACT_ADJUDICATION_20260908.md | `47a779ab1fca686b69041c94492b08046616c10e20426a1824d8eabee6f81494` |
| TS_PROPERTY_FINAL_ADJUDICATION_20260908.md | `7d43ac37c43e5eef5f4f86dad4a8738e4e52945801008b5bcb8414183b4dab13` |

## Exact affected IDs and prior evidence

Every JavaScript row adds both C and J. Every TypeScript row adds C only. Evidence paths are relative to this report's directory; “position” is the original queue position, not a line number. The sample evidence is SEVEN_CRITERIA_JAVASCRIPT.md or SEVEN_CRITERIA_TYPESCRIPT.md and sample-criteria-reconciliation-v2.json. No omission is hidden behind a numeric ID range.

| Candidate ID | New memberships | Pinned status | Prior inspection evidence |
|---|---|---|---|
| exp-v1-javascript-generation-0002 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_1.md (position 1) |
| exp-v1-javascript-generation-0004 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_1.md (position 2) |
| exp-v1-javascript-generation-0005 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW.md (position 3) |
| exp-v1-javascript-generation-0006 | C, J | Surviving; reconcile scoped evidence | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0008 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_1.md (position 14) |
| exp-v1-javascript-generation-0011 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW.md (position 13) |
| exp-v1-javascript-generation-0013 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_2.md (position 20) |
| exp-v1-javascript-generation-0014 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_2.md (position 21) |
| exp-v1-javascript-generation-0015 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_2.md (position 22) |
| exp-v1-javascript-generation-0016 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_2.md (position 23) |
| exp-v1-javascript-generation-0018 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_2.md (position 23) |
| exp-v1-javascript-generation-0022 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_2.md (position 30) |
| exp-v1-javascript-generation-0026 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_3.md (position 35) |
| exp-v1-javascript-generation-0027 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_3.md (position 35) |
| exp-v1-javascript-generation-0028 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_3.md (position 36) |
| exp-v1-javascript-generation-0029 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_3.md (position 37) |
| exp-v1-javascript-generation-0030 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_3.md (position 36) |
| exp-v1-javascript-generation-0031 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_3.md (position 44) |
| exp-v1-javascript-generation-0033 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_3.md (position 45) |
| exp-v1-javascript-generation-0034 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_3.md (position 45) |
| exp-v1-javascript-generation-0035 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_4.md (position 46) |
| exp-v1-javascript-generation-0036 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_4.md (position 47) |
| exp-v1-javascript-generation-0037 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_4.md (position 55) |
| exp-v1-javascript-generation-0041 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_4.md (position 54) |
| exp-v1-javascript-generation-0042 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_4.md (position 56) |
| exp-v1-javascript-generation-0043 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_5.md (position 67) |
| exp-v1-javascript-generation-0044 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_4.md (position 60) |
| exp-v1-javascript-generation-0045 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_5.md (position 68) |
| exp-v1-javascript-generation-0047 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_5.md (position 61) |
| exp-v1-javascript-generation-0048 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_5.md (position 69) |
| exp-v1-javascript-generation-0049 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_6.md (position 79) |
| exp-v1-javascript-generation-0050 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_6.md (position 80) |
| exp-v1-javascript-generation-0052 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_5.md (position 67) |
| exp-v1-javascript-generation-0053 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_6.md (position 81) |
| exp-v1-javascript-generation-0054 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_6.md (position 82) |
| exp-v1-javascript-generation-0055 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_7.md (position 95) |
| exp-v1-javascript-generation-0056 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_7.md (position 96) |
| exp-v1-javascript-generation-0057 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_7.md (position 97) |
| exp-v1-javascript-generation-0058 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_7.md (position 98) |
| exp-v1-javascript-generation-0059 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_7.md (position 99) |
| exp-v1-javascript-generation-0060 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_7.md (position 100) |
| exp-v1-javascript-generation-0063 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_6.md (position 76) |
| exp-v1-javascript-generation-0064 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_8.md (position 110) |
| exp-v1-javascript-generation-0065 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_6.md (position 77) |
| exp-v1-javascript-generation-0067 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_6.md (position 87) |
| exp-v1-javascript-generation-0069 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_6.md (position 88) |
| exp-v1-javascript-generation-0070 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_6.md (position 89) |
| exp-v1-javascript-generation-0071 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_8.md (position 115) |
| exp-v1-javascript-generation-0073 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_7.md (position 98) |
| exp-v1-javascript-generation-0074 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_8.md (position 118) |
| exp-v1-javascript-generation-0078 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_7.md (position 99) |
| exp-v1-javascript-generation-0079 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_9.md (position 121) |
| exp-v1-javascript-generation-0080 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_9.md (position 122) |
| exp-v1-javascript-generation-0083 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_7.md (position 104) |
| exp-v1-javascript-generation-0084 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_7.md (position 105) |
| exp-v1-javascript-generation-0086 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_9.md (position 125) |
| exp-v1-javascript-generation-0087 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_8.md (position 117) |
| exp-v1-javascript-generation-0088 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_9.md (position 126) |
| exp-v1-javascript-generation-0093 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_10.md (position 139) |
| exp-v1-javascript-generation-0094 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_9.md (position 121) |
| exp-v1-javascript-generation-0096 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_10.md (position 140) |
| exp-v1-javascript-generation-0097 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_9.md (position 127) |
| exp-v1-javascript-generation-0098 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_9.md (position 128) |
| exp-v1-javascript-generation-0099 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_10.md (position 150) |
| exp-v1-javascript-generation-0100 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_11.md (position 151) |
| exp-v1-javascript-generation-0101 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_11.md (position 152) |
| exp-v1-javascript-generation-0102 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_11.md (position 153) |
| exp-v1-javascript-generation-0103 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_9.md (position 130) |
| exp-v1-javascript-generation-0104 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_11.md (position 157) |
| exp-v1-javascript-generation-0105 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_11.md (position 158) |
| exp-v1-javascript-generation-0106 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_9.md (position 131) |
| exp-v1-javascript-generation-0107 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_9.md (position 132) |
| exp-v1-javascript-generation-0108 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_11.md (position 159) |
| exp-v1-javascript-generation-0112 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_12.md (position 169) |
| exp-v1-javascript-generation-0113 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_12.md (position 170) |
| exp-v1-javascript-generation-0114 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_12.md (position 171) |
| exp-v1-javascript-generation-0115 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_10.md (position 144) |
| exp-v1-javascript-generation-0119 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_10.md (position 145) |
| exp-v1-javascript-generation-0120 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_10.md (position 146) |
| exp-v1-javascript-generation-0121 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_13.md (position 184) |
| exp-v1-javascript-generation-0123 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_13.md (position 185) |
| exp-v1-javascript-generation-0124 | C, J | Surviving; reconcile scoped evidence | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0125 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_13.md (position 186) |
| exp-v1-javascript-generation-0122 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_13.md (position 189) |
| exp-v1-javascript-generation-0127 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_11.md (position 157) |
| exp-v1-javascript-generation-0128 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_11.md (position 158) |
| exp-v1-javascript-generation-0129 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_11.md (position 159) |
| exp-v1-javascript-generation-0130 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_13.md (position 194) |
| exp-v1-javascript-generation-0131 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_13.md (position 195) |
| exp-v1-javascript-generation-0132 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_14.md (position 196) |
| exp-v1-javascript-generation-0137 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_12.md (position 169) |
| exp-v1-javascript-generation-0138 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_14.md (position 201) |
| exp-v1-javascript-generation-0139 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_14.md (position 209) |
| exp-v1-javascript-generation-0141 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_14.md (position 210) |
| exp-v1-javascript-generation-0142 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_15.md (position 211) |
| exp-v1-javascript-generation-0140 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_12.md (position 180) |
| exp-v1-javascript-generation-0146 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_13.md (position 187) |
| exp-v1-javascript-generation-0147 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_13.md (position 188) |
| exp-v1-javascript-generation-0148 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_13.md (position 189) |
| exp-v1-javascript-generation-0149 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_13.md (position 190) |
| exp-v1-javascript-generation-0150 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_13.md (position 191) |
| exp-v1-javascript-generation-0165 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_14.md (position 208) |
| exp-v1-javascript-generation-0168 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_16.md (position 236) |
| exp-v1-javascript-generation-0172 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_17.md (position 245) |
| exp-v1-javascript-generation-0173 | C, J | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0174 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_15.md (position 215) |
| exp-v1-javascript-generation-0175 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_15.md (position 223) |
| exp-v1-javascript-generation-0177 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_17.md (position 255) |
| exp-v1-javascript-generation-0178 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_15.md (position 224) |
| exp-v1-javascript-generation-0179 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_15.md (position 225) |
| exp-v1-javascript-generation-0180 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_18.md (position 256) |
| exp-v1-javascript-generation-0182 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_16.md (position 235) |
| exp-v1-javascript-generation-0183 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_16.md (position 236) |
| exp-v1-javascript-generation-0184 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_16.md (position 237) |
| exp-v1-javascript-generation-0185 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_16.md (position 238) |
| exp-v1-javascript-generation-0186 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_16.md (position 239) |
| exp-v1-javascript-generation-0188 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_17.md (position 244) |
| exp-v1-javascript-generation-0190 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_19.md (position 272) |
| exp-v1-javascript-generation-0191 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_19.md (position 273) |
| exp-v1-javascript-generation-0193 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_17.md (position 248) |
| exp-v1-javascript-generation-0195 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_17.md (position 249) |
| exp-v1-javascript-generation-0196 | C, J | Surviving; reconcile scoped evidence | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0197 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_17.md (position 250) |
| exp-v1-javascript-generation-0198 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_19.md (position 276) |
| exp-v1-javascript-generation-0199 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_18.md (position 260) |
| exp-v1-javascript-generation-0200 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_18.md (position 261) |
| exp-v1-javascript-generation-0201 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_18.md (position 262) |
| exp-v1-javascript-generation-0202 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_18.md (position 263) |
| exp-v1-javascript-generation-0203 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_18.md (position 264) |
| exp-v1-javascript-generation-0206 | C, J | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0209 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_19.md (position 272) |
| exp-v1-javascript-generation-0210 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_20.md (position 289) |
| exp-v1-javascript-generation-0208 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_19.md (position 275) |
| exp-v1-javascript-generation-0212 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_20.md (position 298) |
| exp-v1-javascript-generation-0215 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_20.md (position 299) |
| exp-v1-javascript-generation-0217 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_20.md (position 291) |
| exp-v1-javascript-generation-0218 | C, J | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0219 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_21.md (position 306) |
| exp-v1-javascript-generation-0220 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_20.md (position 292) |
| exp-v1-javascript-generation-0221 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_20.md (position 293) |
| exp-v1-javascript-generation-0223 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_20.md (position 295) |
| exp-v1-javascript-generation-0225 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_21.md (position 310) |
| exp-v1-javascript-generation-0226 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_21.md (position 311) |
| exp-v1-javascript-generation-0227 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_21.md (position 312) |
| exp-v1-javascript-generation-0228 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_20.md (position 296) |
| exp-v1-javascript-generation-0229 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_21.md (position 303) |
| exp-v1-javascript-generation-0230 | C, J | Surviving; reconcile scoped evidence | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0231 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_21.md (position 304) |
| exp-v1-javascript-generation-0232 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_21.md (position 305) |
| exp-v1-javascript-generation-0234 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_22.md (position 321) |
| exp-v1-javascript-generation-0235 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_22.md (position 330) |
| exp-v1-javascript-generation-0236 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_23.md (position 331) |
| exp-v1-javascript-generation-0237 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_21.md (position 309) |
| exp-v1-javascript-generation-0238 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_21.md (position 310) |
| exp-v1-javascript-generation-0239 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_21.md (position 311) |
| exp-v1-javascript-generation-0243 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_21.md (position 315) |
| exp-v1-javascript-generation-0245 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_22.md (position 316) |
| exp-v1-javascript-generation-0246 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_22.md (position 317) |
| exp-v1-javascript-generation-0247 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_22.md (position 327) |
| exp-v1-javascript-generation-0249 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_23.md (position 337) |
| exp-v1-javascript-generation-0250 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_23.md (position 338) |
| exp-v1-javascript-generation-0251 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_23.md (position 339) |
| exp-v1-javascript-generation-0252 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_23.md (position 340) |
| exp-v1-javascript-generation-0253 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_24.md (position 348) |
| exp-v1-javascript-generation-0254 | C, J | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0255 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_24.md (position 349) |
| exp-v1-javascript-generation-0256 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_24.md (position 350) |
| exp-v1-javascript-generation-0257 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_23.md (position 334) |
| exp-v1-javascript-generation-0258 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_24.md (position 351) |
| exp-v1-javascript-generation-0264 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_23.md (position 344) |
| exp-v1-javascript-generation-0265 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_24.md (position 359) |
| exp-v1-javascript-generation-0267 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_24.md (position 360) |
| exp-v1-javascript-generation-0268 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_25.md (position 361) |
| exp-v1-javascript-generation-0269 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_25.md (position 362) |
| exp-v1-javascript-generation-0270 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_25.md (position 363) |
| exp-v1-javascript-generation-0276 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_25.md (position 371) |
| exp-v1-javascript-generation-0277 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_24.md (position 360) |
| exp-v1-javascript-generation-0278 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_26.md (position 385) |
| exp-v1-javascript-generation-0279 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_25.md (position 361) |
| exp-v1-javascript-generation-0280 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_26.md (position 386) |
| exp-v1-javascript-generation-0281 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_25.md (position 362) |
| exp-v1-javascript-generation-0282 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_26.md (position 387) |
| exp-v1-javascript-generation-0283 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_26.md (position 390) |
| exp-v1-javascript-generation-0284 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_27.md (position 391) |
| exp-v1-javascript-generation-0285 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_27.md (position 392) |
| exp-v1-javascript-generation-0286 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_25.md (position 365) |
| exp-v1-javascript-generation-0287 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_27.md (position 393) |
| exp-v1-javascript-generation-0288 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_25.md (position 366) |
| exp-v1-javascript-generation-0289 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_25.md (position 373) |
| exp-v1-javascript-generation-0290 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_27.md (position 400) |
| exp-v1-javascript-generation-0291 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_27.md (position 401) |
| exp-v1-javascript-generation-0293 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_25.md (position 374) |
| exp-v1-javascript-generation-0294 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_27.md (position 402) |
| exp-v1-javascript-generation-0295 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_26.md (position 383) |
| exp-v1-javascript-generation-0296 | C, J | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0298 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_26.md (position 384) |
| exp-v1-javascript-generation-0299 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_26.md (position 385) |
| exp-v1-javascript-generation-0302 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_27.md (position 391) |
| exp-v1-javascript-generation-0303 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_28.md (position 415) |
| exp-v1-javascript-generation-0304 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_28.md (position 416) |
| exp-v1-javascript-generation-0306 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_28.md (position 417) |
| exp-v1-javascript-generation-0307 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_29.md (position 422) |
| exp-v1-javascript-generation-0308 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_27.md (position 393) |
| exp-v1-javascript-generation-0309 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_27.md (position 394) |
| exp-v1-javascript-generation-0310 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_29.md (position 423) |
| exp-v1-javascript-generation-0311 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_29.md (position 424) |
| exp-v1-javascript-generation-0313 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_29.md (position 433) |
| exp-v1-javascript-generation-0315 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_29.md (position 434) |
| exp-v1-javascript-generation-0316 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_27.md (position 399) |
| exp-v1-javascript-generation-0317 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_29.md (position 435) |
| exp-v1-javascript-generation-0318 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_30.md (position 436) |
| exp-v1-javascript-generation-0319 | C, J | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0320 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_27.md (position 402) |
| exp-v1-javascript-generation-0321 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_30.md (position 440) |
| exp-v1-javascript-generation-0322 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_27.md (position 403) |
| exp-v1-javascript-generation-0323 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_30.md (position 441) |
| exp-v1-javascript-generation-0324 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_30.md (position 442) |
| exp-v1-javascript-generation-0325 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_30.md (position 449) |
| exp-v1-javascript-generation-0326 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_28.md (position 408) |
| exp-v1-javascript-generation-0329 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_28.md (position 409) |
| exp-v1-javascript-generation-0330 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_30.md (position 450) |
| exp-v1-javascript-generation-0332 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_31.md (position 456) |
| exp-v1-javascript-generation-0334 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_31.md (position 457) |
| exp-v1-javascript-generation-0335 | C, J | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0336 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_31.md (position 462) |
| exp-v1-javascript-generation-0337 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_31.md (position 463) |
| exp-v1-javascript-generation-0339 | C, J | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0340 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_31.md (position 464) |
| exp-v1-javascript-generation-0341 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_31.md (position 465) |
| exp-v1-javascript-generation-0342 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_28.md (position 420) |
| exp-v1-javascript-generation-0343 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_32.md (position 471) |
| exp-v1-javascript-generation-0344 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_29.md (position 427) |
| exp-v1-javascript-generation-0345 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_32.md (position 472) |
| exp-v1-javascript-generation-0348 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_32.md (position 475) |
| exp-v1-javascript-generation-0350 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_32.md (position 478) |
| exp-v1-javascript-generation-0351 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_32.md (position 479) |
| exp-v1-javascript-generation-0353 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_32.md (position 480) |
| exp-v1-javascript-generation-0355 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_30.md (position 440) |
| exp-v1-javascript-generation-0356 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_33.md (position 482) |
| exp-v1-javascript-generation-0357 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_33.md (position 483) |
| exp-v1-javascript-generation-0358 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_30.md (position 441) |
| exp-v1-javascript-generation-0360 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_33.md (position 484) |
| exp-v1-javascript-generation-0361 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_30.md (position 449) |
| exp-v1-javascript-generation-0362 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_33.md (position 490) |
| exp-v1-javascript-generation-0364 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_33.md (position 491) |
| exp-v1-javascript-generation-0365 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_33.md (position 492) |
| exp-v1-javascript-generation-0366 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_33.md (position 493) |
| exp-v1-javascript-generation-0367 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_31.md (position 454) |
| exp-v1-javascript-generation-0368 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_34.md (position 504) |
| exp-v1-javascript-generation-0369 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_31.md (position 455) |
| exp-v1-javascript-generation-0370 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_34.md (position 505) |
| exp-v1-javascript-generation-0371 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_31.md (position 456) |
| exp-v1-javascript-generation-0372 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_31.md (position 457) |
| exp-v1-javascript-generation-0373 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_31.md (position 461) |
| exp-v1-javascript-generation-0374 | C, J | Surviving; reconcile scoped evidence | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0375 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_31.md (position 462) |
| exp-v1-javascript-generation-0376 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_34.md (position 507) |
| exp-v1-javascript-generation-0377 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_31.md (position 463) |
| exp-v1-javascript-generation-0378 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_34.md (position 508) |
| exp-v1-javascript-generation-0379 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_35.md (position 519) |
| exp-v1-javascript-generation-0380 | C, J | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_35.md (position 520) |
| exp-v1-javascript-generation-0381 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_32.md (position 477) |
| exp-v1-javascript-generation-0382 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_32.md (position 478) |
| exp-v1-javascript-generation-0383 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_32.md (position 479) |
| exp-v1-javascript-generation-0385 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_32.md (position 480) |
| exp-v1-javascript-generation-0386 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_33.md (position 481) |
| exp-v1-javascript-generation-0388 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_33.md (position 482) |
| exp-v1-javascript-generation-0389 | C, J | Held; retain exclusion | ARRAY_STRATUM_REVIEW_33.md (position 483) |
| exp-v1-javascript-generation-0390 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_35.md (position 521) |
| exp-v1-javascript-generation-0392 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_35.md (position 522) |
| exp-v1-javascript-generation-0393 | C, J | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_35.md (position 523) |
| exp-v1-javascript-generation-0394 | C, J | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_JAVASCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-javascript-generation-0395 | C, J | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_33.md (position 484) |
| exp-v1-typescript-generation-0003 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_1.md (position 6) |
| exp-v1-typescript-generation-0012 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW.md (position 11) |
| exp-v1-typescript-generation-0013 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_2.md (position 21) |
| exp-v1-typescript-generation-0015 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_2.md (position 18) |
| exp-v1-typescript-generation-0016 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_2.md (position 22) |
| exp-v1-typescript-generation-0018 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_2.md (position 19) |
| exp-v1-typescript-generation-0019 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_2.md (position 29) |
| exp-v1-typescript-generation-0020 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_3.md (position 31) |
| exp-v1-typescript-generation-0026 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_3.md (position 42); TARGETED_STRATUM_REVIEW.md (position 1) |
| exp-v1-typescript-generation-0027 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_3.md (position 43) |
| exp-v1-typescript-generation-0029 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_3.md (position 43) |
| exp-v1-typescript-generation-0030 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_3.md (position 44) |
| exp-v1-typescript-generation-0039 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_5.md (position 66) |
| exp-v1-typescript-generation-0043 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_6.md (position 77) |
| exp-v1-typescript-generation-0046 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_6.md (position 78) |
| exp-v1-typescript-generation-0054 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_7.md (position 94) |
| exp-v1-typescript-generation-0055 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_5.md (position 74) |
| exp-v1-typescript-generation-0056 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_8.md (position 109) |
| exp-v1-typescript-generation-0057 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_5.md (position 75) |
| exp-v1-typescript-generation-0076 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_9.md (position 124) |
| exp-v1-typescript-generation-0085 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_9.md (position 124) |
| exp-v1-typescript-generation-0086 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_9.md (position 125) |
| exp-v1-typescript-generation-0087 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_9.md (position 126) |
| exp-v1-typescript-generation-0099 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_10.md (position 142) |
| exp-v1-typescript-generation-0104 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_13.md (position 193) |
| exp-v1-typescript-generation-0113 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_14.md (position 199) |
| exp-v1-typescript-generation-0123 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_13.md (position 185) |
| exp-v1-typescript-generation-0125 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_15.md (position 215) |
| exp-v1-typescript-generation-0126 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_13.md (position 186) |
| exp-v1-typescript-generation-0134 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_16.md (position 230) |
| exp-v1-typescript-generation-0137 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_16.md (position 231) |
| exp-v1-typescript-generation-0141 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_16.md (position 233) |
| exp-v1-typescript-generation-0147 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_17.md (position 244) |
| exp-v1-typescript-generation-0157 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_16.md (position 231) |
| exp-v1-typescript-generation-0158 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_16.md (position 232) |
| exp-v1-typescript-generation-0159 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_16.md (position 233) |
| exp-v1-typescript-generation-0160 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_16.md (position 234) |
| exp-v1-typescript-generation-0169 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_19.md (position 280) |
| exp-v1-typescript-generation-0170 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_18.md (position 259) |
| exp-v1-typescript-generation-0174 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_19.md (position 281) |
| exp-v1-typescript-generation-0176 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_18.md (position 270) |
| exp-v1-typescript-generation-0178 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_20.md (position 287) |
| exp-v1-typescript-generation-0179 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_20.md (position 288) |
| exp-v1-typescript-generation-0183 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_19.md (position 281) |
| exp-v1-typescript-generation-0198 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_21.md (position 302) |
| exp-v1-typescript-generation-0224 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_24.md (position 354) |
| exp-v1-typescript-generation-0228 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_25.md (position 370) |
| exp-v1-typescript-generation-0234 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_26.md (position 383) |
| exp-v1-typescript-generation-0236 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_27.md (position 399) |
| exp-v1-typescript-generation-0242 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_26.md (position 381) |
| exp-v1-typescript-generation-0245 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_28.md (position 408) |
| exp-v1-typescript-generation-0246 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_26.md (position 382) |
| exp-v1-typescript-generation-0247 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_28.md (position 414) |
| exp-v1-typescript-generation-0249 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_26.md (position 390) |
| exp-v1-typescript-generation-0253 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_27.md (position 397) |
| exp-v1-typescript-generation-0255 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_27.md (position 398) |
| exp-v1-typescript-generation-0256 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_29.md (position 428) |
| exp-v1-typescript-generation-0257 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_29.md (position 429) |
| exp-v1-typescript-generation-0258 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_29.md (position 430) |
| exp-v1-typescript-generation-0267 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_28.md (position 417) |
| exp-v1-typescript-generation-0273 | C | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_TYPESCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-typescript-generation-0274 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_29.md (position 425) |
| exp-v1-typescript-generation-0275 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_29.md (position 426) |
| exp-v1-typescript-generation-0289 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_34.md (position 502) |
| exp-v1-typescript-generation-0312 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_36.md (position 528) |
| exp-v1-typescript-generation-0320 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_36.md (position 536) |
| exp-v1-typescript-generation-0321 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_36.md (position 537) |
| exp-v1-typescript-generation-0335 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_37.md (position 548) |
| exp-v1-typescript-generation-0345 | C | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_TYPESCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-typescript-generation-0352 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_35.md (position 514) |
| exp-v1-typescript-generation-0355 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_38.md (position 565) |
| exp-v1-typescript-generation-0358 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_35.md (position 520) |
| exp-v1-typescript-generation-0364 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_38.md (position 568) |
| exp-v1-typescript-generation-0365 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_35.md (position 524) |
| exp-v1-typescript-generation-0368 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_36.md (position 529) |
| exp-v1-typescript-generation-0369 | C | Surviving; reconcile scoped evidence | JS_TS_RESIDUAL_REVIEW_39.md (position 572) |
| exp-v1-typescript-generation-0378 | C | Surviving; reconcile scoped evidence | ARRAY_STRATUM_REVIEW_36.md (position 530) |
| exp-v1-typescript-generation-0379 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_36.md (position 533) |
| exp-v1-typescript-generation-0380 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_36.md (position 534) |
| exp-v1-typescript-generation-0381 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_36.md (position 535) |
| exp-v1-typescript-generation-0382 | C | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_TYPESCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-typescript-generation-0383 | C | Held; retain exclusion | ARRAY_STRATUM_REVIEW_36.md (position 536); TARGETED_STRATUM_REVIEW.md (position 10) |
| exp-v1-typescript-generation-0390 | C | Held; retain exclusion | Frozen sample: SEVEN_CRITERIA_TYPESCRIPT.md; sample-criteria-reconciliation-v2.json |
| exp-v1-typescript-generation-0392 | C | Held; retain exclusion | JS_TS_RESIDUAL_REVIEW_40.md (position 586) |

