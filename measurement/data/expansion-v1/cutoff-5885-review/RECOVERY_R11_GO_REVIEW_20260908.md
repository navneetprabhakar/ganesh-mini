# R11 Go0386 independent static review — 2026-09-08

**Decision: STATIC POSITIVE**, subject to main's actual sandbox reference/control verification and admission. Full derived problem, reference, complete test/support files and mutant were read against the fully read original record and approved scope note/plan. No candidate execution, new selection, central edit or new original-row coverage credit.

## Scope and implementation

The derived prompt freezes decoded case-sensitive member names, exactly-once root/item members, escaped-name equivalence and object-local duplicate scope. It also spells out the approved preserved native-int, name, date, whitespace and zero-error-result semantics. The plan's prose requested inserting only the clarification paragraph; the architect additionally restated those already approved preserved semantics and lightly edited introductory/output wording. This is not byte-identical minimal insertion, but no substantive unapproved API/domain change was found. It is correctly classified contract-clarification, not reference-fix; original duplicate policy is not retroactively declared settled.

Reference uses streaming delimiters/member tokens and per-object seen-name sets, so multiplicity is checked before it can be collapsed into a map. Member tokens are JSON-decoded strings, making literal and escaped equivalent spellings compare equally. Exact switches reject case variants and unknown keys at both levels. Per-page ID uniqueness is independent of each item's member set.

Scalar RawMessage decoding explicitly rejects null and unmarshals into int/string, preserving native int token/range rules rather than float conversion. Items are initialized nonnil, returned in array order, and names are retained without trimming. Date parsing and format round-trip match the approved contract. Top-level wrapper returns exactly zero ReleasePage on every subordinate or trailing-value error. JSON decoding owns resulting strings rather than retaining caller byte storage. No concrete new reference defect found statically.

## Tests and control qualification

The supplied control `accepts_repeated_object_members` removes root/item seen-member rejection while retaining case-sensitive keys, scalar validation, ID uniqueness and date handling. This is one coherent duplicate-acceptance bug class across both object levels.

Valid decisive witnesses include equal duplicate root `items` arrays, equal duplicate cursors, repeated item `id`, `name` and `published`, and literal/escaped duplicate pairs. For example, `{"items":[],"items":[],"next_cursor":0}` is valid JSON but forbidden by the clarified exactly-once rule; the control would accept it while the test requires error and zero page. This is a semantic witness, not a compile/invalid-oracle failure claim. Null-first duplicate cases are less discriminating because scalar validation alone rejects them, but the independent equal-valued cases establish the distinction.

Tests also directly reject the original case-folded root/item names, accept sole escaped names, allow member reordering and surrounding JSON whitespace, verify local duplicate scope versus page-wide duplicate numeric IDs, preserve whitespace/control names, exercise native MaxInt and overflow with tiny input, reject decimal/exponent/quoted/boolean numbers, retain negative-zero cursor, and check malformed/trailing/null/unknown inputs. Date oracles follow the explicitly frozen time.Parse/roundtrip contract. Input mutation and late-error zero result are exercised. No unsupported error subtype/message, map layout, raw escape spelling or extra input restriction found.

The test's valid date set starts at0001 rather than0000; it does not reject0000 or claim a narrowed year range. Reference retains the specified time.Parse behavior. Exhaustive date coverage is not required to close this precise correction. A redundant TrimSpace assertion on the literal name stable does not impose normalization because independent whitespace-name tests require exact content.

## Seven criteria

1. **Clarity:** duplicate policy and decoded-key comparison are explicit; int/date/name and error rules are bounded and coherent. No unresolved contract decision remains for this scoped recovery.
2. **API consistency:** original exported types/function and standard package remain; reference implements the clarified member policy and all preserved behavior.
3. **Independent tests / valid oracle:** separate specification-only authoring is bound below; complete tests contain valid direct defect witnesses and no found unsupported oracle.
4. **Nontriviality:** nested strict parsing, member multiplicity, numeric/date validation, identity, ordering and error rollback interact; this is not elementary padding.
5. **Idiom:** standard JSON decoder tokens plus typed scalar decoding and local validation state fit the task. No unnecessary dependencies or unsafe storage reuse.
6. **Isolation:** Go1.22 support module and standard-library tests/reference only; no network, filesystem service, external package or clock-derived fixture. Main owns constrained execution.
7. **Realistic known-bad failure:** duplicate-acceptance control has concrete valid rejecting tests. Actual compiler/reference/control results must still be supplied by main; this static positive alone is not admission.

## Exact bindings

Directory: `datasets/cache/expansion-v1/versioned-recovery/r11/`.

- Candidate: `exp-v1-recovery-r11-go-generation-0386.candidate.json`.
- Candidate canonical SHA-256: `d36e2a2e2282763b35bf71f55b8ceace5d799891871f1a7aabfa2d4ca00d3ec6`.
- Candidate file SHA-256: `3225a8902cefcf1377bb31693e3f39a340905d1735a6d52d66e8d8d6677cd0e6`.
- Derived prompt SHA-256: `94e330b94823fe54b7c1b840e0ed21c5da2a4ac49e8665fead1a2e2433de411d`.
- Reference SHA-256: `cdc4558b56baaa00a2457d474e73ff4f881888c4438b26d1de50ec37148db365`.
- Test SHA-256: `efb54572898f3bd758abcafe1be3168b7e3ba01b1cf4acaf070b7f66943928b7`.
- Mutant SHA-256: `4ef854a03e6c4ff9ac601de754b89a82ac6b5443338265dcd72bd9766fa75636`.
- Plan file SHA-256: `2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6`.
- Architect evidence `go-recovery-architect-evidence.json`: `a37e40378059b1714b640f2e06dec4e1106ee0fcc5abbf7af284be116f3fd6a7`.
- Independent author evidence `go-recovery-independent-tests-evidence.json`: `982e7e3e27178d4beec1b59148428815ac7b2bc3f3732cde45f29ed5b6f20e16`.

Parent `exp-v1-go-generation-0386`, canonical SHA-256 `74d38e3539a8ee3765eada0f7313188fb1ff8aa67e84e64c905e526283e065f4`; original corpus `datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`, frozen SHA-256 `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

Approved scope evidence `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_GO0386_SCOPE_20260908.md`, SHA-256 `c772c0dcfec824576bcb14250532e11006d949fec5fff6fade6714054fbd0910`. Original hold evidence `GO_NONTRIVIALITY_REVIEW_31.md` in that review directory, SHA-256 `03179b4ce3250f9973eca3222985da27492f510d6331e5cfe9b6f755dc955f4f`.

Source retained: McEval-Instruct, revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row-16048, source-record SHA-256 `10182ee6cc22a20f9461469aa57e2c9eeca38f6715ad863e66aa7a7734b2a74b`, CC-BY-SA-4.0; dataset URI https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct. All five rights flags remain true, and transformation explicitly names the parent ID/hash and derived ID. Rights approval is preserved, not reopened.

Authoring evidence has returncode0, no timeout, no parse error, no disallowed tool items and matching prompt hashes. Derived prompt/reference match architect returned values; test matches independent returned test_code. Independent author receives IDs/specifications only, not reference, control or source tests. These authoring checks are not candidate execution. Canonical hashes use sorted compact UTF-8 JSON with ensure_ascii=False and allow_nan=False.
