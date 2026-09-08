# Recovery r2 JavaScript corrected-test review — 2026-09-08

Scope: only `exp-v1-recovery-r2-javascript-generation-0014` and `exp-v1-recovery-r2-javascript-generation-0270`, full corrected tests, unchanged prompt/reference/known-bad and exact correction context/output. Static review only: no candidate execution, teacher invocation, cloud access, candidate modification or central-state edit. This is the one requested bounded correction review, not an automatic repeat critic loop.

**Both r2 artifacts are scoped static quality-positive for sandbox verification.** The r1 oracle blockers are removed and correction-specific known-bad witnesses now exist. No admission or executed result is claimed; original and r1 held artifacts are not cleared.

## 0014

The unsupported existing-key `changes: []` rejection has been removed; the test takes no position on that unrequired prohibition. Array-valued *commands* without a type still reject, correctly as unknown/malformed commands. Mandatory optional-extra retention assertions were removed and replaced with required-field value checks. No universal deep-copy or inherited-patch rule was added.

The test now constructs one entry with all four required properties non-enumerable and another with all four inherited. Construction must preserve their directly readable strings in copied records. The unchanged reference explicitly materializes those fields; the mutant spreads both into empty objects and then encounters duplicate undefined keys. That thrown duplicate error is a meaningful consequence of required-field loss, not an impossible-input or unrelated oracle failure. The individual required-value checks would also detect the loss if reached. Inherited-field addition and reference-preserving search provide further coverage. Own non-enumerable `code` changes are exercised without demanding descriptor preservation.

Missing-key edits with `changes: null` and with an irrelevant invalid code value must return the original registry. The reference checks key absence first; the mutant rejects null changes before checking absence. This separately supports the no-op precedence correction. Ordinary add/remove/edit, successful-copy identity, unchanged-entry sharing, duplicates, malformed input and case-insensitive search remain covered.

Residual coverage limitation, not a discovered defect: the new edit witness uses a hidden patch against ordinary current entries, rather than an externally supplied current entry with hidden required fields. Full reference inspection confirms its affected-record copy explicitly materializes all four fields, so this omission is not a reason for another automatic correction cycle or hold. The requested required-field mechanism has meaningful constructor/add witnesses and the edit code is statically supported.

## 0270

Metadata/note retention expectations have been removed. Replacement checks only required `id`, `label`, `hours`, `pinned` values and object detachment. No descriptor-preservation assertion was added. Ordinary null-prototype/ordering/special-key checks remain; `-0` is copied without arithmetic normalization, and finite maximum hours is valid under the stated contract.

The decisive fixture now supplies a valid external null-prototype dictionary with hidden own `engine`, enumerable `wing`, and order `["engine", "wing"]`. Pinning wing must retain the exact engine reference, preserve order identity and replace only wing/root/dictionary. The unchanged reference copies all own keys; the mutant's `Object.assign` drops engine, so the engine identity assertion meaningfully distinguishes the original defect. Unpinning the resulting state checks continued sharing and state transition. The unpin fixture follows the corrected pin output, so it is not an independent hidden-dictionary unpin witness; the shared pin/unpin implementation and direct pin witness suffice for this bounded correction decision.

Hidden required part fields on replacement are now exercised. No inherited-field or hidden affected-record pin fixture was added; static inspection confirms explicit required-field materialization in replacement and affected-copy paths. These are bounded coverage limitations, not new reference defects. Unknown-ID identity, repeated pin/unpin allocation, invalid replacement atomicity, required validation, `__proto__` data IDs and no input mutation remain covered.

## Seven-criterion reconciliation

| Criterion | 0014 | 0270 |
| --- | --- | --- |
| Prompt clarity | Positive under unchanged required-field/no-op contract; optional extras remain optional. | Positive under bounded required-part/dictionary preservation contract; arbitrary extras not imposed. |
| API consistency | Positive: exact CommonJS exports and supported operation/identity assertions. | Positive: reducer export, normalized state and selective-sharing assertions. |
| Independent test origin | Positive with qualification: specification-and-proposed-test-only independent correction, not fresh specification-only authorship. No reference/mutant exposure in archived context. | Same. |
| Non-triviality | Positive: complete immutable registry lifecycle, validation and search interactions, carried from full r1 review. | Positive: transactional normalized replacement and structural-sharing transitions, carried from full r1 review. |
| Idiomatic code | Positive: unchanged explicit required-field materialization and ordinary collection operations. | Positive: unchanged all-own-key null-prototype dictionary copy. |
| Dependency isolation | Static positive: CommonJS and Node standard library; execution remains pending. | Same. |
| Realistic known-bad failure | Positive statically: hidden/inherited required-field loss and absent-key validation-order witnesses. | Positive statically: hidden unaffected dictionary-entry loss witness. |

No newly identified unsupported assertion or static reference mismatch. Counts: 2 scoped static positives, 0 new holds, 0 unresolved contract questions, 0 executions, 0 admissions, 0 new unique-original-row coverage.

## Exact evidence and hashes

Both prompts/references/mutants are byte-identical to their r1 equivalents, verified directly. The correction prompt embeds exact r1 test files and the unchanged specifications plus specification-derived reviewer guidance; it does not embed reference or known-bad code. Corrected output test strings exactly equal the candidate test files. Thus this evidence is an independently authored correction with visible proposed tests, not an assertion that the critic saw only a specification.

Correction metadata reports return code 0, timeout false, no disallowed tool items and no event parse error. Prompt/final output/stdout/stderr hashes were recomputed and match declarations. These are author metadata, not candidate-verification evidence.

All r2 paths below are beneath `datasets/cache/expansion-v1/versioned-recovery/r2/`.

| Binding | SHA-256 |
| --- | --- |
| `plan.json` file | `5dae7eac34ac462f6173dc6b740364d5c4b68129950359f453f4038111ad1d29` |
| `javascript-recovery-test-correction-evidence.json` file | `3355294570b371c6e8c6e19b8f441d91d511317cfbc9b13270f1251938aed03c` |
| Critic prompt/context content | `6ab100c0f93f5fe38e0b5675337ee82861b210716c7c5aa20ec9ad3e1c74feb6` |
| Critic final output content | `4c29af5d0adcb69adf271fe4fbe8db65cbaaff8d678eac4c20b79dcd797eb5c7` |
| Critic stdout content | `c36c10414eb8f0cb001843749110b8d24faaa4cdbc4515d91200556da60c6ced` |
| Critic stderr content | `9c72468673da8afbdc7e9043a93c77a88a1107c6a0bf95a0698e60ee72307081` |
| Bound r1 JavaScript review file | `6a80604727741b6c2a57cdc05b55a6aa0f3c360d0cf0661318a82ec3982aff28` |

| Content binding | 0014 | 0270 |
| --- | --- | --- |
| Candidate file (exact r2 ID plus `.candidate.json`) | `4acdf7f3c6028629f8f0660b3154f4859703f7907f53679ae30369d76b9002d1` | `7724ff4d99939b072725802adf1edc0a59ec83c2079d37c1d1c66862eb451d68` |
| Prompt | `6365dfb0f4ff6941ebe8b2cd2aa6a255224f600c5151f16b2976823f1878cacc` | `e1f5f3610d02b4c5ac79babb64c6862da58b21af8b6f333f63feff086c57097a` |
| Reference | `d179ac45d8be8f63af8e742704a2ad8704b4880312d35de41f2544db74ed3551` | `c47477ae5bbe2f2abde5006f3e7700ca5124247b9fd652bb8d27da6bfa02e464` |
| Corrected test | `e39ae81d699d3d535fedc58f7e56f745c3e06f1014cd6c0cae9b52bc0f42d051` | `9be21f762b7b23c691a6f4433870c8083cfce6bc1f9731e64898da7f3ee38f2b` |
| Known-bad | `f00baa13dd4a65cf6adb69e89c4b41f317c7abe27a8933f109fe344146f980e9` | `d72c38f3d309f37d2b9d402e69b911759c131b4042149727bfcc489a061aa8cc` |

The r2 plan binds original parents `exp-v1-javascript-generation-0014` / `0270` to canonical hashes `e545f4c21fb6f2b5cbbd468b700b96f652be2cc4c7cb3a1a7b0e36678e3931e8` / `a7b809fba05e9a23cf9977b895faa05a982b73cf871ff9bcc8e70f99b42820cd`, preserving the original held-parent lineage rather than silently replacing it. Main owns serial resource-limited network-disabled verification and all remaining admission/separation gates.
