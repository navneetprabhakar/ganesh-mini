# Recovery r3 TypeScript generation review — 2026-09-08

Scope: six derived generation candidates 0022, 0140, 0195, 0261, 0270 and 0281 under `datasets/cache/expansion-v1/versioned-recovery/r3/`. Full derived prompts, references, independent tests and supplied mutants were read, together with each approved r3 plan entry. No execution, generation, cloud access, central edit or admission. Zero original-row coverage credit.

**Decision: all six current artifacts HOLD for test adequacy; three additionally have concrete compiler/oracle issues.** References statically implement the requested corrections, but no supplied suite exercises its recovery-defining difference. Ordinary coverage or an unrelated failure cannot establish meaningful mutant rejection. Main owns serial sandbox evidence; the findings here are static predictions, not executed outcomes.

## Individual decisions

| Suffix | Current artifact | Reference correction | Blocking issue |
| --- | --- | --- | --- |
| 0022 | HOLD | Safe own data-property insertion and copying preserve arbitrary allowed parameter names. | No __proto__ parameter witness; test accesses nullable matches after a non-narrowing void assertion helper. |
| 0140 | HOLD | All three fallback branches unescape ordinary text once. | No escaped unknown/malformed/incomplete fallback witness. |
| 0195 | HOLD | Per-registration objects and explicit Workshop/row/filter fields repair both scoped defects. | No duplicate-function unsubscribe witness and no hidden typed-field fixture. |
| 0261 | HOLD | Per-registration objects preserve independent unsubscribe order; frozen field snapshots retained. | No duplicate-function unsubscribe witness. |
| 0270 | HOLD | Per-registration objects plus complete-match-length check repair unsubscribe and trailing-newline acceptance. | Neither repair witness; tests impose unsupported RangeError for blank identifiers, while reference throws TypeError. |
| 0281 | HOLD | Per-registration objects preserve unsubscribe identity and ordered mutations. | No duplicate-function witness; tests demand excluded per-listener event isolation and unsupported RangeError for blank labels. |

### 0022 — path matcher

The reference uses Object.defineProperty for captured keys and safe output copying; specificity keeps the earliest equal-score route, fallback remains first, and parameter strings remain raw. The supplied mutant is the original unsafe dictionary implementation. Tests use ordinary id/item/value names only: none contains __proto__, constructor or toString. No normal case distinguishes the repaired defect.

The test declares `assert(condition: boolean, message: string): void`, then checks `matchOne !== null && matchTwo !== null` through that helper and subsequently accesses both `.params` values. A void helper is not a TypeScript assertion signature; the nullable union therefore remains. Strict compilation is predicted to reject these accesses. Fix test narrowing explicitly or use a correctly declared assertion helper; do not weaken RouteMatch|null or add a reference overload merely to compile the test. Add a grammar-valid /:__proto__ capture and assert its own key/value, without constraining the params prototype.

### 0140 — inline notes

Unknown markers, routes without an unescaped separator and incomplete markers now append unescapeText of their raw fallback slice. This is the requested single unescape pass without reparsing escaped delimiters. Existing tests exercise escapes in recognized payloads and ordinary outside text, but the unknown/malformed/incomplete fixtures contain no escape. The original mutant therefore behaves identically on those fixtures. Add escaped content in each fallback class, doubled/trailing backslashes and adjacency coalescing. The current non-nesting fixture uses the first closing marker boundary and is consistent with the non-nesting contract; it is not itself the recovery witness. No static reference mismatch identified.

### 0195 — workshop toolbar

Subscription records are unique objects, removed by their own identity; required Workshop, WorkshopRow and WorkshopFilter fields are copied explicitly. Transactional row replacement, loading/mapping error reporting, dialog cancellation/rejection, reset-filter emission and per-listener filter copies remain coherent. Existing tests cover these ordinary interactions but use distinct listener functions only and plain enumerable objects throughout. Add A,B,A with the last A's unsubscribe, expecting A,B; independently test hidden required typed fields from loader input, mapper output and filter input. Do not force copying arbitrary extras. The reference is statically supported; the suite cannot reject the supplied original mutant on either documented defect.

### 0261 — panel store

Unique subscription records repair the original indexOf(function) bug without skipping listeners removed from the captured notification list. Every delivery obtains a fresh frozen explicit-field snapshot; repeated values still notify and state commits before exception propagation. The suite uses distinct first/second/late callbacks; no duplicate callback registration is removed out of order. Add A,B,A then unsubscribe the last A twice, and trigger a supported set/toggle. Preserve existing explicit-undefined initial rejection and snapshot tests. No new runtime domain or reentrant state-snapshot rule is inferred.

### 0270 — fixed-scale vault

The reference preserves scale grammar and bigint arithmetic while requiring match[0].length===text.length, blocking the original regex dollar-anchor terminal-line-break acceptance. Unique account subscription records repair independent removal. The test's malformed strings omit terminal line breaks and its subscriptions use distinct callback functions; neither repair is witnessed.

It also demands RangeError for whitespace-only symbol, account and allowance owner. The specification requires non-whitespace identifiers but does not mandate that subtype; the unchanged reference's TypeError is valid and was retained under the approved scope. These assertions will reject reference and mutant for an unrelated reason. Relax only unsupported identifier exception-subclass assumptions; preserve the explicitly specified malformed-amount RangeError and non-string amount TypeError. Add terminal LF/CR/CRLF/U+2028/U+2029 at zero and nonzero decimals and independent duplicate removal after discarding required immediate callbacks. Do not infer subscribe rollback after an immediate listener throws.

### 0281 — release timeline

Unique subscription records repair removal order. The reference intentionally shares one detached event object across the listener snapshot; its event entry cannot mutate internal state. The approved r3 plan explicitly says per-listener event isolation is not promised. Yet the first test listener writes event.entry.label='listener mutation' and the second is expected to see 'One', described as independent event copies. Both reference and mutant instead deliver the shared detached mutation. This is an unsupported oracle, not authority to change the reference.

The tests also require RangeError for blank append/rename labels; the prompt mandates RangeError for malformed/absent IDs, not blank-label subclass, and the reference uses TypeError. Require rejection without adding an unsupported subtype, while preserving explicit ID error requirements. Finally, add A,B,A unsubscribe-last to actually distinguish the supplied mutant. Keep mutation commitment on listener error, snapshot membership, insertion/promote order, no reuse in bounded sequences and detached public state; do not add event-per-listener isolation.

## Seven original quality criteria

| Criterion | Assessment |
| --- | --- |
| Prompt clarity | All six have self-contained APIs and supported bounded repair scope. Identifier/label error subtype and timeline per-listener event isolation are not promised and must not be silently added by tests. |
| API consistency | Reference APIs are statically coherent. 0022 test null narrowing is invalid under strict compilation; 0270/0281 oracles conflict with permitted reference behavior. |
| Independent test origin | Supported: archived independent prompt contains only exact task IDs/specifications and generic runtime/test instructions; no reference, mutant or original tests. Independence does not establish adequate coverage. |
| Non-triviality | Positive scoped judgment: ranking/validation matcher, escape parser, async transactional toolbar, frozen snapshot state store, bigint vault, ordered observable timeline. No padding was added to justify the fixes. |
| Idiomatic code | Scoped positive: standard TypeScript/JDK-free JavaScript library mechanisms, registration identities, explicit records and safe key insertion; no new reference style blocker found. |
| Dependency isolation | Static positive: standard-library source and local manual tests; sandbox compilation/execution is still main's gate. |
| Realistic known-bad failure | Each original-reference mutant has a real specified defect, but every current suite lacks the corresponding distinguishing witness. HOLD all six until meaningful rejection is established. |

No fresh reference-defect hold is asserted. Counts: 6 artifact holds, 0 artifact positives, 3 artifacts with additional compiler/oracle blockers, 0 executions, 0 admissions, 0 original-row coverage credit.

## Evidence bindings

R3 plan file SHA-256: `cbad9d14a504531e749b5eb3433f0bf4670e21f2a8e8d5f310d2e843e53c6231`. Plan scope is bound to RECOVERY_TRANCHE_JS_TS_20_20260908.md SHA-256 `029d28f88e1b4923dcc5ca64e84bafb9c08c0031ff631750bba9c672445261f9`. Candidate prompt/reference/mutant match architect output exactly; candidate tests match independent output exactly. Independent prompt task objects contain only id/problem, and every problem equals the corresponding full derived prompt read above.

Both author evidence records have returncode 0, timeout false, no disallowed tool items and no event parse error. Prompt/final-output/stdout/stderr hashes reproduce declarations. This is teacher metadata, not verifier success.

- `typescript-recovery-architect-evidence.json`: file `28d496ea7bf987a57b8485efc0c68bf1ddfe971e3cba4ff0b396b61a78d5c39a`; prompt `20bc81bbbcd076c89176fc0f8bd289117b979c6dc98ee724b0b2f8ce15e21408`; final output `dfa1621f495affbb9005b8e056c0ca79c5aa5ea0150644405dc90880b8cde515`.
- `typescript-recovery-independent-tests-evidence.json`: file `eeb9d23864ab6567b32fc2bd0e93afe297c7bae8c8e3addb4f9a63f7c621df62`; prompt `442e9ea6ec9c18296499eecf1489bf7217ddd2e74a4696fe5cfb19a0f8727e78`; final output `db51da318e54e3aebd56757929c0d6026601f3ecb57dc79ee540d3279e004ed9`.

| Candidate suffix | Exact candidate file SHA-256 | Prompt SHA-256 | Reference SHA-256 | Test SHA-256 | Mutant SHA-256 |
| --- | --- | --- | --- | --- | --- |
| 0022 | `28c35c80422048a76de85b14e70e028116b7b36d4736b613d1e210c3971a793e` | `ffeea915662c1262010a07df2d279d76fe3300d4826d3fdf37ccb56789eaad0a` | `e6265e1491e19f9d1b4dd76e4749f414385ba1772a39a6af0bc4a3d495c4f754` | `083d3da449281371f5268c99ce15712161b71d9c8bed33915cc780c0b492469d` | `da2c1e73a3bf56d4d20f3c6d57a6c2a54a30e173b1239120655df0b82590e46d` |
| 0140 | `ef3b8d4c4529f5c7ba28eac5e7b334ed2690f915455b7c804445b0ab729ecddf` | `995abcda56cb7663e3ee1fb64b853cff7201b4802b06939abaaaafd5644b0c81` | `c0a088c1c91c95e015b7f1cf1d2f92e053a76fa290ceafd744fa0fdea203acd1` | `94e2fb442aa88984618e377934e5efc7821258a060977f2563eb2c628c75eda7` | `b574373092cc0a3d7fe2d2b20d56d24df02fd3ffa04a1cc1e21701f6e871b2f1` |
| 0195 | `fa48f88c5e73046566883a57970a5c3f8345f78c3f0def608114e577f3240ff7` | `1c738d11e23d7fb56d52dcd02c565f14235329527eb5258669892a8a9bb6e795` | `63846daa0d61eab62ea3633e15e8ec708abbe29da09f5c11855fa5c6d701b081` | `dccd76cfb747478d1ad2a4eb08d3305f36172d2880e289fb39b7de87dfdcb29e` | `129530f486259e63e1650fec3f6d9e23244547f6b265083ca394107f6fdebc45` |
| 0261 | `8d0093abef4ddda20bcdb615c8ca594a3ce246d679b284404009388433399d39` | `bb2725ae5e1b2406d199df12f5da1ceb5026a197e30714306dbe8fb6f291fbbb` | `869056d2a4ef89fc3de1f4d206dc8983caf9e79dc88cee261526648ecb4fa7cb` | `153e6f01cf8c5c72d8d3b207c90dbeb87acf16e6aa66253d4e9f2a7b7711b33c` | `2b0c8f3d7aef870357d76a0fa0e115f7691eb8ce3b17d0c74b4acd83f373eafc` |
| 0270 | `10539beacef8af4e46ba04e9797959bcd3fe5c8d5a92a22c4a8dd9d00271ee19` | `ab79fa4e045e022c27b28ab24fe2b882a113accccf7520803f550f03785aca74` | `0f0029d01571422784d146b562c70e38d909028223f202c823075b16e5a9c285` | `8d3964d1b547e28ce5ae183eb16bd511da3e437dbd908aad959cb7a6c5303e4c` | `fd0745deeaff8191499002392bba848514b652f7fd61d9705b59a3428ce06bb4` |
| 0281 | `376f2181dad2cce21ab5795a3ad545f0ee9168dbf05866461b9b796aa823c2f3` | `eabdc05e517362182a5a2d0fd9fe36a2a6e8ee3bf392b7ce527714df1c5599b7` | `61b09bd9494b92340be8f13698d97f97c0752dbb97721183f8821fe93e9d263d` | `6ce01f954c0266c29b649acd74241c5bbb36f55b203e2c8a7b8ea25eeb9b11c6` | `ddcfbce998e78f6e17bfc96ca081bbd3cfffe0503054dbd97a41b10f8a122d20` |

Candidate filenames are `exp-v1-recovery-r3-typescript-generation-<suffix>.candidate.json` in the scoped r3 directory. Future corrections must remain versioned/hash-bound; do not overwrite this evidence or silently change the reference to satisfy an unsupported oracle.

