# Recovery r5 JavaScript bounded correction review — 2026-09-08

Scope: five derived candidates 0137/0212/0219/0221/0339 in `datasets/cache/expansion-v1/versioned-recovery/r5/`. Full prompts, references, corrected tests and supplied mutants were read. This is one bounded correction review; no automatic repeat critic, execution, generation, cloud access, central edit or admission. No original-row coverage credit.

**Decision: five scoped static quality-positive artifacts, suitable for main's sandbox verification.** All five now contain a meaningful witness against their unchanged supplied mutant. No newly unsupported oracle or static reference mismatch was identified within the approved scope. This does not claim executed success or clear original/r3 holds.

## Individual dispositions

| Suffix | Disposition | Actual defect witness |
| --- | --- | --- |
| 0137 | Static positive | Frozen external ticket with hidden title/details and root with hidden nextId; toggle must retain each required value. Original spread mutant loses them. |
| 0212 | Static positive | Sparse own hole with local Array-derived prototype index 0:7; mapper and fallback must both receive undefined. Raw-index mutant passes 7. |
| 0219 | Static positive | Spaces-only nonempty failure message is retained exactly with fresh values/saved objects. Mutant trim-empty rejection throws. |
| 0221 | Static positive | Spaces-only POST text produces status 201 with exact stored text. Mutant returns 400. |
| 0339 | Static positive | Both omitted and explicit undefined on/off handlers reject with TypeError. Mutant wrongly accepts them. |

### 0137 — immutable ticket transitions

The reference explicitly copies required changed-ticket fields and root nextId/tickets. Corrected tests supply non-enumerable title/details and nextId, frozen to expose mutation, and verify retained values on toggle. This is a valid directly readable required-field input, not descriptor cloning or arbitrary-extra preservation. Hidden add payload values, identity of unchanged tickets, trimmed new title, original status, counter progression, deletion and non-reuse in bounded sequences are also checked. Recognized malformed payloads retain their explicit TypeError rule; generic malformed/unknown action identity behavior is preserved.

Coverage qualification: delete is applied to the newly added state, whose counter is already enumerable, rather than directly to the hidden-root fixture. That is not an independently distinguishing hidden-root-delete witness. The toggle witness already rejects the supplied mutant and the reference's delete branch explicitly materializes nextId, so this is a nonblocking coverage limitation rather than grounds for another automatic cycle.

### 0212 — sparse-safe mapping with error/fallback identity

The fixture creates a local prototype inheriting Array.prototype, places index 0:7 there and attaches it only to one sparse array. No global prototype mutation occurs. The corrected test checks mapper values, fallback values, error records, dense output ordering and unchanged own-hole status. The reference's own-property test correctly supplies undefined for the inherited numeric position; the mutant cannot satisfy those assertions.

Normal mapping, empty arrays, malformed arguments, direct fallback identity, callback result identity, thrown-error identity and fallback exception propagation remain covered. No callback-driven length mutation policy or cloning promise was invented.

### 0219 — profile editor

The spaces-only failure message witness follows the raw nonempty rule and preserves exact contents. Save-start remains separately trim-based and rejects a whitespace name with the required Name required error. The reference differs from its mutant only in the relevant failure-message emptiness predicate; the witness therefore rejects the actual defect. Fresh state/values/saved identities, separate saved/live copies, loading/editing/saving, empty/non-string failure rejection and prior-state/action nonmutation are retained. No optional extra-field preservation requirement was introduced.

### 0221 — task dispatcher

The corrected suite explicitly creates whitespace text and checks status 201/id/exact content. Empty/non-string bodies remain invalid and failed creation does not consume an ID. PUT uses a space-padded nonblank value and checks exact retention; missing PUT is tested before body validation, following the supplied specification-derived feedback and approved ordering. Snapshot mutation, instance separation, GET/list ordering, deletion and exact unsupported paths/methods remain tested.

Coverage qualification: the PUT fixture is '  updated  ', not spaces-only. It therefore does not independently reject the PUT trim-empty branch. The reference's POST and PUT both visibly use length===0, and the whitespace POST rejects the supplied combined original mutant, so this is not a new hold. Do not claim both branches have independent spaces-only test coverage.

### 0339 — snapshot signal hub

The corrected suite covers explicit undefined and omitted handlers for both on and off, as the function-handler requirement demands. The reference splits topic validation from mandatory handler validation; publish still permits arbitrary payloads, including undefined, null, zero, empty string and symbol. The mutation is meaningfully distinguished at the first undefined-handler assertion.

Same-function registration remains idempotent Set-like behavior, unlike the separate-registration TypeScript tasks. The test preserves ordered callbacks, off Boolean/idempotent unsubscribe behavior, snapshot membership changes, exact payload identity, exceptions stopping delivery and independent hub instances. It does not impose a duplicate-subscription contract from another task.

## Seven-criterion accounting

| Criterion | Assessment for these five artifacts |
| --- | --- |
| Prompt clarity | Positive within approved bounded semantics: required fields, sparse-as-undefined, nonempty message/text and required on/off handlers are explicit; missing-PUT ordering follows recorded feedback. |
| API consistency | Positive statically: CommonJS APIs, return shapes, identities and specified error behavior align. |
| Independent test origin | Positive as an independent specification/proposed-test/feedback correction, not fresh specification-only test generation. No reference or mutant is present in critic context. |
| Non-triviality | Positive: immutable ticket lifecycle, ordered mapping/fallback propagation, saved/live editor transitions, detached stateful CRUD, and snapshot event hub; no new padding. |
| Idiomatic code | Positive scoped static assessment: explicit record materialization, own-index membership, narrow predicates and separate validation helpers. |
| Dependency isolation | Static positive: source and tests use standard JavaScript/Node facilities; no external dependency or candidate execution here. |
| Realistic known-bad failure | Positive statically: each test has an actual contract-grounded witness against its supplied unchanged mutant, as detailed above. Main must verify rejection in the sandbox. |

Counts: 5 scoped static positives, 0 new holds, 0 executed results, 0 admissions, 0 original-row coverage credit. Two nonblocking per-branch coverage qualifications are stated rather than concealed.

## Exact immutable bindings

All five r5 specifications, references and mutants were compared byte-for-byte with their exact r3 counterparts and are unchanged. Each critic input object has only id/problem/test_code; problem and proposed test equal the exact r3 artifacts. The context prefix contains only correction/runtime instructions, and the suffix contains specification-derived feedback for these five IDs. Those complete instructions/feedback were read; the embedded specifications/tests were matched to the inspected artifacts. No reference or mutant code is included. Every corrected output test equals the r5 candidate test exactly.

Evidence `javascript-recovery-test-correction-evidence.json` SHA-256: `e592e8c2eed106b0c5df385c227d061326eb37af196d7a33a12383f0ad5df3ea`.
Prompt/context SHA-256: `c80b4a1afbc8b2d33a124b9e42034afabf1d1b2c68e6ad881858cda1d20a7967`.
Final output SHA-256: `4eca7f13f1190d6cdb4840f60a6338b2014cb8e10ca9b54485f89012462c735e`.
Stdout SHA-256: `8a322db34a565c25eb60152fcc4b16ad29c0a8bd275bd0537412d84df46e78f6`.
Stderr SHA-256: `be8b4b83c29bcf1a56c4317d674bdfb4f01ff46afb24e21824854fbc0d1aad72`.
R5 plan file SHA-256: `778e0071bec56248081e741f4c742d522c75b4b006e069d8301b75440c2732ec`.

All evidence content hashes reproduce their declarations. Critic metadata reports returncode 0, timeout false, no disallowed tool items and no event parse error; these are author-run metadata, not verifier results.

| Suffix | Candidate file SHA-256 | Prompt SHA-256 | Reference SHA-256 | Corrected test SHA-256 | Mutant SHA-256 |
| --- | --- | --- | --- | --- | --- |
| 0137 | `b8359cd2337778198fec5ec182dd6f8c6f89067920e2c6e48bcb8264331465af` | `f041504729bb73eaa79af937ddee020e89266b05950a5909837839b4e001db60` | `1b05724868fd1c2a4326d03e5184e8110fdc30cd3ba15bded5edc79617ba6f60` | `6637041138e40dd076aa69ff218d0a2d1166bc453f8a7880eb854a68de1b530b` | `f4eba6c9d50fd76089ab76264b58a7bdbd32c4535cdf0915f73eef4966cc1655` |
| 0212 | `5ee4ca1f86e7f59307ca1f2249c09fc1a60b892cf569130b7b5dc69c4b30c94e` | `35ebf5e8e9698de6175b3f0e255ed14d8d2afd086e9e49357e302bf90582365f` | `611fd4f0a58ff3533adf3a16aeb822af78e56ae1753d05e5000cffbcc7628fce` | `e644acce3516a4ad69e0128656aea8f25771ff7374a3dcac93fce7a42d12cecf` | `dace07f9dff26051e4db69318f49fa977335111327c8ea9b6d39b22ee817f1dc` |
| 0219 | `415b87990b7793a76006683f6c0913b012f7a27fc24bac066638ae20414d94d8` | `a0989fe15a1af98a87b686b021f9161b338538217256d282313f420420ba177a` | `30e5bdd818886794edb13f8b2e791d91f53f3115411565f3ac04a428be2a2f4f` | `c1dcad2c1f2c3cf79e74d124697aeff26f88b3bcf926066f29d715aff38abfce` | `3417efe51fa95651527c951a71206b0ecd7f3360119d8e66e9b3800354d73764` |
| 0221 | `3cf8a06f7e04f10e54dee2544b7294de8103fd9b665bdf9a8d195808fed488cb` | `60cfbd15684d4ae8871820bfcbade6fdc4d98029cb1f395dbad1eeeab3edbe5b` | `ca6508731c48a4fb930e9aa145146f6f89828742142b8f74ccd1f8ba68df2cad` | `cc8ef20a52ccebc0d5fd7f6084e043505043705069c8a23f08db2b6365c671e1` | `c9cf39b09df69acbe9fa3f98422c1d39dd86e72d01bd53b9646a023872eb6d97` |
| 0339 | `814f4363506bf7e077710e8fcde0ecf6621a4019cb00839ba30a8307fcbd5eb3` | `adb3c1cdb40f24974a4c34c5df5b74945e8a400ee3bf362940988bea88c3c3bb` | `41bad082081e05b36104cb52062c59b46b9ee5f4bfc73a0ad1f6c7b600e91ba9` | `165d8d9e99dce6fc7a5b8f737b8f7c5989f1bf54da06f2a7b935d7e3805419c4` | `e01eb7245e37e7afcdf930b3f871b6ebd2f8deec17ea9ed7355e15131569a7c7` |

Candidate filenames are `exp-v1-recovery-r5-javascript-generation-<suffix>.candidate.json` under the scoped r5 directory. Main owns resource-limited network-disabled sandbox verification, admission/separation decisions and all central bookkeeping. This review does not modify any candidate or authorize an unbounded correction loop.

