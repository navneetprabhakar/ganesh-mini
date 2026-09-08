# Recovery r6 Rust independent static review — 2026-09-08

## Scope and result

Four derived generation candidates reviewed in full: prompts, references, independent test files, known-bad implementations and approved r6 plan scopes. Current gate is versioned recovery quality review before sandbox verification/admission. Only this report is changed. No execution, generation, cloud use, admission, original-row coverage credit or central ledger change is claimed.

**1 scoped positive (0757); 3 holds (0558, 0704, 0778).** All four retain their parent/source lineage. A static positive still requires the main agent's independently recorded sandbox gates.

Seven criteria are prompt clarity, API consistency, independent test origin, entire-target non-triviality, idiomatic implementation, dependency isolation and realistic known-bad failure. Behavioral/oracle adequacy is assessed as well: independent origin alone does not make a test valid or sufficient.

## Per-candidate findings

| Candidate suffix | Decision | Substantive basis |
|---|---|---|
| 0558 | HOLD — regression test gap | The reference correctly trims a Zone query and returns Invalid for blank input, but the suite never calls Zone with a blank string. Blank AddZone tests exercise another branch. The supplied mutant's blank Zone bug is not distinguished. |
| 0704 | HOLD — zero-area bounded-work defect and missing capacity witness | A supplied test passes a zero-width tile with height usize::MAX. Although the output has zero bytes and valid dimensions, the reference loops once per row, performing usize::MAX zero-byte copies. The actual capacity-overflow correction lacks a decisive test. |
| 0757 | Scoped positive | Two-pass kind validation precedes checked accumulation; the independent test places a kind mismatch after an overflowing matching prefix and expects UnexpectedKind. This directly distinguishes the one-pass mutant without demanding unpromised traits. |
| 0778 | HOLD — unsupported vertical-tab success oracle | The whitespace success fixture includes U+000B. The reference uses Rust ASCII whitespace, which excludes vertical tab. The approved repair requires ASCII record padding, not a new POSIX or Unicode whitespace policy. |

### 0558 — workshop command dispatcher

Prompt/API: the exact public declarations explicitly require Clone, Debug, PartialEq, Eq and Workshop Default. Their use in tests is therefore justified, unlike imposing derives on an unspecified interface. Names are trimmed, empty-after-trim names are invalid, valid absent zones return NotFound, and failed operations must not mutate state.

Reference: the repaired Zone arm trims once and rejects the empty result before lookup. The command-built state behavior remains coherent: BTreeMap summary ordering, per-zone insertion ordering, tool/zone consistency, cascade removal and nonmutation on failed commands. No new policy for externally corrupted public maps is inferred.

Tests: health/summary, trimmed names, insertion order, invalid additions, duplicate/missing operations and cascade behavior are meaningful. However, their blank-name assertion is AddZone, not Zone. No blank Zone query exists, including no Unicode-trim witness. The reference and supplied mutant otherwise share the relevant behavior, so the advertised mutation is not exercised.

Minimal correction requirement: a spec-only independent test must query Zone with empty/space/tab padding and a Rust-trim Unicode blank such as U+2003, expect Invalid, verify unchanged state, and distinguish a nonblank absent zone yielding NotFound. This is a test correction, not a reason to alter the repaired reference.

Seven-criterion judgment: clarity/API/independence/non-triviality/idiom/isolation are supported; the semantic mutant is realistic but the actual regression witness is absent. The entire target is a stateful dispatcher with coordinated collections and transactional failures, not an elementary blank-string patch.

### 0704 — tile atlas

Prompt/API: tile dimensions and pixel counts are checked, errors are ordered, zero dimensions are explicitly valid, and the derived scope adds vector-capacity/fallible-reservation Overflow behavior. The tests match enum variants and unwrap successful Atlas values with their own match helper; they do not require Debug, Clone or equality derives on the public API.

Reference: quotient/remainder row calculation, checked dimensions, the isize::MAX vector bound and try_reserve_exact all address the approved capacity issue. Nonetheless, after allocating zero output bytes, the copy phase still iterates over every y in each tile's height.

The existing test `representable_zero_area_atlases_are_valid_at_dimension_boundaries` supplies `Tile { width: 0, height: usize::MAX, pixels: vec![] }` with one column. All dimensional calculations succeed, and the result should have width zero, height usize::MAX and empty pixels. The copy loop then entails usize::MAX zero-byte copies. This is a concrete source-level bounded-work defect on an explicitly valid, tiny-memory input, not a speculative allocation failure. No timeout execution is claimed.

Minimal reference requirement: after preserving all required validation and checked output dimensions, skip the copy phase for zero-area output (or skip zero-width tiles). Do not return before mandatory dimension-overflow checks.

Tests also omit the decisive approved capacity witness: one valid 1×1 tile with usize::MAX columns must return Overflow promptly rather than overflow a row formula or panic in vec allocation. Existing zero-area dimension tests are useful but do not establish that correction. Keep genuine zero-area tests; do not weaken them to accommodate the loop.

Seven-criterion judgment: clarity/API/independence/non-triviality/dependency isolation supported; checked-arithmetic idiom is partially repaired but bounded empty-output behavior remains defective. The capacity mutant is realistic; suite adequacy remains held. This is interacting geometry, checked arithmetic, validation precedence and allocation behavior, not arithmetic padding.

### 0757 — aggregate readings

Prompt/API: inspect every reading for the first kind mismatch before returning a sum; otherwise checked u128 accumulation produces Overflow when necessary. Empty input gives zero and an empty expected kind is allowed. Tests inspect returned variants/fields without requiring unpromised public traits.

Reference uses a first pass for mismatches and a second pass for checked addition. This correctly returns the first mismatch even after values whose matching prefix would overflow. Owned error fields are produced without modifying the borrowed input.

The decisive independent witness is the equivalent of `[(u128::MAX, "ok"), (1, "ok"), (0, "wrong")]`: expect UnexpectedKind with expected "ok" and found "wrong". The supplied one-pass mutant returns Overflow at the second record instead. Additional tests cover exact maximum, matching overflow, first mismatch, empty kinds, empty input, ownership and stable input.

All seven criteria supported statically. Non-triviality is the validation-priority/numeric-overflow interaction across the complete input, consistent with the approved frozen calibration; no claim is based on patch size or artificially added boilerplate. No oracle defect found. Execution remains the main agent's gate.

### 0778 — record transcoder

The reference now trims ASCII whitespace around the bracket container and each record. It retains strict interior key/value syntax, percent-byte parsing, UTF-8 validation, duplicate rejection, sorted output, canonical escapes and the specified two output forms. These interacting parsing/rendering rules make the target substantive. Tests match error variants directly; no unsupported public derives are demanded.

The success fixture in `bracketed_whitespace_is_accepted_only_around_records_and_container` contains the sequence `a=one%20two \\u{000b}]`. Trimming with char::is_ascii_whitespace leaves U+000B attached to the encoded value; decode consequently returns Malformed. The oracle expects success.

Rust's documented ASCII whitespace is SPACE, HT, LF, FF and CR; it explicitly excludes VT and warns that other definitions differ. [Rust char::is_ascii_whitespace](https://doc.rust-lang.org/std/primitive.char.html#method.is_ascii_whitespace). The unchanged task says ASCII whitespace but does not specify a POSIX six-character expansion. Thus the VT assertion cannot be used to demand a broader reference policy. This is a definite oracle hold, not a mandate for universal Unicode trimming.

Minimal correction: remove VT from the success fixture, retaining independently meaningful HT/LF/CR/FF record/container padding. Those witnesses distinguish the mutant that only trims literal spaces around records. Do not add a VT rejection assertion unless the contract is explicitly clarified; ambiguity is not permission to add another requirement. Ordinary malformed interior whitespace, percent/UTF-8 errors, duplicate keys and normalized rendering tests remain useful.

Seven-criterion judgment: clarity/API/independence/non-triviality/idiom/isolation and the realistic space-only mutant are supported within Rust ASCII semantics; oracle fidelity blocks the current artifact.

## Provenance and exact bindings

All paths below are relative to `datasets/cache/expansion-v1/versioned-recovery/r6/`. SHA-256 was recomputed from exact file/text bytes. Each independent author input task has exactly `id, problem`; all four problem strings match candidate prompts exactly. Independent output test_code strings match each installed test file exactly. Architect output problem/reference_code/known_bad_code strings match all four candidate prompt/reference/mutant strings exactly. No reference or mutant was supplied in the independent task list. Evidence has no disallowed tool-item events.

Architect input SHA-256: `a0c58ac8ca6a0fc83b2be479cf94e3da23eb8e57a7fc7a9bbe63260ec222e014`.
Architect output SHA-256: `fd805430631bf5a4dbeebe59ff6ec9e77f368e6d733a0e041e60ea115e360a82`.
Independent test input SHA-256: `0b8fffd16a35e2255f8eb4386d6e1ff55e9655448b40ef9ce18fc34ad0b375e5`.
Independent test output SHA-256: `a4fcdb245e922ef17f95c647548cb55b62c23e4f5a325e77762548864b611d21`.

- plan.json: `803f0308b33b4b8a834347d5976a148bc66001d6fc8606a1e206fb0e2b4a6795`
- run-contract.json: `b4f970f572157f127481011b99a4c8056776a03f13ecdfb099455b974a183a27`
- rust-recovery-architect-evidence.json: `48b5ac4e87fe520ae4d9118dbe60d8b362f9282e43add4e7b50de60061ce80cb`
- rust-recovery-independent-tests-evidence.json: `0608ab6396fe178f0de726815617bd1e8503ec536c5fb07082c2a42d7671c008`

Approved scope evidence: `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R6_SCOPE_PROVISIONAL_20260908.md`, plan-bound SHA-256 `91666df9bc114362a55cf7fb4a55aa674077c92ec60a35d31577e6d356337790`. The plan's content binding is `0c7d76825c37e2291eb56549277aaa29b44812a6d6b842d2825faf7da69b3295`.

All four carry McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, CC-BY-SA-4.0, source record hashes and parent canonical hashes below, with all five recorded rights flags true. This preserves the approved lineage; it is not a new legal determination.

### exp-v1-recovery-r6-rust-generation-0558

- Candidate file: `exp-v1-recovery-r6-rust-generation-0558.candidate.json`
- File SHA-256: `ac80b042539052a53c9837f156bdf8d876b74b845563650639a5f1819be969fd`
- Prompt: `327b75f4cc99495529ae51b0007dafd9a898819ad735587127af14f1e6edc257`
- Reference: `c062b41d65bd7e1866c3c658dbd2ccfd7381f45826df8c3d99cc614a384dd780`
- Independent tests: `906afc59c6dadee5698dfe2bcf1c514822b99fa1c2bbcf48d3ad3acd7070690b`
- Mutant: `1102f4fb30a4ccb75a80112246414eaf39b5b6c6c5df6a66cf74c05cce805116`
- Parent canonical candidate: `aa56c6090a2bfa2124c29e7066c9d42c995b3c6cd4e026063007dfa8ce6786f5`
- Source row-23825: `e3f1d50c3bf33512a51aad31899bfc92d6f7e0b0d6d418b6b1cbfb7dd1e240de`

### exp-v1-recovery-r6-rust-generation-0704

- Candidate file: `exp-v1-recovery-r6-rust-generation-0704.candidate.json`
- File SHA-256: `aee2aeac9a27df9eaac0833f3fd22d4dabc45656d6dffca636f5004afdd3b31c`
- Prompt: `f2ffd3e0109e427624cc5c3ca16056a0ac7704bb82ec038eb333a1042f24ad74`
- Reference: `1202b96882f5aa9ee3ba5cd0c77589e9e4e0677e54114c00dcb2477e281d57be`
- Independent tests: `b4ea22abc45552aa03d0a7b7f36d077904ef66fe749fc63c6b2aafb7507db20a`
- Mutant: `032a5ddecdb994baf3f53e709a36ef90962db01ff62ecd74dca05a9e90df8c47`
- Parent canonical candidate: `a31e3ea788faae40f14f0db4a78c0354ac049f306ae5ef7757d4084b51f3761d`
- Source row-03222: `a5ca26bf3ea193deadab1d88a5f8aec2527f84ff7ed9cb1a6ad229fbc937130a`

### exp-v1-recovery-r6-rust-generation-0757

- Candidate file: `exp-v1-recovery-r6-rust-generation-0757.candidate.json`
- File SHA-256: `070ba81a71aa97938ed8b683f26e084066e60feef6e405d3f2280f875aa4b3af`
- Prompt: `0cae7a9b90fb212cb21667ac2efd6d70760ddb38cb9f103900953f364d23961b`
- Reference: `3a25d44d83ca8e076f7bbae8cc5ee2d2cadbe826905de3eb6ff7ef631851eeb2`
- Independent tests: `002a84d671a606f25cb41a2dc61f37a726e79469d0fa3945aa5cb1b560fdbc49`
- Mutant: `23c46242f185a0adcfed30ac02dfc0ea2017d9dca4fcd3e9cb654c2cee5a1672`
- Parent canonical candidate: `e4f39e83aa6be47b212b1ef506b86afe040a3222d17d0968decfbf9beaa90e0c`
- Source row-03237: `780529f1e9d418b3d3d121d7cc9c3ab31b8e44d5f40b1825a8aff73d4272c5c6`

### exp-v1-recovery-r6-rust-generation-0778

- Candidate file: `exp-v1-recovery-r6-rust-generation-0778.candidate.json`
- File SHA-256: `baf06e6f390c254dcfab5591242e7c992329b03f23dcdec44d289e2ca03669e7`
- Prompt: `ff9c5303d9b7f7d5721a32bfc450d222b6234f62cd8328a2840b1d088119142e`
- Reference: `e5c2d1bb16d34161a2de45835d2bd196ee4095f2e8b52617da7e3abfb50c362f`
- Independent tests: `2fee2a6440cf263f6676a708e3cda094ae01cb2f9122d318634cd3b59f0d215f`
- Mutant: `28fd769b7714cfa448eb86aec061ce2a6b6d602a368de55eede7532ad16ca989`
- Parent canonical candidate: `e37bd12235442df21853d1913997f065186671d0f5077ab950f00a6b0c44232d`
- Source row-05920: `cfe7fa0ee1917f6fd254bcb710d56ad9ca2a3a3387fc4553ebc098abe4568cc8`


## Handoff

Main may proceed with sandbox diagnostics on unchanged artifacts and preserve failures as evidence. Do not admit the three held artifacts or silently repair their tests/reference during verification. Any correction requires the separately approved versioned workflow and fresh exact bindings. No automatic second correction or expanded review was initiated.
