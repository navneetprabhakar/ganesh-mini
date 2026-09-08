# R26 JavaScript and TypeScript independent static quality review — 2026-09-09

Gate 2; static review only. I reviewed exactly the two JavaScript and three TypeScript R26 test-correction candidates against the frozen R26 request, feedback, plan and run contract; their exact R24 predecessors; the R24 independent reviews and bound defect evidence; the complete prompts, references, known-bad implementations and corrected tests; the independent correction-author archives; and the private evaluation task corpus. I did not execute candidate or generated test code, mutate a candidate, admit data, create a plan, or use cloud resources.

## Decision

**Five unconditional static quality positives; zero holds.** The R24 defects are corrected within the authorized test-only scope. This is a review decision, not an admission, verification receipt, quality seal, or permission to count the records in training.

| Candidate | R24 defect | R26 correction | Decision |
| --- | --- | --- | --- |
| `exp-v1-recovery-r26-javascript-generation-0120` | Unsupported extra-field rejection made the oracle stricter than the prompt | Removes only that assertion; retains sparse candidate, candidate-skills and required-skills witnesses | Positive |
| `exp-v1-recovery-r26-javascript-generation-0292` | No witness for exact primitive command typing | Adds boxed `String` and coercible-object rejection | Positive |
| `exp-v1-recovery-r26-typescript-generation-0294` | Sparse tags and per-registration duplicate removal were not distinguished | Adds sparse constructor/replacement tags and an `A,B,A` unsubscribe-last-`A` witness | Positive |
| `exp-v1-recovery-r26-typescript-generation-0366` | Duplicate callback outputs did not identify which registration was removed | Adds distinguishable `A,B,A` witnesses in both `create` and `transfer` buckets | Positive |
| `exp-v1-recovery-r26-typescript-generation-0368` | Missing early-year witness and a mutable/readonly helper mismatch | Uses `readonly string[]`; adds valid years 0099/0096 and Gregorian 1900/2000 controls | Positive |

## Immutable binding and correction scope

For every record, a recursive R24/R26 comparison found differences only at `/id`, `/source/transformation`, `/verification_task/task_id`, and the corrected test file's `/content` and `/sha256`. The complete user prompt, assistant message, verification prompt, rendered prompt, reference source, complete known-bad object, rights, runtime/limits, and all source fields other than the explicit R26 transformation are byte-identical to R24. Each R26 prompt equals its rendered prompt and user message; each assistant message equals its validation reference. Declared prompt/reference/test/mutant hashes recompute from the actual UTF-8 content.

The approved feedback binds the exact canonical R24 candidates: JavaScript 0120 `1a11364fe49009462761f69820a97111a5380354cad9b3868bedfb0670ccafe1`, JavaScript 0292 `3d02098306ea9ce9854d70862e2cccebd989ee92ba44962ba57ee2009f194139`, TypeScript 0294 `c9e8d748162d0dead05c139804106126ff84f31fe4790fac367c35da13cc97f3`, TypeScript 0366 `6591a155453e236af96711c0bb08c45db3621d395dd1ad16453cfd7aee6b4c83`, and TypeScript 0368 `eb740f69cec46cb470f23f3bfefc922d8bc3657528549768b1785e6bcba4a867`. These equal independently recomputed canonical hashes of the exact R24 files. The run contract records `correction_attempt: 1`, `status: test-correction-not-admitted`, and `unchanged: [specification, reference, known-bad]`; no further critic correction is authorized.

The R26 correction-author prompt exposes only each derived ID, frozen problem and proposed R24 test, plus the approved specification-review instruction. It contains no reference or known-bad source. Both lane archives returned code 0, did not time out, contain no disallowed tool item type or event parse error, and their normalized emitted test text equals the stored R26 test byte-for-byte. This establishes correction provenance and blindness; it is not candidate execution evidence.

## Per-candidate findings

### JavaScript generation-0120 — positive

The prompt enumerates usable criteria fields but does not prohibit unrelated own fields. Removing `assert.throws(() => selectCandidates([], { extra: true }), TypeError)` resolves the unsupported oracle without weakening stated behavior. The suite still covers normalization, filtering, all sort modes, stable ties, boundaries, fresh objects/arrays, nonmutation, whole-input validation, trimmed duplicate IDs/skills, malformed values, and sparse arrays at all three relevant locations. The reference uses indexed loops, so sparse candidates and sparse skill arrays are observed as invalid; the retained mutant uses `candidates.map`, skips a sparse candidate slot, and is directly rejected by the sparse-candidates assertion. The reference remains plausible and idiomatic.

### JavaScript generation-0292 — positive

The new `new String('N')` and `{ toString: () => 'N' }` cases directly enforce the prompt's “exactly one of” primitive commands. The reference's explicit `typeof command !== 'string'` rejects both. The retained mutant omits that type check and lets `hasOwnProperty` coerce both keys, so the witnesses distinguish it. Existing tests retain all four primitive directions, blocked/out-of-bounds fresh returns, rectangular/dense/binary whole-grid validation, plain/null-prototype position handling, start validation, exact result shape, and nonmutation. No unrelated policy was added.

### TypeScript generation-0294 — positive

Indexed tag validation in the reference correctly rejects sparse constructor and replacement arrays. The replacement witness is followed by unchanged-state and unchanged-notification assertions, preserving the atomicity requirement. The new identity fixture registers `A,B,A`, unsubscribes only the last `A` twice, then expects `A|B`; the registration-object reference satisfies this, while callback-index removal deletes the first `A` and yields `B|A`. Existing ownership, normalization, snapshot, listener mutation, later-subscription, per-listener-copy and error tests remain intact. The API and reference are coherent strict TypeScript.

### TypeScript generation-0366 — positive

The new isolated controller registers `A,B,A` independently in the `create` and `transfer` buckets, unsubscribes the last `A` idempotently, and expects `A,B` for each event. Registration-object removal in the reference preserves that order; callback-index removal leaves `B,A` in both buckets. The fixture therefore distinguishes registration lifetime rather than merely callback count. The existing suite retains title semantics, all event methods, insertion/snapshot behavior, duplicate calls, idempotence, runtime validation and immediate exception propagation.

### TypeScript generation-0368 — positive

Changing `errorsOf` to `readonly string[]` aligns the helper with the exported discriminated union and removes the static TypeScript mismatch. Equal-boundary successes for years `0099` and leap year `0096` directly exercise the 0–99 UTC-year hazard. The reference initializes a date and uses `setUTCFullYear`, preserving those literal years; the retained `Date.UTC` mutant remaps them to 1999/1996 and fails. Invalid 1900 and valid leap-century 2000 cases independently anchor Gregorian logic. The correction deliberately removes the old year-zero case rather than creating an unapproved year-zero policy. Existing ordered/unique validation, exact syntax/calendar rules, email, online venue normalization, ownership and nonmutation checks remain intact.

## Seven-criterion assessment

1. **Prompt clarity:** all five frozen prompts are self-contained and unambiguous for the behavior exercised. R26 adds no behavioral prompt prose.
2. **API consistency:** CommonJS exports and TypeScript exported types/classes/functions match their prompts; return, error, ownership and notification semantics are mutually consistent. The sole R24 static type mismatch is corrected.
3. **Independent tests:** correction inputs are problem-and-test-only, archived outputs bind exactly to stored tests, and every corrected suite now contains a decisive witness for its retained known-bad. No generated code was run in this review.
4. **Non-triviality:** tasks combine validation with stable ordering, dense-array edge cases, grid movement, snapshot subscriptions, ownership isolation or Gregorian date logic. They are substantive training examples.
5. **Idiomatic reference:** indexed validation, primitive type guards, registration tokens, defensive copying and explicit UTC full-year handling are suitable JavaScript/TypeScript mechanisms. No reference defect was found statically.
6. **Dependency isolation:** all five use only the pinned Node/TypeScript standard environment; no external package, network, filesystem, service or cloud dependency appears.
7. **Realistic known-bad:** each mutant is a narrow semantic regression derived from a documented parent failure, and each is now separated by a focused oracle without overfitting to error text or implementation structure.

## Evaluation separation and source lineage

I statically compared each R26 prompt, reference and corrected test by SHA-256 against every textual component of 546 checked-in evaluation tasks: 540 private development/decision tasks plus six synthetic harness fixtures. There are **zero exact prompt, reference or test matches**. Maximum prompt token-set Jaccard similarity is low: 0.2384 (JS0120), 0.2448 (JS0292), 0.2361 (TS0294), 0.1972 (TS0366), and 0.2200 (TS0368). The nearest tasks are unrelated by behavior, so no eval leakage signal was found. This is an independent static separation check, not a replacement for the frozen admission deduplication gate.

All five retain McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, CC-BY-SA-4.0, with all five rights booleans true. Source records/hashes are: JS0120 row-06678 `69c6cfffad19490be61a88c476d533da295ec04d364fe78a0011f976745c23a3`; JS0292 row-26721 `ccefb7d9983b1c6a9c0ff788151ed0f947772372e767b324f5dc87474ffa2320`; TS0294 row-32734 `91c45d3dda6eef386f52513c5b4891329f5311810d4555c71a6d7495a098f89d`; TS0366 row-33158 `f2abb47eda2e3a2d3a2062d239d15f84ab6f0b01d6bb32155210d9f9b7c9f383`; TS0368 row-33254 `8cc7bc1f483937bc4a3c629ab2a27146064eff63ce575e798cf399a4f1b63751`.

## Exact artifact bindings

Shared raw-file hashes:

- R26 request: `1dc3ec0d046bc5beca47b72d2a5c3d37cd1e2cf86f39c275947b445622000677`.
- R26 feedback: `dc8ecab5c4911bc85b92f90d1392af7db49750e1dc080fdeb9f8345367bb4dc7`.
- R26 plan file: `48d7a05990b0882f209c78a0942b8e21ae44a103e1cad192241ec33c6c8d4071`; declared logical plan: `11dce4e35cb0afa717cc966b9540f541caf5f6258b967f260ade7131df0f0293`.
- R26 run contract: `bd94fcb8b81d1efb14380d496d5f5dcdc8715c3b47678d1865e2488c3b8c9448`; prior logical R24 plan: `d2816d2eaf52f5c8427808ec807f04439218bb6a502eb95f4bcee5df970d71bc`.
- R26 generation registry: `2045083c185c671803a717a81df41eeb8edd176523a3736401455a4a59330478`; combined candidates JSONL: `51eaef24706eb6031cd6205ef81b20f4509e2c624b9ccbbaa8f94240611b457c`.
- JavaScript correction evidence: `b8936f4f092d4ec1e7fefeedef3dd2748f5a13628be714f42cbd604907210a54`; final-output hash `efb6c487b0aea87cbc9ee06502e02824ba53fd44728b58c40dc33573080f5ad8`.
- TypeScript correction evidence: `26dcd0b4233b1d4bbcff197c35c0cf3bb527f579c3cdb4dbd0f08535f52a8503`; final-output hash `20a7f0de077e3ffdc21c14491492403563ce209e04e21c20ceee11bc02e5f4bd`.
- Parent corpus: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`; hold ledger: `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`.
- R24 JavaScript review: `2e7364d8f3c81ec492db2f4c425ca6d97818fe347fc68308f2ae879beb327f2a`; R24 TypeScript review: `911145bad77d8920b09fcd9d56c8abde2fed0cfc8889d6086bf8cecccea0df7d`.

Candidate hashes below are raw file bytes and canonical compact sorted JSON as labeled. Prompt/reference/test/mutant hashes are exact UTF-8 content hashes.

| Candidate | Raw file | Canonical JSON | Prompt | Reference | Corrected test | Mutant |
| --- | --- | --- | --- | --- | --- | --- |
| JS0120 | `ed48eeda06c6e8be3450505ceabdfb5641eb597a3a3e044f304a4b8d44393849` | `4807d2fb945a01fec775b666469382b79d4ef9e00e3a511447f90990b449dad8` | `fbd7759157b096cf29a3e26792567a8740c488379f1d8f137550ced6378fd1a5` | `1ae983a81af46f2404706e50b55fb70a673b425611284c97b32241702fbe4dcd` | `88bc4f535856d124e5aa5598696ec236b862a0be79ae3e8ef493e335800d6691` | `d16e2693faa0cf08dc8f4f5baa99cb99160b5b5e9aaa830a1c382ca16f4793c6` |
| JS0292 | `79a6e2d6f901cab49c2cfdea38dbd2b6cdd1896559272e4e7cc8b1384eb38324` | `7e375c11d8c15fc8a49d615a8479918c426badd07167e630d2cad97cdc9373bb` | `f52acc2ad2f434986b92081c1d3d94e9c94554346dd78acaa25d09a6bec7a88e` | `0428490cf58a6a878d428fdc343feea17d73f1954d6300ee3d0c258a62a4f4d7` | `ed59c4062c2dd904d7ac9cfb42b79dba3be9cd5326b1075276f498540c58faa0` | `818716c419f90dd5044d507fd786b86cbb04c8eb6f6aa381c949af3570166194` |
| TS0294 | `91f24e38ae9f95e0098de78f6df7bb23cf437c13bb9b2190aae9ebed838cf831` | `f726cbda75d5ce67266a7679d568abd4a87002457592320e779367782a451271` | `cd5ca15648adb86896b25b15026017f2e97dedaf223e7138853ad2d5112e02ea` | `2cc6f4fab53f9f87f31a4c9ad8436cfb1434eec35f24c760451bca959024b328` | `9708765e60be5b588218bfb25e7e6ec5c2b3eafd83035ab2e9bce9f00900914d` | `a07ec64c670cfa92ba83d55fe38b4ebe3a5ca59f22ae223d49b86118f9ded863` |
| TS0366 | `66f73d5a89ba3fccd24f795455d9c9d9939bff9c88ba62afa3764ae832409a8c` | `eec1871643bc904e8d070050d0cb110c539046160d2e8bccc3f423babc6286e3` | `cbccd01987d29e94683586f1f6cec54cc7836c0b4086ac311a58283af641a4f9` | `007b2ae8593535fdc4c435a83504c82d2059194c33f79656bb6b2536756f19cb` | `ca2a3d1d6e62d5f0d6f9492f92923b8a1d372c15b14e1b395e16540136efa9d9` | `0d56f1c639b53168b8c23d5e5470446af9d08484d22f7791a2ea92587981b3a2` |
| TS0368 | `33644052b8dedbcf24bd70746f9cdf5040f8fe74bb8029ad4081d76ee40ed467` | `7bced912c2129f482da8a65ee84036dae20c0d3f9f3ceeda883a532d3f6225dd` | `23910463ceac6581da65a37806a63b1120762f6429793c3384a83cd6c003c4c3` | `adcdaf2e12e71c8cfe821f607c05679e5edb562258e2e1cd7c8f140e4116078a` | `296280584c6f35f779ebad2b215a86b238fdba38b8cb3f578c037358d1c20ab0` | `2163414e32cce1677952064fe35c40474f02364920e82a3253ca5ad63baf23dc` |

Bound defect-evidence raw hashes: JS0120 `candidates-sparse-result.json` `09174d481b2a55c4d3159eb7c87fa9c56d7c198a585349c794bf77db80b00cc5`; JS0292 `robot-command-type-result.json` `2613728e58ad543a404048e38677c5c9532e1262808a6130ab8bb87aaaeb08e5`; TS0294 duplicate `c6d94e6538dbe6cde768340ec39b090e9f2b1b99a20b04be9ff16cc522e7ecb4` and sparse `d50e53603e0c9950fd7e937ea590d513bbdbd6f5fa387be52a8ed5a24b490a61`; TS0366 `54e8ef3280eeaeb8f988f82e3a314972d2c20ce2b0bb428898d2d1bf1d032ff6`; TS0368 `6e0517b692c7351625612ef7730320d99e824c5f7a73a79cb30480972ca2be3c`.

Main may carry these five static positives into the separate pinned sandbox reference/mutant verification and admission-dedup gates. Until those gates and an explicit admission seal pass, the truthful state remains generated, statically reviewed, **not verified by this review and not admitted**.
