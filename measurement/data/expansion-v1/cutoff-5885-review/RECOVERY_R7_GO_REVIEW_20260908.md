# R7 Go test-only correction review — 2026-09-08

All nine corrected test files were read completely, including support go.mod, against the previously fully read r4 specification/reference/mutant and the bounded correction scope. Exact equality checks confirm r7 messages and entire validation objects equal r4: specification, reference and supplied mutant remain unchanged. This is a static assessment, not execution or admission. No further critic cycle, cloud operation or central mutation; zero new original-row coverage.

## Dispositions

**Nine static positives; zero new static holds.** Actual reference pass and semantic mutant rejection remain main's sandbox responsibility; 0439 and 0522 additionally require the separately planned actual race-detector qualification. No executed claim is inferred from static witnesses.

| Suffix (`exp-v1-recovery-r7-go-generation-`) | Decision and specific justification |
| --- | --- |
| 0330 | STATIC POSITIVE. Different equal-sized empty-valued keys now require update and exact desired labels, whereas matching empty-valued keys require none. This directly rejects missing-key/zero-value equivalence. Creation, removal, updates, nil/empty equivalence and copied labels/conditions remain tested. The table-case selector itself uses missing-key zero-value lookup and consequently selects desired-empty labels for several cases; this weakens their original specificity but does not create false oracles or erase the separate explicit regression and name-change case. No new correction required. |
| 0439 | STATIC POSITIVE; actual -race qualification separate. Runtime identifiers use Go Unicode escapes representing actual NUL, not literal backslash text. Both colliding concatenation pairs survive and sort structurally; replacement/deletion leaves the other intact. Mixed concurrent Apply/Snapshot assertions are safe, detailed below. |
| 0499 | STATIC POSITIVE. Native MaxInt is used as a logical attempt limit with first-call success, exact one-call count and used=[1]; tiny actual work distinguishes premature full-limit allocation. Saturation, bounded final-error identity, invalid no-call behavior and propagated panic retained. No claim of unlimited physical resource guarantees. |
| 0514 | STATIC POSITIVE. Existing/absent/nonpositive IDs now occur together in multiple permutations, requiring ErrInvalidNote and retained records. All-positive missing batch remains atomic, duplicates delete once, empty succeeds. UTF-8 byte-length case is valid. Unspecified error-return Note{} assertions removed; explicitly promised pagination nil/non-nil distinctions retained. |
| 0522 | STATIC POSITIVE; actual -race qualification separate. Both present and absent invalid destination matrices require error only, including absent scalar/typed nil. This directly distinguishes validation-before-absence. Genuine incompatible decoding via valid nonnil pointer requires true/error. Unpromised invalid-destination found and empty-Keys nonnil requirements removed. Copy/encode atomicity and concurrency/value checks retained. A separate custom-unmarshal absent-call counter is not present, but reference checks absence before unmarshalling and valid absent destination preservation is tested; no new mandatory oracle invented. |
| 0567 | STATIC POSITIVE. Declared final variadic []string invocation, typed/untyped nil slices and rejected expanded/scalar arguments now exercise CallSlice semantics. Nil unsafe.Pointer parameter is separately accepted without dereference. Signature types, assignability, exported names, zero results and panic/prior mutation remain covered. Supplied r4 mutant contains both omissions; tests now cover both, without representing it as a new single-defect isolated control. |
| 0692 | STATIC POSITIVE. Appending through first live returned slice before subsequent Take checks future zero initialization; separate adjacent-live-region append checks isolation. Tests demand behavioral separation, not a particular capacity. Tiny arena, fallback isolation, exact fit and reset behavior remain valid; no post-reset independence invented. |
| 0720 | STATIC POSITIVE. [a requires b,b,c] now requires b,a,c, and multiple newly ready earlier steps are tested. These distinguish stale forward selection. Failure/skipped outcomes use complete unique-name/status/error comparison rather than unsupported skip/executable interleaving; executable callback order stays asserted. Whole-graph prevalidation and immutable inputs retained. |
| 0774 | STATIC POSITIVE. One/two-article queues with native MaxInt logical page limit and nonzero start directly exercise overflow-safe clipping, including exact trace. Empty Items now checked by length only, while explicitly zero error PageResult remains enforced. Sorting, cursor, budget and snapshot rules retained. |

## Concurrency adequacy

0439 uses 30 distinct structural writer keys, each sequentially inserting, replacing, deleting and finally inserting an exact replica value. Four readers each perform 50 snapshots and check structural uniqueness and elementwise sorting without assuming transient count. A shared start channel and WaitGroup bound the run; worker failures use t.Errorf with return, not t.Fatal. Post-join exact sorted records and replica values are deterministic because no other writer touches a writer's key.

0522 uses 20 distinct writer keys, each performing Put/Get/Has, replacement/Get, Delete/absent Get, and final Put. Local destinations and exact values make its per-key assertions sound without scheduling assumptions. Four readers perform 40 Keys snapshots checking sorting/uniqueness. Final joined keys and every final decoded value are checked. Test-owned mutable state is local or synchronized, so the harness introduces no evident data race.

Both are suitable bounded mixed-method workloads for actual -race execution. They do not prove every possible interleaving or guaranteed overlap of every operation; that is not asserted. Their static correctness does not substitute for actual race-detector results.

## Seven quality criteria

1. Prompt clarity: unchanged r4 contracts determine the witnesses. No new input restriction, cycle guarantee, unlimited-resource guarantee or unspecified secondary return representation is imposed. The intentionally unspecified 0720 skipped/executable interleaving stays unspecified.
2. API consistency: r4 scoped-positive reference corrections carry forward by exact equality, not assumption; full validation object unchanged. Required APIs, standard domains and error rules remain intact.
3. Independent test origin/validity: corrected tests come from the bounded critic that saw only specifications, earlier independent tests and specification-derived feedback. Direct intended witnesses now replace the previous qualification gaps; identified unsupported oracles are removed.
4. Nontriviality: all nine retain substantive whole-target state, graph, callback, validation, reflection, allocation or ownership interactions described in the r4 report. Test-only correction adds no padding and earns no new original unique-row credit.
5. Idiom: unchanged standard-library references remain appropriate; corrected tests use ordinary deterministic fixtures, safe nil-pointer comparison and bounded synchronization. Minor redundancy in 0330 is not a correctness hold.
6. Dependency isolation: Go 1.22 module, package solution and standard library only. No network, external service or unsafe dereference. Actual execution remains constrained to main's resource-limited network-disabled sandbox.
7. Realistic known-bad failure: every row now has a direct legitimate semantic witness, individually explained above. Compiler failure, arbitrary oracle failure and authoring success are not substitutes for verified mutant rejection. Execution remains separate.

## Provenance and immutable hashes

Prior review: `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R4_GO_REVIEW_20260908.md`, SHA-256 `ba2bc832162e4d97b4831c59385fb8d1440ea271ff6a2138612a2656975bed05`. It contains exact original-parent and r4 candidate hashes and complete reference assessments.

R7 directory: `datasets/cache/expansion-v1/versioned-recovery/r7/`. Candidate filenames are `exp-v1-recovery-r7-go-generation-NNNN.candidate.json`. Canonical SHA-256 uses sorted compact UTF-8 JSON with ensure_ascii=False and allow_nan=False; file SHA-256 hashes exact bytes. Test SHA-256 hashes exact solution_test.go content.

| Suffix | Canonical SHA-256 | File SHA-256 | Test SHA-256 |
| --- | --- | --- | --- |
| 0330 | 294bc65541b99a628308951501bd23fc0f6f42661ac3e874a354d7b1766215a5 | 9bdcc0e6326b0a25a4de95ee2535cdd23ccb137fb840acb0f51b32ccc820ce4a | f0e7ec190f8c45a59db81547249745532a7a2050057597f0de27bb90638908bf |
| 0439 | b8936ff975c3ef2fd3be07cf1fede375c220340d9ef19f70396a14745caa4d04 | cc2a0441668d13803266efa87fd4b3c43aadc5a7555062481f57c4eca521157d | 048e994db124fc006a7e2375dd5d5ca2dc2a524b6e4dbbb40af5ed0c270f3fc9 |
| 0499 | 551303ec9dadd3fa5a950d684499e4f71ee2bbc3acd53683b155ed6921c90cbb | b949a9254678f55d2be6991a3683c290a4831d2f93dba0d6301b6b44c1a4ba59 | bb042fc68f34e1a443f920233c4259f9afc2e7382fcb5a56c68d88d0b757cf3f |
| 0514 | 1cb8f7f26ea19c23c7f0dbf81bfaf4ed675591fcccbacaee49fe72d7b3067930 | cb79dbcc230ee6d8dc81ed2ba4ed431189537d05af7fed24faa4c46edd1eff4b | f46ef5645baceb750e4a2d368e7ea0ddb61981b215949d0beaf0ab7acc2b30e3 |
| 0522 | 3a20d4e335c8894279b410d081cb92bbe6b639330fc05b5f8f93ead04567960c | c2816889cc21fc5c0803533773baf37e837140bbbe582e8f8ea8215eae20fe2e | 23ead8e5fb11e41b6cdbc06c1e371180af78b76e548e9ef03d028e683d26a573 |
| 0567 | fc724e17e1ab43ea3112bcf57cd6cd342f4f2797b9cff9720d9d67fb1816260b | c5dfd3d1b19ebd06cc6d2203e9392533614f373fe1ed7658f88fe9feb416a8b1 | 921f0dd558e86674a993b4c6ff5bd27548d29a0ee830ad7203d0a9c8cfd0b1ea |
| 0692 | 32613df7bdad0e0a9720552905a73ea3efe1c8701e1da03411c39695ddea4975 | f178ffdc9cab9fcf66610cadb838edc5f27e84723f644f01fe884537976b8c17 | 232c7e94d7188d23f1b609542dba140f2998c49f144d94546fa64ed48495e37c |
| 0720 | 08e43134db4ad9a9fdc974d7e8aff8458681c3d6ba50c4f98debac47c412e5c8 | 3ec99ff010ab04ffbea27bfd2209fb7410af1c5264d07083f374e23ae59663c5 | 0ab52c30577f3db7e2a7a710f9d781721daf966c0996f862a7a845a49b414715 |
| 0774 | 7de6923a49484654559b8efdc5468b2408a523dfb511598145256f5b4343745d | c7190a5f8e5ce3ba75b42ab4ffc5079c32574855035871c48545fa05a523a8db | 2a4a36c1b3f9c6cb9dc18d0e3d44413da51286ff1d5c357ee907ec48dba19e89 |

Evidence file SHA-256:

- `plan.json`: `f0a3b5d14eb983206ac83c99571c5522925feaf7ac0443ec3c59ad172d5f293e`
- `go-recovery-test-correction-evidence.json`: `48bef311cdeacb4898e34554485dbe742843711296047015e3f7af20639c5c47`
- `generation.json`: `d844028cd12e8a0bce00a5f8f89cb5ec6f39fd1da4fefda5d38ee5b839adae32`

For each exact ID, parsed critic input has only id/problem/test_code; its problem and proposed test equal r4 prompt and test. Its final test_code equals r7 test byte-for-byte. The intervening instruction requests specification-compatible test correction and the appended feedback contains specification-derived review, no implementation source. Recorded authoring returncode=0, no timeout, no parse error, empty disallowed tool items and matching request prompt hash. These are provenance checks, not candidate execution evidence. Main owns final admission and preservation of original source/rights lineage.
