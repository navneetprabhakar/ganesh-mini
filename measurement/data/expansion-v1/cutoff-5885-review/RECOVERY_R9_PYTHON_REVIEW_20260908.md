# R9 Python test-only correction review — 2026-09-08

Gate 2 static review of exactly four derived candidates. **Four static positives; zero new quality holds.** No execution, cloud activity, admission, repeated critic request or central edits. Original unique-row coverage credit remains zero.

The complete corrected test files were read. Every prompt object and entire reference/known-bad validation object is byte-for-byte equal to its fully reviewed R6 counterpart. The reference judgments in `RECOVERY_R6_PYTHON_REVIEW_20260908.md` therefore carry forward without silently substituting another implementation. R9 changes the tests only, within the single approved correction.

## Per-ID adjudication

All suffixes below identify `exp-v1-recovery-r9-python-generation-<suffix>`.

| Suffix | Decision | Concrete basis |
|---|---|---|
| 0355 | Static positive | New MappingProxy batch mapping has integer key 7 and tuple key `(region, 2)`. Required key order and sample2/xor4 descriptors are checked by contents, without concrete Mapping-type demands. The string-key-restriction mutant rejects this valid input. Existing one-shot multi-scheme, ordered replacement, partial-block, empty, malformed and payload-ownership tests remain meaningful. |
| 0445 | Static positive | Matching MappingProxy notice and authenticated MappingProxy principal now exercise the actual accepted Mapping domain. Ordinary nested dict/list values are checked for isolation through independent mutations in both directions. The direct-deepcopy mutant fails on the outer proxy. Unsupported filter-rejection tests, including locality=None, are removed rather than converted into a new policy. Tests still exercise exact filtering, duplicates, empty string fields, authorization and correctly shaped malformed notice fields. No concrete copied-mapping type is asserted. |
| 0298 | Static positive | Rank `10**500` and its neighbors now cross the float-conversion boundary using five tiny records. Expected order is top, a, b, c, low, correctly combining descending rank, casefolded title and ID. Exact integer ranks are preserved. This distinguishes unconditional math.isfinite coercion. Normal finite floats, search, pagination, snapshots and invalid inputs retain coverage; no invented float-result or rank-cap requirement. |
| 0672 | Static positive | Integer attribute key now requires TypeError under the explicit dict[str, object] contract, distinguishing the missing-key-validation mutant. Empty-string attribute keys are separately accepted, with nested ownership checks. Frozen dataclass, field order/defaults, normalized strings/tags, duplicate rejection, supported kinds and nested copies are still covered. No nonempty-key rule was introduced. |

These are static predictions about realistic known-bad discrimination, not reported sandbox pass/fail metrics.

## Seven criteria

1. **Clarity:** frozen specifications remain intact. Corrected tests respect the distinction between unrestricted batch keys and string record names, Mapping notice inputs and declared dict attributes, and exact integer ranks versus float representability.
2. **API consistency:** top-level names, function/class signatures, declared schemas, field ordering, container ownership and exception categories are preserved. The former 0445 oracle no longer invents filter validation from notice-field requirements.
3. **Independent origin:** the critic input contains only IDs, frozen specifications, previous tests and specification-derived prose feedback; no reference or mutant source. Exact provenance checks below pass. Origin and oracle validity were assessed separately.
4. **Whole-target nontriviality:** unchanged substantive targets retain multi-scheme one-shot processing (0355), authenticated validated filtering and deep ownership (0445), fuzzy retrieval/ranking/pagination (0298), and typed frozen options with normalization/uniqueness/deep copies (0672). Positives are not based on patch size.
5. **Idiomatic code:** unchanged references retain the appropriate standard Python validation, iteration, dataclass and copying idioms reviewed in R6. New tests use straightforward unittest fixtures and standard numeric/Mapping examples, not hostile custom objects.
6. **Dependency isolation:** all four suites are standard-library-only, import the requested solution APIs and retain executable unittest entry points. No execution or compilation was performed here.
7. **Realistic failure:** each new fixture now reaches its specific reinstated parent defect. No unrelated shared failing assertion is used as substitute evidence. Static inspection found no new unsupported oracle demand.

## Exact bindings

Paths below are under `datasets/cache/expansion-v1/versioned-recovery/r9/` unless qualified.

- `plan.json` file SHA256: `0f0d6e653bbabff308a912cc764d1373b20faf3f4cf68a4c7341c94f36b5ae79`.
- `python-recovery-test-correction-evidence.json` SHA256: `5e51e82a7609a7b6dd5315625afcd8fac91ca942a5458d2668f5670212b3e311`.
- Review-root `recovery-requests-r9.json` SHA256: `886fb742fffb91825f419f4b4f05552f42ab965868768bc77b0a5155fcda42c9`.
- Review-root `recovery-test-feedback-r9.json` SHA256: `df584f198eeae9c3117219c270efad47e70d7e7812cf0ca99bb3cf38f58f7979`.

Evidence prompt and final-output hash fields recompute correctly; disallowed tool-item list is empty. Each parsed critic item has exactly `id`, `problem`, `test_code`. Its problem and old test_code match the exact R6 candidate. All four feedback previous-candidate canonical hashes match R6. All four final output test_code strings match installed R9 tests. Every frozen prompt/reference/mutant remains unchanged, as confirmed by equality of prompt and complete validation objects.

| Suffix | Candidate file SHA256 | Corrected test content SHA256 |
|---|---|---|
| 0355 | 2e71a3cb0826d653eece315bcf6199a8583c40b80ebd829ad6feaefada6a4acb | 530a6491bb9b6e86234eb33b75775924f656cf0bff4fe75e356008dfe9156199 |
| 0445 | 9a6d2f077822f7f8646d9f824475bbcb6d218913dd17c47fc92319a0af6454a4 | 70a2588313fef39d6c5d7eac270e3b01e5fe574e0bd649bdb96e01ae12b5c906 |
| 0298 | cdb646e9683782234ab2b7fd51aee4a9e31afb708d517d4a1b6cf77b01844509 | a257e4744b2a501c273f82c9c97dedff62ef4f6cec931b3126174e7c20a380b3 |
| 0672 | 82791daa1766b16503353651e1684fcf001edbe9060d0db9b92cee448b304004 | 7c6f11ed7e615b77331f788a69b3cddb3c72d7652ce75f831099b15264354701 |

| Suffix | Frozen prompt SHA256 | Frozen reference SHA256 | Frozen mutant SHA256 |
|---|---|---|---|
| 0355 | eee7633773233463861add808aeb885ac96f1b0e123610c18a2163359c59775a | f5928770e98792d8a2a97a23bcb2217ca393aba7f366451c55c2ccd592878a41 | 9a9559c49aeb981b655c25834e2cefeafbad8cfce1c5c3b28afa14f6958a5500 |
| 0445 | 8187eea886aa094141dfc5caac2b1e15cb3c3fb80d30482318ba0c4392ffc3c5 | cc29757118fa3fc5a8862c3faa19f5b56bac54fd7afbb9960f46ee7db18d9b9e | 4d4870713bdab37c4bc4f565014dac63c562385f455c6745ec2f98c8c1ae44d4 |
| 0298 | 879c6fb43290e8a23967ce56bdf682263ee1d0643be61009c537d36e48ebcfce | 1db93a06df2d1135256d32098a38b9794804ca8ff4bbdd519dbed04031323774 | eaaf114d1ac9e129bfe332f16312fae2a011b522031e570bb7237058de10d232 |
| 0672 | b1031b1c96a8d866d71e60e2193f139cf27aa6c225de4cebe5d22bdd001061f7 | 45473b113a838d135083aea3f61a04c481d60509c36b3b933f3390644aa3f28d | bb77755d0d767dcbd911a4781e9b23aaa854a09df8d90e406f4ace8d1768c2d8 |

Main owns serial sandbox diagnostics, provenance/admission integration and any final disposition. The four R6 holds remain historical facts; these positives apply only to the exact corrected R9 hashes.
