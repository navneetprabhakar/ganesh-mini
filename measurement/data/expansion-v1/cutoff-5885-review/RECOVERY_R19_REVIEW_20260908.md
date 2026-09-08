# R19 Python0717 / Rust0487 independent review — 2026-09-08

Static review only: full original and R12 artifacts, approved R19 request/plan, and complete R19 problems, references, independent tests and known-bad implementations. No generated code executed, no admission, no new original-row coverage, no further critic call or central changes. Seven-criterion calibration follows SEVEN_CRITERIA_GO.md and the Python/Rust frozen sample notes.

## Dispositions

| Derived ID | Reference / substantive correction | Terminal review disposition |
| --- | --- | --- |
| exp-v1-recovery-r19-python-generation-0717 | Static positive: Mapping snapshot and invalid-kind ValueError restored. | HOLD — explicit approved independent-test coverage incomplete: ordinary unhashable invalid kinds and MappingProxy reply omitted. Not a newly demonstrated reference failure. |
| exp-v1-recovery-r19-rust-generation-0487 | Static positive: all four traits implemented on all three public types; different-query-arity fallback preserved. | HOLD — explicit trait qualification does not instantiate Eq, and tests include Debug-text assertions prohibited by the approved scope. Not a missing-trait reference failure. |

Counts: two complete derived reviews; two reference positives; two test-scope holds; zero admissions. Main owns final integration and any separately authorized disposition of these gaps. This report does not initiate another correction loop.

## Python0717

The problem is byte-identical to original/R12. Reference validates kind using comparisons, so ordinary invalid unhashable values such as [] and {} reach ValueError instead of hashing failure. None and integer 1 also reach ValueError, restoring the R12 regression. Validated Mapping fields are converted using dict(fields) before deepcopy: MappingProxyType no longer has to be pickled. Keys, ID, priority 0..9 excluding bool, unique nonempty list tags and exact boolean reply values retain their original contracts. Constructor and property deep copies isolate mutable tags; is_consistent catches its validation errors without imposing private-layout tests. No new descendant-copy guarantee or hostile equality protocol is inferred.

Tests directly witness MappingProxy job construction and backing-tag mutation isolation, UserDict job and custom Mapping reply, None/1 ValueError, bool priority exclusion, exact schemas, empty/nonempty values, deep property-copy isolation and read-only properties. The mutant differs only by deepcopy(fields), retaining corrected kind handling. MappingProxy job is a decisive semantic rejection witness; this is not a syntax-only mutant. The R12 non-string-kind TypeError regression is independently rejected by the existing None/1 cases.

However, approved request explicitly requires ordinary unhashable invalid kinds and MappingProxy reply tests. Neither is present. Restoring set-membership kind validation would still satisfy all current invalid-kind tests while failing []/{} with TypeError; this makes the unhashable gap concrete, not exhaustive-testing speculation. MappingProxy reply is the specifically approved second schema branch, although common constructor code is statically correct and job coverage already rejects the supplied mutant. Existing valid oracles need no weakening. No unsupported oracle or new reference conflict found.

Seven criteria: prompt clear; API/reference consistent; test origin independent; complete target nontrivial due schema/type/value validation and nested ownership interactions; code idiomatic; dependencies standard library only; known-bad realistic and directly witnessed. The hold is approved targeted-test completeness, not failure of source provenance or elementary-padding calibration.

## Rust0487

The R19 clarification explicitly names Debug, Clone, PartialEq and Eq for Observation, ModelError and ObservationStore, retaining R12 constructor locations, nonempty different-arity query fallback and original update/average rules. Both reference and mutant derive all four traits on all three types. Store owns BTreeMap<String, Vec<Observation>>, so Clone is independent and equality includes complete stored content. No missing-trait mutant is used.

Update rejects invalid batches before mutation, enforces observation arity across later updates, and leaves empty updates without model creation. Prediction requires an existing model even for empty queries, rejects empty query vectors, permits all nonempty query arities, uses complete-vector equality, i128 sums and truncation toward zero. No arithmetic or indexing conflict found on supported materializable inputs. Tests cover append behavior, late-invalid rollback, names, exact match/fallback order, i64 extremes, negative fractional averages, clone mutation in both directions, and state equality distinctions.

The mixed-query test with outcomes 3 and 9 at two-feature observations expects [6,3,6,9,6] for one-, two- and three-feature queries. This is substantively equivalent to the approved tiny 10/20 ->15 witness; changing these numeric literals is not a defect or hold. It decisively rejects the mutant's extra query-arity check while both implementations retain all traits and constructors.

The test named public_types_support_required_traits_and_fields invokes clone, assert_eq and Debug formatting, but never uses an Eq bound. assert_eq only requires PartialEq and Debug: deleting Eq derives would not be rejected by any test. This is precisely the approved public-trait qualification gap. Also, contains("7") and contains("ArityMismatch") assert Debug text despite the request explicitly excluding such assertions. The current prompt says derive Debug, so these are not claimed to be a demonstrated false result against the submitted reference, nor is a new cross-version Debug-output contract invented. They are an explicit approved-scope violation and unnecessary to prove the trait. No private store layout is accessed.

Seven criteria: prompt clear; actual reference API consistent; test authorship independent; target substantively nontrivial due transactional state, exact/fallback matching, wide averaging and ownership; idiomatic standard-library code; no external dependencies; realistic semantic mutant with decisive witness. Hold remains the specific test qualification/scope issue above, not reference architecture or mutation validity.

## Immutable bindings

Paths below are repository-relative. Candidate/evidence files are under datasets/cache/expansion-v1/versioned-recovery/r19/. Canonical hashes use UTF-8 JSON with sorted keys, compact separators and ensure_ascii=False; file hashes bind exact archived bytes.

| Artifact | SHA-256 |
| --- | --- |
| recovery-requests-r19.json (review root) | c174093a3eb792c57d0940c656ae0e8cef1447702bd9afeff5e9ed1733279886 |
| plan.json file | 401d56a11f2ca2929eb42be7ffb36fe694cfded2500ed56a96759560b8b65f62 |
| plan embedded payload seal | ef6c38e0eadab9fa90f94dcfcec012c01160c8b9d1c5ff1adfc33b3b94b087e2 |
| run-contract.json | a0b4a39242bee4710967f7d01a0d6031bf4a81401f3aca98bcab09c80b80c6a8 |
| Python candidate file | 7cf1a28c74d1a2f171775e95889039a4fecb3332a145914797762def3cf57b20 |
| Python candidate canonical | b624bad0311feff0e19e0ded806618f78f56d6d6515dfd516c990d7093e1794a |
| Python prompt/rendered prompt | 49701ab781d8b5d856d109aab003eefd3548095d2471b20e8975195434763be5 |
| Python answer/reference | 7c76f2a9375c1b67da0e3b45de6a0f1aebb6abab43376c6afcb2e486bcd13eb5 |
| Python test_solution.py | e1e8d8bff3c458df78e943b52f9e0ec2be5c5c097afdc0792753c3733758640e |
| Python mutant | 4d7a5924ea9389791e9eae3edf56150c753281cd4df093b610daa4ca5eace301 |
| Rust candidate file | bdb6610f5848b885ee103e6aa96b6ef0ca2c39f2dd12af23e72c7ceecc9b5c09 |
| Rust candidate canonical | 047f9334346c3c5711dfa3577f23decd78373b5f3e819fb86c98645c40711179 |
| Rust prompt/rendered prompt | 0a5e39e8643655c11636eef891770f507145c632582fb12b94fb7ee405b62db2 |
| Rust answer/reference | 241b3cf5acdeb01cca500b0e50abadf8179bdaee62128608b46d9a71f570633a |
| Rust solution_test.rs | 345a1a02f5bf633b9cd766f2a04df3e796e12a67a1919133cb1b1c8ea23a5df1 |
| Rust mutant | 90f5aa84e99e7a1c4b4da8a4bb6df028b51ef2b6a3603b5a10970017931c6b85 |

Original parent canonical hashes: Python 4432a25372e0cd1ef3da2401dbab9b82886ecdeb5d0a791dbf22d3fb4768e3e4; Rust 9ee8d243d8728a71c43c64ab9122fceb8e0db37aabc8e8e1f055ff82fb726ad4. R12 canonical hashes: Python 068140f7cd0ffbab9afd76b9a283b20d223e306e83d784e9332c0114bda33114; Rust 8bd4fdde9168e90a56a025f0d7b3117ebfc0e872a1e30905361efc2b40ee264c.

Approved evidence RECOVERY_R19_PROVISIONAL_20260908.md: b52335e0dc0b278940407ee91c308465b5af7acf7b059f231f12c546a4694d5b. Prior R12 review evidence: RECOVERY_R12_PYTHON_REVIEW_20260908.md 4aa736c5fa48090c3a2c45b3798492231d61363f1ff8ffae0756f290a2b4dc4b; RECOVERY_R12_RUST_REVIEW_20260908.md e8fafe162d914b4726b5ddab87ed1a4cb6d3542156eb6000756ff47a9997e625. Original hold evidence remains work-message-mapping-proxy-result.json and RUST_STRATUM_REVIEW_29.md, respectively, as bound in plan.json; no new execution is attributed to this review.

Both retain McEval-Instruct revision 57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0 source attribution and recorded prompt/answer/tests/model_training/redistribution rights=true. Python source row-04048 SHA b8192424da7167dcfab7af8b53b2274881ef6bc31f775bd4c07e409ddb958cca; Rust row-05991 SHA ff9d9a8308576f019c50bec2336ce85b8a7d1ca4ecacc6a08345cf7037ae633a. Source metadata is not generated-answer/test evidence and recorded rights are not a new legal opinion. Transformation strings retain original parent IDs/hashes.

## Independent author provenance

Exact candidate IDs, problem/reference/mutant bytes match architect final items; test bytes match separate independent-author final items. Candidate answer equals reference, and user problem equals verification/rendered prompt. Independent prompts expose IDs/specifications and general test guidance, not architect answers/mutants. Thus omitted recovery-specific tests are not evidence of answer leakage; the specificity in the approval rationale was not supplied as a test checklist.

| Evidence filename | File SHA-256 | Prompt SHA-256 | Final output SHA-256 |
| --- | --- | --- | --- |
| python-recovery-architect-evidence.json | ad6e2d7328eddbec78806e006dfcb32c23c7e50c982b553fc87ddeee930e9768 | b4f82fe02b27f845f550bb80de736d7b3bf216d668027d9b033da1839f2c824e | 4bb588d51fc678f9a55271252c8506e8e02db337997ec2bcdacb958a4a4b44e2 |
| python-recovery-independent-tests-evidence.json | 8e6eb9947473d2a7b5ea85042f2e41f651cb46d86c4e4ac0f7e5f415943aee5d | 05c92f110fb9ad28fc3dc89a405921f481d3c1eb9a3297eb06557bd6d8839add | dc80b3fa0ac90a8d025286f732614ca8635b342d6329391dc6e46c712af0e69d |
| rust-recovery-architect-evidence.json | bec8f7d358a3ab0475380ed1ecc6ab8db806a17289b1c56dccca7b8b1b355042 | aa890609e3c7519d0b14fb2c310d682b62f19d26d24c1424c9ef15c5c557c4e0 | d243f9f0eb60dc4cc3cca57f083e6582b33d4df69f6cd233237f1bc2bc6dc363 |
| rust-recovery-independent-tests-evidence.json | 5dbb7ee37231b17e8759ae07d4e6e0616ff42a01733efd01fc727869416b4577 | 23a00cd1e1f8ca3dea65980a27465d1d2613805d852e5ae32cf6e5f2469ee33d | 07dde9a32d5be9f0b5de3ca89865731a9bf5f37fcd9f9ac69d3d3393de3575d9 |

Author return codes are 0 with timed_out=false; these describe generation, not sandbox verification. Execution and release gates remain separate.
