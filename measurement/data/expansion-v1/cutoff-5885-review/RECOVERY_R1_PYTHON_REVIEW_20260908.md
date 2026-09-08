# Recovery r1 Python static quality review — 2026-09-08

## Result

**Both reference corrections are substantively complete for the documented outer-Mapping defect, but neither derived candidate is ready for quality approval as packaged.** The independent tests omit non-dict Mapping inputs in both cases;0220 also introduces a contradictory oracle. No candidate was executed in this review. Main owns sandbox results and any successor correction; these findings must not be reported as executed failures or admission.

Scope is exactly exp-v1-recovery-r1-python-generation-0220 and exp-v1-recovery-r1-python-generation-0517. Full derived prompts, references, complete independent test files, known-bad implementations, immutable parent prompts/references/tests/known-bad implementations, and the two Python request/output evidence streams were read. Seven-criterion calibration follows SEVEN_CRITERIA_GO.md and SEVEN_CRITERIA_PYTHON.md. No candidate, plan, ledger, or central document was changed.

## Binding and lineage

Both plan records are reference-fix. Their derived prompts are byte-for-byte identical to their respective parent prompts. Canonical parent JSON hashes recompute to the plan bindings below; parent rights are preserved. Derived prompt/reference/known-bad/test strings exactly match the architect and independent-test final outputs for the exact derived IDs. All four stored content hashes per candidate recompute correctly. The test files are newly generated independent output, **not accidentally copied parent tests**.

The independent-test request includes only IDs and frozen specifications, not reference code, known-bad code, original tests, or architect correction context. Its prompt/output hashes recompute, its disallowed-tool list is empty, and its archived events contain no tool access. This supports independent origin but does not establish oracle correctness or coverage. Architect evidence separately receives the parent reference and correction request, as intended.

Original unique coverage remains unchanged: these parents were already reviewed. This is a fresh two-derived-candidate quality assessment, not two additional original inspected IDs and not two admissions.

## Exact findings

### exp-v1-recovery-r1-python-generation-0220

Reference materializes the outer mapping with dict(documents), then deep-copies the resulting content. None still means an empty collection. This removes the standard read-only MappingProxyType constructor failure without narrowing the original mapping domain. Outcome identity, field resets, truthy-broken handling, nonempty-list-of-strings validation, detached load/initialize results, failure short-circuit and unique remember history are unchanged. The entire target is a substantive state/ownership workflow; the two-line correction is not elementary merely because it is short.

**Blocking oracle defect:** test_initialize_accepts_only_nonempty_list_of_strings places `{'sections': ['']}` in invalid_documents and asserts failure. A one-element list containing the empty string is a nonempty list of strings and must succeed. The same generated test accepts `['intro', '']`, confirming that no consistent extra nonempty-string interpretation explains the assertion. The original parent test explicitly accepted `['']`. The derived reference correctly accepts it; do not change the reference to accommodate the test.

**Blocking discrimination gap:** every supplied documents collection is None or an ordinary dict. The derived known-bad is the original reference, whose sole difference is direct deepcopy of the outer mapping. These tests do not exercise the held Mapping-wrapper defect. Both reference and known-bad would be rejected by the same bad empty-string oracle; such rejection would not prove mutant discrimination.

Required successor test work: correct the `['']` expectation, retain empty-list and non-string-element rejection, and add a specification-grounded read-only outer Mapping with ordinary nested dictionary/list contents. Mutate the backing inputs after construction and returned nested values after activation; assert stored isolation, Outcome identity, and unchanged input mapping. MappingProxyType is a standard accepted-domain witness, not a hostile custom object. A corrected reference must pass and the direct-wrapper deepcopy mutant must fail for the intended reason.

### exp-v1-recovery-r1-python-generation-0517

Reference changes only result_cache construction from deepcopy(cache) to deepcopy(dict(cache)). It therefore supports read-only Mapping input while returning detached writable storage. Parsing, first qualifying script, exact attribute value, URL-path suffix, standard resolution, basename cache key, cache precedence, missing-download KeyError and input type checks remain unchanged. Available is read-only through ordinary lookup and its values are specified strings; no extra nested noncopyable-value domain is inferred.

**Blocking discrimination gap:** all cache/available fixtures in the independent file are ordinary dicts. The known-bad restores direct deepcopy(cache), exactly the held defect. On every supplied valid fixture, that copy has the same behavior as deepcopy(dict(cache)); the suite contains no case that distinguishes this mutant. No contradictory expected result was identified in this file, but a likely passing reference suite is insufficient when the realistic mutant remains undetected.

Required successor test work: use read-only MappingProxyType caches on no-match, cached-hit and download paths; verify the returned cache is detached and accepts inserted content, cache-hit avoids available lookup, and missing available URL leaves both inputs unchanged. At minimum, an empty read-only cache on the no-match path distinguishes the direct-deepcopy defect without large input or networking. Add a read-only available mapping on a normal download to exercise the stated breadth. No URL-domain expansion or custom malicious object is necessary.

## Seven-criterion disposition

| Criterion | 0220 | 0517 |
| --- | --- | --- |
| Prompt clarity | Positive: typed Outcome fields and activation/history/error/copy rules are explicit; nonempty list does not mean nonempty strings. | Positive: function schema, HTML/URL selection, cache and error behavior are explicit. |
| API consistency | Reference positive; supplied test oracle conflicts on `['']`, requiring correction. | Positive on static full read; exact return keys and TypeError/KeyError boundaries retained. |
| Independent test origin | Provenance positive; oracle quality blocked and original defect not covered. | Provenance positive; original defect not covered. |
| Non-triviality | Positive: ordered load/initialize, mutable Outcome identity, failure and history plus deep ownership. | Positive: parser/URL selection and filename-cache precedence with error atomicity and ownership. |
| Idiomatic implementation | Positive: normalize mapping contents, standard deepcopy, direct state updates. | Positive: HTMLParser and standard URL functions; isolated copied cache. |
| Dependency isolation | Positive static: standard library only, deterministic in-memory work, no network/filesystem operations. | Positive static: standard library only; available simulates downloads without network activity. |
| Realistic known-bad failure | Plausible exact held defect, but suite cannot attribute failure to it; oracle itself is wrong. | Plausible exact held defect, but no supplied test distinguishes it. |

Overall: **two derived quality holds pending independent-test correction/coverage; zero reference changes requested by this review.** Preserve original r1 artifacts and request/output evidence; any correction must receive the versioned immutable binding required by the recovery workflow. Fresh sandbox reference-pass/mutant-fail and further admission checks remain main-owned. This is not a reason to reopen the completed original review.

## SHA-256 evidence

All candidate paths below are under datasets/cache/expansion-v1/versioned-recovery/r1; IDs retain the full exp-v1-recovery-r1-python-generation prefix.

| Object | 0220 | 0517 |
| --- | --- | --- |
| Parent canonical candidate | bca2cf2f83b29f86f9b5cd86f07a8256cccca0fabb12438d232066376f9212ce | 05afcd1e6831356400649b9e287629fdc3016e152134d58ab70a83652eb58c93 |
| Derived candidate file bytes | 2f309e8e90be0b44ee95ace95c9feb162c6a070da08c09b7765e9add09bcafed | 902ce9c0abb2c51a053673a37f4477b6257c092cf55bda3f10283206b79ede1d |
| Prompt | 748e621fffc1d90382d20631555e690bdcd7685666e988bc04c4ab8f1e82bc46 | 391cb3ebd0c7ed8fc2506d9e52941d90bca7a0502ec8f833e92edcea70854d2f |
| Reference | ce12550e9a3ceab437adb1c695010bc2dac40b142c01495c82ded995ba4d7303 | 407e201a35967e17ec6ad767757328ac5a362c07fa38be744870c7acbc816948 |
| Known-bad | a30330fedbd0794e0a45553fc9d9492383cfd7e3de0045a16337dcda97696d32 | b9db74fbe3891f4bbb07cc7e341cf0547b570c85dd87045fcbbc9e5e62caa948 |
| Independent test file | 8db8a20be0891e6789dbcd52836edf44b2ed2c0a2eca031a60fa6047fa44bb3d | 85f871a58fbca0827843fc9552984337850a39704141181d823f1d8561bd6ac6 |

- Original corpus: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
- Python architect evidence file: c015379bc8651ee06d4449af035157a6034987db9828c7aa21be5dac562d84e7.
- Python independent-tests evidence file: 72150a47b328f24d21aed07dfa7e05ccc24c279259ab618e98c1ee5029a01e06.
- Plan's recorded logical plan_sha256: ff64db89a09b39d0ca9b19f2b7231ded79cbff17823b21be51d36ea4c0647fdb; distinguish this embedded logical binding from a file-byte hash.
