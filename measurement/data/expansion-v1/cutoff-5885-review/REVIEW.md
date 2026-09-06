# Cutoff quality review — in progress

Current checkpoint: **975 holds (972 additive plus historical three)**; 2,508
unique outside-sample inspections. All 544 array queue positions inspected;
Rust generation queue complete: 684 of 684 inspected.
Python generation queue complete: 684 of 684 inspected; batches 45–46 backed up.
Python repair queue complete: 426 of 426 inspected; all 29 batches backed up.
JS/TS residual queue: 165 of 587 checkpointed; continue166. Batch11 awaits backup.
GCS authentication restored; Python repair archive through 426 now verified.
GCS verified through 973 holds / residual batch10 / 2,493 outside-sample inspections.
See QUALITY_STRATUM_973_BACKUP.md. Scope v6: 11 groups, 14 strata, 3,085 records.
See JS_TS_RESIDUAL_REVIEW_11.md. Remaining strata and quality criteria are pending;
inspection is not admission. All 97 data tooling tests pass.
No training seal or new VM. Older entries are historical.

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

Latest: **129 holds (126 additive plus historical three)**; 159 unique outside-
sample targeted inspections plus unchanged 300 sample. Batch 10 preserved;
continue array-hit position 151. GCS verified through 119 holds, batch 10 pending.
No new VM, revised partition or training seal. Earlier checkpoint history follows.

Current: **119 holds**, 116 additive plus historical three; 144 unique outside-
sample targeted inspections. See `ARRAY_STRATUM_REVIEW_9.md`.

Current: **110 holds**, 107 additive plus historical three; 129 unique outside-
sample targeted inspections. See `ARRAY_STRATUM_REVIEW_8.md`.

Current: **104 holds**, 101 additive plus historical three; 114 unique outside-
sample targeted inspections. See `ARRAY_STRATUM_REVIEW_7.md`.

Current: **96 holds**, 93 additive plus historical three; 99 unique outside-
sample targeted inspections. See `ARRAY_STRATUM_REVIEW_6.md`.

Current: **89 holds**, 86 additive plus historical three; 84 unique outside-
sample targeted inspections. See `ARRAY_STRATUM_REVIEW_5.md`.

Current: **85 holds**, 82 additive plus historical three; 69 unique outside-
sample targeted inspections. See `ARRAY_STRATUM_REVIEW_4.md`.

Current: **78 holds**, 75 additive plus historical three; 54 unique outside-
sample targeted inspections. See `ARRAY_STRATUM_REVIEW_3.md`.

Current: **72 holds**, 69 additive plus historical three. Forty outside-sample
targeted inspections; `ARRAY_STRATUM_REVIEW_2.md` records the latest batch.

Current: **63 holds**, 60 additive plus historical three. Twenty-five targeted
outside-sample inspections; see `ARRAY_STRATUM_REVIEW.md`. All 92 tooling tests
pass; verified GCS checkpoint through 53 holds. Later batch remains additive.

Current: **53 holds**, 50 additive plus three historical. Ten targeted
outside-sample inspections reproduced ten failures on eight new held records;
one first-match control passed. See `TARGETED_STRATUM_REVIEW.md`. These are not
new frozen sample rows or an unbiased defect rate. Earlier checkpoints follow.

Latest: initial inspection complete; **45 holds** including three historical.
Six recurring groups reopen 11 strata (2,567 records of review scope, not
rejections). See `STRATUM_REVIEW.md`. All 86 data tooling tests pass. The
300/41-hold archive is GCS roundtrip verified; later follow-up remains additive.

Population: 5,885; deterministic sample: 300. Cutoff corpus SHA-256:
`3ca9209b51d36b9137d65f6f0424bfc369a662bd5af7f99666f4ecc60ee24e92`.
Prepared manifest SHA-256:
`0a58d3d30f98202bd6fd87fafb1c7ddb415a2fabbfa21f6378da0399e72b6623`.

Initial inspection complete: **300/300**, indices 0–299. Counts: Go 56, Java 60,
JavaScript 30, Python 61, Rust 62, TypeScript 31. `FOURTH_BATCH_REVIEW.md`
preserves the last 135 inspections and focused Python/Rust/TypeScript findings.
`additional-holds.json` contains 38 additive holds; 41 with the original three.
These are not the complete rejected set or a sealed admission count. Repeated
sparse validation, subscription identity, API/test accommodation and numeric
envelope issues require affected-stratum review. Seven TS probes reproduced
defects; one CSS hypothesis was disproved. All 82 data tooling tests pass.
Inspection is not automatic seven-criterion approval. Original artifacts and
the v1 partition remain unchanged. The following is the historical 100 checkpoint.

This is a partial review, not a passed sample. One hundred candidate specifications,
reference implementations, original tests, and known-bad implementations have
been read: frozen sample indices 0–99. The earlier Go repair 0465 follow-up is
index 37 and counted only once. The remaining 200 have not had semantic review.
Archived test-origin checks now trace all 300: 297 unchanged specification-only
test-author outputs and three specification-only test-critic chains. The earlier
295/300 audit remains unchanged. This automated trace is not 300 semantic
reviews or a quality seal. See `test-origin-all300-chains.json`.
See `test-origin-all300.json`, `FIRST_BATCH_REVIEW.md`, and
`SECOND_BATCH_REVIEW.md`. New sandbox-confirmed holds: Go 0330 (label keys),
0720 (ready-step order), and 0791 (JSON key case); Java 0514 (null suffix) and
0794 (final no-swap pass). Static contract/test holds:
Java 0549 (missing-ID lookup) and 0080 (configuration preservation). These are
additive exclusions in `additional-holds.json`, not changes to original records.
Together with the three historical partition holds, eleven records are held;
excluding those eleven would leave 5,874 before other open findings are adjudicated.
No revised partition or training seal has been created. Repeated exception/API
ambiguities and elementary tasks require criterion-specific adjudication and
affected-stratum review; passing execution does not clear them.

## Confirmed gap: exp-v1-go-generation-0165

The ticket registry's Consume deletes any existing ticket, including one whose
start tick is in the future. The specification allows deletion for currently
valid and expired tickets; a not-yet-valid ticket is neither. Existing tests
cover Check before start, Consume while valid, and Consume when expired, but
omit Consume before start followed by Check at start.

`probe_test.go` was executed as `cutoff_review_test.go` with the original
reference code and original go.mod in the pinned network-disabled Go sandbox.
It failed normally with exit 1, no timeout, in 28,132 ms. `probe-result.json`
preserves the actual result. The original candidate is unchanged and is bound
through the cutoff manifest's candidate origins and task hash.

Disposition: blocks passing this sample. Correct and independently re-admit,
or exclude with an explicit derived-corpus manifest. Audit temporal lifecycle
tasks for the same test gap before deciding whether the defect is systematic.
Passing original tests in final re-execution cannot waive this finding.

## Other inspected rows

- `exp-v1-go-generation-0251`: alias directory. Static inspection found the
  advertised validation, atomic batch, insertion order, copied slices, and
  mutex protection implemented. Tests exercise these properties and reject
  the missing-prefix-separator mutation. No defect identified in this read.
- `exp-v1-go-generation-0491`: attempt policy. Static inspection found total
  attempt bounds, halt-before-repeat precedence, original error identity,
  nil validation, and wrapping implemented. Tests cover the principal paths;
  the strict-upper-bound mutation is a plausible failure. No defect identified
  in this read. Neither row has a completed seven-criterion sign-off yet.

Final VM re-execution is complete. Training remains blocked by incomplete
review. The original ticket finding is held out in review-partition-v1; the
additional stock-ledger finding below must also be held out before sealing.

## Confirmed nondeterministic directionality: exp-v1-go-generation-0058

The stock-ledger known-bad implementation commits changes while iterating an
unordered map. The original atomicity tests can miss the defect when invalid
entries happen to be visited first. A pinned, network-disabled sandbox probe
ran the unmodified original suite in 64 fresh child processes for each code:
the reference passed 64/64; the known-bad passed 2/64 and failed 62/64.
Neither outer execution timed out. This is a test reliability defect, not a
newly demonstrated reference-code defect. Do not treat 2/64 as a population
estimate or alter the original VM report.

A second diagnostic retained the combined output and exit status of every
child trial: reference 64/64 passed, known-bad 0/64 passed. All 128 trial
records are present and neither run timed out. This does not negate the first
run's observed false accepts; the variation is consistent with the map-order
dependence. Keep both runs rather than selecting the more convenient result.
The full-output run is `stock-repeatability-trial-output-result.json`; each
result embeds its own exact diagnostic task, including the test version.

`stock_repeatability_test.go`, `stock-repeatability-result.json`, and
`scripts/data/probe_stock_repeatability.py` preserve the diagnostic and exact
inputs. The outer diagnostic deliberately reports nonzero to expose counts;
interpret its child counts, not the outer exit as reference failure.

Disposition: additional hold, separate from the three original held records.
The historical 5,882-row v1 partition is unchanged and must not be sealed as-is;
it still contains this row. Excluding it leaves 5,881 before any further review
exclusions. Audit map-order-dependent atomicity tests before signing off the
affected stratum. Go repair 0465 uses ordered slice changes and explicit
valid-then-invalid sequences; static review found it does not share this gap.
That single follow-up is not a corpus-wide systematic-defect clearance.
