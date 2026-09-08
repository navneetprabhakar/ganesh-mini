# Recovery r5 TypeScript bounded correction review — 2026-09-08

Scope: six derived generation candidates 0022/0140/0195/0261/0270/0281 in `datasets/cache/expansion-v1/versioned-recovery/r5/`. Complete corrected test files were read; each complete prompt/reference/mutant was reconciled with the fully read r3 content and confirmed byte-identical. Critic context and exact input/output bindings were inspected. No execution, generation, cloud access, central edits or admission. This is one bounded correction review, not authorization for a second automatic correction.

**Decision: five scoped static positives; 0195 remains HOLD for unsupported test oracles.** No original/r3 hold is cleared and no original-row coverage is credited. Main owns serial sandbox results and final admission gates.

## Per-ID dispositions

| Suffix | Disposition | Correction-specific evidence |
| --- | --- | --- |
| 0022 | Static positive | Explicit nullable guard fixes test narrowing; own __proto__ capture and constructor/toString values are now tested. |
| 0140 | Static positive | Unknown, malformed route and incomplete fallback each contain escapes and require a single unescape pass. |
| 0195 | HOLD | Hidden typed fields and A,B,A fixtures added, but mapper identity assertion rejects the unchanged valid copying reference; extra-field absence also overconstrains outputs. |
| 0261 | Static positive | A,B,A, remove last A twice, then set/toggle must notify A,B; frozen distinct snapshots retained. |
| 0270 | Static positive | A,B,A after immediate callbacks and terminal LF/CR/CRLF/U+2028/U+2029 rejection at zero/nonzero decimals; unsupported identifier exception subclasses removed. |
| 0281 | Static positive | A,B,A unsubscribe-last plus notification-start snapshot; per-listener isolation and blank-label exception subclass demands removed. |

### 0022 — path matcher

The test now uses explicit if-null throws before accessing matchOne/matchTwo and each special-key result, so the former non-narrowing-helper issue is removed without changing the nullable API. /:__proto__ must produce an own key with exact raw value; constructor/toString parameters are independently checked. These are valid nonempty parameter names. The original mutant loses __proto__ during ordinary assignment, while the unchanged reference defines own data properties safely. Tests do not mandate a params prototype. Root, specificity/declaration ties, fallback order, fresh output mutation, raw encoded values and invalid syntax remain covered. No static oracle mismatch found.

### 0140 — inline parser

Corrected tests put an escaped closing brace into unknown and incomplete markers and an escaped pipe into a route without an unescaped separator. Fallback must remain ordinary coalesced text while removing the escape once. The original mutant appends raw slices and therefore meaningfully differs; the unchanged reference unescapes each fallback. Tests also preserve recognized payload escapes, first unescaped route separator, escaped opener not reparsed as a marker, doubled/trailing backslash adjacency, non-nesting and call independence. No unsupported exception or normalization rule was introduced.

### 0195 — workshop toolbar: HOLD

The reference copies loader Workshop fields into a new object before calling the mapper, exactly as its r3 copyWorkshop helper did. The corrected test's mapper contains:

`assert(workshop === hiddenWorkshop, 'loader entries reach mapper without replacement')`

The specification says initialize loads workshops and maps them in source order. It does not promise the mapper receives the original object by identity; the approved scope expressly supports explicit required-field copying. The test therefore throws inside mapping even though required values are preserved. initialize catches that error, reports it and returns false, so the immediately following success assertion is statically predicted to fail before the intended row-copy and duplicate-subscription witnesses are reached. This is an oracle mismatch, not a reference defect or evidence of failed repair.

Additionally, `!('extra' in initializedRows[0])` and `!('extra' in filter)` require unspecified extras to be absent. The feedback's “do not clone unspecified extras” bounded what tests may demand; it did not turn absence of extras into a new API guarantee. Full deep-equality checks on the deliberately decorated mapped output have the same concern. Required fields, independent copies and protected internal state are the actual promises. The hidden-field/A,B,A inputs themselves are appropriate, but these unrelated assertions prevent a current-artifact positive.

Reference semantics remain statically supported: unique registration records, explicit copied Workshop/row/filter fields, isolated per-listener filter values, transactional mapper/load failure and dialog/reset behavior. Preserve this held artifact and report the blocker. Do not change the reference to pass the identity oracle or start another correction automatically.

### 0261 — panel store

A,B,A registration with the final unsubscribe invoked twice now distinguishes token identity from indexOf(callback): reference yields A,B; original mutant yields B,A. Fresh frozen per-listener snapshots, no immediate subscription, repeated same-value notification, toggle behavior, subscription changes affecting later notifications, explicit undefined initial rejection and commit-before-listener-exception remain tested. No new setter runtime domain is imposed. Static positive.

### 0270 — bigint vault

Terminal line-character strings are tested against both decimals 0 and decimals 3; the reference's complete-match-length guard rejects them, while the original dollar-anchor mutant permits at least the terminal newline cases. A,B,A removal after clearing required immediate callbacks independently distinguishes subscription identity. Nested subscription still receives its immediate current-balance callback, while current emission membership remains snapshotted.

Unsupported RangeError requirements for blank identifiers have been replaced by rejection checks. The explicitly stated parseAmount non-string TypeError and malformed-amount RangeError remain exact. Other validation checks do not add an unspecified subclass. Canonical parsing/formatting, duplicate-value silence, case-sensitive balances/allowances, mutation commitment and listener propagation remain coherent. No immediate-callback rollback policy is invented. Static positive.

### 0281 — release timeline

The first listener no longer mutates an event before the second is checked for an independent copy. Instead an event is mutated after delivery and internal-state detachment is verified: this is the actual requirement and permits the reference's shared detached event. A,B,A unsubscribe-last now provides the real ordering witness; A removes B during delivery but the captured B still runs. Original mutant runs B,A and fails the order expectation.

Blank append/rename labels require rejection without an invented subtype; explicit malformed/absent ID RangeError expectations remain. Ordered append/rename/promote/remove, output/snapshot detachment, bounded ID non-reuse, no event on absent removal and committed state on listener throw remain covered. Static positive.

## Seven original quality criteria

| Criterion | 0022 / 0140 / 0261 / 0270 / 0281 | 0195 |
| --- | --- | --- |
| Prompt clarity | Supported scoped APIs and boundary semantics; no new promises inferred. | Prompt remains supported; test-only loader identity and absence-of-extras requirements are not stated. |
| API consistency | Static positive; former narrowing and unsupported subtype/isolation issues removed. | HOLD: mapper identity assertion conflicts with permitted copied input. |
| Independent test origin | Supported independent specification/proposed-test/feedback correction, not fresh spec-only authorship. | Same provenance; independence does not cure incorrect oracle. |
| Non-triviality | Positive: ranked matching, escaping parser, frozen observable state, bigint vault, ordered timeline. | Positive whole-target async transactional toolbar; no padding. |
| Idiomatic code | Scoped positive, unchanged references with safe key insertion, fallback unescape and subscription tokens. | Scoped reference positive: explicit fields and token identities. |
| Dependency isolation | Static positive: TypeScript standard library/local manual tests, sandbox execution pending. | Same. |
| Realistic known-bad failure | Positive statically: direct contract-grounded witnesses now exist. | Realistic original mutant, but unrelated oracle failure prevents a valid reference-positive/mutant-negative decision. HOLD current artifact. |

Counts: 6 reviewed derived artifacts, 5 static positives, 1 held artifact (0195), 0 executions, 0 admissions, 0 new original-row coverage. Static positives remain subject to main's actual pinned compiler/reference/mutant checks.

## Exact bindings

All six r5 prompt/reference/mutant strings equal their corresponding r3 strings byte-for-byte. Each critic input object contains only id/problem/test_code, with the exact r3 prompt and test; corrected output equals the exact r5 test. The context prefix contains generic correction/runtime instructions and the suffix contains specification-derived feedback. Those instructions/feedback were read, and embedded artifact texts were reconciled with full reads. No reference or mutant code is in critic context.

R5 plan SHA-256: `778e0071bec56248081e741f4c742d522c75b4b006e069d8301b75440c2732ec`.
Critic evidence file `typescript-recovery-test-correction-evidence.json`: `df67e3ab3e631f5e148a9ebec16237bd3f798a6fbb3a2b8881adca9eb1c37919`.
Prompt/context: `1780e133d3aa4fae6efeab5bf587c34d9107b63b45b8d5e010e8db8a6b7780a6`.
Final output: `a9f8cc4472d06075047a20e6f90c550453baa249f9076c17b8928b2e5c6f7e1c`.
Stdout: `415e8ca268ae7e4159ec042072ed927cf319c42ce042c029500cca3c96776f9e`.
Stderr: `80569cc7ddfaf35bc0ce9fedbe1220e059a804de053c5e8179b9556760aeb36c`.

All content hashes reproduce evidence declarations. Author metadata: returncode 0, timeout false, no disallowed tool items, no event parse error. This metadata is not candidate-verification evidence.

| Suffix | Candidate file SHA-256 | Prompt SHA-256 | Reference SHA-256 | Corrected test SHA-256 | Mutant SHA-256 |
| --- | --- | --- | --- | --- | --- |
| 0022 | `98e3ff3905159c7cf23731d984d2ad049cd89c09846c7eed9a2b0b02ce827e07` | `ffeea915662c1262010a07df2d279d76fe3300d4826d3fdf37ccb56789eaad0a` | `e6265e1491e19f9d1b4dd76e4749f414385ba1772a39a6af0bc4a3d495c4f754` | `6a28979f6d9d53a10ed4895b4041971a23a6dffbcd4d8f1741104fa3ad9924e0` | `da2c1e73a3bf56d4d20f3c6d57a6c2a54a30e173b1239120655df0b82590e46d` |
| 0140 | `39289141aef9b435cd373d0fa6b2759dcd01d65582095fbdfb74e789ad2e534d` | `995abcda56cb7663e3ee1fb64b853cff7201b4802b06939abaaaafd5644b0c81` | `c0a088c1c91c95e015b7f1cf1d2f92e053a76fa290ceafd744fa0fdea203acd1` | `7da0e4af79ebfdc0ee71d64acf8561ea8c5809a2968b84a598b2939b4438ed73` | `b574373092cc0a3d7fe2d2b20d56d24df02fd3ffa04a1cc1e21701f6e871b2f1` |
| 0195 | `6386b8d68b718029b9c1efde0e22e779a3741cc7d6b672a76fa0a1e2e7af7b67` | `1c738d11e23d7fb56d52dcd02c565f14235329527eb5258669892a8a9bb6e795` | `63846daa0d61eab62ea3633e15e8ec708abbe29da09f5c11855fa5c6d701b081` | `b03e16208ae30090dae86130545ee7be849caf60e5bbdb8f50c05dc8b8a5b88b` | `129530f486259e63e1650fec3f6d9e23244547f6b265083ca394107f6fdebc45` |
| 0261 | `5028a8912e3745354cf1504a1b33f6e691b3f01503b0ee6d02c7976c6e708146` | `bb2725ae5e1b2406d199df12f5da1ceb5026a197e30714306dbe8fb6f291fbbb` | `869056d2a4ef89fc3de1f4d206dc8983caf9e79dc88cee261526648ecb4fa7cb` | `82cacda4bd05d592bd2e03ebe2676e90749b83f7c5f6274c80cbb8f27ae75a5e` | `2b0c8f3d7aef870357d76a0fa0e115f7691eb8ce3b17d0c74b4acd83f373eafc` |
| 0270 | `14d10f60949def2a4bbf1f220fe8589f467f5de7e0d3ba210c515cdf8e787914` | `ab79fa4e045e022c27b28ab24fe2b882a113accccf7520803f550f03785aca74` | `0f0029d01571422784d146b562c70e38d909028223f202c823075b16e5a9c285` | `1dc48fdd8e4d601b3b493b48b1fc49d00cf709ee7b697cabe15f8d5119c508fd` | `fd0745deeaff8191499002392bba848514b652f7fd61d9705b59a3428ce06bb4` |
| 0281 | `fd15fbbb79c23bab05b4859473d649e26046a9ebf60d425303c16b586e61da18` | `eabdc05e517362182a5a2d0fd9fe36a2a6e8ee3bf392b7ce527714df1c5599b7` | `61b09bd9494b92340be8f13698d97f97c0752dbb97721183f8821fe93e9d263d` | `b24412bc2da02b51be6b8b098a93ed02b3da5c9cd4245ac3c9291cd45bcb26af` | `ddcfbce998e78f6e17bfc96ca081bbd3cfffe0503054dbd97a41b10f8a122d20` |

Candidate basenames: `exp-v1-recovery-r5-typescript-generation-<suffix>.candidate.json`, under the scoped r5 directory. Preserve hash-bound artifacts and evidence; no silent edits, original hold clearance or automatic second correction follows from this report.

