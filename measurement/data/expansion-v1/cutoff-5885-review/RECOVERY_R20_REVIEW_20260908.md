# R20 terminal recovery review — 2026-09-08

Gate 2. Exactly two corrected artifacts reviewed in full against R19 and approved R20 feedback: Python generation-0717 and Rust generation-0487.

**Two scoped seven-criterion positives; no new derived quality holds.** No candidate execution, generation, admission, second critic or central changes. Zero new original-record coverage. Main owns serial diagnostics and admission.

## Python 0717 — scoped positive

The complete WorkMessage reference validates invalid kinds through comparisons, not hash membership; ordinary [] and {} therefore receive the specified ValueError. Corrected tests include both, plus None/integer controls and separate malformed-field TypeError cases. This is an invalid-kind exception contract, not an invented custom equality domain.

MappingProxyType is now tested for both job and reply. The reply uses accepted=False, then mutates backing id/accepted/extra and a returned fields dictionary; subsequent fields and is_consistent preserve the original reply. Job tests separately mutate nested tags. UserDict, a straightforward Mapping implementation and plain dict controls remain accepted. The reference validates a Mapping, materializes dict(fields), then deep-copies, avoiding direct deepcopy of a noncopyable wrapper.

Tests retain exact job/reply keys, nonempty raw strings (including valid whitespace), priority bounds and bool exclusion, exact boolean accepted, duplicate tags, read-only public properties and fresh nested copies. No concrete Mapping wrapper preservation or private-field manipulation is demanded. Reference is_consistent catches the schema's ordinary TypeError/ValueError failures; no universal promise over hostile custom objects is inferred.

The actual retained mutant changes constructor storage to deepcopy(fields), so the MappingProxy witness distinguishes the held copy-boundary defect. The []/{} cases separately protect the repaired invalid-kind behavior; provenance alone does not qualify either witness.

## Rust 0487 — scoped positive

The complete reference derives Debug, Clone, PartialEq and Eq for Observation, ModelError and ObservationStore. Corrected tests instantiate require_traits<T: Debug + Clone + PartialEq + Eq>() for all three; Eq is therefore genuinely required, not inferred from assert_eq. No Debug text, field labels, private maps, Default or extra trait is asserted.

Tests retain populated clone equality and independent changes in both directions, complete supported-state equality controls, entire-update atomicity, empty update no-creation, existing-model requirement for empty query lists, exact feature-vector matching, query order, i128 sum extremes and truncation toward zero. Required Debug makes these Result unwrap/assert_eq uses legitimate.

The explicit tiny fixture stores outcomes10 and20 on two-feature vectors, then queries one feature and expects15. Mixed nonempty arities are valid under the frozen approved contract; an empty query vector remains EmptyFeatures. The retained mutant adds a query-arity rejection, so the tiny fixture distinguishes an actual semantic defect. No deep/astronomical or runtime-dependent witness is needed.

### Original-parent control must remain separate

The immutable original Rust0487 reference omits the required ObservationStore traits. Proper R20 trait qualification, clone use and equality tests therefore cannot compile against that original control. This is a known original API/trait compile defect, **not a semantic mutant failure** and not evidence that the original passes admission. Do not report that compile failure as successful behavioral discrimination.

The recovered R19/R20 reference and retained mutant both have the required traits. The R20 quality conclusion concerns those exact recovered bytes; main must preserve and disposition the original-control compile evidence separately under its admission rules. This review neither changes those rules nor waives a required control.

## Seven criteria

- Prompt clarity: the existing Python exception/schema rules and approved Rust nonempty-query fallback policy remain unchanged. No new []/{} exception policy or arity policy was invented in R20.
- API consistency: Python properties/schema and Rust public methods/types match their frozen specifications. All explicitly required Rust traits are now test-qualified without representation demands.
- Independent test origin: each archived correction input has exactly id/problem/prior test_code, with the problem and test equal to R19. Corrected output matches emitted test content after prescribed strip-plus-newline normalization. Reference and mutant were not input fields for the test author.
- Non-triviality: Python combines disjoint schemas, Mapping normalization, deep ownership and consistency checks; Rust combines atomic model updates, arity invariants, exact-match/fallback numeric aggregation and independent cloned state. Both complete targets remain substantive.
- Idiomatic code: Python uses Mapping validation with normalized dict copying; Rust uses owned vectors/BTreeMap, prevalidation, i128 accumulation and derived public traits. No additional dependencies or private hacks.
- Dependency isolation: Python standard library/unittest and Rust standard library only. No I/O or network dependency was introduced.
- Realistic known-bad failure: Python direct wrapper deepcopy fails the valid MappingProxy boundary; Rust rejects a valid different-arity query instead of model-wide fallback. These are static predictions tied to concrete tests, not newly executed results.

## Byte preservation, provenance and bindings

Both R20 messages, verification prompt/rendered prompt and complete validation objects exactly equal R19. Reference and known-bad source bytes are therefore unchanged. Each approved feedback previous_candidate_sha256 equals canonical R19. Each emitted test SHA is recomputed and agrees with metadata and archived independent output. Run contract records correction_attempt=1, and both archives returned zero without timeout/disallowed tool items/event parse error. Those archive statuses describe test generation, not candidate execution.

All source fields except the versioned transformation equal their immutable originals; rights equal the all-true original bindings. Sources remain McEval-Instruct revision57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0. Canonical SHA uses sorted compact JSON, ensure_ascii=False and UTF-8. Files reside under datasets/cache/expansion-v1/versioned-recovery/r20/<full ID>.candidate.json.

### exp-v1-recovery-r20-python-generation-0717

- file SHA-256: `a168c38783605db4a09f76308c59d099b3d3d9d86a9eb311cca1c91b666f7901`
- canonical SHA-256: `027f579f61952d4776a2d3d0af749b76a7aa8c94870f0dd9d243b9f2e3366d65`
- previous SHA-256: `b624bad0311feff0e19e0ded806618f78f56d6d6515dfd516c990d7093e1794a`
- original SHA-256: `4432a25372e0cd1ef3da2401dbab9b82886ecdeb5d0a791dbf22d3fb4768e3e4`
- prompt SHA-256: `49701ab781d8b5d856d109aab003eefd3548095d2471b20e8975195434763be5`
- reference SHA-256: `7c76f2a9375c1b67da0e3b45de6a0f1aebb6abab43376c6afcb2e486bcd13eb5`
- test SHA-256: `fdff59c16197dfffd4c692e59ed9332f074c294081f6d441700d877927b5864e`
- mutant SHA-256: `4d7a5924ea9389791e9eae3edf56150c753281cd4df093b610daa4ca5eace301`
- Source record: `row-04048`; SHA-256 `b8192424da7167dcfab7af8b53b2274881ef6bc31f775bd4c07e409ddb958cca`.
- Rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

### exp-v1-recovery-r20-rust-generation-0487

- file SHA-256: `878ae24264ce0f7c38d192729f801181066f17444af0b86f645c328079a21195`
- canonical SHA-256: `d03d883a3daae94487c369bf83a6de5d9141b54a37ae99d8dda98c46e85aae77`
- previous SHA-256: `047f9334346c3c5711dfa3577f23decd78373b5f3e819fb86c98645c40711179`
- original SHA-256: `9ee8d243d8728a71c43c64ab9122fceb8e0db37aabc8e8e1f055ff82fb726ad4`
- prompt SHA-256: `0a5e39e8643655c11636eef891770f507145c632582fb12b94fb7ee405b62db2`
- reference SHA-256: `241b3cf5acdeb01cca500b0e50abadf8179bdaee62128608b46d9a71f570633a`
- test SHA-256: `3a6b2c7a288008acec52dfb24086febf2ecda18684c933fd6281087dddec38b8`
- mutant SHA-256: `90f5aa84e99e7a1c4b4da8a4bb6df028b51ef2b6a3603b5a10970017931c6b85`
- Source record: `row-05991`; SHA-256 `ff9d9a8308576f019c50bec2336ce85b8a7d1ca4ecacc6a08345cf7037ae633a`.
- Rights: `{"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}`.

## Shared evidence hashes

- datasets/cache/expansion-v1/versioned-recovery/r20/python-recovery-test-correction-evidence.json: `852ec388c3f72f16de8fbd5a8f88741100ac6e516d061e65ffd1cb5d98e7ba1c`
- datasets/cache/expansion-v1/versioned-recovery/r20/rust-recovery-test-correction-evidence.json: `673808b7b4bf6e51d1834a391a9a9743126488632b201670d323ea2a57db978d`
- datasets/cache/expansion-v1/versioned-recovery/r20/run-contract.json: `886eb5c9e7ab6f13546d6981b3c334dfc7884fb47748864c6b46734d01f3463d`
- measurement/data/expansion-v1/cutoff-5885-review/recovery-test-feedback-r20.json: `a6d12ffbb09bde23a588eae378dce6a78e0910deae38bedb75cbbd5366e13e55`
- measurement/data/expansion-v1/cutoff-5885-review/recovery-requests-r20.json: `16b1ffa454301fb48e4cc9589ce2912402620eb89e368e2e0c5d6b1bfd6cc2a0`
- measurement/data/expansion-v1/recovery-plans/r20/plan.json: `879eb4184b49e09a171cbe35592096a296d9d2af6e1e52eea68315fb6b7eb224`

