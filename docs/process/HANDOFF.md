# Ganesh Mini 1.0 handoff

## Final handoff — 2026-10-02 IST

The local full public MultiPL-E HumanEval run finished and all six paired
language lanes passed fail-closed scoring. Sealed report:
`artifacts/public-benchmark/full-humaneval-20261001/full-six-lane-paired-report.json`,
report SHA `753181b3042e5445d8e70bcba3de5a15244c9fbaa76e896deef314af64788fb2`.
Ganesh Mini passed 338/952 public tasks versus upstream 339/952, with 8
paired wins and 9 losses. Full method and report are published under
`https://huggingface.co/Executespec/ganesh-mini-1.0` at commit
`f3aa8dadc583621da8a7a9561036804b085a8d04`. The public files were
byte-checked against local sources. This result does not support an
improvement claim. The previous 30-task sample is a subset of this run.

The exact benchmark controller and model server exited; the localhost tracker
was stopped and its port is free. Raw outputs remain locally preserved and
ignored by Git. Do not restart the assessment for closure. Private Gate 3
quality failure, unexecuted Gates 4–7, Gate 8 NO-GO, unopened private
decision set, and the Gate 0B raw-report gap remain historical facts. The
user-directed public experimental checkpoint is not a passed release.
No GCloud usage is involved in this final public diagnostic. Entries below
describe earlier running states and are retained for audit only.

Benchmark-specific tests passed (11/11). Two wider-suite inference tests
still fail because the historical Gate 1 evaluation workspace seal binds an
older `scripts/campaign/run_host.py` hash. Preserve that fail-closed behavior
and original seal; do not reinterpret the project as release-ready.

## Local refreshable tracker — 2026-10-01 IST

The full public run has a local read-only dashboard at
`http://127.0.0.1:8765/`, served by
`scripts/benchmarks/serve_public_progress.py` in exec session `26961` /
PID `41434`. It binds only to `127.0.0.1`, polls every five seconds, and
shows generated, correctness-tested, and `OK`-passed tasks for both models
in each lane. Live pass counts are provisional, while the final paired score
requires the fail-closed sealed report. It shows no raw outputs. The dashboard is independent
of the benchmark controller PID `38260`; do not restart the benchmark if only
the dashboard stops. The UI was opened in the in-app browser and verified
through both initial load and manual page refresh.

## Full local public benchmark controller active — 2026-10-01 IST

One sequential controller, exec session `1302` / PID `38260`, is running
`full-humaneval-v1` at
`artifacts/public-benchmark/full-humaneval-20261001`. The run order is JS,
TS, Rust, Python, Java, Go, each candidate then pinned upstream. Full pinned
task counts are 161, 159, 156, 164, 158 and 154. `caffeinate -i` prevents
idle sleep while the command runs. It uses the same local Q8 models and
network-disabled MultiPL-E evaluator as the completed 30-task public slice,
with the Rust full-program stop-token correction applied prospectively to
both models. **Do not duplicate the controller, model server, or verifier.**
Check the process, exact manifests, generation logs and verifier output
before resuming after an interruption. Once all six paired lanes seal, score
with `scripts/benchmarks/score_public_multipl_e.py --run-prefix full-humaneval-v1`
using the pinned verifier digest. Do not publish partial counts or present
this local full run as an official leaderboard score. The 30-task public
report already on Executespec remains a separate prior diagnostic. No
GCloud or private evaluation use is authorized by this run.

## Public assessment published — 2026-10-01 IST

The single sequential local benchmark controller completed all six public
language lanes and exited successfully. Its sealed paired report is
`artifacts/public-benchmark/20261001/six-lane-paired-report.json`, report
seal `9619bb5dabbf3f7d335c41a28ce52ae3db8d475d65027571caebb8a60f5efa1c`.
Ganesh Mini passed 70/180 sampled public tasks against pinned upstream
71/180, with 2 paired wins, 3 losses and 175 ties. The versioned Rust
reassembly uses the same saved outputs and the published stop token; the
uncorrected Rust result is retained and excluded. The method and report,
without prompts/tests/raw completions or private scores, are public under
`Executespec/ganesh-mini-1.0` at commit
`86cee3536304bdd83bdc8e996ee1a489d3a71600`. Anonymous byte-hash
verification passed; the Q8 artifact hash is unchanged. The card states
the sample and serving limitations and makes no improvement claim. No further
benchmark process or cloud compute should be started by this handoff. The
frozen private Gate 3 quality failure and original Gate 8 NO-GO remain
internal, unchanged records; public checkpoint publication does not mark
those gates passed.

## Historical: public benchmark controller active — 2026-10-01 IST

One sequential local controller is running in exec session `59609`:
`scripts/benchmarks/execute_public_suite.py`. It performs a deterministic
30-task sample in each of Go, Java, JavaScript, TypeScript, Rust (pinned
MultiPL-E translations), and Python (pinned HumanEvalPlus file), comparing
the public Q8_0 checkpoint to a locally converted Q8_0 of pinned upstream.
It applies MultiPL-E's stop-token rule to exact-prefix completions and runs
generated code only in the pinned image with no network and CPU/memory/PID/
privilege limits. The initial uncorrected Go format pilot is preserved but
excluded. Before restarting, inspect the controller process and per-run
manifests/logs; do not duplicate model servers. On complete paired evidence,
run `scripts/benchmarks/score_public_multipl_e.py`, review the result, then
publish only the executed public benchmark report and settings. No score yet.

## User-directed public checkpoint upload — 2026-10-01 IST

Navneet explicitly directed publication despite the Gate 3 quality failure,
without a categorical failure label, followed by public benchmark evaluation.
He specified the Executespec organization and directed that only public
benchmark assessment be shared, not our private development assessment.
`https://huggingface.co/Executespec/ganesh-mini-1.0` is public and anonymously
verified at commit `5cba9d01cf4fb99e8ff1964c4877320d187c2d09`.
It contains the original LoRA adapter, merged BF16, tokenizer, F16 GGUF,
Q8_0 GGUF, license and card; remote large-file hashes match local staging. The card
contains no private development scores and makes no improvement claim.
Earlier public commits with private scores were removed from reachable repo
history by super-squash, but external caching cannot be ruled out. The
card in `artifacts/hf-staging/20261001-selected-1e-5/README.md` matches the
current public state. Public assessment has not run yet; pinned MultiPL-E
dataset revision `28441b6024e71d4a1c1c0f6bf171c935cd5a43f2` and
upstream-paired local Q8 serving are being prepared.
The original Gate 8 release decision remains NO-GO; the release-eligible
publisher remains fail-closed. Do not publish private prompts/tests or use
GCloud for this work.

## Resume instruction after no-go closure — 2026-10-01 IST

Navneet said to continue despite the failed Gate 3 result. Preserve the
terminal no-go record below as historical evidence, but do not treat it as a
current stop-work request. Gate 3 remains failed under the frozen plan. Local
artifact/readiness checks may resume immediately; do not silently convert the
failed checkpoint into a passing `ganesh-mini-1.0` release, open the private
decision set, or incur new GCloud charges without a scoped plan. Clarify
whether the target is a corrected model under the original gates or a
transparently labelled experimental artifact with separate publication scope.

## Terminal no-go closure — 2026-10-01 IST

Navneet directed an end to improvement work and closure today. Treat the
selected Gate 3 quality failure as terminal for this project iteration, not
as a license to skip forward. Gate 3 did not pass; Gates 4–7 are unexecuted;
Gate 8 model release is NO-GO. No Hugging Face model/adapter/GGUF publication,
no opening of the 360 private decision tasks, and no new compute or GCloud
retry. The exact VM/disk/network/subnet for the completed 180-task evaluation
were backed up and absent twice; this is not a project-wide billing audit.
See `docs/process/GANESH_MINI_1_0_NO_GO_CLOSURE_20261001.md` for retained
evidence, missing gates, and restart prerequisites. Pause the 30-minute Gate 3
automation as part of closure. Historical entries below remain as evidence,
not live work instructions.

## Gate 3 development quality failure — 2026-10-01 IST

The selected `1e-5` development attempt `20261001T020646Z` completed 180/180
tasks with evaluation exit 0. Independent terminal GCS backup verified 375
objects, local control mirror verified 167, and exact VM/disk/network/subnet
absence passed twice. Sealed frozen adjudication:
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T020646Z/development-adjudication.json`,
SHA `4177c8e5782481877d0de5e20b861e46886a3c93138bf2d3a8037e4cfe088cd3`.
Status is `quality-criteria-failed`: only Python improved versus the admitted
upstream (required at least four of five families); Java and TypeScript lane
pass counts each declined by one (zero regression required). Paired transitions
were 3 wins, 4 losses, 173 ties. Gate 3 remains open; do not open the 360
decision tasks, scale to Gate 4, publish a model, or reinterpret this as a
runtime failure eligible for a same-recipe retry. Analyze failed cases locally
and propose a prospective data/mechanism correction under the frozen plan.
Any new GCloud work needs a scope and budget reconciliation; retain the $15
absolute incremental ceiling and all paid/transfer operations. Gate 0B raw
report remains a separate release hold.

## Active Gate 3 selected-adapter 180-task VM — 2026-10-01 IST

Exact allocated development attempt:
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T020646Z`.
Sealed card `24569f6a90742f23502d3e55c0c8c3ead6908d393d4e4de7b4a0fa8723c36451`.
One `g2-standard-8` L4 VM `ganesh-g3-eval-20261001t020646z` is RUNNING in
`us-central1-c` since 2026-10-01T02:12:52Z, two-hour provider STOP. Exactly
one watcher, PID `82840` / exec session `40414`, began 02:13:29Z. **Do not
duplicate VM or watcher.** Inspect its process, provider status, serial, and
checkpoint GCS. When TERMINATED, let the live watcher independently verify
complete terminal GCS backup, delete exact VM/disk/network/subnet, and check
absence twice. If it fails, recover complete backup before any deletion.
This is selected `1e-5` on 180 development tasks; decision set stays closed.
Prior allocated reserve $5.00 and card upper $13.263870928 remain within
approved $15, subject to prior transfer/operations reconciliation. After
finalization, run frozen 180-task adjudication; no quality verdict yet.

## Gate 3 development fifth sequential capacity attempt — 2026-10-01 IST

Four selected-adapter development requests in `us-central1-a` and
`us-east1-b/c/d` were pre-allocation L4 stockouts. All exact refusals have
78-object independently verified GCS backups and VM/disk/network/subnet
absence twice after cleanup. No 180-task development result exists. Prior
allocated reserve remains $5.00, subject to cumulative transfer/operations
under the $15 ceiling. One sequential preparation is active at
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T020646Z`
in approved `us-central1-c`. Do not duplicate it. After sealing, verify
DIVERGENCE, card/input hashes, auth/project absence and budget before one
launch. If allocated, one watcher must back up terminal evidence before
teardown/double absence. Decision tasks remain closed.

## Fourth sequential Gate 3 development capacity attempt — 2026-10-01 IST

Selected-adapter 180-task development requests `20261001T011522Z`
(`us-central1-a`), `20261001T012619Z` (`us-east1-b`), and
`20261001T014614Z` (`us-east1-c`) all failed before allocation from L4
stockout. Each 78-object refusal control backup is independently verified;
exact VM/disk/network/subnet absence passed twice. No development quality
evidence was produced. Prior allocated cost reserve remains $5.00, with
repeated GCS transfer/ops to be considered under the same $15 ceiling.
One sequential preparation is active at
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T015703Z`
in approved `us-east1-d`. Do not duplicate it. After card seal, verify
DIVERGENCE, auth/resources, hashes and cumulative budget before a single VM
request. If allocated, start one watcher and independently verify terminal
GCS evidence before exact teardown/double absence. Decision tasks stay closed.

## Active Gate 3 development preparation, `us-east1-c` — 2026-10-01 IST

The first two selected-adapter development VM requests (`20261001T011522Z`
in `us-central1-a`, `20261001T012619Z` in `us-east1-b`) were pre-allocation
L4 stockouts. Each 78-object refusal control backup is independently verified
and exact VM/disk/network/subnet absence passed twice. No development task ran
on either. Prior allocated cost reserve remains $5.00. One sequential retry
preparation is active at
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T014614Z`
in approved, provider-suggested `us-east1-c`. Do not duplicate it. Once card
seals, verify DIVERGENCE, auth/resources, hashes and $15 ceiling, launch one
VM only, start one watcher if allocated, and verify terminal GCS backup before
exact teardown/double absence. Apply the 180-task frozen development
adjudication after successful finalization; keep decision tasks closed.

## Gate 3 development sequential capacity retry — 2026-10-01 IST

The first selected-adapter 180-task development attempt
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T011522Z`
was a pre-allocation L4 stockout in `us-central1-a`; it produced no quality
evidence. Its 78 refusal controls were independently verified in GCS, and
the exact VM/disk/network/subnet are absent twice after cleanup. Prior
conservative allocated reserve remains $5.00. One replacement preparation is
active at `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T012619Z`
in approved `us-east1-b`. Do not duplicate it. After sealed preparation,
recheck DIVERGENCE, auth/project resources, hashes and $15 ceiling before
one launch; if allocated, run one watcher and verify terminal GCS evidence
before exact teardown/double absence. Then adjudicate all 180 development
tasks under the frozen no-regression rule. Decision tasks remain closed.

## Gate 3 selected 180-task development preparation — 2026-10-01 IST

Canary VM attempt `20261001T002557Z` completed both frozen 30-task runs, exit
0. Its 136-object terminal backup and 140-object local control mirror were
independently verified; exact VM/disk/network/subnet absence passed twice.
Sealed canary report
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T002557Z/canary-selection.json`
has SHA `1eb78aa5949923013b6d5fe776a3648ed9f3d1b707574391b949c6e632fb9331`:
upstream and both adapters are 5/30 with identical lane totals, hence frozen
tie rule selects `1e-5` for 180-task development only. No Gate 3 quality pass.
Selected staging card seal is
`477d0c069fc4f913a9d698b1039d65106e6d70471691cb0c051a21e8255c324e`.
One sequential development preparation is active at
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T011522Z`
in `us-central1-a`. Do not duplicate preparation, VM, or watcher. When card
seals, check DIVERGENCE, auth, project resources, exact hashes and $15
ceiling before single launch. If allocated, run exactly one watcher, verify
terminal GCS evidence before exact teardown, then apply frozen 180-task
development adjudication. Keep the private decision set closed.

## Active two-adapter Gate 3 canary VM — 2026-10-01 IST

The exact v2 retry `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T002557Z`
has one RUNNING `g2-standard-8` L4 VM
`ganesh-g3-eval-20261001t002557z` in `us-central1-a` (provider start
2026-10-01T00:36:53Z; two-hour STOP). Card seal
`4e2cc2cf9f7fb5561dd2abfe4f9c6eb6e1871c0075add60d25239a038ccb5539`.
Exactly one watcher, PID `26066` / exec session `26076`, began at 00:37:28Z.
**Do not launch another VM or watcher.** Inspect this watcher, provider status,
serial output, and checkpoint GCS. On TERMINATED, let the live watcher finish;
if it fails, independently download/hash complete terminal GCS backup before
deleting exact VM/disk/network/subnet and verify absence twice. Both frozen
30-task canaries are intended to run sequentially. No canary quality result
exists yet. Count allocated runtime conservatively under the approved $15
ceiling; keep the 360-task decision set closed.

## Active Gate 3 canary capacity retry — 2026-10-01 IST

The v2 canary attempt `20261001T000513Z` received a pre-allocation L4
stockout in `us-central1-b`; no VM or watcher ran. The refusal control GCS
backup was independently hash-verified before deleting the exact subnet and
network; VM, disk, network, and subnet absence passed twice. Its immutable
failure evidence remains at `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T000513Z`.
One **sequential** replacement preparation is active at
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T002557Z`
in approved zone `us-central1-a`. Do not duplicate it or launch a second
watcher. Inspect live process and exact output, then verify card seal, auth,
resources, DIVERGENCE, and the cumulative $15 ceiling before one allocation.
If allocated, run one watcher with the two-hour provider STOP; verify complete
terminal GCS evidence before exact resource teardown and double absence.
Neither the earlier startup failure nor this stockout is candidate quality
evidence. The frozen 30-task canary and 180-task selected-adapter development
must pass before Gate 3 can close; keep decision tasks sealed.

## Gate 3 canary VM startup failure under verified teardown — 2026-10-01 IST

Attempt `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20260930T231842Z`
allocated once but terminated before model load/evaluation. Terminal startup
exit is 1: `inspect_model_archive.py` imported a missing
`scripts.train.preflight_gate3_capability_pilot` module because the separate
587-file evaluation workspace did not contain that one materializer dependency.
The cleanup-time `docker: command not found` is secondary. No 30-task result
exists. The eight-object terminal GCS backup was independently verified;
`finalization.json` says exact VM/disk/network/subnet absence twice. The one
watcher, PID `1714` / exec session `19974`, subsequently timed out while
redundantly mirroring the 876-MB local verifier roundtrip to GCS; this was
**after** terminal verification and teardown. Fresh project-wide checks found
no VM/disk and only the default network. Complete the small control-evidence
mirror without reuploading already pinned/terminal-backed large roundtrips
before any retry.
Preserve the failed card, seal
`08ed09f4362a6bd293a488c63e47ac2971b224635d08e5afadfcc31bbe7a1b17`,
all transfer and launch-recovery evidence, and the terminal logs. The
conservative allocated reserve for this failure is $0.75, or $4.00 total
prior reserve including both training candidates and first training failure.
A prospective one-file dependency fix is being locally tested for a **new**
attempt; do not mutate old evidence or count it as model quality. Recheck
DIVERGENCE, budget, auth, project-wide resource absence and finalization
before one sequential new L4 allocation. Keep the decision set closed.


## One Gate 3 canary evaluation VM and watcher active — 2026-10-01 IST

Exact attempt: `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20260930T231842Z`.
Card seal: `08ed09f4362a6bd293a488c63e47ac2971b224635d08e5afadfcc31bbe7a1b17`.
The `g2-standard-8` L4 VM `ganesh-g3-eval-20260930t231842z` allocated in
`us-central1-b`; one watcher, PID `1714` / exec session `19974`, began at
2026-09-30T23:41:01Z. **Do not start another VM or watcher.** Inspect the
watcher, provider status, serial output and GCS checkpoints. Once the VM is
TERMINATED, allow that watcher to independently download/hash the terminal GCS
backup, delete only its exact VM/disk/network/subnet, and verify absence twice.
If watcher finalization fails, preserve resources and recover backup first.
The first large verifier upload timed out during preparation; its partial
evidence remains. Exact resumption revalidated the small inputs and freshly
downloaded/hashed the historical pinned verifier archive. An initial launch
path error occurred before VM creation; exact `resume_launch` verified the
network/subnet and allocated once. Both frozen candidate canaries are intended
sequentially; no quality result exists yet. Do not open the 360 decision tasks.


## Two canary configs and adapter bundle locally staged — 2026-10-01 IST

`scripts/eval/prepare_gate3_candidate_evaluation.py` verified both complete
sealed runs, adapters, independent 54-object terminal backups, the 180-task
evaluation workspace and exact 30-task canary hashes. It staged two canary
configs plus a candidate-input bundle at
`measurement/gate3/capability-scale-v1/full-pilot-eval/candidate-staging-v1/`.
The evaluation card is `prepared-only`, seal
`2c2ead6df00e2e9769ee1562216d8d6340b1d99ad1f079ec6bee9dceb502a8ff`.
Do not allocate from this card alone. Provider execution/backup/teardown and
budget guards are being implemented and tested separately; no candidate
canary has run. Development config remains blocked until sealed canary
selection. Keep 360-task decision set closed.

## Evaluation-only workspace prepared locally — 2026-10-01 IST

The checked-in development-only packager sealed 587 allowlisted files and
exactly 180 private development tasks in
`measurement/gate3/capability-scale-v1/full-pilot-eval/evaluation-workspace-v1.tar.gz`;
manifest seal
`8ed2f45d87b3b867a59c6eca03be6e9d991bd1070037bd52311ed63a07585edc`.
No training/seed/decision content entered the workspace. This is preparation,
not executed evaluation. Next bind both sealed adapters and frozen canary
task IDs to a fail-closed evaluation card/controller, validate actual-host
runtime and budget, then run both canaries before any full 180-task opening.

## Both Gate 3 candidate epochs sealed; canary next — 2026-10-01 IST

The frozen `3e-5` attempt `20260930T220936Z` completed the 900-row,
651,639-input-token epoch with 113 optimizer steps, exit 0 and save/reload
pass at zero maximum logit difference. Run-evidence seal:
`19daa16303a72a195329cc1bf06984f12414d76a1dc85e343f25bafe94f86ed2`.
The sole watcher independently verified 54 terminal GCS objects before exact
VM/disk/network/subnet teardown and double absence. Fresh project-wide
VM/disk/address inventories are empty; only default network remains. The
`1e-5` candidate's full epoch/save-reload and independent backup were
already sealed. No more candidate training is needed under this frozen pair.
Prepare a **separate** evaluation workspace and run each candidate on the
same frozen 30-task canary. Only then select by the no-regression rule and
evaluate the selected adapter on all 180 development tasks. Keep the
360-task decision set closed. Gate 3 quality is not passed yet; Gate 0B raw
report recovery and Gates 4–8 still block release. Preserve both adapters
and all raw training/backup evidence.

## Second LR VM running; one watcher — 2026-10-01 IST

After `20260930T220004Z` (`us-central1-c`) and `20260930T220454Z`
(`us-east1-c`) both ended as pre-allocation stockouts with independently
verified GCS refusals and exact double absence, `3e-5` attempt
`20260930T220936Z` allocated VM `ganesh-g3-pilot-20260930t220936z` in
`us-east1-b`. Card seal:
`f629892c135020cf9e7dbca75ae8442b25b5b9be274df30ce4ad794699de3ad9`.
Provider RUNNING began 22:12:20Z with two-hour STOP. **One watcher is
active**, PID `88102` / exec session `63139`, started 22:12:26Z. Do not
launch another watcher or VM. Inspect its process, provider/serial state
and checkpoint GCS evidence. On TERMINATED let it independently verify all
terminal GCS objects, delete exact resources, then check absence twice.
Only afterward assess sealed 651,639-token result and save/reload. First LR
already completed its full epoch; canary/dev quality is still not measured.
Keep evaluation separate and Gate 0B raw-report recovery as a release hold.

## Second LR stockout and sequential retry — 2026-10-01 IST

`3e-5` attempt `20260930T220004Z` in `us-central1-c` got a pre-allocation
L4 stockout. Refusal GCS backup and independent verification passed; exact
resource cleanup and double absence yielded `refusal-finalized`. No second
LR training or GPU runtime. The prior-allocation check still returns the
conservative $3 reserve, leaving the unchanged $6 candidate slice within
the $15 ceiling. A single sequential `us-east1-c` retry is being staged;
do not overlap or duplicate it. The first LR full epoch remains sealed, but
Gate 3 model-quality evaluation has not begun.

## First LR complete; frozen second LR staging — 2026-10-01 IST

The corrected `1e-5` full-pilot attempt `20260930T205829Z` finished all 900
unique rows and 651,639 input tokens with 113 optimizer steps, exit 0 and
save/reload pass (zero maximum logit difference). Run-evidence seal:
`21d78a7e339fb75dd89bdd9ada83a53bdbb10678bd7c3c9b09d182786b698537`.
Its watcher independently verified 54 terminal GCS objects, deleted exact
VM/disk/network/subnet, and confirmed absence twice. Project-wide VM/disk/
address inventories are empty; only the default network remains. The
controller validated the sealed prior result and derived a conservative $3
prior-cost reserve for the unchanged `3e-5` candidate, within its $6 slice
and Navneet's $15 absolute incremental ceiling. Stage/launch only one second
LR VM and one watcher, sequentially. Gate 3 quality is still unmeasured:
the 30-task canary for both adapters and 180-task development evaluation for
the selected adapter remain separate. Gates 4–8 and Gate 0B raw-report
recovery still block Hugging Face release.

## Corrected first LR VM running with one watcher — 2026-10-01 IST

Attempt `measurement/gate3/capability-scale-v1/full-pilot-gcloud/20260930T205829Z`
allocated the single L4 VM `ganesh-g3-pilot-20260930t205829z` in
`us-central1-c` for the corrected `1e-5` candidate. Card seal is
`8133a95f3fde266a36cde45d0792f574c930c926519953f25c692bec42e32744`.
Provider RUNNING began 21:01:20Z. Watcher PID `72123` / exec session
`49372` started 21:01:30Z; **do not start another watcher or VM**. The
two-hour provider STOP and $15 overall ceiling remain. Card prior-cost
reserve is $0.75 from the earlier paid failure. Inspect process, serial
output and checkpoint GCS evidence; on VM termination let this watcher
independently download/hash terminal GCS evidence before deletion and double
exact resource absence. No training or quality result is yet verified.
Only after finalization assess the sealed 651,639-token full-epoch result,
then consider `3e-5`; evaluation remains separate and Gate 0B raw-report
gap still blocks release.

## First full-pilot allocation finalized with pre-training CLI-path failure — 2026-10-01 IST

Attempt `20260930T192827Z` in `us-east1-c` stopped after 808 seconds, exit 1,
before optimizer steps. Actual-host 16-row throughput passed at 314.457 input
tokens/s and card binding passed. `run_sft.py` rejected the startup CLI's
validation file path: it used the Gate 3 artifact path instead of the frozen
config's `artifacts/train/expansion-pilot-v1/prepared-validation.jsonl`. The
correct file is already in workspace-v8 with matching pinned SHA. All 17
terminal GCS objects were independently verified; watcher deleted exact
VM/disk/network/subnet and checked absence twice. Project VM/disk/address
inventories are empty. Do not count this as a candidate epoch or quality pass.

The startup argument is fixed and a regression test checks all three training
CLI data paths against the frozen config. The approved plan/workspace hashes
are unchanged. The controller's under-budget retry path validates sealed
failure/teardown/provider time and reserves $0.75 conservatively for the
allocated attempt; a further two-hour L4 still fits the candidate $3 slice
and overall $15 ceiling. Corrected retry `20260930T200133Z` had a clean
pre-allocation stockout and is independently backed/finalized. No live VM.
The 30-minute automation may attempt a single sequential eligible L4 zone
after rechecking auth, all prior finalizations, resource absence and budget.
Do not duplicate allocated work. Gate 3 model quality remains unmeasured;
Gates 4–8 and Gate 0B raw-report recovery block HF release.

## First full Gate 3 LR candidate allocated — 2026-10-01 IST

Attempt `measurement/gate3/capability-scale-v1/full-pilot-gcloud/20260930T192827Z`
allocated `ganesh-g3-pilot-20260930t192827z` in `us-east1-c` for `1e-5`
after seven clean capacity stockouts. Card seal:
`11547ac26ad5831bb6f6cbd021cc7329e7c821a57c0ed5c828297a5050296085`.
The first provider status was `RUNNING` at 19:30:41Z. A single watcher is
active in exec session `5732`; do not duplicate it or allocate another VM.
The VM has a two-hour provider STOP. Watcher must verify terminal GCS backup
by independent roundtrip before deletion, then exact resource absence twice.
No optimizer, full epoch or quality result is verified yet. The allocated
attempt consumes a conservative $1.762043024 VM+disk upper plus transfer
reserve against Navneet's $15 incremental ceiling even if it fails. If the
watcher fails, preserve disk/evidence and recover before any retry. The
30-minute same-task automation must inspect this live attempt rather than
retry capacity. Gate 3 and HF release remain blocked.

## Six GCloud L4 stockouts; bounded automatic retries active — 2026-09-30

Navneet approved exact plan SHA
`d4659d3b503d4eb0a0a38d5af6129f668ccef7994a7f678e920ced1a5e55dd09`
with a $15 absolute incremental ceiling and under-budget retries without
repeated approval. The first `1e-5` full-epoch candidate was sequentially
staged in `us-central1-b/c/a`, then equivalent `us-east1-c/b/d`; every
`g2-standard-8` L4 create failed with pre-allocation
`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`. Each refusal has independent GCS
backup, verified download hashes, cleanup and double exact absence at
`measurement/gate3/capability-scale-v1/full-pilot-gcloud/<timestamp>`.
Two project-wide checks afterward found no VM, disk or reserved address and
only the default network. No paid GPU runtime, trained candidate, Gate 3
model-quality result, or HF release resulted. Small GCS operation/storage
charges remain possible; budget must account for them conservatively.

Automation `ganesh-mini-gate-3-capacity-retry` is active on this task every
30 minutes to retry sequentially under the same $15 ceiling. Before any
attempt check DIVERGENCE, auth/project, resource absence, all prior
finalizations and budget. Do not overlap allocation or shortcut evidence
backup/teardown. If allocated, use the one watcher, provider STOP and sealed
terminal backup before deletion. Gate 3 canary/development evaluation is not
yet implemented; Gates 4–8 and Gate 0B raw-report recovery still block release.

## Full Gate 3 VM execution pending new ceiling — 2026-09-30

Navneet requested VM execution ASAP. The new prospective $15 incremental
Gate 3 pilot plan at `docs/plans/GATE3_FULL_PILOT_GCLOUD_EXECUTION_20260930.md`
has SHA256 `d4659d3b503d4eb0a0a38d5af6129f668ccef7994a7f678e920ced1a5e55dd09`.
The ceiling has not yet been explicitly accepted, so no new GCloud action or
VM start occurred. The old $5 qualification-only approval is closed.

The training-only workspace is `artifacts/train/gate3-capability-pilot-v2/workspace-v8.tar.gz`,
SHA256 `a9eee2d31de0cf3728d10c8ee5652615006df83dbb371cf942a4e4ee79a036d8`.
The prospective controller/startup are
`scripts/train/gcloud_gate3_full_pilot.py` and
`scripts/train/gcloud_gate3_full_pilot_startup.sh`. They passed 19 focused
tests and shell syntax, but have not run on GCloud. Revalidate all inputs,
absence and DIVERGENCE state before any allocation. One training LR per VM,
first `1e-5` then `3e-5` only after a sealed complete full-epoch result;
allocated failures get no automatic paid retry. Terminal GCS evidence must
be independently verified before deletion and exact resources absent twice.
The frozen separate canary/development evaluation orchestration is not yet
built; no Gate 3 model-quality result exists. Gates 4–8 and the historical
Gate 0B raw-report gap block Hugging Face release.

## Fresh VM absence check; continue local readiness only — 2026-09-30

On Navneet's request, current `executespecv1` read-only inventories showed
instances `[]`, disks `[]`, reserved addresses `[]`, and only the default
network. No VM existed to kill. The previous qualification's 12 verified
terminal GCS objects remain present; do not re-run or delete them. The local
static preflight and intentionally non-executable draft card are under
`measurement/gate3/capability-scale-v1/full-pilot-local-readiness-20260930`.
Read `docs/plans/GATE3_POST_QUALIFICATION_LOCAL_READINESS_20260930.md` before
full-pilot implementation. The local Mac is not a qualified CUDA training
host, and existing capability-pilot provider binding rejects GCloud. Continue
locally on the distinct bounded GCloud card/runner/backup implementation and
tests only. No new GCloud compute or full quality pilot without a separately
approved scope and absolute ceiling. Gate 3 remains open.

## Gate 3 L4 qualification passed; zero live project compute — 2026-09-30

Attempt `gcloud-qualification/20260930T131906Z` is finalized with exit 0.
The 16-row/two-step report passed on the approved single L4, with finite loss,
4,634,705,920 peak-VRAM bytes, and 329.666 input tokens/second. It is sealed
at `380c96b93ba1b7d8272c8e1c04823432309610b0cc21e6e4afb71f7a456a9b47`.
The explicit GPU preflight passed at 23,659,151,360 CUDA-visible bytes, BF16
supported, one device. Terminal backup verification reports 12 objects and
the runtime inventory passed before resource deletion. Finalization says
`terminal-backup-verified-and-exact-resources-absent-twice`; project VM/disk/
reserved-address inventories are `[]`. The watcher completed; do not restart
it or allocate another VM under the consumed retry. The prior
`20260930T131318Z` zone refusal is separately backed and finalized at zero
GPU runtime.

Next: locally build and validate the actual-host full capability-pilot cards,
retaining the frozen two learning rates and quality/evaluation gates. The
qualification establishes throughput and hardware feasibility only. A full
quality pilot on GCloud needs new explicit authorization and a fresh bounded
cost plan; the earlier $5 approval was qualification-only. Current Gate 3
model quality is unmeasured, Gates 4–8 and HF release remain blocked, and the
historical Gate 0B raw-report recovery gap still needs exact evidence.

## One approved L4 retry is live — 2026-09-30

Authentication was restored. The project had no VM, disk, or reserved address
before launch. `us-central1-a` produced a zero-runtime capacity refusal,
preserved in `gcloud-qualification/20260930T131318Z`, with independent GCS
backup and double exact resource absence. The one allocated attempt is now
`gcloud-qualification/20260930T131906Z` in `us-central1-b`, VM
`ganesh-g3-qual-20260930t131906z`, card seal
`e37df182b74d65b5629ad01afd434afa797132f8c98d0c07a237efaa217f3045`.
Watcher PID `10161` / exec session `46951` began 13:21:16Z and must remain
the only watcher. Do not allocate again, even if this probe fails. Observe
its status/serial output, then verify terminal backup and double absence via
the existing watcher before claiming cleanup. The same cumulative $5 includes
the $2.50 reserve for all earlier starts. No current optimizer result, full
quality pilot, Gate 3 pass, or HF release yet. The Gate 0B raw-report recovery
gap remains a separate release hold.

## Await GCloud CLI login before approved bounded retry — 2026-09-30

The user approved the 22-GiB L4 usable-floor plan. Local wiring/workspace-v4
and 57 focused tests pass; `usable-floor-retry-v1/local-provenance-manifest.json`
is sealed at `7a5280d6053fcf2341003347df8ba1b49b6e1448257812487605c3531df49770`.
No GCloud allocation has begun. The first read-only instance-list call failed
with reauthentication required for the existing CLI account. Ask Navneet to
complete `gcloud auth login` for `admin@executespec.ai`; never seek credentials
in chat or bypass the login. After confirmation, check account/project, then
project VM/disk/address inventories and exact related resources; stop on any
unexpected active resource. Revalidate local provenance and plan SHA before
preparing. Use `--usable-floor-retry-prior` at `20260929T133600Z`, `--approved-plan-sha`
`3bee60eb0987eccd8147d638b31beb5f4322539c32f68537b6c06d2943573de7`,
workspace-v4, and $2.50 prior-spend reserve within the SAME cumulative $5.
One new allocation maximum; no automatic paid retry after failure. One watcher,
terminal backup/independent verification before deletion, double exact absence.
Historical Gate 0B raw-report recovery gap remains separate release hold.

## Approved L4 floor retry staging; no new allocation yet — 2026-09-30

Navneet approved the exact plan SHA
`3bee60eb0987eccd8147d638b31beb5f4322539c32f68537b6c06d2943573de7`.
The versioned CUDA host check, card builder, SFT guard and training-only
qualification now use L4 >=22 GiB usable/BF16/exactly one CUDA device; non-L4
still needs 24 billion bytes. A sealed separate hardware operand report is
written before model load even on failure. Workspace-v4 is sealed with 73
evaluation-free files, archive SHA
`0b044e5dc44cc7bc1828cc73f5964a825baafb90d16c7aeac4d8264537d114ae`.
Fifty-seven focused tests and the real three-attempt finalization/budget binding
pass. Prepare using `--usable-floor-retry-prior` pointing to
`gcloud-qualification/20260929T133600Z` and `--approved-plan-sha` above;
do not reuse v3 or reset $2.50 prior spend. This is ONE additional allocated
qualification start under the SAME cumulative $5, not a full quality pilot.
No new VM yet. Preserve all historical evidence and the Gate 0B raw-report
recovery gap; no HF release claim. On allocation, one watcher, terminal
backup verification before deletion, and double resource absence mandatory.

## Retry authority received; do not repeat unresolved hardware guard — 2026-09-29

Navneet said “ok try again”; no new allocation started. Before spending, obtain
explicit direction on the prospective nominal-versus-CUDA-usable L4 contract in
`docs/plans/GATE3_L4_USABLE_MEMORY_RETRY_20260929.md`. Proposed same L4 class with
22-GiB usable floor plus BF16; larger classes keep literal 24-billion-byte floor.
Runtime code/workspace have not been changed to this proposed interpretation.
Carry all THREE prior paid starts, not just two, within the same cumulative $5.
Read-only recovery checks are recorded in
`measurement/gate3/capability-scale-v1/hardware-floor-reconciliation-v1`.
The passed Gate 0B raw qualification's original URI/current object/all versions
are unavailable; local admitted summary and backup manifests remain preserved.
No equivalent report found in the related archive roots checked. Do not infer
every copy is lost; recover exact hash-matching raw evidence before release.
No further GPU job until hardware clarification; no full quality pilot or HF
publication. Current data seal/draft count remain unchanged, Gate 3 open.

## No live VM; GPU preflight stop preserved — 2026-09-29

Attempt `gcloud-qualification/20260929T133600Z` finished with qualification
exit 1; watcher session 21750 completed verified backup and double-absence
teardown. No GPU/disk remains in the recorded project inventories. Ten terminal
objects were independently verified. Canonical materializer passed on the VM
with the same 13-file seal as local verification; the packaging fix worked.
The probe stopped before model loading at the combined BF16 / 24-billion-byte
memory floor. Neither current CUDA-memory bytes nor BF16 support was recorded
separately. No optimizer step, throughput, OOM or model-quality claim is valid.
Historical L4 CUDA bytes were below this literal guard, suggesting nominal vs
usable-memory mismatch; do not present historical bytes as this device's result.
See `hardware-guard-failure-assessment-v1.json` in the exact attempt directory.
Next local work: reconcile the frozen hardware floor with previously executed
mechanism evidence and design explicit operand diagnostics, prospectively.
No paid retry is authorized: the approved exception was consumed. No full pilot,
Gate 3 pass or HF release. Preserve all immutable inputs and failures. Keep
the 30-minute automation active but quiet on unchanged blocked state.

## Live corrected qualification; allocated exception consumed — 2026-09-29

Current attempt `gcloud-qualification/20260929T133600Z` is RUNNING in
us-central1-a, VM `ganesh-g3-qual-20260929t133600z`, card
`f5a61b95a48fddf25e941613446d3e82ff259120dabb19e096f4abee542d21d5`.
Exactly one watcher PID 85859 / session 21750 started 13:37:58Z. Verify its
process before doing any finalization; never duplicate a live producer/watcher.
The user-approved canonical-input exception is consumed by this allocation.
No paid retry if it fails. Same cumulative $5 and $2 prior-spend reserve.
Startup verifies the materializer's generation/SHA, materializes only the 13
canonical upstream files, then runs the unchanged offline 16-row/two-step probe.
Runtime output includes model-canonical-materialization.json; original archive
and all old failures remain immutable. Forty-nine focused tests pass and the
implementation snapshot is backed to GCS. No throughput result, full quality
pilot, Gate 3 pass or release. Watcher verifies all terminal files before
deletion and double resource absence; preserve disk if backup fails. Keep the
30-minute automation active and quiet on unchanged state until Gate 3 passes.

## Approved canonical-input exception; qualification staging — 2026-09-29

Navneet approved `0cb94af6f12bae840c6657c7d7f6402759b0313d7301b81c96afcb9fb5fb342e`.
Launcher/startup wiring is complete; 49 focused tests and actual prior-evidence
binding pass. Use `--canonical-rescue-prior` pointing to `20260929T114450Z`
and `--approved-plan-sha` for preparation. Carry $2 prior reserve within the
same cumulative $5; exactly one additional allocated start, no paid retry.
The CPU materializer is an additional immutable input; workspace-v3 remains
unchanged and evaluation-free. No new VM yet; staging in bounded US regions.
Gate 3 remains open, no quality pilot or release approval. If capacity refuses,
complete failure_finalize before another zone. If allocated, one watcher only;
verify terminal backup before deletion and double absence. Do not duplicate.

## Next user action: one prospective canonical-input correction — 2026-09-29

No VM is live. Both allocated starts and all refusals have complete verified
GCS backups and exact temporary-resource absence twice. Current pilot has zero
optimizer steps; Gate 3 is not passed and no HF release is admissible.
The exact cached archive's 13 upstream files passed full CPU hash verification,
canonical-only materialization, and the unchanged inventory checker. Preserve
the original archive plus 47 sidecar and 29 download-cache metadata hashes.
The reusable clean input is `artifacts/models/gate3-canonical-input-v1`.
Forty-five focused tests pass. CPU materialization seal is
`fe540d05ffa45b1392b87d83885dda21d9598a6dc6b7f2b19a126b088bd98402`;
strict recheck seal `12ef547d30aac92d4303b30a2ae56295480a2dfaf2cd64905598702b1add1026`.

Await explicit approval of
`docs/plans/GATE3_CANONICAL_MODEL_MATERIALIZATION_RESCUE_20260929.md`, SHA
`0cb94af6f12bae840c6657c7d7f6402759b0313d7301b81c96afcb9fb5fb342e`.
It is a prospective exception for ONE additional allocated correction, within
the SAME cumulative $5 ceiling with $2 reserved for prior usage, not a new $5.
After approval, wire the tested CPU canonicalizer as a hash-pinned startup
input and carry both prior runtime attempts into the new budget/card; the
current launcher supports only the exhausted first preprobe rescue and must
not be reused with a reset prior-cost field. No further paid start before this
exception is approved. No full quality pilot, eval opening or training under
this qualification-only proposal. Keep the 30-minute automation active until
Gate 3 genuinely passes, quiet on unchanged blocked checks.

## No live qualification VM: metadata preflight failure finalized — 2026-09-29

The corrected `20260929T114450Z` attempt failed before model load with
`model directory file inventory differs` (exit 1). Watcher session 17524 / PID
75202 completed terminal hash verification, exact teardown, double absence,
and evidence upload. Both paid startup attempts and every refusal are fully
preserved. Project VM, disk and reserved-address inventories are empty.
No optimizer step, throughput report or current model-quality pilot exists.
The cached `artifacts/gcloud-inputs/gate3/model.tar.gz` matches the pinned GCS
SHA `846221797a5b57db5d7184680df4e74641a61504f687f86b81d85a471bb8c930`.
Archive diagnosis found AppleDouble sidecars plus Hugging Face download-cache
entries. `scripts/train/inspect_model_archive.py` is performing offline byte
verification against the 13-file canonical upstream inventory. Preserve the
strict checker and original archive; any correction must materialize only
verified canonical files while preserving excluded metadata evidence. No
chained paid retry under the current contract. Gate 3 is not passed; leave the
30-minute automation active, quiet on unchanged blocked checks.

## Current corrected qualification attempt — 2026-09-29

The corrected startup rescue is at
`measurement/gate3/capability-scale-v1/gcloud-qualification/20260929T114450Z`
in us-central1-a, suggested by the previous capacity response. Its card seal
is `464bb74ce4eda39dcc939d8da5ff920202f6a3c57afccf0aac1af036cd0e4ce1`.
Launch succeeded: VM `ganesh-g3-qual-20260929t114450z` is RUNNING. The bounded
watcher is active (PID 75202, exec session 17524, started 11:47:26Z); verify the
actual process before any independent finalizer. Never duplicate/restart the
VM or watcher. Thirty-seven focused tests pass, including stopped-VM serial
handling and the entrypoint override. The original paid preprobe
failure at `20260929T112530Z` and all five capacity refusals (including
`20260929T114020Z`) are fully backed and finalized, with double resource
absence. This attempt retains the $1 prior-cost reserve within cumulative $5.
The fixed script explicitly overrides the image entrypoint. No probe or
optimizer step has executed yet; Gate 3 remains open. The watcher verifies
every terminal inventory file and independent GCS recovery before exact
teardown and double absence proof. If backup fails, preserve the evidence disk.

## Preprobe entrypoint failure: cleanup before one same-budget rescue — 2026-09-29

`gcloud-qualification/20260929T112530Z` stopped with exit 2: the inherited
image entrypoint attempted missing `/workspace/scripts/cuda/qualify.py`.
The intended throughput script never executed; no optimizer step or quality
result exists. Watcher PID 69510/session 23671 exited on unavailable stopped-VM
serial output. Manual `finalize` completed independent terminal verification,
exact teardown, double absence checks and evidence upload. Keep that failed
attempt immutable. The corrected rescue at
`gcloud-qualification/20260929T114020Z` was refused for capacity in us-central1-b;
its `failure_finalize` is running in session 36351 (verify actual process).
The service explicitly recommends us-central1-a as available; retry there
only after the current refusal is finalized. Preserve the original prior-spend
reserve by supplying `--prior-preprobe-attempt` on every capacity retry.
The corrected startup uses explicit `--entrypoint python3`, and the inspector
skips stopped-VM serial output. Thirty-five focused tests pass.
After complete finalization, prepare one bootstrap-only rescue with
`--prior-preprobe-attempt measurement/gate3/capability-scale-v1/gcloud-qualification/20260929T112530Z`.
The controller requires this exact independently backed, pre-training failure,
double resource absence and a measured runtime under 15 minutes; it binds a $1
prior-spend reserve within the existing cumulative $5, not a new budget. No
chained paid retries, no quality pilot, no change to recipe/data/evaluation.

## Live L4 qualification VM: never duplicate — 2026-09-29

`gcloud-qualification/20260929T112030Z` in us-central1-a was refused for L4
capacity. Its `failure_finalize` completed verified GCS backup, double resource
absence and cleanup evidence upload. Preserve all four finalized refusals.
The current us-central1-b attempt launched successfully at
`measurement/gate3/capability-scale-v1/gcloud-qualification/20260929T112530Z`,
VM `ganesh-g3-qual-20260929t112530z`. Card seal
`f0268ab2cb3fede3034bb081e01a8e50b30dec141f218b75a919b256cbdf739a`.
Use the controller's `inspect`/`finalize` commands against that exact directory;
never duplicate or restart this VM. Fresh authority covers ONLY this live
qualification, its evidence inspection/backup and teardown within cumulative
$5. The provider STOP cap is two hours; probe timeout is 30 minutes. Once
stopped, verify terminal inventory and independent GCS backup before deletion,
then check exact-resource absence twice and project billable leftovers. Same
scope; Gate 3 remains open with no GPU measurement yet.

The bounded local `watch` controller is active (PID 69510, exec session 23671),
started 2026-09-29T11:32:38Z. It observes only this VM every 60 seconds and, once
TERMINATED, performs independent terminal backup verification before exact
teardown and double absence checks. Do not run another watcher or finalizer
while that process is alive. Check its actual process and sealed finalization
artifacts; a stale `watcher-started.json` marker is not process-liveness proof.
If the watcher exits on a backup error, preserve the stopped evidence disk and
resolve the exact backup before cleanup. Thirty-three focused tests pass,
including stopped-only finalization and duplicate-watcher rejection.

## US capacity fallback, same cumulative $5 scope — 2026-09-29

All three us-east1 attempts (`20260929T110307Z`, `20260929T110950Z`,
`20260929T111500Z`) were refused for L4 capacity, with zero GPU runtime.
Every refusal has independently verified GCS backup, exact temporary-resource
absence twice, and backed cleanup evidence. Preserve them as infrastructure
results, never model-quality failures.
The current us-central1-a fallback is staging at
`measurement/gate3/capability-scale-v1/gcloud-qualification/20260929T112030Z`.
Use the controller against this exact directory to launch/inspect/finalize;
do not duplicate a live VM. The prospective location fallback is recorded in
DECISIONS and reserves $0.50 for inter-region transfer within the existing
$5 ceiling. Thirty-one focused tests pass. The recipe, input bytes, 16-row
probe, two-hour STOP limit and backup-before-delete contract are unchanged.
No full quality pilot is authorized under this qualification budget.
Gate 3 remains open; teacher drafts remain 1,060/1,200.

## Qualification zone retry after verified zero-runtime refusal — 2026-09-29

The first us-east1-c attempt at
`measurement/gate3/capability-scale-v1/gcloud-qualification/20260929T110307Z`
was refused for L4 capacity, generated no VM/disk, and has a verified GCS
backup plus double exact-resource absence. Keep its evidence immutable.
The us-east1-b retry is being staged at
`measurement/gate3/capability-scale-v1/gcloud-qualification/20260929T110950Z`.
This remains the same $5 cumulative qualification-only authority, not $5
per attempt. Use the checked-in qualification controller's inspect/finalize
commands against that exact path once launched; never duplicate a live VM.
No full-epoch pilot or Gate 3 quality pass yet. Preserve the 1,060/1,200 draft
count and evaluation separation. No additional unrelated GCloud usage.

## Gate 3 GCP qualification approved at $5, staging — 2026-09-29

Navneet authorized GCP GPUs and approved the $5 qualification-only ceiling.
Use `scripts/train/gcloud_gate3_qualification.py` with the new isolated
startup script. The frozen workspace-v3 and three generation-pinned upstream
archives remain unchanged. Qualify in us-east1 beside the existing GCS inputs,
not Mumbai, avoiding cross-region transfer charges. One g2-standard-8 has a
two-hour provider STOP cap; the exact 16-row probe has a 30-minute timeout.
Full pilot runs require a measured budget assessment after qualification.
Verify every terminal file against its inventory and independently recovered
GCS objects before deleting the VM/auto-delete disk, subnet and network;
double-check exact resource absence and inspect project billable leftovers.
The earlier no-GCloud-authority entries are historical, superseded only by
this narrow approval. Gate 3 remains open; do not pause its automation yet.

## Bounded non-GCloud throughput qualifier prepared, not run — 2026-09-24

The 72-file evaluation-free training workspace is now
`artifacts/train/gate3-capability-pilot-v2/workspace-v3.tar.gz` (manifest seal
`b5f83fef4b87bdcb21de5a7bd9756928d84cc54b3ffc42a4539bd0cf5a3ca924`).
It includes `scripts/train/measure_gate3_capability_throughput.py`, which
measures exactly 16 longest admitted rows/two optimizer steps with the frozen
recipe, without retaining a model adapter or touching evaluation. Require an
actual Linux single-CUDA host, instance ID, observed hourly price, and an
absolute incremental ceiling before running it. Its result is input to the
host-bound card builder, not a Gate 3 quality pass. No provider access has
been supplied; no training or GCloud action occurred. Gate 3 remains open.

## Capability pilot locally staged; compute access still needed — 2026-09-24

Use static preflight v2 (seal
`e921f11edfb59f1d1fbf57336b36652b1ad142189071e20c213caf53f8272831`),
local draft card v3 (seal
`7ab68ae1be9e8bc1876bcf89a5c7921755d44d6d8e6a9990ea3a4d38b4108166`),
and `artifacts/train/gate3-capability-pilot-v2/workspace-v2.tar.gz`
(manifest seal `0af157f1d1ecf0bbb8673fd17211b28d520cf58b94c330d715712317f368048a`).
The archive has 71 allowlisted files and zero evaluation files; the pinned
13-file model inventory passed byte verification locally. Card v3 is
deliberately `prepared-not-executable`. The binder needs an actual Linux
single-CUDA host, measured exact-recipe throughput, bounded provider price,
and backup/teardown evidence. No non-GCloud provider credential or local CUDA
was found. Do not fabricate a ready card or reuse old measured throughput.
No GCloud action without fresh explicit authorization, including GCS backup.
The Gate 3 automation stays active; no model training or publication.

## Capability runner/schema added; host execution remains pending — 2026-09-24

`scripts/train/run_sft.py` has a separate fail-closed capability-pilot path.
Old cards, changed data paths/recipe, non-full-epoch token budgets, and
provider/cost mismatches are rejected before model load. The sealed static
preflight is at
`measurement/gate3/capability-scale-v1/pilot-readiness-v1/static-preflight.json`,
report seal `c0b4e4ec9b2967faac984792a96b75e30ffaee223c51705983cb24d4b7313250`.
Static inputs pass, but there is no ready actual-host execution card or local
CUDA; training has not run. Next build a host-bound provider/cost/retention
card after qualified non-GCloud CUDA throughput measurement, then the two
full-epoch LR pilots and frozen executable promotion. No GCloud action without
fresh explicit authorization. Gate 3 remains open; automation stays active.

## Capability pilot static contract added; no CUDA execution — 2026-09-24

`configs/train/gate3_capability_pilot_v1.json` and
`scripts/train/preflight_gate3_capability_pilot.py` now validate the exact
900-row package and frozen recipe. Local static checks pass, but the result
is deliberately `static-inputs-passed-host-and-execution-card-pending` with
`execution_card_ready=false`, `training_executed=false`, and no CUDA on this
Darwin host. Four focused tests pass. Next add the versioned SFT runner/card
path and actual-host preflight, then obtain qualified non-GCloud single-CUDA
compute or fresh GCloud authorization. Keep the old execution cards and
training evidence immutable. Gate 3 remains open; do not publish.

## Gate 3 pilot input prepared, not executable yet — 2026-09-24

Use `artifacts/train/gate3-capability-pilot-v2/prepared-manifest.json`, seal
`4bae0de2096ce8ae973d0f7b3ecc9214d8b6ef2e3addfb31cc4afd37446c2d01`,
for the current 900-row/651,639-input-token response-only cohort. The frozen
50-row validation encoding is byte-identical to
`artifacts/train/expansion-pilot-v1/prepared-validation.jsonl` (SHA-256
`6a9d3aa37b30bc2672517f6d63113011de5f8156aa1049e588fdc70a36b77f46`).
Keep v1 preparation and all old pilot evidence immutable. Do not feed this
cohort to an old execution card: current runner/card schemas bind different
corpus sizes and token budgets. Next version the 900-row pilot contract and
fail-closed preflight, then execute only on qualified non-GCloud single-CUDA
compute or after fresh explicit GCloud authorization. No local MPS substitute,
model-quality pass, or release claim. The Gate 3 automation stays active.
The prospective checklist is in
`docs/plans/GATE3_CAPABILITY_PILOT_EXECUTION_CONTRACT_20260924.md`.

## Corrected Gate 3 900-row data package admitted; pilot not run — 2026-09-24

Navneet approved one-cell plan SHA-256
`1844d190adcdc47496fc18fa9ec94babaeb469931985b384ac0c575726d4b13c`.
The prebound TypeScript repair `reserve-06` generated one 1,151-token draft,
passed semantic, independent test-author, blind delta, executable, scale
separation, and two fresh affected-capability blind AI quality reviews.
Teacher usage is 1,060/1,200. The corrected 720 cohort is at
`measurement/gate3/capability-scale-v1/token-length-replacement-v1/assembly/capability-720.jsonl`,
seal `cfe5877afcf6a78cb26aa55ee2f59b1e82026436e9b8bbb646e55b7cb7b7ae3e`.
The resealed 180 replay rows are byte-identical to prior selection.
The new 900-row package passed full separation, untruncated tokenization,
weighting, and final validation. Data-package seal:
`149b030f11bc0eb054f0a4d511432f33b4123e3b65fab77c2166dca23d1190aa`;
canonical training JSONL SHA-256
`57bf0b35f16f7e846fe9548553124cabc175f969f9bfe6a2a398227056a93df1`.
The source files and manifest are under `token-length-replacement-v1/final-package/`.
Do not confuse data-package admission with a Gate 3 pilot pass. The local
machine has MPS but no CUDA; the frozen BF16/CUDA pilot has not run. No GCloud
inspection or execution is authorized. The original failed 900 package and
3,032-token row remain preserved. Do not publish a model or claim human
review; the blind reviewers were AI. Next: verify bounded pilot/runtime plan,
then execute only on qualified non-GCloud CUDA compute or after fresh explicit
GCloud approval, and assess promotion against the frozen executable gate.

## HARD STOP: Gate 3 900-row token length — 2026-09-24

The new package separation passed 900/900 with zero exact, normalized, or
fuzzy failures, seal `e1df396fd714c9b984649630d03da22efc816245841e80dbdb2e637dc0c805d8`.
The pinned tokenizer then rejected one TypeScript repair row at 3,032 tokens,
88 over the frozen 2,944 maximum; failed report seal
`4e44bd293e5a7d5404ed44600c7534cf0fcf12bb46da60d835281e8449456927`.
No final 900-row admission or training. Do not truncate. Two same-cell
prebound reserves exist but are unused; post-admission token-length replacement
needs a prospective rule because the frozen plan hard-stops on a failed final
corpus gate. Read `docs/process/GATE3_TOKEN_LENGTH_HARD_STOP_20260924.md`
before any further Gate 3 construction. No GCloud action is authorized.

## Gate 3 720 capability admission sealed; replay selected — 2026-09-24

Use `measurement/gate3/capability-scale-v1/capability-720-seal-v1/manifest.json`
(seal `1bf0e65c4704fcab266f97da4af793ff9d7fdcd3a37df792be9cfc1271e1b448`)
with `provisional-capability-720-v2/capability-720.jsonl`, not v1. The 20
deterministic samples passed two independent blind AI review batches with no
failures (quality seal `863190b2519742ec2b16e404910fcad9749b9d38f5af4ef82c1aecbd234101bf`);
do not claim human review. The 720 seal binds prior entry, unique verified
scale rows, passed scale separation and the quality evidence. The selected
180 broad-replay rows are at `broad-replay-v1/replay-180.jsonl`, selection seal
`5b98721409b514e0ea830d24721aa327cecbad4a8fd6d16259af96b3b902fb65`.
Next: complete package-level 900-row separation, tokenization and weighting,
final Gate 3 validation, then the bounded pilot. No GCloud authorization;
do not inspect GCloud. No final 900-row corpus or training pass exists yet.

## Prospective one-cell repair provisionally assembled — 2026-09-24

Navneet approved one new source-unique Python repair replacement to resolve
the duplicate-reserve deficit. The original failed cohort remains immutable
and cannot be counted as 546 unique rows. See the prospective plan at
`docs/plans/GATE3_DUPLICATE_RESERVE_PROSPECTIVE_REPLACEMENT_20260924.md`
(SHA-256 `81ba26cbe4b6557bc693ac63e261e6c6d787f08c669b6b42f1415a4649f8d3ad`).
The sole new source `exp-v1-python-repair-0365` is prebound in
`measurement/gate3/capability-scale-v1/prospective-replacement-v1/` under
manifest seal `92e32585027a80c3637383d0c0c025f3c943529c6953ef95b0e857e4c0b89a18`.
The one allowed new teacher draft generated successfully, bringing counted
usage to 1,059/1,200. Its semantic, independent test-author, blind delta, and
executable checks all passed. The new provisional 546-row assembly has 546
unique candidate IDs and source identities under report seal
`4f5845d95193e3cbb5df7ff32a1c47c7b432bf484229b7162251addd81384e40`.
Next perform global separation and construct the 720 capability plus 180
broad-replay package; quality, tokenization/weighting, and final validation
remain mandatory. The old queue stays hard stopped, and no training or
Hugging Face publication is eligible yet. No GCloud action is authorized.

Update: `materialized-scale-v1` binds all 546 rows to admitted matrix
envelopes with independent tests, seal
`8f27cb55c1b6fedea24b2a2e7d086a78203b327c94022fa18f08a213a0a1023b`.
Its content-free separation against 3,399 prior/retained training rows and
540 frozen private evaluation tasks passed every exact, normalized, and fuzzy
check with zero failures, seal
`c59b89500390781b21a520983a68f5c33830427e7eef4ea6108b07491dde3475`.
Use `provisional-capability-720-v2`, not v1: v2 contains the verified
envelopes and has 720 unique IDs/sources, six per cell, report seal
`5cd935997b35647e111ed809329c5831c498e762d449fb33cad4caab22c206cc`.
The capability cohort is not yet a passing 720 admission seal. Blind quality
review, replay, package-level separation, tokenization, and validation remain.

## HARD STOP: duplicate canary reserve in scale cohort — 2026-09-24

Do not continue generation, reserve activation, separation, packaging, or
training under the current Gate 3 queue. The provisional 546-row assembler
correctly rejected 546 rows / 545 unique IDs because
`cap-scale-associative_aggregation-python-repair-reserve-06` was used as a
canary admission and again in the 16-reserve phase. The source identity is
identical; candidate content differs. No corpus output was written. That
cell has only five unique records toward six, and its sole allocated reserve
was already consumed. The remaining first-pass failure is a known-bad
cross-cutting failure, not eligible for blind test reauthor. Preserve all
prior teacher, semantic, delta, and executable results, but do not grant
duplicate admission credit. See
`docs/process/GATE3_DUPLICATE_RESERVE_HARD_STOP_20260924.md` for the exact
record/source hashes. Counted teacher usage is 1,058/1,200; training
inventory remains 174/900. A prospective user-directed resolution is needed.
No GCloud action occurred.

## Go requalification accepted; reserve teacher active — 2026-09-24

The uniform 89-Go-candidate single-worker matrix sealed 83 admitted / 6
rejected / 0 unresolved under report
`1f7f770109b5c54b1d83746e181d63db81b7900d63e47c21a3d9c28df6d0c0d7`.
The fail-closed assessment accepted it with zero original-admission regressions,
seal `49ae1b356c318513da0fb034f1602bf0046ff65cc3f527091913e305b5b8524f`.
The derived 534-row first-pass matrix is 508/26 admitted/rejected, and the
one-correction reconciliation is 518/16, report seal
`fc3cdd3285be248dd01021898ce42229f06de841e62576e4c0e3033faff3c0ee`.
These are provisional executable counts, not training admissions. The 16
remaining failures each have an eligible reserve; the sealed ledger is
`895bb5ac34499b9722a767c057654a1f4bcb66e8cf32005f99c6a99b1def73ae`.

A 16-request reserve cohort completed teacher, semantic, independent
test-author, and fresh blind delta at 16/16 each. Its one-worker executable
matrix sealed 15 admitted / 1 rejected under
`f0d4cfba3059b179050af25e0df8741157c7549abd794df29968a7500c540eb4`.
The sole Go reference-primary failure used its one allowed blind reauthor;
the correction passed fresh delta and executable matrix under seal
`ce68d2f3ad1c6dc9cfe15d2f8bb88f4db30c1d93ca6b92f4a16571ea32758b75`.
No reserve verifier is running. All 16 slots are provisional executable
admissions. Conservative teacher usage is 1,058/1,200; do not reset this
accounting.
Continue to final separation, six-per-cell capability admission, 15-per-pair
replay selection, quality review, tokenization/weighting and package sealing.
Training inventory remains 174/900, and model training has not started.
No GCloud usage is authorized without a fresh explicit approval.

## Go single-worker requalification active — 2026-09-23

The 534-row first-pass executable matrix sealed 476 admitted, 24 rejected,
34 unresolved under report
`01ab1d4b460a922e81b61497a923e2ac0c577eceb607288f9734a5a7f951f5e3`.
All unresolved were Go 60-second timeouts. The first blind test-reauthor
correction covered 18 reference-failing rejects: one structural reject,
17 fresh delta passes, and a new executable matrix with 10 admitted / 7
rejected under seal
`d8425db28fcffbbd052d70d7677d42c3db8f7803303415c7a63cdc36b8c9af91`.
These results are additive only after final cohort reconciliation; do not
alter original artifacts or count failures as admissions.

A uniform requalification of all 89 original Go first-pass candidates is
running locally with one verifier worker under
`measurement/gate3/capability-scale-v1/first-pass-v2/go-single-worker-v1/`.
Input manifest seal:
`d35ec1d47706d409b92260d21f4595d9431f9f2eeabcb33cef4a61e199fc7ea0`.
It keeps exact candidate/test/delta/runtime/60-second-limit bytes, changing
only scheduling. Inspect that process and sealed results; do not start a
second campaign. See
`docs/plans/GATE3_GO_SINGLE_WORKER_REQUALIFICATION_20260923.md` for the
fail-closed acceptance rules: all 89 input hashes equal parent, no unresolved,
no regression of original admissions, and no cherry-picking. If it passes,
derive a new aggregate by replacing the entire Go slice, then assess exact
per-cell deficits, remaining bounded corrections, reserves, separation, and
corpus packaging. The authoritative inventory is still 174/900; training and
release are not ready. No GCloud action occurred in this continuation.

## Gate 3 executable matrix active — 2026-09-23

Current local campaign: the remaining 534 first-pass teacher requests are
complete. The original 381 generated / 153 no-output usage-limit result is
preserved; a targeted replay generated all 153, and the merged teacher report
seal is `f53ab8e2da3182819874b67aaf6de21d5c131f6fb7d1175221dfc5399ec49f6c`.
Semantic review passed 534/534 (seal
`357627f4f5ea43eb99578c9eb81fb47cb1d09084d5f09c91034029ad60d79e82`),
and independent test authoring passed 534/534 structural checks (seal
`c4961be372d978e8f79b2b9313c044964c84366a4ede9b0ae16dfa30ff03a3ca`).
The first blind delta campaign sealed 407 passed / 127 CLI transport-fallback
classification failures. Its original evidence is intact. A narrow parser
correction recognizes only a completed WebSocket-to-HTTPS fallback notice as
non-tool, and 127 new targeted calls passed. The merged delta report seal is
`97d41488f34db77e1831f528d8f27e5cd45ca6d33e50ef7b5a596554e5e094e7`.

The exact four-way executable matrix is running locally in Docker under
`measurement/gate3/capability-scale-v1/first-pass-v2/final-matrix-v1/`.
At 2026-09-23 14:37 UTC, 44 of 534 per-candidate matrix artifacts were
sealed: 38 admitted, 6 rejected, 0 unresolved. Read the current artifact
count and statuses rather than treating this snapshot as final. The live
controller may still be running; do not launch a second matrix process.
After it seals, inspect actual per-cell deficits, then activate only eligible
source-unique reserves and allowed one-time test reauthors under the frozen
1,200-teacher-draft ceiling. Historical 489 + canary 19 + remaining first pass
534 = 1,042 returned drafts, leaving at most 158. Then complete separation,
the 720+180 corpus package, and later gates. The authoritative training-entry
inventory remains 174/900 until final admission/package evidence is sealed.
No GCloud operation was performed on 2026-09-23; a fresh explicit approval is
required before any GCloud usage. An hourly same-task continuation is active
under automation `ganesh-mini-hourly-continuation` and should remain quiet
while the matrix is merely progressing.

## Scale canary passed; remaining first pass active — 2026-09-18

Resume from the passed 12-cell canary result at
`measurement/gate3/capability-scale-v1/canary-final/canary-result.json`, seal
`dc239958fc66b793830a19c254c54cdfad316263cc0eb04607a0e76454a13ad3`.
It contains 12 admissions, 19 teacher drafts, seven activated source-unique
reserves, two blind test reauthors, zero unresolved outcomes, and zero
evaluation reads. Preserve every failed v1 and pre-correction artifact.

The remaining 534 first-pass teacher requests are running locally under
`capability-scale-primary-delta-teacher-prompt/v2` with artifacts rooted at
`measurement/gate3/capability-scale-v1/first-pass-v2/`. The v2 prompt requires
the sole known-bad defect to target the primary capability while already
satisfying the scheduled cross-cutting behavior. Resume this exact campaign;
do not regenerate the consumed 12 first-pass requests. After teacher closure,
run semantic review, independent test authoring, fresh delta audits, executable
matrices, bounded reserves, separation, and package assembly. The admitted
training-entry count remains 174/900 until that package is sealed. No GCloud
resource or training job is active.

## Scale source queue sealed; implement resumable construction — 2026-09-17

Resume from
`measurement/gate3/capability-scale-v1/source-queue-manifest.json`, manifest
seal `f3e3e312625ec85f067c0089f40b16ed4591fe320745445e34f23825a3dc6d55`.
The queue contains 546 first-pass and 165 reserve requests with 711 unique
sources. The queue file SHA-256 is
`a8d9eb96cdbdb8ccd4ec126b512c71ae832856beff9dd46a799c99571eefba51`.

Next implement and locally preflight a resumable, per-candidate sealed
construction controller using the V9 canonical teacher/test/delta/executable
contract. Start with content-free schemas and one canary per lane/task type;
do not launch the 546-call first pass until readiness, restart behavior, and
exact source/queue bindings pass. Reserves remain ineligible until a matching
first-pass failure is terminal. No GCloud action or training is active.

## Training entry passed for construction; freeze the scale queue — 2026-09-17

Resume from `measurement/gate3/training-entry-v1/manifest.json`, manifest seal
`fbf45982984c2c669e03abf1c773d768019651184547104271de12c42f79318c`.
The exact qualified inventory is 174 records: 114 generation and 60 repair,
with 174 unique sources and complete 120-cell coverage. Do not discard the 54
non-anchor generation admissions.

Next seal the deterministic unused-source queue and prospective construction
contract for 546 additional capability admissions—246 generation and 300
repair—plus 180 broad replay records. The final target is 720 capability rows
and 180 replay rows. Training remains blocked until the complete 900-row
package passes integrity, balance, quality, separation, tokenization,
objective-weighting, retention, and runtime checks. No GCloud resource or
training job is active.

The prospective scale contract is
`docs/plans/GATE3_CAPABILITY_SCALE_CONSTRUCTION_PLAN_20260917.md`, file SHA-256
`d0e2b112eaa17eb96d2a0284964c9d107bc94b3fcd8edc6369cf7792026100ee`.
It conservatively counts 489 historical teacher drafts against the 1,200 cap,
leaving 711: 546 first-pass requests plus at most 165 replacements. Next build
and seal that source-unique queue; do not start candidate calls before its
historical source-exclusion and count checks pass.

## Gate 2 passed under V9; resume at training-entry assessment — 2026-09-17

Resume from the sealed V9 qualification, not from any V6–V8 intermediate
attempt. The repair cohort is complete: 60 admitted, 0 rejected, and 0
unresolved. V2 generation equivalence is still passed for 60/60 generation
cells, yielding 120/120 combined generation/repair coverage.

Canonical current artifacts:

- V9 plan:
  `docs/plans/GATE2_REPAIR_DELTA_V9_LITERAL_KEY_GUARD_PLAN_20260917.md`,
  SHA-256
  `b050cb106bbbef023f99780ce5b3d843fe0f3d247f82f67adf2375f49142e641`;
- V9 readiness:
  `measurement/gate2/capability-stratified-v9-literal-key-guard/final-v1/readiness-v9.json`,
  report seal
  `008e6a3479fd40066c648753d78d342989a72adf5359f9b54ad7cdf6f3998452`;
- V9 qualification:
  `measurement/gate2/capability-stratified-v9-literal-key-guard/final-v1/qualification-summary-v9.json`,
  report seal
  `cb0eafa84cbd76ff90c72456883c854d22356bb87da7a1ecf6a7bd4cf50ade0e`;
- result narrative:
  `docs/process/GATE2_V9_RESULT_20260917.md`, file SHA-256
  `328fd26edf953a1369847179d92246adf927a72c6df4c92f46b52dcd597b47a6`;
- complete-cohort separation report seal:
  `6939abd59610a771288f9232604f6d2c32c8ad74be1bc3398337ab22f8063647`;
- V2 generation qualification seal:
  `293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139`.

Preserve the predecessor results unchanged: V6 readiness failed under seal
`39a8264850aafb9c8b8db6ed9de4f8d6e0d46b4ad331329a4e2c21c6cce3f778`;
V7 ended at 58/60 and zero unresolved under seal
`1bbdd82b8558542547f0476e8b753089a0c93e73221f4db4c6b6b9787dde3f06`;
V8 stopped before delta/execution on the validator no-go under seal
`ff2de8bc59f6f0da95e53bb020470df3b2abbda5b1f76c83f03f6814f6648af5`.
Do not relabel or rerun those contracts.

Next, freeze the exact 120-cell qualified corpus/training-input lineage and
perform the explicit Gate 3/4 training-entry assessment. The V9 qualification
does not itself authorize training. No new training has run, no compute is
running, and no GCloud resource is active. Untouched evaluation, publication,
and release remain downstream gates.

## Gate 2 V5 terminal no-go; design a new prospective contract — 2026-09-17

Resume from the sealed V5 result, not from either interrupted attempt and not
from pre-separation. The final ordered cohort is complete: 29 admitted, 31
rejected, 0 unresolved. Frozen first-pass thresholds failed, so no V5 reserve
is eligible and no V5 candidate may be relabeled or rerun.

Canonical artifacts:

- terminal inventory:
  `measurement/gate2/capability-stratified-v5-interface-replay/primary-two-phase-v3/two-phase-inventory.json`,
  report seal
  `6e1512cf01b00272120e041b74487bfc66105627d01db13e9f9a1b1bbe99796d`;
- exact ordered terminal artifacts:
  `measurement/gate2/capability-stratified-v5-interface-replay/primary-two-phase-v3/terminal-artifacts.jsonl`,
  file SHA-256
  `5ab70923a54311db8942fa7210c7689e0418ed09f7065d5b8d035a19bcbcdf70`;
- admission report:
  `measurement/gate2/capability-stratified-v5-interface-replay/primary-admission-v3/report.json`,
  report seal
  `3b112519be6c3f122499d137983a58288bdad16bdfaea8c7c83f34c45dc58b11`;
- qualification summary:
  `measurement/gate2/capability-stratified-v5-interface-replay/qualification-summary-v5-primary-v3.json`,
  report seal
  `f169894cc32557388ec7812180d1524502af1ae35c310e8f31f3c4177e5452e5`;
- result narrative:
  `docs/process/GATE2_REPAIR_DELTA_V5_RESULT_20260917.md`, file SHA-256
  `0e7571e0b345568dcbc073d4c7086ec33ee58d73327dfeeea2ae33c0e3e53ca0`.

Failure taxonomy: 14 strict test-author rejects, 17 executable rejects, and 29
admissions. Lane admissions are Go 8, Java 5, JavaScript 1, TypeScript 4,
Python 10, and Rust 1. The post-run audit finds 10 validator false positives,
4 Java role-path collisions, and 17 authored-suite runtime-binding failures;
none demonstrates a bad reference. All model calls in the final attempt
completed successfully and there are no unresolved infrastructure outcomes.
Do not relabel V5; use these mechanisms only to design a prospective contract.

The controlling successor is
`docs/plans/GATE2_REPAIR_DELTA_V6_CANONICAL_TEST_REPLAY_PLAN_20260917.md`,
SHA-256
`4fe6a1374c01a0a682bf256c91a141b36b26680bdb5279049070f4f143418ec1`.
Implement its controller-owned role paths, exact lane import contracts,
executable outcome adjudication, structural retry ledger, and readiness suite.
V6 uniformly carries all 60 teacher candidates and semantic outcomes but runs
60 fresh test authors and fresh blind delta audits; it carries no V5 test or
disposition into its decision.
Do not generate V5 reserves, train, open untouched evaluation, or publish. No
compute is running and no GCloud action is authorized or required. Historical
status percentages remain training 84%, release 58%, overall 72%.

## Gate 2 v4 terminal no-go; v5 plan sealed — 2026-09-16

Resume from the completed V4 result, not from preflight. The ordered first pass
contains 60/60 terminal dispositions: 5 admitted, 55 rejected, and 0
unresolved. Frozen thresholds failed, so no V4 reserve is eligible. Do not
relabel or retry V4 under the same contract.

Canonical result artifacts:

- original two-phase inventory:
  `measurement/gate2/capability-stratified-v4-repair-delta/primary-two-phase-v3/two-phase-inventory.json`,
  report seal
  `8fc2c4ea31628287ae5b8eb83353f13e1e5aebb1fa93af97256d255c3120e087`;
- evidence-only retry-ledger correction:
  `measurement/gate2/capability-stratified-v4-repair-delta/primary-terminal-correction-v3/correction-report.json`,
  report seal
  `05cb34251ceaca6c3c4289779128e208ddd0d238ac2f8aa594253ff5cd1aee51`;
- final admission report:
  `measurement/gate2/capability-stratified-v4-repair-delta/primary-admission-v3/report.json`,
  report seal
  `bfc80e399b44fb350048ed459c2bb611801757fb2c73286389d5c4c98aca99d2`;
- qualification summary:
  `measurement/gate2/capability-stratified-v4-repair-delta/qualification-summary-v4-primary-v3.json`,
  report seal
  `af2ce7ea3cab939ea219eef840af9e42bcb379f0f5de7002bcdf7e688da8c2e5`.

The complete result narrative is
`docs/process/GATE2_REPAIR_DELTA_V4_RESULT_20260916.md`, file SHA-256
`1c550c9fe5141d63d21b3b92a7002293464cebbf80e7b052e51f05d263b40433`.

Failure taxonomy: 30 test-author contract rejects, 23 post-teacher
cross-witness rejects, 2 final-validator rejects, and 5 admissions. The largest
measured mechanisms are interface defects: 27 multi-file role-shape outputs,
3 Java entry-point violations, 10 JavaScript witnesses importing an unstaged
`reference.js`, 10 Rust `main` witnesses compiled as an empty test harness, and
1 Java missing-working-directory failure treated as semantic. Two TypeScript
witness failures and the two final-validator rejects are candidate-local.

The successor contract is
`docs/plans/GATE2_REPAIR_DELTA_V5_INTERFACE_REPLAY_PLAN_20260916.md`, file
SHA-256
`132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b`.
It requalifies all 60 cells with 58 immutable V4 teacher carries and exactly
two fresh TypeScript candidates, but reruns test authorship and all affected
downstream evidence uniformly. First implement the carry/source manifests,
corrected JavaScript/Rust/Java witness interfaces, exact two-role test-author
schema, explicit Go per-suite attempt bounds, and full production-path
fixtures. No V5 model call is eligible until the readiness report passes.
Preserve the V4 plan and evidence unchanged.

No model training or GCloud action is active. Historical process percentages
remain training 84%, release 58%, and overall 72%, but all remain blocked at
Gate 2. Current status is ACTIVE LOCAL V5 IMPLEMENTATION; no compute is
running. `ganesh-mini-1.0` is not ready for public release.

## Gate 2 v3 failed; v4 preflight and source extension active — 2026-09-16

Resume at Gate 2. Do not train, generate a v3 reserve, reuse any v3 candidate,
or perform any GCloud action. V3 is terminal at 60 generated, 0 admitted, 52
rejected, and 8 unresolved after the allowed identical replay. Canonical
artifacts:

- `measurement/gate2/capability-stratified-v3-repair-delta/primary-two-phase/terminal-artifacts.jsonl`,
  file SHA-256
  `b96078c4ea226786b33cd84a802f63232e79d3142e033ac0dde041527efc6aeb`;
- `measurement/gate2/capability-stratified-v3-repair-delta/primary-admission-terminal/report.json`,
  report seal
  `48961ecc86e732afd1fd293d100e214a30e78ad4f692dc248be36f49ea89d8be`;
- `measurement/gate2/capability-stratified-v3-repair-delta/qualification-summary-v3-terminal.json`,
  report seal
  `b2b718a1d61f3a6858b28f9b9938438548a89eb37e04a091ace5036f914c3727`.

Failure breakdown: 3 pre-separation semantic/delta rejects; 40 deterministic
test-staging failures caused by hashed paths versus fixed runtime filenames; 1
real Go known-bad/cross-test orthogonality failure; 8 strict CommitPackFT
provenance-schema rejects; and 8 Go verifier timeouts. The Go timeout signature
is 64/64 attempts at roughly 60 seconds with empty output under concurrent
linux/amd64 emulation on Apple arm64. No v3 rerun is allowed.

The controlling next plan is
`docs/plans/GATE2_REPAIR_DELTA_V4_QUALIFICATION_PLAN_20260916.md`, file SHA-256
`79849d2f8b70ba69572b4c3fa1761bdb413562c6f6d9a12537d93a1724812ef6`.
Implement and seal canonical role staging, compile/cross-witness preflight,
exact dataset-specific provenance, final-validator readiness, lane-aware caps
(Go 1, TypeScript 2, global 6), and end-to-end fixtures before any v4 teacher
call. Strict CommitPackFT provenance support has been implemented locally and
its focused/full data tests passed; it still requires integration in the final
batched commit.

Fresh-queue feasibility is currently negative: 55/60 cells have two sources
after excluding prior, v2, and all 120 v3 lineages. The five deficits are
callbacks/events Python and Go/Rust plus graph/tree Python and Rust. The plan
therefore requires one fixed, content-blind native CommitPackFT tranche: first
1,000 permissively licensed eligible records each from pinned Go, Python, and
Rust files, selected before ontology labels with the v4 seed. Classify all
3,000 once, with no early stop or adaptive top-up. If it does not close the
five deficits, seal v4 source-infeasible before candidate generation.

Current status: ACTIVE LOCAL GATE 2 V4 PREFLIGHT; no GCloud resource or model
training is active. Historical status percentages remain training 84%, release
58%, overall 72%. Gate 2 ETA is 18–36 hours if the single source tranche works;
project ETA is 2–4 weeks after Gate 2 and remains conditional on measured
training transfer.

## Gate 2 v3 repair-delta plan ready — 2026-09-14

Navneet authorized creation of a new plan after the sealed v2 no-go. The new
contract is `capability-stratified-v3-repair-delta/v1`, frozen in
`docs/plans/GATE2_REPAIR_DELTA_QUALIFICATION_PLAN_20260914.md` at file SHA-256
`4023a896300112f9f93f2a16698d549f203e3e75b4e71ae054f3a98463e2f0f0`.

V3 does not retry only the observed Python cell. It requalifies the complete
changed surface: all 60 capability/language repair cells, one fresh candidate
per cell, with at most six uniformly governed reserves. The absolute candidate
budget is 66. The revised contract requires the known-bad implementation to
fail primary-capability tests while already passing the scheduled secondary
cross-cutting tests. It carries the unchanged 60-cell v2 generation surface
only through a sealed equivalence audit; v2 remains recorded as failed.

Current state is READY FOR LOCAL GATE 2 V3 IMPLEMENTATION. Intended paths are
the Gate 2 data pipeline and focused tests plus a new
`measurement/gate2/capability-stratified-v3-repair-delta/` evidence root. No
training or GCloud action is authorized by the plan. Warm execution after
implementation is estimated at 2–4 hours; the low-confidence warm-path estimate
for implementation plus qualification and evidence closure is 4–8 hours.
Project delivery remains 1–3
weeks if Gate 2 passes and later training transfer succeeds. Historical process
progress remains training 84%, release 58%, and overall delivery 72% until v3
produces executed evidence.

## Gate 2 capability qualification terminal no-go — 2026-09-14

The capability-stratified qualification campaign is complete under the sealed
contract and failed its all-cell requirement. The canonical final run admitted
217 of 247 generated candidates (87.85%) and covered 119 of 120 cells. The sole
empty cell is `numeric_reasoning/python/repair`. All 240 original drafts and all
seven permitted replacements were generated and dispositioned; the replacement
for the remaining cell failed independent semantic review. There are no pending
or eligible replacement cells, and the final executable run had no timeout-driven
gap.

Language-family admissions are Go 37/41, Java 35/41, JavaScript/TypeScript
74/81, Python 34/42, and Rust 37/42. The 30 final rejections comprise 18
semantic-ontology rejects, seven reference-solution verification failures, four
terminal no-change correction attempts, and one known-bad-accepted failure.

Canonical decision artifacts are:

- `measurement/gate2/capability-stratified-v2/admission-campaign-final-v2/admission-report.json`
  with report seal
  `c576ef4f5b0f137edac829703eae6d7c4a63cae513544d36471f7ffcf81b7cb7`;
- `measurement/gate2/capability-stratified-v2/admission-campaign-final-v2/qualification-summary.json`
  with summary seal
  `293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139`;
- `measurement/gate2/capability-stratified-v2/replacements-v1/manifest.json`
  with manifest seal
  `435fba0091304f03cedb324fd35ad019a92559f7e76b13202f852fff93bb3209`;
- augmented semantic and separation reports sealed at
  `276e9c90129703393d5223221f6686198bf39e2a267268e22560998a0b3fe3b5`
  and `d323de11ae4e16b1a09b3874534974ff7d022d1e0170af25e6a5408f74cecaf9`.

Current state is STOPPED AT GATE 2 / NO-GO. Do not scale this corpus, start
training, consume a second replacement, or claim `ganesh-mini-1.0` is ready for
public release. No compute is running and no GCloud action was taken for this
campaign. The previously reported workflow percentages remain training 84%,
release 58%, and overall delivery 72%, but all are blocked and must not be read
as quality or release-readiness scores. There is no valid delivery ETA under the
current contract.

Navneet's next decision is one of two materially different paths: close
`ganesh-mini-1.0` as a documented no-go, or explicitly authorize a revised Gate
2 construction contract and a fresh qualification round. A revised contract is
new work; it cannot be represented as another retry under the sealed contract.

## Gate 2 qualification source queue sealed — 2026-09-14

The deterministic qualification source-assignment queue is complete. It binds
240 fresh training-only source stimuli to the sealed 120-cell capability
matrix, exactly two assignments per cell and 240 unique source identities.
All 2,996 source identities already used by the 3,225-row corpus were excluded.
The ignored working queue hashes to
`0cf1a51055d58c4ae0c454aad0f6b8e844cae27517a16516f59bbe428a967c9f`;
the tracked manifest seal is
`53a2465181f10a19a2fe3cbf9d562d5d74d7a19aa9984c878dfbeace559708af`.
Independent replay confirmed the queue hash, manifest seal, record count,
source uniqueness, cell count, and two-per-cell distribution.

These are source assignments, not generated or admitted candidates. Qualified
records remain zero. Next implement the capability-specific isolated teacher,
independent test-author, semantic-review, executable-admission, and reporting
path; do not reuse the old all-edge-cases teacher prompt unchanged. No GCloud
action or model training occurred. Progress remains training 84%, release 58%,
overall 72%; delivery ETA remains conditional at roughly 1–3 weeks.

## Capability-stratified Gate 2 contract sealed — 2026-09-14

The next training-only construction contract is sealed at
`0181751bdd912b8d04ccf954c358cb22681d6fc4aa5b3896a986e7a1ce73af01`.
It defines ten neutral primary capabilities across six languages and both
generation/repair, producing 120 cells. Cross-cutting edge semantics are
scheduled one per cell rather than repeated as generic boilerplate.

Qualification drafts two distinct training-source candidates per cell: 240
total. It must admit at least 120 and at least one per cell, with only one
bounded replacement for an empty cell. Passing qualification can unlock
construction planning for 720 new records plus 180 broad replay records;
new drafting is capped at 1,200. Construction remains isolated from all
evaluation surfaces and uses reference-pass, known-bad-fail, semantic-
conformance, separation, and lineage gates. The 240-draft non-GCloud
qualification is authorized by standing project scope; implementation is next.
The contract grants no training or GCloud authority. Detailed plan:
`docs/plans/GATE2_CAPABILITY_STRATIFIED_CORPUS_PLAN_20260914.md`.

## Gate 2 reopened for a new corpus contract — 2026-09-14

A training-only diversity audit now compares the full authorized 3,225-row
corpus with the 640-row v3 selection without reading any evaluation surface.
The selection is 19.84% of the corpus; all thirteen observable contract tags
are represented between 17.69% and 23.87%, so there is no gross selection-
specific topic dropout. The full corpus has 2,812 unique source records and no
duplicate normalized prompt scaffolds, but its observable wording is dominated
by the teacher contract's repeated string/Unicode, error/malformed, ordering,
and alias/mutation requirements. Lexical uniqueness does not prove capability
diversity. Report seal:
`714fe87491fb798c6248f53e40dd80c9d305125f39dd631db8d7c47114b8f793`.

The prior Gate 2 sufficiency decision was explicitly for one bounded pilot and
is exhausted. The full-corpus failure plus negative capacity, scheduling,
checkpoint, and gradient-conflict experiments now rule out another optimizer-
only probe. Reopen Gate 2 and freeze a new training-only capability-stratified
corpus contract before constructing or training anything else. Private
development and decision tasks remain excluded and must not become templates.
No GCloud action is authorized or active. Detailed audit:
`CORPUS_DIVERSITY_AUDIT_20260914.md`.

## Gate 4 gradient-conflict hypothesis rejected; probe torn down — 2026-09-14

Approved attempt `20260914T003000Z` under proposal
`af67925bf32f28b2708862a517af58b00f161cbbd66c2c3d00db05987f98cd88`
completed as a valid audit-only diagnostic. All eight frozen optimizer groups
were measured before any optimizer step. Across 120 pairwise lane-gradient
cosines, the minimum was `+0.035201297582185986`; no cosine was negative and
none crossed the frozen `-0.05` conflict threshold. Qualifying conflict groups
were `0/8` versus required `4/8`, including `0/8` with JavaScript or TypeScript
participation versus required `4/8`. Stage 2 was correctly blocked with zero
optimizer steps and zero seen training tokens. No PCGrad training, retention
guard, or canary ran. This is a valid mechanism verdict, not infrastructure or
model-training failure.

The audit, run, ledger, and campaign seals verify at
`411885c12f8db68ce22986244c6d67822abcae16aa9f9c23d7a755a740eea69e`,
`af3ea3cf1545f3711f9ca4fdd5a9dca88941a34f820f7403c8245c0d6c9cbfad`,
`a32b193e407719fbff07cbcab2fcb50f00c02850ba36e1a59ca77f2b45db3bc7`,
and `d31915796be69a2f9f0c6e20f0ea387b435d98a9507221f881ced3d842d7785f`.
All 25 terminal-manifest entries independently hash-verified. Control archive,
recovery record, and receipts were exact-generation round-tripped in GCS;
teardown receipt generation is `1789359329656748`, seal
`d73e72e35542428ba5a96a6706e2e036cd26b6c79f789b26a135b54b889dafd9`.
The complete post-teardown provider audit also passed exact-generation GCS
roundtrip at generation `1789359494557821`; its preservation record is
generation `1789359520965327`.
Projected compute cost is `$0.08009125052911889715777777778`.

The exact VM, disk, subnet, and network are absent in two checks 52 seconds
apart. No Ganesh Compute surface remains. The unrelated
`laxmi-wmv2-training-01` disk remains untouched and may bill, so project-wide
GCS-only remains false. Do not run PCGrad, weaken the audit threshold, or open
the canary. Gate 4 is still model-quality blocked. Next return locally to
task/corpus diversity and the persistent `collapse-runs` cluster before
freezing any new bounded mechanism. Full result:
`GRADIENT_CONFLICT_PROBE_RESULT_20260914.md`.

## Gate 4 v3 checkpoint sweep terminal; do not promote — 2026-09-11

Attempt `20260910T150000Z`, approved under proposal
`7c54481ab57c5538c0d779f6dbb9a51aeb78183684e38185e26aee400bb9867d`,
completed five earlier-checkpoint canaries. The pass curve is `5, 5, 3, 6, 5`
for token checkpoints 78,487, 156,090, 239,231, 312,423, and 389,093. The
previously measured final at 466,614 tokens is 6/30; upstream is 5/30. No point
passes net +2 plus zero lane regression. Earlier stopping is rejected and all
v3 checkpoints remain `do-not-promote`. Full development, further training,
merge, quantization, publication, and public claims remain blocked.

Sweep report SHA-256 is
`55fb67ff6b1a438c0f14c617ede45f3ffdf0ac5a32694cac4afd5b73bc32742f`;
campaign result is
`15041b9000812305fab0573cd72b16385bf2aa67efbb67226125f2b84bc20ddc`.
The campaign completed with exit code 0, but shell finalization hung. Approved
rescue proposal
`896b6115b51876a32abea65141b0a2872f05f5930f4b693684b85be938f501aa`
used a temporary IAP-only SSH rule to recover the stable terminal directory.
The rescue has 332 GCS objects/4,050,250 bytes; all 331 inventoried files
hash-verified and local semantic replay matched exactly. Record, do not repair,
the sealed phase-ledger `status: running` bookkeeping anomaly.

The temporary firewall, VM, disk, subnet, and network are absent twice. Ganesh
compute billing is closed. The unrelated detached disk
`laxmi-wmv2-training-01` remains outside scope, so project-wide GCS-only is
false. Result summary seal:
`1b8968595287d979e62cd2e0d29008c12a5559c62ccdfb61d4d44c46c2297bf0`.
The local trajectory audit is complete at seal
`15629f7407727fb9477eb6da892d709f174589575225e807ca14ec88f64ce9cc`:
21/30 tasks always fail, one always passes, and eight oscillate; five changing
tasks are `collapse-runs`. Next prepare a bounded LoRA-gradient conflict audit
and conditional gradient-surgery probe. Its local design is sealed at
`4e04c8029e42605d7c5aba913e97644a952e2c28bfc1140d278c7c76a936d73d`;
implementation and local validation are next. No GCloud action is currently
authorized. Any future controller must also replace the observed unbounded
process-substitution log drain without changing the historical uploaded source.
Detailed record: `LANE_STRATIFIED_CHECKPOINT_SWEEP_RESULT_20260911.md`.

The first implementation slice is complete locally: deterministic selection
of groups 0/9/18/27/36/45/54/63, all-pairs gradient cosine measurement,
fail-closed conflict adjudication, deterministic lane-order rotation, and
weighted PCGrad projection are implemented in `scripts/train/gradient_conflict.py`.
Eight unit tests cover projection, sparse parameter layouts, selection,
rotation, and the two-part conflict threshold. Runtime integration, CUDA shape
qualification, workspace packaging, and any GCloud proposal remain pending.

The v4 configuration and local execution card are now frozen without provider
authority. Config file SHA-256 is
`4b7d335d31ea5b5a4b940b9b240f708a9680e17d81dfa8222d7115f8f62610be`;
local card seal is
`087e3c4b7000957e022dadb12efa5f2fe9879a11b14208b67c5811e4d8086423`.
The runtime primitives validate the real dataset as 64 complete groups and can
collect response-token-mean lane gradients while taking zero optimizer steps.
The production SFT engine now admits the v4 card, writes a sealed eight-group
audit before any optimizer step, stops with `gradient-audit-stop` when the
frozen threshold fails, and otherwise applies deterministic PCGrad at every
complete optimizer-group boundary. Resume requires the exact audit identity
and seal; PCGrad telemetry records lane losses, pre/post cosines, projection
order/count, and aggregate norm. Thirty-five focused config/card/runtime tests
pass. The host campaign now treats a failed conflict threshold as a successful
terminal diagnostic with zero optimizer steps and no candidate evaluation;
when the threshold passes it requires the sealed audit again during terminal
verification and keeps the v4 canary unable to authorize full development.
The startup logger now closes and waits for both named FIFO tee processes
before inventory and backup, removing the prior unbounded process-substitution
drain. The 56-file training workspace reproduced byte-identically at
6,255,789 bytes with archive SHA-256
`c014652032e2bcc557891776f5abcab6c1265f238330fdbd8c8cd8e50dceb23d`
and manifest seal
`8c39aabd8b13b0282e1837581cd163cbb851c9bf3f6b3043f686f73be59c86bf`.
The paired 587-file development workspace, containing the v4-aware host
campaign and terminal verifier, reproduced byte-identically at 1,013,124 bytes
with archive SHA-256
`4d46b67a42e1868fea45123ad761492bc68426fbffb55b17c79f7731bd8bf8a2`
and repository-path manifest seal
`e39cce631f57762588ed98d7a6bfa68427b828ab83ea891e0a4188ac75d143a3`.
Ninety-five focused training/campaign tests pass and three CUDA-only tests
skip locally. CUDA shape qualification and a sealed upload/inspection/execution
chain remain. No upload or GCloud execution is authorized.

The next hard boundary is now sealed as a five-object, create-only GCS upload
plan totaling 7,424,438 bytes. It contains only the v4 training workspace and
manifest, development-v8 workspace and manifest, and corrected startup
controller; exact-generation download and byte comparison are mandatory. Plan
seal is
`b24b0b0db1ec876782ec4031a9dd1426f0903e4b0d94f93c284b022bc0b8d58c`.
It grants no Compute/network inspection, provider binding, training, or
evaluation authority. Navneet approved the exact plan. All five objects were
uploaded create-only, assigned immutable generations, downloaded by exact
generation, and matched local size, SHA-256, and bytes. Receipt seal is
`4ab0ab64e896efcb4000abc1125f59eced2534a93cce6d8eeca3fb5a6ecfa88b`;
uploaded bytes are exactly 7,424,438. No Compute or infrastructure action
occurred.

The separate read-only prerequisite plan is sealed at
`b35f9ff928066701a3aa94c2e54eb5e81c1050f984393a0819d9e56479fce4b4`.
It binds the five new immutable generations and five previously verified
runtime/model/verifier generations, permits only metadata, absence, IAM,
quota/availability, and current-price inspection, and grants no mutation or
execution authority. Navneet approved the exact plan. Execution stopped before
the first provider read because the selected `admin@executespec.ai` account
requires interactive `gcloud auth login`; token refresh cannot prompt in the
non-interactive inspection process. No cloud mutation occurred. The same
approved plan may resume after authentication without a new approval.

## Gate 4 six-lane-stratified probe terminal; do not promote — 2026-09-10

Proposal `8184f4694efdfab2da3b895393caec4c753d6b782f8c810067824f5d957926fa`
was approved at a `$2.25` ceiling. Attempt `20260910T043000Z` completed the
640-row/466,614-token probe, all 64 optimizer steps, save/reload, runtime
identity checks, and the 60-row disjoint retention guard. Every lane's
retention loss improved; five-family record-mean loss fell 13.36%.

The frozen canary completed 30/30 and scored 6 passes versus upstream 5. Java
gained one and Rust gained one; TypeScript lost one; Go, JavaScript, and Python
were unchanged. Net +1 missed the required +2 and the TypeScript loss violated
zero lane regression. Decision: `do-not-promote`. Do not run the 180-task
surface, main training, merge, quantization, or publication for this adapter.

All 129 terminal entries independently hash-verified. Terminal manifest
SHA-256 is
`b437b8aece9ae8afef8bc0703efd02e9ef6d3802bc426bc3815af1d61f231551`;
final adapter SHA-256 is
`8bf926578f0e6efe31152fba3f74756b4e93203cf69c57182a9accd5628d60c8`.
Control/recovery generations are `1789016588012192` and
`1789016586942988`; teardown receipt generation is `1789016873044612`.
Projected compute cost was `$0.2733293`.

The VM, disk, subnet, and network are absent twice. Only the unrelated
`laxmi-wmv2-training-01` disk remains in project Compute inventory; do not
touch it. Ganesh billing is GCS-only, project-wide GCS-only is false. The local
three-way transition audit is complete: v3 traded one v2 Go pass for one
TypeScript pass with no total gain, while three `collapse-runs` gains and two
boundary-condition losses persisted. Audit seal:
`074bd2853eb8ed9643fb3311976b5ac773a765766fa98963807b7d57969905b4`.
Do not scale or rebalance this recipe again. Full result:
`LANE_STRATIFIED_PROBE_RESULT_20260910.md`; audit:
`LANE_STRATIFIED_PROBE_TRANSITION_AUDIT_20260910.md`.

Local continuation planning has sealed a diagnostic-only sweep of the five
earlier v3 checkpoints on the same frozen 30-task development screen. The
config manifest seal is
`4c5c8b31d7dbeea1de913c3869fc901d8095036d2251700bf606aa9e5b495f37`;
it binds training evidence
`1393f0fab569e46d71d64273afeac69a91841f9f3c26f39d6248644b73dc4087`
and has no promotion authority. Focused tests pass 14/14. This is local
scaffolding only: no workspace/recovery upload, GCloud inspection, or compute
is authorized yet. The verified v3 terminal has now also been packaged into a
deterministic 528,065,805-byte recovery archive. Archive SHA-256 is
`260857a3057d1b5943eb540921478345d3c2b2aba6571bb6c51dc5d706d26172`;
package-manifest seal is
`37b9752dadb15d15dcdd6e290c624d4441d9e3467b42b5112b2b8fdfe7b5a865`.
All 130 source files were reverified against the terminal inventory before
packaging, and a second build reproduced byte-identically. The candidate-
specific workspace and startup controller also reproduce byte-identically;
workspace archive SHA-256 is
`56e2fda042b6c3fb0e9584151aa54cee1b7f9dad1bbe19037bf7e0a2f6872531`
and controller SHA-256 is
`32ea79030c0917a0506bb6fe7a3a46f1226cd032f73fd770be21a0cf0b03c87e`.
An extraction rehearsal passed complete workspace, training, six-checkpoint,
and final-canary identity admission. Focused tests pass 29/29.

The exact six-object, 529,256,224-byte upload-only plan is sealed at
`8f5eede2e94cddafda84636ab10d81bb2d4d8373289ee1b8bbc3fdde833cbda8`.
It permits only create-only GCS uploads, generation capture, exact-generation
downloads, and byte comparison. It prohibits all Compute/network inspection
or mutation and all training/evaluation/promotion actions. Navneet approved
the exact plan. All six objects were uploaded create-only, assigned immutable
generations, downloaded by exact generation, and matched local size, SHA-256,
and bytes. Receipt seal is
`6da07f1fcfa4296828e2a8cf406873d1f347d9436fa852f389c09fad087170b1`;
uploaded bytes are exactly 529,256,224. No Compute or infrastructure action
occurred. The separate read-only inspection plan is sealed at
`a0d283e3b82ac591937905160058f5512e2a8f5766c2b56cd2c508ac13de77bd`.
It binds the upload receipt, all six new immutable objects, six reused runtime
objects, and four exact planned resource names. It permits only provider,
quota, IAM, price, resource-absence, and object-metadata reads. Compute and all
cloud mutation remain unauthorized until Navneet explicitly approves this
exact read-only plan. Navneet approved it, and every prerequisite passed: zone
`UP`; `g2-standard-8` and `nvidia-l4` exposed; L4 quota 16 with usage 0; VM
service account has bucket objectAdmin; all four exact planned resources are
absent; and all twelve immutable inputs match exact-generation metadata. No
mutation occurred. Inspection report seal is
`fd7e557ac4bb7e17c4c46d3138eaf544087beea5e9be5fe36dd0896c5f23e69a`.

The exact Standard two-hour diagnostic execution proposal is sealed at
`7c54481ab57c5538c0d779f6dbb9a51aeb78183684e38185e26aee400bb9867d`.
Provider upper bound is `$1.762043024`; absolute incremental ceiling is
`$2.25`. It allows only serial evaluation of the five earlier v3 checkpoints
on the frozen 30-task screen, complete GCS preservation, teardown, and double
absence verification. It grants no training, checkpoint-selection, full-
development, promotion, or publication authority. Do not create resources or
execute until Navneet explicitly approves this exact proposal and ceiling.

## Pre-execution lane-stratified record (superseded) — 2026-09-10

The next mechanism is sealed locally but is not cloud-executable. It uses 640
unique rows/466,614 tokens in 64 accumulation groups of 10. Every group has
Go2, Java2, JavaScript1, TypeScript1, Python2, Rust2 and exact
20/20/10/10/20/20 objective mass. This fixes the v2 mismatch where TypeScript
received 7.17% while the gate protected it independently. Adapter capacity and
learning rate remain v2-equivalent.

A 60-row authorized training-corpus retention slice (10/lane) is disjoint from
training. It blocks continuation if any lane loss rises over 5% or the
five-family macro loss rises. The frozen executable canary still requires two
improved families, net +2, and zero lane regression. Full development remains
forbidden.

Dataset manifest seal:
`4258e58a4f1d6a46124e413512d7ba436d47eb780582410ecd96cd9a8d0b7404`.
Local card seal:
`2ff26cb52a1c630e324891717aae6e8d4ec61615a7d7cf681cbe6704ef0da82d`.
Training/evaluation workspace archive SHA-256 values:
`5bfb4616b467690e298fc41c15657ff55cc48631a498860ecd395717af477e15`
and `9e74b86085033c2ab008242cf505c6837c5a9e9b6ac4260b2d93cea395c75346`.
Both reproduced byte-identically and passed per-file verification. Focused
tests pass 39/39. Source commit is
`7711fa636cb4b08043518ec1bc97d76aadca889b`. The exact four-object,
7,399,962-byte GCloud upload-only plan
`9c92677248903be640ad6b4905cbba268126659540ac70ac2ee082e9da97fc61`
completed. All four assigned generations match local bytes; receipt seal is
`f3e127d0db29b4623fef251e76852ac1c3428fbb67d74ab79eaa1d4b00cf8e4f`.
No compute or infrastructure action occurred. Next is read-only provider and
input inspection under exact plan
`32804a7e859b7567910f62bc4b403fa3781a6d26b826a033775c7174d9526be4`.
It completed with all prerequisites passing; report seal is
`230e727c55c6323a1dbdeb8a0cacc7ce1ed0ae0ade65eb76d1c8d730b023e8b3`.
The exact Standard two-hour execution proposal is
`8184f4694efdfab2da3b895393caec4c753d6b782f8c810067824f5d957926fa`
with provider upper bound `$1.762043024` and absolute ceiling `$2.25`.
Do not bind cards, create resources, train, or evaluate until that exact seal
and ceiling are approved. Detailed contract:
`LANE_STRATIFIED_PROBE_PLAN_20260910.md`.

## Gate 4 capacity probe terminal; do not promote — 2026-09-10

Attempt `20260909T173721Z`, authorized by proposal
`461e968ae2fa79d3401e522d52bf91cbcc359cdded68d8fff62dff51631934f0`,
completed the bounded 624-row/468,601-token rank-16 probe and all six
checkpoints. Training and save/reload passed. The frozen 30-task canary finished
6/30 versus base 5/30: Go +1, Java +1, Rust +1, TypeScript -2, other lanes
unchanged. Continuation fails on net +1 (< +2) and two lane regressions, so the
exact mechanism is terminal `do-not-promote`. Never run its 180-task surface,
main training, merge, quantization, or publication.

All 129 terminal files passed independent SHA-256 recovery. Control evidence
roundtrip generation is `1788981472815348`; teardown receipt generation is
`1788981697224407`. The named VM/disk/subnet/network were deleted and returned
absent twice. Project inventory has no instances or other Compute surfaces,
but unrelated disk `laxmi-wmv2-training-01` remains and may bill; do not touch
it. Project-wide GCS-only remains false. The local transition audit is
complete: four gains, three losses, with three gains concentrated on
`collapse-runs`; TypeScript had only 7.17% of the prefix objective despite
lane-level no-regression. Next seal a six-lane-stratified mechanism with a
non-evaluation retention check. Full result:
`CAPACITY_PROBE_RESULT_20260910.md`; audit:
`CAPACITY_PROBE_TRANSITION_AUDIT_20260910.md`.

## Gate4 response-only training package ready — 2026-09-09

The sealed3225-row Gate2 source corpus is now deterministically tokenized with
the exact pinned Qwen tokenizer and non-thinking chat template. Prepared train
has2,438,853 input tokens, all rows at or below2944, and exact weighted objective
shares Go20%, Java20%, JavaScript10%, TypeScript10%, Python20%, Rust20% without
row duplication. Prepared train SHA256 is
0e7111f51c8ec6e7dcf23ee96ea4873b03ae944ce51aaab4aed6782493133224;
the50-row preserved validation SHA256 is
6a9d3aa37b30bc2672517f6d63113011de5f8156aa1049e588fdc70a36b77f46;
manifest seal is fc7409c3e68e372e1b1c05b07e5c36db0e3923c84731fe70a0f7937cfd413c25.
Focused training-preparation tests pass6/6. Artifacts are under
artifacts/train/expansion-pilot-v1 and remain local pending authenticated GCS
backup. Next build the exact one-recipe Gate4 execution controller/card and
local archive rehearsal. No VM/cloud compute or billable resource is active.

## Gate2 corpus sealed; pilot throughput resolved — 2026-09-09

Navneet directed resolution of Gate2 corpus sufficiency and pilot throughput.
The terminal retained-plus-admitted corpus is3225 rows/2,438,853 Qwen input
tokens, 5.288x the completed seed pilot, with zero records above2944 tokens and
a2659-token maximum. Immutable source corpus
datasets/cache/expansion-v1/pilot-sealed-3225/train.jsonl is sealed at SHA256
4254b6f82323421edbbece17fe1a0eb43a622c697059921afbf34aca600b949d and
is sufficient for one bounded executable pilot. The former4000-row pilot-entry floor is
retired; quality, lineage, separation, five-family weighting, executable
promotion and release gates remain unchanged. The bound JSON and interpretation
are PILOT_SUFFICIENCY_AND_THROUGHPUT_20260909.json/.md.

The executed repaired L4 rate is295.541 input tokens/s. Including measured
phase overhead, corpus training projects2h26m expected/3h14m at75%; a
30-task canary projects5m and full180 evaluation29m. Recommend a six-hour hard
runtime ceiling with the final30m reserved for backup. This is planning evidence,
not GCloud authorization.

All R26 reviews and diagnostics are terminal. Static review held Java0123 and
Rust0635. Fresh execution additionally held Go0542 (test/reference name
collision) and TypeScript0366 (compile/load failure). The other21 R26 records
plus R24 Java0512/Python0159 passed final serial admission23/23, zero rejected,
raising actual admission to152. The bounded critic is consumed. Gate2 source-
corpus closure is complete. Next construct and locally verify the response-only,
five-family-weighted Gate4 training package. No teacher, verifier, admission or
cloud process is active.

## R26 correction terminal; three-way static review active — 2026-09-09

R26 completed all 25 planned bounded test corrections with no rerun and no
second critic: Go6, Java4, JavaScript2, Python6, Rust4 and TypeScript3.
`generation.json` is terminal and `candidates.jsonl` SHA256 is
51eaef24706eb6031cd6205ef81b20f4509e2c624b9ccbbaa8f94240611b457c.
Request SHA256 remains
1dc3ec0d046bc5beca47b72d2a5c3d37cd1e2cf86f39c275947b445622000677,
feedback SHA256 remains
dc8ecab5c4911bc85b92f90d1392af7db49750e1dc080fdeb9f8345367bb4dc7
and logical plan SHA256 remains
11dce4e35cb0afa717cc966b9540f541caf5f6258b967f260ade7131df0f0293.

Three explicitly authorized disjoint static reviews are ACTIVE: Go+Java (10),
JavaScript+TypeScript (5), and Python+Rust (10). Reviewers must verify immutable
bindings, corrected-test quality, source-only prompt scope, reference
plausibility and evaluation separation; they must not execute or admit
candidates. Main must integrate the reports before fresh pinned serial,
resource-limited, network-disabled diagnostics on unconditional positives.
The two prior R24 static positives, Java generation0512 and Python
generation0159, already have directionality PASS but remain unadmitted pending
quality/separation disposition. Actual admission remains129. No generator,
verifier or admission process is active; no GCloud compute or new VM is in use.
Preserve all evidence for the next batched commit and verified GCS backup.

## R26 bounded test correction launched — 2026-09-09

Main fully read and integrated all six R24 lane reviews plus the R25 Java
review. R24 has exactly two unconditional static positives: Java generation0512
and Python generation0159. Both completed fresh pinned serial diagnostics with
reference PASS, supplied known-bad behavioral FAIL and original-parent
behavioral FAIL. Directionality PASS does not itself admit them.

Of the remaining R24 artifacts, 25 have scoped-positive references and are
eligible for one bounded specification-only test correction: Go6, Java4,
JavaScript2, Python6, Rust4 and TypeScript3. Excluded from R26 are every
prompt-scope hold and every reference-defective artifact. Main generated and
validated recovery-requests-r26.json and recovery-feedback-r26.json. Request
SHA is 1dc3ec0d046bc5beca47b72d2a5c3d37cd1e2cf86f39c275947b445622000677;
feedback SHA is dc8ecab5c4911bc85b92f90d1392af7db49750e1dc080fdeb9f8345367bb4dc7;
logical plan SHA is 11dce4e35cb0afa717cc966b9540f541caf5f6258b967f260ade7131df0f0293.
The correction helper now supports deterministic plan-order output with up to
three disjoint lane calls; 29 focused tests pass and diff-check passes. R26
session68650 is ACTIVE with lane-workers3. It is the sole bounded test critic
for these R24 artifacts; never rerun or apply a second critic. No verifier or
admission may overlap its serial execution phase. Actual admission remains129,
Gate2/no corpus, training or release seal. No GCloud compute. Preserve all raw
R24/R25/R26 evidence for the next batched commit and verified GCS backup.

## R24/R25 generation terminal; review wave 2 active — 2026-09-09

R24 generation completed48 with candidate JSONL SHA
b4663ef50c102174ddf8cdd041f34c3e3f58e9e8dd8038420501f69913e32ae1;
generation status is generated-not-verified-not-admitted. R25 then completed
its one Java repair with candidate JSONL SHA
c700ab2211f45cb48e22eb331ab446a8ca6871e2e2260844d948619d73a2e2fd.
Neither version may be rerun or counted as admission.

Main fully read and integrated the completed R24 Go, Java and JavaScript static
reviews. Current unconditional positives: Java generation0512 only. Go0/7
positive (six test holds plus generation0327 reference+test hold); Java1/10
positive (nine holds); JavaScript0/9 positive (two generation test/reference
holds and seven repair prompt-scope holds). R25 Java repair0409 is a substantive
reference/test positive conditional on scope but is held because its generated
behavioral prose exceeds the approved source-only/neutral-diagnosis operation;
see RECOVERY_R25_JAVA_REVIEW_20260909.md. No failure is misreported as a
pipeline failure, and no held artifact is silently waived.

Three disjoint static reviews are ACTIVE: Python7, Rust6 and TypeScript9,
targeting RECOVERY_R24_PYTHON_REVIEW_20260909.md,
RECOVERY_R24_RUST_REVIEW_20260909.md and
RECOVERY_R24_TYPESCRIPT_REVIEW_20260909.md. Main must fully read and validate
their final reports before any disposition. No teacher or verifier/admission is
active. After integration, run pinned serial network-disabled diagnostics only
for unconditional static positives, then prepare one bounded correction version
for eligible test-only/reference holds if justified. Actual admission129,
Gate2/no training or release seal. No new GCloud compute. Preserve all raw R24/
R25 evidence for batched commit and verified GCS backup before cleanup.

## R24 accelerated recovery generation active — 2026-09-08

Hourly continuation checkpoint: first three R24 lanes emitted26 candidate
artifacts (Go7, Java10, JavaScript9). The generator remains ACTIVE under parent
PID70924 with exactly three teacher calls now working the remaining TypeScript9,
Python7 and Rust6 lanes; no terminal generation/failure marker yet. Three
explicitly authorized, disjoint static reviewers are ACTIVE on the completed
Go, Java and JavaScript lanes, targeting RECOVERY_R24_GO_REVIEW_20260908.md,
RECOVERY_R24_JAVA_REVIEW_20260908.md and
RECOVERY_R24_JAVASCRIPT_REVIEW_20260908.md. Drafts require main integration;
reviewers must not execute candidates. No verifier/admission is active.

Main completed the full read and binding validation of the three batch-3
selection reports. All 49 selected parents remain held, have intact recorded
rights, and are disjoint from the 153 unique parents reserved by r1-r23.
Frozen corpus SHA256 remains 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec;
hold-ledger SHA256 remains 9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee.

The per-lane hard cap required an immutable split. R24 contains 48 records:
Go7, Java10, JavaScript9, TypeScript9, Python7 and Rust6. Request SHA256 is
2e881ce718f8509655f0a894daddc305c869bc787deb6672a9b68d6e0d416451;
plan logical SHA256 is d2816d2eaf52f5c8427808ec807f04439218bb6a502eb95f4bcee5df970d71bc.
Teacher generation is ACTIVE in exec session48088 with lane-workers=3; the
version is reserved and must never be relaunched or reused. R25 contains only
Java repair0409, request SHA256
3dbb94a523d0cbf8cc4ac98cb7af6f015bd5b8360a651046f1f21c8d4c180eab,
plan logical SHA256 93c8e5340b15878b8f5f7bbc48713577527fd0a540f05571d0588ef0be0d805c.
R25 is planned but NOT generated; launch it only after R24 reaches a terminal
state so total active teacher calls never exceeds three.

The three selection reviewers are DONE; their reports are the immutable review
evidence bound in r24/r25. No verifier or admission may overlap candidate
execution; after generation, perform static quality review and then fresh
serial, resource-limited, network-disabled directionality checks. Failures are
review dispositions, not a run-level failure. Actual admission remains129;
Gate2/no training or release seal. No new VM and no GCloud compute. Preserve all
r24/r25 raw evidence for the next GCS backup before any teardown or cleanup.

## Post-backup next-selection dispatch — 2026-09-08

Admission129 archive and receipt verified as recorded below. Follow-up proof
commit eadd24d pushedSUCCESS. No teacher/verifier/admission active. Three
explicitly authorized disjoint reviewer assignments now ACTIVE for fresh held
original parents excluding every r1-r23 reserved parent: rust391_420 Go/Java up
to30 total, rust421_450 JS/TS up to30, rust451_480 Python/Rust up to30. Reports:
RECOVERY_NEXT_GO_JAVA_BATCH3_20260908.md,
RECOVERY_NEXT_JS_TS_BATCH3_20260908.md,
RECOVERY_NEXT_PYTHON_RUST_BATCH3_20260908.md. Drafts are not approved/countable;
main must full-read and validate exact bindings before requests/plans. Do not
duplicate selection. Actual129, minimum gap798, Gate2/no seal. No GCloud compute.

## Admission129 terminal local checkpoint — 2026-09-08

R23 generation17, three disjoint terminal reviews and serial diagnostics all
DONE: all17 static positives and all17 directionality PASS. One bounded critic
consumed; no repeat. R21/R22 prepared3 and admitted3; R23 prepared/admitted17,
zero rejected. Actual cumulative129=Go23/Java19/JS22/TS22/Python21/Rust22,
generation118/repair11. Maximum combined3202/minimum gap798. See
RECOVERY_ADMISSION129_20260908.md. Gate2, no corpus/training/release seal.

Main fully read/integrated R22 Go/Java reports. Only unconditional R22 positives
were Go0218/0180. R22 Java five repairs and Go0233 stay excluded for generated
prompt edits beyond approved source-only scope. Go0095 race directionality PASS
but test hold remains. No silent scope waiver or second critic.

No verifier/teacher/admission is active. Commit3267123 pushed. Verified GCS
archive now covers all R21/R22/R23 raw evidence plus admission129: generation
1788886177368453, bytes10934109, SHA
e79b3c46cda3afab00cada6fdc759fdcd145a99198c4b031ebf167b54d6244ed;
exact-generation download/cmp PASS. Receipt generation1788886264954026,
bytes1117, exact-generation download/cmp PASS. See
RECOVERY_ADMISSION129_BACKUP.md. Next continue new-parent recovery toward
minimum4000. No cleanup, VM use or billing certification. No GCloud compute
authorization inferred. Training50%/release35% remain milestone estimates;
idle until next bounded selection, next hourly check, overall ETA unproven until
corpus sufficiency and pilot throughput.

## R23 bounded correction launched — 2026-09-08

Main integrated complete R21 JS/Rust reports and verified all11 candidate raw
and canonical hashes. JS0090 sole quality positive; JS0097 source-domain hold
(new array rejection), excluded from test-only correction. Remaining17 test
holds comprise Python4/TS4/JS3/Rust6. Main read provisional requests/feedback,
validated corpus/ledger/parent/review/prior-candidate bindings, and finalized
recovery-requests-r23.json plus recovery-feedback-r23.json. Main added explicit
removal of JS0119 unknown-extra rejection and explicit Rust0064 malformed-Named
category caveat. Plan SHA
01c72e624891ad3d0e304c9bc2bb8a31eca614d430f6b7ecb43053e5868f3aeb.
R23 teacher73087 ACTIVE, one test-only critic per lane, prior R21 code immutable.
No second automatic correction allowed. R23 is reserved; never duplicate.

R22 Go8 diagnostics7005 DONE: positive0095/0218/0280/0180/0233;0027 all pass,
0121 all compile failures,0048 all behavioral failures. No admission inferred.
Additional Go0095 serial race qualification48951 now active, output r22-go0095-race.
No concurrent verifier/admission allowed. Reviewer rust391_420 R22 Java6 and
rust421_450 R22 Go8 full quality reports ACTIVE; drafts not main-integrated.
rust451_480 completed R23 draft and idle. Main must integrate reports before
combining eligible R22 with R21 JS0090 for admission.

Data pytest suite completed successfully (144 tests); git diff --check passed.
Admission109 unchanged; no training seal. All R21/R22/R23 later evidence remains
outside verified GCS109 backup. Next terminal batch must preserve it before any
cleanup. No VM usage or billing certification. Gate2; training50%/release35%
estimated milestones; active, next10–30min low confidence, overall ETA unproven.

## Post-interruption resume — 2026-09-08

R22 teacher4217 completed14 successfully, generation.json present. Do not rerun.
R21 TS/Rust/JS diagnostics46588 completed15: directionality positive only
JS0090 and Rust0111/0342; no admission without integrated quality review.
R22 Java diagnostics18566 completed6:0075/0401/0460/0464 directionality positive;
0026 all behavioral failures,0065 all pass. Main fully read0026 and0065 current
spec/ref/tests/mutant:0026 test wrongly labels valid 1,2,*,*,3,*,* invalid;
0065 misses the100/100/29/29 exact rational witness. These are test holds,
not evidence to alter references. Full Java review still pending.

One serial verifier7005 now active on R22 Go8, output directory
artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r22-go. No other
verifier/admission may run concurrently. Go0095 race qualification still pending.

All three reviewer attempts hit usage limit before completed reports/drafts.
On explicit user continue, resumed same disjoint assignments: rust391_420 R21
JS5 final report, rust421_450 R21 Rust6 final report, rust451_480 provisional
R23 Python4/TS4 request+feedback. No R23 reserved or generated. Check completion
before redispatch. JS preliminary finding0097 derived array rejection may be a
reference-domain regression; not main-integrated and not eligible test-only yet.
Main verified all8 Python/TS final report raw/canonical candidate bindings.

Actual admission109 unchanged; Gate2/no seal. No VM or cleanup. Evidence since
R21 remains outside the verified admission109 GCS backup. Next integrate final
reviews, batch bounded correction, review R22 and preserve terminal evidence.

## Authorized acceleration resumed — 2026-09-08

User reaffirmed authorization. R21 is terminal partial: 19 completed candidates
(Python4/Rust6/JS5/TS4), Go8/Java6 architecture guard failures preserved.
Main completed reading R22 failure analysis/request and approved the exact14
incomplete Go/Java parents, validating original corpus, ledger, parent and review
hashes. Eight repairs use oracle-rebuild solely to replace embedded broken source
and neutralize stale nonbehavioral diagnosis; five generation rows remain
reference-fix, Go0218 retains the approved idempotence clarification. No new
parents, guard relaxation, candidate renaming, VM use or admission claimed.

Approved request recovery-requests-r22.json; plan logical SHA
d3d5da006458fdaf86086c1297bcf2fc146887d9951f09e17eed8d3306faae35.
R22 teacher session4217 ACTIVE with two lane workers; version reserved and
run-contract persisted. Check process/output before any relaunch; never reuse.
One serial diagnostic session46588 ACTIVE for R21 TS4/Rust6/JS5 in
artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js.
Do not run another verifier/admission concurrently.

Main fully read final R21 Python4 and TS4 reviews: all eight remain test-quality
holds, references scoped-positive. No critic reserved or invoked this checkpoint.
Rust6/JS5 full reviews still pending; no new reviewer assignment made this turn.
Next integrate those reviews, prepare one bounded test-only critic for eligible
R21 holds, and review fresh R22 outputs before diagnostics/admission.

Actual admission109 unchanged; maximum combined3182/minimum gap818, Gate2,
no final corpus or training seal. Latest verified GCS checkpoint remains109;
all R21 generation/diagnostics/reviews and R22 are NOT covered by that backup.
Preserve for the next terminal evidence backup. No cleanup or billing claim.

## Post-backup dispatch checkpoint — 2026-09-08

Commitdb60b59 pushedSUCCESS (session78616 exit0). Admission109 GCS archive AND
receipt exact-generationcomparisonsPASS. Count109 unchanged, Gate2/no seal.
R21 TypeScript4 nowemitted; reviewer rust391_420 assigned fullqualityreview
->RECOVERY_R21_TS_REVIEW_20260908.md. Don'tduplicate. Otherreviewersidle after
completed R21Python4 report and combined R22Go8/Java6 failure/retrydraft;
both stillmain-unread/unapproved. R21Rust6/JS5 notyetemitted atlastcheck.
Teacher7233 remainsactive; no verifier/admissionactive. Next mainintegrate
reports/drafts, checkslots beforeR22launch, serialR21TSdiagnostics, thenremaining
lanes. AllR21current/lateroutputs excluded fromverifiedadmission109backup.

## Exact admission109 resume — 2026-09-08

Admission37020 DONE16/0rejected; cumulative109=Go21/Java19/JS18/TS18/Python17/
Rust16, generation99/repair10. Max combined3182/minremaining818. Main verified
all prior admission report/output seals. No final corpus/training/release seal.
See RECOVERY_ADMISSION109_20260908.md. Alloriginalholds2812 unchanged.

R20 diagnostics72388 DONE: Python positive/admitted; Rust correctedreference
PASS/suppliedmutant behavioralFAIL/originalparent COMPILE failure, excluded.
Don't repair the original, conflate outcomes, or weaken admission control.

R21 teacher7233 ACTIVE. Java6 andGo8 architecture lanes failed exact embedded
broken-source guard; no candidate files for those lanes. Otherlanes continue.
Root cause is main-approved request classification conflict: reference-fix freezes
old repair prompt while rationale requires a new mutant embedded in that prompt.
Preserve r21 raw andfailure JSON; don't blame only teacher or weakenexactguard.
Reviewer rust421_450 is drafting combined fresh R22 Go8/Java6 retry request and
RECOVERY_R21_JAVA_FAILURE_20260908.md. For eight repairrows only, oracle-rebuild
permits exact broken-code replacement while allbehavioralprose stays unchanged;
generationrows preserve reference-fix/approved clarification. Main has NOT read
or approved this draft; no r22 reserved. Wait availableteacher slots beforelaunch.

R21 Python4 emitted and serial diagnostics61671 DONE:0063/0156/0781 allthree
programsPASS (missingwitnesses);0017directionalityPASS but preliminary timer-
dependent test hold. Reviewer rust451_480 writing RECOVERY_R21_PYTHON_REVIEW;
mainhasNOTreadfinal yet. Preliminary holdsall4:valuelessrel missing,falseylogger
missing/privatefieldoracle,sharedbaserow missing,timer-dependentgather witness.
Do not admit from preliminary review. rust391_420 idle after integratedR20.
R21 Rust6/JS5/TS4 notyetemitted atlastcheck; dispatch disjointreviewswhenfilesexist.
No verifier/admission nowactive. No additionalnew-parentselectionneeded.

Admission109 archive AND receipt exact-generationdownload/cmpPASS; receipt
generation1788873297960611. See RECOVERY_ADMISSION109_BACKUP.md.
Archivegen1788873211725614 bytes10827870 SHA
c95e152e14337f7d7ef66421f897754995a19f735f0d6c2f31ecf725051d2355.
Includes all109 admissions, terminalr15-r20teacher/diagnostics/reviews andr21
planonly. Excludes activer21outputs/diagnostics/reviews andr22drafts. Preserve
these fornextbackup. No cleanup/VM/billingcertification.144datatestsPASS.

R22 combined14 draft and R21 Python4 finalreview nowcomplete, bothmain-unread.
Next: batchcommit/push; integrateR21remainingreviews,
freshserialdiagnostics, validate/launchR22 afterslotcheck, boundedR21 test-only
correction when justified. Working, notpermissionblocked. Training50%/release35%
estimatedmilestones; next10–30minlowconfidence; overallETAunproven.

## Admission93 and R21 generation — 2026-09-08

Queue78047 DONE:25 admitted/0rejected -> R17 thirteen diagnostics PASS,
R18 two PASS, R19 Python PASS but still prior test-scope hold; R19 Rust reference
PASS/supplied mutant behavioral FAIL/original-parent COMPILE failure. Never
count compile failure as semantic evidence or weaken that control.
Main fully read/validated all R17/R19/R20 reviews. R20 two static positives;
R20 Rust original-parent trait failure must remain excluded from current
admission path. Fresh R20 two diagnostics now running (session recorded next).

Actual93=Go21/Java19/JS11/TS12/Python15/Rust15; generation85/repair8;
max combined3166/min remaining834. See RECOVERY_ADMISSION93_20260908.md.
Standalone prepared r15-sixteen-v1 is superseded by admitted combined25;
NEVER admit that old16 separately. LatestverifiedGCScheckpoint68 excludes25.

R20 teacher59634 DONE2. R21 teacher7233 active33 with3laneworkers, allnew
parents: Go8/Java6/Python4/Rust6/JS5/TS4, generation25/repair8. Main fully read
allthree batch2reports, validated35proposals and selected33. Rust0133 compile-
only andJavarepair0270 oracle-only deferred. Three narrowclarifications approved
in RECOVERY_R21_SELECTION_20260908.md. PlanSHA
a395242261d87d3bdf5189dcf02e06d7e501043dfac6d9c36cb9c5a2780fe9bc.
Unique reserved parents153. Reviewers idle afterall completed selections;
dispatch disjoint R21 reviews only aftercandidatefiles exist. No newparenttask.

Next: finish R20 diagnostics, prepare/admit R17 thirteen+R18two+eligibleR20
Python (expected16, onlycountactual), then verified terminalGCSbackup ofalllater
evidence. R21active outputs excluded untilterminal. No otherverifier/admission
concurrent withR20. Gate2/holdsunchanged/notrainingseal/newVM. Training50%/
release35% estimates; working, next10–30minlowconfidence; overallETAunproven.

## Post-commit live queue — 2026-09-08

Commit1eb0655 pushed successfully; session87528 exited0.
R17 generation13 and R19 generation2 now have terminal generation.json files.
Sessions12703/80444 exited0; no teacher generation remains pending.
Main dispatched three disjoint quality reviews: rust391_420 R17 JS7,
rust451_480 R17 TS6, rust421_450 R19 Python/Rust2. Reports respectively
RECOVERY_R17_JS_REVIEW_20260908.md, RECOVERY_R17_TS_REVIEW_20260908.md,
RECOVERY_R19_REVIEW_20260908.md. Drafts not main-integrated; don't duplicate.
ONE serial diagnostic queue75000 continues R16 Go; keep other execution idle.
R15 sixteen preparation81112 DONE zero overlaps; admission not launched.
R18 two review main-integrated/positive, diagnostics pending. Count68 unchanged.
After75000, run pending admission and R17/R18/R19 diagnostics serially, integrate
reviews, then batch next backup. New terminal teacher outputs17/18/19 NOT in
verified admission68 archive. No cleanup or final corpus/training seal.

## Exact accelerated resume — 2026-09-08, 12:45 UTC checkpoint

Actual admissions remain68, max combined3141, minimum gap859 before exclusions
and token balance. Training50%/release35% are milestone estimates, not metrics.
Original quality review closed; all original holds immutable; Gate2, no seal.

R15 teacher41307 DONE19; R16 teacher98811 DONE10; R18 teacher11969 DONE2.
Main fully read/validated all R15 Java/Python/Rust and R16 Go quality reports:
R15 static positives16, terminal oracle holds Java0334/Python0741/Rust0449;
R16 static positives9, terminal oracle hold Go0084. These completed one-critic
holds do NOT authorize another automatic critic. No original coverage credit.
All R15 diagnostics DONE57 runs, all directionality pass; oracle holds still
excluded. Main saved selection recovery-admission-r15-sixteen.json and started
non-executing preparation81112 into recovery-admission/r15-sixteen-v1.
Preparation81112 DONE16, zero overlap; compared3073 originals plus68 prior
recoveries. Admission itself NOT launched, count remains68.

ONE serial diagnostic queue75000 is now on R16 Go10 (after terminal R15).
Do not start any other verifier/admission until it exits. Main integrated R16
report and checked all10 file/canonical bindings. After completion combine
eligible R16 nine with pending R15 sixteen if practical, or admit saved16 then9
serially. Use report filename admission.json for compatibility with prior loader.
The earlier two-row run used admission-report.json; added byte-identical
admission.json alias, cmp PASS, preserving original report and logical seal.
Initial R15 preparation failed before writing its output directory due to that
filename mismatch; rerun81112 only after alias repair. No candidate re-execution
or metric reconstruction was performed for this naming repair.

R17 teacher12703 active13 (JS7/TS6), one lane at a time. R18 two main-read
static positives and file hashes verified; still needs fresh serial diagnostics.
R19 fresh architecture80444 active2 with two lane workers. Main fully read
R19 provisional note/request, validated original corpus/holds/evidence bindings,
approved exactly Python0717 invalid-kind/Mapping repair and Rust0487 required
store traits plus query-arity fallback. Plan SHA
ef6c38e0eadab9fa90f94dcfcec012c01160c8b9d1c5ff1adfc33b3b94b087e2.
R17 plan SHA6317915062299e23afd07e2e709b0c310c60039681b2c917b336ead0363a0506;
R18 plan SHA45fa983fd232df4cad2924d0335971eade69ac2b92d697374be3922971486d73.
All versions reserved; never duplicate. Total teacher calls at most3.
Reviewers completed assignments and are idle; dispatch disjoint R17/R19 reviews
only when candidate files exist. R18 review already main-integrated, no duplicate.

Latest verified GCS checkpoint now admission68. Archive and receipt exact-
generation download/cmp PASS, see RECOVERY_ADMISSION68_BACKUP.md. Covers all68
admissions, terminal r12-r16 teacher outputs and r11-r14 diagnostics. Excludes
r15/r16 diagnostics/new quality reports, r17/r18/r19 outputs and later edits
(including new admission.json alias). Preserve those for next terminal backup.
144 data tests passed. No cleanup/VM use/billing certification claim.

Next: finish75000, admit eligible positives, serial R18/R17 diagnostics with
quality integration, inspect R19 output, then batch terminal evidence backup.
Working, not permission-blocked; next10–30min low confidence. Overall release
ETA still ungrounded. New GCloud compute requires scoped approval/cost ceiling.

## Current authorization continuation — 2026-09-08

User confirmed authorization. No new VM or uncapped GCloud compute inferred.
Gate 2 remains active; original holds unchanged and no training/release seal.

Diagnostic queue 7997 DONE: all r12 JS/TS14, r13 Rust0361 and r14 two.
Only r12 TS0267 and r13 Rust0361 have both main-integrated static quality
approval and passing behavioral directionality. r12 JS0391 and r14 Python0138
remain oracle-held despite directionality passing. Never count those as admitted.

Serial preparation/admission queue 89883 DONE: two accepted, zero rejected.
Selection: recovery-admission-r12-r13-two.json; output: recovery-admission/
r12-r13-two-v1, report admission-report.json. Terminal report confirms 68 total
recoveries. This queue is now terminal; no verifier remains active.

Teacher r15 session 41307 remains active (19 one-test corrections, one lane at
a time). Main fully read and validated r16 Go10 provisional review/request/
feedback, original parent and prior canonical hashes, and evidence bindings.
Final r16 request/feedback preserve the provisional files and approve exactly
one test-only correction, with unchanged specification/reference/mutant bytes.
R16 launched session 98811; plan SHA
14fa2d6c97639d3c36ff599309d367515fd7e7eb2ccf257dcd06c9c219a32801.
Maximum two teacher calls currently; version r16 reserved, never duplicate it.

R17 JS7/TS6 and r18 Python/Rust2 provisional drafts are complete but NOT yet
main-read/approved/reserved. Read and validate before launching; total teacher
calls must stay at most three. r13/r14 generation and all r12 diagnostics done.
Latest verified GCS backup still admission50, excluding latest16 admissions
and later terminal evidence. Preserve all data; next batch backup must cover it.

Current actual recoveries68 (Go12/Java14/JS11/TS12/Python10/Rust9),
generation60/repair8; maximum combined3141; minimum gap859 before
further exclusions/token balance. Estimated milestones training50%/release35%,
not measured completion percentages. Working, not approval-blocked. Next batch
ETA10–30minutes low confidence; full release ETA still not defensible.

## Exact live resume: admission66 and allr12 generated — 2026-09-08

Queue36333 admitted6/0rejected, thenautomaticallyenteredr12Go10diagnostics.
Currentactual66=Go12/Java14/JS11/TS11/Python10/Rust8,generation59/repair7;
maxcombined3139,minremaining861. See RECOVERY_R12_ADMISSION66_20260908.md.
ONEserialverifier36333 outputrecovery-diagnostics/r12-go; nootherexecution.
R12first27 completed81executions; sixadmitted,19test-onlyholds+2referenceholds.
LatestverifiedGCScheckpoint50 excludes latest16admissions andalllater evidence.

R12generation57681 DONE51. R13onecritic84508 active; r14twoarchitecture76396
activewith2laneworkers, totalteachermax3. Bothversionregistriesnowreserved,
don'tduplicate/reuse. Inspectoutputsbeforedispatchingcandidate reviews.

Reviewers: rust421_450r12Go10active; rust391_420r12JS7/TS7(14)active;
rust451_480finishedPROVISIONALr15request/feedback19(Java6/Py6/Rust7), idle.
Main hasNOTreadr15draft yet; validatebeforeplan/launch. No r15versionreserved.
Main HASfullyread/integratedr12Java/Python/Rust reports,verifiedfile/prompt/ref
bindings. R12Gopreliminaryoraclegapsnotfinal/mainread; don'tcountdrafts.

Next: finishGoqueue, integrateremainingreviews, seriallyverifyJS/TS14;reviewr13/
r14outputs, mainread/validateandlaunchr15whenboundedteachercapacityfree. Separate
future reference correctionsPy0717/Rust0487 stillneeddisposition. Batchnextbackup
mustinclude latest16admissions/r11diagnostics/r12terminal/r13-r15laterstates.
Commit a1d4d5e pushedsuccessfully; subsequentnotes/artifactsuncommittedfornextbatch.
Originalreviewclosed/holdsunchanged/nocorpusseal/training. Currentworkapproved,
noVM. Estimatestraining50%/release35%; working, next10–30minlowconfidence,
fulldeliveryETAunproven. Continueactualwork, notstatus-only.

## Latest post-commit execution queue — 2026-09-08

Commit a1d4d5e push SUCCESS. Actual cumulative60 remains until newadmission exits.
R12first27 diagnostics30205 DONE all81 programruns. Main fullyread allthree
Java/Python/Rust reports and validated every27 candidatefile/prompt/reference
hash. Six static+directionalitypositives: Java0514/0794,Py0070/0400,Rust0092/0509.
Nineteen test-only holds; Py0717 referenceerrorclass andRust0487 missingrequired
publictraits are referenceholds, never admit from current passing tests alone.

ONE newserialqueue36333: prepare/admit above6 ->r12Go10diagnostics, outputdirs
recovery-admission/r12-six-v1 and recovery-diagnostics/r12-go. Do not launch a
parallel verifier/admission. R12first27diagnostics andalllateradmissions are NOT
covered by verifiedadmission50backup. Count only terminaladmissionreport.

R12generation57681 stillactive:37 emitted(Java8/Py9/Rust10/Go10), JS7/TS7pending.
Go lanecomplete leaves only2teacherlanes; main used free capacity for approved
r13one-testcorrection session84508 (prior-run r11, exactfinalfeedback), nowreserved.
Max3totalteacher calls respected. R14approved2architecture stillNOT launched;
wait until at least2slotsavailable orr12complete, no duplicate/version reuse.

Current reviewers: rust421_450 reviewingr12Go10 ->RECOVERY_R12_GO_REVIEW_20260908.md;
rust451_480 draftingPROVISIONALr15testcorrection19(Java6/Py6/Rust7), excludesPy0717
andRust0487. Main mustfullyread/validate beforeplan/launch. rust391_420idle after
integratedRust10; canreviewJS/TSwhenemitted. No currentnew-parentselectiontask.
R12Go/JS/TS reviews/diagnostics notyetcomplete. Main acceptedfirst27 staticreports
only; dynamicqualifications retainall compile/timeout/oracle failures separately.

Next: inspectqueue36333admissionresult, finishr12generation/reviews, preserve
r13output andreview/verifyserially, launchr14whenboundedslotsfree; integrate
r15draft thenonecritic, separatelydispositionPy0717/Rust0487. Batchnextcommit/
GCSbackupafterterminalboundary. No corpusseal/training/release. Estimates50%/35%,
actualgeneration/correction/verification/reviewworking; next10–30minlowconfidence,
fulldeliveryETAungrounded. Currentworkapproved; newcloudcomputeneedsscope/budget.

## Admission60; serial r12-first27 now running — 2026-09-08

Queue80706 exited0:10accepted/0rejected. Cumulative60=Go12/Java12/JS11/TS11/
Python8/Rust6, generation53/repair7. Max combined3133,minimumremaining867.
See RECOVERY_R11_ADMISSION60_20260908.md. LatestverifiedGCScheckpoint50 does
NOT cover these10 or r11diagnostics; include them in nextterminalbackup.

ONE new serialdiagnostic queue30205: r12Java8 ->Python9 ->Rust10, outputdir
recovery-diagnostics/r12-first27. R12teacher57681 continues remainingGo/JS/TS.
Reviewerassignments unchanged: rust451_480Java8,rust421_450Python9,rust391_420Rust10.
Drafts notyetmainread/integrated. Don'trunadmissionorGo/race concurrently.
R13onecritic andr14twoarchitectureplansapprovedbutnotlaunched; keepteachermax3.
R12Go/JS/TScandidatereviews stillneeddispatchafterfilesexist/slotsfree.

Batchcommit includes terminaldiagnostics throughr11, admissions60 andplansr10-r14;
noactive r12diagnostic artifacts orunfinishedreviews. Trailingblanklines in
hash-bound review/request evidence are preserved intentionally; don't reformat.
All144datatests pass. Originalreviewclosed/holdsunchanged/no trainingseal.

## Post-backup exact queue checkpoint — 2026-09-08

Cumulative50 unchanged at this checkpoint. Terminal admission50 archive AND
receipt exact-generation download/cmp PASS; see RECOVERY_ADMISSION50_BACKUP.md.
Covers terminalr6-r10 plus r11generation/reviews, not r11diagnostics/r12generation
or later r13/r14 plans. No cleanup/VM/billing certification.144data tests pass.

R11 diagnostics session12474 DONE:10 directionality positives, Rust0361
referencepass/bothcontrolstimeout, Rust0102 referencecompilefailure with both
controlsbehavioralfail. Fullthreequalityreportsmainintegrated. ONE active
prep/admission queue80706 for10 positives, output recovery-admission/r11-ten-v1,
selection recovery-admission-r11-ten.json. Prepared against3073 originals+50
priorrecoveries withzerooverlap; notyetadmitted. Do not parallelize execution.

R12 generation57681 stillactive with3teacherlane workers. Java8/Python9/Rust10
candidatefiles nowexist; assigned reviewers rust451_480Java8,
rust421_450Python9,rust391_420Rust10. Isolated RECOVERY_R12_*_REVIEW_20260908.md
outputs; drafts notmainintegrated yet. OtherGo/JS/TSlanes stillgenerationpending.
Do not duplicate these assignments or launch anynewselection campaign.

Main fullyread/validated/approved finalr13 request/feedback: one test-only
Rust0361 correction, prior-run r11, plan SHA
6659bda4b3701570d6f60becde828d288df12744712859ae4c4179e5b0c6e903.
Main fullyread/validated/approved r14two fresharchitecture retries Py0138/Rust0102,
plan SHA d940f00a1c6b1669cec71865040489c9cd3890bf3a6bdb43490df3bf807d153b.
Neither generationregistryreserved/launched; wait untilr12complete or explicitly
verified availableteacher slots. No automatic repeatedcritic. See R13/R14_SELECTION
notes for exactscope; provisionalartifacts preserved. No originalholds changed.

Next: finishr11admission, serialr12diagnostics ofemittedlanes whileintegrating
reviews, launchapprovedr13/r14 withboundedteacher capacity, terminalbackupoflater
evidence. Training/release estimates50%/35%; actualgeneration/admission/review
working; next10–30minlowconfidence, overallETAnotdefensible. No currentapproval
blocker. NewGCloudcompute stillrequires scope/costceiling.

## Exact resume: admission50, r11 diagnostics and r12 generation — 2026-09-08

Admission queue13583 exited0:25 accepted/0 rejected, cumulative50 (Go11,Java12,
JS9,TS7,Python8,Rust3), allgeneration. Max combined3123,min additional877 before
further exclusions/tokenbalance. See RECOVERY_ADMISSION50_20260908.md. No seal.

ONE serial verifier session12474 now runs all12 emitted r11 candidates, output
recovery-diagnostics/r11. All three r11 quality reports main-fully-read:10 static
positives (Go1/Rust3/JS2/TS4); Rust0102 predicate-signature reference hold and
Rust0361 missing bounded arithmetic witness (huge mutant loop likelytimeout).
Do not classify compile/timeout as semantic failure or start parallel execution.
R11 Python raw exact-ID failure remains preserved; no candidate to review.

R12 generation session57681 active,3 lane workers,51 new generation parents
(Go10/Java8/Python9/Rust10/JS7/TS7). Plan logical SHA
3edbe358f89bc7396eb1ae1c694acf685213164bda40030cf54c5c033467f78d.
Main fully read/validated all three next-selection reports and parent/test/source/
rights/evidence hashes;51 selected from53. TS0241/0242 deferred explicitly;
see RECOVERY_R12_SELECTION_20260908.md. All51 disjoint from prior69; current
unique reserved parents120. No duplicate launch/version reuse. Reviewersidle
after completed r11 reports; dispatch next disjoint candidate reviews only when
r12 files exist. No new selection task is needed until these51 are processed.

Next: terminal r6-r10/admission50 GCS checkpoint plus r11 generation/reviews;
exclude active r11 diagnostics and r12 generation from that snapshot, then save
their terminal evidence later. Latest verified backup still admission21 until
new exact-generation proof. No cleanup/VM/training. Continue r11 admission and
bounded correction decisions, then r12 review/verification. Estimates50%/35%,
working, next10–30minlowconfidence; full deliveryETAnotdefensible. No approval
needed for current work; newcloudcompute requires scoped budget.

## Exact resume: admission batch25 active — 2026-09-08

User confirmed acceleration authorization. No new cloud resources or uncapped
cloud budget inferred. Current gate2; no runtime/model/gate changes.
Serial diagnostic queue39155 exited0: r7 Go0439/0522 actual-race directionality
passed; r10 Java0641/0617/0687/0762 normal directionality passed. All selected
candidate file hashes were checked against their main-read quality reports.

ONE active preparation/admission queue session13583: r7 Go9 +r8 Java6 +r9
Python4/Rust2 +r10 Java4 (25 total). Selection is
cutoff-5885-review/recovery-admission-r7-r10-selected25.json; output directory
recovery-admission/r7-r10-selected25-v1. Race summary/reference file hashes for
Go0439/0522 additionally bound and candidate canonical hashes verified. Do not
start another verifier/admission until this queue exits. Actual admitted count
remains25, max combined3098, minimum gap902 until this admission completes.

R11 generation session44585 exited1, preserving partial completion:12 candidates
across Go1/Rust5/JS2/TS4; Python0138 failed strict returned-ID guard (original
parent ID returned instead of requested derived ID). Do not rename output,
overwrite r11, or count it as a complete generation. Completed candidates still
need independent quality review and serial diagnostics. Raw failure preserved.

Three next-selection reviewer reports completed: RECOVERY_NEXT_GO_JAVA_20
(18 proposals), RECOVERY_NEXT_PYTHON_RUST_20 (19), RECOVERY_NEXT_JS_TS_20 (16),
all suffixed _20260908.md. Main has NOT fully read/approved these53 proposals;
no new reservations. Reviewers idle. Existing69 unique parent exclusions apply.

Next: finish batch admission, integrate/review r11 and next-selection evidence,
then batch a verified GCS backup covering terminal r6-r11 and new admissions.
Latest verified GCS checkpoint remains admission21; no cleanup authorized by
an incomplete backup. Training/release estimates50%/35%, not measured fractions;
admission active, no training active. Next admission estimate10–20min low
confidence; full delivery ETA not yet defensible.

## Exact resume: admission25 and serial queue41369 — 2026-09-08

Latest after commit4090ef6 (push SUCCESS): queue41369 completed r9all6 directionality
positive, r8six directionalitypositive matching staticpositives;0641/0617 allthree
pass,0687/0762 allthree behavioralfail. Queue is now running r7Go9. Do not start
admission/race until queuefinishes. Those12 new qualified r9/r8 candidates are not
yetadmitted. r10provisional request/feedback drafts completed; main has NOT read
or approved them. All reviewersidle. Next main: read/validate r10 then launchone
bounded testcorrection while serialGo continues; batch12 admission afterGo/race.

Post-checkpoint main FULLY READ final r8Java report: sixstaticpositives0710/0642/
0647/0677/0785/0763, fourholds0641/0617/0687/0762 as described below. Reviewer
rust391_420 now drafting r10 PROVISIONAL request/feedback for one test-only
correction of thosefour. Do not reserve/launch until main reads and validates.
Other reviewersidle. All r7/r8/r9 staticreports are main-integrated; actual
serialqueue41369 still controls execution. No additional admissions beyond25.

R6 all33 diagnostic executions andfour actual admissions completed. Total25
(Go2,Java2,JS9,TS7,Python4,Rust1), allgeneration. Max combined3098,min remaining902;
holds2812 unchanged; no training seal. See RECOVERY_R6_ADMISSION_20260908.md.
Rust0704 allthree timedout on huge zero-area loop; retain reference defect hold,
never count timeouts as semantic control failures. R5 TS0195 no-repeat oracle hold
and earlier unresolved r1/r2 holds remain. Do not restart original quality review.

All r7/r8/r9 teacher runs completed. Main fullyread r7Go all9staticpositive and
r9Python/Rust all6staticpositive; actual admission notyet. R8Java reviewer
rust391_420 finalreport pending mainread; preliminary6positive/4holds on0641/0617
missingwitness,0687constructorstage oracle,0762standalone-newline oracle. Do not
count its draft as reconciled. Other reviewersidle.

ONE ACTIVE SERIAL VERIFIER QUEUE session41369 runs r9six ->r8ten ->r7nine,
output directories recovery-diagnostics/r9,r8,r7. It advances automatically;
do not start any parallel verifier/admission/race job. Once complete, read actual
summaries, integrate Java review, then Go0439/0522 actual-race qualification and
batched candidate admission. r9six currently first in queue. No teacher jobrunning.

GCS terminal r4/r5+r6generation/admission21 checkpoint now VERIFIED by exact
generation download+cmp for archive andreceipt. See RECOVERY_R5_BACKUP.md.
Later r6diagnostics/admission4 andr7/r8/r9 artifacts NOT covered; nextterminalbackup
must include them before anycleanup. No VM/teardown/billingclaim.
144data tests pass. Training/release estimated50%/35%; verification/review active,
notpermissionblocked. Next20–45minlowconfidence; fulldeliveryETAstillungrounded.

## Admission21 checkpoint; r7/r8/r9 and r6 diagnostics active — 2026-09-08

R5 terminal33 diagnostic executions,10 actual admissions (JS5/TS5), zero rejected.
TS0195 remains unsupported mapper identity/extra-absence oracle hold; no repeat
critic. See RECOVERY_R5_ADMISSION_20260908.md. Total21: Go2,Java2,JS9,TS7,Python1,
Rust0, allgeneration. Original holds2812; maximum combined3094,min gap906. No seal.
R4 initial Go27 executions finished; no directionality positives. All9 static
reference corrections positive but tests lack witnesses/contain stated oracles.
Both r4Go and r5TS reports fully main-read/integrated. e4ec08c push succeeded.

R6 generated11; both Python/Rust reports fully main-read. Static positivesPy0269,
0314,0319 andRust0757. Serial actual diagnostics active19463, output r6; don't
start another verifier concurrently. Rust0704 held for huge zero-area copy loop;
preserve actual timeout if observed, never report it as semantic mutant failure.

Active teacher jobs: r7Go9 one-time correction session53332,
pland9a276bd7abdd4537ef3a8ee1dbafa12dc9ce9f6b12447d4948aa3c459d3fabb;
r8Java10 fresh retry session49992,
planf31c7ad69bd41772cd6615be4d3a7afced449ffbd07feb086d5936b9d9365c4c;
r9Py4/Rust2 one-time correction session22325,
plan4b9e973fae402fab5d6bf1db89ea2430e60807d343cb453ab22b2e97924fd63f.
All versions reserved, no duplicates/reuse; up to3 independent calls total.
All reviewers idle after integrated reports/provisional requests. Dispatch new
disjoint reviews only once candidate files exist. Original review stays closed.

Main approved r7/r9 final JSON after complete reads and actualhash validation;
provisional source files preserved. r8 preserves original exact problem guard,
does not rewrite failed r4Java.144 data tests pass. Next: finish r6 diagnostics,
review/verify completed new lanes, candidate admissions and terminal backup.
Latest verified GCS checkpoint remains admission11 until new proof; terminal
r4/r5/admission21 +r6generation snapshot backup in progress, excludes active
r6diagnostics andr7/r8/r9generation. No teardown/VM/training. Estimates50%/35%,
working notapprovalblocked; next10–30minlowconfidence, full-deliveryETAungrounded.

## Latest exact resume checkpoint — 2026-09-08

Post-commit checkpoint: r5 generation/correction completed11; rust451_480 now
reviewing TS6 -> RECOVERY_R5_TYPESCRIPT_REVIEW_20260908.md. Queue TS diagnostics
after Go session95197, not concurrently. Go reviewer preliminary all9 lack exact
defect witnesses, with unsupported0522/0774 nil-empty/found oracles; final report
not yet main-read/integrated. Await final report and actual diagnostics before
freezing one bounded correction. Commit e4ec08c created; push session57186 was
still pending at last check. No extra admissions. R6 generation remains active.

R3 terminal evidence + admission11 total now VERIFIED in GCS (archive and receipt
exact-generation download+cmp). See RECOVERY_R3_BACKUP.md. Active/later runs are
excluded, so preserve/backup them later; no VM/teardown/billing claim.

R4 Go generated9; Java stopped at strict prompt guard:0687 changed only initial
Create to Implement. All Java raw architecture preserved, no tests/candidates
emitted for that lane. Do not weaken guard or overwrite r4. Go artifacts intact;
overall partial-run failure deliberately has no complete candidates.jsonl.
Main started serial Go diagnostics session95197 (output recovery-diagnostics/r4-go);
rust421_450 reviewing all9 -> RECOVERY_R4_GO_REVIEW_20260908.md. Don't duplicate.
Java needs a new versioned disposition; currently no retry is active.

R5 JS5 generated, all15 diagnostic executions passed correct directionality
(session50657 complete, recovery-diagnostics/r5-javascript). Main fully read and
accepted RECOVERY_R5_JAVASCRIPT_REVIEW_20260908.md: all5 static-positive, with
nonblocking coverage limits documented. NOT YET admitted; wait until Go verifier
finishes before running admission to preserve serial host qualification.
R5 TS6 correction continues in session69865; inspect files before dispatching
review or diagnostics. No automatic second critic pass.

R6 request main-read/validated/approved;11 generation parents7Python/4Rust.
Generation active session28510 with ONE lane worker to bound total teacher calls.
Plan0c7d76825c37e2291eb56549277aaa29b44812a6d6b842d2825faf7da69b3295.
See RECOVERY_R6_SELECTION_20260908.md; provisional source files are preserved
and hash-bound, not unreviewed drafts anymore. Thirteen of original57 remain
unselected (repairs and explicit contract deferrals), plus failed-Java disposition.
rust391_420 and rust451_480 idle. No current approval blocker.144 data tests pass.

Counts unchanged:11 admissions, original holds2812, maximum combined3084,
minimum additional916. No training/corpus seal. Training/release estimated50%/35%;
generation/correction/Go verification running. Next decision15–45min lowconfidence;
full delivery ETA ungrounded. Next: finish diagnostics/reviews and batched admission,
then verified terminal backup. Do not restart original quality review.

## R3 closed/admitted2; r4 generation + r5 correction active — 2026-09-08

R3 session49105 completed14; all42 serial diagnostic executions completed in
session87300. All three quality reports main-read/integrated. JS0025/0394 passed
fresh admission (session11278, accepted2/rejected0), including3073 retained
originals +9 prior recoveries +546 evaluation files. See RECOVERY_R3_ADMISSION_20260908.md.
Now11 admitted recoveries; maximum combined3084, minimum gap916. No corpus seal.
JS0296 remains reference+oracle held (required hidden id lost); not in test-only
correction. Original holds2812 unchanged, original quality review remains closed.

Active r4 generation session57980:19 (Go9/Java10), max3workers/twoactual lanes.
Plan91360b15b1ca538a5bfc89b1bf60f55ba8417929cb68406268b677c6f7f46660.
Active r5 one-time test-only correction session69865:11 (JS5/TS6), sequential
lanes, no repeated critic. Plan1d4b2c5d735c02a1e0701546eae007383765129b2886a72aa0f3f66b029eae12.
Both registries reserved; do not duplicate jobs or reuse versions. Generic
spec-grounded adversarial test guidance added for r4;144 data tests pass.

rust391_420 drafting PROVISIONAL r6 request for11 Python/Rust generation parents;
main must read/validate before reserving/launching. Others idle after r3 reviews.
Remaining24 of original57 proposals not yet selected; don't restart selection.
Next: preserve terminal r3/admission2 GCS checkpoint, inspect active run outputs,
review and serially verify, then candidate admission. Current remote verified
checkpoint remains admission9 until new backup proof. No teardown/VM/training.
Training/release estimated50%/35%; generation/correction running, not permission
blocked. Next decision15–45min low confidence; overall delivery ETA ungrounded.

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

## 14. Current continuation — 2026-09-09

Sections 11–13 describe the older 6,000-row plan snapshot. The current terminal
Gate2 decision is recorded in `DECISIONS.md`: one bounded pilot proceeds with
3,225 admitted rows and 2,438,853 input tokens. The source and prepared dataset
are sealed; the latest prepared-manifest seal is
`fc7409c3e68e372e1b1c05b07e5c36db0e3923c84731fe70a0f7937cfd413c25`.

Gate4 local preparation is complete through archive rehearsal. Use
`configs/train/expansion_pilot_v1.json` and
`scripts/train/expansion_pilot.py`; the local execution card seal is
`5d1307c342cf837d5b908ea2579fcad7dfe91b0708d485c08fd498118ded8b7e`.
The reproducible 44-file workspace archive has SHA256
`72e366aa7274723f4c89bb819780a4972a014ac0a2b9b94db4f56955bfaebb3e`
and re-preflights identically after extraction.

After training, run `scripts/train/verify_expansion_pilot.py` before any
evaluation. It rejects a non-executable card, incomplete/token-short run,
identity mismatch, failed save/reload, cost or VRAM escape, and any adapter
file mutation.

Then use `scripts/eval/adjudicate_expansion_canary.py` on the frozen tranche-1
candidate and canonical base task evidence. Only status
`promote-to-full-development` authorizes the 180-task development run; a
successful training process or lower validation loss does not.

`scripts/eval/build_expansion_evaluation.py` creates the candidate canary and
full-development inference configs after terminal verification. The generated
manifest deliberately records `canary-ready-full-blocked`; do not run its full
config until the canary adjudicator produces the matching promotion seal.

Do not execute this card as-is. Its status is deliberately
`prepared-not-executable` and `provider_execution` is null. Next, after GCloud
authentication is restored, gather current read-only price/quota evidence only
under explicit authorization, bind zone, machine, price, total cost ceiling,
image and archive generation into a new executable card, obtain fresh explicit
approval, then run training -> save/reload -> 30-task canary -> conditional
180-task development evaluation -> evidence backup. No VM is active now.

## 15. Verified terminal input backup — 2026-09-09

GCS authentication is restored and both launch-critical local archives now
have exact-generation roundtrip proof. The Gate2 archive is generation
`1788908479441360`; the Gate4 workspace is generation `1788908484381745`.
Their downloaded bytes match local SHA256 values `b49fcf31...05845` and
`72e366aa...ebb3e`, respectively. The sealed receipt at
`measurement/data/expansion-v1/PILOT_SEALED_3225_GATE4_INPUT_BACKUP_20260909.json`
is GCS generation `1788908613275676` and was also byte-compared after download.
No compute inspection or mutation occurred. The next hard boundary is explicit
authorization to inspect current L4 availability/quota and bind the priced
execution card; VM creation requires a second explicit approval of that card.

## 16. Exact Gate 4 prelaunch proposal — 2026-09-09

Read-only inspection is complete. `us-east1-c` is UP, `g2-standard-8` resolves
to 8 vCPU and 32 GiB, regional L4 quota is 16 with usage 0, and replacement
image `common-cu129-ubuntu-2204-nvidia-580-v20260831` is READY. These checks do
not guarantee capacity.

All rehydrated launch inputs have exact-generation roundtrip proof. Important
generations are model `1788910413265608`, CUDA image `1788913987238416`,
verifier archive `1788912580629555`, training workspace `1788908484381745`,
evaluation workspace v4 `1788916797595767`, startup controller v2
`1788916809873874`, and metadata wrapper `1788916091334917`. See
`measurement/gate4/gcloud/20260909T001300Z/` for the canonical receipts.

The exact pending proposal is Standard on-demand `g2-standard-8` in
`us-east1-c`, one L4, 200 GiB `pd-balanced`, no external IP, automatic restart
disabled, eight-hour VM maximum, six-hour training wall, and `$7.50` absolute
incremental ceiling. Its seal is
`5bb6b25b448a509f570dd924b6d508ab057fd2f2455d06db8353054cda06aba3`.
Official pricing used is `$0.853624312/hour` for compute and
`$0.000136986/GiB-hour` for balanced disk. The 200 GiB disk replaces the unsafe
50 GiB minimum while remaining within the same ceiling.

The final corrected prelaunch evidence archive is GCS generation
`1788917258351261`, SHA-256
`80952626cd3cfd785cde8aa0217e32646acb5a98b31d34ff92a3662727615781`;
its receipt is generation `1788917344648616` and was byte-compared. Earlier
preflight archive generations are superseded because their internal seals used
`jq` numeric canonicalization; do not use them for authorization.

No VM exists. The hard stop is fresh explicit approval of the exact proposal.
After approval: write sealed approval evidence, bind a provider-executable
training card, upload and roundtrip-verify that card and the outer execution
card, then create the named temporary network/subnet/disk/VM. Run training ->
save/reload verification -> canary -> conditional full development evaluation
-> terminal backup -> independent verification -> full teardown -> two absence
checks. A canary `do-not-promote` is a completed result and must not be labeled
an infrastructure failure.

## 17. Gate 4 approved execution active — 2026-09-09

Navneet explicitly approved proposal
`5bb6b25b448a509f570dd924b6d508ab057fd2f2455d06db8353054cda06aba3`
and its `$7.50` ceiling. Attempt `20260909T015118Z` uses the one approved
Standard `g2-standard-8` instance `ganesh-mini-g4-l4-20260909t015118z` in
`us-east1-c`, provider ID `8737372232357839343`, with one L4, a 200 GiB
auto-delete `pd-balanced` boot disk, no external IP, automatic restart
disabled, and provider maximum duration eight hours with termination action
`DELETE`. Temporary network `ganesh-mini-g4-net-20260909t015118z` has provider
ID `5984537846207021268`; its subnet has Private Google Access. No address or
NAT was created.

The first boot failed closed before training because the approved proposal and
prelaunch receipt contained a 65-character evaluation-manifest hash with one
duplicated `f`. The exact-generation object itself and local roundtrip copy are
unchanged and hash to
`cf88badcc33c78c824c24dc67c9accf9f5c3527fe3b140e4218f33f59c42a360`.
The wrapper preserved this failure under the attempt's
`wrapper-failure-20260909T015118Z/` GCS prefix and shut down. See
`measurement/gate4/gcloud/20260909T015118Z/bootstrap-correction.json`.

The same approved VM, disk, network and subnet were retained. Only the bad
control binding was corrected. Outer card v2 is GCS generation
`1788919774477052`, file SHA-256
`ef5e3727e58a6873d6256e8bfed2ae92e53d9f0ebf2aeb5dc4c41920c29e6aa9`,
internal execution seal
`f1b1ff38c7c393f2cdd7ca724d679d4dbb178703731b0a8725303b9bd285c0c8`.
The same instance restarted successfully. All ten immutable runtime inputs
passed guest-side download hashes, the Docker/CUDA runtime loaded, and the
campaign ledger reached `workspace-and-provider-admission=passed`. Runtime
checkpoints are active at
`ganesh-mini-1.0/training/expansion-pilot-v1/attempts/20260909T015118Z/runtime-checkpoints/20260909T015118Z/`.

Current state is ACTIVE Gate 4 campaign execution. Do not create a second VM
or duplicate the attempt. Monitor the checkpoint phase ledger and terminal
prefix. After terminal backup, independently download exact generations and
verify completeness, then delete the retained VM/disk/subnet/network and
perform two absence checks. Preserve the failed first-boot evidence as part of
the final audit trail.

## 18. Gate 4 cost-binding failure and same-VM retry preparation — 2026-09-09

The v2 campaign passed workspace/provider admission and verifier-runtime
readiness, then failed closed before model initialization or any trained token.
`run_sft.py` correctly rejected the controller's live elapsed-cost value because
the provider-bound training card requires `prior_cost_usd=0.0`. Terminal exit
codes are both `1`; exact terminal evidence was downloaded and its
`runtime-files.sha256` inventory passed. A separate GCS failure archive is
generation `1788920860248908`, SHA-256
`e8b53c43e9d579091f5ce8ca6f99e07898b410895680b41c3566afad4d0e5bdf`.
The VM is `TERMINATED`; no compute cost is accruing, but its retained disk
remains billable pending the same-VM retry or teardown.

The controller now passes the exact provider-bound prior cost rather than its
own elapsed estimate. A regression test asserts `--prior-cost-usd 0.0`; focused
tests pass. Startup v3 preserves old work/evidence directories before a restart
so retained disk state cannot violate fresh-output guards. Evaluation workspace
v5 (containing the corrected controller) is GCS generation
`1788920896367400`, SHA-256
`717119c690765e9516c43e0c82a1ed5adc193f023ebe6667c10f9359a5fcf1b6`;
manifest generation `1788920902310400`, SHA-256
`6aa5a4e83ae6a4cde12b9b112d477805f8efb3a0247d074274c85237fb8a68ca`.
Startup v3 is generation `1788920906112661`, SHA-256
`84d211347059192d061c50988e86f9ad38d9675e07b2d4faa35923d6b3192b41`.

Next: commit the fix/evidence, seal and roundtrip a new outer card for a new
attempt prefix, update metadata on the same provider instance ID, and restart
that instance. Do not create a new instance. If the same-VM restart cannot
proceed within the approved ceiling, tear down and request a new exact card.

## 19. Gate 4 retained-disk retry bootstrap correction — 2026-09-09

Attempt `20260909T022847Z` reused the same provider instance and passed all ten
immutable input downloads. It then failed closed before the campaign
controller, model initialization, or training because reinstalling the pinned
Docker packages on the retained boot disk opened an interactive debconf
question without a terminal. Startup exit is `1`; the VM returned to
`TERMINATED`, so GPU compute is not accruing.

The exact terminal inventory was downloaded and verified. Its distinct GCS
archive is generation `1788922020962270`, SHA-256
`af0dd839bbe717ac9aea59f9ca78b54e45adc4fcddd2e3dd9ece9797e16249db`,
and an exact-generation download compares byte-for-byte. The startup controller
now exports noninteractive debconf/needrestart settings, preserves installed
configuration, and bounds each `dpkg` attempt to 300 seconds. The focused
campaign tests and shell syntax check pass.

Next: publish and roundtrip startup v4, commit the correction and evidence,
seal a new attempt card with a reduced remaining runtime envelope, update only
the retained instance metadata/scheduling, and restart the same provider ID.
No second VM is permitted. After any terminal result, verify all evidence in
GCS before deleting the VM/disk/subnet/network and completing two absence and
billing checks.

## 20. Gate 4 training attempt active — 2026-09-09

Google authentication was restored. Attempt `20260909T025013Z` is active on
the same instance ID `8737372232357839343`; no second VM was created. Startup
v4 is GCS generation `1788922338878446`, SHA-256
`a0006bdb1ef68b3f4fe063fcfafae2b3631c26ddcd51d4611224e9e8b189327c`.
The outer execution card is generation `1788922391795570`, file SHA-256
`8e3aa8d90fb3abae13f5320ba1b2d46ea0f8b5f6821a232fd705931c3d7b22db`,
and internal seal
`bc9376f67a44b5a9fe2fd94462bf53eb83ae5a7e2938d34a1a01a4dd0e09add8`.
Both uploads have exact-generation byte-identical roundtrips.

The provider maximum duration was reduced from eight hours to 27,000 seconds
(7.5 hours), with automatic restart still disabled and termination action
`DELETE`. The v4 boot passed the retained-disk package-install point, loaded
Docker successfully, and created runtime checkpoints. The latest verified
campaign ledger is `running` with
`workspace-and-provider-admission=passed`; model initialization/training is the
current phase. Monitor the attempt prefix only. On terminal state, download
and verify the complete inventory before teardown and the two absence/billing
checks.

## 21. Gate 4 expansion pilot terminal; do not promote — 2026-09-09

Attempt `20260909T025013Z` completed all 2,438,853 training tokens. Training
evidence seal is
`3f589131eee6b214013e41cf6e81d6b7bab41b216586c93f3ddc4d29db704158`;
the eight-check terminal training report passed under seal
`6a09478412aad9200097b8142b498c112b60fa0e6c35ba82328f1a61b06fee13`.
Final adapter safetensors SHA-256 is
`552d85a0687d41986c1b8608db907ba0b8ae7192c96b082de18ab235e28f42a8`.

The candidate canary completed 30/30 and passed 6 versus base 5. Candidate
lane passes are Go0/Java1/JavaScript1/TypeScript2/Python1/Rust1. Only Rust
improved, so the frozen four-of-five-family rule failed even though net gain,
zero lane regression, non-code, truncation, and save/reload checks passed.
Adjudication is terminal `do-not-promote`, seal
`3d53bc8b484f295823344984ca37e4dc87c842452aaa3c20ceb5d02d661d249d`.
Do not run the full 180 candidate evaluation or scale this recipe.

The original adjudicator rejected unselected
`dev-t2-javascript-decode-hex`, but the frozen evidence was not stale. Its
captured stderr contains U+00E9 (`é`); the adjudicator incorrectly used
ASCII-escaped JSON while the project evidence contract hashes canonical UTF-8
JSON. An independent audit recomputed every seal and binding: all 180 base task
seals, the run seal, all 180 generated-output bindings, and all 180 verifier
result bindings pass. No frozen evidence was changed or repaired. The
adjudicator and checkpoint-sweep builder now use the project canonical
serializer (`ensure_ascii=False`, `allow_nan=False`, UTF-8). Audit report seal:
`307bff0cafd28b02278b5fdcbbd7117677269cd9707d6beaba133f22dba96c98`.

Before teardown, the 128-object/56,925,573-byte terminal prefix was verified
against its 127-file runtime hash manifest. A separate 51,674,173-byte archive
was uploaded at generation `1788935240864459`, SHA-256
`24abdb78753ad59a25adbc3ca1ddab31da0176c3de935b02b874e5638dab8e31`,
and exact-generation roundtrip passed. Finalization receipt generation is
`1788935386817248`; teardown receipt generation is `1788935763309387`, both
byte-identical on roundtrip.

The instance, auto-delete disk, subnet, and network are deleted. Two checks 12
seconds apart returned 404 for each, and project inventories show zero
instances, addresses, forwarding rules, routers, reservations, snapshots,
images, or machine images. An unrelated unattached 200 GiB balanced disk named
`laxmi-wmv2-training-01` remains in `us-central1-a`; do not delete it without
Navneet's explicit ownership decision. Temporary OAuth material was zeroed and
removed. Next: preserve/commit the decision evidence and reader canonicalization
fix, then run the bounded checkpoint diagnostic before
designing a new data/mechanism hypothesis.
No compute is active and no further GCloud action is authorized by this result.

## 22. Checkpoint diagnostic prepared locally — 2026-09-09

Failure analysis is in
`docs/process/GATE4_EXPANSION_PILOT_FAILURE_ANALYSIS_20260909.md`. Of 30 final
candidate programs, 10 are byte-identical to base; 20 changed, but only the
Rust `collapse-runs` change altered failure to pass. Validation loss improved
without broad executable transfer.

The five unmeasured checkpoint configs bind adapters at 406,491; 814,098;
1,224,637; 1,629,235; and 2,036,559 seen tokens. The final 2,438,853-token
checkpoint is already measured. Sweep manifest seal is
`6af2ad473e2d119bcf1149540705a3d7faaf7f4584b1b7626bf568cabfec4b5c`.
Evaluator support verifies each adapter against its checkpoint manifest and
the original training identities. The summarizer is diagnostic-only and cannot
select or promote a checkpoint. Twenty-five focused tests pass.

The fail-closed evaluation-only host/startup package is implemented locally.
It serializes the five checkpoint canaries on one GPU, executes generated code
only through the existing network-disabled verifier containers, seals each
task/run/summary, and has no training or promotion authority. The workspace
can now be sealed locally. GCS upload of the new workspace/controller/wrapper
is the next hard boundary because exact object generations are required before
the provider proposal can be materialized. VM creation then requires separate
explicit approval of that exact sealed proposal. Planning bound: Standard
`g2-standard-8`/L4 in `us-east1-c`, two-hour maximum, no external IP, restart
disabled, auto-delete 200 GiB disk, estimated 25–40 minutes of evaluation plus
restore/backup, and a $2.25 absolute incremental ceiling. No cloud resource is
active.

The deterministic local workspace contains 596 files. Its manifest seal is
`0b5baf8ded482fefa8b827169fc425c6881365e1a08ed814bcda226e4ffa94ae`;
the 1,019,144-byte archive SHA-256 is
`8a3619ee9bbb9816359eecad4c7b46c92f202644e29090880b3d44e7b485d3d6`.
It was extracted and independently re-verified against every manifest file.
The 26 focused tests pass. The broader campaign/eval/inference suite has 164
passes, one skip, and the same three historical Gate 1 stale-workspace/source-
identity failures; none is on the new sweep path.

The next authorization boundary is deliberately upload-only. Plan
`measurement/gate4/checkpoint-sweep-20260909/gcloud-upload-plan.json` permits
exactly four named uploads totaling at most 1,163,234 bytes, generation capture,
and exact-generation byte roundtrips. It forbids compute and all infrastructure
creation, deletion, training, evaluation, promotion, and publication. Its seal
is `22357cac8b6da43aa56bd11eaede2f199995a90035aa76caf5c235ccb485cc4b`.
Do not execute it without fresh explicit approval of that exact seal.

## 23. Checkpoint-sweep inputs uploaded; exact VM proposal pending — 2026-09-09

Navneet explicitly approved upload-only plan
`22357cac8b6da43aa56bd11eaede2f199995a90035aa76caf5c235ccb485cc4b`.
Exactly four named objects totaling 1,163,234 bytes were uploaded. Their GCS
generations are workspace archive `1788943258027996`, workspace manifest
`1788943277835940`, startup controller `1788943280088544`, and metadata wrapper
`1788943280777084`. Every exact generation was downloaded and compared
byte-for-byte with its approved source. Upload receipt seal:
`36711a078822cca4ffa60da6f8c2f368ad1c1454d199c9051355f22052088e81`.
No compute or infrastructure action occurred.

All ten runtime inputs are now generation-bound under bindings seal
`2ba45d22404120afe6b081aa67455d3604a717a349a4cfe1c20225055b036763`.
The exact non-executable checkpoint-sweep proposal is one Standard
`g2-standard-8` with one L4 in `us-east1-c`, 200 GiB auto-delete balanced disk,
no external IP, automatic restart disabled, and 7,200-second maximum lifetime.
It permits five serial 30-task development-canary evaluations only: no
training, decision-surface opening, promotion, or publication. Provider upper
bound is `$1.762043024`; absolute incremental ceiling is `$2.25`. Proposal
seal: `b31d95b6e9097fa1056a522628773240d0c2d80ebd925becf457163b28900db5`.

Current state is waiting for fresh explicit approval of that exact proposal.
Do not create, inspect, or mutate GCloud compute/infrastructure until approved.

## 24. Checkpoint-sweep first execution closed; corrected v2 local — 2026-09-09

Navneet explicitly approved proposal
`b31d95b6e9097fa1056a522628773240d0c2d80ebd925becf457163b28900db5`
and its `$2.25` ceiling. Approval seal is
`52da6ca8eeca3c9b2ddac6a138ce4d547f7631092a65f128356e21c6092c63f3`;
execution-card seal is
`60bec199932815236ae11477fd3a5884daeb1ee59ade201390bd8b1a38a57fd3`.
The attempt used exactly one Standard `g2-standard-8`/L4 in `us-east1-c`, no
external IP, an auto-delete 200 GiB boot disk, restart disabled, and the
7,200-second provider maximum.

The guest downloaded and verified all generation-bound inputs and loaded the
CUDA image. It then failed at the first host workspace check because
`run_checkpoint_sweep_host.py` hardcoded
`ganesh-mini-development-evaluation-workspace/v1`; the supplied manifest
correctly declared `ganesh-mini-checkpoint-sweep-workspace/v1`. The failure was
before verifier preparation, model loading, or evaluation. Exactly zero tasks
executed and no checkpoint result exists. Failure receipt seal:
`abf1b6b5133684681714621b5e0baf143f5b62a3fcae852ec1f054c57c75c4c3`;
GCS generation `1788952964615784`; exact roundtrip file SHA-256
`5bad200cfcec84bbfa1f8c2c4b186cefd66c79ed780399d76a97f43a03d7960a`.

All five raw terminal files are retained at their exact generations. The
terminal `runtime-files.sha256` is deliberately not treated as valid evidence:
the terminal backup command continued appending to `startup.stderr.log` after
the inventory was created. The other four inventory rows match. Full serial
output was unavailable after guest shutdown; the preserved stderr contains the
exact workspace-contract failure line.

The VM, auto-delete disk, subnet, and network were deleted. The sealed teardown
receipt records two 404 absence sequences, 12 seconds apart. Receipt seal:
`2a99287bb679ac16a7499dd45342cf4ad246498be2ba81f0e804fd764d06afef`.
Its create-only GCS object is generation `1788953722389669`, 1,084 bytes,
SHA-256
`31331677c10eb0b4ab653bfe25d7544d1c32f518350dfa8a23d568214e85a448`;
the exact-generation roundtrip is byte-identical. Raw provider deletion/404
responses were not persisted locally, so do not overstate the receipt as
independent provider-level corroboration. No Ganesh resource from this attempt
is active. The unrelated `laxmi-wmv2-training-01` disk remains out of scope.

Local corrections are complete: the runner expects the dedicated sweep schema;
startup captures both log-tee PIDs, restores fd 1/2, waits for both tees to
drain, and only then inventories terminal files. The rebuilt deterministic v2
workspace contains exactly 596 unique regular files and independently matches
all 596 manifest size/hash rows. Current inputs:

- workspace archive: 1,019,245 bytes, SHA-256
  `fd1cee18029e53644ba3c694558b52cbca9e91c5a5e47a9150d6f8b73240e441`;
- manifest file: 134,866 bytes, SHA-256
  `6c11b79d4dfb099c5f97cebd10eee3b114c06369199eac613f7612dd235b7264`,
  internal seal
  `bf8f11a413425d0c2f530db8db0a0de3f88a4bb2cf335fffac6b155aa342f816`;
- startup controller: 7,198 bytes, SHA-256
  `202730fe842e272c302d1624a9dd1b1195e8c470e6557ad48de5129ac355ad97`.

Twenty-two checkpoint-sweep tests, Python compilation, shell syntax, and diff
checks pass. Failure evidence and the corrected package are committed and
pushed at `1a5a2e0b201bf689b8374e6d2275aa0a47c60f4a`.

The new upload-only plan permits exactly three named corrected objects totaling
1,161,309 bytes under the commit-bound `input/1a5a2e0/` prefix, generation
capture, and exact-generation byte roundtrips. It forbids compute,
infrastructure, overwrite/delete, training, evaluation, promotion, decision
opening, and publication. Its seal is
`356dc0403d6ccc82683774bb3d381280bbc87b432e1f1116cb9b0a12a7b7f769`.
That upload is the next hard stop and requires fresh explicit approval of this
exact seal. Only after exact-generation roundtrips may a replacement VM
proposal be sealed; VM creation requires another separate approval. Do not
reuse the consumed `b31d95...` approval.

Milestone estimate: training program 70%, release readiness 52%, inception-to-
delivery 60%. Current state is ACTIVE on local sealing, not technically stuck.
After the two new GCloud approvals, checkpoint evaluation plus backup/teardown
is estimated at 1.5–3 hours. End-to-end release ETA remains 2–5 days at low
confidence because the sweep may still require a new data/mechanism experiment.

## 25. Corrected sweep inputs uploaded; replacement VM proposal pending — 2026-09-09

Navneet approved upload-only plan
`356dc0403d6ccc82683774bb3d381280bbc87b432e1f1116cb9b0a12a7b7f769`
by replying `approved` directly to the exact-plan request. Approval seal is
`ae06276ec433c59a4b6ae288890091880efbf5b42005536ad46e09996b5d3a0f`.
Exactly three corrected objects totaling 1,161,309 bytes were uploaded
create-only. No compute or infrastructure action occurred.

Exact immutable generations are workspace archive `1788958259527767`,
workspace manifest `1788958261099778`, and startup controller
`1788958261821760`. Every exact generation was downloaded and compared
byte-for-byte with its approved source. Upload receipt seal is
`45a61f7866b0966dba7ec00cd7d49304be6cb13b3acaa764ea272c69f3fc224e`.

All ten runtime inputs are now rebound under bindings seal
`58df54d10772db3655cd25d42f8068779d9a226853e3b7c8df35da87499be0fa`.
The unchanged recovery/model/CUDA/Docker/verifier/metadata-wrapper generations
remain exactly as previously verified; only workspace archive, manifest, and
startup controller point to the corrected commit-bound objects.

The replacement non-executable VM proposal preserves the original resource and
cost envelope: one Standard `g2-standard-8`/L4 in `us-east1-c`, 200 GiB
auto-delete balanced disk, no external IP, restart disabled, 7,200-second
maximum, provider upper bound `$1.762043024`, and `$2.25` absolute incremental
ceiling. It permits exactly five serial 30-task checkpoint evaluations and
forbids training, full-development evaluation, decision opening, promotion,
and publication. Proposal seal:
`ab86a71a0178d6f7a9232f9ee9dee72650d2fd7dd5568844c10a7ffd68dd1de4`.

Current state is WAITING at the required GCloud compute boundary. Do not
inspect, create, start, stop, mutate, or delete GCloud compute/infrastructure
until Navneet explicitly approves that exact proposal and `$2.25` ceiling.
After approval, record a new one-use approval and attempt ID, perform provider
preflight, create one temporary resource set, run the sweep, preserve and
roundtrip all terminal evidence, then delete resources and verify absence
twice. Training 70%, release readiness 52%, overall 60%. Sweep-to-teardown ETA
after approval is 1.5–3 hours; end-to-end release ETA remains 2–5 days at low
confidence.

## 26. Replacement checkpoint sweep closed; proceed to mechanism redesign — 2026-09-09

Navneet explicitly approved proposal
`ab86a71a0178d6f7a9232f9ee9dee72650d2fd7dd5568844c10a7ffd68dd1de4`
and its `$2.25` ceiling. Attempt `20260909T130347Z` used the exact authorized
Standard `g2-standard-8`/L4 resource contract. The first creation request hit
`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`; one bounded identical retry
succeeded. No alternate zone, machine, or price was used.

Sealed input admission and verifier preparation passed. Four checkpoints
completed 30/30 tasks with valid run and task bindings:

- 406,491 tokens: 6/30; Go0, Java1, JavaScript2, TypeScript2, Python1, Rust0;
  run seal `c588d4679ce3ccd88d1168ac300a0690769699d6d09802e4a16cb80620bdd853`.
- 814,098 tokens: 4/30; Go0, Java1, JavaScript1, TypeScript1, Python1, Rust0;
  run seal `64fd1edc2d30f56a4e2fa8e0aeea8771f33b47f2e17364d5182fd0bf43cd35c3`.
- 1,224,637 tokens: 5/30; Go0, Java1, JavaScript1, TypeScript1, Python1, Rust1;
  run seal `4db2aefdf1ee39d9c38c2cedd88c29cb184feb77fe86674bfaa2a0c29867d54f`.
- 1,629,235 tokens: 5/30; the same lane counts as 1,224,637; run seal
  `a065d563a4f4193d5237382e18ad4d570dc2cd4ebfcd12b66692e7191cc46397`.

The fifth 2,036,559-token checkpoint produced only empty stdout and a 230-byte
weight-loading stderr. It created no generated/task/run evidence and remained
unchanged from 13:45:07Z through 14:21:33Z despite the 1,200-second checkpoint
limit. Do not call this a model failure and do not reconstruct a score. The
host/controller terminal path did not complete; root cause is not yet proven.

Before deletion, all 260 GCS objects totaling 3,071,483 bytes were downloaded
at their exact generations and verified against size and MD5 metadata. Listing
file SHA-256 is
`04b6cc7ef4283d69a091950be5177b9e204d127694171cc9624b450dba338466`.
Interruption receipt seal is
`e7f96448ddf96ffb4ac309d9e892c9ff8c125cdeba465258edfff2483db8549c`
(file SHA-256
`41ae1ab624448b568d5d3e229d0bee55eba23b8aa0864235e11570ee98ac0db7`);
teardown receipt seal is
`8fb800123772f4578103577e8492cb7b5b776499aea33355b645fe5599b7c02c`
(file SHA-256
`9505a31cc955aaf4a5754eff2d23bcc9fcff42c3c206676f9c93cc0c7839948d`).
The 447,771-byte full evidence archive is generation `1788964553220467`,
SHA-256 `f9314b0e959bc9522ef35e099d15eb865a931d470fa0f9c29789afd9d95047f7`.
Every finalization object passed exact-generation roundtrip. Finalization
receipt seal is
`a7f803fc2d50edba18d42dfcd95fb74de83ff5731dfbedf1d8f04691610f42c5`;
its object generation is `1788964556536552`.

The VM, auto-delete disk, subnet, and network were deleted and returned 404 in
two checks 32 seconds apart. No project instance, address, forwarding rule,
router, reservation, snapshot, image, or machine image exists. The unrelated
`laxmi-wmv2-training-01` disk remains; do not delete it without a separate
ownership decision. Ganesh sweep compute billing is closed, but project-wide
GCS-only billing is not true while that disk exists.

The sweep evidence rejects early stopping as the repair: no completed
checkpoint shows broad multilingual transfer. Gate 4 remains `do-not-promote`.
Continue locally with task-level trajectory analysis, a bounded process-group
timeout repair, and a materially different data/mechanism pilot design. Any
new GCloud execution needs a new sealed proposal and explicit approval.

## 27. Capacity probe locally prepared — 2026-09-09

The sealed trajectory report covers the exact base, four valid intermediate
checkpoints and the final adapter. Across the six points, 23/30 canary tasks
are stable failures, four are stable passes and three change status. Earlier
stopping cannot satisfy Gate 4. The missing 2,036,559-token run stays excluded
as controller/runtime evidence, not a model result.

`configs/train/expansion_capacity_probe_v2.json` defines one rank-16 combined
capacity/scope probe: all 24 language-model attention layers plus MLP
gate/up/down in layers 16–23. Shape-derived trainable parameters are 7,520,256,
10.3x the prior 729,088. The probe is bounded to the first 624 existing rows
and 468,601 tokens; weighted family objective shares span 18.32%–21.95%.
Continuation requires two improved families, net +2, zero lane regression,
zero non-code/truncation increase and save/reload reproduction. It has no
promotion or release authority.

Config file SHA-256 is
`3e201e80560052a503ab4b56b71684a4c50430750bb6de9cc8419dbd30bb5aa5`;
local preflight card seal is
`15ec9533a547c0cc45a1fa0dcfb5267440d4118e2c8f4c0a255f502c391afafd`.
The 46-file/5,575,271-byte training archive SHA is
`0550d2f39bda880077b03b5f0cc57e2eff0e08db0ba130339abb17f715797945`;
manifest seal is
`fbb4b4cf30e6664fe583c9a8ff5a2042b7ab282663174fd21f534b7e51350bcd`.
The development-only evaluation archive is 1,012,468 bytes with SHA
`6bca993d7ba0a744724aef324b303e1caf95a7be7943ba18a874e02fe0758db3`;
its manifest seal is
`752eb6a124dd2949226164fbe237e1f31c7a264c9fe5a0b69534c517c8f39b02`.
Thirty-eight focused tests pass. The full Python 3.12 suite retains only the
three documented stale Gate 1 failures. State is local-prepared,
cloud-unbound. Do not
inspect or mutate GCloud until a new exact proposal is explicitly approved.

## 28. Capacity-probe upload boundary awaiting approval — 2026-09-09

The upload-only plan at
`measurement/gate4/capacity-probe-20260909/gcloud-upload-plan.json` binds four
new immutable objects totaling 6,729,319 bytes: the sealed training archive and
manifest plus the sealed development-only evaluation archive and manifest.
Plan seal is
`a218b5f6ded99c9277d2e26e4a3c10737568906290894152cf4df5e94e7add5d`.

This boundary allows create-only upload, assigned-generation capture,
exact-generation download/byte comparison, and a sealed local receipt. It
forbids GCloud resource inspection, provider pricing/card binding, compute,
network changes, training, evaluation and publication. Authentication alone
does not approve it. After explicit approval and successful upload, build a
separate exact compute proposal with current price and an absolute ceiling.

## 29. Capacity-probe workspace upload complete — 2026-09-09

Navneet approved exact upload-only plan
`a218b5f6ded99c9277d2e26e4a3c10737568906290894152cf4df5e94e7add5d`.
All four objects were created without overwrite, assigned immutable
generations, downloaded by those exact generations and matched against their
sealed sizes and SHA-256 values. Total bytes are 6,729,319. Receipt seal:
`ad5c9ae541bc0ef53a0c0fdbdb9a49512e002a01920ee95e3d927fb6c4464e01`;
receipt file SHA:
`ffe17da6f4b6924484927e6a347cf15e4a6c52d3a3a69f0e6ed25f4793be9a33`.

No compute, network, disk or provider inspection occurred. The next hard
boundary is a fresh approval to inspect current Standard L4 price, quota,
resource absence, IAM and immutable-input availability, then seal an exact VM
proposal. That inspection does not itself authorize VM creation or training.

The read-only inspection plan is now sealed at
`50b3783cb1287bfa3a44e00772db6f24bfd2b70b8d102b1b9f537276042fd521`.
It binds attempt ID `20260909T173721Z` and exact prospective resource names.
It permits only zone/machine/L4/quota, resource-absence, IAM,
generation-availability and price reads. It requires explicit approval and
does not authorize resource creation, object mutation, card upload or compute.
# Capacity-probe inspection complete; exact VM proposal pending — 2026-09-09

Current gate: Gate 4. Navneet approved only GCloud read-only inspection plan
`50b3783cb1287bfa3a44e00772db6f24bfd2b70b8d102b1b9f537276042fd521`.
That inspection is complete with sealed report
`74b3757f92d614a4f65d02bd4f8a60b15aac5134a9e1d0acd98c05a466bb4a0f`:
the exact VM/disk/network/subnet names are absent; `us-east1-c` is UP;
`g2-standard-8`, `nvidia-l4`, unused L4 quota 16, VM bucket objectAdmin and all
ten generation-pinned inputs passed. This does not claim point-in-time GPU
capacity. No upload, compute, infrastructure mutation or billing action was
performed.

The next exact execution proposal is local and non-executable, seal
`461e968ae2fa79d3401e522d52bf91cbcc359cdded68d8fff62dff51631934f0`.
It is one Standard `g2-standard-8`/L4 attempt, 200 GiB auto-delete balanced PD,
no external IP, restart disabled, maximum 7,200 seconds, provider upper
`$1.762043024`, absolute incremental ceiling `$2.25`. After exact approval it
authorizes only two create-only execution-card uploads, the 624-row capacity
probe, save/reload and the frozen 30-task continuation screen. It explicitly
forbids full 180-task evaluation, decision opening, main training, merge,
quantization, publication and release claims. Preserve and independently
verify all GCS evidence before teardown; then delete only named Ganesh
resources and verify absence twice. Never touch unrelated disk
`laxmi-wmv2-training-01`.

Current status: the lane-stratified probe is terminal `do-not-promote`; no
Ganesh Compute resource is active. Gate 4 remains blocked on model-quality
transfer, not infrastructure or authorization. Local transition analysis is
the next active step.

## 30. Gradient-conflict probe inspection complete; execution approval pending — 2026-09-13

The v4 gradient-conflict mechanism package is locally sealed and its five new
workspace/controller objects are generation-pinned in GCS under upload receipt
`4ab0ab64e896efcb4000abc1125f59eced2534a93cce6d8eeca3fb5a6ecfa88b`.
Navneet approved read-only inspection plan
`b35f9ff928066701a3aa94c2e54eb5e81c1050f984393a0819d9e56479fce4b4`.
After authentication was restored, the inspection completed without any cloud
mutation. Report seal:
`d92854a13a237c44cf6a172dfa53794c4c2ce32d77cf8adf9d99ed7b85d08d14`.

The exact VM/disk/network/subnet names are absent; `us-east1-c` is UP;
`g2-standard-8` is 8 vCPU/32 GiB; `nvidia-l4` is visible; regional L4 quota is
16 with usage 0; VM bucket objectAdmin is present; and all ten immutable inputs
match their generation URIs and sizes. These facts do not guarantee
point-in-time L4 capacity.

The resulting non-executable proposal seal is
`faf9ed1f062f49d6f48c0a3cfeec2beedc1dcd67aa5ab85a757ec384de4af7ff`.
It authorizes, only after exact approval, one Standard `g2-standard-8`/L4 VM,
200 GiB auto-delete balanced disk, no external IP, restart disabled, and a
7,200-second maximum. Provider upper bound is `$1.762043024`; absolute
incremental ceiling is `$2.25`.

Execution first performs an eight-group gradient-conflict audit with zero
optimizer steps. If its frozen threshold fails, stop with no training or
canary. If it passes, run the bounded 640-row PCGrad probe, the sealed 60-row
retention guard, and only the frozen 30-task continuation screen. Back up and
independently verify every terminal artifact in GCS before deleting the named
resources, verify absence twice, preserve all GCS evidence, and never touch
`laxmi-wmv2-training-01`. Full development evaluation, decision opening, main
training, merge, quantization, publication, and release remain forbidden.

Current state is WAITING FOR EXACT EXECUTION APPROVAL. No Ganesh compute is
active. After approval, audit-only failure can close in roughly 30–60 minutes;
the conditional PCGrad path through verified teardown is roughly 2–3 hours.

## 31. Gradient-conflict probe execution active — 2026-09-13

Navneet approved exact proposal
`faf9ed1f062f49d6f48c0a3cfeec2beedc1dcd67aa5ab85a757ec384de4af7ff`
with the `$2.25` absolute incremental ceiling. Approval seal is
`8734cf0dea1e77a9ad59d89619b5444863d370c82fd7e01278eaebf28067ac2f`.
The two execution cards were uploaded create-only and exact-generation
roundtrips passed. Training card generation is `1789320243256446`; outer card
generation is `1789320280154764`; outer execution seal is
`319673d048a063af9f1b8b6b4d609783ad89c0fa26a45b6253b40a57cf1e063c`.

The single named Standard L4 VM is active in `us-east1-c`, provider instance
ID `2866150186379076149`, with no external IP, restart disabled, auto-delete
200 GiB disk, and provider termination timestamp `2026-09-13T19:26:52Z`.
All immutable guest downloads passed and the network-disabled audit container
started. It exited after about 4m20s, which is too short to infer the PCGrad
path. The host has not yet uploaded terminal evidence, so do not claim an audit
decision, training result, or failure. Preserve the VM until sealed terminal
evidence is in GCS; then roundtrip it before deleting the exact resources and
checking absence twice.

## 32. Gradient-conflict attempt invalid; teardown complete — 2026-09-14

The provider deleted instance `ganesh-mini-g4-grad-20260911t020000z` and its
auto-delete boot disk at the sealed lifetime boundary before terminal-rescue
approval arrived. GCS contains only the two immutable input cards; no terminal
or checkpoint objects exist. Attempt `20260911T020000Z` is therefore
`invalid-no-terminal-evidence`. Its gradient-audit decision, optimizer-step
count, training status and model-quality outcome are unknown and must never be
reconstructed or reported as an executed result. Loss-evidence seal:
`a0e8097d972fbe14e1e004290b0d3acfd4e8d6f831ac1d79140185f5aa1644a6`.

The remaining named subnet and network were deleted. Two absence checks and a
wider inventory confirm zero Ganesh-named instances, disks, networks, subnets,
addresses, forwarding rules, routers, snapshots, images or machine images.
Teardown-audit seal:
`8a4d970a4be5d2a930098b8960718627e8fbefe37aceeae11e01d8652be0cbfc`.
The unrelated `laxmi-wmv2-training-01` disk remains untouched, so the account
cannot be described as GCS-only.

Local diagnosis found two finalization defects: the sealed audit-stop exit code
`2` was rejected before its evidence could be validated, and background
watchdog/checkpoint/NVML descendants inherited the FIFO logger descriptors,
which could keep `stop_loggers` waiting until provider deletion. Both defects
are fixed locally with focused regression coverage; nine focused tests and
shell syntax pass. Current state is Gate 4 / fresh rerun package required. No
Ganesh compute is active, and no rerun is authorized by the rescue approval.

## 33. Corrected rerun upload package awaiting approval — 2026-09-14

The corrected evaluation workspace and startup controller are sealed from
source commit `c01a99b81e9712e9be5d01d7a09595e8e2c65fee`. Eighteen packaging and
controller tests pass. A new upload-only plan binds five create-only objects,
7,424,694 bytes total, under unique prefix `input/c01a99b8`; plan seal:
`b3cc9c24470a0efa851c986f6dfe9125fe7c627f80f2463d887871542267c0ce`.

This plan authorizes no inspection, compute, infrastructure, training or
evaluation. Exact approval is required before upload. After upload and exact-
generation roundtrip, a fresh read-only inspection and then a separately
sealed execution proposal remain required. No Ganesh compute is active.

## 34. Corrected rerun inputs uploaded; inspection approval pending — 2026-09-14

Navneet approved upload-only plan
`b3cc9c24470a0efa851c986f6dfe9125fe7c627f80f2463d887871542267c0ce`.
All five objects were created under prefix `input/c01a99b8`, assigned immutable
generations, downloaded by exact generation and matched to their sealed sizes
and SHA-256 values. Receipt seal:
`96a76d12f8d8e5e54556514e83194e7edc4cbe9fccf7144a5c60e0d590ea9e11`.
No compute or infrastructure operation occurred.

A fresh read-only plan binds attempt `20260914T003000Z`, four new resource
names and all ten generation-pinned inputs. Its seal is
`e7b1602ca2c01b785cc5f93b9d3b8543e81affecf14c3787ce219cf2bf367c66`.
It authorizes only provider, resource-absence, IAM, input-metadata and current
price reads. Exact approval is required; it authorizes no resource mutation or
execution. No Ganesh compute is active.

## 35. Corrected rerun inspection passed; execution approval pending — 2026-09-14

Navneet approved read-only inspection plan
`e7b1602ca2c01b785cc5f93b9d3b8543e81affecf14c3787ce219cf2bf367c66`.
The four exact fresh resource names are absent; `us-east1-c` is UP;
`g2-standard-8` and `nvidia-l4` match; regional L4 quota is 16 with usage 0;
the VM service account retains bucket objectAdmin; and all ten generation-
pinned inputs match their metadata. Official prices remain USD 0.853624312 per
g2-standard-8 hour and USD 0.000136986 per pd-balanced GiB-hour. Report seal:
`be5a8cebb3b07b9c15a8fff271092bb041d8f3e2c7cef6ac4c969fc5f3ed2017`.
No cloud mutation occurred and point-in-time L4 capacity is not claimed.

Fresh non-executable proposal
`af67925bf32f28b2708862a517af58b00f161cbbd66c2c3d00db05987f98cd88`
binds attempt `20260914T003000Z`, one Standard g2-standard-8/L4 VM, 200 GiB
auto-delete balanced disk, no external IP, restart disabled, 7,200 seconds
maximum, provider upper USD 1.762043024 and absolute ceiling USD 2.25. It
retains the audit-first stop and terminal-evidence-before-teardown contracts.
Exact execution approval is required. No Ganesh compute is active.

## 36. Corrected gradient-conflict rerun active — 2026-09-14

Navneet approved exact execution proposal
`af67925bf32f28b2708862a517af58b00f161cbbd66c2c3d00db05987f98cd88`
under the USD 2.25 ceiling. Both provider-bound execution cards were uploaded
create-only and exact-generation verified. The training-card generation is
`1789357621181016`; the outer-card generation is `1789357653715057`.

The single Standard g2-standard-8/L4 VM is RUNNING with provider ID
`268054164708970511`, no external IP, restart disabled, auto-delete 200 GiB
balanced disk, and calculated provider deletion at `2026-09-14T05:50:01Z`.
The metadata wrapper completed. Current state is ACTIVE / waiting for the first
sealed runtime checkpoint. Do not claim an audit or model result until terminal
evidence is recovered and verified. Do not teardown before that verification.
