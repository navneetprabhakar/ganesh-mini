# Recovery r9 Rust static quality review — 2026-09-08

## Scope and disposition

**2 scoped positives; 0 holds:** exp-v1-recovery-r9-rust-generation-0558 and exp-v1-recovery-r9-rust-generation-0778.

Current gate: bounded recovery test correction, before independent sandbox verification and admission. Full corrected prompts, references, tests and known-bad implementations were read. The r9 approved Rust plan scopes and critic context were inspected. Only this report is changed. No candidate execution, generation, cloud action, repeated critic, central-ledger mutation or new original-row coverage is claimed.

Both specifications, references and mutants are byte-for-byte identical to r6. Only the test corrections and versioned metadata changed. This report closes the two r6 test-quality findings, not other candidates' holds or executable admission gates.

## 0558 — scoped positive

The new `malformed_zone_names_and_lookups_are_rejected_atomically` test creates a legitimate workshop through commands, inserts tool IDs 4 then 2, and invokes **Zone itself** with empty, spaces-only, tab-only and U+2003 strings. Every query must return Invalid with the entire workshop unchanged. A padded nonblank absent zone must return NotFound; a padded existing zone returns "4,2".

This is now a direct semantic witness: the unchanged reference trims and detects an empty name before lookup, whereas the known-bad Zone arm looks up the empty string and returns NotFound. No execution result is inferred or reported.

All seven criteria are supported:
- **Clarity/API:** exact public declarations and required derives are given. Tests' Clone, Debug, equality and Default use is explicitly authorized by the prompt.
- **Independent tests:** bounded critic sees only unchanged specification, prior tests and specification-derived feedback; exact bindings checked below.
- **Non-triviality:** complete dispatcher coordinates ordered zone IDs and tool records, duplicate/missing validation, cascading removal and failed-command atomicity. This judgment does not rely on the small repair size.
- **Idiomatic implementation:** exhaustive command matching, borrowed trimmed strings, BTreeMap ordering and owned outputs implement the declared command-built-state behavior.
- **Dependency isolation:** standard library only, no filesystem/network/external dependency.
- **Realistic known-bad:** malformed lookup incorrectly classified as missing; now meaningfully distinguished by the test.

The full suite retains sorted summaries, normalized stored names, case sensitivity, u64 boundary IDs, insertion order, duplicate/missing commands and cascade behavior. It does not corrupt public maps into an unspecified state. No unsupported oracle requirement or remaining correction gap found.

## 0778 — scoped positive

The corrected `bracketed_ascii_whitespace_is_accepted_around_records_and_container` fixture places SPACE, HT, LF, CR and FF around **each record**, the comma boundaries, and the outer container. It expects sorted canonical Lines output `a=one%20two\nb=x\n`. U+000B is removed; neither its acceptance nor rejection is asserted.

The unchanged reference trims the permitted ASCII set at each boundary. The known-bad implementation trims literal spaces only inside brackets, leaving record-leading HT/LF/CR/FF, so its key parsing rejects a valid record. This is a genuine in-record-padding witness, not merely outer-container whitespace that both implementations already handle.

All seven criteria are supported:
- **Clarity/API:** declared formats/errors/function signature and grammar remain unchanged. Tests match variants and unwrap through match helpers, imposing no unpromised Debug, Clone, Copy or equality traits.
- **Independent tests:** exact spec/tests/feedback-only critic lineage verified.
- **Non-triviality:** two grammars, byte percent encoding, UTF-8 validation, duplicate detection, sorting and canonical rendering interact across the whole target.
- **Idiomatic implementation:** checked percent pairs, byte-level allowed characters, String UTF-8 validation and owned output implement the stated behavior.
- **Dependency isolation:** standard-library-only in-memory implementation.
- **Realistic known-bad:** valid ASCII record padding incorrectly rejected; new fixture distinguishes it without expanding the contract.

Remaining tests preserve malformed interior whitespace, malformed Lines/CR/blank records, key restrictions, bad escapes, invalid UTF-8, duplicate keys, case sensitivity, canonical escapes, compact/noncompact rendering and stability. The prior skipped empty-Bracketed string was removed from a malformed-input loop without adding a new rule. No universal Unicode whitespace policy is introduced.

## Provenance and immutable bindings

Paths below are relative to `datasets/cache/expansion-v1/versioned-recovery/`.

The critic input has exactly `id, problem, test_code` for each Rust item, plus specification-derived feedback. Each input problem and proposed test is exactly the r6 artifact; each returned test_code is exactly the installed r9 test. Neither reference nor mutant code appears in the supplied item schema/context. The recorded run has correction_attempt 1, returncode 0, timed_out false, and no disallowed tool-item events. These are teacher-provenance facts, not candidate execution evidence.

Recomputed input/output hashes match evidence declarations:
- r9/rust-recovery-test-correction-evidence.json: `3939c03358a15d65abed93b428f73b91c79e21a31c724ea9e73a4332284b9b3f`
- Critic input: `786a235a70e527068e41b44175a27a5475c6bc2a014ccf295732901eb5c82127`
- Critic output: `3d7e9d8fe8ab57cd6276b011b04a8cd8d2fe2be263ac43890d574c049f350e7a`
- r9/plan.json file: `0f0d6e653bbabff308a912cc764d1373b20faf3f4cf68a4c7341c94f36b5ae79`
- r9/run-contract.json file: `adf45a76bade2ad56f6b0bb9a1c7be19a9292dc6c527c50667d5d559cf2991b3`
- Plan content binding: `4b9e973fae402fab5d6bf1db89ea2430e60807d343cb453ab22b2e97924fd63f`

Both plan records bind `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R6_RUST_REVIEW_20260908.md` at SHA-256 `e3eac3970bd506d649ae71735930075124cbe92ba84bc76a3248dbfb2dfa73b8`. Prior candidate-file hashes were recomputed and match the r9 run contract.

### exp-v1-recovery-r9-rust-generation-0558

- r9 candidate file: `r9/exp-v1-recovery-r9-rust-generation-0558.candidate.json`
- Candidate file SHA-256: `89caecbeb6ba209e714dfe63377c11c712208ee32192efc60a7347d500807ecd`
- Prior r6 candidate file SHA-256: `ac80b042539052a53c9837f156bdf8d876b74b845563650639a5f1819be969fd`
- Unchanged prompt: `327b75f4cc99495529ae51b0007dafd9a898819ad735587127af14f1e6edc257`
- Unchanged reference: `c062b41d65bd7e1866c3c658dbd2ccfd7381f45826df8c3d99cc614a384dd780`
- Unchanged mutant: `1102f4fb30a4ccb75a80112246414eaf39b5b6c6c5df6a66cf74c05cce805116`
- Corrected independent test: `12ed5b670e9a383f3ae3f47552d60af484cc2fdc362c8367ce18426e3a7bee9c`
- Original parent canonical candidate: `aa56c6090a2bfa2124c29e7066c9d42c995b3c6cd4e026063007dfa8ce6786f5`
- Source row-23825: `e3f1d50c3bf33512a51aad31899bfc92d6f7e0b0d6d418b6b1cbfb7dd1e240de`

### exp-v1-recovery-r9-rust-generation-0778

- r9 candidate file: `r9/exp-v1-recovery-r9-rust-generation-0778.candidate.json`
- Candidate file SHA-256: `ddc1068e83bfec30dabf0429e42f5ed870a974be7b0e6b1060b8ac1b4058b023`
- Prior r6 candidate file SHA-256: `baf06e6f390c254dcfab5591242e7c992329b03f23dcdec44d289e2ca03669e7`
- Unchanged prompt: `ff9c5303d9b7f7d5721a32bfc450d222b6234f62cd8328a2840b1d088119142e`
- Unchanged reference: `e5c2d1bb16d34161a2de45835d2bd196ee4095f2e8b52617da7e3abfb50c362f`
- Unchanged mutant: `28fd769b7714cfa448eb86aec061ce2a6b6d602a368de55eede7532ad16ca989`
- Corrected independent test: `acbc7d55a39bed48ca23cbc7a20e366745aa18705dbf51473da84bd84a4bb05a`
- Original parent canonical candidate: `e37bd12235442df21853d1913997f065186671d0f5077ab950f00a6b0c44232d`
- Source row-05920: `cfe7fa0ee1917f6fd254bcb710d56ad9ca2a3a3387fc4553ebc098abe4568cc8`


Source binding remains McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, CC-BY-SA-4.0, with all five recorded rights flags true. Existing rights decisions are preserved, not reopened.

## Handoff

Both are suitable for the main agent's serial sandbox diagnostics on these exact artifacts. Static positives are not admission: reference pass, genuine semantic mutant failure, evaluation separation, deduplication, corpus composition and a fresh admission seal remain required. If executable checks fail, preserve evidence and retain exclusion; no additional automatic critic loop is authorized by this report.

