# R16 provisional Go test-only correction — 2026-09-08

Status: **PROVISIONAL — main validation/approval required**. Exactly ten original Go generation parents, each reusing its exact reviewed R12 candidate for one bounded independent test correction. No reservation, generation, execution, cloud use, admission, ledger edit or new original coverage occurred. No additional critic rounds are authorized by this draft.

## Workflow/schema reconciliation

Read complete `scripts/data/correct_recovery_tests.py` (SHA-256 `407f14c7a07babfce0e5f06a86cfd2c00c24b8504cc8b82874dbca0a0278f975`) and the R7 provisional request/feedback examples. Requests retain original parent IDs/canonical hashes and declare `oracle-rebuild`. Feedback is keyed by exact new R16 IDs with `previous_candidate_sha256` binding the R12 candidate, plus nonempty `specification_review`. There is no reference/mutant source code in that feedback.

The correction workflow copies the prior candidate and changes only derived identity/lineage plus test content/hash; specification, assistant reference and known-bad code must remain byte-identical. Its run contract rejects a prior run already marked correction_attempt. Main must validate the current closure/corpus/hold ledger and lane batch limits before finalization; never call the workflow merely to validate, because main() reserves a version and invokes a teacher.

The primary quality basis is `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R12_GO_REVIEW_20260908.md`, SHA-256 `adbf72043d37d718a1d05ac4c114c7bdd0f8c7a0ccc5ad3cce4f1311bc919b5b`. All ten references had scoped static-positive correction assessments; all ten tests were held. These proposals do not clear those holds.

## Exact selection and prior bindings

Original IDs use `exp-v1-go-generation-<suffix>`; previous IDs use `exp-v1-recovery-r12-go-generation-<suffix>`; required new IDs use `exp-v1-recovery-r16-go-generation-<suffix>`. Prior candidate paths are in `datasets/cache/expansion-v1/versioned-recovery/r12/`. Canonical SHA-256 uses sorted compact UTF-8 JSON, ensure_ascii=false.

| Suffix | Original parent canonical SHA-256 | Previous R12 candidate canonical SHA-256 |
|---|---|---|
| 0072 | `324059f2ab4588d324dd392c8a09206050c98db6a903c813c0449725896146a6` | `23b132e85571fd015604b0c918bcd0363069c0b4ddbc3fb098e310d8d6ee2c53` |
| 0084 | `4880da15d57b6cae3153e1410178ca61728e95848149fcf63cb1c0381b20bc29` | `429f9aa02d85f993ab46394d3ae0ed5c29d3c0d271b87c916129aad569233743` |
| 0133 | `001f7a5e4245bb8e664d489f74364def16276ca5bb674f1691e5cf6250f330c0` | `73982812c6677b8d04e08731e91ac05e5e5815e30b3106fb2c17d25aeccff016` |
| 0149 | `ced5e779da6d43dfa9e1cb49213bcbda6f2b6351f2e9063a742ac79537fb564c` | `0115aca38d542c4ac729fdeb7237aac032c45d9b9819260c3f1fb9e15a9132f0` |
| 0204 | `b0911cfea3b4bfeaa79feffc2e1ef1fee103e28aba5320515d0cbdaebcd6b5ce` | `c70866696af5d51a3f0824fde9f9eff98b09f4bb7c77da39882352c2d1605a7f` |
| 0234 | `f743b378be9f7bcb536e86973669c1cbead45f0b1556d79cc8077f14c19682cb` | `958417d368d3c44592112e70ad6a93d2ae5203cea8b12b645b6e377ef631c5e2` |
| 0266 | `16aab2d4078c16d399336e6fba8bccb6c41a7162f2f2093fe95fc30c7428a122` | `7168f5f04b9cbc6748e07eb6568d59d10a8c8143c7120b3248292ed4c768a0b9` |
| 0326 | `643ed0c3f460d89800673636d0609ac2250861752908ecb56f713e0ed0737198` | `c5dc02ecff1a44e9665cf05135cc405a21dfbfa6d7db1e1d01f99530cd277c51` |
| 0360 | `64b45b8fc1a1ce9398a14fb2e1bee722871bd506168b02d7dc1f2a95efe05846` | `5fc2ec2a2e5543aa175c61779c41d466f654270f656112143b213164d8bf845b` |
| 0409 | `a9adb8cd38d9b6a6d8c6217e807c6139a9cd7939785e1234255c9cbf581ed5a8` | `6266a732a2380a001bf495c6df15c060b461cce1453e633d0ebf7516a423e3a3` |

Original source records/rights remain those in the R12 plan and bound review appendix: McEval-Instruct/CC-BY-SA-4.0, all five recorded rights true. No source/rights reinterpretation or admission claim. R12 plan file SHA-256 `0c522543ba287bb2d4fc45029e1c35807197a3451b7ae581181798fb27bff121`.

## Correction contents

- 0072: control-character JSON round-trip, emitted key order and json.Compact comparison before the final newline. Do not constrain equivalent escape spellings or reject whitespace inside strings. Preserve exact Go-quoted line semantics.
- 0084: restore required URL→Url match; lowercase url is ineligible. Add Aİ/Ai nonmatch and Unicode self-match with valid ambiguity/type/order controls.
- 0133: two valid NUL-containing structural identities with independent lifecycle. Only empty scope has an explicit nonnil empty List requirement.
- 0149: two NUL-containing method/pattern identities, exact resolutions and true duplicate rejection. Constructor errors do not imply a nil Router; Resolve retains its explicit failure tuple.
- 0204: MaxInt requested prefix has only41 real results, bounded recurrence and permanent exhaustion; no giant allocation or iteration in the test.
- 0234: textual ID18446744073709551616 through CRUD, lexicographic ordering and tag isolation, no machine-int cap.
- 0266: Cursor1/PageSizeMaxInt with one/two records. Remove success-empty nonnil assertions and non-promised error secondary-value constraints; malformed timestamps retain the explicit nil/empty/error tuple.
- 0326: correct suffix length using the actual expected string or full expected output. Independent span/gap overflow and single-span MaxInt exact fit. Rejection requires error, not unspecified empty output.
- 0360: Unicode-invalid minimum in parse/filter. Pick one of six values0..5 absent from all five exported constants; this is guaranteed and avoids overflow, numeric-origin or iota assumptions. Do not use Fatal+1.
- 0409: original item at empty-string key must be returned on error. Preserve nilness when snapshotting a nil table; retain atomicity and pointer ownership.

Full specification-derived feedback is in the companion JSON. Every change is test-only; no reference or specification amendments are proposed. Eight defining witnesses were missing; 0326/0360 already had their held witnesses but need valid oracles.

## Draft artifact hashes and next gates

- `recovery-requests-r16-PROVISIONAL.json`: `954230e75cc0a57cee0e177f995c839b8e3a77bce6feda832daf5c5d2786e97e`.
- `recovery-test-feedback-r16-PROVISIONAL.json`: `5adbfe13ec77231b8fd45010b4b639c2ab0c89523a41bf16426e29ffae9816a4`.

After main approval, normal workflow must preserve exact prior artifacts and provenance, obtain fresh corrected tests under the one-correction limit, verify byte preservation, perform independent quality review and resource-limited network-disabled sandbox directionality. False-oracle or compile failures do not count as semantic mutant evidence. Nothing here launches or reserves R16.

