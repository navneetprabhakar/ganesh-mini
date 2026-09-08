# Recovery r2 Python bounded static review — 2026-09-08

## Disposition

Exactly two test-only successors reviewed. **0220: static quality positive;0517: retain a narrow oracle-quality hold.** Both now contain meaningful MappingProxy witnesses for the original held defect. No candidate code was executed and no admission is claimed. This completes the assigned bounded review; no automatic further critic loop is requested.

Full updated test files, frozen specifications, r1 source/mutant lineage, correction request and archived critic output were read. The existing r1 reference-quality positives carry forward because r2 prompt/reference/known-bad objects are byte-for-byte unchanged. Only tests and version/binding metadata change. Main owns fresh serial sandbox verification and remaining admission checks. Zero new original-row coverage; original parent and r1 failure evidence remain preserved.

## 0220: both identified test defects corrected

The new initialize test explicitly accepts both `['']` and `['intro', '']`, preserving Outcome identity, successful fields and detached nested outputs. Empty lists, tuples, strings, None and lists containing non-string elements remain rejected. This matches the unchanged nonempty-list-of-strings contract and removes the r1 contradictory oracle.

Constructor coverage now includes MappingProxyType containing ordinary dictionary/list document values. Mutating the original nested sections/meta after construction must not affect loaded data. The direct-deepcopy-wrapper known-bad would fail at construction on this accepted standard Mapping, while the normalized-content reference supports it. UserDict adds a second legitimate Mapping input and later source-entry mutation/insert isolation. These are real semantic witnesses, not tests requiring exotic hostile objects or particular private storage.

Outcome defaults, missing/broken reset behavior, first failure for broken-plus-invalid documents, unique remember history, load/initialize identity, input ownership and repeated returned-value isolation remain covered. No new unsupported expectation was identified. The MappingProxy fixture retains a numeric key and checks that exists requires a string key, consistent with the explicit exists rule and prior parent/r1 fixtures; it does not require undocumented constructor rejection of non-string keys.

Static seven-criterion outcome: prompt clarity, API consistency, independent test lineage, whole-target non-triviality, idiomatic unchanged reference, dependency isolation and realistic mutant discrimination all have positive evidence. The last remains a static prediction pending the main sandbox, not an executed pass/fail result.

## 0517: regression coverage fixed, concrete-type oracle remains unsupported

MappingProxyType caches now cover no qualifying script, cached hit without an available entry, normal download and missing-download failure. Available is also read-only. The tests verify input preservation, cache-result independence, filename-collision precedence and normal parser/URL rules. These fixtures distinguish the direct-deepcopy(cache) known-bad: standard read-only wrappers cannot be deep-copied directly, whereas snapshotting their contents is feasible. This closes the r1 mutant-coverage gap.

However, three tests newly assert `isinstance(result['cache'], dict)`:

- test_resolves_first_qualifying_script_and_downloads_it;
- test_cached_filename_wins_without_available_entry;
- test_no_qualifying_element_returns_mutable_detached_cache.

The frozen specification requires the **outer result** to be a dictionary and calls the nested `cache` a deep copy of the input mapping. It does not prescribe the nested cache's concrete built-in dict type. A detached writable collections.UserDict containing the same source strings, supporting lookup/insertion and preserving input ownership, can satisfy that contract but fails these assertions. This is a compact standard-library counterexample to the oracle, not a claim that the current reference is wrong. The current reference happens to return dict and therefore would not expose this overconstraint in a reference-pass run.

The phrase “Returned cache must be detached mutable dict” appears in the critic feedback, not the frozen specification. Thus this additional concrete-type rule is traceable to feedback; independent authoring does not make it a valid task requirement. Behavioral equality, writable independent contents and input nonmutation are sufficient to test the intended recovery. The exact dict assertions should not be treated as contract proof or silently justified by the reference's implementation choice.

Static disposition: reference correction still positive; prompt/API intent, non-triviality, idiom and isolation unchanged; independent origin verified; intended mutant now distinguished; **test-oracle fidelity remains held**. No new reference change or unbounded review is requested. Under the one-correction limit, preserve and separately disposition this candidate rather than automatically launching another critic. Main may decide the subsequent bounded policy action; this report does not mutate tests or broaden that authority.

## Lineage and evidence verification

The r2 plan binds the original parent IDs/hashes, not the intermediate r1 candidate as its parent. Its rationale identifies the one bounded correction under unchanged r1 specification/reference/mutant. The critic request contains those frozen specifications, the proposed r1 tests and specification-review feedback; it contains no reference or mutant source. Archived events contain only thread/turn and agent-message entries, no tool events. Request and final-output hashes recompute. Each corrected test matches the exact derived-ID output and its stored SHA-256.

The unchanged source was already fully reviewed in RECOVERY_R1_PYTHON_REVIEW_20260908.md. Both complete prompt objects and validation objects compare equal between r1/r2. The r2 plan's parent hashes remain the original canonical0220 `bca2cf2f83b29f86f9b5cd86f07a8256cccca0fabb12438d232066376f9212ce` and0517 `05afcd1e6831356400649b9e287629fdc3016e152134d58ab70a83652eb58c93`.

| SHA-256 object | 0220 | 0517 |
| --- | --- | --- |
| r2 candidate file bytes | b0bb79b2063a6c01f25c555e413bb331fefd24a9de99c154f8b3618922ca1978 | 25ca85ebc35ef1c44777c0e65a64aae2f5da274f5250c119ff04ded178c31096 |
| r2 independent test content | 9ffb2c2befc18725c73e85ed19af7f4c8e2582f2e98ad1718312b2744230db91 | 4ffebb6c5254f51daf475959cd999c146e5a68062ab0cbedd5cb23bb2a61887b |
| r1 candidate canonical JSON, comparison only | 67f3b2671a6865345c1278c8f7d7276e2dcbe3cb036ba564da729254adb5a47d | 400f72dbfd98c60324af0fc21add0e7c41fe1a94836218beb2bd87810a17e3e4 |

Files are under datasets/cache/expansion-v1/versioned-recovery/r2. python-recovery-test-correction-evidence.json file SHA-256: `cb9566aec558c674939277404fb0162cae4f4203e11bd25320510bba3359544b`. Plan embedded logical hash: `c303b148ed2cbfab90d88297706128b1ddfd11dbb06dac1949a67d1ef1d9549d`; this is not represented as a file-byte hash.
