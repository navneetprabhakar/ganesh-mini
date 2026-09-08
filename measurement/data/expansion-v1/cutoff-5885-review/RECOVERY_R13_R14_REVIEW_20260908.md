# R13/R14 independent repair quality review — 2026-09-08

Gate 2; exactly three derived repairs. **One scoped static positive, two test-oracle holds.** No candidate execution, admission, generation, central mutation or new original coverage. Full originals and current derived problems/references/tests/mutants read; approved R11/R13/R14 scopes reconciled. Main owns actual sandbox and admission decisions.

## R13 Rust repair0361 — scoped positive

Exact R11 specification, reference and mutant bytes are preserved. The 64-bit usize domain and maintained remainder imply representable quotient; u128 elapsed-plus-remainder computes exact arithmetic without saturation. Bulk per-axis movement remains equivalent to repeated clamped steps, opposing directions cancel, zero elapsed preserves maintained state, and constructor error order and shown traits are retained. Whole target is time/state interaction, not elementary patch padding.

The correction adds assert_bounded_exact_time_carry: fresh 1x1 grid, interval u64::MAX, elapsed MAX-1/MAX/1 gives 0/1/1 and stationary coordinates, followed by zero elapsed giving zero. The saturation mutant instead yields 0/1/0 after at most one loop in each call. Both mathematical_sum_survives_u64_overflow_boundary and maximum_representable_step_count_is_returned_without_a_huge_loop invoke this helper inside their own test function before any enormous-work call. No reliance on test order or cross-test state; on the supplied mutant the bounded assertion prevents reaching either huge call even with parallel test scheduling.

Large valid tests remain rather than weakening the declared bulk-work contract. Existing partial/exact/zero interval, independent-axis cancellation, all-edge clamping, constructor order and borrowed input tests remain valid. No new traits, private-coordinate injection, timing assertion or expected panic. Seven criteria scoped-positive: clear API, independent correction provenance, substantive target, idiomatic standard library, dependency isolation and now a real bounded defect witness. This is static reasoning, not a reported runtime pass.

## R14 Python repair0138 — hold: unsupported custom-number oracle

Fresh architecture returns the exact r14 ID. Corrected reference preserves accepted-only filtering and full event schema/Mapping handling, removes lossy float conversion for exact Real values, rejects bool and ordinary nonfinite floats, and adds totals in native accepted-event order from integer zero. Exact integers and Fraction remain exact; native mixed Fraction/float OverflowError propagates, while finite float inputs may yield infinity. These are the approved contracts, not universal custom-number guarantees.

The accepted 10**500 fixture directly distinguishes the retained float-conversion mutant. Ordinary Fraction, MappingProxy/UserDict, ordering/count, finite-float infinity, native mixed-operation error, rejected nonfinite events and fresh-result controls are substantively useful. The original accepted-only objective is already fixed in the embedded mutant.

Blocking oracle: test_every_event_is_validated_before_aggregation introduces ExplodingFloat(float) whose __radd__ raises ArithmeticError, then supplies a later rejected event with empty category and requires ValueError. The public wording requires all events validated before any result is produced, not before every internal numeric operation; it explicitly disallows special custom-number behavior. A one-pass accumulator that raises the native numeric error and returns no partial result need not prioritize the later validation error. The embedded implementation happens to prevalidate, but its two-phase layout is not a new public custom-number error-precedence rule. Remove this custom probe; retain the ordinary late malformed rejected-event test. Do not alter the reference or contract to satisfy it.

Approved selection also requested integer cancellation and rejected huge values, which are not present; add them during a bounded test-only correction. Their absence alone does not erase the already decisive huge accepted-integer witness. No other concrete static reference defect found within the stated ordinary integer/Fraction/float domain. Clarity/API, whole-target numeric validation/ordered grouping, idiom, isolation, origin and realistic mutant are supported, but valid-oracle criterion blocks promotion.

## R14 Rust repair0102 — hold: VT oracle contradicts named predicate

Fresh architecture uses trim_matches(|c: char| c.is_ascii_whitespace()), fixing the prior method-item signature problem without changing the named predicate. Exact-one .git stripping, last slash/colon component, trailing slash removal, qualified branch/tag identities, stable category deduplication and shown traits are preserved. Embedded mutant retains only Unicode trim after the prior suffix correction.

The U+2003-prefix/suffix fixtures genuinely distinguish the overbroad trim defect. Common remotes, operation ordering, exactly-one suffix, immutable borrowed text and stable RepoPlan output tests are justified. Target remains substantive parsing/normalization/deduplication and uses standard library only.

Blocking oracle: qualified_ref_rejects_unknown_kinds_and_malformed_names includes U+000B vertical tab among characters that must be rejected. Rust char::is_ascii_whitespace is the named predicate and excludes VT; its whitespace set is HT/LF/FF/CR/space. Thus qualified_ref("branch","left\\u{000b}right") is permitted by the declared rule and produces a mapping, not None. Remove VT from the rejection loop (or test predicate-consistent acceptance); retain FF and other named whitespace. Do not broaden the reference predicate to satisfy the invalid test. This is a concrete oracle conflict, not a new policy choice. Seven-criterion reference/API/origin/nontriviality/idiom/isolation/realistic witness are otherwise supported; test validity prevents positive disposition.

## Source, rights and author integrity

All three original canonical hashes match approved plans; original source and rights match plan parent objects. Derived sources preserve every original source field except appended versioned lineage; rights remain unchanged with all five flags true. Embedded complete known-bad source is byte-identical to supplied mutant in all three.

R13 critic receives exactly id/problem/prior-test objects plus approved specification-review feedback, with the prior tests matching R11; its output becomes current tests after terminal-newline normalization. R13 contract records correction_attempt=1 and exact prior candidate binding; no repeated correction is requested here.

Both R14 lanes have separate fresh architect and independent-author artifacts with exact single r14 IDs. Architect problem/reference/mutant matches current fields; independent tasks contain only id/problem and exact current specification. Emitted tests match author test_code after terminal-newline normalization. Five prompt/final-output hashes recompute correctly; all five calls returncode=0, timed_out=false, no disallowed tool items.

Repair provenance caveat: both independent-author boilerplate and critic preamble say no known-bad implementation was seen. That generic sentence is inaccurate because these repair specifications embed broken source. Actual evidence establishes no separate corrected-reference exposure, not blindness to the embedded repair input. This is permitted by scope, not reference leakage.

Python source is m-a-p/MdEval-Instruct (MIT), not the Rust McEval source. Preserve distinct source/license/revision bindings below; no new rights assessment or public release decision is made.

## Exact bindings

Hashes are SHA-256. Canonical candidate/parent hashes use sorted compact UTF-8 JSON; content hashes use exact emitted text; file hashes use raw bytes.

### exp-v1-recovery-r13-rust-repair-0361

- file: `datasets/cache/expansion-v1/versioned-recovery/r13/exp-v1-recovery-r13-rust-repair-0361.candidate.json`
- file_sha: `1282581a81e3bd64690d6aa96e71c55c394694ecc6e59b7f1ce40a7e22d2d74e`
- canonical: `685e8a0c213527dd0fbcd734c866520b5aad18bcd16c60d3feedb684a9fb05d9`
- parent: `7f4a1f8b5996c876c97df3b662c4198b0e58ea0420b219abf391399d3a6aa015`
- prompt: `d34bfd43761720379a766fb3ee60f19bf3e4a3d2b147143d993024af3d1f28c0`
- reference: `ed316859966eeb6b8bffebea10cd9607a14bb387ca3ae3177a5ea2046e274e40`
- mutant: `3b87f6a3c1e515e6cf3e568016625dd897a0f497cdbca8ad311b08e7afaf6d78`
- test: `6ec8e6213b47f9faf6ef5a3b6d1b6e72a36d61b3f127356ed4d91d5c0261be49`

Source binding:

```json
{
  "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
  "license": "CC-BY-SA-4.0",
  "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
  "record_id": "row-23923",
  "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
  "source_record_sha256": "69e904572e01dba6a53d62c34aff15a6a7af7dbbc934bdf50c1b14464c7a80db",
  "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r13-rust-repair-0361 from exp-v1-rust-repair-0361 sha256=7f4a1f8b5996c876c97df3b662c4198b0e58ea0420b219abf391399d3a6aa015",
  "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
}
```

### exp-v1-recovery-r14-python-repair-0138

- file: `datasets/cache/expansion-v1/versioned-recovery/r14/exp-v1-recovery-r14-python-repair-0138.candidate.json`
- file_sha: `df73ba067c0cd39243867b525c75cd84ca0510b802d767a706fa6bb7f2f61dda`
- canonical: `d510f25bd5b259f24dcb32ad719a010f970fc8af350827526df2407b5fc926a9`
- parent: `097e1648410b0391b52875d213ea6a982c8d3418fe08bfd48153bf2c6da17c72`
- prompt: `3e9530f8fdd09d0ac73827fa5fa1987318f9efc6674002ebfa0934b0c1c16200`
- reference: `a343644ad08e3f93bd8f4a1e0f3f6af06a69ce2e46eedb388e4d474fa520a197`
- mutant: `73863c0d4a7512b23d97468999075f0f08ec352f543d9d5d24f5790d94919779`
- test: `0613b34b8f02ae09bfda5c362d6c55b7ab6fbfe7a8166cddef722a1ab8cbcb3c`

Source binding:

```json
{
  "dataset": "m-a-p/MdEval-Instruct",
  "license": "MIT",
  "license_uri": "https://opensource.org/license/mit/",
  "record_id": "row-01990",
  "revision": "38c9197e3add996fae624eb198ebd06155b2101e",
  "source_record_sha256": "73599e4b3e0df122a094495051835c773da202b671b7dc60365f75a9854362de",
  "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r14-python-repair-0138 from exp-v1-python-repair-0138 sha256=097e1648410b0391b52875d213ea6a982c8d3418fe08bfd48153bf2c6da17c72",
  "uri": "https://huggingface.co/datasets/m-a-p/MdEval-Instruct"
}
```

### exp-v1-recovery-r14-rust-repair-0102

- file: `datasets/cache/expansion-v1/versioned-recovery/r14/exp-v1-recovery-r14-rust-repair-0102.candidate.json`
- file_sha: `d2e12a454017a0a5fcf3dc40254828c49270ac6e87a17e48376cc710980a86c6`
- canonical: `4d58a05badc57e8b8cc24efec7263633d26e7eed2c88814c063455cb783a93ef`
- parent: `8c2b016284660327c9d77e34b6ccf76585bcaf4e147c761ef4d9bfe7d4a923f0`
- prompt: `43d8a017a339391d2af9944a758a6b8aee68964c2c4b7a6f6bcbc3e4fa32fce4`
- reference: `29be4e94463fd7b8c1aa670cb7c750e6db3d93cd71aaaab0412d6ccd61bf54b2`
- mutant: `6b2ec40b5b9a4653c04112c1490efe0704952f24c0bede3e1b95de727ea94637`
- test: `9475e5f31c7434341a514db945ccfcf5405e8c3ba0e86f3d8ba8a4d6cd9f54ae`

Source binding:

```json
{
  "dataset": "Multilingual-Multimodal-NLP/McEval-Instruct",
  "license": "CC-BY-SA-4.0",
  "license_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
  "record_id": "row-03276",
  "revision": "57bd46727e49ac3e2890218a146d35c2454a8496",
  "source_record_sha256": "d11d77577758ac7332e12deb503c8cf60f1257cbd1c6e0fe66cc774fe35152b2",
  "transformation": "Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r14-rust-repair-0102 from exp-v1-rust-repair-0102 sha256=8c2b016284660327c9d77e34b6ccf76585bcaf4e147c761ef4d9bfe7d4a923f0",
  "uri": "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
}
```

## Author and plan files

- datasets/cache/expansion-v1/versioned-recovery/r13/rust-recovery-test-correction-evidence.json: `5c5d51c6a02b8340f53a752b06107a2b985bb2968ee94b9e5bcd9fd8715dd702`; prompt `90347c93ccd5afff4dcbb99f33c0fac019a013177679f58039a01c91a088693c`; final output `521acc0ad5321500aab571e28a0647e549740110bf6304d58435d9bc337354b2`.
- datasets/cache/expansion-v1/versioned-recovery/r14/python-recovery-architect-evidence.json: `d89d2685b3e4a1b72b414c5773bf3d4635f3cee22e3814ac084bb5d1cd71360a`; prompt `3213021c6c10742d6067457b5bab2e5fa30c4becf6ea11467fa76a56b594183c`; final output `711e7cc7a5888eced3b45a36c3681ac7d6856736c66734baf2b6f8bdd6a01c47`.
- datasets/cache/expansion-v1/versioned-recovery/r14/python-recovery-independent-tests-evidence.json: `82c41e8a4ee3415cb24025650795c1bcf39d638b1c47399a344a2c9b151f2e12`; prompt `d668e9fc501fd8c2a68c579c889740e09c4cabbe9f0d0dcd4a796cdeb0180ef8`; final output `3eea3fbf74f18c056d78e71c2f9f891456417492a1442f3126c9b057c0fdb063`.
- datasets/cache/expansion-v1/versioned-recovery/r14/rust-recovery-architect-evidence.json: `b329797a1dbd422bddf53e6245f1b8f60d92f1d04f757d96b92863f6ca1d40b8`; prompt `555591bb76d6992b4461cf04cbb638a4ee4e9ede966f5376cca65d6a04ade96a`; final output `97a43914bf01ff859cd28702f12bb36bc45bfd323748505604808065ddfb8a71`.
- datasets/cache/expansion-v1/versioned-recovery/r14/rust-recovery-independent-tests-evidence.json: `0efddf68244ea527ee0991c07a57db67b1a8a0b5e13a4756cc0a2181d6ee7b52`; prompt `cf02d832d2337d226406be08aa2c6d15f2c31fb54f104661813b8970cee552bf`; final output `4c05e946f4382ca6b6132ec0b40f09f72c2ba821ccb1653bd7dc59304e4841a2`.
- datasets/cache/expansion-v1/versioned-recovery/r11/plan.json: `2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6`.
- datasets/cache/expansion-v1/versioned-recovery/r13/plan.json: `dead1489bb779934327bf3c8786d89c65b7604832829fa17129ea41ff1773217`.
- datasets/cache/expansion-v1/versioned-recovery/r13/run-contract.json: `b2a3c7756d99b5f75716ef57571cd4ca07fbd146fba13d26bd1e835b49e854db`.
- datasets/cache/expansion-v1/versioned-recovery/r14/plan.json: `2d59789fea811ba7ebe844564ee4dc66569fe4719067dea6d6a1524b049ea51f`.
- datasets/cache/expansion-v1/versioned-recovery/r14/run-contract.json: `a0b4a39242bee4710967f7d01a0d6031bf4a81401f3aca98bcab09c80b80c6a8`.

