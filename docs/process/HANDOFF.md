# Ganesh Mini 1.0 handoff

## Accelerated r3 generation active — 2026-09-08

Session49105 is generating14 approved derived proposals (8JS/6TS) concurrently
across two lanes, configured maximum3. Plan logical SHA
617a754bf9ae98a4e595077de132e15c5556db21554da5f7d98a9f88e236a712.
Registry datasets/cache/expansion-v1/versioned-recovery/r3 is reserved; never reuse
or duplicate it. At launch checkpoint only plan/run-contract exist; no candidate
completion or admission claimed. Check process/session and per-lane evidence.
See RECOVERY_R3_SELECTION_20260908.md and recovery-requests-r3.json.
All three recommendation notes have been main-read, but only these14 selections
have main scope approval and hash validation. Other43 remain queued, including
repair embedded-source contract decisions. Do not restart original quality review.

Generator now supports bounded lane concurrency, per-lane failure isolation,
deterministic output and immutable partial evidence. Partial failure does not
emit a complete candidates manifest. Run contract binds worker count/source SHA.
Admission preparation now automatically compares every saved hash-bound prior
recovery admission in the registry as well as retained originals and current
selection. Actual prior9 bindings validated. All144 data tests pass.

Next: inspect r3 outputs, independent quality review, serial pinned sandbox
directionality, then separation/admission. No training or VM; Gate2 remains open.
Admitted9, original holds2812, maximum combined3082, minimum gap918 unchanged.
Training/release estimates50%/35%; generation is running, not approval-blocked.
Next generation checkpoint ETA10–60 minutes low confidence; verified admission
requires further review/execution. Full delivery ETA remains ungrounded.
Latest verified GCS checkpoint is admission9; r3 is NOT remotely backed up yet.
Preserve terminal r3 evidence and verify GCS backup before any cleanup/teardown.

## First nine recoveries admitted; next selection in progress — 2026-09-08

**9 candidate admissions /0 rejected**, all generation: Go2,Java2,JS2,TS2,Python1,
Rust0. Read RECOVERY_ADMISSION9_20260908.md for exact IDs, execution and hashes.
All r1/r2 teacher and diagnostic/admission jobs have completed. r2 generated7;
all pass directionality, but Python0517 remains a static oracle hold. Rust0359
scope and0396 contract/test holds remain. No automatic repeated critic loops.
Go0761 also passed the actual pinned resource/network-limited go test -race.

Selection checked against3073 retained originals and546 evaluation tasks;
zero overlaps/rejections. Final training balance/seal is NOT passed. Original
2812 holds unchanged; maximum originals+admitted recoveries3082, at least918
additional admissions to4000 before further exclusions/token balance.
Artifact: measurement/data/expansion-v1/recovery-admission/selected9-v1/admitted.jsonl
SHA0f82c006387283c45d88270a431988dae6becc6167c8e15ae2eb7d1979ead45a.
139 data tests pass. Full r1 backup verified in GCS: QUALITY_CLOSURE_R1_BACKUP.md.
Terminal r2+admission9 archive and receipt verified by exact-generation download
and byte comparison; see RECOVERY_ADMISSION9_BACKUP.md. No teardown in progress.

Completed reviewer selection drafts (not main-read/approved yet):
rust421_450 Go/Java up to20 -> RECOVERY_TRANCHE_GO_JAVA_20_20260908.md;
rust451_480 JS/TS up to20 -> RECOVERY_TRANCHE_JS_TS_20_20260908.md;
rust391_420 Python/Rust up to20 -> RECOVERY_TRANCHE_PYTHON_RUST_20_20260908.md.
Go/Java20 and JS/TS20 proposed; Python/Rust17 (8 Python/9 Rust), shortfall3
explicitly deferred. All reviewers idle; do not dispatch duplicate selection work.
These57 proposals are excluded from the terminal admission9 backup until main
integration. Read the complete three notes and validate hashes before planning.
Exclude all12 first-tranche parents. Do not count drafts or force quota with weak
or ambiguous examples. Main reads final notes, validates hashes and minimal scope,
then freezes new versioned requests. Current local work needs no new approval.
No training job/VM. Training/release estimates50%/35%; next-selection/recovery
ETA30–90 minutes low confidence; full-delivery ETA still ungrounded until scale
recovery throughput and corpus sufficiency are established. Continue, not status-only.

## Recovery r1 verified; bounded test correction active — 2026-09-08

r1 generated12/12; serial sandbox diagnostics complete for all12 (36 program
executions). Four pass reference/mutant/original directionality, but only
TS0087 and Java0781/0788 also have main-accepted static quality positives.
Rust0359's unrequested trait additions remain a scope hold. Eight other r1
candidates have test/oracle/coverage failures; preserve them rather than patch
correct reference code to satisfy faulty tests. See RECOVERY_R1_INTEGRATION_20260908.md.
All six r1 review reports read/integrated; original review is closed and remains
2812 holds / at most3073 originals / at least927 admissions still needed.

r2 is one test-only correction for seven exact parents. Active session60992;
registry datasets/cache/expansion-v1/versioned-recovery/r2. Do not duplicate or
reuse versions. Python0220/0517 both pass sandbox directionality;0220 also
quality-positive,0517 retains an unsupported nested-cache concrete-type oracle
hold and must not enter an automatic further critic loop. Go r2 generated;
rust421_450 reviewing it; JS/TS r2 generation follows. All other reviewers idle.
Main next: integrate r2 reviews, serially verify remaining candidates, complete
Go0761 race qualification, then separation/dedup against evaluations and retained
originals. No recovered admission seal yet. New tooling tests total136 pass.
Original generation session94073 finished; commit fd81284 successfully pushed.
No training job/VM. Training/release estimated50%/35%; current work needs no new
approval. Correction/review ETA10–30 minutes low confidence, excluding unresolved
scope and whole-corpus sufficiency. Overall delivery ETA not yet supportable.
A new verified GCS backup of2812 closure/full r1 is the immediate preservation
step; r2 is still active and requires a later terminal backup. No teardown action.

## Original review closed; recovery r1 launched — 2026-09-08

The final E/U reconciliation adds49 holds: **2812 total** (2809 additive plus
three historical), at most3073 original unheld rows; at least927 additional
admissions needed before further exclusions and token balancing. Frozen sample
remains165 positive/135 held; exact outside coverage5222. Original5885 unchanged.
Main accepted ORIGINAL_REVIEW_CLOSURE_AUDIT_20260908.md and saved the hash-bound
original-quality-closure-v1.json. No required original review obligation remains;
this is review closure, NOT admission, corpus sufficiency, or training readiness.

Main selected12 held parents (two each Go/Java/JS/TS/Python/Rust), preserving
source/rights and exact canonical parent hashes. Requests: recovery-requests-r1.json;
plan: measurement/data/expansion-v1/recovery-plans/r1/plan.json,
SHA ff64db89a09b39d0ca9b19f2b7231ded79cbff17823b21be51d36ea4c0647fdb.
TS0064/0087 are explicit contract clarifications for optional undefined values;
Java0788 and Rust0396 also have explicit derived semantic rules. Rust0359 is
oracle-rebuild plus reference correction, not a silent original-test rewrite.

Generator launched locally in session94073 with frozen Codex teacher configuration;
check process and datasets/cache/expansion-v1/versioned-recovery/r1 before starting
anything else. One sequential architect/test pair per lane; tests see only derived
specifications. A reserved version is never reused, including interrupted attempts.
Each phase preserves raw evidence, including timeouts.126 data tests passed.
No recovered candidate is yet verified/admitted, and no training job or VM launched.
Next: inspect generation outcomes, preserve all failures, verify fresh controls and
references in pinned network-disabled sandboxes, then quality/separation checks.
No GCloud action occurred in this update. Current local work needs no approval.
Current2812 closure and r1 artifacts are not yet included in a new verified GCS
backup; latest verified remote checkpoint remains2763. Back up at next safe boundary.
Training/release estimates remain50%/35%, not measured completion metrics.
Overall ETA remains ungrounded until recovery yield and pilot throughput are measured.

## Copy/API delta complete; recovery planner tested — 2026-09-08

Current checkpoint **2763 holds** (2760 additive plus historical three), maximum
3122 original unheld; minimum878 recoveries before further exclusions/balancing.
C/J delta181 complete:12 holds/169 scoped positives. Five retained quality
questions adjudicated separately add3 holds (JS0004/0191 elementary;0047
supplementary capitalization);0027/0103 scoped positive. No new execution.
Unique outside5222 and frozen sample165positive/135held unchanged.
See final-delta-reconciliation-v1.json. Parent reports remain historical.
Recovery-plan builder scripts/data/plan_versioned_recovery.py and10 tests added;
113 data tests pass. New IDs, parent/source/rights/hold hashes, create-only outputs;
no candidate generation/admission or teacher calls. See docs/data/VERSIONED_RECOVERY.md.
No recovery selection until original systematic-quality reconciliation completes.
Active next queue js-elementary-capitalization-queue-v1.json:273 affected,
143 held,130 survivors. Existing C/J closed; only E and narrowly defined U.
rust391_420 positions1–44, rust421_45045–87, rust451_48088–130. Filter only
frozen prior_held false, preserve order. Isolated JS_FINAL_EU_* notes; main integrates.
All three drafts now complete but NOT integrated: proposed E holds17/11/21,
U has one scoped positive and129 not-applicable. Main must read/validate before
counting; reviewers currently idle. Next continuation integrates these drafts.
No new unique inspection scope or blanket Unicode review. Original data unchanged.
Training/release estimated50%/35%; no training job/VM. ETA overall remains
unreliable until recovery/admission throughput. Current work needs no approval.
2763 checkpoint archive/receipt exact-generation byte comparisons passed;
see QUALITY_DELTA181_2763_BACKUP.md. Includes recovery planner and pending
E/U queue, but excludes isolated JS_FINAL_EU reviewer drafts until integrated.

## Legacy criteria adjudicated — 2026-09-08

Current checkpoint supersedes older counts: **2748 holds** (2745 additive plus
three historical); maximum3137 original unheld rows. At least863 recoveries
needed before further exclusions and family-token balancing. The57 targeted
adjudications (52 scoped questions plus5 explicit out-of-membership caveats)
resolve27 holds and30 scoped positives, zero pending among those57.
Unique outside inspections5222 and sample165positive/135held unchanged.
See legacy-final-adjudication-20260908.json and LEGACY_FINAL_INTEGRATION_20260908.md.
Four Python Mapping witnesses executed: each exit1 without timeout; remaining
new findings are static only. No admission seal or training/VM launch.
Scope delta frozen in final-systematic-delta-queue-v1.json:357 affected IDs,
176 already held,181 survivors/326 criterion obligations. No new unique scope.
Active: rust391_420 TS36 C; rust421_450 JS positions1–73 C/J;
rust451_480 JS positions74–145 C/J. Filter frozen prior_held false and lane,
not changing current holds. Main integrates isolated FINAL_DELTA_* notes.
Do not silently treat prior per-ID coverage as closure of a newly expanded
criterion. Then versioned recovery implementation and fresh admission checks.
Training/release estimates50%/35%; overall ETA not grounded until recovery yield
and pilot throughput. No new authority needed for current in-scope work.
2748 checkpoint archive and receipt exact-generation byte comparisons passed;
see QUALITY_LEGACY57_2748_BACKUP.md. Scope delta/queue postdate that archive
and are preserved in the repository pending next batched GCS checkpoint.

## Python reconciliation complete — 2026-09-08

Current canonical checkpoint supersedes older counts below: **2721 holds**
(2718 additive plus historical three), maximum3164 original unheld rows.
Python numeric/elementary668/668 complete:216 new holds since queue start,
452 scoped resolved without hold, zero numeric pending. This integration adds
124 holds. All other criteria and prior caveats remain unresolved unless
separately adjudicated; this is not admission. Unique outside coverage5222;
frozen sample165 positive/135 held unchanged; all103 data tests pass.
See PYTHON_CRITERIA_COMPLETION_20260908.md and
python-criteria-reconciliation-v1.json. Original5885 candidates unchanged.
Repair0059 tiny-result probe: controls pass; target raises OverflowError,
exit1 in422ms without timeout. Evidence preserves pinned sandbox and hashes.
Remaining-scope audit completed. Exact-ID closure accounting now assigned:
rust391_420 Python Mapping/enum two groups; rust421_450 eight JS/TS/array
groups; rust451_480 four Java/Rust groups. Isolated notes only; main integrates.
Next: adjudicate concrete remaining quality gaps, then versioned recovery;
at least836 recoveries needed before further exclusions/family balancing.
Training/release estimates remain50%/35%; no training job or new VM launched.
Overall ETA remains ungrounded until recovery/admission and pilot throughput.
GCS archive and receipt verified by exact-generation byte comparison; see
QUALITY_PYTHON668_2721_BACKUP.md. Remaining-scope audit completed read-only:
14 older overlapping groups need evidence closure accounting, not automatic
bulk re-review. See REMAINING_QUALITY_SCOPE_AUDIT_20260908.md (post-archive).

## Accelerated review authorized — 2026-09-08

User explicitly authorized parallel reviewers, larger work batches and shorter
continuation intervals. Python draft batches4 (301–420),5 (421–540),6 (541–668)
are complete but NOT yet main-reviewed/integrated. Expected proposals34/43/37
holds respectively; validate before counting. Active independent followups:
rust391_420 -> PYTHON_NUMERIC_PENDING_FOLLOWUP_1.md (pending from1–300);
rust451_480 -> _2.md (pending batch4/6);
rust421_450 -> _3.md (pending batch5). They write only isolated notes;
no ledger edits or candidate execution. Check live status before redispatch.
Rust batches1–31 passed
main-agent queue, hold uniqueness, frozen-corpus and sample-binding validation.
Canonical Rust checkpoint is complete942:359 holds and583 scoped positives.
See rust-elementary-reconciliation-v1.json for exact IDs and note hashes.
Python queue python-criteria-followup-queue-v1.json freezes1110 outside records,
442 prior holds and668 pending;613 need both numeric and elementary review,
55 numeric only. All were previously inspected: zero new unique-row credit.
Main integrates Python notes against the frozen prior_hold-is-None order.
Python1–300 integrated:92 new holds,200 scoped resolved without hold,8 unheld
numeric questions pending. Ten numeric questions total include two already
held for elementary criteria. Do not equate reviewed300 with resolved300.
See python-criteria-reconciliation-through300.json. Next368 assigned.
Reviewers write only their own notes; main owns holds/state, validation and
batched commits/backups. Check live agents and draft files before redispatching.
No quality gates, GCloud compute boundaries or frozen data changed.

## Required status-update format — user instruction, 2026-09-07

Every status update must include two progress bars: inception-to-training
closure and inception-to-release delivery. Label milestone-weighted percentages
as estimates, distinct from measured row counts or training-step completion.
Include ETA ranges and assumptions, confidence, current activity (running,
idle, or blocked), the immediate next action, and any approval needed.
Never imply background work continues when no job or scheduled continuation
is running. Release ETA is conditional on frozen gates passing; distinguish
release-decision readiness from guaranteed public release.

Planning estimate at this checkpoint: training closure about50%, overall
release delivery about35%. These are judgment estimates, not executed metrics.
Earlier3–5-day training and5–10-day release estimates are withdrawn as unreliable.
The old serial-review ETA is superseded by authorized parallel review;
552 further Rust records were integrated since390, completing that scope.
Python368 unreviewed remain plus8 unheld numeric questions. A reliable
overall ETA still needs recovery/admission and pilot throughput. Percentages
are unchanged planning estimates, not executed metrics or calendar commitments.

## Quality review continuation — 2026-09-06

Current checkpoint: **2597 holds (2594 additive plus historical three)**;
5,222 unique outside-sample inspections. All 300 frozen sample records now have
seven-criterion dispositions: 165 positive, 135 held. By lane: Go 39/17,
Java 29/31, JavaScript 10/20, Python 32/29, Rust 41/21, TypeScript 14/17
(positive/held). See SEVEN_CRITERIA_*.md and sample-criteria-reconciliation-v2.json.
All 103 data-tooling tests pass. Review positives are not admission.

Old focused queues completed: arrays544, Rust generation684, Python generation684,
Python repair426, JS/TS residual587. Historical v6 coverage is reconciled.
Latest scope v14: 21 groups, 21 strata, 5,500 records (278 sample, 5,222 outside).
Java sample positives reconciled against null-query/percentage/page patterns;
five blank-domain holds added. See JAVA_SAMPLE_SCOPE_RECONCILIATION_V2.md.
New criterion scopes require explicit reconciliation against existing notes;
no automatic reuse or new-inspection credit. Go non-triviality757/757 complete.
Java combined queue1112/1112 complete (684 generation,428 repair total).
RESUMED2026-09-07: user approved review completion and versioned recovery.
Next: Python/Rust scope reconciliation, then versioned recovery.
Additional non-triviality
scopes: JS repair200, Python993, Rust1006, TS generation262 (overlap prior
semantic inspections; these are not additive unique-record counts). Python
numeric scope1110 must be reconciled with prior numeric evidence.

GCS verified through2597 holds including Rust942 and Python1–300.
See QUALITY_PYTHON300_2597_BACKUP.md. JS elementary queue200:76 already held;
unheld124/124 reconciled with60 new holds and64 criterion positives. JS outside
scope complete and backed up. TypeScript queue262:107 initially held;
unheld155/155 reconciled:57 new holds and98 criterion positives. TypeScript outside
elementary scope complete; batches1–5 and four diagnostic probes are GCS verified.
Rust elementary queue1006 is now frozen:64 prior-held exclusions and942 requiring
criterion reconciliation. All942 reconciled:359 holds,583 scoped positives.
423 first-time repair inspections add unique coverage. Rust scope complete.
Rust through942 and all ten diagnostic probes are GCS verified.
Archive and receipt passed exact-generation byte comparison; originals unchanged.
Rust scope and two new numeric probes are backed up. Python1–300 integrated:
92 holds,200 scope-resolved without hold,8 unheld numeric pending; backup verified.
Canvas0215 public-width change panics on valid coordinate: compile0/test101.
Generation0322 checksum overflow is static only; no large allocation executed.
Repair0181 returned origin0 outside half-open range; repair0186 returned zero
density for finite MAX sigma. Both probes compiled then failed without timeout.
Repair0171 has a static empty-envelope credential-collision contract hold;
no new executed failure claimed. See RUST_ELEMENTARY_REVIEW_11.md.
Recovery tooling preflight read: existing rejection-repair script cannot directly
process semantic holds or supply new candidate identities; see
RECOVERY_TOOLING_PREFLIGHT_20260908.md. No recovery/training was launched.
Active5-minute continuation: continue-ganesh-mini-to-release-gates, created
2026-09-08, accelerated with explicit parallel-review authorization.
Resume work from saved position; preserve all approval boundaries.
Repair0093 finite arithmetic and repair0095 Default IDs both compile then fail.
Two large-array probes failed, one exact-progress probe failed, and a date-suffix
probe passed. See TYPESCRIPT_ELEMENTARY_REVIEW_1.md through _5.md.
Executed generation0710 batch overflow and repair0460 forbidden negative zero;
see JAVA_RECOVERY_PROBES_20260907.md. Both compile, then fail assertions/runtime.
Earlier evidence has exact-generation roundtrip proof. Frozen inputs unchanged.
Prior page arithmetic reconciled; generation0716 eager-allocation hold added.
See JAVA_PAGE_RECONCILIATION_20260907.md. Cross-lane scopes remain open.
At most3288 rows remain outside holds, below the planned4000 lower bound.
The user approved versioned recovery to address this shortfall without lowering
quality gates. See CORPUS_SUFFICIENCY_PAUSE_20260907.md for the resolved pause.
No training seal or new VM. Complete review, then recover suitable held examples
with fresh checks and parent lineage; original5885 and admission gates unchanged.
Older entries are historical.

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

Current checkpoint: **189 holds (186 additive plus historical three)**; 249
unique outside-sample inspections. Batch 16 complete through position 240;
continue 241. GCS verified through 178 holds / batch 15 / scope v4.
Batch 16 awaits backup. No training seal or new VM. Older entries are historical.

Current checkpoint: **184 holds (181 additive plus historical three)**; 244
unique outside-sample inspections. Batch 16 partial through position 235;
continue 236. GCS verified through 178 holds / batch 15 / scope v4.
Latest six holds await the next backup. No training seal or new VM.
All older entries below are historical checkpoints.

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

Latest: **131 holds (128 additive plus three historical)**; 164 unique outside-
sample inspections. Batch 11 partial covers positions 151–155; resume 156.
GCS verified through 129 holds; these latest five inspections are local only.
All 97 tooling tests pass. Frozen sample/partition unchanged; no training seal.

Backup update: 129-hold / batch-10 checkpoint is exact-generation GCS
roundtrip verified; see `QUALITY_STRATUM_129_BACKUP.md`. Next batch in progress.

Latest: **129 holds (126 additive plus historical three)**; 159 unique outside-
sample targeted inspections plus unchanged 300 sample. Batch 10 preserved;
continue array-hit position 151. GCS verified through 119 holds, batch 10 pending.
No new VM, revised partition or training seal. Earlier checkpoint history follows.

Current: **119 holds (116 additive plus historical three)**. Array batch 9 adds
15 inspections / nine holds / ten reproduced failures; 144 unique outside-
sample targeted inspections. Continue at array-hit position 136. Frozen sample
300 unchanged. GCS verified through 110 holds and v3 scope; batch 9 pending.
All 97 tooling tests pass. No new VM, revised partition or training seal.

Scope v3 now records nine systematic groups / 14 strata / 3,085 records,
NOT a rejection count. Key-storage/property-copy groups are candidate-bound.
All 97 tooling tests pass. Continue array inventory at position 121; batch 8
and v3 scope postdate the verified 104-hold GCS archive.

Current: **110 holds (107 additive plus historical three)**. Array batch 8 adds
15 inspections / six holds / seven reproduced failures; 129 unique outside-
sample targeted inspections. Continue at array-hit position 121. Frozen sample
remains 300. GCS verified through 104 holds; batch 8 pending. No training seal,
new VM or revised partition. All 97 tooling tests pass.

Backup update: evidence through 104 holds / array batch 7 passed exact-generation
GCS download/hash comparison; see `QUALITY_STRATUM_104_BACKUP.md`. Resume array
hit position 106; no change to frozen sample/partition or training readiness.

Current: **104 holds (101 additive plus historical three)**. Array batch 7 adds
15 inspections / eight holds / nine reproduced failures; 114 unique outside-
sample targeted inspections. Continue at array-hit position 106. Initial 300
unchanged. GCS verified through 96 holds (`QUALITY_STRATUM_96_BACKUP.md`); batch 7
pending. No new VM, revised partition or training seal. Tooling: 97 tests pass.

Current: **96 holds (93 additive plus historical three)**. Array batch 6 adds
15 inspections / seven holds / eight reproduced failures; 99 unique outside-
sample targeted inspections. Continue at array-hit position 91. Initial 300
unchanged. GCS roundtrip verified through 89 holds (`QUALITY_STRATUM_89_BACKUP.md`);
batch 6 pending. All 97 tooling tests pass. No new VM, partition or training seal.

Current: **89 holds (86 additive plus historical three)**. Array batch 5 adds
15 inspections / four holds / five reproduced failures and a passing control;
84 unique outside-sample targeted inspections. Continue at array-hit position
76. `ARRAY_STRATUM_REVIEW_5.md` distinguishes ambiguous inputs from defects.
GCS verified through 78 holds; later batches pending. No training seal/new VM.

Current: **85 holds (82 additive plus historical three)**. Array batch 4 adds
15 inspections / seven holds / nine diagnostic failures; 69 unique outside-
sample targeted inspections total. Initial sample still 300. Continue at array
hit position 61. `ARRAY_STRATUM_REVIEW_4.md` preserves scope and negative findings.
GCS verified through 78-hold checkpoint including v2 scope; later batch pending.
All 97 tooling tests pass. No new VM, training seal or revised partition.

Current: **78 holds (75 additive plus historical three)**. Array batch 3 adds
14 unique outside-sample inspections (54 total) and six reproduced failures.
ArchiveService 0026 is not double-counted. Continue at JS generation0035, array
hit position 46. See `ARRAY_STRATUM_REVIEW_3.md`. All 97 tooling tests pass.
No VM, generation restart, training seal or revised partition.

Scope update: v2 adds finite-intermediate arithmetic, now seven groups / 13
strata / 3,056 records of review scope, NOT rejections. All 97 data tooling
tests pass. The 72-hold checkpoint passed exact-generation GCS roundtrip;
see `QUALITY_STRATUM_72_BACKUP.md`. Numeric-scope v2 changes postdate that archive.

Current: **72 holds (69 additive plus historical three)**. Array batch 2 brings
outside-sample targeted inspections to 40, with nine more reproduced failures
and a passing parcel-filter control. See `ARRAY_STRATUM_REVIEW_2.md`. Next array
hit is JS repair-0015; initial 300 remains unchanged. Review numeric and
parameter-object systematic scope too. No training seal or new VM. Earlier
checkpoint details below; all data-tooling tests still 92 passing.

Current: **63 holds (60 additive plus historical three)**. `ARRAY_STRATUM_REVIEW.md`
adds 15 outside-sample inspections, ten reproduced failures and a passing sparse
directory control; 25 total outside-sample targeted inspections. All 92 data
tooling tests pass in `.venv`. The 53-hold checkpoint is GCS roundtrip verified
(`QUALITY_STRATUM_53_BACKUP.md`); later array batch awaits backup. Continue array
inventory at JavaScript repair-0008; do not repeat the first 15. No new VM,
generation, training seal, or rewritten partition. Earlier details follow.

Latest targeted follow-up: **53 holds (50 additive plus historical three)**.
Ten outside-sample pattern inspections, ten sandbox-confirmed failures on eight
new held records, and one passing JS first-match unsubscribe control. Frozen
sample remains 300/300; these are not new seven-criterion approvals. See
`TARGETED_STRATUM_REVIEW.md`. Probe helper now explicitly supports hash-bound
full-cutoff selection. No VM, training seal or revised partition. Next: external
array validation versus internal dense-array callbacks, then API/numeric review.
This follow-up awaits its new GCS checkpoint. Earlier checkpoint details follow.

Latest follow-up: 45 holds (42 additive plus historical three). All 300 initial
inspections are complete. Six recurring defect groups reopen 11 frozen strata
covering 2,567 records; this is review scope, not a rejection count. See
`STRATUM_REVIEW.md` and `stratum-followup-inventory-v1.json`. The initial
300/41-hold checkpoint passed exact-generation GCS roundtrip; later four JS
sparse probes and stratum inventory postdate it. All 86 data tooling tests pass.
Next: inspect high-signal subscription/overload hits outside the sample and
continue stratum resolution. The prior checkpoint details follow.

Initial semantic inspection is **300/300**, frozen indices 0–299. Go 56,
Java 60, JavaScript 30, Python 61, Rust 62, TypeScript 31. Inspection is not
seven-criterion approval. `FOURTH_BATCH_REVIEW.md` preserves the last 135
inspections. `additional-holds.json` contains 38 additive holds, or 41 with
the historical three. No revised partition, training seal or new VM.
Seven TypeScript probes compiled and reproduced behavioral defects without
timeouts; a CSS terminal-newline hypothesis was disproved and is not held.
Rust/Python probes, raw outputs and exact diagnostic tasks are also preserved.
All 82 data tooling tests pass. Next: criterion-specific adjudication and
related-stratum audits for sparse validation, subscription identity, API/test
accommodation, numeric envelopes and elementary tasks. In particular Rust
0192 and TypeScript 0382/repair0208 contain test-accommodating reference changes.
Continue locally; do not restart generation or infer training readiness from
the historical 5,882-row partition. All candidate execution stays sandboxed.

The paragraph below records the earlier 100-record checkpoint:

Semantic inspection is now 100/300: frozen indices 0–99. Go repair 0465 at
index 37 is counted once. Archived provenance now traces all 300: 297 unchanged
specification-only original tests and three specification-only critic chains.
Nine focused provenance tests pass. See the review directory's
`SECOND_BATCH_REVIEW.md` and `test-origin-all300-chains.json`.

New hold: Go generation 0058 has nondeterministic known-bad rejection. Its
unchanged original tests passed the known-bad 2/64 times in fresh sandboxed
processes; the reference passed 64/64. Preserve the original VM evidence.
The v1 5,882-row partition is unchanged and still contains this additional
hold. Additional sandbox-confirmed reference defects: Go 0330, 0720, 0791;
Java 0514, 0794. Static contract/test holds: Java 0549, 0080. Eleven total holds
including the historical three would leave 5,874 before open findings are
adjudicated. No revised partition or training seal exists. Continue sample
order at index 100; do not end work at this checkpoint. Repeated API/exception
ambiguities and elementary-task non-triviality questions remain open. Audit
related atomic-map/temporal/early-return-validation cases. No new cloud compute
was used for this review; local probes use pinned network-disabled sandboxes.

## Completed verification and separate review — 2026-09-06

The native VM run completed 5,885 records: 5,883 passed and two Rust references
timed out (`exp-v1-rust-generation-0161`, `exp-v1-rust-generation-0224`).
Navneet directed reviewing flagged records separately and continuing with the
passing corpus. Preserve the original strict-seal report (`status=failed`)
as executed evidence; this is a completed verification run with exceptions.
The separate partition under `datasets/cache/expansion-v1/review-partition-v1/`
holds those two plus the independently confirmed Go quality defect, leaving
5,882 review-eligible rows. Quality review is incomplete; no training seal.

All 13 VM artifacts were verified from GCS before VM/disk/network/subnet
deletion. Both project-wide Compute inventories were empty. Cloud Asset API
is disabled, leaving broader non-Compute billing verification unresolved.
Do not claim GCS-only billing without resolving that gap. No VM remains to
stop. Local source/candidate/teacher history is additionally archived to the
campaign's `archive/` prefix so lineage survives independently of this laptop.
The full-history archive is 122,389,351 bytes, generation `1788638543675053`,
and passed an exact-generation download/SHA-256 roundtrip. See
`measurement/data/expansion-v1/cutoff-5885-review/BACKUP_COMPLETION.md` for its
hash and scope. Follow-up SQL, GKE, Artifact Registry, and Cloud DNS listings
were also empty; these do not close the broader billing-audit gap.

## VM verification campaign — 2026-09-05

Latest user instruction: after VM work completes, save all evidence and data
in GCS, verify those backups, then tear down the VM and related resources.
Perform two post-teardown checks for non-GCS chargeable resources. The watcher
now requires the backup inventory and resource identity to roundtrip through
GCS before deletion, and uploads two project-wide resource inventories spaced
60 seconds apart after teardown. Review scan errors and non-Compute assets;
do not equate resource absence with instantaneous zero billing, because usage
postings can lag. Preserve and report any unrelated resources rather than
deleting them under this campaign's cleanup authority.

Navneet approved a 16-vCPU CPU verification VM with a $15 pre-tax budget and
eight-hour runtime ceiling. Private VM `ganesh-mini-verify-20260905` in
`executespecv1/us-central1-a`, instance ID `5175709884199568151`, started at
2026-09-05 16:06 UTC. Provider maximum duration is 28,800 seconds with STOP;
automatic restart is disabled. See
`measurement/data/expansion-v1/cutoff-5885-review/VM_EXECUTION.md`.

VM results are under
`gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/verification/cutoff5885-20260905/results/`.
Qualification compares 1/4/8 workers, then the fastest passing setting verifies
the complete cutoff. This is execution only; quality review remains incomplete.

Qualification passed 12/12 at every setting: 85.059 seconds with one worker,
31.645 with four, 32.018 with eight. The VM selected four and started full
verification. The redundant laptop admission process was stopped after this
qualification passed. Do not restart either laptop generation or verification.

Local launchd job `com.ganesh-mini.vm-cutoff-watch` runs the finite evidence
retrieval/cleanup watcher. Its logs and verified downloads are under
`artifacts/verification/cutoff-5885-vm/`. It verifies instance identity and
downloaded object checksums before removing the named VM/disk/subnet/network.
If backup is incomplete it fails closed and retains the stopped disk. Check
watch.err.log and resource-absence.json before claiming cleanup succeeded.

## Latest override — user cutoff, 2026-09-05

Construction is stopped at 5,885 rows by Navneet's instruction. The original
production state still says running; preserve it as historical evidence and
do not restart generation. Batch 144 is excluded. Use the manifest under
`datasets/cache/expansion-v1/cutoff-5885/` for the accepted cutoff. Its status
is pending final execution and quality review. All 5,885 original executable
candidates were recovered by matching their admitted task and content identity.

The active final-admission launchd label is
`com.ganesh-mini.cutoff5885-final-admission`. Logs and eventual final report
are in the cutoff directory. The intended command is:

```bash
.venv/bin/python -m scripts.data.admit_expansion \
  --config datasets/cache/expansion-v1/cutoff-5885/cutoff.config.json \
  --input datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl \
  --output datasets/cache/expansion-v1/cutoff-5885/final.admitted.jsonl \
  --report datasets/cache/expansion-v1/cutoff-5885/final.admission.json \
  --record-workers 1 --verifier-workers 1 --seal
```

Do not launch a duplicate. The older command below using admitted training
rows is invalid: admission requires executable candidate objects. Eight-way
verification is also superseded. Review the 300 original executable candidates
in `quality-sample.candidates.jsonl`; record actual review findings separately
from the immutable pending selection report. Full execution and quality review
must pass before token balancing and a bounded training pilot.

Review progress: 3/300 records inspected; the review is incomplete. A focused
sandbox counterexample confirmed a missing temporal edge case in
`exp-v1-go-generation-0165`. See
`measurement/data/expansion-v1/cutoff-5885-review/REVIEW.md` and its executed
probe evidence. Passing the original tests cannot waive this defect. Resolve
it and audit related lifecycle tasks before a quality sign-off. The full
suite reproduced the same three historical readiness/workspace failures;
20 focused cutoff/admission/sampling tests passed.

Last verified snapshot: 2026-09-04 14:38 IST

This document is an operational handoff, not a replacement for the canonical
plan or evidence. Live state can advance after the timestamp above. Re-read the
files in the "Start here" section before acting.

Continuation update: 2026-09-04 16:36 IST

- Commit `3632f23` is pushed to `origin/main`.
- Batch 111 was recovered from exact hash-bound candidate/teacher evidence
  using one verifier container. It admitted 8/10 rows: four generation and
  four repair. Two corrected rows remained behavioral rejects.
- Live corpus is 5,616/6,000: Go generation 474/720 and repair 342/480; every
  other lane is complete. Corpus SHA-256 is
  `02d7598aae42064d4cb38a3acedfc5d01dd1484f6b379ee7d13c90879af83ac4`
  and matches production state.
- The single launchd controller is running batch
  `go-0112-g0678n6-r0452n4`. Production admission now defaults to one record
  and one verifier container because the attempted eight-container setting
  caused host-contention timeouts under AMD64 emulation. Timeout status remains
  contextual: a timeout that persists when serialized is a behavioral failure,
  as proven by batch 111's malformed generated test.
- `scripts/data/build_expansion_quality_sample.py` now implements and tests the
  missing deterministic 300-row review sample. It remains intentionally
  blocked until the corpus reaches exact quotas and complete state.
- The full suite still has the same three known stale Gate 1/workspace failures;
  353 tests passed and one optional Docker test was skipped. Focused data and
  verifier tests pass.

This continuation update supersedes older live counts, concurrency guidance,
and the immediate batch identity below. Preserve the older text as timestamped
historical context.

Continuation update: 2026-09-05 09:34 IST

- Batch 128 failed before corpus commit because a verifier subprocess emitted
  invalid UTF-8 and Python attempted implicit text decoding. Docker verifier
  output is now captured as bytes; valid UTF-8 remains direct text and invalid
  UTF-8 is preserved exactly in a `base64:` envelope.
- Focused verifier and expansion tests pass: 35 passed. Exact recovery reused
  the recorded hash-bound candidate and teacher evidence. First-pass admission
  accepted 9/10; the remaining behavioral rejection passed the one permitted
  correction, so the batch atomically admitted 10/10.
- At the recovery checkpoint the corpus was 5,769/6,000: Go generation
  564/720 and repair 405/480, with every other lane complete. Corpus SHA-256
  `1a99cd89e3172300d4aadd1d10cb24b383ca9f6de581223f4aef310e2eb499c5`
  matched state and aggregation rejections were zero.
- The single launchd controller was restored and opened
  `go-0129-g0780n6-r0520n4`. State was `running`; no GCloud action occurred.

This update supersedes all older live counts and immediate batch identities.

## 1. Executive summary

The project is building `ganesh-mini-1.0`, a Qwen3.5-2B coding model intended
to improve executable correctness in Go, Java, JavaScript, TypeScript, Python,
and Rust while remaining usable on personal laptops. The intended release is:

- a merged BF16 Hugging Face checkpoint;
- a GGUF F16 artifact for the 16 GB profile;
- a GGUF Q8_0 artifact for the 8 GB profile;
- optionally, the LoRA adapter and reproduction evidence.

The primary serving claim is text-only, non-thinking inference at an 8,192
token context. Vision and the upstream 262k context are outside the laptop
acceptance claim.

Measurement and the original seed pilot are complete. The first trained
candidate regressed from the exact Qwen base's 20/180 development passes to
13/180, so it was correctly rejected. The current strategy is still verified
SFT with BF16 LoRA; the remedy is a stronger execution-verified corpus, not
more epochs over the regressing seed and not an unqualified switch to RL.

The active work is local Gate 2/3 input construction: expansion v1 must reach
exactly 6,000 admitted rows and pass a deterministic 5% quality review before
another training run. At this snapshot it is 5,608/6,000 (93.47%). Only Go is
unfinished. No release candidate exists and nothing has been published to
Hugging Face.

## 2. Start here

Read these in order before making changes:

1. `AGENTS.md`
2. `docs/plans/GANESH_MINI_1_0_PLAN_PASS2.md`
3. `docs/process/DECISIONS.md`
4. `docs/process/PROJECT_STATE.md`
5. `docs/research/PRIMARY_SOURCES.md`
6. `docs/data/EXPANSION_V1.md`
7. this file
8. current `git status`, production state, corpus hash, and active processes

The pass-2 plan is canonical. `PROJECT_STATE.md` contains historical evidence
and many superseded attempts; prefer the latest applicable decision rather
than copying an older recipe or execution card.

## 3. Non-negotiable boundaries

- Any GCloud use is a hard approval boundary. Do not even inspect GCloud
  resources without fresh, explicit approval for that usage.
- Local work, datasets, downloads, non-GCloud compute, training,
  benchmarking, publication after the release gate, and repository operations
  are already authorized.
- Ganesh v0.1 training data is user-owned and authorized. Preserve its source
  commit, hashes, IDs, split lineage, and evaluation separation.
- Public benchmarks, private development tasks, and private decision tasks
  must never enter training.
- Generated code runs only in pinned, resource-limited, network-disabled
  verifier containers.
- Never reconstruct or invent executed evidence. Every decision result must
  bind prompts, rendered prompt hashes, raw output, extracted code, verifier
  output, runtime identity, model identity, and artifact hashes.
- A complete training job is not automatically a successful candidate.
- Publication is blocked unless the frozen Gate 8 decision is
  `release-eligible`.
- Do not add GitHub CI; the user explicitly does not want it in this repo.
- User-owned untracked historical GCloud evidence must not be deleted or
  folded into an unrelated commit without an explicit, evidence-aware reason.

The earlier recurring goal-audit and production-monitor automations were
cancelled at the user's request. The live `launchctl` production job described
below is the actual controller, not a recurring Codex automation.

## 4. Current live state

At the snapshot timestamp:

```text
overall                         5,608 / 6,000  (93.47%)
remaining                        392

Go generation                    470 /   720
Go repair                        338 /   480
Go total                         808 / 1,200

Java                           1,200 / 1,200
JavaScript                       600 /   600
TypeScript                       600 /   600
Python                         1,200 / 1,200
Rust                           1,200 / 1,200
```

State and corpus:

```text
state:  datasets/cache/expansion-v1/production/state.json
corpus: datasets/cache/expansion-v1/production/admitted.jsonl
rows:   5,608
SHA-256 a8419804a375107d8294a4777aafa6b371c23c4983389f09938bfbc9161770db
```

The hash recorded in state matched the corpus bytes. There were zero
aggregation-level duplicate rejections.

Active batch at the snapshot:

```text
go-0106-g0642n6-r0428n4
selection: 6 generation + 4 repair candidates
attempt: 1
phase: bounded teacher correction after first-pass admission
first pass: 0 admitted, 10 rejected because reference behavior failed tests
```

The repair worker and an isolated Codex architect call were live. The zero-row
first pass is a quality/yield event, not a Docker infrastructure error. The
batch remains within the declared one-correction policy; do not manually force
its rows into the corpus.

Controller identity at the snapshot:

```text
launchd label: com.ganesh-mini.expansion-production-20260901c
controller: .venv/bin/python scripts/data/run_expansion_production.py --workers 6
wrapper: /usr/bin/caffeinate -dimsu
stdout: datasets/cache/expansion-v1/production/controller-launchd-20260901c.log
stderr: datasets/cache/expansion-v1/production/controller-launchd-20260901c.err.log
```

Only one lane remains, so `--workers 6` correctly results in one Go lane
writer. Within a batch, teacher construction uses two deterministic shards.
Admission can verify four records concurrently with two implementations per
record, giving a hard ceiling of eight verifier containers. Corpus insertion,
deduplication, ordering, and persistence are replayed serially.

## 5. Live health check

Use read-only checks first:

```bash
cd /Users/navneetprabhakar/Documents/git/ganesh-mini

jq '{status, counts, consumed, targets, corpus_sha256,
     last_batch:(.batches[-1] // null),
     aggregation_rejections:(.aggregation_rejections|length)}' \
  datasets/cache/expansion-v1/production/state.json

wc -l datasets/cache/expansion-v1/production/admitted.jsonl
shasum -a 256 datasets/cache/expansion-v1/production/admitted.jsonl

pgrep -fal 'run_expansion_production.py|generate_expansion_source_batch.py|repair_expansion_rejections.py|admit_expansion.py|codex exec'

launchctl print gui/$(id -u)/com.ganesh-mini.expansion-production-20260901c

tail -100 datasets/cache/expansion-v1/production/controller-launchd-20260901c.err.log
tail -100 datasets/cache/expansion-v1/production/controller-launchd-20260901c.log
```

Healthy means all of the following:

- state is `running`, or `complete` after quotas are reached;
- the state hash equals the actual corpus hash;
- corpus line count equals the sum of all lane/task counts;
- exactly one controller holds the lock;
- there is at most one unfinished batch for Go;
- child generation, correction, or admission work corresponds to that batch;
- no persistent verifier infrastructure failure or partial-evidence mismatch
  is present.

Counts change only after a whole batch has been generated, independently
tested, verified, optionally corrected once, replayed through global
deduplication, and atomically persisted. A flat counter during an active batch
is normal.

## 6. Current risks

### 6.1 Go yield has deteriorated

The recent Go batches admitted between zero and two rows each, materially
below earlier production yield. Batch 0106 also rejected all ten rows on its
first pass. This is not an infrastructure anomaly, but it threatens schedule
and reserve sufficiency if it persists.

At the snapshot, the reserve math was:

| Stratum | Accepted | Target | Needed | Stimuli consumed | Reserve left | Minimum future yield |
|---|---:|---:|---:|---:|---:|---:|
| Go generation | 470 | 720 | 250 | 648 | 432 | 57.87% |
| Go repair | 338 | 480 | 142 | 432 | 288 | 49.31% |

Historical cumulative yields were about 72.53% generation and 78.24% repair,
so the frozen reserve was still mathematically sufficient. The margin is not
large enough to ignore continued zero-to-two-row batches. If either stratum's
required future yield rises above a defensible observed yield, stop before
reserve exhaustion and diagnose task construction/test behavior. Do not relax
tests, deduplication, or quotas to manufacture 6,000 rows.

### 6.2 Verification is expensive on this host

The Mac is ARM64 while the pinned Go verifier is Linux/AMD64. Docker therefore
uses emulation. Each candidate runs both reference and known-bad code, and
failed candidates may receive one correction and full reverification. This is
the main reason progress is slow.

The current bounded concurrency is already eight containers, each limited to
one CPU and 512 MB. Raising it further without measurement can increase Docker
contention and timeouts. A native ARM64 verifier could help substantially, but
changing runtime architecture mid-corpus requires qualification proving the
same compiler/test behavior and evidence identity. Do not silently mix
runtime contracts.

### 6.3 Laptop sleep stops wall-clock progress

`caffeinate` prevents idle sleep but cannot keep a closed laptop running.
Earlier apparent stalls included roughly 58.5 hours of host suspension. Keep
the Mac awake, powered, and Docker Desktop running.

### 6.4 Canonical status prose lags live state

`PROJECT_STATE.md` is evidence-heavy and contains earlier expansion counts.
Treat `state.json` plus the corpus hash as the live source of truth. Update the
canonical prose only at a meaningful evidence boundary, especially final
sealing, rather than committing every batch.

### 6.5 Existing unrelated untracked evidence

The worktree is otherwise aligned with `origin/main`, but contains historical
untracked files under `measurement/cuda/gcloud/...` and
`measurement/gate1/gcloud/...`. They predate this handoff and are not part of
the expansion-controller changes. Preserve them.

## 7. Failure and recovery procedure

The controller is fail-closed and protected by a non-blocking process lock.
Never start a second controller while the existing process is alive.

If the process disappears while state is nonterminal:

1. Do not immediately restart it.
2. Inspect the last batch entry, its directory, logs, state hash, corpus hash,
   and lock-holder PID.
3. If both `candidates.jsonl` and `teacher-evidence.json` exist, verify that
   the candidate bytes and recorded selection are hash-bound. The controller
   may resume that exact selection without regenerating it.
4. If both are absent and the batch directory has no unexpected artifacts,
   the same recorded selection may be regenerated.
5. If only one of candidate/evidence exists, unexpected artifacts exist, or a
   hash differs, stop. Preserve everything and diagnose; do not improvise.
6. A verifier infrastructure failure may be retried only through the bounded
   classified retry path. It must not be sent to the teacher as data repair.
7. Candidate/reference behavioral rejection may take the one declared
   correction pass. Remaining rejection is final for that candidate.
8. Resume only one controller after the evidence is proven safe.

The normal foreground recovery command is:

```bash
cd /Users/navneetprabhakar/Documents/git/ganesh-mini
/usr/bin/caffeinate -dimsu .venv/bin/python \
  scripts/data/run_expansion_production.py --workers 6
```

Use `--recover-only` when the intent is strictly to finish a recorded
failed/running batch without opening a new one. Do not use it as a substitute
for examining ambiguous partial artifacts.

## 8. Completing expansion v1

When the controller reaches `complete`, do not train immediately. Complete
these boundaries first:

1. Recalculate line count and SHA-256 and require equality with state.
2. Require exact quotas: Go 1,200; Java 1,200; JavaScript 600; TypeScript 600;
   Python 1,200; Rust 1,200; generation 3,600; repair 2,400.
3. Rerun final sealed admission against all evaluation roots. A suitable
   invocation is:

   ```bash
   .venv/bin/python scripts/data/admit_expansion.py \
     --input datasets/cache/expansion-v1/production/admitted.jsonl \
     --output datasets/cache/expansion-v1/production/final.admitted.jsonl \
     --report measurement/data/expansion-v1/production-final.admission.json \
     --record-workers 4 --verifier-workers 2 --seal
   ```

   This is intentionally expensive: it independently reopens execution and
   separation for the final corpus. Do not replace it with state accounting.
4. Confirm zero exact/fuzzy overlap with diagnostic, development, and sealed
   decision surfaces and zero cross-batch/corpus collision.
5. Build and manually inspect the deterministic 5% stratified quality sample
   (300 rows), covering lane, source, task type, and rejection history. Check
   clarity, API consistency, test independence, non-triviality, idiomatic
   code, dependency isolation, and known-bad realism.
6. A systematic quality defect reopens the affected stratum. It cannot be
   waived because the row count reached 6,000.
7. Seal source lineage, rights, corpus, admission, sampling, and hashes.
8. Update `docs/data/EXPANSION_V1.md`, `docs/process/PROJECT_STATE.md`, and
   `docs/process/DECISIONS.md` at that evidence boundary.
9. Run focused data tests, then the full suite. Distinguish any known stale
   Gate 1 readiness fixture failures from new failures; do not casually waive
   them.
10. Batch the related code, evidence summaries, tests, and docs into the
    fewest practical commits and push to `main` without GitHub CI.

There is currently no dedicated final 5% production-sample builder visible in
the repository. That is a real implementation gap. Implement it
deterministically and test it before declaring the corpus training-ready.

## 9. Training strategy after data closure

Do not rerun the rejected seed recipes. The next bounded pilot must use the
sealed 6,000-row expansion and the qualified mechanism:

- supervised fine-tuning with response-only loss;
- BF16 LoRA as the primary path;
- attention-only targeting in language-model layers 16–23;
- rank 8, alpha 16, dropout 0.05;
- joint six-lane training with a five-family 20% token objective;
- one bounded unique epoch initially;
- QLoRA only as the declared measured OOM/VRAM fallback;
- fused linear cross-entropy through qualified Liger Kernel 0.8.2 to avoid
  full-vocabulary logit materialization;
- executable development evaluation for selection; loss is diagnostic only.

The expansion training package/config is not yet the old seed-pilot package
with a path changed. It must bind the new corpus manifest, tokenization,
weights, recipe, model revision, toolchain, evaluation exclusion, runtime
image, budgets, checkpoint/finalization behavior, and output hashes.

Before paid compute:

1. Prepare the expansion train/validation split and token-balance manifest.
2. Prove response-only rendering and no evaluation leakage.
3. Rehearse the exact archived workspace locally/offline where possible.
4. Create a new immutable execution card with price, time, VRAM, checkpoint,
   backup, and teardown ceilings.
5. Obtain fresh explicit GCloud approval for the exact proposed campaign.

Promotion from the bounded pilot requires positive executable directionality:
at least four of five product families improve, no material lane regression,
format/truncation failures do not increase, and save/reload reproduces. If it
fails, change data or mechanism before scaling.

## 10. Remaining gates to release

### Gate 4 — Pass A joint verified SFT

Train the technically qualified expansion recipe and select checkpoints using
the 180-task development surface, per-lane paired transitions, malformed and
truncated output rates, and general-instruction retention. Do not select on
validation loss alone.

### Gate 5 — optional targeted correction

Only if Pass A succeeds, cluster remaining base/Pass-A failures without
opening decision prompts. Train at most 20–35% of Pass A token budget with
15–20% broad replay. Retain Pass A as a comparator and reject Pass B if it
forgets an improved lane or exploits verifier artifacts.

### Gate 6 — untouched comparison

Open the private 360-task decision suite once for immutable candidates:

- exact Qwen base revision `15852e8c16360a2fea060d615a32b45270f8a8fc`;
- selected Ganesh Mini Pass A;
- selected Pass B, if qualified;
- Ganesh v0.1 through its own pinned Gemma serving/template contract.

Report lane and five-family macro pass@1, paired wins/losses/ties, confidence
intervals, McNemar result, size-normalized quality, throughput, startup, peak
RSS, and available energy measurements. Ganesh v0.1 is a larger reference
competitor, not the causal baseline.

### Gate 7 — artifacts and laptop certification

Merge the selected adapter, export GGUF F16 and Q8_0 with the pinned llama.cpp
revision, prove six-lane export equivalence, then certify:

- Q8_0: peak RSS at or below 7 GB on the 8 GB profile at 8,192 context;
- F16: peak RSS at or below 14 GB on the 16 GB profile at 8,192 context.

Record artifact sizes and hashes, load time, prompt/decode throughput, thermal
behavior, and failures. If a profile misses, narrow the claim; do not tune the
decision result after opening it.

### Gate 8 — release and Hugging Face

Release only if the fail-closed adjudicator returns `release-eligible`. The
minimum outcome includes a macro win over Qwen base, statistically supported
paired improvement, no lane regression greater than two of 60 decision tasks,
at least 98% Q8 solved-task retention or an explicit exception, passing RAM
profiles, and complete evidence lineage.

The release tooling already exists:

- `scripts/release/build_artifacts.py`
- `scripts/release/verify_export_equivalence.py`
- `scripts/release/certify_laptop.py`
- `scripts/release/adjudicate.py`
- `scripts/release/build_model_card.py`
- `scripts/release/publish_huggingface.py`

Publication is authorized only after those technical gates pass. The
publisher requires a `release-eligible` v2 decision plus the bound artifact,
comparison, laptop, export, and lineage seals. Run it without `--execute`
first to produce and review the upload plan; then use `--execute` for the
approved destination. No Hugging Face model repository or artifact has yet
been published by this project.

## 11. What is complete versus incomplete

Complete and reusable:

- exact Qwen identity and revision pin;
- Gate 0 Apple/runtime/export smoke and Gate 0B L4 training-mechanism proof;
- frozen 180-task development and 360-task decision surfaces;
- exact Qwen development baseline: 20/180;
- authorized v0.1 seed import, lineage, compatibility, and separation;
- one valid historical `1e-5` seed candidate adapter with save/reload evidence,
  but no executable canary score and therefore no promotion claim;
- expansion contract, sources, teacher isolation, execution admission,
  bounded recovery, and parallel local controller;
- local release and Hugging Face fail-closed tooling.

Incomplete:

- the last 392 admitted expansion rows at this snapshot;
- final sealed 6,000-row admission;
- deterministic 300-row production quality review and its tooling;
- expansion-specific training dataset/package and bounded pilot;
- Pass A and optional Pass B;
- untouched decision comparison with Qwen and fresh Ganesh v0.1 execution;
- merged BF16, GGUF F16, and GGUF Q8_0 artifacts;
- laptop certification and release adjudication;
- Hugging Face publication.

## 12. Git and repository state

At the snapshot:

```text
branch: main
HEAD:   0c3a8d5 Scale expansion verification across records
remote: origin/main at the same commit
```

The two most recent acceleration commits are:

```text
0c3a8d5 Scale expansion verification across records
a4ca61a Parallelize expansion teacher and verification
```

Focused data tests for those changes passed (50 after the latest change). The
full repository suite had three pre-existing failures around stale Gate 1
readiness/sealed-workspace expectations; re-run and diagnose them before a
release boundary instead of treating this note as a permanent waiver.

Do not commit the continuously changing production cache one batch at a time.
At the 6,000-row boundary, commit the intended durable corpus/evidence only
according to `.gitignore` and the repository's evidence policy.

## 13. Immediate next-action checklist

1. Verify the live state has advanced from this snapshot and hashes still
   match.
2. Let batch `go-0106-g0642n6-r0428n4` finish its one correction pass.
3. Continue the existing single controller; do not start a duplicate.
4. Track Go generation/repair reserve sufficiency after every meaningful
   batch boundary.
5. Stop and diagnose if the controller fails closed, evidence hashes differ,
   partial artifacts are ambiguous, or reserve math becomes untenable.
6. At 6,000 rows, run sealed admission and implement/run the deterministic 5%
   quality sample.
7. Seal and document the final dataset.
8. Prepare and locally rehearse the expansion-specific bounded SFT campaign.
9. Present an exact GCloud execution card and obtain fresh approval before any
   GCloud access.
10. Execute Gates 4–8 in order; publish only a release-eligible result.

The most important handoff rule is simple: protect evidence integrity even
when progress is slow. A forced 6,000-row count, a successful training exit,
or a generated GGUF is not the goal. The goal is a defensible, executable
improvement over the exact Qwen base, with honest comparison to Ganesh v0.1
and laptop artifacts whose claims were actually measured.
