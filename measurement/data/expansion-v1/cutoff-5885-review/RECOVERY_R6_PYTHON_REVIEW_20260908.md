# R6 Python static quality review — 2026-09-08

Scope: exactly seven derived generation candidates, not another original-corpus review. Gate 2; no candidate execution, generation, cloud activity, central edits, or admission. Complete derived prompt, reference, independent tests and known-bad source were read for every row. Conclusions below are static predictions, not sandbox results. Original unique-row coverage credit: **zero**.

## Decision

**Three static positives: 0269, 0314, 0319. Four derived quality holds: 0355, 0445, 0298, 0672.** The latter references correct the targeted parent defect, but their independent tests do not establish that correction; 0445 additionally contains an unsupported failing oracle. Do not change a contract/reference to satisfy that oracle.

Every ID below has prefix `exp-v1-recovery-r6-python-generation-`.

| Suffix | Reference / contract | Independent oracle and intended-defect witness | Static disposition |
|---|---|---|---|
| 0355 | Removes only the unstated string-only batch-key restriction; preserves supplied mapping keys and all four descriptors, materialization and order semantics. | All tested batch keys are strings. The sole mutant difference rejects non-string keys, so ordinary descriptor/ownership tests cannot distinguish it. Integer/tuple-key witness requested by the approved scope is absent. | HOLD: missing actual recovery witness. |
| 0445 | Selected outer mappings are normalized with `dict(notice)` before deep copying. This addresses ordinary matching `MappingProxyType` notices without requiring a concrete copied mapping type. | Only dict notices are tested; no MappingProxy witness. `test_malformed_filter_arguments_are_rejected` demands an exception for `locality=None` on empty notices, although the unchanged prompt does not impose this filter-type restriction and the reference accepts None and returns an empty list. | HOLD: unsupported oracle plus missing actual recovery witness. |
| 0298 | Integer ranks avoid float conversion; finite-float validation, ranking, fuzzy matching and snapshots remain intact. | The nominal huge rank is only `10**200`, still within finite binary-float conversion range. It does not trigger the original `math.isfinite(rank)` overflow. No test supplies an overflow-range integer such as the approved `10**500`. | HOLD: missing actual recovery witness. |
| 0314 | Explicit approved mixed-numeric policy is present in the derived prompt. Integer-only addition remains exact; mixed conversion OverflowError propagates; native infinite float results are permitted. | `10**1000` integer value and offset require exact `2 * large`, distinguishing the mutant's unconditional `math.isfinite`. Native overflow, infinite result, unmatched malformed corrections, duplicate keys, ordering and copied tags have specification-grounded tests. | POSITIVE, static only. |
| 0319 | Prompt explicitly separates input validation from native arithmetic and freezes validation before lifecycle shortcuts, bool-limit rejection and atomic overflow. Reference computes into a local before changing state. | Huge integer coordinates and limit with exact movement distinguish the unconditional-finiteness mutant. Tests cover refire/boundary, active invalid fire, inactive invalid advance, overflow state preservation and permitted infinite movement. | POSITIVE, static only. |
| 0269 | Exact integral/rational Real values avoid float coercion, ordinary nonfinite floats and bool are rejected; comparison and output container semantics remain intact. | `10**1000` threshold with equal and neighboring integer values exercises the original overflow defect. Schema, duplicate-ID equality, iteration order and independent bucket containers are tested. | POSITIVE, static only. |
| 0672 | Adds string-key validation for the expressly declared `dict[str, object]`; no nonempty-key restriction is introduced. Existing normalization, frozen options and nested copying remain intact. | Every supplied attributes dictionary has string keys. The wrong-type test supplies a list, which both implementations already reject; it does not reach the new key check. | HOLD: missing actual recovery witness. |

## Seven-criterion assessment

1. **Prompt clarity:** the five reference-fix prompts are byte-for-byte unchanged from their parents. The two approved clarification prompts explicitly state numeric input types and native arithmetic/error policies. No silently narrowed integer range or finite-output guarantee was introduced. For 0445, notice-field string requirements must not be silently transplanted onto filter arguments.
2. **API consistency:** requested names, signatures, schemas, ordering, ownership and state transitions are retained. 0672's dict type is expressly declared, unlike the generic Mapping inputs in 0355/0445/0269. The 0445 filter oracle is not justified by that API.
3. **Independent tests:** recorded specification-only provenance and exact output bindings pass for all seven. This does not make an unsupported expectation valid or imply intended-defect discrimination. The four specific holds above remain necessary.
4. **Whole-target nontriviality:** 0355 combines four byte descriptors with one-shot multi-scheme processing and ordered replacement; 0445 combines authorization, complete row validation, filtering and nested ownership; 0298 combines validation, fuzzy retrieval, ranking and pagination; 0314 joins validated unique composite keys with arithmetic and sorting; 0319 has interacting reusable lifecycle and atomic numeric transitions; 0269 enforces cross-mapping schemas and ordered multi-metric partitioning; 0672 combines typed frozen configuration, normalized uniqueness and nested copying. These are substantive complete targets, not approved because the recovery patch is small.
5. **Idiomatic implementation:** standard Python iteration, dictionaries, dataclasses, copy utilities and explicit validation are appropriate. The finite-value changes do not require invented hostile custom numeric objects or global allocation guarantees. Static scope accepts ordinary built-in/exact standard numeric behavior; no fresh universal-domain review is claimed.
6. **Dependency isolation:** reference and test imports are standard-library-only; requested top-level APIs and executable unittest files are present. No execution was performed by this reviewer.
7. **Realistic known-bad failure:** each mutant reinstates a plausible held defect. 0269/0314/0319 include actual distinguishing inputs. 0355/0298/0672 do not. 0445's common filter assertion would fail the reference too and cannot stand in for a Mapping recovery witness.

The approved test suggestions are not all present verbatim: 0269 lacks Fraction/MappingProxy controls, and 0314 uses huge addition rather than the suggested no-correction/cancellation pair. These are recorded scope breadth omissions, not fabricated failures: the actual tests exercise the repaired numeric mechanism, and full static reference inspection supports the omitted ordinary cases. Conversely, the four holds lack the intended mechanism altogether or contain an unsupported oracle; they are not merely missing arbitrary extra cases.

## Exact evidence binding

All paths in this section are relative to `datasets/cache/expansion-v1/versioned-recovery/r6/` unless stated otherwise.

- `plan.json` file SHA256: `803f0308b33b4b8a834347d5976a148bc66001d6fc8606a1e206fb0e2b4a6795`; embedded plan digest: `0c7d76825c37e2291eb56549277aaa29b44812a6d6b842d2825faf7da69b3295`.
- `python-recovery-architect-evidence.json`: `9a1969d11e2fabb3d589fb4779a230c42104edffc0585dd531e283edd3fcdffe`.
- `python-recovery-independent-tests-evidence.json`: `088a5d59f6e04df05467f57d807cf9b4843045adff3c713f4e5b477a34b375cc`.
- Original corpus SHA256 verified: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
- Approved review scope SHA256 verified against plan: `91666df9bc114362a55cf7fb4a55aa674077c92ec60a35d31577e6d356337790` (`measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R6_SCOPE_PROVISIONAL_20260908.md`).

Both evidence prompt/output SHA256 fields match their recorded strings. Test-request payload contains only exact `id` and `problem` fields; specifications match candidate prompts. Both disallowed-tool lists are empty. All seven reference/mutant strings match architect output and all seven test files match independent output exactly. All parent canonical hashes match the immutable corpus; source metadata excluding the appended recovery transformation and rights match the parents and plan. The source remains McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, CC-BY-SA-4.0, with per-record hashes and recovery lineage preserved; this review does not reopen authorized provenance.

| Suffix | Candidate file SHA256 | `test_solution.py` content SHA256 |
|---|---|---|
| 0355 | a7c72e3734f4e8c446a10d64a813085f51956f177a0ebee60e5f29c117133833 | d764a2d45b266f7b8c20e7863fc6f3122c2c446dede4db3a45078ede62942a0d |
| 0445 | 4daab5435aa5e2406eb132427ab69a9e8290fab0311ce35a9b97f73ced5761a3 | cb3e5ce49dbb877a186bb34dc397b1e1d7c699b87661211e4b5a3e4bf9dda3f0 |
| 0298 | f6b332207949880489f4a1bf99e59358b4c9242f2d479eb3bedb73c43febe254 | baab3c3a5100f26d9d7956caae16f9a3087c28a7a961f6d2c33f5c66a5604d90 |
| 0314 | 3fed262cc490e71917f49eeeef64c12c20ceb7befa0115b88453cf1651eb072f | 30dffc4d87e283685cd78c6975f4b6f0f6da7db6f1bc8fd86602b60f6d9a27e0 |
| 0319 | 7d0b4bb1768a760b84fbe385071b154358917ad1e3b3fefdbbb40e5ea26c2181 | be09dfe3eab051f9e315adcbd81fa4372dd4ec3a4172d1e7826ee3bc3a81b6b3 |
| 0269 | b33e7cbf6d77ffc3d6cdbc4d62d9aeb444418c60ca95492d956e79f60ca45fab | 1e59931a3b99c812dbbf8abfe8f9148cc41a32c227737a0665ada029f7bf72b1 |
| 0672 | eab00fc8738a13834de02e0f9b5a5f57909f6ca79bbae7b3363b67d6b816760a | 9d4e56d74e7cc0cc7c140f4ba29a76903f72aa0bce478e7ce3b69e9680fdd694 |

Static positives remain subject to the main agent's separately preserved serial sandbox diagnostics and admission gates. No automatic correction loop is requested by this report.
