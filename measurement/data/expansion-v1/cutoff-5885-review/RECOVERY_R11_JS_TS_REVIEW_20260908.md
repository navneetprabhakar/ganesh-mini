# Recovery r11 JS/TS independent static review — 2026-09-08

## Result and scope

**6 scoped positives; 0 blocking holds:** JavaScript generation 0021/0390 and TypeScript repair 0096/0100/0174/0149.

Current gate: derived quality review before pinned serial sandbox diagnostics/admission. Full original and derived prompts, references and tests were read; all derived mutants were read; approved plan scopes were reconciled with `RECOVERY_REPAIR_SCOPE_JS_TS_20260908.md`. This report makes no execution, admission, original-row coverage, new selection, generation, cloud or central-state claim. Only this file is written.

All six have concrete regression witnesses. No invalid oracle was found. Two specific coverage omissions are recorded below as nonblocking because the actual repaired defects are already witnessed; they are not represented as completed exhaustive coverage.

## Individual decisions

| Derived candidate | Static decision | Decisive test behavior |
|---|---|---|
| exp-v1-recovery-r11-javascript-generation-0021 | Scoped positive | Whitespace-only host ID/name, workshop name and address succeed; normalized blank workshop names collide; hidden required own fields and symbol extras exercise clarified schemas. |
| exp-v1-recovery-r11-javascript-generation-0390 | Scoped positive | Matching whitespace-only title yields an empty string; an unrelated whitespace-only loan validates before null; padded IDs join correctly. |
| exp-v1-recovery-r11-typescript-repair-0096 | Scoped positive | Register A,B,A, remove final A twice, broadcast produces A,B; captured removed callback still runs during current broadcast. |
| exp-v1-recovery-r11-typescript-repair-0100 | Scoped positive | Caption A,B,A removes final registration independently; invalid update is atomic and original key/event order remain correct. |
| exp-v1-recovery-r11-typescript-repair-0174 | Scoped positive | Selection A,B,A removes final registration independently; failed replacement preserves expansion/selection and old expansion-only traversal remains repaired. |
| exp-v1-recovery-r11-typescript-repair-0149 | Scoped positive | Malformed irrelevant and duplicate-tail escapes reject despite an earlier usable case; mock mode bypasses malformed input entirely. |

### JavaScript 0021 — closed-own-schema transactional registry

The derived specification explicitly states raw-length-nonzero strings, closed own-field schemas, non-enumerable required fields, rejection of extra own string/symbol keys, and no additional prototype restriction. This matches approved scope rather than silently transferring trim rules or assuming plain objects.

The reference uses Reflect.ownKeys plus own-property checks and copies required fields explicitly. Host IDs remain exact; only workshop-name uniqueness normalizes trim/lowercase. Host addition is deferred until the complete registration validates, and snapshots detach the nested host.

The supplied mutant changes only the nonEmpty helper to trim-based rejection, retaining corrected own-key handling. The independent blank-host/workshop fixture distinguishes this directly. Tests additionally exercise hidden required fields, inherited required-field rejection, unusual prototypes with correct own fields, symbol extras, duplicate names/host IDs, exact host case, pending-host rollback, registration order and snapshot isolation. No unpromised public API requirement was found.

**Coverage omission:** extra non-enumerable string keys are not explicitly supplied, despite that variant appearing in the approved scope. Symbol extras and hidden required-key success do test the substantive own-key correction, and the reference directly counts all own keys. This is not a missing mutation witness or contradictory oracle; no hold is assigned. Do not claim that specific variant was tested.

Whole-target substance: coordinated host/workshop identity, normalization, validation, commit atomicity and nested copies—not a standalone nonempty-string exercise.

### JavaScript 0390 — fully validated reader/loan join

The derived prompt explicitly separates after-trim reader validity from raw-nonempty loan strings and states trimmed loan-ID matching. It retains structural readable fields, including inherited fields, without extra schema/prototype restrictions.

The reference validates all readers and loans through full iteration, captures fields once, chooses the first normalized reader match, and constructs fresh scalar/array output. A whitespace-only matching title legitimately trims to empty. The mutant only reintroduces trim-empty checks for loan fields.

Tests contain both decisive cases: a matching blank title produces an empty active title, and an unrelated loan with whitespace ID/title is accepted when no reader exists. Padded-ID matching, first duplicate reader, duplicate titles, returned filtering, inherited/hidden fields, null-prototype records, frozen inputs, malformed unrelated trailing values, sparse holes and independent result arrays are covered. Undecorated empty arrays in malformed-record fixtures fail for missing fields; they do not impose an array exclusion on valid decorated objects.

Whole-target substance: validation before selection/null return, normalized cross-collection matching, ordered duplicates and detached output. No invalid oracle or remaining repaired-defect witness gap found.

### TypeScript 0096 — relay registration identity

The complete embedded mutant is exactly the original parent reference: the first-listener slice bug is already fixed. Only unsubscribe-by-function-identity remains.

Reference registration objects identify each subscription independently. Broadcast captures raw callback values before invoking them, so later removal cannot suppress an already captured callback. Tests explicitly remove the final duplicate twice and check A,B; then remove the surviving first duplicate independently. Other tests preserve first callback, snapshot removal/addition, exact thrown-value identity, immediate stop, empty relay and registry replacement/blank-name behavior. Public exports/signatures are preserved; no new runtime domains or type hacks appear.

Whole-target substance: registration identity interacts with call order, idempotence and mutation during notification.

### TypeScript 0100 — typed controller events

The complete embedded mutant is the original parent reference with key preservation already fixed. The reference adds per-event registration objects and keeps callback snapshots. Rating prevalidation precedes any update effect, immutable key is retained, and fields change in caption/artwork/rating order.

Tests preserve rating bounds and exact error message already present in the repair input, change-only emissions, ordered update events, failed-update atomicity, fresh state, caption duplicate-registration identity and snapshot changes. No unsupported rollback-after-listener-error behavior is demanded. Readonly state mutations are performed through local test-side writable views to check returned-copy isolation, not by weakening the public API.

**Coverage omission:** duplicate-unsubscribe is exercised on captionChanged only, not independently on a second event bucket as proposed in the scope. Other buckets are exercised by ordered events, and the generic reference implementation and mutant share the same registration mechanism. The actual defect is decisively witnessed, so this is nonblocking incomplete variant coverage rather than a static hold.

Whole-target substance: validation and immutable identity interact with typed ordered change notifications and registration ownership.

### TypeScript 0174 — immutable hierarchy and selection snapshots

The complete embedded mutant is exactly the parent reference with expanded-only traversal already fixed. The derived clarification states distinct duplicate subscriptions and atomic replacement; frozen returned arrays preserve the existing source behavior.

Reference cloning finishes before state replacement, detects blank/duplicate IDs and active-path cycles, resets expansion/selection on successful replacement, and copies callback values before notification. Registration tokens resolve the current defect.

Tests check complete state preservation after blank/duplicate/cyclic replacement, input detachment, frozen fresh arrays/rows, expanded preorder, reset semantics, unknown-ID behavior, non-immediate notifications, final-duplicate unsubscribe and later-only listener changes. They do not force out-of-type sparse hierarchies or invent per-listener rollback.

Whole-target substance: recursive immutable graph validation, visibility state and ordered subscriptions. No invalid oracle or missing mutation witness found.

### TypeScript 0149 — full decoding before precedence selection

The complete embedded mutant is exactly the parent reference with case-before-message precedence already fixed. The new description expressly requires decoding both halves of every nonempty pair, including irrelevant and duplicate tails, before choosing a result.

The reference does one complete decode pass, retains first nonempty trimmed case/message values and selects case only afterwards. Mock mode still exits before any decoding. The destination function retains its original behavior and API.

Tests directly distinguish the mutant using malformed irrelevant value after a usable case and malformed duplicate tail; they also cover malformed content before a valid case, malformed name, leading question mark, first-equals split, plus/percent decoding, first nonempty duplicate, precedence in both orders, mock bypass and detached trimmed destinations. No forgiving URLSearchParams interpretation, hidden wire format or arbitrary error text is demanded.

Whole-target substance: full-input validation interacts with decoding, duplicate selection, precedence and explicit bypass.

## Seven-criterion reconciliation

For each scoped positive:
- **Prompt clarity:** derived clarification is within its approved scope and repairs have complete embedded source.
- **API consistency:** original requested exports/types/methods remain; no unpromised traits/global overloads are imposed.
- **Independent test origin:** verified specification-only author inputs, with the important repair qualification below.
- **Non-triviality:** the complete behaviors described individually are substantive; patch size is not the criterion.
- **Idiomatic code:** direct reconstruction, Map/Set usage, registration-token ownership, captured callbacks and complete decoding are appropriate static implementations.
- **Dependency isolation:** standard JS/TS runtime facilities only; test files use node:assert for JS and local assertions for TS.
- **Realistic known-bad:** all six contain an identified semantic bug and a distinguishing test; this is static witness reasoning, not a claim that the mutant has executed and failed.

No artifact may be admitted solely from these findings. Compiler errors, runtime errors or infrastructure failures remain separate from semantic mutant proof.

## Test-author provenance and lineage

Each independent task object has only `id` and `problem`, exactly matching the installed derived problem. Each independent output test_code equals the installed test file. Architect output problem/reference_code/known_bad_code also matches the installed artifact exactly. All recorded teacher runs return 0, are not timed out, and have no disallowed tool-item events.

**Repair qualification:** the TS author did see the full broken implementation embedded in each repair problem, which is intentional task input. The generic evidence preamble saying no known-bad implementation was seen is not literally accurate for repair tasks. There is no separate corrected-reference or separate mutant-source field in the independent context; the author was not blind to the embedded broken code, and this report does not claim otherwise.

For all four TS repairs, the known-bad code bytes equal the full original parent reference bytes, and those exact bytes (including final newline) occur in the derived prompt. This implements the approved replacement of the repair target without changing the historical parent.

Parent canonical hashes, base source fields and rights were checked against the original corpus and plan. All source dataset/revision/record/hash/license/URI fields match their original parent; source transformation adds recovery lineage. All five rights flags remain true. Original rights decisions are preserved, not re-adjudicated.

Plan: `datasets/cache/expansion-v1/versioned-recovery/r11/plan.json`, file SHA-256 `2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6`.
Run contract file SHA-256: `a0b4a39242bee4710967f7d01a0d6031bf4a81401f3aca98bcab09c80b80c6a8`.
All six plan rows bind `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_REPAIR_SCOPE_JS_TS_20260908.md` at `9516eb39a7fe10786d8aae08c434ff70233fa639b11fb960ca6022da3a35df24`.

### Raw author-evidence bindings

Paths below are relative to `datasets/cache/expansion-v1/versioned-recovery/r11/`. Input/output text hashes were recomputed and match their evidence declarations.

- `javascript-recovery-architect-evidence.json`: file `e916b908d757b81bd5726023fae580f39ffeebddca93acba46d8641f168179fc`; input `9b413c4a35d51a468bbaa54fadf199b64136016c113bb0c2ef29224471fe72a5`; output `717c7f6a914b55effcc7c284633525df7608b5212a4a9740e808c9aea6f19c5b`.
- `javascript-recovery-independent-tests-evidence.json`: file `52ef99f1f3c94ec6c2b1626ac74ba201bc9342f8a0f2aa9bcf9f2dbe5663a494`; input `d71f075ae92d9e39992e6a0800b9c7089da360fec3b305dfa4df827d7793f17c`; output `f8958f02708023ce67ec2672d7585da43a9aad942dbc954a1b5f6c43579286fd`.
- `typescript-recovery-architect-evidence.json`: file `05bbe4401515ad359a335110152abdafd55d3346e237a5e84581a8a5d62ffc75`; input `9f5f696c4f8fc1a50830042c4944062684d4766f867ece5672cd7be58f388da7`; output `6299fcc162127f86063025c7b23c55855da4a527c59d6aa84762f68d926efcef`.
- `typescript-recovery-independent-tests-evidence.json`: file `71e47ec441300aa9c82e5e0d7e739513f168785b8118d90ce21ef084a9a34a79`; input `97a94178951a841f681742c16ebb06574213410acd079f35c211cab62844aa50`; output `8e38363e6daf338310b4c92869a2c155d0009b674cf69f25c387b4fa28a8418c`.

### Exact candidate bindings

#### exp-v1-recovery-r11-javascript-generation-0021

- File: `exp-v1-recovery-r11-javascript-generation-0021.candidate.json`; raw file SHA-256 `fe3c83eb41ccf2f0652e5cfe372dac41e36765535a2399d39fd6a3ec4334e157`.
- Parent canonical SHA-256: `2cf9f5f966b6ebf90bd0478cee68748624b1d576a048c6e6615ffef14a2430b7`.
- Derived prompt SHA-256: `a677b9bdc56849c2b23c7e5ba9c45666810db33e84a674dbc779deec31ef9011`.
- Reference SHA-256: `f6cdce2f338fcfd8463e36d945af79634afd0adac2387602299104d6fe186f6d`.
- Independent test SHA-256: `7274acef20c5ceb6a347810a65ef6ee683efd25af56eabb4d4f9a8fba6d8602d`.
- Mutant SHA-256: `4e8f828a47b466ba8c8189451910d9bd2fce68213cdac55473aa3c895ed08aa1`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-00219`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source record SHA-256 `570aca93538e32791fd137a753998ec31fea164be8938475b081bbb2c257de75`, license `CC-BY-SA-4.0`.
- Rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

#### exp-v1-recovery-r11-javascript-generation-0390

- File: `exp-v1-recovery-r11-javascript-generation-0390.candidate.json`; raw file SHA-256 `634985d240b999e65438b4a7ed2ef5a7431e40acadcb601b015dbd5f1a74254a`.
- Parent canonical SHA-256: `3f0c6bd651ef327055ce000ff862d1be3fdd00b3d3c7b7a45e4ad60bb34971a5`.
- Derived prompt SHA-256: `792fcb1b9197bbeefcd8996db2328e26286acb00b4ad89359ce155389c2f069b`.
- Reference SHA-256: `2d44b6fa444e4534e4e1a7498b9da6a0dbac433d7e1accc584c6359a1af40b02`.
- Independent test SHA-256: `63af7d8fda1bd61a6d1ba7b2b9aebcbb38514a4ae93755782343acec4a44d185`.
- Mutant SHA-256: `3da6e07ccc94b6dc700332eee87f48a6583935b731765ccbefa7ab55d870e502`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-26423`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source record SHA-256 `f5feb893a39d7ad8c864d967a146e4114c4dabdbb9cc0107bb7602018449c1cc`, license `CC-BY-SA-4.0`.
- Rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

#### exp-v1-recovery-r11-typescript-repair-0096

- File: `exp-v1-recovery-r11-typescript-repair-0096.candidate.json`; raw file SHA-256 `760fac12a40323076afd8e4d4888c2bd2b2c297b123ac14eee3bb8fe8f2e4b03`.
- Parent canonical SHA-256: `846868f13ef88886da1a492d2412a57a583f7b3d4a8c2aa847ecf23465c4b878`.
- Derived prompt SHA-256: `b3bc393d4aed973969f3a1b73f426fd21430b1f43983854d7851f8016b2b36c8`.
- Reference SHA-256: `3fa1b4a44d50816cc01e53dbede9c1fb3906f7d4a3c6c14f68e19c356c9970b8`.
- Independent test SHA-256: `5aa600034e7ec34154ba0331a1ad2c35ba21a4535af2f8d60a48f84c57a71109`.
- Mutant SHA-256: `d48feaffe4ae253855fd179d79734009bb9247b18ca2c56fb130906d11d0d8b0`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-32595`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source record SHA-256 `e06bf1a82e23c47bbb0795abb447726303719143e3db08136b27598235730eec`, license `CC-BY-SA-4.0`.
- Rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

#### exp-v1-recovery-r11-typescript-repair-0100

- File: `exp-v1-recovery-r11-typescript-repair-0100.candidate.json`; raw file SHA-256 `e41aed360084a95f221c96d826245014e639963734e77c96d52a439c137ac68a`.
- Parent canonical SHA-256: `0c9f232fce163505b6652cfa7e6053964dbd919796ca2219933b2dd408fbb9f6`.
- Derived prompt SHA-256: `0f9ea809ca343652176bf7fdabfbbd4f4714945572e32a49ae878a0bbdf2e5dd`.
- Reference SHA-256: `c3af3205413ae5902149c995fa783b32fe813e23b64b6772e7226cd992ad6bdb`.
- Independent test SHA-256: `029a76c724fa7c6b8255ae68783b3cd37e02dcca96a5773f9fd15d9bf80c02a2`.
- Mutant SHA-256: `f182cd21d551ba4b15e673281419d5079210649cce077b64b1d57bf3458f7aeb`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-33061`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source record SHA-256 `db399baac0df2bb26333f3e5960eb91617067d0ad7ee3f6401d7d82916a30944`, license `CC-BY-SA-4.0`.
- Rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

#### exp-v1-recovery-r11-typescript-repair-0174

- File: `exp-v1-recovery-r11-typescript-repair-0174.candidate.json`; raw file SHA-256 `f83e71e6d3a2c49d8f69caaf3cd2cc321c44c0faf14909d6ab7656fb24cc05da`.
- Parent canonical SHA-256: `f316c5339d54566a1d44c10b172495ba5d1627e71456053fe921fa9cd2dce650`.
- Derived prompt SHA-256: `c929a7b6f173befa831d305f329ff144089918d5827dda71da91c2efce880667`.
- Reference SHA-256: `6be5b480be88fb4407fe5f0e00e42351d4d38f0f3b857148e9bb270e5de53cc4`.
- Independent test SHA-256: `068b8235684e186ad8f7dcfbe0a4af2374da668e911d62d7c217700f31bb4edb`.
- Mutant SHA-256: `14d21dc4a5f33b1097d528d0af716a3b73c36a63b5e291d524de965a7a54754e`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-33501`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source record SHA-256 `e9a3ff191369d76e6ceb1757553eb47446ea1b8c748d0892ee5ce15f0f3f8ca2`, license `CC-BY-SA-4.0`.
- Rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

#### exp-v1-recovery-r11-typescript-repair-0149

- File: `exp-v1-recovery-r11-typescript-repair-0149.candidate.json`; raw file SHA-256 `619c736d5c81044f8902ce000d831e451046db2a8a81ec4f7575d783d887ab41`.
- Parent canonical SHA-256: `4a041dc80f6d1a47c8c6baae237c8d73e94c6d924c956e5bdc1f5a907939e04b`.
- Derived prompt SHA-256: `ebfcc69a72fff2e5324bc0969d333806edd750ab4855a43e1800935523423480`.
- Reference SHA-256: `17572e482ae2deae446ad3ef2c7c312ac11b9a04b0b8d2194bece4929a48b298`.
- Independent test SHA-256: `258328228ce99fd9242ea5a390591db3f63c90cbc9db295815dd21d63eb5a6f7`.
- Mutant SHA-256: `013bbc75503631fff4695a228ec7ee7657c3f2456c021ca329737891e4bb1e5b`.
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-33252`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source record SHA-256 `3f671bf1def355a753f591af287f0357d65c8fa0a31cca84b77f64a004d679bf`, license `CC-BY-SA-4.0`.
- Rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

## Handoff

Main may run serial diagnostics against these exact six files. Preserve all results, including failures, and retain the unchanged original evidence. Separate evaluation separation, deduplication, corpus composition and admission seals still apply. This report does not claim the entire r11 run completed: other lanes/run-level status are outside this six-artifact review.

