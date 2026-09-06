# Quality follow-up decision

The original verification campaign is complete, with candidate exceptions.
The frozen sample's initial inspection is complete, but its quality gate does
not pass. This is not a judgment that every passing VM candidate is defective.

There are 42 additive candidate holds plus the three historical holds (45).
Four JS generation sparse-array failures were reproduced after the initial
300-record archive: recipe 0233 (359 ms), activity 0173 (380 ms), shipment
0206 (509 ms), workshop 0319 (362 ms). All exited 1 without timeout in the
pinned sandbox. These join three JS repair and one TS generation sparse holds.

The frozen contract requires reopening affected strata for systematic defects.
`stratum-followup-inventory-v1.json` maps six established recurring groups to
11 unique lane/source/task-type/correction-history strata, containing **2,567
records**. That number is review scope, not 2,567 rejected examples. It is a
minimum established scope; numeric-envelope and non-triviality adjudication
can add further groups. The other 3,318 are not automatically cleared.

| Recurring group | Records in associated strata |
| --- | ---: |
| Sparse element validation | 655 |
| Subscription registration identity | 535 |
| Reference accommodating incorrect tests/API | 211 |
| Incomplete Rust generation API | 614 |
| Python mapping support | 597 |
| Python invalid-enum exception behavior | 720 |

Groups overlap; do not add the rows for a unique population total. The inventory
binds every record to its immutable candidate line and canonical hash. Its
heuristics flag 571 JS/TS collection-callback references, nine listener-index
references, three subscription-owner references, three public find overloads,
and one exact Rust data/x:y exception. These are search hits, not automatic
semantic defects. Some match multiple patterns; many collection callbacks
operate on internally constructed dense arrays and are valid.

## Seven-criterion disposition

- Prompt clarity: not cleared. Repeated missing exact Rust APIs and conflicting
  validation/normalization/error boundaries need versioned specification work.
- API consistency: not cleared. Forty-five concrete holds include runtime
  contradictions, unsupported required inputs, and static reference/test conflicts.
  TypeScript repair0208's false non-null overload is a direct API violation.
- Test independence: archived provenance established for all 300: 297 original
  specification-only test outputs and three specification-only critic chains.
  This is procedural independence, not semantic oracle correctness. Incorrect
  tests plus test-accommodating reference changes still block quality approval.
- Non-triviality: not cleared. Several tasks reduce to a literal lookup, one
  explicitly described operator replacement, or a library wrapper. Do not invent
  a lines-of-code threshold or count these as approved because tests passed.
- Idiomatic code: not cleared globally. In particular, test-specific exceptions
  and unsound overloads cannot be endorsed as training targets; remaining notes
  include unnecessary compression and unclear numerical/runtime envelopes.
- Dependency isolation: inspected sample uses standard-library/pinned support
  dependencies and original execution was network-disabled. All new candidate
  execution uses the unchanged pinned sandbox. This does not clear other criteria.
- Realistic known-bad failure: not cleared globally. Go 0058's original mutant
  escapes rejection in 2/64 trials; JS 0160 depends on an unspecified return.
  Other individual mutation rationale is recorded in the four batch notes.

This is a fail-closed quality disposition, not an all-record boolean review
fabricated from pattern matches. Original quality-review.json remains pending
and immutable. No revised admission partition or training-ready seal exists.

## Current work

First inspect the small, high-signal subscription/overload pattern inventory
outside the sample. Then distinguish validation on external arrays from safe
internal-array callbacks, and review relevant numeric and API cases. Preserve
negative controls and false positives. Resolve strata through documented,
versioned changes and revalidation, not silent candidate edits or resampling.
Generation remains closed at 5,885; no new VM or training is started.
