# Provisional JS/TS recovery scopes — 2026-09-08

## Decision boundary

Six proposed held parents: two JavaScript generation tasks and four TypeScript repair tasks. **Selection proposal only; main approval pending.** No version, reservation, generation, execution, admission, training or central state change. Original prompts, full references and test files were freshly read; exact existing hold evidence was reconciled. No new executed result is claimed.

All six use **contract-clarification**. For JS this resolves exact schemas/matching rules explicitly. For TS this authorizes a new self-contained repair description and replacement complete embedded known-bad source, while preserving APIs and the original corrected objectives. It is intentionally not a reference-fix request: an embedded-source repair cannot both retain unchanged prompt bytes and replace its buggy source. Original parent records remain immutable.

For each TS repair, the approved proposal is to use the complete original parent reference (hash below) as the future known-bad baseline. It already contains the original repair but still exhibits the independently documented current defect. The future derived prompt must embed that entire exact known_bad_code, not an excerpt, diff, placeholder or the stale original broken source. No new candidate code is created here. The corrected answer must address the current defect and continue satisfying the original objectives. The independent test author may see only the resulting full specification (including its intentionally embedded repair source), never the separate corrected reference or old test suite.

## Scope decisions

### exp-v1-javascript-generation-0021

Clarify the closed OWN-field schema explicitly: initialHosts is an array of non-null non-array objects with exactly own keys id,name; register input has exactly own keys name,kind,address,host; host selection has exactly own id OR exactly own newHost, whose object has exactly own id,name. Required non-enumerable own fields are valid; reject every extra own string or symbol key, enumerable or not. Inherited fields do not satisfy required own keys; do not otherwise introduce a prototype restriction. All nonempty string checks mean typeof string and raw length>0, including whitespace-only IDs, names and address; preserve strings verbatim. kind stays exactly lab/kitchen/garden/studio. Only workshop uniqueness uses name.trim().toLowerCase(), so whitespace-only workshop names are valid but collide at the empty normalized key. Host IDs match exactly, including whitespace/case. Retain TypeError malformed/unknown-host, RangeError duplicate IDs/workshop names, registration order, detached schema snapshots and failed-registration atomicity. Fix both raw-length validation and own-key accounting in the reference; a new single-defect mutant should retain correct own-key handling and only reintroduce trim-empty rejection, not combine two bugs. Independent tests must accept whitespace host ID/name/address and workshop name, test normalized duplicates, hidden required own fields and extra hidden/symbol own keys, exact host IDs and failed pending-host rollback.

- Parent canonical JSON SHA-256: `2cf9f5f966b6ebf90bd0478cee68748624b1d576a048c6e6615ffef14a2430b7`
- Original prompt SHA-256: `46efe83fbe2c4f9f97f5d5cb14cde5b68b78e52c2b73c8151781477de02b8f23`
- Original reference SHA-256: `3248c5d66e3ad1661936484ae07908705af79b56e6f0c9f83e700c9f6eb39582`
- Original test SHA-256: `edfaabac10117b713e390b939cace42f5e7292a1f8e82b6898fef9bed4658d0b`
- Existing evidence: `measurement/data/expansion-v1/cutoff-5885-review/JS_TS_FINAL_CONTRACT_ADJUDICATION_20260908.md`
- Evidence SHA-256: `47a779ab1fca686b69041c94492b08046616c10e20426a1824d8eabee6f81494`
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-00219`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source-record SHA-256 `570aca93538e32791fd137a753998ec31fea164be8938475b081bbb2c257de75`.
- License: `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/); source URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Exact recorded rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

### exp-v1-javascript-generation-0390

Clarify matching separately from validation: requested readerId and reader id/displayName must be nonempty after trim; compare trimmed reader IDs with the trimmed requested ID and select the first reader. Loan readerId/title must be strings of raw length>0, with whitespace-only values valid; returned is boolean. Explicitly compare loan.readerId.trim() with the selected trimmed reader ID. Returned summary id/displayName and included titles are trimmed, so a valid matching whitespace title contributes an empty string. Preserve full validation of both arrays before returning null or a profile, order, duplicates and detached outputs. Do not introduce closed-own schemas, plain-object/prototype restrictions, scalar caps, or own-only fields for these structurally read records. A single-defect mutant may reintroduce trim-empty rejection only for loans. Tests must accept an unrelated whitespace loan even with no selected reader, accept a matching whitespace title, verify padded matching IDs, reject malformed unrelated trailing records, retain first-reader precedence, duplicate active titles and snapshots.

- Parent canonical JSON SHA-256: `3f0c6bd651ef327055ce000ff862d1be3fdd00b3d3c7b7a45e4ad60bb34971a5`
- Original prompt SHA-256: `b0cf03a840c972b2213ea15a1e8bc9705d44b67e5bb9d60a87f38b93f0f0f1f1`
- Original reference SHA-256: `9353415e30ed72f6ca49bc55b756e014643540d945dafe59e72037b06e5dfcce`
- Original test SHA-256: `0e1a8b0f092aaa57a7df065fd2dc424813a0b638555917486a415846a59b06ab`
- Existing evidence: `measurement/data/expansion-v1/cutoff-5885-review/FINAL_DELTA_JAVASCRIPT_2_20260908.md`
- Evidence SHA-256: `38297aefe5ac527dd764175fee0ebbc95579ec21091abe75cd8e6b8a7e8d910c`
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-26423`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source-record SHA-256 `f5feb893a39d7ad8c864d967a146e4114c4dabdbb9cc0107bb7602018449c1cc`.
- License: `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/); source URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Exact recorded rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

### exp-v1-typescript-repair-0096

Contract-clarification permits replacing the complete embedded known-bad source and its repair description, not changing exports or broadening types. Use the complete ORIGINAL PARENT REFERENCE as the new known-bad baseline: it already fixes slice(1) to slice() and retains exactly the current duplicate-unsubscribe defect. Explain that each subscribe call owns one registration and its idempotent unsubscriber removes that registration, not the first equal function. Correct reference with unique registration identity; capture callback values for the start-of-broadcast snapshot so an active flag cannot suppress a captured callback. Preserve every original objective: include the first listener, synchronous registration order, later-only subscription changes, immediate throw-value propagation, empty relay, exact registry name validation/replacement/get behavior. Test A,B,A removing final A twice yields A,B, independently removing first A yields B,A, snapshot removal/addition and all original objectives. The derived prompt must embed byte-for-byte the complete new known_bad_code; retain the original parent/hash separately. Do not label this reference-fix because the embedded prompt must change.

- Parent canonical JSON SHA-256: `846868f13ef88886da1a492d2412a57a583f7b3d4a8c2aa847ecf23465c4b878`
- Original prompt SHA-256: `d9dba29e91788a63582cb9d77fa71ae6e747d32e70f90fb4b5342560e1eb28eb`
- Original reference SHA-256 (proposed complete new embedded mutant): `d48feaffe4ae253855fd179d79734009bb9247b18ca2c56fb130906d11d0d8b0`
- Original test SHA-256: `ddadf4685da052b7f3c9ef77ad907477266cf4223b268097c40347c6e13f8e36`
- Existing evidence: `measurement/data/expansion-v1/cutoff-5885-review/relay-duplicate-result.json`
- Evidence SHA-256: `aaf9917218bf110dde5c487e74a505885c5f52cdbb7c107d1a77f008b548e908`
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-32595`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source-record SHA-256 `e06bf1a82e23c47bbb0795abb447726303719143e3db08136b27598235730eec`.
- License: `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/); source URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Exact recorded rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

### exp-v1-typescript-repair-0100

Contract-clarification permits replacing the complete embedded known-bad source and repair description while preserving Exhibit, ExhibitEvents and ExhibitController API. Use the complete ORIGINAL PARENT REFERENCE as new known-bad: original key-preservation repair already applied, only registration-identity removal remains defective. Clarify per-event subscription-call identity and idempotent unsubscribe. Correct registration storage while preserving captured callback snapshot values, typed event buckets, finite rating 0..5, rating prevalidation before update effects, original immutable key, caption/artwork/rating event order, change-only emission, fresh state and input nonmutation. Test A,B,A remove final A twice on captionChanged yields A,B; separately exercise another typed bucket and first-registration removal, snapshot changes, invalid-update atomicity and original identity/order repair. Do not demand rollback after listener exceptions or add blank caption/key restrictions. Embed the exact complete new mutant in the rewritten repair prompt; retain original parent lineage. Use contract-clarification, not reference-fix.

- Parent canonical JSON SHA-256: `0c9f232fce163505b6652cfa7e6053964dbd919796ca2219933b2dd408fbb9f6`
- Original prompt SHA-256: `76b756e1c36b5f2be6208cb4392df62e17d67dea1c16b4662b9609cfefc3491f`
- Original reference SHA-256 (proposed complete new embedded mutant): `f182cd21d551ba4b15e673281419d5079210649cce077b64b1d57bf3458f7aeb`
- Original test SHA-256: `ff343bb78fe59b6be6b6e09e4a6f2da65cfe9b6d6f70b14ac299b536e21f72f4`
- Existing evidence: `measurement/data/expansion-v1/cutoff-5885-review/exhibit-duplicate-result.json`
- Evidence SHA-256: `19147789d723257348b669eed0b51a25b53924cd34bcc953483388d0d7afd9ed`
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-33061`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source-record SHA-256 `db399baac0df2bb26333f3e5960eb91617067d0ad7ee3f6401d7d82916a30944`.
- License: `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/); source URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Exact recorded rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

### exp-v1-typescript-repair-0174

Contract-clarification permits replacing the complete embedded known-bad source and repair description while preserving OutlineNode, OutlineRow and OutlineTree API. Use the complete ORIGINAL PARENT REFERENCE as new known-bad: expand-only traversal is already repaired; duplicate-unsubscribe identity remains defective. State explicitly that repeated registration of the same listener creates distinct subscriptions and each idempotent unsubscribe removes its own registration. Correct using registration identity with captured callback values for each selection snapshot. Retain immutable hierarchy copy, blank/duplicate/cycle TypeError validation, atomic replacement then expansion/selection reset, root/sibling order, collapsed-descendant exclusion, new frozen rows, unknown-ID return behavior and non-immediate ordered subscription snapshots. Tests must use A,B,A removal of final A -> A,B, plus first removal and snapshot additions/removals; preserve original expansion repair, input detachment, cycle/duplicate validation and failed replacement atomicity. Do not invent sparse/out-of-type hierarchy domains or per-listener state rollback. Embed exact complete new known_bad_code in the updated repair prompt and preserve parent lineage; class is contract-clarification.

- Parent canonical JSON SHA-256: `f316c5339d54566a1d44c10b172495ba5d1627e71456053fe921fa9cd2dce650`
- Original prompt SHA-256: `127590c62cd5972fb8ada0c25148d18786ced8ee906b53c1adf8259f8f1118a2`
- Original reference SHA-256 (proposed complete new embedded mutant): `14d21dc4a5f33b1097d528d0af716a3b73c36a63b5e291d524de965a7a54754e`
- Original test SHA-256: `40d7e3bcd1f868ec970e85e4271ac63a2e8abbd1d2e9205d4c624556c16bf29b`
- Existing evidence: `measurement/data/expansion-v1/cutoff-5885-review/outline-duplicate-result.json`
- Evidence SHA-256: `5168844e7e3587055fc413f8e3faeb46853d517cf61e2a667f829c954b6d1053`
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-33501`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source-record SHA-256 `e9a3ff191369d76e6ceb1757553eb47446ea1b8c748d0892ee5ce15f0f3f8ca2`.
- License: `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/); source URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Exact recorded rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

### exp-v1-typescript-repair-0149

Contract-clarification permits replacing the complete embedded known-bad source and repair description while preserving all original exports/APIs and objectives. Use the complete ORIGINAL PARENT REFERENCE as new known-bad: case-before-message precedence is already repaired; short-circuit/selective decoding remains the one defect. State explicitly that outside mock mode every nonempty ampersand-delimited pair has BOTH name and value decoded with plus-to-space then decodeURIComponent, including irrelevant names, later duplicate fields and fields after a usable case; no selection return may mask malformed escapes. Preserve optional leading ?, first-equals split, first nonempty trimmed duplicate value, case precedence independent of order, mock bypass of all parsing, URIError when no reference, and unchanged returnDestination URL/text/trim/detachment behavior. Tests include case=valid&message=%ZZ, ignored=%ZZ&case=valid, case=valid&%ZZ=x, and malformed duplicate tails, plus original precedence, valid encoding and mock bypass. Do not replace URIError semantics with forgiving URLSearchParams parsing or invent field limits. Embed exact complete new mutant in the repair prompt; retain original parent lineage; class is contract-clarification.

- Parent canonical JSON SHA-256: `4a041dc80f6d1a47c8c6baae237c8d73e94c6d924c956e5bdc1f5a907939e04b`
- Original prompt SHA-256: `cff20d4df2933998f63a480a51f2aad9cba79b04fb65ebc7983b21ef00ec4c6b`
- Original reference SHA-256 (proposed complete new embedded mutant): `013bbc75503631fff4695a228ec7ee7657c3f2456c021ca329737891e4bb1e5b`
- Original test SHA-256: `dc277d34fc9b25a7b5402cfea73bf5ebc74b14f2396a3ab361f9801be2c021b8`
- Existing evidence: `measurement/data/expansion-v1/cutoff-5885-review/query-invalid-tail-result.json`
- Evidence SHA-256: `15e27a6c2f036e408dfd51f412ee006c8ebc54fa8dc3549cbd43e2bd82a35e78`
- Source: `Multilingual-Multimodal-NLP/McEval-Instruct`, `row-33252`, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, source-record SHA-256 `3f671bf1def355a753f591af287f0357d65c8fa0a31cca84b77f64a004d679bf`.
- License: `CC-BY-SA-4.0` (https://creativecommons.org/licenses/by-sa/4.0/); source URI: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct.
- Exact recorded rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

## Seven-criterion scope calibration

- Prompt clarity: exact additions above, not inferred new domains. JS0021 closed-own schema is a proposed contract choice rather than a claim it was fully explicit originally. JS0390 raw loan validation and trimmed ID matching are separately specified. TS0174 duplicate registration identity is made explicit.
- API consistency: original exports, types, methods and original repaired behavior remain. Repair source replacement is explicit and versioned.
- Independent test origin: future authoring must follow the existing separated workflow. This proposal does not establish future test independence.
- Non-triviality: workshop transactions and detached snapshots; whole-collection validation/join semantics; ordered event snapshots with independent subscriptions; immutable tree validation and visible traversal; and full query decoding/selection are substantive whole targets. No elementary padding is proposed.
- Idiomatic behavior: use ordinary own-key accounting/explicit field extraction, exact string rules, registration identity without suppressing captured callbacks, and full native decoding before selection.
- Dependency isolation: preserve standard runtime facilities and existing pinned sandbox targets; add no external packages.
- Realistic known-bad: JS mutants should target only the specific validation bug while honoring clarified schemas; TS uses the exact parent reference with the original repair already applied. The four existing isolated diagnostics each compile and then fail semantically, with recorded exit codes [0,0,1] and no timeout. Those are historical artifact facts, not new execution.

## Evidence and proposal format

Parent corpus: `datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`, SHA-256 `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`. Canonical parent hashes were freshly recomputed using sorted-key compact JSON. Existing evidence files were freshly hashed. Source/rights objects are copied exactly into the accompanying proposal; their previous authorization is preserved, not reopened.

`recovery-repair-js-ts-PROVISIONAL.json` contains only a top-level selections array. Each selection binds this report plus the exact parent, original hold evidence, source and rights, with the narrow scope in rationale. It intentionally lacks a version, reserved derived IDs, approval claim and executable plan seal. Main must explicitly approve these choices, bind the then-current hold ledger/corpus and assign a fresh version using normal planning. Extra provenance fields in this proposal are explanatory; the planner independently recovers authoritative source/rights from the hash-bound parent.

If a future correction fails quality or sandbox gates, retain the exclusion and its evidence. This proposal does not authorize repeated automatic critics, broader schema restrictions, silent oracle relaxation or release.

