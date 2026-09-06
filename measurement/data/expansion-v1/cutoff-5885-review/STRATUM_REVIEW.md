# Quality follow-up decision

Current checkpoint: **1033 holds (1030 additive plus historical three)**; 2,718
unique outside-sample inspections. All 544 array queue positions inspected;
Rust generation queue complete: 684 of 684 inspected.
Python generation queue complete: 684 of 684 inspected; batches 45–46 backed up.
Python repair queue complete: 426 of 426 inspected; all 29 batches backed up.
JS/TS residual queue: 375 of 587 checkpointed; continue376. Batch25 awaits backup.
GCS authentication restored; Python repair archive through 426 now verified.
GCS verified through 1028 holds / residual batch24 / 2,703 outside-sample inspections.
See QUALITY_STRATUM_1028_BACKUP.md. Scope v6: 11 groups, 14 strata, 3,085 records.
See JS_TS_RESIDUAL_REVIEW_25.md. Remaining strata and quality criteria are pending;
inspection is not admission. All 97 data tooling tests pass.
No training seal or new VM. Older entries are historical.

V6 adds contradictory_suffix_uniqueness, supported by TS generation0173/0190.
Scope: 11 groups / 14 strata / 3,085 review records (not rejection count).
Decision SHA-256: `361cd6f09f19585bd01e5286414bec22afcc252050c1488665cf853ff487566f`.
Report SHA-256: `0510ab4e2d1122715ecd7c3c3feec3267042f5a284e3c17eb01013404e71db26`.
Previous inventories remain preserved.

Current checkpoint: **223 holds (220 additive plus historical three)**; 308
unique outside-sample inspections. Batch 20 complete through position 300;
continue 301. GCS verified through 217 holds / batch 19; batch 20 awaits backup.
No training seal or new VM. Older entries are historical.

Current checkpoint: **217 holds (214 additive plus historical three)**; 294
unique outside-sample inspections. Batch 19 complete through position 285;
continue 286. GCS verified through 209 holds / batch 18; batch 19 awaits backup.
No training seal or new VM. Older entries are historical.

Current checkpoint: **212 holds (209 additive plus historical three)**; 284
unique outside-sample inspections. Batch 19 partial through position 275;
continue 276. GCS verified through 209 holds / batch 18 / scope v5 (10 groups,
14 strata, 3,085 review records). Latest five inspections await backup.
No training seal or new VM. Older entries are historical.

V5 adds JS generation0204 to the existing JavaScript test-accommodation group.
Scope remains 10 groups / 14 strata / 3,085 records, not rejections.
Decision SHA-256: `f21e0ac56134e94b135c2543019875bd7855d4e44221e1e71612c04fdcc9cdf3`.
Report SHA-256: `7adfccbdb8504cc62e5cc086ce421dcf022c64e56bd7a2f4500bb06cf27432de`.
Previous inventories remain preserved.

Current checkpoint: **209 holds (206 additive plus historical three)**; 279
unique outside-sample inspections. Batch 18 complete through position 270;
continue 271. GCS verified through 200 holds / batch 17; batch 18 awaits backup.
No training seal or new VM. Older entries are historical.

Current checkpoint: **200 holds (197 additive plus historical three)**; 264
unique outside-sample inspections. Batch 17 complete through position 255;
continue 256. GCS verified through 189 holds / batch 16. Batch 17 pending backup.
No training seal or new VM. Older entries are historical.

Current checkpoint: **191 holds (188 additive plus historical three)**; 254
unique outside-sample inspections. Batch 17 partial through position 245;
continue 246. GCS verified through 189 holds / completed batch 16. Latest five
inspections await backup. Scope v4 remains 10 groups / 14 strata / 3,085 review
records, not rejections. No training seal or new VM. Older entries are historical.

V4 report SHA-256: `73f184c662a13cb55e4464990feb5abe85c427bb191387317b9cab95194104e3`.
Explicit follow-up decisions SHA-256:
`7fdb307e645c71bcdbf7ce60e29fa0fb8dc6d07e091808ed0b62056e19eed639`.
JS repair0088/0113 extend the test-accommodation evidence to JavaScript repair;
that stratum is already reopened, so population scope does not increase.

Latest: **178 holds (175 additive plus historical three)**; 234 unique outside-
sample inspections. Batch 15 complete through position 225; continue 226.
Scope v4: 10 groups / 14 strata / 3,085 review records, not rejections. GCS
verified through 168 holds; batch 15/v4 pending. Frozen 300/partition unchanged.
No training seal or new VM. Earlier checkpoints below are historical.

Latest: **171 holds (168 additive plus historical three)**; 224 unique outside-
sample inspections. Batch 15 partial through position 215; continue 216.
GCS verified through 168 holds; later five inspections pending. All 97 tooling
tests pass. Frozen 300/partition unchanged. No training seal or new VM.

Latest: **168 holds (165 additive plus historical three)**; 219 unique outside-
sample inspections. Array batch 14 complete through position 210; continue 211.
GCS verified through 159 holds; batch 14 pending. Frozen 300/partition unchanged.
No training seal or new VM. Earlier checkpoints below are historical.

Latest: **159 holds (156 additive plus historical three)**; 204 unique outside-
sample inspections. Array batch 13 complete through position 195; continue 196.
GCS verified through 149 holds; batch 13 pending. Frozen 300/partition unchanged.
No training seal or new VM. Earlier checkpoints below are historical.

Latest: **149 holds (146 additive plus historical three)**; 189 unique outside-
sample inspections. Array batch 12 complete through position 180; continue 181.
GCS verified through 139 holds; batch 12 pending. Frozen 300/partition unchanged.
No training seal or new VM. Earlier checkpoints below are historical.

Latest: **139 holds (136 additive plus historical three)**; 174 unique outside-
sample inspections. Array batch 11 complete through position 165; continue 166.
GCS verified through 129 holds; batch 11 pending. Frozen 300/partition unchanged.
No training seal or new VM. Earlier checkpoints below are historical.

Latest: **119 total holds** after array batch 9; initial sample unchanged.

Scope v3: **nine groups / 14 strata / 3,085 records** require resolution, not
automatic rejection. Two added groups bind repeated prototype-key storage loss
and required-property copy loss to executed diagnostic/candidate hashes.
`followup-systematic-groups-v3.json` and `stratum-followup-inventory-v3.json`
preserve v1/v2. Report SHA-256:
`9e684fb786c217c67f68037b30bea000b7dbc0adee91a55dfef47abc2596e7a6`.
All 97 data tooling tests pass. No automatic labels or frozen-sample enlargement.

Latest: **110 total holds** after array batch 8; initial sample unchanged.

Latest: **104 total holds** after array batch 7; initial sample unchanged.

Latest: **96 total holds** after array batch 6; initial sample unchanged.

Latest: **89 total holds** after array batch 5; initial sample unchanged.

Latest: **85 total holds** after array batch 4; initial sample unchanged.

Latest: **78 total holds** after array batch 3; initial sample unchanged.

Current scope v2: seven systematic groups reopen **13 strata / 3,056 records**.
The added finite-intermediate-arithmetic group binds executed JS generation0017,
TS repair0014 and Python repair0473 diagnostics to their immutable candidate
hashes. `stratum-followup-inventory-v2.json` preserves original sample size 300;
outside-sample evidence does not enlarge it. This is review scope, not rejection.
The original v1 report remains unchanged. All 97 data tooling tests pass.
The 72-hold checkpoint is GCS roundtrip verified; v2 scope postdates that archive.

Latest: **72 total holds** after array batch 2; see `ARRAY_STRATUM_REVIEW_2.md`.
The v1 systematic scope remains a minimum, not clearance of other strata.

Current count: 60 additive holds plus three historical (63). Array batch 1
adds ten held records, with a passing directory sparse control. See
`ARRAY_STRATUM_REVIEW.md`. Earlier scope/disposition details follow.

The original verification campaign is complete, with candidate exceptions.
The frozen sample's initial inspection is complete, but its quality gate does
not pass. This is not a judgment that every passing VM candidate is defective.

There are now 50 additive candidate holds plus the three historical holds (53).
`TARGETED_STRATUM_REVIEW.md` records ten outside-sample targeted inspections,
ten reproduced diagnostic failures on eight new held records, and one passing
first-match unsubscribe control. The following describes the earlier 45-hold
checkpoint and frozen v1 scope; it is not a revised partition.
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
- API consistency: not cleared. Fifty-three concrete holds include runtime
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

The small high-signal subscription/overload inventory is now inspected, with
false positives preserved in the targeted report. Next distinguish validation on external arrays from safe
internal-array callbacks, and review relevant numeric and API cases. Preserve
negative controls and false positives. Resolve strata through documented,
versioned changes and revalidation, not silent candidate edits or resampling.
Generation remains closed at 5,885; no new VM or training is started.
