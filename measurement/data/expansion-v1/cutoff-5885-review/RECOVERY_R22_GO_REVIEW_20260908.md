# R22 Go independent quality review — 2026-09-08

Scope: exactly eight R22 Go derived candidates. Complete original/derived specifications, references, independent tests and known-bad sources were read; approved request and prompt differences reconciled. Static review only: no candidate execution, generation, admission, ledger edits or new original coverage. Main-owned existing serial diagnostics are distinguished below from this review.

## Disposition

Two quality positives: generation0218 and repair0180. Five test-only holds: generation0027/0095/0121/0280 and repair0048. One scope hold: repair0233. All eight references are semantically positive under their stated contracts; that does not clear defective tests or unauthorized specification changes. Go0095 actual race qualification remains separate and main-owned.

Seven criteria: prompt clarity (C), API consistency (A), independent test origin (I), substantive nontriviality (N), idiomatic implementation (G), dependency isolation (D), realistic known-bad failure (K). Origin independence is not oracle correctness. All eight have I/G/D positives and plausible semantic mutants; K execution evidence must be valid, not merely a compiler failure. Entire-target interactions, not patch length, govern N.

| Candidate suffix | C / A | N basis | K and oracle disposition | Decision |
| --- | --- | --- | --- | --- |
| generation0027 | Positive | Ordered bracket selection, whole-input validation and finite arithmetic interact | Direct endpoint difference is realistic but survives current tests; missing defining witness | Test hold |
| repair0048 | Positive | Copy-sort adjacency, full-width comparison and lexical ties | Signed-width mutant has decisive boundary case; empty snapshot falsely fails reference | Test hold |
| generation0095 | Positive | Timestamp domain, sequence lifecycle, atomic errors and concurrent allocation | Huge delta witness rejects mutant; unsupported error-value assertions and incomplete atomicity control | Test hold; race separate |
| generation0121 | Positive | Tuple identity, replacement/URI ambiguity, ordered pages and detached snapshots | Structural collision mutant realistic, but test syntax prevents any semantic proof and both correction witnesses absent | Test hold |
| generation0218 | Positive under approved clarification | Interacting publish/removal/suspend transitions and map boundaries | Repeated request rejects realistic non-idempotent mutant; tests valid | Positive |
| repair0180 | Positive | Exact full-width rational floor, saturation and invalid live size | Remainder overflow mutant rejected by independent full-width oracle | Positive |
| generation0280 | Positive | JSON shape/EOF, wrapped errors and native field semantics plus exact membership | Null witness valid; approved empty-level success boundary omitted | Test hold, narrow completeness only |
| repair0233 | Clear API but unauthorized method restriction | Full-width extrema/differences, stable order and detached normalization | Adjacent large values decisively reject float-before-difference mutant; current tests otherwise positive | Scope hold, not test-only |

## Concrete findings and bounded specification-only feedback

### generation0027

Reference performs complete validation before exact returns and uses a convex weighted sum for opposite signs, avoiding overflowing endpoint subtraction; same-sign differences remain bounded. Ordinary fractional, boundary and invalid-later-observation cases are valid. Add the approved two-observation midpoint between negative MaxFloat64 and positive MaxFloat64, then reverse signs: both results must be finite zero. Include a same-sign large finite control and retain ordinary fractional interpolation with appropriate tolerance, not arbitrary bitwise fractional equality. Current ordinary tests let both mutant and original reference pass; reference-pass alone cannot close recovery.

### repair0048

Unsigned ordered differences correctly cover MinInt through MaxInt; strict smaller replacement preserves lexical ties and copying preserves input. The empty nonnil table input is snapshotted with append to a nil slice; this produces nil, then reflect.DeepEqual reports false against untouched empty nonnil input. This is a test defect, not mutation. Preserve nilness in snapshots or compare values with a separate pre-call nilness record. Retain the existing decisive [MinInt, MaxInt-1, MaxInt] closest-last-pair case, duplicates, ties and short-input tuple. Add the approved tiny [MinInt,0,1] and two-endpoint controls if rebuilding. No reference change needed.

### generation0095

Unsigned timestamp difference after pre-epoch rejection correctly covers all int64 inputs; started flag avoids sentinel collision and lock protects validation/state commit. Current error branches demand returned ID zero, although the contract promises only an error and unchanged generator state. Remove zero-ID-on-error demands, including nil receiver, regression, bound and exhaustion paths. Retain successful ID layout assertions and the existing MinInt64 epoch/MaxInt64 invalid-delta witness. After that failure, call at the epoch and require sequence zero; also test a huge rejected timestamp after one valid call, then the same valid timestamp must advance by exactly one. Existing ordinary failure controls do not replace this numeric-boundary atomicity witness. The bounded 512 same-millisecond goroutines, buffered collection and join check a unique contiguous set without assuming scheduling. Actual race-detector qualification remains required separately; this report does not claim it.

### generation0121

Reference uses structural tuple keys and caps limit by remaining entries before offset addition; both fixes are sound. Tests omit a closing brace for the artifact insertion loop before the expected ordered list declaration in TestCatalogListOrderingPaginationAndIsolation. The later function declaration therefore triggers a parser error. Fix test syntax, not implementation.

Add distinct tuples (a+NUL+b,c,d) and (a,b,c+NUL+d), distinct payloads, independent lookup/list/replacement/deletion checks. Add two ordinary sorted entries and List(1,MaxInt), expecting only the second. Existing List(MaxInt,MaxInt) exits before addition and is not that witness. Remove zero Artifact assertions on invalid, ambiguous and nil Get error returns: only the error is promised. Preserve specified nonnil empty pages, exact raw strings, error identities, URI ambiguity and snapshot isolation. Current compile failures for all three implementations are not mutant rejection.

### generation0218

The only behavioral prompt delta is the approved successful idempotent RequestRemoval from removal-pending and explicit rejection from removed. Other API/state/scope/reviewer rules remain unchanged. Tests exercise reachable queued/publishing/ready/failed/suspended states, two requests followed by finish, and rejection after removed; publishing outcomes, ready-only suspension, reviewer validation and detached map mutation are covered. No blanket nil/zero catalog or error-map representation contract is inferred. Reference retains raw nonblank IDs and independent maps. The realistic mutant rejects the second removal request; archived behavior failures correspond to this boundary. Quality positive, not admission.

### repair0180

Only embedded broken source and an accurate stale diagnosis changed. Quotient saturation bounds the whole-percent component; wide remainder multiplication/division yields the exact fractional floor. Div64 divisor precondition is safe because remainder is less than live and high product word is less than live. Tests include live 2^63, target MaxUint64 yielding 99 and independent big.Int arithmetic, ordinary fractional floors, saturation and zero-live behavior. No arbitrary smaller domain or unsupported exception detail is imposed. Realistic mutant restores remainder multiplication overflow while retaining original divide-order correction. Quality positive.

### generation0280

Reference rejects top-level null before semantic validation, checks EOF and preserves native encoding/json duplicate/field matching semantics. Current null/error-class/zero-Badge assertions are explicitly supported; ordinary duplicate last-value, exact case/space-sensitive levels and nonmutation controls are valid. No exact-case-only JSON key or duplicate prohibition was introduced.

Narrow completeness hold: approved request expressly requires successful allowed empty level; current tests only reject missing level when allowed list is nonempty and lacks empty. Add a nonblank label with omitted/empty level and allowedLevels containing empty, expecting success and empty Level. Retain null malformed classification (also whitespace-surrounded null), native duplicate behavior and trailing-value rejection. This is not a finding that the reference fails empty membership; it handles it correctly. Existing executed directionality already isolates null, so do not mislabel the hold as missing null rejection.

### repair0233

Reference unsigned differences fix adjacent large integer collapse and signed-range subtraction; existing adjacent MaxInt and full-range tests provide real witnesses with finite endpoints/middle. Exact embedding passes. However, outside the source block and diagnosis the final behavioral paragraph was changed from correctness with negative values to correctness across full int range plus the imperative “compute integer differences without signed overflow before converting them to float64.” The approved oracle-rebuild request explicitly preserves all original behavioral prose, permitting only source replacement and neutralizing stale diagnosis. Full int-domain correctness was already implicit; mandating operation order is a new implementation restriction. This cannot be cleared by test-only feedback or silently deleting candidate text. Main must decide a separately approved architecture/scope disposition preserving the raw artifact. The semantically correct reference and passing diagnostics do not override that boundary.

## Provenance and integrity

Canonical hashes use UTF-8 JSON with sorted keys, compact separators and ensure_ascii=False. File hashes bind raw bytes. Parent identities match approved request bindings. Source dataset/revision/record/license fields and all rights flags match immutable parents; transformation appends derived lineage. Generations retain McEval CC-BY-SA-4.0; repairs retain MdEval MIT. This records existing rights declarations, not new legal clearance.

Architect final items exactly match derived problem/reference/mutant; independent-author final test_code exactly matches candidate test. Decoded Tasks array contains exactly ID/problem pairs matching all eight derived specifications; no separate reference or mutant context is supplied. For repairs the public specification necessarily includes its embedded broken source: independence means no hidden solution/source-test access, not invisibility of the task's own code. Both archived authors returned zero, did not time out, and have empty disallowed tool-item lists. Prompt/final-output hashes were recomputed. Generation specifications except0218 are byte-identical to parents; repair0048/0180 changes stay within source/diagnosis scope; repair0233 exception is recorded above.

- datasets/cache/expansion-v1/versioned-recovery/r22/plan.json: `34b141407c111f6df7999027d57540860ccb3b47c0d10c2c5ce8ba105f8facc0`
- datasets/cache/expansion-v1/versioned-recovery/r22/run-contract.json: `a0b4a39242bee4710967f7d01a0d6031bf4a81401f3aca98bcab09c80b80c6a8`
- datasets/cache/expansion-v1/versioned-recovery/r22/go-recovery-architect-evidence.json: `20dd71aa7c61e7695519d940365ca64f5b6503397b3bff80c21a8f3c99eb72a9`
- datasets/cache/expansion-v1/versioned-recovery/r22/go-recovery-independent-tests-evidence.json: `7664e87a11e2bc272993650fb7de3f316ec6fc9cacfc63283e4cf7a436b99b1c`
- measurement/data/expansion-v1/cutoff-5885-review/recovery-requests-r22.json: `f2d66783fc2c5877a4016585c40f0b279a4991c809d59d1757eda35c6238eb00`
- measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R21_JAVA_FAILURE_20260908.md: `493ab0a73263481e6e54adacffcd1674e8b542a1fdaf0236900a0f14d268926d`
- artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-go/summary.json: `068922b02276555f07466c8a6f3a1a5b3b186a28bad213111ccd301f25063ec0`

recovery-architect: prompt `ce89140555f5bb006d73d06334d1ba3631c1d910ee8ef34725f903b29ebdfc1c`; final output `d6e8d73ef2faf6bf2754843f07855b9b5a5093e4e9ffff40a52e7acc881c5d43`.

recovery-independent-tests: prompt `65e5002a30a22297ef2bcfb45a7170a3a2129a6ed4b4a0c0668702eb8e354233`; final output `c775d43374c7b7fe27e16b9b53ef3ba431b89b3bd56521ac4a1048d8fcacd64f`.

## Exact candidate bindings

Candidate files are datasets/cache/expansion-v1/versioned-recovery/r22/<ID>.candidate.json. Answer and reference byte hashes are identical in all eight. Common rights canonical hash: `8ee7b37991bb05fd4a2eec731bb4f25b0468d6d9c69ddda1dcc5089ddd7aea5b`.

### exp-v1-recovery-r22-go-generation-0027

- File: `1b5fb95aab0c1ae542aeb210fd889e86d2cf98856bfc75edc56863be9945c328`
- Candidate canonical: `27a36ed533cde529cb237a3d69ff6ea2b82a32adc4ae916e5525a6bef8ecc71b`
- Original parent canonical: `3fca5e99057f8713a19a8bbe37827effe22c5ff22c04366cf98a656cb31dc0ac`
- Source object: `f1ad26cf199cb75fc52c891462eb170bce4c25baeea8d8c58564cdd92ab62965`; source record: `1a9ed05364034dc652c7173ba9e7edc1cae10da0379ad88a4e890126c67ecea2`; license CC-BY-SA-4.0.
- Problem: `96baab03bcc8a98fb487b72346b5bd9403d39830360085dedf711aa2273691d6`
- Answer/reference: `59b7f20084a8d64cdd6a70850f0236a55c2531b4d567bd17077bd96ca2f096ef`
- Independent test: `d6efdbb634e817b6065d8d4eaab58755def1cf38e822c07346504daebe9c1a9d`
- Mutant: `28f492a8bab7648a3127dfa2c529b0e0a999b815ddc1ea6bd75d282eecba0af0`

### exp-v1-recovery-r22-go-generation-0095

- File: `905cf0e637f5ce8863da77d66f82d688140e5f69c97d830eb5f43e5179279304`
- Candidate canonical: `8141fd6ea9724680b2a78ae661cf9dbbb9427c3098214b0dffeaeb7af8da62ef`
- Original parent canonical: `179863828385f6d0259eb99b885c38820d13b3d8c6844f45620e3dc9cb03e573`
- Source object: `643fd2f4a1dac404509354406bdf8e16b750d4c77716b3d6e67b57b0d5437b55`; source record: `f5aa52ee5881c9450065352f784eac6d229abb418c6c0376d1071e089df5bdf2`; license CC-BY-SA-4.0.
- Problem: `2f7bf5287781a5534abc28810d82ad1a362684773c16c930bdd183720612fcce`
- Answer/reference: `6a76e339ed6ee0d8b43490dc76f5dc9680712d8303d12cf8e824896bf7bb0890`
- Independent test: `eab1123bc0b84cb037bb77425b84082810233695061e310464c530c9cec2a538`
- Mutant: `2a90c42f289d23776b99bc269be123dbc93c957f0707c06f92e6ae06b8a4f55e`

### exp-v1-recovery-r22-go-generation-0121

- File: `fa31f524f2ac1b6e3d7e0e3bb713d528ca59aaf4c75055b61003b26514635d1f`
- Candidate canonical: `1d7289ad0be49cc3cd1710b98c53bd06e3f8abaacf9ee9400e0f449c04e65e77`
- Original parent canonical: `748e3d3563c5167ffd6fcbec801b9191aa48a4b28d852a5dcd78b1c5ff6e721d`
- Source object: `1c9c2997c3e81a32c87ba37c14514c1a69d388243f55dc15989dece774557ffe`; source record: `7c070187bd90893cde5d662efe2f622ce5aff653ff3ebd40a2f4267fbacc8a6f`; license CC-BY-SA-4.0.
- Problem: `e289568f43c8807df18d1cb48eff6990c09fc769933c5aa58d1b4ee8b80fdd42`
- Answer/reference: `e955b4a7ba6db8c673450b2de9e8109b0da47d8e57b8797853a9c093e022329e`
- Independent test: `e8e645cf98e8e72347ce899f6e3ba14ce30aebdd13ddb047bbd7d6255c4f3b0b`
- Mutant: `66151e69f9dd8f9c12913c822bf3d52d59bcc9b40207ea945f710ab020a0d455`

### exp-v1-recovery-r22-go-generation-0218

- File: `f1eb8519d29e4f55a66aa1f39055b801a9b117eccc0667fee635106f5346ffee`
- Candidate canonical: `1005a6bb8285050407bad138a2e173bb3feb836bae8450df7055c84b148731b3`
- Original parent canonical: `9e86e83b0e915ce72b597e18fa741ba566dc55109e2b1b951245c55ca4dfcfc7`
- Source object: `223eb3087b80f54b09ac0b14bb306667ed094c86efe20f7c072f32466dc39c63`; source record: `2bdf1e2757b3bb800b3caf52479e9585f8993d1fb6810215b1ee9c574b6ec4fb`; license CC-BY-SA-4.0.
- Problem: `02c9939ae5db93b0d450d0258533fceeda8154c2835a4a574989e10467e8b57e`
- Answer/reference: `dca3b9a2c8c43f1966ef2323cf3df213df8c2f898e40cb891a11edd40a4b69ca`
- Independent test: `2b8ac6dce776695d34363dfcdbd0576f7944b97644487d55f6d147a572a8305c`
- Mutant: `9bf53b08de206935c55faf56b824f67c0575a713e35391d32227be5392e35203`

### exp-v1-recovery-r22-go-generation-0280

- File: `d24a986c993b130ad6b52ffe23d21ffa5d8c93d080e5ff44220bf03bc43d3723`
- Candidate canonical: `b6aea48c41adee79814c1d715fb4b4099eb7f2dca606b490b8596dc22ed225b1`
- Original parent canonical: `a3e286b919262fbae3b53571ec92273fb0df3a94d347c153277c09f0fff9d39a`
- Source object: `4b9739409fc3bf332e823573cefa307ef8bdc61f7211e3c07fe672e00a2fe918`; source record: `bcab7a773879d76851c2be5e4d8092c6a9a4b84a70f04f92246616faf3d3bec7`; license CC-BY-SA-4.0.
- Problem: `4c13666bb4ca43e61f0ee911475426a911b30eb600029165d0467852bae067c0`
- Answer/reference: `a10e6a7c12a90ecdd98b3bff5cf73df9bbe267618c80ec51a5250e50746989a4`
- Independent test: `624237a4e2365b18ff0c23dba4310c3df999467b74269b30973f4d97576d8736`
- Mutant: `daf0854bbc80ad5e57ba9be7155e2617cf1dc63eca2c87d96f36c5135d681297`

### exp-v1-recovery-r22-go-repair-0048

- File: `f8523d65684a0452ab6ae5189e9d46702b5ea19ad26505dd5b26a0134d500b3d`
- Candidate canonical: `d99aad83180bf37c2a6b249a7997a338ed254f36c35b5e74af4ddf545b480d2d`
- Original parent canonical: `750c4daa922b861fd2013145a76364da01755ac8c61c1fa092e4c0cb950392b5`
- Source object: `a16b0ca45c52bf4d34e23f4b4f478c4eb9d432588db674d8cf372cb8c7d30e5b`; source record: `a359818cd6f9e35da3cb1d15ca4da60ed09578855a0c542c8606bb39c11ff9cd`; license MIT.
- Problem: `3fc99b936d59009025d1ba8c5947c7260258b361c220aaa3aae0376b0ef144a1`
- Answer/reference: `384727b7c8fa361983f81700ab8a4388c014e59399a750843c8cd796de6eedd8`
- Independent test: `48cae138674ac44fa7bc40bc887a6d09dfff22ba90f5dbc69ee33b10d999b661`
- Mutant: `3ce1f3020a7f2827e65ce864fbd79c0226aeae322db0012c769af26785e9d364`

### exp-v1-recovery-r22-go-repair-0180

- File: `ea46187e558eb6949a858b8a0dcc8c84220ad228b132598e4b89b8715b2064f6`
- Candidate canonical: `b946cde07ef530ab81bff2faeb478b825e0e42c2fccf2c153db8e2eba66df1de`
- Original parent canonical: `7b5faf2fe549940745ff9bab52fa3bc710b837ce12d956656ff511a5648e6112`
- Source object: `318364e73181a2cfc741b68c5c071ba00d5812a161d258179fca18e6a368c079`; source record: `ade965862f69231d186a52f7fe4929c39946818a77eee9b7e5718f779440ac86`; license MIT.
- Problem: `442e7e1fbd8c6adf67e3b427cf11ba4a3ea98a0fb7a99a082775875846aae318`
- Answer/reference: `55806f1ffe7965d8420f7803835db1a8f36117d59fdd760e7c7cad38fcc9237a`
- Independent test: `3eb0f38733cc2fbf8b5d660ce2b0ad211733e64a7f26a4416fea0458c5a7c6f6`
- Mutant: `cf4fdbd2ea95fa927b5ae62d5b8ee7dc444ea509017e15c925f94fe67bb8cf69`

### exp-v1-recovery-r22-go-repair-0233

- File: `2938b5a890c56bdf468081e2e5ce38d21161885b9c9d87daed9e3e5a33dbab05`
- Candidate canonical: `ec36618cf021d0fff4edee09f10f53500453e99fa78963794fbf9ea89460d894`
- Original parent canonical: `353fc94add0a23ae2f54cdee93f18fc3d68ca42b298cbb0e7239d595237cdf6f`
- Source object: `e13840d7a0b3f9dc72276704f599d0e3c9d454a20ae4f0b9114d7e1dce405cc7`; source record: `b676eda5236fc21bceb7add437cb7f764b8a901279e1ef35caf5c6897b1fe096`; license MIT.
- Problem: `18fbd66d6df4b45037b4d64b2514b8af59fdce7e176692db0e4c4aa4cb8bba34`
- Answer/reference: `887a9c52bf17efc16224c6cb2f7e9709ebbeaf6ce46d65323634d1a391027df8`
- Independent test: `ccc7851c739537812ddd766d2807a6437592e8f44cd88dd1c11c0d6fd8012c1a`
- Mutant: `835f04dc3397ef829b5fa314e161e72086f2750be222f29ec5c15efe0ea0ac91`

## Existing diagnostic interpretation

Main-owned r22-go summary at the hash above contains all eight records. Reference/mutant/original outcomes:0027 pass/pass/pass;0095 pass/behavioral-fail/behavioral-fail;0121 compile-fail/compile-fail/compile-fail;0218 pass/behavioral-fail/behavioral-fail;0280 pass/behavioral-fail/behavioral-fail;0048 behavioral-fail/behavioral-fail/behavioral-fail;0180 pass/behavioral-fail/behavioral-fail;0233 pass/behavioral-fail/behavioral-fail. For0048 reference stdout identifies untouched empty input as mutated; for0121 stderr identifies solution_test.go:165 expected '(' at the next function. These support test defects, not reference failures. The summary's exact per-label evidence hashes remain the diagnostic binding; no new run is claimed.

No approval, reservation, correction loop, candidate mutation or admission performed. Main owns final integration, independently authorized corrections and Go0095 race evidence.

