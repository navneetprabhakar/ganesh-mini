# Provisional Python/Rust repair recovery scope — 2026-09-08

Gate 2 selection only: exactly one Python and five Rust repairs from the already reviewed seventeen-parent proposal. Full current parent prompts/embedded faulty sources and references were rechecked for minimal coherence; this is not a new original sweep. No version reserved, candidate generated/executed, cloud used, original hold removed or admission claimed. Main must validate and approve before launch.

## Repair-specific contract boundary

All six selections use **contract-clarification**, not reference-fix. The derived repair prompt may replace the complete embedded known-bad source and corresponding repair description to isolate one current realistic defect. The original corrected objectives and public APIs remain required. Derived embedded code must exactly match its known_bad_code. A byte-for-byte original-problem guard would contradict this authorized repair transformation and must not be applied; immutable original parents remain archived with their hashes.

Fresh independent tests must receive only the derived specification and complete embedded faulty repair source inherent in that specification, never the reference or original tests. That repair-task visibility is not a generation-task claim that the author has never seen faulty code. Preserve origin evidence honestly. Required Rust traits are those already shown in the public contract; no new Debug/equality/private-field requirement may be inferred for test convenience.

## Proposed exact scopes

### exp-v1-python-repair-0138

Preserve aggregate_metrics API, exact event schema, validation of all events including rejected rows, accepted-only count/sum, first-accepted category order and fresh outputs. Clarify that finite exact integer/rational Real values are not converted to float for validation; bool is excluded and ordinary nonfinite floats are invalid. Totals start from integer zero and use native numeric addition in accepted-event order. Arbitrary-precision integer and standard Fraction totals remain exact; native mixed-operation OverflowError propagates without reclassification as malformed input, and finite float inputs may produce native infinity without an extra output-finiteness rule. No input mutation or partial returned result on failure. Embed complete faulty code with accepted-only predicate already corrected and only the realistic lossy finiteness-validation defect retained. Tests must include accepted 10**500, integer cancellation, Fraction controls, rejected huge values, later malformed rejected events, order/count and independent outputs. Do not narrow Mapping classes, cap integers, change global digit limits or invent custom-number exception behavior.

- Parent canonical SHA256: `097e1648410b0391b52875d213ea6a982c8d3418fe08bfd48153bf2c6da17c72`.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/SEVEN_CRITERIA_PYTHON.md`, SHA256 `5760e665691c09509d0cf198bbbabc4447e35bc8da86306c6f5454992965173d`.
- Source: m-a-p/MdEval-Instruct revision `38c9197e3add996fae624eb198ebd06155b2101e`, record `row-01990`, source SHA256 `73599e4b3e0df122a094495051835c773da202b671b7dc60365f75a9854362de`, license MIT.

### exp-v1-rust-repair-0343

Preserve extract_action_label, exact restricted markup grammar, case-sensitive first action-label selection, Some(empty) for empty matching value and full-input validation after a match. Reject a forbidden closing bracket in either extracted kind or value; allow all otherwise permitted UTF-8/newlines without a new ASCII-only domain. Embed complete faulty code with the original action-label selection bug already corrected and only the omitted forbidden-bracket validation retained. Tests must include a forbidden bracket in a matching value, forbidden kind after an earlier valid match, valid-first then malformed suffix, empty matching value, nonmatching records and ordinary Unicode text. No early return after finding an answer.

- Parent canonical SHA256: `c9dd3f8da96f17de8beb02fa7caa4db8b37bcc8ac5310049ba80d78352dc61dc`.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_21.md`, SHA256 `079207144cccdb572f633febe23b60ed2a9c26bb42e395fb6cd124da2a1d038d`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-23662`, source SHA256 `69f046905718618b53c19cc17341846b06ede647a6a851c5dbf0d7922941a78a`, license CC-BY-SA-4.0.

### exp-v1-rust-repair-0361

Preserve FixedGrid/HeldInput/GridError public API, required existing traits, constructor error order step then width then height, exclusive width/height bounds, opposing-direction cancellation, exact-interval steps and carried remainder. Explicitly target the pinned 64-bit usize runtime. Compute mathematical elapsed-plus-remainder without u64 saturation loss; step quotient and remainder must be exact. Bulk clamped movement may replace per-step iteration but must match repeated steps under the same held input, including independent axes and zero elapsed. Embed complete faulty code with >= interval behavior already fixed and only saturating time accumulation retained. Tiny decisive test: 1x1 grid, step u64::MAX, elapsed sequence MAX-1, MAX, 1 returns 0,1,1. Preserve partial/exact/zero intervals and validation controls. No huge loop/allocated grid is needed; do not mutate public coordinates into unspecified malformed state or promise 32-bit return representability.

- Parent canonical SHA256: `7f4a1f8b5996c876c97df3b662c4198b0e58ea0420b219abf391399d3a6aa015`.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_22.md`, SHA256 `556d8b77f2081976d98289781c3be970575497703a7b708d57d782761d3ee8ad`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-23923`, source SHA256 `69e904572e01dba6a53d62c34aff15a6a7af7dbbc934bdf50c1b14464c7a80db`, license CC-BY-SA-4.0.

### exp-v1-rust-repair-0113

Preserve FocusRing and UiState public APIs and shown traits, empty index zero, safe next/previous wrapping, set_len clamp/reset and independent page/overlay/focus changes. Use overflow-safe previous decrement with zero-to-last wrap; retain already-correct next behavior rather than restoring the original len-1 divisor bug. Embed complete faulty code whose only current defect is previous arithmetic overflowing for a large logical ring. Test usize::MAX ring after next then previous, zero previous to last, empty/singleton, shrink/grow and UI isolation. Logical lengths require no allocation; no private-field injection or new collection-size cap.

- Parent canonical SHA256: `942bc20053c7f88bad642fef157e0cc411dd89b5b27ad9f5479166fe70e921f7`.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_7.md`, SHA256 `f59c4574805967e005972ce8dfb22631d84d718b697fac03246865e592422e60`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-06274`, source SHA256 `8fcbdea35247717fcc566870d4b776765c99c868dff6533147fe2d90cf04f6fb`, license CC-BY-SA-4.0.

### exp-v1-rust-repair-0102

Preserve qualified_ref, project_slug and RepoPlan APIs and existing traits. Define surrounding ASCII whitespace by Rust char::is_ascii_whitespace for consistency with the original predicate; do not broaden to general Unicode whitespace. Keep exactly one .git suffix removal already corrected, final slash/colon component selection, trailing slash removal, and stable primary/supporting/tag deduplication with branch/tag identities distinct. Embed complete faulty code retaining only project_slug's overbroad Unicode trim defect. Test U+2003-prefixed/suffixed slug components remain exact, ASCII HT/LF/CR/FF/space padding is removed, repo.git.git yields repo.git, malformed refs skipped and stable category order. Do not introduce URL parsing, escaping, or a new VT acceptance/rejection rule beyond the explicitly named Rust predicate.

- Parent canonical SHA256: `8c2b016284660327c9d77e34b6ccf76585bcaf4e147c761ef4d9bfe7d4a923f0`.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_7.md`, SHA256 `f59c4574805967e005972ce8dfb22631d84d718b697fac03246865e592422e60`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-03276`, source SHA256 `d11d77577758ac7332e12deb503c8cf60f1257cbd1c6e0fe66cc774fe35152b2`, license CC-BY-SA-4.0.

### exp-v1-rust-repair-0095

Preserve IdentityBook/Identity/Permission/IdentityError APIs and only their already shown trait requirements. Explicitly state public Default and new both construct an empty book whose first successful ID is 1. Implement coherent default initialization while retaining the corrected same-entry address AND secret authentication, case sensitivity, nonempty credential rules, success-only sequential IDs and observer nonmutation. Embed complete faulty code retaining correct authentication but the derived zero-initialized Default defect. Tests must compare new/default first IDs, invalid/duplicate additions not consuming IDs, independent books, wrong address/secret combinations and permission/length/empty observers. Do not add public error variants or inaccessible lifetime-exhaustion/private-layout requirements.

- Parent canonical SHA256: `1f0349892f99919906a6a1150d189fdeb1404b3d04dc11a6db486c2478f36ad7`.
- Hold evidence: `measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_6.md`, SHA256 `2e5a33cf86973a29052f686083002293dc924375abc0a129ffa7d02f570c296f`.
- Source: Multilingual-Multimodal-NLP/McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-23720`, source SHA256 `d8d862ca93eac78348575794a692db1cab7dfeca2f6ee7eba370ca9c88656da8`, license CC-BY-SA-4.0.

## Integrity and next boundary

The companion `recovery-repair-py-rust-PROVISIONAL.json` contains only a selections object (no version reservation), with complete original source, rights and hold objects, parent canonical hashes, hold-evidence hashes and exact rationale. All six parents remain held. Each has prompt/answer/tests/model_training/redistribution rights true; Python0138 uses the already authorized MIT MdEval source, the five Rust parents use the authorized CC-BY-SA-4.0 McEval source. No ownership decision is reopened.

Original corpus SHA256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`. Current additive-hold file SHA256 at binding: `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`. Prior seventeen-parent proposal SHA256: `20f3a799b68be2c6d5453977aa2f9ca6634d08628092d80f557af0cf4f44c632`.

Python0138's native mixed-numeric arithmetic policy is an explicit derived choice, not a retroactive assertion about the parent. Rust0361's exact quotient fits 64-bit usize because the carried remainder is less than the positive interval; the elapsed-plus-remainder intermediate requires wider arithmetic. Its maximum-interval witness requires only zero/one logical steps, not enormous work. Rust0113's logical maximum ring allocates no collection. Rust0102 explicitly names Rust's ASCII predicate to avoid repeating the VT ambiguity from another recovery; this does not authorize universal Unicode normalization. These are narrow coherence decisions, not weakened numeric gates.

All six complete targets preserve their original interactions: validation/order/aggregation, grammar/full-input validation, time-carry/clamped motion, ring/UI state isolation, slug/ref ordering, and insertion/authentication/default invariants. No elementary padding is added. Main should check generated prompt/code consistency and require independent oracle review plus resource-limited network-disabled sandbox evidence before any admission. This proposal authorizes no automatic repeated critic loop.
