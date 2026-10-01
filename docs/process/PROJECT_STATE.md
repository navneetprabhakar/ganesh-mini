# Project state

## Final public diagnostic and local session closure — 2026-10-02 IST

The full local public MultiPL-E HumanEval assessment is complete. All 12
candidate/upstream lane runs have completed generation and executed the pinned
network-disabled verifier. The fail-closed paired report is
`artifacts/public-benchmark/full-humaneval-20261001/full-six-lane-paired-report.json`,
seal `753181b3042e5445d8e70bcba3de5a15244c9fbaa76e896deef314af64788fb2`.
It covers 952 public tasks: Ganesh Mini 338 passes, correctly served Qwen
upstream 339, with 8 paired wins and 9 losses. Per-lane candidate/upstream
passes are Go 45/43, Java 51/52, JavaScript 64/64, TypeScript 59/59,
Python 84/86, and Rust 35/35. The full report and exact public method were
published under `Executespec/ganesh-mini-1.0` at commit
`f3aa8dadc583621da8a7a9561036804b085a8d04`; the three changed files
matched remote bytes and the Q8 LFS hash was unchanged. No private
evaluation material was uploaded. This is a local public diagnostic, not an
official leaderboard result, and it does not establish model improvement.

The benchmark controller exited normally. The exact localhost tracker was
stopped, port 8765 has no listener, and no benchmark model server remains.
All raw benchmark outputs and verifier evidence remain under the ignored
local artifact directory. The earlier 30-task sample is a subset, not an
additional 180 independent tasks. The selected pilot's frozen Gate 3 quality
failure and Gate 8 NO-GO release eligibility remain unchanged; Gates 4–7
were not run, the private decision set remains unopened, and the Gate 0B
raw-report gap remains open. The user-directed public artifact is an
experimental checkpoint publication, not a gate-passed release. No GCloud
resources were used for this public run or report publication.

All benchmark-specific tests passed (11/11). The broader data/eval/train/
inference/release/benchmark test run has two failures in
`tests/inference/test_gate1_gcloud_preparation.py`: its historical sealed
evaluation workspace no longer matches the current source hash of
`scripts/campaign/run_host.py`. The fail-closed test and historical seal were
not relaxed or rewritten for closure. All other tests in that run passed;
this is an unresolved reproducibility gap, not a public benchmark failure.

The entries below are historical snapshots of the running campaign; their
PID and live-status claims are no longer current.

## Local public benchmark tracker live — 2026-10-01 IST

A read-only localhost tracker for the active full MultiPL-E run is available
at `http://127.0.0.1:8765/`. Its server is
`scripts/benchmarks/serve_public_progress.py`, restarted as PID `41434`,
exec session `26961`, bound only to `127.0.0.1`. It reads public benchmark
artifact counts and the exact controller PID `38260`; it does not execute
generated code, start model servers, or expose prompts/outputs. It now
distinguishes generated outputs, correctness tests executed, and `OK` passes
from parsed verifier results. Live pass counts are explicitly provisional;
the final paired report still requires the sealed scorer.
The page auto-refreshes every five seconds and also supports manual browser
refresh. Tests and browser verification passed. Keep the tracker process
running alongside the benchmark; if it stops, the benchmark controller is a
separate process and must not be duplicated just to restore the page.

## Full local public MultiPL-E HumanEval assessment running — 2026-10-01 IST

Navneet requested identifying runnable public benchmarks and starting a local
assessment. A single sequential full-suite controller is active in exec
session `1302`, PID `38260`, protected from idle sleep by `caffeinate -i`.
Run root: `artifacts/public-benchmark/full-humaneval-20261001`, prefix
`full-humaneval-v1`; lane order JS, TS, Rust, Python, Java, Go. It compares
the published Q8_0 checkpoint to the pinned upstream Q8_0 under the same
8,192-context/non-thinking/temperature-zero serving contract, then executes
programs only in the pinned network-disabled, resource-limited MultiPL-E
container. Full pinned task counts are 161, 159, 156, 164, 158 and 154
respectively. The Rust published stop token is applied prospectively to
full-program responses for both models. Do not start a second controller or
model server; inspect this exact process and per-lane manifests before any
recovery. The prior 30-task sample and its public report remain immutable.
No GCloud usage or private evaluation opening is involved. A full-suite
score is not yet available and must not be inferred from the earlier sample.

## Public six-lane assessment published under Executespec — 2026-10-01 IST

The user-directed public checkpoint and local paired public diagnostic are
published at `https://huggingface.co/Executespec/ganesh-mini-1.0`, commit
`86cee3536304bdd83bdc8e996ee1a489d3a71600`. Anonymous reads of the
card, method and paired report matched local SHA-256 hashes; the public Q8
LFS hash remained `f4a3a394e4551211b4de0a58ad5cea1382e5b88ff450c996f1452d3c22388d89`.
The sealed public report is
`artifacts/public-benchmark/20261001/six-lane-paired-report.json`, report
seal `9619bb5dabbf3f7d335c41a28ce52ae3db8d475d65027571caebb8a60f5efa1c`.
It covers 30 deterministic public tasks per lane: Ganesh Mini 70/180,
pinned upstream 71/180; paired 2 wins, 3 losses, 175 ties. Per-lane passes
(candidate/upstream): Go 9/8, Java 12/13, JavaScript 12/12, TypeScript
13/14, Python 18/18, Rust 6/6. This is a sampled local public diagnostic,
not an official leaderboard or an improvement claim. The original Rust
`sha30-v2` 0/30-per-side result was caused by duplicate closing-brace
assembly and remains excluded evidence; `sha30-v3` re-executed the same
saved outputs with the dataset's published stop token and is disclosed in
the method. No private assessment was uploaded. The frozen Gate 3 no-go and
Gate 8 release-gate state remain unchanged. No GCloud usage was made for
this public assessment or upload.

## Historical: public benchmark paired run active — 2026-10-01 IST

The public checkpoint and all model exports are live under Executespec.
Public assessment is now a deterministic 30-task-per-lane sample from the
pinned MultiPL-E HumanEval translations (Go, Java, JavaScript, TypeScript,
Rust) plus the pinned HumanEvalPlus Python file in the MultiPL-E repository.
This is a new public diagnostic under the user's publication direction, not
an alteration of the earlier frozen Gate 1 public-admission result.
Candidate and pinned upstream use local Q8_0 GGUF exports, the same pinned
llama.cpp non-thinking 8,192-context/temperature-zero serving contract, and
the same sample, prompt, output cap and stop-token postprocessing. Generated
programs run only in the pinned MultiPL-E image with no network and explicit
CPU, memory, PID, capability and privilege limits. The first uncorrected Go
format pilot is preserved locally and excluded from scoring. A single
sequential controller, `scripts/benchmarks/execute_public_suite.py`, is active
in exec session `59609`; inspect that process and exact per-run manifests
before restarting it. No public score has been reported or published yet.

## Public checkpoint publication directed despite Gate 3 no-go — 2026-10-01 IST

Navneet explicitly requested publishing the existing model without a
categorical failure label and using public benchmarks for subsequent
evaluation. He then specified the Executespec organization and directed that
the public card share public-assessment results, not our private development
assessment. The public repo is
`https://huggingface.co/Executespec/ganesh-mini-1.0`, with the LoRA adapter,
merged BF16, tokenizer, F16 GGUF, Q8_0 GGUF, license and card anonymously
verified at commit `5cba9d01cf4fb99e8ff1964c4877320d187c2d09`. All
remote large-file SHA-256 values matched local staging. Its current card has no
private development scores and makes no improvement claim. Earlier public
commits containing those scores were squashed out of the repo's reachable
history, though prior exposure or external caches cannot be ruled out.
This user-directed checkpoint publication does **not** change the sealed
negative Gate 3 result or the original Gate 8 NO-GO decision. Keep the
private assessment internal; publish only executed, pinned public benchmark
results. Local BF16 merge and GGUF F16/Q8 artifacts were built
from the selected `1e-5` adapter; the first converter output failed to load
because PEFT omitted the unused MTP head. A corrected `--no-mtp` target export
passed local BF16, F16 and Q8 text-only smoke. Publication staging is under
`artifacts/hf-staging/20261001-selected-1e-5`. No new GCloud usage was needed
for publication. Public benchmark evidence is pending; the MultiPL-E dataset
revision `28441b6024e71d4a1c1c0f6bf171c935cd5a43f2` and pinned local
llama.cpp are being prepared for an upstream-paired assessment.

## Work resumed after no-go closure — 2026-10-01 IST

Navneet explicitly directed continuation after the no-go closure. The
closure record remains preserved historical state, but its stop-work
instruction is superseded. Gate 3 still has a sealed quality failure; no
quality gate is waived or retrospectively passed by resuming. Continue with
local, read-only artifact and downstream-readiness checks while the intended
path is resolved: either a prospective correction toward the original gates
or an explicitly labelled failed-experiment publication scope. No new GCloud
usage, private decision-set opening, Gate 4 training, or `ganesh-mini-1.0`
release follows from the word “continue” alone.

## Project closure: no public model release — 2026-10-01 IST

Navneet stopped improvement work and directed project closure today. The
frozen Gate 3 selected pilot failed its 180-task development quality checks;
therefore Gate 3 is **not passed**, Gates 4–7 were not run, and Gate 8 model
release is **NO-GO**. Do not publish `ganesh-mini-1.0` weights, adapter, GGUF,
or a claimed improvement. The private 360-task decision set remains unopened.
The independent Gate 0B raw-report gap also remains unresolved. Closure does
not relabel any failed or incomplete gate as passed. The evidence and precise
restart conditions are recorded in
`docs/process/GANESH_MINI_1_0_NO_GO_CLOSURE_20261001.md`. The Gate 3 recurring
monitor is to be paused; no new training, candidate generation, GCloud job, or
release preparation is authorized by this closure entry.

## Gate 3 selected pilot failed frozen development quality criteria — 2026-10-01 IST

The exact selected `1e-5` 180-task development run `20261001T020646Z`
finished with evaluation exit 0. Its 375 terminal GCS objects and 167 local
control-mirror objects were independently verified; the exact VM, disk,
network, and subnet were removed and absent twice. The frozen adjudication
report at `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T020646Z/development-adjudication.json`
is sealed as `4177c8e5782481877d0de5e20b861e46886a3c93138bf2d3a8037e4cfe088cd3`
with status `quality-criteria-failed`. Against the admitted upstream 180-task
baseline, the candidate had 3 paired wins, 4 losses, 173 ties; only Python
improved at the product-family level, below the required four of five, and
Java plus TypeScript each regressed by one passed task. The candidate did not
increase malformed/non-code/repetitive/truncated output failures, and
save/reload passed, but these do not override the two failed quality checks.
**Gate 3 is not passed, Gate 4 training and model publication remain blocked.**
The 360 private decision tasks remain closed. Preserve both candidates and all
failed evidence. Do not rerun a candidate or relax criteria; the frozen plan
requires a prospective data or mechanism change before scaling, with a new
bounded evaluation plan and budget check before further GCloud use. The older
Gate 0B raw-report recovery gap remains an independent release hold.

## Gate 3 selected-adapter 180-task VM active — 2026-10-01 IST

After four backed-up/cleaned pre-allocation L4 stockouts, exact development
attempt `20261001T020646Z` allocated one `g2-standard-8` L4 VM
`ganesh-g3-eval-20261001t020646z` in `us-central1-c`. Sealed card
`24569f6a90742f23502d3e55c0c8c3ead6908d393d4e4de7b4a0fa8723c36451`.
Provider RUNNING began 2026-10-01T02:12:52Z under two-hour STOP. Exactly one
watcher, PID `82840`, started 02:13:29Z. **Do not allocate another VM or
start a second watcher.** This is the selected `1e-5` adapter against all 180
frozen private development tasks, with decision tasks still closed. Prior
conservative allocated reserve is $5.00; card's two-hour plus staging and
support bound is $13.263870928 under $15, with repeated pre-allocation
transfers to be reconciled. No development quality verdict exists yet.

## Gate 3 development retry in `us-central1-c` — 2026-10-01 IST

Selected `1e-5` development requests in `us-central1-a`, `us-east1-b/c/d`
all returned pre-allocation L4 stockouts. Each exact attempt has a verified
78-object GCS refusal backup, cleaned temporary network/subnet, and exact
VM/disk/network/subnet absence twice. No 180-task result exists; conservative
allocated prior reserve remains $5.00. One sequential preparation is now
active at `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T020646Z`
in approved `us-central1-c`. Do not duplicate it. Repeated transfer/operations
remain under the retained support allowance but must be counted within the
$15 absolute ceiling. Gate 3 and release remain open.

## Gate 3 development fourth sequential capacity attempt — 2026-10-01 IST

Three selected-adapter development VM requests (`20261001T011522Z` in
`us-central1-a`, `20261001T012619Z` in `us-east1-b`, and `20261001T014614Z`
in `us-east1-c`) each hit pre-allocation L4 stockout. Each refusal has a
78-object independently verified GCS control backup and exact VM/disk/network/
subnet absence twice. No development tasks ran. One sequential preparation is
active at `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T015703Z`
in approved `us-east1-d`; do not duplicate it. Conservative allocated prior
reserve remains $5.00; account repeated transfer/operations under the $15
absolute ceiling before any further retry. Gate 3 quality remains open.

## Gate 3 development retry in provider-suggested zone — 2026-10-01 IST

The selected `1e-5` 180-task development attempts `20261001T011522Z`
(`us-central1-a`) and `20261001T012619Z` (`us-east1-b`) both received
pre-allocation L4 stockouts, not quality results. Each exact refusal has a
78-object independently verified GCS control backup and VM/disk/network/subnet
absence checked twice after cleanup. Prior conservative allocated reserve
remains $5.00. A single sequential preparation is active at
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T014614Z`
in approved, provider-suggested `us-east1-c`. Do not duplicate it. Gate 3
quality and Gate 8 release remain open; decision tasks stay closed.

## Gate 3 development capacity retry — 2026-10-01 IST

Selected-adapter `1e-5` development attempt `20261001T011522Z` got a
pre-allocation `g2-standard-8` L4 stockout in `us-central1-a`. Its 78 refusal
control objects were independently downloaded/hash-verified before exact
subnet/network cleanup; VM, disk, network, and subnet absence passed twice.
No development task ran. Conservative allocated prior reserve remains $5.00.
One sequential replacement preparation is now active at
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T012619Z`
in approved `us-east1-b`. Do not duplicate preparation, VM, or watcher.
The 30-task canary selected `1e-5` only for 180-task development; Gate 3
quality remains open and the decision set remains closed.

## Gate 3 selected-adapter development preparation — 2026-10-01 IST

The v2 canary VM `20261001T002557Z` completed both frozen 30-task runs with
evaluation exit 0. All 136 terminal GCS objects and 140 local control objects
were independently downloaded/hash-verified; exact VM, disk, network, and
subnet absence passed twice. The sealed selection report
`1eb78aa5949923013b6d5fe776a3648ed9f3d1b707574391b949c6e632fb9331`
finds upstream and both adapters at 5/30 with identical lane totals, so the
frozen conservative rule selects `1e-5` **only for full 180-task development**.
This is not a Gate 3 quality pass. Selected evaluation staging is sealed at
`measurement/gate3/capability-scale-v1/full-pilot-eval/candidate-staging-selected-v1`,
card `477d0c069fc4f913a9d698b1039d65106e6d70471691cb0c051a21e8255c324e`.
One sequential development preparation is active at
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T011522Z`
in `us-central1-a`. Do not duplicate it. Prior conservative allocated reserve
is $5.00; the unchanged $15 ceiling and decision-set closure remain binding.

## Gate 3 two-adapter canary VM active — 2026-10-01 IST

The sequential v2 retry `20261001T002557Z` allocated one `g2-standard-8`
L4 VM `ganesh-g3-eval-20261001t002557z` in `us-central1-a` under sealed card
`4e2cc2cf9f7fb5561dd2abfe4f9c6eb6e1871c0075add60d25239a038ccb5539`.
Provider RUNNING began 2026-10-01T00:36:53Z with two-hour STOP. Exactly one
watcher, PID `26066`, started at 00:37:28Z. **Do not duplicate the watcher or
allocate another VM.** It must independently verify all terminal GCS evidence
before exact teardown and double absence. The preceding v2 zone stockout is
finalized, backed up, and resource-absent. The prior conservative cost reserve
is $4.00; this attempt's two-hour plus support and staging upper bound totals
$12.263870928 under the unchanged $15 ceiling. No canary quality result or
Gate 3 pass exists yet; the 360-task decision set remains closed.

## Gate 3 sequential canary capacity retry — 2026-10-01 IST

Both full-epoch training candidates remain sealed. The v2 canary attempt
`20261001T000513Z` reached `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` in
`us-central1-b` before VM allocation. Its bounded refusal controls were
independently downloaded and hash-verified; the exact VM, disk, network, and
subnet are absent on two post-cleanup checks. The refusal is not a candidate
quality result. Under the unchanged approved plan SHA
`d4659d3b503d4eb0a0a38d5af6129f668ccef7994a7f678e920ced1a5e55dd09`
and $15 absolute incremental ceiling, one sequential replacement preparation
is running at `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T002557Z`
in `us-central1-a`. Do not duplicate preparation, VM, or watcher. Gate 3
quality is still open; the private 360-task decision set remains closed, and
Hugging Face release remains held by Gates 4–8 and the Gate 0B raw-report gap.

## Gate 3 canary replacement inputs preparing — 2026-10-01 IST

The failed first canary's terminal backup, exact double resource absence and
clean `local-evidence-controls-v2` mirror are independently verified: 135
control objects matched local SHA-256 inventory. The first mirror's exclude
syntax had copied redundant roundtrips and timed out; that partial prefix is
preserved, not used as the control seal. A prospective provider v2 pins and
overlays the single missing materializer dependency into the ephemeral
evaluation-only tree; 29 focused evaluation tests and local import rehearsal
pass. A sequential new canary preparation is active at
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T000513Z`
in `us-central1-b`, under the unchanged approved $15 ceiling and $4.00 prior
reserve. **No new VM has allocated yet.** Do not duplicate preparation or
start another attempt. Gate 3 quality and release remain open.

## Gate 3 canary startup stopped before evaluation — 2026-10-01 IST

The one allocated canary attempt `20260930T231842Z` terminated with startup
exit 1 before model loading or any canary result. All pinned inputs downloaded
and hash-checked on host, and the 587-file evaluation workspace plus adapter
overlay passed verification. The model materializer then failed because its
hash-pinned `scripts.train.preflight_gate3_capability_pilot` dependency was
not included in the separate evaluation workspace. The later `docker: command
not found` message came from exit cleanup and is secondary. This is a launcher
packaging defect, **not a candidate quality result**. Eight terminal GCS
objects were independently downloaded/verified; `finalization.json` records
terminal backup and exact VM/disk/network/subnet absence twice. A single
watcher is still mirroring local control evidence to GCS; do not allocate
another VM until it ends and the failure is fully reconciled. The immutable
failed card seal is
`08ed09f4362a6bd293a488c63e47ac2971b224635d08e5afadfcc31bbe7a1b17`.
The conservative allocated cost reserve is $0.75, bringing accounted prior
reserve to $4.00 under the unchanged $15 absolute ceiling. The watcher then
timed out while redundantly mirroring the 876-MB local verifier roundtrip;
this happened **after** terminal backup, finalization and double absence.
Fresh project-wide checks again found no VM or disk and only the default
network. A targeted control-evidence mirror (excluding already pinned or
terminal-backed large roundtrips) and a prospective one-file dependency
correction are being tested. The failed attempt will not be rewritten or
counted as canary evidence.

## Gate 3 two-adapter canary VM allocated — 2026-10-01 IST

The approved $15 full-pilot plan now has one evaluation-only canary attempt at
`measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20260930T231842Z`.
The sealed execution card is
`08ed09f4362a6bd293a488c63e47ac2971b224635d08e5afadfcc31bbe7a1b17`.
After an interrupted large input transfer and a launch-path correction, its
single `g2-standard-8` L4 VM `ganesh-g3-eval-20260930t231842z` allocated in
`us-central1-b`. One watcher (PID `1714`, exec session `19974`) started at
2026-09-30T23:41:01Z. Do not duplicate the VM or watcher. The provider has a
two-hour STOP; the watcher must independently verify complete terminal GCS
evidence before exact teardown and double absence. Both 30-task candidate
canaries are intended to run sequentially in this evaluation-only workspace.
No executable quality result or Gate 3 pass is yet established. Keep the
360-task decision set closed, preserve all evidence, and leave Gate 0B and
Gates 4–8 as release holds.

## Gate 3 candidate evaluation inputs prepared locally — 2026-10-01 IST

The fail-closed local staging generator bound both sealed full-epoch runs,
adapter file hashes, 54-object terminal backups, the separate 180-task
workspace and all 30 frozen canary task hashes. It emitted two canary configs
and an evaluation-only adapter bundle under
`measurement/gate3/capability-scale-v1/full-pilot-eval/candidate-staging-v1/`.
The `prepared-only` card seal is
`2c2ead6df00e2e9769ee1562216d8d6340b1d99ad1f079ec6bee9dceb502a8ff`.
This is **not** an executable provider card or a quality result. A separate
GCloud evaluation controller, runtime/verifier preflight, bounded budget,
terminal backup and exact teardown contract must pass before allocation.

## Separate Gate 3 evaluation workspace locally sealed — 2026-10-01 IST

The checked-in development-only packager produced
`measurement/gate3/capability-scale-v1/full-pilot-eval/evaluation-workspace-v1.tar.gz`
and manifest seal
`8ed2f45d87b3b867a59c6eca03be6e9d991bd1070037bd52311ed63a07585edc`.
It contains 587 allowlisted files and exactly 180 development tasks, with
no training artifacts, seed rows, or private decision tasks. This is local
workspace preparation only; no candidate canary or development inference
has run. An evaluation execution card, verified adapter binding, runtime
and terminal evidence are still required before Gate 3 quality can be judged.

## Both Gate 3 LR epochs complete; executable quality pending — 2026-10-01 IST

The frozen second `3e-5` attempt `20260930T220936Z` completed all 900
unique rows, 651,639 input tokens and 113 optimizer steps with training exit
0. Adapter save/reload passed at zero maximum logit difference. The verified
run-evidence seal is
`19daa16303a72a195329cc1bf06984f12414d76a1dc85e343f25bafe94f86ed2`.
Its one watcher independently downloaded and verified 54 terminal GCS
objects, then deleted exact VM/disk/network/subnet and checked absence twice.
Fresh project-wide VM/disk/address inventories are empty; only the default
network remains. The first `1e-5` candidate is separately sealed under
`21d78a7e339fb75dd89bdd9ada83a53bdbb10678bd7c3c9b09d182786b698537`.
Both training lifecycles passed, **not Gate 3 model quality**. Next seal a
separate evaluation workspace, run the frozen 30-task canary on each adapter,
select by the existing no-regression rule, then run 180 development tasks on
the selected adapter. Do not open the 360-task decision surface. Gate 0B raw
report recovery, Gates 4–8 and Hugging Face release remain downstream.

## Second Gate 3 LR allocated with one watcher — 2026-10-01 IST

After independently backed and double-absence-finalized pre-allocation
stockouts in `us-central1-c` (`20260930T220004Z`) and `us-east1-c`
(`20260930T220454Z`), the unchanged `3e-5` candidate
`20260930T220936Z` allocated `ganesh-g3-pilot-20260930t220936z` in
`us-east1-b`. Card seal is
`f629892c135020cf9e7dbca75ae8442b25b5b9be274df30ce4ad794699de3ad9`.
Provider RUNNING began 2026-09-30T22:12:20Z with a two-hour STOP. Exactly
one watcher, PID `88102` / exec session `63139`, started 22:12:26Z. Do not
launch another watcher or VM while it is active. On termination, let the
watcher independently verify complete GCS backup before deleting exact
VM/disk/network/subnet and checking absence twice. The first LR passed its
full training epoch/save-reload lifecycle; no second LR result or Gate 3
model-quality pass yet. The $15 ceiling and conservative $3 prior reserve
remain in force.

## Second LR first capacity refusal — 2026-10-01 IST

The frozen `3e-5` attempt `20260930T220004Z` staged with card seal
`e297d127086e1a0572ea2a913ff6100967b8118a2f734597936c59d02aec4316`
but `us-central1-c` returned a pre-allocation L4 stockout. Its refusal was
backed to GCS, independently downloaded and verified; exact resources were
cleaned and absent twice (`refusal-finalized`). No second LR optimizer step
or GPU runtime occurred. A sequential retry may proceed only after the same
resource and budget checks; the first LR's sealed result remains unchanged.

## First Gate 3 LR full epoch sealed; second LR staging — 2026-10-01 IST

Corrected `1e-5` attempt `20260930T205829Z` completed its unique 900-row,
651,639-input-token epoch: 113 optimizer steps, training exit 0, and adapter
save/reload passed with zero maximum logit difference. Its run-evidence seal is
`21d78a7e339fb75dd89bdd9ada83a53bdbb10678bd7c3c9b09d182786b698537`.
The single watcher independently verified all 54 terminal GCS objects before
deleting exact VM/disk/network/subnet and confirming absence twice. Project
VM/disk/address inventories are empty and only the default network remains.
The fail-closed prior-allocation check admitted the frozen second `3e-5` LR
with a conservative $3 prior-cost reserve inside its $6 candidate slice and
the $15 absolute incremental ceiling. This is a training-lifecycle result,
**not** a Gate 3 model-quality pass: both-candidate canary, selected-candidate
development evaluation, Gates 4–8, and Gate 0B raw-report recovery remain.

## Corrected first LR L4 allocation running — 2026-10-01 IST

Scheduled attempt `20260930T205829Z` in `us-central1-c` allocated
`ganesh-g3-pilot-20260930t205829z` for the corrected `1e-5` candidate.
Execution card seal is
`8133a95f3fde266a36cde45d0792f574c930c926519953f25c692bec42e32744`.
One watcher, PID `72123` / exec session `49372`, started at 21:01:30Z;
provider status was `RUNNING` with VM start 21:01:20Z. Do not duplicate
watcher or allocation. Provider STOP is two hours. The card carries the
conservative $0.75 reserve from the prior paid pre-training failure within
the $3 candidate slice and $15 overall ceiling. No optimizer step or full
epoch is verified yet. Watcher must independently verify terminal GCS backup
before deleting exact VM/disk/network/subnet and confirm absence twice.
Gate 3 quality, Gates 4–8 and Gate 0B raw-report recovery remain open.

## Scheduled capacity check unchanged — 2026-10-01 IST

Attempt `20260930T202822Z` staged the corrected `1e-5` candidate in
`us-central1-a` but received pre-allocation L4 stockout. Its GCS refusal
backup was independently verified, exact resources were absent twice, and
project VM/disk/address inventories remain empty. No additional GPU runtime
or training result. The prior conservative $0.75 reserve and overall $15
ceiling remain; the 30-minute continuation stays active.

## First allocated Gate 3 pilot stopped before training; backed and cleaned — 2026-10-01 IST

Attempt `20260930T192827Z` ran one L4 for 808 seconds and stopped with startup
exit 1 before an optimizer step. Its actual-host 16-row probe **passed** at
314.457 input tokens/s, and the GCloud provider/card binding passed. The
training CLI then rejected a validation-file path that differed from the
frozen config: startup passed `artifacts/train/gate3-capability-pilot-v2/prepared-validation.jsonl`
while config pins `artifacts/train/expansion-pilot-v1/prepared-validation.jsonl`.
The latter exists in sealed workspace-v8 and matches its pinned SHA256
`6a9d3aa37b30bc2672517f6d63113011de5f8156aa1049e588fdc70a36b77f46`.
No training result or model-quality result was produced. The watcher verified
all 17 terminal GCS objects independently, then deleted exact VM/disk/network/
subnet and confirmed absence twice. Project VM/disk/address inventories are
empty. The failure remains immutable.

The startup argument alone was corrected prospectively and covered by a
regression test; workspace-v8 and plan SHA are unchanged. The retry controller
now derives a conservative $0.75 prior-cost reserve from the sealed provider
runtime, $0.50 transfer and $0.05 operation allowance, and requires prior
backup/teardown evidence before admitting a retry within the candidate $3
slice and overall $15. Corrected attempt `20260930T200133Z` staged but got
pre-allocation L4 stockout in `us-east1-c`; its GCS refusal is independently
verified and exact resources absent twice. No VM is currently running. The
30-minute automation remains active for one sequential bounded retry at a
time. Gate 3 quality, Gates 4–8 and Gate 0B raw-report recovery still block
Hugging Face release; ETA depends on L4 capacity and subsequent gate results.

## Full Gate 3 first LR VM allocated; one watcher active — 2026-10-01 IST

After seven clean pre-allocation stockouts, the scheduled `us-east1-c`
attempt `measurement/gate3/capability-scale-v1/full-pilot-gcloud/20260930T192827Z`
allocated `ganesh-g3-pilot-20260930t192827z` for the unchanged `1e-5`
candidate. Execution card seal is
`11547ac26ad5831bb6f6cbd021cc7329e7c821a57c0ed5c828297a5050296085`.
One controller watcher was started in exec session `5732`; the first provider
status was `RUNNING` at 2026-09-30T19:30:41Z and startup serial output showed
normal boot/network initialization. Do not start another watcher or VM while
this allocation exists. Provider STOP is two hours. No actual-host probe,
optimizer step, full epoch or quality result is yet verified. The watcher must
independently download/hash terminal GCS evidence before resource deletion and
double-check exact absence. The $15 incremental ceiling remains; this
allocation consumes a conservative $1.762043024 VM+disk upper plus transfer
reserve, regardless of outcome. Gates 3–8 and Gate 0B raw-report recovery
still block HF release.

## Scheduled L4 capacity retry: seventh clean stockout — 2026-10-01 IST

The first 30-minute continuation revalidated all six prior refusal seals,
plan/workspace hashes, CLI project and empty project compute inventories.
Attempt `20260930T185836Z` retried `us-central1-b` for the unchanged `1e-5`
candidate and again received pre-allocation
`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`. Its GCS refusal backup was
independently verified; exact VM/disk/network/subnet absence passed twice.
Another project-wide check found no VM, disk or reserved address and only
the default network. No training occurred, no GPU runtime cost was incurred,
and the $15 ceiling remains in force; GCS operation/storage charges may exist.
The same-task 30-minute retry automation remains active. Gate 3 quality and
Hugging Face release remain blocked.

## Full Gate 3 VM pilot approved; six L4 capacity refusals — 2026-09-30

Navneet approved plan SHA256
`d4659d3b503d4eb0a0a38d5af6129f668ccef7994a7f678e920ced1a5e55dd09`
and its $15 absolute incremental GCloud ceiling, and authorized retries
without re-asking while within budget. Training candidate `1e-5` was staged
and sequentially requested in `us-central1-b`, `-c`, `-a`, then `us-east1-c`,
`-b`, `-d`. All six returned `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`
**before VM allocation**. Each attempt has its own immutable execution card,
GCS refusal backup, independent two-download verification, exact cleanup,
and double resource-absence finalization under
`measurement/gate3/capability-scale-v1/full-pilot-gcloud/`. Two further
project-wide inventories showed instances, disks and reserved addresses empty;
only the default network remains. No full training token was processed and no
Gate 3 quality result exists. GCS storage/operations may incur small charges;
do not call the entire effort free or claim a live billing invoice.

The same `g2-standard-8` L4 has the same published $0.853624312/hour price in
both US regions, so the fixed $0.881021512/hour VM+disk STOP bound and $15
ceiling remain unchanged. No larger GPU or altered recipe was used. A same-task
30-minute capacity retry automation, `ganesh-mini-gate-3-capacity-retry`, is
active and must stay quiet on unchanged stockout. It must reconcile all prior
resources and budget before another sequential attempt. Gate 3 and Gates 4–8
remain open; historical Gate 0B raw-report recovery still holds release.

## Full Gate 3 VM controller locally sealed; spending ceiling pending — 2026-09-30

The user requested VM execution as soon as feasible. The prospective full-pilot
plan is `docs/plans/GATE3_FULL_PILOT_GCLOUD_EXECUTION_20260930.md`, SHA256
`d4659d3b503d4eb0a0a38d5af6129f668ccef7994a7f678e920ced1a5e55dd09`.
Its **new $15 absolute incremental ceiling has not yet been accepted**. Do not
prepare, upload, inspect GCloud, or allocate against that plan until it is.
The prior $5 authorization was qualification-only and is closed.

Local training-only `workspace-v8.tar.gz` is sealed at
`a9eee2d31de0cf3728d10c8ee5652615006df83dbb371cf942a4e4ee79a036d8`.
The new prospective one-candidate-per-VM controller and startup path implement
actual-host throughput/card binding, a two-hour provider STOP, periodic
checkpoint upload, terminal GCS backup, independent two-download verification,
backup-before-delete and double exact resource-absence checks. Nineteen focused
tests, shell syntax, and diff whitespace checks pass; the path has **not been
live executed**. The second LR is blocked unless the first has a verified,
sealed 651,639-token full-epoch report with save/reload pass. The separate
evaluation workspace/controller is still outstanding. No full candidate or
quality evaluation has run. Gate 3 remains open, Gates 4–8 and the historical
Gate 0B raw-report recovery remain release holds. Do not publish the model.

## Full Gate 3 VM pilot requested; local execution path under construction — 2026-09-30

Navneet requested VM execution to accelerate Hugging Face publication. The
previous $5 GCloud approval covered qualification only and is consumed; no
new VM has been created under this request. A versioned prospective full-pilot
scope and $15 incremental ceiling is recorded in
`docs/plans/GATE3_FULL_PILOT_GCLOUD_EXECUTION_20260930.md`; its ceiling is not
yet accepted. The new fail-closed GCloud provider binding and runner checks
have focused local tests, and a 73-file evaluation-free workspace is sealed
as `workspace-v6`, archive SHA
`4473c7decea8ec7b2649a9b4e9f4cdfb0e3e78d657c2b505f7e1efc1cfa85d1d`.
This is not a runnable full-pilot controller: actual-host card creation,
periodic checkpoint backup, terminal verification/teardown, and separate
evaluation orchestration still need implementation and tests. No full
candidate epoch or executable quality evaluation has run. Gate 3 remains
open; publication remains blocked by Gates 3–8 and the Gate 0B raw-report
recovery gap.

## No live VM; local full-pilot readiness assessed — 2026-09-30

Navneet asked to save artifacts, kill any VM, and continue locally. Fresh
`executespecv1` inventories returned no instances, disks, or reserved
addresses; only the default network remained. The prior qualification's 12
terminal GCS objects are still present, and its independent verified backup
and double resource-absence finalization remain intact. Nothing was deleted
because no Ganesh VM or related temporary resource existed. Local static
preflight passed 900 training rows, 651,639 input tokens, and 50 validation
rows; draft card remains intentionally non-executable on Darwin/no CUDA.
Focused tests passed. See
`docs/plans/GATE3_POST_QUALIFICATION_LOCAL_READINESS_20260930.md` for the
measured-throughput estimate and GCloud-specific full-pilot implementation
gaps. No full candidate training, canary, or development evaluation occurred;
Gate 3 remains open. No new GCloud allocation is authorized by this check.

## Gate 3 L4 qualification passed and fully finalized — 2026-09-30

The single approved allocated retry `20260930T131906Z` completed the exact
16-longest-unique-row, two-optimizer-step throughput probe, exit 0. The
hash-sealed `terminal-roundtrip/output/throughput.json` reports `passed`,
finite loss, 37,480 input tokens in 113.691 training seconds (329.666 input
tokens/second), 4,634,705,920 peak-VRAM bytes, and no retained adapter.
Its preceding hardware preflight passed on one BF16-capable NVIDIA L4 with
23,659,151,360 CUDA-visible bytes against the approved 23,622,320,128-byte
floor. The report seal is
`380c96b93ba1b7d8272c8e1c04823432309610b0cc21e6e4afb71f7a456a9b47`.
The pinned model revision, prepared train hash, manifest, and recipe hashes
match the execution report. This is qualification, not model quality.

The watcher independently verified all 12 terminal GCS objects, runtime file
hashes, and exit code before deleting the VM/disk/network/subnet. Exact
resource absence passed twice; project-wide VM, disk, and reserved-address
inventories were empty afterward. Provider RUNNING interval was 695.234
seconds, within the two-hour STOP bound. The same cumulative $5 ceiling and
$2.50 conservative prior-use reserve remain; this allocated retry is consumed
and no further GCloud allocation is implied. Data admission remains 900/900,
but no full Gate 3 model-quality pilot has run, Gates 4–8 remain open, and HF
model release is blocked. The historical Gate 0B raw-report recovery gap is
also unresolved. Next local work: bind actual-host throughput into a bounded
full-pilot card and its two LR candidates; any new GCloud usage needs a fresh
explicit scope and budget approval. Do not treat the qualification as Gate 3.

## Gate 3 L4 retry RUNNING under one watcher — 2026-09-30

CLI authentication was restored for `admin@executespec.ai` in `executespecv1`.
Preallocation project inventories showed no VMs, disks, or reserved addresses;
only the default network/subnets remained. The exact approved plan and all
local provenance file hashes matched. The first bounded zone,
`us-central1-a`, refused capacity without a GPU allocation; attempt
`20260930T131318Z` has independent GCS backup and verified exact resource
absence twice. Its zero-runtime refusal permitted a zone change.

The next bounded zone, `us-central1-b`, allocated the ONE approved L4 retry:
`ganesh-g3-qual-20260930t131906z`, evidence directory
`measurement/gate3/capability-scale-v1/gcloud-qualification/20260930T131906Z`,
execution card seal `e37df182b74d65b5629ad01afd434afa797132f8c98d0c07a237efaa217f3045`.
Watcher PID `10161` started at `2026-09-30T13:21:16Z`; the first provider
status was RUNNING. Do not duplicate the watcher or allocation. The same
cumulative $5 boundary includes a $2.50 conservative reserve for all three
prior allocated attempts. This allocation consumes the additional-start
permission regardless of probe outcome. No throughput or optimizer result is
yet verified, no full quality pilot has run, and HF release remains blocked.
The watcher must verify complete terminal GCS backup before teardown and
double-check exact absence. The Gate 0B raw-report recovery gap remains.

## Gate 3 L4 retry locally staged; GCloud CLI reauthentication required — 2026-09-30

The 22-GiB usable-floor change was approved and locally implemented. Fifty-seven
focused tests, shell syntax, workspace-v4 sealing and three-prior-attempt budget
binding pass. Local source provenance is sealed at
`measurement/gate3/capability-scale-v1/usable-floor-retry-v1/local-provenance-manifest.json`,
seal `7a5280d6053fcf2341003347df8ba1b49b6e1448257812487605c3531df49770`.
The first read-only preallocation `gcloud compute instances list` failed because
CLI token refresh requires interactive `gcloud auth login`. No new VM, disk,
network or qualified GPU probe was created by this turn. Preserve the same $5
cumulative ceiling and all prior attempts; do not bypass authentication or
claim resource absence was rechecked today. Await Navneet's login confirmation,
then verify current project resources before any allocation. Gate 3 remains
open, current probe still has zero optimizer steps, and HF release is blocked.

## Gate 3 L4 usable-floor retry approved; preallocation checks — 2026-09-30

Navneet approved plan SHA
`3bee60eb0987eccd8147d638b31beb5f4322539c32f68537b6c06d2943573de7`.
The qualification, later SFT actual-host check, and card builder now share an
explicit L4 22-GiB CUDA-visible/BF16/single-device contract; other GPU classes
retain the 24-billion-byte floor. The preflight writes separate sealed operands
before model load, including failure. Workspace-v4 is 73 evaluation-free
files; seal `93441a457ed91769ae52bdc497a0b001021f75f088c6496b5ec1b2b99b34bae1`.
Fifty-seven focused tests, shell syntax, source diff, real prior-attempt binding,
and workspace-manifest checks pass. No new VM has been allocated yet. One
allocation maximum, same cumulative $5 with $2.50 prior reserve. Gate 3 still
has no current optimizer result. Raw Gate 0B report recovery remains unresolved
and blocks final release evidence.

## Retry requested; hardware-floor clarification required before allocation — 2026-09-29

Navneet said “ok try again.” No new VM has started. Repeating workspace-v3
unchanged would repeat its literal 24-billion-byte CUDA guard. The prospective
clarification is `docs/plans/GATE3_L4_USABLE_MEMORY_RETRY_20260929.md`: same
nominal L4 class, explicit 22-GiB usable-memory floor and BF16, separate operand
diagnostics, unchanged recipe/data/quality gates, same cumulative $5 carrying
all three prior starts. The floor interpretation still needs explicit direction;
do not silently reduce the frozen hardware floor or allocate another failed run.
The admitted passed Gate 0B summary remains local, but its original pinned raw
report is not currently recoverable from the recorded GCS URL, current object,
historical prefix or all-version lookup. Related archive roots checked did not
yield a replacement. Do not claim universal loss or reconstruct missing raw
evidence. Raw-evidence recovery is now an additional release-readiness gap.
Current qualification has zero optimizer steps. Gate 3 is open; release blocked.

## Gate 3 qualification stopped at GPU preflight; finalized — 2026-09-29

Attempt `20260929T133600Z` exited 1 before model loading or optimizer steps.
Canonical materialization passed on the VM: all 13 upstream files, seal
`fe540d05ffa45b1392b87d83885dda21d9598a6dc6b7f2b19a126b088bd98402`.
The intended probe stopped at its combined BF16 / 24,000,000,000-byte CUDA
memory guard. It did not record the actual CUDA memory or BF16 operands;
do not claim a measured OOM, unsupported BF16, throughput or model-quality result.
Host nvidia-smi showed one L4, 23,034 MiB total and 471 MiB reserved. Historical
L4 CUDA observations had 23,659,151,360 bytes and a 22-GiB historical recipe
floor, so nominal-versus-usable memory is a supported mismatch hypothesis,
not a new current-device measurement. Reconcile prospectively before compute.
All ten terminal objects passed independent downloads and runtime inventory.
VM/disk/network/subnet were deleted and absent twice; project VM/disk/reserved
address inventories were empty. Watcher session 21750 completed successfully.
The one allocated correction exception is exhausted; no new paid retry.
Gate 3 remains open; 900-row data admission is unchanged and release is blocked.

## Gate 3 corrected qualification RUNNING; one watcher — 2026-09-29

The approved canonical-input exception allocated
`ganesh-g3-qual-20260929t133600z` in us-central1-a. Evidence directory:
`measurement/gate3/capability-scale-v1/gcloud-qualification/20260929T133600Z`.
Card seal `f5a61b95a48fddf25e941613446d3e82ff259120dabb19e096f4abee542d21d5`.
Watcher PID 85859 / exec session 21750 started 13:37:58Z; it verifies terminal
inventory and independent GCS downloads before exact teardown and double
absence. Do not duplicate a watcher or allocation. This allocated start consumes
the exception; failure does not permit another paid retry. Same cumulative $5,
$2 prior reserve, pinned materializer and evaluation-free workspace-v3.
Forty-nine focused tests pass; implementation provenance is backed to GCS.
Startup is running; no throughput result or model-quality pass yet. Gate 3
remains open; no full pilot or HF release is authorized by this qualification.

## Gate 3 canonical-input exception approved; staging qualification — 2026-09-29

Navneet approved proposal SHA
`0cb94af6f12bae840c6657c7d7f6402759b0313d7301b81c96afcb9fb5fb342e`.
The launcher now binds both prior paid starts and $2 prior reserve within the
same cumulative $5, and prevents another allocated retry under this exception.
Startup uses a separately hash-pinned CPU canonical materializer before the
unchanged offline CUDA probe. Forty-nine focused tests pass; shell syntax,
actual historical evidence binding and diff checks pass. No new VM is launched
yet, no optimizer step or quality result exists. Current work: staging one
qualification in bounded US regions. Preserve historical attempts and seals.

## Gate 3 metadata remedy verified locally; prospective paid exception pending — 2026-09-29

The exact model archive passed full CPU byte verification: 13 canonical files,
47 AppleDouble sidecars and 29 bounded Hugging Face download-cache files.
Canonical-only materialization was executed on the real archive and passed the
unchanged model inventory checker (13 files). Forty-five focused tests pass.
All paid starts/refusals are backed, deleted and absent twice; there is no live
VM, disk or reserved address in the inspected project inventories. No model
load, optimizer step or current throughput measurement occurred.

The prospective exception is
`docs/plans/GATE3_CANONICAL_MODEL_MATERIALIZATION_RESCUE_20260929.md`, SHA-256
`0cb94af6f12bae840c6657c7d7f6402759b0313d7301b81c96afcb9fb5fb342e`.
It proposes one further allocated qualification start after wiring the tested
canonical materializer, with $2 prior-spend reserve within the SAME cumulative
$5 ceiling. It is not approved; do not launch another paid start under the
exhausted one-rescue contract. No corpus, recipe, teacher-cap, evaluation or
quality-gate concession. Gate 3 remains open; HF release remains blocked.

## Gate 3: second preprobe failure finalized; CPU archive diagnosis — 2026-09-29

`gcloud-qualification/20260929T114450Z` reached the intended throughput script,
but exact model-directory inventory rejected archive extras before model load
or optimizer steps. Its terminal backup passed independent verification, all
temporary resources were deleted, and absence passed twice. Project instance,
disk and reserved-address lists are empty. No qualification throughput exists.
The local cached archive matches the exact pinned GCS object SHA-256. Partial
header inspection showed AppleDouble sidecars; full archive listing also shows
Hugging Face download-cache metadata. A CPU byte verifier is checking all 13
canonical upstream files and classifying excluded metadata. Do not relax the
model inventory or count this as a quality result. No more paid chained
startup retries under the current execution contract; resolve prospectively.
The admitted 900-row corpus, 1,060/1,200 draft count and evaluation separation
are unchanged. Gate 3 remains open; public model release is still blocked.

## Gate 3: corrected startup rescue launching in recommended zone — 2026-09-29

Current attempt `gcloud-qualification/20260929T114450Z` launched successfully in
us-central1-a, card seal `464bb74ce4eda39dcc939d8da5ff920202f6a3c57afccf0aac1af036cd0e4ce1`.
VM `ganesh-g3-qual-20260929t114450z` is RUNNING. Bounded watcher PID 75202 /
session 17524 handles verified terminal backup and cleanup. Thirty-seven
focused tests pass. Never duplicate that VM, watcher or finalizer while live.
The previous corrected us-central1-b capacity refusal is completely finalized.
The first paid startup failure and all capacity-refusal evidence remain
immutable and backed up. No training-only probe has executed. Preserve the
$1 prior-spend reserve and cumulative $5 ceiling; no chained paid startup
rescues or full quality pilots. Do not duplicate a pending/running allocation.

## Gate 3: preprobe launcher failure preserved; entrypoint correction — 2026-09-29

The us-central1-b VM loaded the pinned image, but its historical image
entrypoint invoked missing `scripts/cuda/qualify.py` instead of the intended
training-only throughput probe. Exit 2 occurred before any training steps or
throughput measurement. It stopped automatically; complete terminal backup
verification and exact cleanup completed, with resource absence checked twice.
The corrected bootstrap rescue at `gcloud-qualification/20260929T114020Z`
was refused for capacity in us-central1-b, without GPU runtime. Its refusal
backup/cleanup is running. Google explicitly suggested us-central1-a as
currently available; try that only after verified refusal finalization, keeping
the same $1 prior-cost reserve and the same cumulative $5 ceiling.
The watcher exited because the
serial endpoint became unavailable after STOP; authoritative VM status was
TERMINATED. The inspector now treats serial as best-effort and skips stopped
VMs; startup explicitly overrides the old entrypoint with `python3`.
Thirty-five focused tests pass, including exact entrypoint command checking.
One prospective bootstrap-only rescue may proceed only after verified teardown,
under the same cumulative $5 ceiling with a $1 prior-cost reserve and no
chained paid retries. This is not a second trained/measured probe. Preserve all
failed attempt evidence. Gate 3 remains open, no model-quality result exists.

## Gate 3: L4 qualification VM launched in us-central1-b — 2026-09-29

Attempt `gcloud-qualification/20260929T112030Z` received the exact
`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` response. No GPU runtime or model
measurement occurred. Its refusal backup, cleanup and double absence checks
are complete. The current attempt is `gcloud-qualification/20260929T112530Z`
in us-central1-b: launch succeeded for `ganesh-g3-qual-20260929t112530z`.
Card seal `f0268ab2cb3fede3034bb081e01a8e50b30dec141f218b75a919b256cbdf739a`.
Startup is being checked; no throughput result yet. Do not duplicate this VM.
The bounded local watcher (PID 69510, session 23671) handles terminal evidence
verification and cleanup after STOP; never duplicate its finalization while
the process is alive. Thirty-three focused tests pass.
All attempts remain under the same cumulative $5
qualification-only ceiling. No current pilot or release-readiness result.

## Gate 3: all us-east1 capacity refusals finalized; US fallback staging — 2026-09-29

The three east-region qualification attempts all refused L4 capacity. Each
backup passed independent immutable-generation verification before exact
network/subnet cleanup; VM/disk/network/subnet absence passed twice. No GPU
runtime was incurred. The current attempt is
`gcloud-qualification/20260929T112030Z` in us-central1-a, staging under the
same cumulative $5 qualification-only ceiling with $0.50 of the existing
support reserve assigned to inter-region input transfer. Thirty-one focused
tests pass. No quality pilot, Gate 3 quality result, or release exists yet.

## Gate 3 qualification: third same-budget zone attempt — 2026-09-29

Both us-east1-c (`20260929T110307Z`) and us-east1-b (`20260929T110950Z`)
refused allocation for capacity. Both refusal backups passed independent GCS
verification, with VM/disk/network/subnet absence checked twice after cleanup;
neither consumed GPU runtime. The current attempt is
`measurement/gate3/capability-scale-v1/gcloud-qualification/20260929T111500Z`
in us-east1-d, card seal
`81a6b75ef81d48d786f46a64520c7e0024b518a95b54609b4cf855432016529e`.
Its launch is pending. All attempts share the cumulative $5 qualification-only
ceiling. Do not duplicate a pending/running allocation. Gate 3 remains open;
no model-quality pilot or release has run.

## Gate 3 first GPU allocation refused; same-budget zone retry staging — 2026-09-29

Attempt `gcloud-qualification/20260929T110307Z` was refused with
`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` in us-east1-c. No VM or disk was
created; this is infrastructure evidence, not a model-quality result.
All launch evidence passed two independent immutable-generation GCS downloads,
and exact VM/disk/network/subnet absence passed twice after cleanup.
The next attempt is `measurement/gate3/capability-scale-v1/gcloud-qualification/20260929T110950Z`
in us-east1-b, using the same pinned inputs and the same cumulative $5
qualification-only ceiling. Thirty focused tests pass. No GPU probe has run;
Gate 3 remains open and full quality pilots remain outside this ceiling.

## Gate 3 GCP qualification authorized and being staged — 2026-09-29

Navneet authorized GCP GPU usage and approved a $5 absolute incremental
qualification-only ceiling. Authenticated read-only inspection succeeded;
the existing model, CUDA image and Docker-bundle GCS generations are present,
and the pinned Ubuntu/NVIDIA boot image is READY. New isolated qualification
launcher/startup scripts bind the evaluation-free workspace, one L4, two-hour
provider STOP limit, 30-minute training-only probe, and verified terminal
backup before exact teardown. No full-epoch model-quality pilot or release
is authorized by this qualification ceiling. Gate 3 remains open.

## Gate 3 bounded throughput qualifier staged; no CUDA run — 2026-09-24

`scripts/train/measure_gate3_capability_throughput.py` now provides a
training-only 16-row/two-optimizer-step CUDA measurement on the longest
source-unique admitted rows. It binds exact model bytes, rank-8 attention
LoRA, BF16/fused loss, the frozen response-only weights, peak VRAM, host
instance ID, and an explicit hourly price plus absolute incremental ceiling;
it has a 30-minute wall bound and 10-minute finalization reserve. This is a
qualification instrument, not a model-quality pilot, and has not run.
The provider-card binder now rejects throughput evidence not bound to the
prepared manifest and train bytes. The refreshed 72-file evaluation-free
workspace is `artifacts/train/gate3-capability-pilot-v2/workspace-v3.tar.gz`,
manifest seal `b5f83fef4b87bdcb21de5a7bd9756928d84cc54b3ffc42a4539bd0cf5a3ca924`.
Its archive hash verifies and it contains zero evaluation files. Twenty-six
focused tests pass. No CUDA host/account or provider-specific spending ceiling
has been supplied; Gate 3 remains open. No GCloud service access occurred.

## Gate 3 non-GCloud pilot staging hardened; no qualified compute — 2026-09-24

The capability pilot now has a host-bound non-GCloud card builder, a
hash-bound runtime and exact upstream model-inventory check before model load,
and an evaluation-free training workspace. The local pinned model's 13 files
passed actual byte verification. A first inventory check exposed that the
weight file's Git OID names its LFS pointer, not downloaded bytes; the verifier
now correctly uses the pinned SHA-256 for LFS content and Git blob hashes for
ordinary files. The 24 GB GPU minimum also now uses the plan's decimal GB,
not an incorrect 24 GiB threshold that could reject an L4.

Current static preflight: `measurement/gate3/capability-scale-v1/pilot-readiness-v1/static-preflight-v2.json`,
seal `e921f11edfb59f1d1fbf57336b36652b1ad142189071e20c213caf53f8272831`.
The latest local draft card is `pilot-readiness-v1/local-draft-card-v3.json`,
seal `7ab68ae1be9e8bc1876bcf89a5c7921755d44d6d8e6a9990ea3a4d38b4108166`,
status `prepared-not-executable`. The refreshed 71-file training archive
`artifacts/train/gate3-capability-pilot-v2/workspace-v2.tar.gz` has manifest
seal `0af157f1d1ecf0bbb8673fd17211b28d520cf58b94c330d715712317f368048a`;
its hash verifies and it contains zero evaluation files. Twenty-five focused
tests pass. No configured non-GCloud GPU provider credential or local CUDA
device was found, so no measured host throughput, ready card, or training run
exists. No GCloud access occurred. Gate 3 remains open.

## Gate 3 capability runner path versioned; static report sealed — 2026-09-24

The SFT runner now recognizes only a separate capability-pilot card/schema for
the 900-row cohort and rejects old card schemas, altered recipe, dataset paths,
token budget, and provider/cost mismatches before model load. It still requires
an actual ready card, Linux single-CUDA host with at least 24 GB VRAM, and a
qualified provider throughput measurement; none exists locally. The static
preflight report is
`measurement/gate3/capability-scale-v1/pilot-readiness-v1/static-preflight.json`,
seal `c0b4e4ec9b2967faac984792a96b75e30ffaee223c51705983cb24d4b7313250`:
900 rows and 651,639 tokens pass, but `execution_card_ready=false` and
`training_executed=false`. Nineteen focused runner/preflight tests pass.
No GCloud action or model training occurred; Gate 3 remains open.

## Gate 3 capability pilot static preflight passed; host and card pending — 2026-09-24

`configs/train/gate3_capability_pilot_v1.json` now binds the 900-row,
651,639-token package, frozen validation, model revision, conservative recipe,
and executable evaluation thresholds. The separate static verifier
`scripts/train/preflight_gate3_capability_pilot.py` passed the exact file
identities, row counts, source-disjoint validation, response-only labels,
2,944-token envelope, and lane objective weights; four focused tests passed.
Its local result explicitly reports `execution_card_ready=false` and
`training_executed=false`: Darwin has no CUDA device. This is not a runnable
host execution card or Gate 3 model-quality result. The runner extension,
actual-host VRAM/throughput/cost/retention preflight, and pilot remain.
No GCloud action occurred.

## Gate 3 pilot preparation verified; CUDA execution contract pending — 2026-09-24

The sealed 900-row data package has been deterministically prepared for the
response-only training objective under
`artifacts/train/gate3-capability-pilot-v2/prepared-manifest.json`, manifest
seal `4bae0de2096ce8ae973d0f7b3ecc9214d8b6ef2e3addfb31cc4afd37446c2d01`.
It contains 900 unique rows and 651,639 input tokens; the existing frozen
50-row prepared validation file was independently re-encoded and found
byte-identical (SHA-256
`6a9d3aa37b30bc2672517f6d63113011de5f8156aa1049e588fdc70a36b77f46`).
The earlier v1 preparation remains preserved. No model training occurred.

The current SFT runner and execution-card schemas are pinned to earlier
1,399-/3,225-row pilot contracts and cannot honestly be reused as-is for this
900-row, 651,639-token cohort. A versioned pilot config/card, runtime
preflight, qualified single-CUDA host, bounded cost/retention plan, and frozen
executable promotion assessment are still required. Local MPS does not meet
the CUDA recipe. No GCloud usage is authorized. Gate 3 remains open; this is
not a model-quality result or release authorization.
The prospective runtime requirements are recorded in
`docs/plans/GATE3_CAPABILITY_PILOT_EXECUTION_CONTRACT_20260924.md`; that
document is not a ready execution card.

## Gate 3 corrected 900-row data package passed; pilot pending — 2026-09-24

Navneet approved exact token-length replacement plan SHA-256
`1844d190adcdc47496fc18fa9ec94babaeb469931985b384ac0c575726d4b13c`.
The prebound TypeScript repair `reserve-06` was activated under seal
`13254cad9b1165c399c1a829a0aa200b2df484875b95f8d4a2c6dc793a5ef925`.
Its one teacher draft raised counted usage to 1,060/1,200 and measured 1,151
untruncated tokens (precheck seal
`770537b9346aac29b3e7edf7af4d745c423a554ce4ff85ecc56810f2a6436369`).
Semantic, independent V9 test-author, blind delta, and executable checks all
passed; final matrix seal
`bbe9bf8bfb16fd1b5f491a2b89003d30be4abdf68e85b27007f93424ad7771d9`.
The new 720 cohort replaced only the 3,032-token row, retained six per cell
and 720 unique IDs/sources, and passed new scale separation and two fresh
blind AI reviews for the affected capability. Corrected 720 seal:
`cfe5877afcf6a78cb26aa55ee2f59b1e82026436e9b8bbb646e55b7cb7b7ae3e`.
The 180 replay JSONL bytes were unchanged but independently resealed.
Package-level exact/normalized/fuzzy separation passed all 900 rows with
zero failures (seal
`c2ac02d92a4b3b0a0612b38b56fea505ed0daf3d1313bb04b197e9a10faa700c`).
All 900 rows tokenized without truncation and met frozen lane objective
weighting (seal
`f530ccdf44e09eec1ac7baea9f962e59ec17633148d07e80b962ed026aaf7c30`).
The final validator accepted 720 capability plus 180 replay rows; the
canonical training JSONL SHA-256 is
`57bf0b35f16f7e846fe9548553124cabc175f969f9bfe6a2a398227056a93df1`.
Data-package admission seal:
`149b030f11bc0eb054f0a4d511432f33b4123e3b65fab77c2166dca23d1190aa`.
This is not a Gate 3 pilot or model-quality pass. No training or GCloud action
occurred. Local PyTorch reports no CUDA device; only MPS is available, which
does not satisfy the frozen CUDA pilot contract. The old overlength package and
failed tokenization remain immutable historical evidence. Reviewer evidence
is AI, not human sign-off. Hugging Face release remains ineligible.

## Gate 3 HARD STOP: one row exceeds the frozen token envelope — 2026-09-24

The exact 720+180 package passed content-free exact/normalized/fuzzy
separation with zero failures against 3,045 remaining prior training rows,
package peers, and 540 frozen private evaluation tasks (report seal
`e1df396fd714c9b984649630d03da22efc816245841e80dbdb2e637dc0c805d8`).
Untruncated tokenization then found one failing TypeScript repair row at
3,032 tokens versus the 2,944-token maximum (failed report seal
`4e44bd293e5a7d5404ed44600c7534cf0fcf12bb46da60d835281e8449456927`).
No final 900-row admission, training, or release is allowed. Two same-cell
prebound reserves are unused, but the frozen activation rule does not clearly
cover a post-executable token-length failure; the final-corpus failure is a
hard stop. See `docs/process/GATE3_TOKEN_LENGTH_HARD_STOP_20260924.md` for
the exact evidence and recommended prospective one-cell remedy. Do not
generate or activate a reserve without that resolution. No GCloud action.

## Gate 3 capability 720 sealed; broad replay selected — 2026-09-24

The deterministic 20-row quality sample passed content-level review by two
independent blind Codex CLI reviewers (one generation and one repair sample per
primary capability), with zero failed checks. This is AI review, not human
sign-off. Quality report seal:
`863190b2519742ec2b16e404910fcad9749b9d38f5af4ef82c1aecbd234101bf`.
The 720-row capability cohort passed its fail-closed admission binder under
manifest seal `1bf0e65c4704fcab266f97da4af793ff9d7fdcd3a37df792be9cfc1271e1b448`:
six rows in each of 120 cells, 720 unique IDs and sources, bound to the
174-row retained entry, 546 verified scale rows, passed content-free scale
separation, and blind reviews. The original duplicate-reserve failure remains
failed and is not counted. The deterministic broad-replay selector chose 180
byte-preserved prior training rows, fifteen per lane/task-type pair, with
unique sources disjoint from capability rows; selection manifest seal
`5b98721409b514e0ea830d24721aa327cecbad4a8fd6d16259af96b3b902fb65`.
Replay selection is not final training admission. Package-level 900-row
separation, tokenization/weighting, final validation, and Gate 3 pilot remain.
No GCloud action or model training occurred. The final 900-row training
inventory remains unsealed; release is ineligible.

## Gate 3 prospective one-row repair executable admission — 2026-09-24

Navneet approved a source-unique, one-cell replacement for the duplicate
canary reserve. The original failed 546-row assembly and 711-request queue
remain unchanged. A new Python repair request is prebound to unused source
`exp-v1-python-repair-0365` under one-row manifest seal
`92e32585027a80c3637383d0c0c025f3c943529c6953ef95b0e857e4c0b89a18`.
The one allowed teacher draft was generated, bringing counted usage to
1,059/1,200. Blind semantic review passed under seal
`ed6e4ffdf4088f26e2e66996d5f2c03016901a78e65ae9c89785b9927bd99e88`;
independent V9 test-author structure passed under
`87f6d8c57ef52198153fa9f53d28c1783e2e9c771caa39227c88f199fc886fed`;
fresh blind delta passed under
`37a037420739179778d7ce0529b2548f7f4473c49991f32b5c9b4e3f3744b3ff`;
and the one-worker executable matrix admitted the row under
`c031e579820a77953eba18816060f681f01e089f450c3ea58bbf5b8d5276e134`.
The new provisional assembly contains 546 candidate- and source-unique rows,
exactly filling all cell deficits, under report seal
`4f5845d95193e3cbb5df7ff32a1c47c7b432bf484229b7162251addd81384e40`.
The first separation attempt stopped before any evaluation read because
pre-test envelopes lacked independent test files. The separate materialization
bound all 546 rows to their exact admitted matrix envelopes, including two
independent test roles each, under report seal
`8f27cb55c1b6fedea24b2a2e7d086a78203b327c94022fa18f08a213a0a1023b`.
The content-free separation comparison of those 546 against 3,225 prior
training rows, the retained 174, and 540 frozen private evaluation tasks
passed all exact, normalized, and fuzzy checks with zero failures under report
seal `c59b89500390781b21a520983a68f5c33830427e7eef4ea6108b07491dde3475`.
The current provisional 720-row capability cohort (174 retained plus 546
materialized) is six per cell and 720/720 ID/source unique under report seal
`5cd935997b35647e111ed809329c5831c498e762d449fb33cad4caab22c206cc`.
The earlier `provisional-capability-720-v1` contains pre-test scale envelopes
and must not be used for downstream package admission; use v2 only.
This is construction-stage admission, not final training admission: blind
quality review, 180 broad replay rows, package-level separation,
tokenization/weighting, and final 900-row package validation remain pending.
The prospective plan file SHA-256 is
`81ba26cbe4b6557bc693ac63e261e6c6d787f08c669b6b42f1415a4649f8d3ad`.
The authoritative training inventory remains 174/900. The old queue remains
hard stopped, and training/release remain blocked until all new and original
gates pass. No GCloud action occurred.

## Gate 3 HARD STOP: canary reserve reused — 2026-09-24

The proposed 546-row scale assembly rejected at 546 rows / 545 unique
candidate IDs. `cap-scale-associative_aggregation-python-repair-reserve-06`
was already admitted in the canary and was reused by the later 16-reserve
ledger. Both attempts share the same source identity; their candidate content
differs. The frozen queue allocates no other reserve in that cell, which has
only five unique rows against the six-row target when combined with the
retained training-entry anchor. The first-pass failure in the cell is not
eligible for blind test reauthor. No provisional 546 or final 720/900 corpus
was sealed. Preserve all completed executable evidence but grant no second
admission credit to the reused reserve. Stop further generation, separation,
packaging, and training pending a prospective resolution. See
`docs/process/GATE3_DUPLICATE_RESERVE_HARD_STOP_20260924.md`. Counted teacher
drafts remain 1,058/1,200; authoritative training inventory is 174/900.
No GCloud action occurred.

## Gate 3 Go requalification accepted; 16 reserves active — 2026-09-24

The uniform 89-candidate local Go requalification completed under matrix seal
`1f7f770109b5c54b1d83746e181d63db81b7900d63e47c21a3d9c28df6d0c0d7`:
83 admitted, 6 rejected, zero unresolved. The frozen assessor accepted all 89
input hashes with no regression of the original 51 Go admissions (assessment
seal `49ae1b356c318513da0fb034f1602bf0046ff65cc3f527091913e305b5b8524f`).
The derived complete first-pass matrix is 508 admitted / 26 rejected, seal
`fdbf0430508bee0b71ee5f4c7310c54bc22c149c3abc48f5b70b21e75fc19138`.

The one allowed blind test-reauthor outcomes were reconciled with the entire
derived cohort: 518 provisional executable admissions and 16 terminal rejects,
zero unresolved, under reconciliation seal
`fc3cdd3285be248dd01021898ce42229f06de841e62576e4c0e3033faff3c0ee`.
These are not yet training admissions; global separation and package sealing
remain pending. The 16 rejects fit the frozen per-cell reserve allocations.
Reserve-chain ledger seal:
`895bb5ac34499b9722a767c057654a1f4bcb66e8cf32005f99c6a99b1def73ae`;
teacher activation report seal:
`26ceb5e58f8153021fb21e5291d28a1a3118c1ca43df03ca5f7e18d4a4205117`.
A 16-request local reserve cohort is recorded under
`measurement/gate3/capability-scale-v1/first-pass-v2/go-single-worker-v1/reserve-v1/`.
It sealed 16/16 generated under report
`fa45f4608663d90dc30718c289517348226414dcd63d149a5e8f0cae3fb03e0d`.
Semantic review passed 16/16 (seal
`85cfa62b63732aa9c2560983542bb87ae98d7221d629b843eaf26a2482869947`),
independent test-author structure passed 16/16 (seal
`7e226e6559a432b45c7a8b4d21ced854994eb862508600168b636d70160d2720`),
and fresh blind delta passed 16/16 (seal
`b0b216a046e2c987e4350db1a396f8337b7e8f4c01fd530fbc5bdff3248bed51`).
Conservative teacher draft usage after this phase is 1,058/1,200.
The one-worker executable matrix sealed 15 admitted / 1 rejected (seal
`f0d4cfba3059b179050af25e0df8741157c7549abd794df29968a7500c540eb4`).
The one rejected Go reference-primary case used its sole blind test-reauthor
correction; fresh delta passed and its isolated executable matrix admitted it
under seal `ce68d2f3ad1c6dc9cfe15d2f8bb88f4db30c1d93ca6b92f4a16571ea32758b75`.
Thus all 16 activated reserve slots have provisional executable admissions.
They still require aggregate integrity, global separation, quality, and
900-row package sealing before training entry.
Authoritative training inventory remains 174/900; model training has not
started. No GCloud action occurred in this continuation.

## Gate 3 first-pass matrix failed; Go requalification active — 2026-09-23

The exact first-pass 534-candidate matrix is complete under seal
`01ab1d4b460a922e81b61497a923e2ac0c577eceb607288f9734a5a7f951f5e3`:
476 admitted, 24 rejected, 34 unresolved. All unresolved are Go timeouts.
Eighteen blind test-reauthor corrections were activated for reference failures;
17 passed structural review and fresh delta audit, and their new matrix admitted
10, rejected 7 (seal
`d8425db28fcffbbd052d70d7677d42c3db8f7803303415c7a63cdc36b8c9af91`).
One reauthor was structurally rejected. No failed row is counted as admitted.

A separate uniform single-worker requalification of all 89 Go first-pass
candidates is ACTIVE locally under
`measurement/gate3/capability-scale-v1/first-pass-v2/go-single-worker-v1/`.
Its input manifest is sealed at
`d35ec1d47706d409b92260d21f4595d9431f9f2eeabcb33cef4a61e199fc7ea0`.
The original matrix is preserved. Until the Go campaign is complete and a
derived aggregate passes, the authoritative training inventory remains
174/900 and model training has not started. No GCloud usage is active.

## Gate 3 first-pass qualification at executable matrix — 2026-09-23

The 534-request remainder is complete: merged teacher 534/534, semantic
534/534, independent test-author structural check 534/534, and blind delta
534/534 after a separately sealed retry of 127 CLI transport-classification
failures. Controlling report seals are respectively
`f53ab8e2da3182819874b67aaf6de21d5c131f6fb7d1175221dfc5399ec49f6c`,
`357627f4f5ea43eb99578c9eb81fb47cb1d09084d5f09c91034029ad60d79e82`,
`c4961be372d978e8f79b2b9313c044964c84366a4ede9b0ae16dfa30ff03a3ca`,
and `97d41488f34db77e1831f528d8f27e5cd45ca6d33e50ef7b5a596554e5e094e7`.
Original failed evidence is retained, not rewritten. The exact executable
matrix is ACTIVE locally under
`measurement/gate3/capability-scale-v1/first-pass-v2/final-matrix-v1/`.
The authoritative inventory is still 174/900 pending full matrix, reserves,
separation, and package sealing. No GCloud usage or training job is active.

## Gate 3 scale canary passed; 534-request teacher campaign active — 2026-09-18

The complete construction canary is 12/12 admitted under seal
`dc239958fc66b793830a19c254c54cdfad316263cc0eb04607a0e76454a13ad3`.
The original canary consumed 12 first-pass drafts; seven terminal delta failures
activated seven source-unique reserves. The corrected primary-delta teacher
prompt produced 7/7 semantic and delta passes. Five reserves passed their first
matrix; two passed after their single permitted blind test reauthor. No result
is unresolved and no evaluation artifact was read.

Current status is ACTIVE LOCAL CONSTRUCTION. A resumable 534-request remaining
first-pass teacher campaign is running with 12 workers under prompt contract
`capability-scale-primary-delta-teacher-prompt/v2`. The sealed training-entry
inventory remains 174/900 until the scale admissions are packaged. No GCloud
resource or training job is active.

## Capability-scale source queue sealed — 2026-09-17

The deterministic source queue is complete at 711 unique requests: 546 first
pass and 165 reserve. Queue SHA-256:
`a8d9eb96cdbdb8ccd4ec126b512c71ae832856beff9dd46a799c99571eefba51`;
manifest seal:
`f3e3e312625ec85f067c0089f40b16ed4591fe320745445e34f23825a3dc6d55`.
All prior-corpus, historical-teacher, qualified-inventory, and within-queue
source collisions are excluded. Current state is ACTIVE LOCAL CONSTRUCTION
CONTROLLER IMPLEMENTATION. No candidate call, training job, GCloud resource,
or billable compute is active.

## Training entry passed for corpus construction — 2026-09-17

The unified qualified inventory is sealed at 174 records and 174 unique source
identities: 114 V2 generation admissions plus 60 V9 repair admissions. It
covers all 120 capability/language/task-type cells and marks one deterministic
anchor per cell. Training-entry manifest seal:
`fbf45982984c2c669e03abf1c773d768019651184547104271de12c42f79318c`.

Current state is ACTIVE LOCAL CORPUS CONSTRUCTION PLANNING. The exact remaining
capability deficit is 546 admissions—246 generation and 300 repair—followed by
180 broad replay records for a 900-row pilot corpus. No training, untouched
evaluation opening, publication action, GCloud resource, or billable compute
is active. The scale contract is frozen at
`docs/plans/GATE3_CAPABILITY_SCALE_CONSTRUCTION_PLAN_20260917.md`, SHA-256
`d0e2b112eaa17eb96d2a0284964c9d107bc94b3fcd8edc6369cf7792026100ee`;
deterministic unused-source queue sealing is next.

## Gate 2 passed under V9; training-entry assessment next — 2026-09-17

The Gate 2 repair-corpus qualification is complete. V9 reconstructed the exact
60-cell repair cohort from 58 sealed V7 admissions, the accepted V8 Python
cross-cutting role, and one fresh Rust primary role. It ran fresh blind delta
audits for the two changed candidates, reran content-free separation across all
60, and passed the exact executable matrix for both corrections. Final state:
60 admitted, 0 rejected, 0 unresolved. Qualification seal:
`cb0eafa84cbd76ff90c72456883c854d22356bb87da7a1ecf6a7bd4cf50ade0e`.

V2 generation equivalence remains passed for all 60 generation cells, so the
qualified combined surface is 120/120 generation/repair cells. Evaluation
artifacts read outside the content-free boundary remain zero. The result
narrative is `docs/process/GATE2_V9_RESULT_20260917.md`, file SHA-256
`328fd26edf953a1369847179d92246adf927a72c6df4c92f46b52dcd597b47a6`.

The preserved terminal sequence is:

- V6 pre-campaign readiness failed on impossible JSON member-order validation,
  seal `39a8264850aafb9c8b8db6ed9de4f8d6e0d46b4ad331329a4e2c21c6cce3f778`;
- V7 completed at 58/60 admitted and 0 unresolved, seal
  `1bbdd82b8558542547f0476e8b753089a0c93e73221f4db4c6b6b9787dde3f06`;
- V8 stopped before delta/execution on an over-broad Rust validator, seal
  `ff2de8bc59f6f0da95e53bb020470df3b2abbda5b1f76c83f03f6814f6648af5`;
  and
- V9 passed at 60/60 with zero unresolved and 120/120 combined coverage.

Current state is GATE 2 PASSED; TRAINING-ENTRY ASSESSMENT PENDING. No new
training using this qualified corpus has been executed, and qualification does
not itself authorize training. No GCloud resource, training job, untouched
evaluation opening, publication action, or release action is active.

## Gate 2 V5 terminal no-go; V6 implementation active — 2026-09-17

V5 is sealed as `qualification-failed`. Its exact ordered first pass contains
60/60 terminal dispositions: 29 admitted, 31 rejected, and 0 unresolved. The
54/60 aggregate gate and all three distribution gates failed, so reserves are
forbidden. The canonical admission report seal is
`3b112519be6c3f122499d137983a58288bdad16bdfaea8c7c83f34c45dc58b11`;
the qualification seal is
`f169894cc32557388ec7812180d1524502af1ae35c310e8f31f3c4177e5452e5`.
The result narrative is
`docs/process/GATE2_REPAIR_DELTA_V5_RESULT_20260917.md`, file SHA-256
`0e7571e0b345568dcbc073d4c7086ec33ee58d73327dfeeea2ae33c0e3e53ca0`.

The terminal taxonomy is 14 strict test-author contract rejects, 17
final-admission executable rejects, and 29 admissions. The final lane counts
are Go 8, Java 5, JavaScript 1, TypeScript 4, Python 10, and Rust 1. A complete
post-run audit classifies all 31 rejects as test-author/validator/staging
interface failures: 10 over-broad syntax-heuristic false positives, 4 Java
role-path collisions, and 17 authored-suite runtime-binding failures. No
reject demonstrates a bad reference candidate. Global separation passed for
all 46 post-test candidates, all final-attempt model calls completed at the
transport/runtime layer, and evaluation artifacts read outside the
content-free boundary remain zero. V5 therefore improved recorded yield over
V4 but did not qualify the repair construction method.

V5 reserves, candidate relabeling, and same-contract reruns are prohibited.
The adopted successor is the V6 canonical-test replay plan at
`docs/plans/GATE2_REPAIR_DELTA_V6_CANONICAL_TEST_REPLAY_PLAN_20260917.md`,
SHA-256
`4fe6a1374c01a0a682bf256c91a141b36b26680bdb5279049070f4f143418ec1`.
It uniformly carries all 60 exact teacher candidates and semantic outcomes,
runs 60 fresh independent test authors and fresh blind delta audits under
controller-owned paths, replaces
syntax adjudication with the exact executable matrix, and permits at most six
structural-only reauthor calls after frozen eligibility gates. It generates no
teacher candidate. Current state is ACTIVE LOCAL GATE 2 V6 IMPLEMENTATION.
No training, GCloud resource, evaluation opening, publication action, or
release action is active. Historical process estimates remain training 84%,
release 58%, and overall delivery 72%; they are not readiness scores and
remain blocked at Gate 2.

## Gate 2 v4 terminal no-go; v5 interface replay implementation active — 2026-09-16

The complete V4 first pass is sealed as `qualification-failed`. All 60 primary
candidates are terminally accounted for: 5 final admissions, 55 rejections,
and 0 unresolved. The frozen aggregate and distribution thresholds failed, so
reserves are forbidden. The admission report seal is
`bfc80e399b44fb350048ed459c2bb611801757fb2c73286389d5c4c98aca99d2`;
the qualification seal is
`af2ce7ea3cab939ea219eef840af9e42bcb379f0f5de7002bcdf7e688da8c2e5`.
V2 generation equivalence remains passed for all 60 generation cells.
The complete result narrative is
`docs/process/GATE2_REPAIR_DELTA_V4_RESULT_20260916.md`, file SHA-256
`1c550c9fe5141d63d21b3b92a7002293464cebbf80e7b052e51f05d263b40433`.

The terminal taxonomy is 30 independent-test-author contract rejects, 23
post-teacher cross-witness rejects, 2 final-validator rejects, and 5 admitted.
Most rejects are construction-interface findings: 27 test authors emitted more
than the exact two required role files; 3 Java tests missed the required entry
point; all 10 JavaScript witnesses looked for an unstaged `reference.js`; all
10 Rust witnesses used `main` while the runtime compiled them as a test
harness; and one Java VM working-directory failure was classified as semantic.
Two TypeScript witnesses and the two final-validator rejects remain
candidate-local findings. This is a failed corpus-construction qualification,
not a model-training result.

The original ordered-60 inventory seal is
`8fc2c4ea31628287ae5b8eb83353f13e1e5aebb1fa93af97256d255c3120e087`.
Two final-admission rejects initially omitted their already sealed retry
ledgers from the terminal wrapper. A narrow evidence-only correction restored
those exact ledgers without changing candidate bytes, executions, reasons, or
dispositions; correction seal:
`05cb34251ceaca6c3c4289779128e208ddd0d238ac2f8aa594253ff5cd1aee51`.

The V4 run also exposed a contract discrepancy: Go used a 120-second limit per
suite attempt, while the sealed plan says 120 seconds per candidate. Therefore
the evidence must not be described as aggregate-120 compliant. The numerical
no-go is unaffected because only 5/60 candidates were admitted, far below the
54/60 threshold.

The sealed successor is
`docs/plans/GATE2_REPAIR_DELTA_V5_INTERFACE_REPLAY_PLAN_20260916.md`, file
SHA-256
`132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b`.
It freezes a full ordered 60-cell requalification: 58 byte-identical V4
teacher carries, exactly two fresh TypeScript primaries from new content-blind
sources, and a uniform downstream rerun under corrected interfaces. It carries
no V4 execution or admission status.

Current state is ACTIVE LOCAL GATE 2 V5 IMPLEMENTATION. No training, GCloud
resource, or publication action is active. Historical process estimates remain
training 84%, release 58%, and overall delivery 72%; they are not readiness
scores and remain blocked at Gate 2. The next contract must correct the measured
interfaces, replace the ambiguous Go wording with an explicit bounded
suite-attempt contract, and predeclare uniform replay versus fresh-generation
rules. Readiness fixtures must pass before any V5 model call.

## Gate 2 v3 terminal no-go; v4 tooling and source repair active — 2026-09-16

V3 is completely sealed as `qualification-failed`. Its 60-record first pass
contains 0 final admissions, 52 rejections, and 8 unresolved Go candidates
after the single permitted infrastructure replay. No reserve was eligible or
generated. Terminal qualification seal:
`b2b718a1d61f3a6858b28f9b9938438548a89eb37e04a091ace5036f914c3727`;
terminal admission seal:
`48961ecc86e732afd1fd293d100e214a30e78ad4f692dc248be36f49ea89d8be`.

Root cause is now measured. Forty of the 41 executable contract failures came
from arbitrary hashed test paths being staged while Java, JavaScript,
TypeScript, Python, and Rust runtimes expected canonical filenames. The one
remaining executable failure is a real Go cross-witness defect. Eight
CommitPackFT candidates hit a strict-schema gap, and eight Go candidates
exhausted 64/64 attempts under concurrent amd64 emulation. None of this changes
the v3 result.

The clean v4 contract is
`docs/plans/GATE2_REPAIR_DELTA_V4_QUALIFICATION_PLAN_20260916.md`, SHA-256
`79849d2f8b70ba69572b4c3fa1761bdb413562c6f6d9a12537d93a1724812ef6`.
Current state is ACTIVE LOCAL GATE 2 V4 PREFLIGHT. Before any teacher call:
finish and seal canonical test staging, compilation/cross-witness checks,
dataset-specific provenance, lane-aware verifier limits, and six-lane/all-
provenance end-to-end fixtures. The fresh classified pool is currently
infeasible at 55/60 queueable cells, so v4 also freezes one non-adaptive native
CommitPackFT tranche of 1,000 Go, 1,000 Python, and 1,000 Rust sources before
ontology classification and queue construction.

No model training or GCloud action is active or authorized. Historical process
estimates remain training 84%, release 58%, and overall delivery 72%; they are
not model-quality or release-readiness scores. Local Gate 2 ETA is 18–36 hours
if the fixed source tranche closes all five deficits. Project delivery ETA is
2–4 weeks after that and remains conditional on later executable transfer.

## Gate 2 v3 repair-delta contract ready — 2026-09-14

A new versioned construction contract is ready at
`docs/plans/GATE2_REPAIR_DELTA_QUALIFICATION_PLAN_20260914.md`, file SHA-256
`4023a896300112f9f93f2a16698d549f203e3e75b4e71ae054f3a98463e2f0f0`.
It preserves v2 as a failed result and requalifies all 60 repair cells rather
than retrying only the observed empty cell. The first pass is exactly 60 fresh
candidates. At most six reserves become eligible only if the frozen first-pass
thresholds pass, for an absolute budget of 66.

Current state is READY FOR LOCAL GATE 2 V3 IMPLEMENTATION. The next work is to
implement the source-affinity, repair-delta, split-test, semantic-review,
generation-equivalence, and reporting contracts; seal the fresh source queue;
then execute the bounded local qualification. No compute is running. No model
training or GCloud use is authorized by this plan.

Progress remains training 84%, release 58%, and overall delivery 72% because
these are historical process-completion estimates and no new executed evidence
exists yet. The low-confidence warm-path ETA is 4–8 hours for v3 implementation
and Gate 2 closure, then approximately 1–3 weeks to complete the remaining training and
release gates if v3 passes and the trained model demonstrates transfer.

## Gate 2 capability qualification failed after bounded recovery — 2026-09-14

Gate 2 is terminal under the current sealed construction contract. The final
canonical campaign generated and dispositioned 247 candidates: 240 originals
plus exactly seven replacements, one for each cell empty after the correction
pass. It admitted 217 candidates (87.85%) and covered 119/120 cells. The sole
uncovered and exhausted cell is `numeric_reasoning/python/repair`; its permitted
replacement failed semantic review. The minimum-admission threshold was met,
but the mandatory every-cell threshold was not.

Admissions by language family are Go 37/41, Java 35/41,
JavaScript/TypeScript 74/81, Python 34/42, and Rust 37/42. Final rejections are
18 semantic, seven reference-solution failures, four terminal no-change
corrections, and one known-bad-accepted failure. The canonical final executable
run has no timeout-driven gap. Final admission report seal:
`c576ef4f5b0f137edac829703eae6d7c4a63cae513544d36471f7ffcf81b7cb7`.
Qualification summary seal:
`293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139`.

Current state is STOPPED AT GATE 2 / NO-GO. The sealed rules do not permit a
second replacement for the empty cell, and a failed qualification does not
authorize scaling or training. No compute is running and no GCloud resource was
used by this campaign. `ganesh-mini-1.0` is not eligible for publication as a
passed model release.

The historical workflow estimates remain training 84%, release 58%, and
overall delivery 72%. They record completed process work, not model quality;
all three are now blocked. ETA is unavailable under the current contract. Work
can resume only after an explicit decision either to close the project as a
documented no-go or to adopt a revised Gate 2 construction contract and rerun
qualification.

## Gate 2 qualification source queue ready — 2026-09-14

The sealed 120-cell contract now has a deterministic 240-row source-assignment
queue: two fresh training-only stimuli per cell, 240 globally unique source
identities, and all 2,996 source identities used by the prior corpus excluded.
Queue SHA-256 is
`0cf1a51055d58c4ae0c454aad0f6b8e844cae27517a16516f59bbe428a967c9f`;
manifest seal is
`53a2465181f10a19a2fe3cbf9d562d5d74d7a19aa9984c878dfbeace559708af`.
Focused tests and an independent seal/distribution replay pass.

Current state is ACTIVE LOCAL GATE 2 IMPLEMENTATION. The 240 rows are drafting
requests, not candidates, so generated and qualified candidate counts remain
zero. The next work item is the capability-specific isolated teacher and
admission pipeline. No GCloud resource is active or authorized by this work;
no model training is running. Progress remains training 84%, release 58%, and
overall delivery 72%. ETA remains 1–3 weeks, conditional on qualification
yield and the later executable transfer gates.

## Capability-stratified qualification contract sealed — 2026-09-14

Gate 2 now has a sealed replacement construction contract at
`0181751bdd912b8d04ccf954c358cb22681d6fc4aa5b3896a986e7a1ce73af01`.
Ten primary capabilities cross six lanes and generation/repair for 120 cells.
Qualification is capped at 240 drafts and must admit at least one record per
cell plus 120 overall after at most one replacement per empty cell. It uses
only training sources and explicitly excludes evaluation data and private
archetype labels.

The conditional pilot target is 720 new records plus 180 broad replay records,
but no pilot construction beyond qualification and no training is yet sealed.
The immediate active work is implementing source assignment, isolated teacher
and semantic-review contracts, executable admission, and qualification
reporting. No GCloud resource is active or authorized. Progress remains
training 84%, release 58%, overall 72%; qualified release candidates remain
zero. See `docs/plans/GATE2_CAPABILITY_STRATIFIED_CORPUS_PLAN_20260914.md`.

## Gate 2 reopened after training-only diversity audit — 2026-09-14

The sealed 3,225-row corpus was sufficient only for one bounded Gate 4 pilot;
that allowance is exhausted. A new non-evaluation audit finds that the 640-row
v3 selection proportionally represents the full corpus's thirteen observable
contract tags: selection shares range from 17.69% to 23.87% around the 19.84%
row sample. It therefore finds no gross selection-specific topic dropout.

The full corpus has 2,812 unique source records and 3,225 unique normalized
prompt scaffolds, but the teacher contract drives heavy lexical concentration
in string/Unicode, malformed-input/error, ordering, and mutation/aliasing
requirements. These are observable words, not proof of semantic capability
coverage. Report seal:
`714fe87491fb798c6248f53e40dd80c9d305125f39dd631db8d7c47114b8f793`.

Current gate is Gate 2: define a training-only capability ontology and a new
cross-lane corpus/admission contract. Do not use evaluation tasks as training
templates, generate more rows through the unchanged teacher contract, or run
another capacity/scheduling/optimizer probe. No GCloud resource is active or
authorized. Training-process estimate remains 84%, release estimate 58%, and
overall delivery estimate 72%; these percentages measure completed pipeline
work, not candidate quality. Qualified release candidates remain zero, so ETA
is still conditional rather than fixed. See
`CORPUS_DIVERSITY_AUDIT_20260914.md`.

## Gradient-conflict audit terminal; PCGrad ineligible — 2026-09-14

Attempt `20260914T003000Z` validly completed the frozen zero-step audit under
approved proposal
`af67925bf32f28b2708862a517af58b00f161cbbd66c2c3d00db05987f98cd88`.
It measured eight groups and 120 pairwise cosines. The minimum cosine was
`+0.035201297582185986`; negative pairs were `0`, qualifying conflict groups
were `0/8` versus required `4/8`, and JavaScript/TypeScript negative-
participation groups were `0/8` versus required `4/8`. The frozen gate stopped
before training: optimizer steps `0`, seen tokens `0`, canary tasks `0`.
Campaign status is `completed-gradient-audit-no-conflict`. This rejects the
declared gradient-conflict/PCGrad mechanism; it is not an infrastructure
failure or a trained-model failure.

All 25 terminal-manifest entries and all four canonical evidence seals passed.
The terminal manifest is
`5fef6e6135a9a4adafcb89d0fa69e66aac956e9fe8e217e372e7cecdf57e0a5f`;
campaign seal is
`d31915796be69a2f9f0c6e20f0ea387b435d98a9507221f881ced3d842d7785f`.
GCS control/recovery generations are `1789358988755320` and
`1789358992992417`; teardown receipt generation is `1789359329656748`.
Post-teardown provider evidence is independently preserved at generation
`1789359494557821`, with preservation record generation `1789359520965327`.
Projected cost is `$0.08009125052911889715777777778`.

The exact VM, disk, subnet, and network are absent twice. Ganesh compute
billing is closed. The unrelated `laxmi-wmv2-training-01` disk remains and may
bill, so the project is not GCS-only. Gate 4 remains blocked on defensible
multilingual executable transfer. Current direction is local diagnosis and a
task/corpus-diversity mechanism focused on persistent `collapse-runs`; no new
GCloud execution is authorized. Training-process estimate remains 84%, release
estimate 58%, and inception-to-delivery estimate 72%, but there is no qualified
release candidate and therefore no defensible fixed delivery date. See
`GRADIENT_CONFLICT_PROBE_RESULT_20260914.md`.

## V3 checkpoint sweep terminal; earlier stopping rejected — 2026-09-11

Approved diagnostic attempt `20260910T150000Z` evaluated all five earlier v3
checkpoints on the frozen 30-task screen. Passes were `5, 5, 3, 6, 5` at
78,487 through 389,093 tokens; the already measured 466,614-token final remains
6/30 versus upstream 5/30. No checkpoint meets net +2 with zero lane
regression. Decision: `do-not-promote`; earlier stopping does not rescue v3,
and this recipe must not be scaled, rebalanced, checkpoint-selected, or opened
on full development.

The guest completed with startup exit code 0, sweep report seal
`55fb67ff6b1a438c0f14c617ede45f3ffdf0ac5a32694cac4afd5b73bc32742f`,
and campaign seal
`15041b9000812305fab0573cd72b16385bf2aa67efbb67226125f2b84bc20ddc`.
Its shell finalizer hung after completion. Approved IAP-only rescue recovered
332 objects/4,050,250 bytes; all 331 inventoried files hash-verified, including
the one verifier record missed by the live rolling backup. Semantic replay was
exact. The sealed phase ledger contains all eight phases but retains
`status: running`; preserve this disclosed bookkeeping defect.

The temporary firewall, exact VM, auto-delete disk, subnet, and network are
absent in two checks. Ganesh compute billing is closed. The unrelated detached
200 GiB disk `laxmi-wmv2-training-01` still exists, so project-wide GCS-only is
false. Result summary seal:
`1b8968595287d979e62cd2e0d29008c12a5559c62ccdfb61d4d44c46c2297bf0`.
The local cross-checkpoint audit is now sealed at
`15629f7407727fb9477eb6da892d709f174589575225e807ca14ec88f64ce9cc`.
Twenty-one tasks fail throughout, only eight change status, and five changing
tasks share the `collapse-runs` archetype. Next prepare a bounded per-lane LoRA
gradient-conflict audit with conditional gradient surgery; do not run another
balance-only or specialist-merge experiment first. No further GCloud use is
authorized. The local non-executable mechanism plan is sealed at
`4e04c8029e42605d7c5aba913e97644a952e2c28bfc1140d278c7c76a936d73d`.
Any future startup controller must also replace the observed
unbounded process-substitution log drain. See
`LANE_STRATIFIED_CHECKPOINT_SWEEP_RESULT_20260911.md`.

Local implementation has started without cloud access. The gradient-conflict
primitive now supports fixed eight-group selection, all 15 pairwise lane
cosines, the predeclared two-part conflict threshold, deterministic PCGrad
projection order, sparse trainable-parameter layouts, and frozen weighted
aggregation. Eight focused tests pass. It is not yet integrated into the CUDA
training engine and creates no execution authority.

The immutable v4 config is now generated at file SHA-256
`4b7d335d31ea5b5a4b940b9b240f708a9680e17d81dfa8222d7115f8f62610be`.
Its local card passes every preflight check and is sealed at
`087e3c4b7000957e022dadb12efa5f2fe9879a11b14208b67c5811e4d8086423`.
It reuses the exact v3 data/capacity/LR and permits PCGrad only after the
zero-step eight-group audit passes both frozen conflict thresholds. Runtime
group validation, gradient collection, sealed audit/stop adjudication,
deterministic per-group PCGrad, exact-boundary resume, and conflict telemetry
are now integrated in the production SFT engine. Thirty-five focused tests
pass. Campaign integration now terminates a failed conflict threshold without
training or evaluation, re-verifies a passing audit before canary construction,
and preserves the v4 full-development block. The corrected startup uses named
FIFO loggers and waits for both before terminal inventory, eliminating the
historical process-substitution drain. The deterministic 56-file training
workspace is 6,255,789 bytes at SHA-256
`c014652032e2bcc557891776f5abcab6c1265f238330fdbd8c8cd8e50dceb23d`;
manifest seal is
`8c39aabd8b13b0282e1837581cd163cbb851c9bf3f6b3043f686f73be59c86bf`.
The paired 587-file development workspace is 1,013,124 bytes at archive
SHA-256
`4d46b67a42e1868fea45123ad761492bc68426fbffb55b17c79f7731bd8bf8a2`;
its repository-path manifest seal is
`e39cce631f57762588ed98d7a6bfa68427b828ab83ea891e0a4188ac75d143a3`.
Ninety-five focused training/campaign tests pass with three CUDA-only skips.
CUDA shape qualification and the separately approved cloud input chain remain;
no provider is bound.

The exact five-object, 7,424,438-byte upload-only boundary is sealed at
`b24b0b0db1ec876782ec4031a9dd1426f0903e4b0d94f93c284b022bc0b8d58c`.
It permits only create-only GCS upload, generation capture, exact-generation
download, byte comparison, and a sealed local receipt. Navneet approved it;
all five objects uploaded with create-only preconditions and round-tripped by
exact generation. Receipt seal is
`4ab0ab64e896efcb4000abc1125f59eced2534a93cce6d8eeca3fb5a6ecfa88b`.
No Compute or infrastructure action occurred.

The next read-only inspection boundary is sealed at
`b35f9ff928066701a3aa94c2e54eb5e81c1050f984393a0819d9e56479fce4b4`.
It binds ten generation-pinned inputs and allows only provider/input metadata,
exact resource absence, relevant IAM, quota/availability, and price checks.
Navneet approved it, but the first provider read was blocked by required
interactive reauthentication for `admin@executespec.ai`. No cloud mutation
occurred. Resume the same approved plan after `gcloud auth login`; it grants no
mutation or execution authority.

## Six-lane-stratified Gate 4 probe completed; do not promote — 2026-09-10

Navneet approved exact proposal
`8184f4694efdfab2da3b895393caec4c753d6b782f8c810067824f5d957926fa`
with a `$2.25` ceiling. Attempt `20260910T043000Z` completed all 64 optimizer
steps over 640 unique rows and exactly 466,614 tokens. Runtime identities,
training, save/reload, terminal checks, and the 60-row disjoint retention guard
passed. Every lane's retention loss improved; the five-family record-mean loss
fell from `0.2444808341` to `0.2118224695` (13.36%).

The frozen 30-task screen completed 6/30 versus upstream 5/30. Java improved
1→2 and Rust 0→1; Go, JavaScript, and Python were unchanged; TypeScript
regressed 2→1. The adapter passed the improved-family and output-form checks
but failed minimum net +2 and zero lane regression. Decision: `do-not-promote`.
Full development, main training, merge, quantization, and publication remain
prohibited.

Both startup and controller exited 0. Projected compute cost was `$0.2733293`.
All 129 terminal manifest entries independently hash-verified. Terminal
manifest SHA-256 is
`b437b8aece9ae8afef8bc0703efd02e9ef6d3802bc426bc3815af1d61f231551`;
final adapter SHA-256 is
`8bf926578f0e6efe31152fba3f74756b4e93203cf69c57182a9accd5628d60c8`.
Control/recovery generations are `1789016588012192` and
`1789016586942988`; teardown receipt seal is
`ccb72c357494d6b5fa6d897dd7f3c9b256444667a20644330f2530d478125df2`
at generation `1789016873044612`.

The exact VM, disk, subnet, and network are absent in two checks 43 seconds
apart. This Ganesh attempt is GCS-only. The unrelated 200 GiB disk
`laxmi-wmv2-training-01` remains and may bill, so the whole project is not
GCS-only. The local three-way task-transition audit is complete under seal
`074bd2853eb8ed9643fb3311976b5ac773a765766fa98963807b7d57969905b4`:
v3 traded one v2 Go pass for one TypeScript pass while the same three
`collapse-runs` gains and two boundary-condition losses persisted. Do not
scale or rebalance this recipe again. See
`LANE_STRATIFIED_PROBE_RESULT_20260910.md` and
`LANE_STRATIFIED_PROBE_TRANSITION_AUDIT_20260910.md`.

The next diagnostic has begun locally without cloud access. Five earlier v3
checkpoint configs are sealed under manifest
`4c5c8b31d7dbeea1de913c3869fc901d8095036d2251700bf606aa9e5b495f37`,
bound to training evidence
`1393f0fab569e46d71d64273afeac69a91841f9f3c26f39d6248644b73dc4087`
and explicitly marked with no promotion authority. The config builder now
binds an explicit candidate identity rather than reusing the earlier v1 label;
focused build, summary, and host-runner tests pass 14/14. No GCloud action is
authorized or active. The terminal recovery input is now packaged and
reproduced byte-identically at 528,065,805 bytes with archive SHA-256
`260857a3057d1b5943eb540921478345d3c2b2aba6571bb6c51dc5d706d26172`
and manifest seal
`37b9752dadb15d15dcdd6e290c624d4441d9e3467b42b5112b2b8fdfe7b5a865`.
All 130 source files were checked against the terminal inventory before each
build. Candidate-specific workspace and startup construction now reproduce
byte-identically with archive SHA-256
`56e2fda042b6c3fb0e9584151aa54cee1b7f9dad1bbe19037bf7e0a2f6872531`
and controller SHA-256
`32ea79030c0917a0506bb6fe7a3a46f1226cd032f73fd770be21a0cf0b03c87e`.
The extraction/admission rehearsal passed, and focused tests pass 29/29.

The next hard stop is explicit approval of upload-only plan
`8f5eede2e94cddafda84636ab10d81bb2d4d8373289ee1b8bbc3fdde833cbda8`.
It binds six objects totaling 529,256,224 bytes and grants only create-only GCS
upload plus exact-generation roundtrip verification. Navneet approved it and
the upload completed exactly: six immutable generations, 529,256,224 bytes,
and six exact-generation downloads matching local size, SHA-256, and bytes.
Receipt seal is
`6da07f1fcfa4296828e2a8cf406873d1f347d9436fa852f389c09fad087170b1`.
No Compute/network action occurred. Cloud inspection, training, and evaluation
remain unauthorized. The next exact boundary is read-only inspection plan
`a0d283e3b82ac591937905160058f5512e2a8f5766c2b56cd2c508ac13de77bd`.
It binds twelve immutable inputs and four exact planned resource names and
permits only prerequisite reads. Navneet approved it. All reads passed: zone
`UP`, machine/L4 exposed, L4 quota 16 and usage 0, service-account bucket
access present, four planned resources absent, and all twelve exact-generation
inputs matching. No cloud mutation occurred. Report seal:
`fd7e557ac4bb7e17c4c46d3138eaf544087beea5e9be5fe36dd0896c5f23e69a`.

The resulting two-hour Standard L4 proposal is
`7c54481ab57c5538c0d779f6dbb9a51aeb78183684e38185e26aee400bb9867d`,
with provider upper bound `$1.762043024` and absolute ceiling `$2.25`. It is
diagnostic-only, covering five serial checkpoint canaries plus preservation
and teardown. It has no training, checkpoint-selection, promotion, or release
authority and is not executable without exact explicit approval.

## Pre-execution lane-stratified record (superseded) — 2026-09-10

The next bounded mechanism is locally complete and has no cloud authority.
It retains the v2 rank-16 adapter capacity but replaces the five-family prefix
with 64 exact optimizer groups. Each 10-record group contains Go 2, Java 2,
JavaScript 1, TypeScript 1, Python 2, and Rust 2 records and realizes exact
20/20/10/10/20/20 objective mass. The 640 unique training rows total 466,614
input tokens, within 0.4240% of the rejected v2 probe. A separate seeded stream
holds out 60 authorized training-corpus rows, 10 per lane, with zero overlap.

The retention guard allows at most 5% relative supervised-token-mean loss
increase in any lane and no five-family macro increase. The unchanged 30-task
continuation screen still requires two improved families, net +2, and zero
lane regression. Full development and all later gates remain prohibited.

Dataset manifest seal is
`4258e58a4f1d6a46124e413512d7ba436d47eb780582410ecd96cd9a8d0b7404`;
local card seal is
`2ff26cb52a1c630e324891717aae6e8d4ec61615a7d7cf681cbe6704ef0da82d`.
Training/evaluation workspace archive hashes are respectively
`5bfb4616b467690e298fc41c15657ff55cc48631a498860ecd395717af477e15`
and `9e74b86085033c2ab008242cf505c6837c5a9e9b6ac4260b2d93cea395c75346`;
both reproduced byte-for-byte and every archive member matches its manifest.
Focused tests pass 39/39. The full repository suite passes except three known
stale historical Gate 1 workspace/readiness assertions unrelated to this
change. Source commit is `7711fa636cb4b08043518ec1bc97d76aadca889b`.
The fresh four-object/7,399,962-byte upload-only plan
`9c92677248903be640ad6b4905cbba268126659540ac70ac2ee082e9da97fc61`
completed exactly. All objects were uploaded create-only, assigned immutable
generations, downloaded by exact generation, and matched approved SHA-256 and
size. Receipt seal is
`f3e127d0db29b4623fef251e76852ac1c3428fbb67d74ab79eaa1d4b00cf8e4f`.
No compute or infrastructure action occurred. Current state is
`waiting-for-explicit-lane-stratified-execution-approval`. Read-only inspection
plan
`32804a7e859b7567910f62bc4b403fa3781a6d26b826a033775c7174d9526be4`
completed successfully: all four planned resource names are absent, the zone
is `UP`, `g2-standard-8` and `nvidia-l4` are exposed, L4 quota is 16 with usage
0, service-account bucket access is present, and all ten generation-pinned
inputs match. Report seal is
`230e727c55c6323a1dbdeb8a0cacc7ce1ed0ae0ade65eb76d1c8d730b023e8b3`.

The resulting Standard two-hour VM proposal is sealed at
`8184f4694efdfab2da3b895393caec4c753d6b782f8c810067824f5d957926fa`.
Provider upper bound is `$1.762043024`; absolute incremental ceiling is
`$2.25`. It permits only the 640-row probe, retention guard, and frozen 30-task
screen, followed by complete GCS backup, independent recovery, teardown, and
double absence verification. No execution is currently authorized. See
`LANE_STRATIFIED_PROBE_PLAN_20260910.md`.

## Capacity probe completed; mechanism rejected and cloud torn down — 2026-09-10

Navneet approved exact capacity-probe proposal
`461e968ae2fa79d3401e522d52bf91cbcc359cdded68d8fff62dff51631934f0`
with a `$2.25` ceiling. Attempt `20260909T173721Z` trained all 468,601 tokens,
sealed six checkpoints, passed save/reload and every terminal training check,
then completed the frozen 30-task screen. Candidate passes were 6/30 versus
base 5/30: Go +1, Java +1, Rust +1, JavaScript/Python unchanged, and
TypeScript -2. Three product families improved, but net gain was only +1 and
the zero-lane-regression rule failed. The terminal decision is
`do-not-promote`; this capacity mechanism is closed and must not scale.

All 129 terminal manifest entries independently passed SHA-256 verification.
The control archive passed exact-generation GCS roundtrip at generation
`1788981472815348`; the teardown receipt is generation `1788981697224407`.
Projected compute cost was `$0.2664489284483141747466666667`. The named VM,
disk, subnet, and network are absent in two checks 94 seconds apart. The
unrelated `laxmi-wmv2-training-01` disk remains and may bill, so project-wide
GCS-only billing is still false. Gate 4 remains `do-not-promote`. The local
transition audit found four gains and three losses, with three gains
concentrated on `collapse-runs`, plus a training/promotion mismatch:
TypeScript received only 7.17% of the prefix objective even though the gate
protects all six lanes independently. Next work is a sealed
six-lane-stratified recipe with a non-evaluation retention check. See
`CAPACITY_PROBE_RESULT_20260910.md` and
`CAPACITY_PROBE_TRANSITION_AUDIT_20260910.md`.

## Checkpoint sweep closed with four valid checkpoints; no broad transfer — 2026-09-09

Navneet approved exact proposal
`ab86a71a0178d6f7a9232f9ee9dee72650d2fd7dd5568844c10a7ffd68dd1de4`
with the `$2.25` ceiling. Attempt `20260909T130347Z` admitted all sealed inputs
and verifier images, then completed four 30-task checkpoint canaries. Pass
counts at 406,491; 814,098; 1,224,637; and 1,629,235 tokens were respectively
6, 4, 5, and 5. All four run seals and all 120 task bindings independently
validate. The 406,491-token checkpoint gained one JavaScript pass over base;
the later two 5-pass checkpoints gained one Rust pass while losing the base
TypeScript advantage. No completed checkpoint improved broadly across
families, so the evidence rejects premature stopping as the remedy.

The fifth 2,036,559-token evaluation created only its stdout/stderr files and
no task evidence. It remained unchanged for more than 36 minutes despite the
20-minute per-checkpoint timeout, so it is classified as a controller timeout
without a terminal result—not as a model-quality failure. The partial attempt
has no promotion authority. Interruption receipt seal is
`e7f96448ddf96ffb4ac309d9e892c9ff8c125cdeba465258edfff2483db8549c`;
its file SHA-256 is
`41ae1ab624448b568d5d3e229d0bee55eba23b8aa0864235e11570ee98ac0db7`.

All 260 available GCS objects (3,071,483 bytes) were downloaded by immutable
generation and matched their size and MD5 metadata. The full evidence archive,
interruption receipt, and teardown receipt were uploaded create-only and
exact-generation roundtrip verified. GCS finalization receipt seal is
`a7f803fc2d50edba18d42dfcd95fb74de83ff5731dfbedf1d8f04691610f42c5`;
its own generation is `1788964556536552` and its roundtrip file SHA-256 is
`73cb883514f486f82a7414cfaab75bb9a87d2d4d6156e84f809b042a1e88ddd4`.

The exact VM, auto-delete disk, subnet, and network were deleted and returned
404 in two checks 32 seconds apart. Project-wide Compute inventory contains no
instances, addresses, forwarding rules, routers, reservations, snapshots,
images, or machine images. The unrelated unattached 200 GiB disk
`laxmi-wmv2-training-01` remains and may bill; therefore “GCS only” is false at
project scope even though all Ganesh sweep compute billing is closed.

Gate 4 remains `do-not-promote`. Task-level trajectory analysis is complete:
23/30 tasks fail at every measured point and no checkpoint improves more than
one family, so early stopping is rejected. A rank-16, all-attention plus
last-eight-layer MLP capacity probe is locally prepared and passes preflight.
It is bounded to 624 rows/468,601 tokens and has continuation-screen authority
only. The exact four-object/6,729,319-byte upload-only plan completed with all
assigned generations downloaded and byte-verified. Receipt seal is
`ad5c9ae541bc0ef53a0c0fdbdb9a49512e002a01920ee95e3d927fb6c4464e01`.
Current state is
`waiting-for-capacity-probe-pricing-and-resource-inspection-approval`.
No compute or infrastructure action occurred. Provider price/resource checks,
executable-card binding and VM execution remain separately unauthorized. The
exact read-only inspection plan seal is
`50b3783cb1287bfa3a44e00772db6f24bfd2b70b8d102b1b9f537276042fd521`.

## Corrected checkpoint-sweep VM proposal awaiting approval — 2026-09-09

Upload-only plan
`356dc0403d6ccc82683774bb3d381280bbc87b432e1f1116cb9b0a12a7b7f769`
is complete. Exactly three corrected objects totaling 1,161,309 bytes were
uploaded create-only and exact-generation roundtrip verified; no compute or
infrastructure action occurred. Generations are archive `1788958259527767`,
manifest `1788958261099778`, and startup `1788958261821760`. Receipt seal is
`45a61f7866b0966dba7ec00cd7d49304be6cb13b3acaa764ea272c69f3fc224e`.

The ten-input binding seal is
`58df54d10772db3655cd25d42f8068779d9a226853e3b7c8df35da87499be0fa`.
The replacement diagnostic-only VM proposal preserves one Standard L4,
7,200-second maximum, no external IP, auto-delete disk, `$1.762043024`
provider upper bound, and `$2.25` absolute ceiling. Its seal is
`ab86a71a0178d6f7a9232f9ee9dee72650d2fd7dd5568844c10a7ffd68dd1de4`.
No compute action is authorized until that exact proposal and ceiling receive
fresh explicit approval.

## Checkpoint-sweep first attempt closed; corrected v2 local — 2026-09-09

The one execution authorized by proposal
`b31d95b6e9097fa1056a522628773240d0c2d80ebd925becf457163b28900db5`
is consumed and closed. Its temporary Standard L4 VM reached the packaged
workspace check, then failed before verifier preparation, model loading, and
evaluation because the runner expected the wrong workspace schema. Exactly
zero evaluation tasks ran, so this attempt contributes infrastructure evidence
only and does not change the final-checkpoint `do-not-promote` decision.

Raw terminal files and a sealed failure receipt were preserved. The terminal
inventory cannot authenticate the final `startup.stderr.log`, because backup
logging appended after inventory creation; this limitation is explicit in the
receipt. The VM, auto-delete disk, subnet, and network were deleted. The sealed
teardown receipt records two 404 absence checks and passed an exact-generation
GCS roundtrip at generation `1788953722389669`, SHA-256
`31331677c10eb0b4ab653bfe25d7544d1c32f518350dfa8a23d568214e85a448`.
No Ganesh compute resource from this attempt is active.

Both defects are fixed locally. The host runner now binds the dedicated
checkpoint-sweep schema. Startup restores its original output descriptors and
waits for both log `tee` processes before hashing terminal files. The rebuilt
workspace contains 596 files: archive SHA-256
`fd1cee18029e53644ba3c694558b52cbca9e91c5a5e47a9150d6f8b73240e441`,
manifest file SHA-256
`6c11b79d4dfb099c5f97cebd10eee3b114c06369199eac613f7612dd235b7264`,
and internal manifest seal
`bf8f11a413425d0c2f530db8db0a0de3f88a4bb2cf335fffac6b155aa342f816`.
It has no GCS generation or provider authority. The fresh three-object,
1,161,309-byte upload-only plan is sealed at
`356dc0403d6ccc82683774bb3d381280bbc87b432e1f1116cb9b0a12a7b7f769`.
No new GCloud action is authorized until that exact seal is explicitly
approved.

## Checkpoint diagnostic locally prepared — 2026-09-09

The lowest-cost recovery diagnostic is locally prepared. Five unmeasured
quarter-epoch adapters are bound to their sealed checkpoint manifests and the
completed training run; the sixth/final checkpoint already has executed canary
evidence. The five diagnostic configs are sealed under manifest
`6af2ad473e2d119bcf1149540705a3d7faaf7f4584b1b7626bf568cabfec4b5c`.
Evaluator checkpoint binding and the diagnostic-only summarizer pass 16 focused
tests. The sweep has no promotion authority and cannot alter the terminal
`do-not-promote` result.

No cloud resource is active. A new evaluation-only GCloud execution would need
a fresh exact approval. The planning envelope is one Standard L4 for at most
two hours, no external IP, restart disabled, auto-delete disk, and a proposed
$2.25 incremental ceiling. The controller/startup package and provider proposal
are not yet executable. The unrelated `laxmi-wmv2-training-01` disk remains a
separate project-wide billing decision.

## Gate 4 expansion pilot completed; candidate not promoted — 2026-09-09

The 3,225-row BF16 LoRA expansion pilot completed 2,438,853 training tokens in
3,501.756 seconds. Its terminal training verifier passed all eight checks,
including immutable card/config identity, completed training, save/reload,
VRAM and cost bounds, and adapter identity. Training evidence seal is
`3f589131eee6b214013e41cf6e81d6b7bab41b216586c93f3ddc4d29db704158`;
terminal report seal is
`6a09478412aad9200097b8142b498c112b60fa0e6c35ba82328f1a61b06fee13`.

The frozen 30-task canary completed 30/30. The exact base passes 5/30 and the
candidate passes 6/30: Go 0, Java 1, JavaScript 1, TypeScript 2, Python 1,
Rust 1. Net gain, zero lane regression, non-code, truncation, and save/reload
checks pass. Only one of five product families improves, below the frozen
minimum of four. The terminal decision is `do-not-promote`, report seal
`3d53bc8b484f295823344984ca37e4dc87c842452aaa3c20ceb5d02d661d249d`.
The complete 180-task development run was correctly not started.

The first adjudication attempt exposed one pre-existing invalid seal among the
180 frozen base task files: `dev-t2-javascript-decode-hex`. It is outside the
30 selected canary tasks. The adjudicator now validates exactly the candidate-
selected base evidence and has a regression test; all 30 selected base seals
and all 30 candidate seals are valid. The frozen base file itself remains
unchanged and must be repaired through a separately versioned evidence action
before any release claim that depends on the full 180-task baseline.

The complete 128-object/56,925,573-byte terminal backup, a 51,674,173-byte
recovery archive, finalization receipt, and teardown receipt all passed exact-
generation GCS roundtrips. The VM, auto-delete boot disk, subnet, and network
were deleted and twice returned 404. There are no project instances, addresses,
forwarding rules, routers, reservations, snapshots, images, or machine images.
One unrelated unattached 200 GiB balanced disk, `laxmi-wmv2-training-01`,
remains in `us-central1-a`; therefore Ganesh compute billing is closed, but a
project-wide GCS-only billing claim is false pending an explicit owner decision
on that disk. No further training or release promotion is authorized by this
pilot result; change data or mechanism before scaling.

## Gate2 and Gate4 input GCS backup verified — 2026-09-09

Authentication is restored. The terminal Gate2 evidence archive and rehearsed
Gate4 training workspace were uploaded create-only to the established evidence
bucket, then downloaded by exact object generation and compared byte-for-byte.
Gate2 generation `1788908479441360` has SHA256
`b49fcf31fa20afa6fa7cc0a3d79db572001cdcc8e5b562c9841469064d505845`;
Gate4 input generation `1788908484381745` has SHA256
`72e366aa7274723f4c89bb819780a4972a014ac0a2b9b94db4f56955bfaebb3e`.
The sealed receipt was itself uploaded and roundtrip-verified at generation
`1788908613275676`. This proves evidence durability only. No VM or compute
resource was inspected, created, or started.

## Gate4 local execution package rehearsed — 2026-09-09

The one-recipe expansion pilot is now locally preflighted and archive-rehearsed.
Its immutable card is `prepared-not-executable`, with zero failed local checks;
it binds the 3,225-row prepared corpus, 2,438,853-token ceiling, BF16 LoRA at
1e-5, quarter-epoch checkpoints, six-hour wall limit, and frozen 30/180-task
evaluation sequence. Card SHA256 is
5d1307c342cf837d5b908ea2579fcad7dfe91b0708d485c08fd498118ded8b7e.
The frozen canary rule requires a net pass gain, improvement in at least four
of five product families, zero per-lane pass regression, no increase in
non-code or truncated outputs, and a passing save/reload proof.

The reproducible training workspace contains 44 allowlisted files and was
successfully extracted and re-preflighted with the same card seal. Archive
SHA256 is 72e366aa7274723f4c89bb819780a4972a014ac0a2b9b94db4f56955bfaebb3e;
manifest seal is a00963ed3d4832793bc2bc98cda0155dc5ea35612a44960b3be368a9b04d72c1.
The workspace now includes a fail-closed terminal verifier for the executable
card, complete run, token/cost/VRAM bounds, save/reload proof, and exact adapter
file hashes.
The post-training canary boundary is also implemented: it compares the exact
30 candidate task-evidence seals against their admitted base counterparts and
permits the 180-task run only if the frozen four-of-five-family, net-gain,
zero-lane-regression, non-code, and truncation checks all pass.
The evaluation-config builder now emits separately hashed 30-task and 180-task
candidate configs only from a passed terminal training report and byte-identical
adapter. Its manifest marks the canary ready and the full evaluation blocked
until the sealed canary adjudication promotes it.
Provider price, cost ceiling, zone, and a fresh explicit GCloud execution
approval are intentionally absent, so the package cannot authorize cloud
execution. GCS evidence upload remains blocked on interactive authentication.

## Gate4 training package prepared — 2026-09-09

The terminal3225-row source corpus is prepared with exact Qwen response-only
rendering and unique-row five-family objective weighting. Prepared train has
2,438,853 input tokens and SHA256
0e7111f51c8ec6e7dcf23ee96ea4873b03ae944ce51aaab4aed6782493133224;
the50-row validation set SHA256 is
6a9d3aa37b30bc2672517f6d63113011de5f8156aa1049e588fdc70a36b77f46;
manifest seal fc7409c3e68e372e1b1c05b07e5c36db0e3923c84731fe70a0f7937cfd413c25.
All six objective shares match their exact20/20/10/10/20/20 targets. No cloud
compute is active. GCS evidence upload remains authentication-blocked; local
Gate4 execution-card/controller preparation can continue independently.

## Gate2 corpus sealed; pilot throughput resolved — 2026-09-09

Gate2 pilot-entry sufficiency and throughput are now measured. The terminal
3073 retained originals plus152 admitted recoveries total3225 rows and2,438,853
input tokens, 5.288x seed-pilot volume. Every row fits the2944-token envelope;
maximum2659. The immutable source corpus is sealed at SHA256
4254b6f82323421edbbece17fe1a0eb43a622c697059921afbf34aca600b949d and
is sufficient for one bounded pilot. The former4000-row pilot-entry floor is
retired; this does not waive correctness, separation, token weighting, corpus
sealing, executable promotion or release gates.

Executed repaired-L4 throughput is295.541 input tokens/second. Corpus training
projects to2h26m expected or3h14m at75% rate; canary approximately5m,
full development evaluation approximately29m. Six hours is the recommended
runtime ceiling including the final30m backup reserve. No new GCloud action is
authorized. R26 review and diagnostics are terminal:21 corrections passed both,
four are held across static/executed review. Together with two R24 positives,
the latest admission accepted23/rejected0, raising actual admission to152.
Gate2 source-corpus closure is complete. Next is local Gate4 response-only
training-package construction and objective-weight verification.

## Admission129 — 2026-09-08

20 additional recoveries admitted with zero rejected: R21/R22 adds3 and R23
test-only correction adds17. Cumulative129: Go23, Java19, JavaScript22,
TypeScript22, Python21, Rust22; generation118/repair11. Maximum combined3202,
minimum gap798 before exclusions and token balancing. Gate2 remains open; no
corpus/training/release seal. See RECOVERY_ADMISSION129_20260908.md.

All17 R23 candidates passed terminal static review and fresh serial sandbox
directionality. R22 unconditional positives are only Go0218/0180. R22 Java
repairs remain excluded for exact approved prompt-scope discrepancies; passing
semantics do not waive lineage/scope. R22 Go0095 race directionality passed but
its test-quality hold remains. Verified GCS archive and receipt now cover
admission129 plus terminal R21/R22/R23 evidence, each verified by exact-generation
download and byte comparison. See RECOVERY_ADMISSION129_BACKUP.md. No cleanup or
billing certification.

## Admission109 — 2026-09-08

41 recoveries admitted since checkpoint68, now109 total: Go21/Java19/JS18/TS18/
Python17/Rust16; generation99/repair10. Maximum combined3182, minimum gap818
before exclusions/token balancing. No corpus/training/release seal. See
RECOVERY_ADMISSION109_20260908.md for exact output and executed evidence.

R20 Rust0487 remains excluded by original-parent compile-control failure, not
misreported as semantic proof. R21 generation33 active; Java lane failed the
exact embedded broken-source integrity guard, with raw output preserved. Other
lanes continue independently. Terminal evidence backup through109 in progress;
Both archive and receipt now verified by exact-generation download and byte
comparison; see RECOVERY_ADMISSION109_BACKUP.md. No cleanup performed.

## Admission93 — 2026-09-08

Combined r15/r16 admission completed25 accepted/0 rejected. Cumulative93:
Go21, Java19, JavaScript11, TypeScript12, Python15, Rust15; generation85/repair8.
Maximum originals plus recoveries3166; minimum remaining834 before exclusions
and token balancing. No training/corpus/release seal. Latest verified backup68
does not yet cover the latest25; preserve for next terminal backup.

R17/R18/R19 serial diagnostics active after admission; main has integrated their
quality reviews. R20 two corrected candidates generated and main-reviewed; Rust
original-control missing traits must remain compile evidence, not semantic proof.
R21 main-approved33 new parents generating with at most3 lanes; selection note
records exact hashes and three narrow contract clarifications. Unique reserved
parents153. Exact current jobs and next steps remain in HANDOFF.md.

## Admission68; next25 in execution — 2026-09-08

68 recoveries are admitted: Go12, Java14, JavaScript11, TypeScript12, Python10,
Rust9; generation60/repair8. Original holds2812 remain unchanged, leaving at
most3073 original rows. Maximum combined3141; minimum gap859 before additional
exclusions and family-token balancing. No final corpus/training/release seal.

Admission68 archive and receipt are backed up to GCS and independently downloaded
by exact generation with byte-for-byte comparison. See RECOVERY_ADMISSION68_BACKUP.md.
Later quality reports/diagnostics and r17-r19 outputs need the next terminal backup.

R15 sixteen plus R16 nine have passed main-integrated quality review, behavioral
directionality and overlap preparation. Combined25 admission now running; do not
count it before the terminal report. Earlier prepared r15-sixteen-v1 is superseded
by combined r15-r16-twentyfive-v1 and must NOT be admitted separately.
R17 all13 JS/TS corrections and R18 two repairs are main-reviewed static positives;
fresh diagnostics are queued after admission25. R19 two reference repairs retain
test-coverage/scope holds; one bounded correction proposal is being prepared.

Gate2 remains active. Working, not permission-blocked; no new VM or training run.
Training50% and release35% are estimated milestone progress, not measured scores.
Exact jobs/assignments in HANDOFF.md; full-delivery ETA remains ungrounded until
corpus sufficiency and a measured pilot. Existing GCS backups approved; new
GCloud compute requires a scoped authorization and cost ceiling.

## Admission60 — 2026-09-08

R11 adds10actualadmissions: cumulative60 (Go12,Java12,JS11,TS11,Python8,Rust6),
generation53/repair7. Max combined3133,min remaining867 before exclusions/token
balance. See RECOVERY_R11_ADMISSION60_20260908.md. No corpus/trainingseal.
LatestverifiedGCScheckpoint50 excludes theselatest10/r11diagnostics; preserve
fornextbatchbackup. R12generation, first27serialdiagnostics andthree disjoint
reviewersactive. Approvedr13/r14 correctionsnotyetlaunched. ExactqueuesHANDOFF.

## Recovery admission50; accelerated r12 active — 2026-09-08

Cumulative50 recoveries admitted, allgeneration: Go11,Java12,JS9,TS7,Python8,
Rust3. Latest25 accepted/0 rejected after independent quality, fresh controls,
retained/prior-recovery dedup and546-file evaluation separation. Go0439/0522
also passed actual pinned race qualification. See RECOVERY_ADMISSION50_20260908.md.
Original5885/holds2812 unchanged; maximum combined3123, minimum additional877
before further exclusions and token balancing. Candidate balance is false;
no final corpus seal, no training/release promotion.

R11 partial generation12 completed (Python lane strict-ID failure preserved).
All12 reviewed:10 static positives, Rust0102 compile hold and0361 bounded-witness
hold; actual serial diagnostics active. R12 main-approved51 generation requests
are running with3 lane workers. Main read all three disjoint reviewer proposals
and validated exact hashes; TS0241/0242 are explicitly deferred, not reserved.
Current exact session/backup/assignment state is in HANDOFF.md. No new VM usage;
existing GCS backup approval remains. Training/release estimates50%/35% only;
full-delivery ETA awaits corpus sufficiency and measured pilot throughput.

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

Last updated: 2026-09-06

## Current gate

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

Latest: 131 holds / 164 outside-sample inspections; batch 11 partial through
position 155. GCS verified through 129 holds, later five inspections pending.
Continue at 156. Frozen sample unchanged; no training seal or new VM.

Backup update: batch 10 / 129 holds now GCS roundtrip verified;
`QUALITY_STRATUM_129_BACKUP.md`. Subsequent reviews remain separate.

Latest: **129 holds (126 additive plus historical three)**; 159 unique outside-
sample targeted inspections plus unchanged 300 sample. Batch 10 preserved;
continue array-hit position 151. GCS verified through 119 holds, batch 10 pending.
No new VM, revised partition or training seal. Earlier checkpoint history follows.

Current: **119 holds (116 additive plus historical three)**; 144 unique outside-
sample targeted inspections plus unchanged 300 sample. Array batch 9 preserved.
GCS verified through 110 holds / v3 scope; batch 9 pending. All 97 tooling tests
pass. No new VM, revised partition or training seal.

Systematic review scope v3: nine groups / 14 strata / 3,085 records, not
automatic rejections. Key-storage and required-property copy findings included.
All 97 tooling tests pass; v3 scope awaits its GCS checkpoint.

Current: **110 holds (107 additive plus historical three)**; 129 unique outside-
sample targeted inspections plus unchanged 300. Array batch 8 preserved. GCS
verified through 104 holds; batch 8 pending. No training seal or new VM.

Backup update: 104-hold checkpoint (through array batch 7) is GCS roundtrip
verified. See `QUALITY_STRATUM_104_BACKUP.md`; later evidence remains separate.

Current: **104 holds (101 additive plus historical three)**; 114 unique outside-
sample targeted inspections plus unchanged 300 sample. Array batch 7 preserved.
GCS verified through 96 holds; batch 7 pending. All 97 tooling tests pass.
No new VM, revised partition or training seal.

Current: **96 holds (93 additive plus historical three)**; 99 unique outside-
sample targeted inspections plus unchanged 300 sample. See array batch 6.
GCS roundtrip verified through 89 holds; batch 6 pending. All 97 tooling tests
pass. No new VM, revised partition or training seal.

Current: **89 holds (86 additive plus historical three)**; 84 unique outside-
sample targeted inspections plus unchanged 300 sample. Array batch 5 records
four new holds and a passing regex control; unresolved API scope is separate.
GCS verified through 78 holds; later batches pending. No seal or new VM.

Current: **85 holds (82 additive plus historical three)**; 69 unique outside-
sample targeted inspections plus unchanged 300 sample. Array batch 4 preserves
latest findings. GCS verified through 78 holds and v2 scope; later batch pending.
All 97 tooling tests pass. No training seal, revised partition or new VM.

Current: **78 holds (75 additive plus historical three)**. Fifty-four unique
outside-sample targeted inspections; array batch 3 is recorded in
`cutoff-5885-review/ARRAY_STRATUM_REVIEW_3.md`. Initial sample remains 300.
No new VM, generation, partition or training seal.

Scope update: seven groups / 13 strata / 3,056 records require review, not
automatic rejection (`stratum-followup-inventory-v2.json`). All 97 data tooling
tests pass. GCS verified through 72-hold checkpoint; v2 scope postdates archive.

Current: **72 holds (69 additive plus historical three)**. Forty outside-sample
targeted inspections plus unchanged 300 initial sample; see
`cutoff-5885-review/ARRAY_STRATUM_REVIEW_2.md`. Nine new reproduced failures and
one passing parcel-filter control. No new VM or training seal.

Current: **63 holds (60 additive plus historical three)**; see
`cutoff-5885-review/ARRAY_STRATUM_REVIEW.md`. Twenty-five outside-sample targeted
inspections now accompany the unchanged 300 initial inspections. All 92 tooling
tests pass. GCS verified through the 53-hold checkpoint; later array review
awaits next backup. No training seal, revised partition, or new VM.

Latest targeted follow-up: **53 holds (50 additive plus historical three)**.
Ten outside-sample pattern inspections, ten sandbox-confirmed failures on eight
new held records, one passing first-match control; see
`cutoff-5885-review/TARGETED_STRATUM_REVIEW.md`. Initial sample remains 300.
No new training seal, partition or VM. Next backup must include this follow-up.
Earlier checkpoint details follow.

Latest follow-up: 45 holds (42 additive plus three historical). Initial sample
inspection complete; six recurring groups reopen 11 strata containing 2,567
records for review, NOT rejection. See `cutoff-5885-review/STRATUM_REVIEW.md`.
All 86 data tooling tests pass. Initial 300/41-hold evidence is GCS roundtrip
verified; subsequent sparse/stratum work requires the next backup checkpoint.
No training-ready seal. The preceding checkpoint follows.

Initial inspection complete: 300/300 frozen sample records. Go 56, Java 60,
JavaScript 30, Python 61, Rust 62, TypeScript 31. Archived provenance also
traces all 300, but neither count is seven-criterion approval. There are 38
additive holds plus three historical holds (41 total), not a revised admission
count. Repeated sparse validation, subscription identity, reference/test API
accommodation and numeric-envelope findings require affected-stratum review.
Details: `cutoff-5885-review/FOURTH_BATCH_REVIEW.md`, `additional-holds.json`.
Seven new TypeScript diagnostic failures are sandbox-confirmed; CSS terminal
newline concern was disproved. All 82 data tooling tests pass. Continue quality
adjudication and targeted audits. No training seal, new partition or new VM.

Historical 100-record checkpoint:

Quality continuation: 100/300 records inspected (frozen indices 0–99), with
archived test provenance traced for all 300: 297 original unchanged tests and
three specification-only critic chains. Go generation 0058 is held after its
known-bad passed the original tests 2/64 times in a pinned sandbox repeatability
probe; reference control passed 64/64. New confirmed reference defects: Go
0330/0720/0791 and Java 0514/0794. Static contract/test holds: Java 0549/0080.
Eleven total holds including historical exceptions imply 5,874 remaining before
open findings are adjudicated; this is not a new partition or admission count.
The historical v1 partition remains unchanged and cannot be sealed as-is.
See `cutoff-5885-review/SECOND_BATCH_REVIEW.md`; 200 semantic reviews remain.

Latest override, 2026-09-06: native CPU verification completed all 5,885 rows
in 12,031.077 seconds. 5,883 passed; two Rust reference executions timed out.
Navneet directed separate review of flagged records, not treating the campaign
as an overall failure. The original strict-seal report remains unchanged.
An independent Go quality defect is also held out, leaving 5,882 rows in
`datasets/cache/expansion-v1/review-partition-v1/review-eligible.jsonl`.
This historical partition is not training-ready; current review counts are above.
Do not restart generation or the superseded laptop final-admission job below.

All 13 VM artifacts were checksum-verified from GCS before the campaign VM,
disk, network, and subnet were deleted. Two project-wide Compute inventories
are empty. Cloud Asset API is disabled; broader GCS-only billing certification
remains unresolved. No VM remains to stop or reuse. See the handoff for the
additional full-history backup and follow-up service inventory.

Latest update, 2026-09-05: Navneet closed construction at 5,885 rows and
authorized validation of that cutoff. Production is stopped; batch 144 is
preserved but excluded. The cutoff snapshot SHA-256 is
`3ca9209b51d36b9137d65f6f0424bfc369a662bd5af7f99666f4ecc60ee24e92`.
All rows resolved to original executable candidates. A separate cutoff config,
manifest, and deterministic 300-row sample are prepared under
`datasets/cache/expansion-v1/cutoff-5885/`. Serial final admission has been
launched under `com.ganesh-mini.cutoff5885-final-admission`; execution and
quality review are pending. Historical counts and 6,000-row targets below are
superseded by this user-authorized cutoff. No training-ready seal exists yet.

Initial quality review has inspected 3/300 sample records and confirmed a
reference/test gap in Go ticket-registry record `exp-v1-go-generation-0165`:
Consume before start deletes a future ticket. A new independent sandbox test
failed with exit 1 and no timeout. Findings and raw evidence are under
`measurement/data/expansion-v1/cutoff-5885-review/`. This must be resolved;
the remaining review is incomplete and full execution continues separately.

Gate 3 is now in source-driven data construction, not another seed retry. The completed
`1e-4` seed pilot passed 13/180 versus the exact base's 20/180, so more epochs
on the 1,399-row corpus are not justified. Expansion v1 is frozen at 6,000
execution-verified rows with five-family 20% balance and a 60/40
generation/repair mix.

The expansion schema and fail-closed admission pipeline are implemented. They
require pinned source rights, independent behavioral tests, a passing
reference, rejection of every known-bad implementation, exact code and
exact/fuzzy prompt separation from all 546 frozen task manifests, within-corpus
deduplication, and exact final quotas. The pinned McEval-Instruct and
MdEval-Instruct snapshots are hash-verified drafting sources under
CC-BY-SA-4.0 and MIT. Their answers and tests are never trusted: Codex creates
a new self-contained task and an isolated test author sees only the transformed
specification. NVIDIA OpenCodeInstruct remains admitted only as a Python
drafting source.

Teacher preparation now uses authenticated Codex CLI 0.144.4 with
`gpt-5.6-sol`, medium reasoning, ephemeral schema-constrained runs, and
separate isolated architect and test-author contexts. The naive qualification
admitted 1/6 rows; explicit runtime contracts admitted 4/6; isolated architect
and test critics brought the final combined qualification to 6/6 with zero
tool events. The final admission report seal is
`0aeedf655a23eacf67cab8d10bf8a4a40e3366c94b779f1734c8b22aa3dece36`.
The 60-row, ten-per-lane tranche is complete. Generation had zero CLI failures
and zero tool events. First-pass executable admission accepted 46/60; one
targeted repair pass changed only the fourteen rejected rows and produced a
final combined 52/60 result with no cross-batch overlap: Go 8, Java 7,
JavaScript 10, TypeScript 8, Python 9, and Rust 10. The admission report seal
is `4324d30331b872e9650c921b018561e16d275b36c2e729b4caf35f74a11ab547`.
A deterministic one-per-lane manual quality sample passed. The source-driven
pilot then generated 80 rows across all lanes, including a second TypeScript
and Rust tranche. After exactly one targeted correction pass, 71/80 were
admitted (88.75%): Go 9, Java 9, JavaScript 10, TypeScript 17, Python 10, and
Rust 16; 41 generation and 30 repair. Cross-batch exact/fuzzy collisions were
zero and the deterministic one-per-lane manual review passed. The pilot is
sealed by `a69cbdd35f2de099eb009a6e82eee53efc33c9951863b2d58f14a1b26d888a77`.

The first correction implementation lost McEval/MdEval lineage on changed
rows by rebuilding them under the Codex source identity. Scale stopped. The
repair path now preserves the original source object; pilot rows were
deterministically restored with explicit evidence and re-executed. Their
acceptance counts reproduced exactly. No old admission report was relabelled.

An adaptive 8,480-row reserve queue is sealed at
`a020b6f66a40688547b71052d5123252102eb91d51f69196bef9a70d7dc9ac78`.
It is a ceiling, not a mandate: the resumable controller stops each lane/task
stratum at the frozen 6,000-row quota and admits only execution-verified rows.
Production reached 5,585 rows under SHA-256
`61d897579d024cf33b3897ca39b4bf06526ac176da5369e8815a3ddfc6b38860`
when the admission-capacity change was prepared. Live state later reached
5,608 rows (Go 808/1,200) with corpus SHA-256
`a8419804a375107d8294a4777aafa6b371c23a4983389f09938bfbc9161770db`
before the timeout-classification defect was diagnosed.
Java, JavaScript, TypeScript, Python, and Rust are complete; Go is the sole
remaining lane. The attempted four-record/eight-verifier configuration caused
repeated emulated-AMD64 task timeouts beginning with Go batch 98. Because
explicit timeouts were missing from the infrastructure classifier, those runs
were incorrectly recorded as behavioral failures and sent to correction;
batches 105 through 110 admitted zero. They are not valid teacher-quality
evidence. Production defaults to one record and one verifier container after
a two-container retry of batch 111 also exhausted the task deadline. A timeout
that persists under serialization remains behavioral; batch 111 exposed a
malformed test file rather than a host failure. Exact
old candidate and teacher evidence is preserved for bounded recovery rather
than relabelled.

The missing deterministic 5% production-quality sample builder is implemented
and covered by focused tests. It will select exactly 300 rows stratified by
lane, source, task type, and correction history only after state is complete,
the corpus/state hash matches, and all frozen quotas are exact. No GCloud
resource is used or authorized for this phase.

Production reached 5,769/6,000 rows after exact recovery of Go batch 128:
Go generation 564/720 and repair 405/480. The corpus SHA-256 was
`1a99cd89e3172300d4aadd1d10cb24b383ca9f6de581223f4aef310e2eb499c5`,
matching state, with zero aggregation rejections. Batch 128 had failed before
commit because verifier output contained invalid UTF-8. Verification now
captures Docker output as bytes and stores non-UTF-8 output losslessly in a
base64 envelope. Recovery reused the exact candidate and teacher artifacts,
admitted nine rows on the first pass, and admitted the remaining behavioral
rejection after the one permitted correction. The single local controller was
then resumed on batch 129. GCloud remains untouched and unauthorized.

Gate 3 continuation attempt `20260827T113051Z` is fully finalized as a strict
sealed bootstrap failure. It had exactly one boot, automatic restart was
disabled, and it stopped after roughly nine minutes. Every immutable input
download passed its hash, the offline Docker stack and qualified CUDA image
loaded, but the host controller failed at its first project import because
direct file execution omitted the archived workspace root from `sys.path`.
The completed `1e-5` candidate was not imported or modified; CUDA model work,
canary evaluation, `3e-5` training, LR selection, and full development
evaluation did not begin.

Terminal backup, strict finalization, four-resource absence, and final
post-delete backup passed under seals
`206a9f8fa0c13a282614524675449712f03ae0dfdd3d44760f51b21c8958d30d`,
`63d08fa9b7be8dc2af81e4d0e228f227077f34a5f303a67435129fac3a7b7978`,
`db8c975853b9e7812b87cdaffb1c0af697e7e09cc2f502a4faae115f0abbc3f8`,
and `6526129fc7289a6dcdf52c32f855c75dc2240b055f490e8f6c0eb029f34c4633`.
The VM, disk, subnet, and VPC are absent, and the campaign monitor is paused.

The local repair now bootstraps the host controller's repository root before
project imports and independently supplies the archived workspace in
`PYTHONPATH`. Runtime-bundle rehearsal executes the archived entrypoint under
isolated Python with caller `PYTHONPATH` removed. The rebuilt evaluation
workspace, deterministic archive, runtime rehearsal, and non-executable
preparation seals are
`c0e1938c7d9574aaae128a787d38c41f3549b56bb9be99fae2f08c3e5008ff05`,
`3c738bf40fe3cda1fb62b4ae7b0d88da265a8318f082c63d91527cfb7c9cc6ef`,
`9c07e39823095cd93f26b580f238ecf9c5f23ad7c3d3d924109dd2f74fba93c1`,
and `915ddc4fdd90641283b9c49f3025f8519dda48c0f208582a566a1d1e623d9eb9`.
The consumed approval authorizes no retry.

Gate 3 v2 attempt `20260827T090603Z` is fully finalized as a strict sealed
failure. The first boot encountered a bucket-IAM 403 before model loading or
optimizer progress. Granting the run's default Compute Engine service account
bucket-scoped object access and resetting the same VM repaired that bootstrap
failure. No training state was resumed or reused from the failed boot.

The `1e-5` candidate then completed the frozen unique epoch: all 1,399 rows,
461,235 input tokens, 242,406 supervised response tokens, and 175 optimizer
steps in 1,560.65 seconds. Save/reload equivalence passed with zero maximum
logit difference. Its five-family validation record mean improved from
`0.3703169807` to `0.3598691403`, and its supervised-token mean improved from
`0.3766998041` to `0.3665855866`. These are diagnostic loss improvements, not
executable promotion evidence. The complete training result is sealed by
`d885af11f3c7346959b2fcfadd6b77c6009bca99410f527038f923ad09f1c5a0`;
the final adapter file hashes include
`6a6ccf88c85a5c16d3569bdedc8ccb5662eeb79f583006a777c7ba2d2f51fc8d`.

The first 30-task canary failed after generating five Go responses because the
host had loaded only the CUDA model image. The six pinned verifier images had
historically been loaded as a side effect of rerunning Gate 1; the Gate 3-only
path correctly reused the canonical Gate 1 result and therefore skipped that
side effect. Docker reported `No such image: ganesh-mini-go-verify:amd64-v1`.
This is an orchestration defect, not a model-quality result. No canary score is
admissible, `3e-5` did not train, LR selection and the 180-task evaluation did
not run, and the current evidence cannot decide whether the seed data is
sufficient.

The repaired campaign now loads, identity-checks, and audits the complete
verifier archive before any paid training. Unit coverage rejects a missing
image load, and the archive-executed rehearsal proves verifier preparation
precedes candidate work. The current continuation seals supersede the earlier
repaired full-campaign fallback seals and are recorded below.

The independently generation-pinned 75-object terminal backup passed under
seal `93d7206401744b7c66e55800352f87a2204d084ae88119d3f6c5038b769f9fb5`.
Terminal validation is `sealed-failure` under
`8adbed352c7e1799468262097225f84a4488736e98c294cce038e8f524b76986`.
The strict deletion gate, exact four-resource absence proof, finalization, and
14-object final post-delete backup are sealed respectively by
`ae8c7556d08ecfeb05b208f95bbd8859cf1a76932230457a27065216209e2086`,
`ecf74ca24bb77c8ccb833326ada8ba6dc5e00dca94d499c1ab6c94271884c394`,
`efb4e971c58873a09ee7575cd17916c1baf951e7ce093c5d82aab89cba6dfc6d`,
and `fea0b331acd56baf7eefcb6591656c3c76f35c5da2313f507380792a32c6fc37`.
The exact VM, boot disk, subnet, and VPC are absent. The run approval is
exhausted; another GCloud execution requires a fresh explicit approval.

The local Gate 3 continuation is now prepared. It does not retrain the valid
`1e-5` epoch. A deterministic 2,711,227-byte bundle contains its final adapter
and run evidence, and is sealed by manifest
`5b882126fe59fcd28f6b1e9ffe578929b0b65ac0bd39fbd029f0baa0e3f325a7`
and archive SHA-256
`95a4a1054bab679dfd3255b752eac01ff3c6d42467304348a8ecff048dc998da`.
The packager proved every included file against the prior generation-verified
terminal backup and source execution/terminal seals. Runtime import then
rechecks the current frozen config, data manifest, model revision, recipe,
epoch size, save/reload result, and adapter hashes before evaluation.

The continuation loads and audits all six verifier images before candidate
work, evaluates the imported `1e-5` canary, trains only `3e-5`, evaluates its
canary, applies the frozen LR selection, and fully evaluates the selected
candidate. The provider contract now disables automatic restart so no VM
reboot can silently restart training. Before any resource is created, the
launcher verifies that the exact VM service account
`1061994342941-compute@developer.gserviceaccount.com` has bucket-scoped object
read/write access; this closes the gap that caused the earlier bootstrap 403.
Its proposed bound is three VM hours,
including a 30-minute terminal-backup reserve, and USD 3.50. The evaluation
workspace, archive, runtime rehearsal, and non-executable preparation seals are
`c0e1938c7d9574aaae128a787d38c41f3549b56bb9be99fae2f08c3e5008ff05`,
`3c738bf40fe3cda1fb62b4ae7b0d88da265a8318f082c63d91527cfb7c9cc6ef`,
`9c07e39823095cd93f26b580f238ecf9c5f23ad7c3d3d924109dd2f74fba93c1`,
and `915ddc4fdd90641283b9c49f3025f8519dda48c0f208582a566a1d1e623d9eb9`.
The deterministically rebuilt training workspace archive and manifest are
`684cb5824d4a5b253a747b8ecb41d0d083316560aac2eb8fe20d8f80a39bcd13`
and `8c8e90ed40938dbe55627e6d2b7c2918ee7334e41097c0ebd2d9372aa0cfcbe8`;
their only substantive downstream change is the repaired v2 run-evidence
schema.
It is still `prepared-not-executable`: fresh price/quota preflight,
VM-service-account IAM verification, generation-pinned uploads, an executable
card, and explicit GCloud approval remain missing.

A local Gates 4–8 audit also repaired a downstream schema and identity gap.
Final artifact construction now accepts only the repaired v2 SFT evidence,
revalidates the exact pinned Qwen inventory and sealed Gate 0 GGUF toolchain,
and records the exact llama.cpp CLI identity. Laptop certification derives its
runtime revision from that sealed artifact manifest and verifies both GGUF
hashes before measurement. Gate 8 now requires all three comparisons to bind
the same frozen decision-task set, binds the decision candidate to the merged
release artifact, and binds laptop evidence to the same artifact manifest and
llama.cpp binary. Focused release tests pass. This is local readiness, not
executed Gate 4–8 evidence.

Gate 3 is closed after the fully finalized staged attempt
`20260826T042539Z`. Gate 1 revalidation reproduced the canonical base score of
20/180 on the same exact Qwen revision and serving contract, although raw
outputs and the run seal differ from the earlier CUDA run and remain separate
revalidation evidence under run seal
`57ea58ece793aee30b8c104dadff5c837d568f5f3effbb5f9770bada91fd64da`.
The original admitted Gate 1 baseline remains canonical and was not
overwritten.

The LR `1e-4` candidate completed 400,652 seen tokens, adapter save/reload,
and all 180 development tasks. It passed 13/180 versus the same-run base's
20/180: Go 2/30, Java 2/30, JavaScript 3/30, TypeScript 1/30, Python 5/30,
and Rust 0/30. Five-family macro fell from 10.0% to 7.33%; paired transitions
were 10 wins, 17 losses, and 153 ties. It therefore cannot be promoted. The
LR `2e-4` candidate reached 339,550 seen tokens and preserved three
checkpoints, then the configured consecutive-loss-spike guard stopped the run.
Its evaluation, LR selection, main 636,093-token SFT, and promotion
adjudication did not execute. Gate 3 therefore requires a data/mechanism and
stop-guard correction before another bounded pilot; scaling is not justified.

The terminal is a strict `sealed-failure` under seal
`8b4acfa783446a210c15ddfc47db71c255c1a8ac6d4ed3616f6f72571ddc03fa`.
The generation-pinned 805-object terminal backup is verified under seal
`e9f1439b6b8b1d5c1b17b8e28c7c4e16344d7a1847c47216d051456cb2ffe180`.
GCP had automatically deleted the exact VM and boot disk under the card's
`instanceTerminationAction=DELETE` contract; provider operations prove guest
shutdown followed by deferred deletion. The finalizer verified that lifecycle,
deleted the remaining subnet and VPC, and proved all four identities absent.
Deletion-gate, finalization, and final 13-object post-delete backup seals are
`3028a74002243b0627f8b90489da06a1b1b18ba16efa14ea7ab7b85d6ce6f57a`,
`f0b6a8049f1d440a2d2e5b602ea62330c1fb30a944d985fe1f7f2ca387743c58`,
and `96bc79aed2a1819dffbb74c1e88278dd8e151bf48d366da0de814bec9aae6c14`.
No run-scoped GCloud resource remains. Another GCloud execution requires a
fresh explicit approval.

The Gate 3 v2 mechanism is now partly executed on CUDA. The
rejected v1 config and 2,155-row duplicated schedule remain immutable
historical evidence. The new versioned config uses all 1,399 authorized rows
exactly once: 461,235 input tokens and 242,406 response tokens. Raw response
volume is not balanced, so every row carries a supervised-token objective
coefficient. The prepared-manifest audit proves the normalized objective is
Go 20%, Java 20%, JavaScript 10%, TypeScript 10%, Python 20%, and Rust 20%,
with one effective epoch and no repeated source ID. Its manifest seal is
`1b24782e32dcab4ea2e42a80564c45cba29fdcff0c198f7c7df465595e3f7edf`.

The repaired primary recipe is BF16 LoRA rank 8/alpha 16 on 16 attention
projections in layers 16–23, excluding every MLP and gating projection. Its
learning-rate candidates are `1e-5` and `3e-5`. The trainer now measures the
untouched base and adapter on the same validation rows, records both record-
mean and supervised-token-mean diagnostics, and replaces adjacent-record loss
comparisons with a post-warmup optimizer-group rolling median/MAD detector
that also preserves group min/mean/max and gradient norm telemetry.

Development tranche 1 is frozen as the deterministic Gate 3 canary: 30 tasks,
five per lane, selected structurally without reading model results. It can
triage the two complete LR candidates but cannot decide promotion or enter
training. The selected candidate still requires the full 180-task development
evaluation. Its manifest seal is
`0b7483141ba64ba223bc976ed7711ad847bc1056888be0e7bd9d261b85cffa44`.

The current Gate 3 v2 evaluation-workspace, training-workspace,
runtime-rehearsal, and non-executable preparation seals are respectively
`6e001b04de84d785feaf96dbd42ce5adcad62fd8e7a6cc969c991e4f90222532`,
`874ac3f8f2bf226a6dd100c470f46ee39b7e7f1591ec5324042e985de17b4ae1`,
`dff92b7d1cf9676ea59f6e5ba66c10ee7447647c84dfd19a876714d126e18594`,
and `bedaf55f5309c40d0044f1d1aff8aa3ae080dead312091fd56a4ea92e9ad04eb`.
The evaluation archive is byte-reproducible at SHA-256
`56c29ec107782fe2870496f4d54ab0fb466269a535210d88823afb1d4f2ae7dd`.
The regenerated local training preflight is `ready` with no failed checks under
card seal
`c33be811a3eaeda5033bcd93313577f0eb716b8bd42a8514da9f41b40eedba0e`.
That preflight is superseded by the approved and rehydrated execution path
described above.

Gate 1 is complete. Approved attempt `20260825T153823Z` executed all 180
frozen private development tasks against exact revision
`15852e8c16360a2fea060d615a32b45270f8a8fc`, with first-EOS trimming and
resource-limited network-disabled verifiers. The exact base passed 20/180
tasks: Go 0/30, Java 2/30, JavaScript 4/30, TypeScript 6/30, Python 5/30,
and Rust 3/30. Run seal
`a04361a047080bc479328d52d8be23fabcedb2b42ebbf0a059775e32db823ceb`
and 365-file admission seal
`c7d7d33d59d804a3dcd1b0f98e5aed9f409b229a3c31d85f1ef19f5b021faa62`
bind the canonical result. Gate 1 readiness is `ready` under seal
`d827ece3d324633a6fc6b0a46be55dcd87a87fb565358d3f2704806ced154971`.

Gate 3 training admission also passed, but the first 0.0001 LR candidate
stopped before model loading or any optimizer/token progress. In the exact
Torch/CUDA image, `torch.cuda.reset_peak_memory_stats(0)` raised
`RuntimeError: Invalid device argument` before the CUDA context had been
explicitly selected and initialized. Production SFT now selects `cuda:0`,
initializes CUDA, then resets the current device's counters without an integer
argument. The call-order regression test, archive rehearsal, and full local
suite pass. The resealed training archive, training manifest, and preparation
seals are
`d06c4d2a71828c61514d62ae3d1c8dccf6b5e8e9d9d403527b7f95833d919688`,
`9af762e484c04f54e1728adca9d87a9214c991cfed78bc9cc78a656bfa45fe19`,
and `b38dcbbb4a8ba0bbbe5a9bbac138ebe335cc0f14e9ceb39b0a171882374cdc5a`.

Strict terminal validation, finalization, and exact resource absence passed
under seals
`c299e90402004e9ce014f0b04f3fa0f2ae9d33211d3fa5971a7c1f58aecad351`,
`94963d2fd2deed795d6a883633f2d8cb2064e36cd4b8c6426c95720a1cf36f5a`,
and `1bb8e75d6662083f8da1b27655507952a913c19234b21ecfd7c35b3a1264e7c1`.
The VM, disk, subnet, and VPC are absent. The final 14-object post-delete GCS
backup is verified under seal
`9a34c63e37a75211234edb5de977c4da5f92e4381e352b4b85fce4a319fbf419`.

That historical repair was superseded by Gate 3 v2. The latest Gate 3-only
attempt completed one of the two planned unique-row candidates but stopped on
the verifier-image orchestration defect before any admissible canary result.
Its approval is exhausted and no run-scoped resource remains.

Gate 0B is now passed. The approved `us-east1-b` Flex-start L4 execution used
Liger 0.8.2 only for Qwen3.5 fused linear cross-entropy and did not materialize
training logits. Exact package, CUDA, Triton, external-kernel, model-load,
text-only inference, frozen-vision, 2,944-token synthetic envelope, 16 real
optimizer steps, adapter save/reload, and safe merge all passed. Peak reserved
VRAM was 18,975,031,296 bytes against the frozen 22,548,578,304-byte ceiling.
Rank, optimizer, learning rates, data, sequence length, and serving context
remain unchanged.

The canonical Gate 0 report is now also `ready`. Its fused-loss CUDA admission
receipt cross-binds the approved card, immutable run plan, exact qualified
Linux/AMD64 image, 16-record/16-step qualification, adapter reload and safe
merge equivalence, double-read terminal backup, runtime inventory, cost bound,
post-run backup, and exact infrastructure absence. The canonical seals are
`6047b522f697be73b7d781b4e5021c8e29d23441767d660db6f9badc50422fd4`
for CUDA admission and
`adde675ce4db676c635ba864af0dd356c292e352443d4ed88607079059b346cc`
for Gate 0 readiness.

Native AMD64 verifier qualification is complete. GitHub Actions run
`32639381229` loaded the exact pinned image archive and passed all 12
development/decision tranches: 540 reference passes, 540 known-bad rejections,
and zero timeouts. All 15 JSON seals, runtime identities, output hashes, and
the global separation report were independently verified. The repaired
development-only v1 workspace and baseline-runner readiness evidence were
sealed before Gate 1 execution. Gate 1 subsequently completed; its canonical
result and the current Gate 3 v2 workspace are recorded above.

The superseded pre-Gate-1 evaluation-workspace manifest seal was
`f6551430af4c5a2cd2ad5d7bcbdcf4daf3105136682c146535e2a2a11c2da5b0`;
the corresponding v1 training-workspace manifest seal was
`9af762e484c04f54e1728adca9d87a9214c991cfed78bc9cc78a656bfa45fe19`.
The v1 archive-executed runtime rehearsal seal was
`7c280c5a5c8ec8c28891818d5171dbdea3507dc11eca6799f86cde2d71d50406`,
and its non-executable preparation seal was
`b38dcbbb4a8ba0bbbe5a9bbac138ebe335cc0f14e9ceb39b0a171882374cdc5a`.

## Completed

- Inspected the committed Ganesh v0.1 plan, training, data-rights, and
  benchmark history without modifying its dirty working tree.
- Verified that `Qwen/Qwen3.5-2B` is an Apache-2.0, post-trained, dense 2B
  checkpoint intended by Qwen for task-specific fine-tuning.
- Verified current Transformers and ms-swift support for Qwen3.5's hybrid
  Gated DeltaNet/full-attention architecture.
- Produced an initial plan and a second-pass critical revision.
- Defined separate Q8/8 GB and F16/16 GB laptop acceptance envelopes.
- Recorded the user's 2026-08-22 authorization to reuse the cleaned Ganesh
  v0.1 training data for the same purpose on the Qwen3.5 backbone.
- Located a 1,399-row training and 50-row validation seed inventory in the
  committed Ganesh source tree across all six compiler lanes.
- Pinned Qwen revision
  `15852e8c16360a2fea060d615a32b45270f8a8fc` and verified its immutable
  13-file, 4,571,274,023-byte upstream inventory without downloading weights.
- Implemented a fail-closed Gate 0 readiness reporter. Its initial local
  macOS report was correctly `not_ready`; the canonical report is now ready
  only through the sealed qualified Linux CUDA evidence chain.
- Deterministically imported all 1,399 training and 50 validation rows from the
  pinned Ganesh commit. No duplicate IDs or conversation groups were found.
- Implemented strict six-lane task/result/comparison schemas, paired scoring,
  five-family macro weighting, and a network-disabled Docker verifier.
- Proved reference-pass and known-bad-fail directionality on synthetic fixtures
  for all six lanes. Full unit suite passes; the Docker integration passes.
- Downloaded and byte-verified the exact 4,571,274,023-byte Qwen checkpoint.
- Locked the qualified Apple environment at Python 3.12.11, PyTorch 2.13.0,
  Transformers 5.15.1, and PEFT 0.19.1.
- Passed text-only non-thinking BF16 inference on MPS.
- Inspected 186 language-model linear modules across 12 target suffixes and
  verified adapter gradients while excluding 99 vision/head modules.
- Passed a 16-record LoRA train/save/reload/safe-merge smoke.
- Converted and ran both F16 and Q8_0 GGUF artifacts using pinned llama.cpp;
  the tiny runtime smoke measured 25.5 and 41.6 decode tokens/second,
  respectively. These are smoke measurements, not final laptop benchmarks.
- Added a fail-closed seed-pilot controller binding model, data, prerequisite,
  balancing, LoRA/QLoRA recipe, checkpoint, resume, budget, and stop-condition
  evidence.
- Audited the pinned Multi-LiveCodeBench v6 slice. All 1,050 language
  projections were excluded because none satisfies the strict task contract;
  no benchmark prompts were redistributed or admitted.
- The recurring 30-minute goal-alignment heartbeat was disabled at Navneet
  Prabhakar's explicit request; no replacement deviation check is active.
- Selected BF16 LoRA as the primary SFT mechanism and NF4 QLoRA as a
  measurement-gated fallback. The controller enforces separate recipe hashes
  and sealed fallback evidence.
- Implemented the exact Qwen base-inference runner with official non-thinking
  prompt rendering, bounded greedy generation, extraction, atomic evidence,
  resume accounting, and verifier integration. Its synthetic harness proof
  completed 6/6 executions but solved 0/6 underspecified synthetic tasks; this
  is runner evidence, not a base benchmark.
- Authored and sealed private development tranche 1: 30 tasks, five per lane,
  balanced 15 generation/15 repair. All prompts expose exact API/file contracts
  and examples; repair prompts include buggy source. Seed overlap is zero, all
  30 references pass, all 30 known-bad implementations fail, and timeouts are
  zero.
- Implemented the production CUDA qualification image/controller with BF16
  LoRA primary on at least 24 GiB and guarded NF4 QLoRA fallback on at least 16
  GiB. Static validation passes, but no CUDA execution is claimed because no
  non-GCloud NVIDIA provider credential, CLI, or local GPU is available.
- Authored and sealed development tranches 2–4: 90 additional tasks, bringing
  the private development surface to 120/180 tasks, 20 per lane. Across the
  three tranches, all 90 references pass, all 90 known-bad implementations
  fail, exact/normalized seed and cross-tranche overlap is zero, and timeouts
  are zero.
- Authored and sealed development tranches 5–6: 60 additional tasks, completing
  the private development surface at 180/180 tasks, 30 per lane and 90 each of
  generation and repair. Across the two tranches, all 60 references pass, all
  60 known-bad implementations fail, exact/normalized seed and cross-tranche
  overlap is zero, and timeouts are zero. The full local suite passes with one
  intentional integration skip.
- Completed the authorized bounded GCloud A100 Gate 0B execution without making
  a qualification claim. Three terminally sealed attempts exposed, in order:
  a missing Docker package in the pinned DLVM image, an optional BuildKit cache
  directive incompatible with the pinned Docker CLI, and verified GCE Spot
  preemption while compiling `causal-conv1d`. No attempt reached model loading
  or training. Cumulative GPU upper cost was `$0.79037286`; the retained
  conservative bound was `$4.92111752`, below the approved `$5` ceiling. Every
  input/runtime/failure/teardown set is generation-pinned and hash-sealed in
  GCS. That execution's VM, NAT, router, subnet, and VPC were deleted and
  independently absent before the later CPU prebuild resources were created.
- Authored all 360/360 private decision tasks, 60 per lane and balanced
  generation/repair. Decision tranche 3 is sealed by manifest
  `26f982c437000012d2eae1f4a3d77260b9f3798931dc938941e29c91f2e3a3d9`
  and zero-overlap report
  `dae97584f926381995f06232381425239fa35e1e0d83ce6b5404b93e0bba15d4`.
  Two independent Docker runs proved a 30-second aggregate limit flaky for
  compiled lanes, so Go/Java/Rust were revised to 60 seconds while JS/TS/Python
  remain at 30. Fresh Docker directionality now passes all 360 executions for
  tranches 1–3: 180/180 references pass, 180/180 known-bad implementations are
  rejected, and no execution times out. The evidence seals are tranche 1
  `8cf851703f67c3c80a0cdafba5e4e68adade135af9aa4f443837b670468005cf`,
  tranche 2
  `203965708f9a238a3e323ad4c7a8d9d7d3b5872764e83185ac5e578274a375a8`,
  and tranche 3
  `15d95ad2530d18410c1e1ebda0974bfc54b20208e29f1273aae5ae4a17a56289`.
  Tranches 4–6 add the final 180 tasks. Across the complete surface, all
  360/360 references pass, all 360/360 known-bad implementations are rejected,
  and no final execution times out. Their manifest/overlap/directionality seals
  are tranche 4
  `118dbb5086725bd36ceed09ba37d1f14c53a7f41d79e365c0a6260ac24fb2658` /
  `e66ee7d1a8fa67b044c4e16a8b1e766d4bdc13283380abdc5281b8453d6d1715` /
  `0119e33afb42cda47383d48e1b300b683732a0d30a8c5864ecd370675207857b`,
  tranche 5
  `ee52d232e2d44411a398ad680def61ffffd54722d8a8fc400ffdd2143d4240e3` /
  `251cee5751463ffa76159823b3ec939a6edbd66e328336ca65e7169022186de5` /
  `cd7cafdec42d97173e877fa74530c5daef3d4c1edded9df1b71de9dd453ecdb1`,
  and tranche 6
  `f97eb03d1206cb7135a520f2fb069a44375b9332a4e36ddc9f78cbb0ca6d7c89` /
  `80f4d7f340fc4994f97e8c332e9eea9a339c7eb4837f9d00595775b0ef1ba0ff` /
  `c9b3c9d888f5c438ca2a7666b620a599bd08da639ef24a42c9f78fa461706dfb`.
  The sealed failed tranche-5 result is preserved as non-decision evidence.
  The earlier failed tranche-4 file (seal
  `874e2308f503a35b4cf74c4f9105f623816834526c51e9d50a36b4dd3d01f0dc`,
  34/60 references, 60/60 known-bad rejections, 26 failures) was overwritten
  before preservation and could not be recovered; it is an explicit audit-gap
  incident and cannot support any decision claim.
  A global separation report byte-binds both seed JSONL files, every
  development and decision manifest/task, all overlap evidence, the shared
  tranche-1/2 cross-overlap evidence, the runtime configuration, and all 720
  final directionality executions. It proves zero exact or normalized overlap
  and was sealed by
  `96ea9669e194c567f304c5462b2be9cc171555bba56ea10801186480bb347a06`.
  That historical seal is superseded by the native AMD64 result described
  below.
- Prebuilt and content-sealed the pinned production CUDA image on the same
  stopped CPU disk after the first archive export failed with exit 141. The
  failure was caused by unbounded `zstd` progress output exceeding the GCE
  metadata logger scanner limit; the retry uses quiet bounded export. The
  original boot's provider serial is unavailable and was not reconstructed, so
  attempt 1 remains failed, non-decision evidence.
- Verified prebuild attempt 2 as 35/35 generation-pinned GCS objects. The image
  is `ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1` with ID
  `sha256:37b7cbcb8280d469bad6213bf09bfa0ccb2dba96a912aaa105183069c2ce5351`;
  its compressed archive is 8,167,013,739 bytes with SHA-256
  `f2dafd6c0b82d46be441dfe2a5c2b23cd5f309e5061f20da3edf91e70eddb8f3`.
  The terminal backup seal is
  `f1a874deac5e5fadf19eeb29d2c4fb80376e62ed130f70439e2894ae6b4ec076`.
- Passed the deletion gate, backed its evidence, deleted the CPU VM, NAT, and
  router, and independently proved them absent. The post-delete backup seal is
  `ac2b9c9f21e0b6f91d72a0d90d80f3eb8a55ea56432fb66980bae76d86e28358`.
  The dedicated VPC and subnet were retained at this point for the later
  no-NAT A100 qualification.
- Ran the explicitly approved Standard A100 qualification attempt from the
  sealed image. The A100 identity, image load, offline inputs, and controller
  startup succeeded, but package identity failed after 31.85 seconds with
  `ModuleNotFoundError: No module named 'torchvision'`; neither the model nor
  training started, and no CUDA qualification is claimed. The exact 31-object
  runtime prefix is independently verified by seal
  `9d1ed5d0e5407ef7f9397ba7e406952865f981eda61ee5d337990bfd298f114d`.
  The deletion gate passed, the VM, retained subnet, and retained VPC were
  deleted, and six-object post-delete evidence is verified by seal
  `24b148309a89282f6ec6bf043a5bb7ff81baaca5ea783fa71ec1bfe138ec2284`.
- Diagnosed the repair locally: Qwen VL utilities import `torchvision` without
  declaring it; Torch 2.13.0 requires the matching Torchvision 0.28.0. FLA also
  initialized Triton before CUDA while the read-only container provided no
  writable executable Triton cache. The repaired definition pins Torchvision,
  initializes Torch and Triton before FLA, requires CUDA backends explicitly,
  and gives Triton a bounded executable tmpfs while keeping the network off and
  the root filesystem read-only.
- Rebuilt that repaired CUDA image on a temporary Standard `e2-standard-8` CPU
  VM. The image is
  `ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1`, ID
  `sha256:b2f9335c64b208e2d692dc45c56df0790573951df835d34604f80e93d0b0f2a6`;
  its 8,174,282,938-byte compressed archive has SHA-256
  `229325473993a1d5b58baec3ed01fe9d3a49b253be92b39b93d9a52e307e3f9f`
  and GCS generation `1787447318500114`. The 36-object terminal backup is
  independently verified by seal
  `8ab74078de47a0055ff8a46285b01148fa33d9a994e2cbc702afb18be876815a`.
- Passed the CPU deletion gate, deleted the VM, NAT, and router, and proved
  their absence. The 12-object deletion evidence is sealed by
  `112d95f7ce787c1c404d51d7b67ba3427b00ea1eebef35e8cc4319dbf63f57cd`.
- Ran the rebuilt image on one Standard A100. The exact pinned package set,
  NVIDIA A100-SXM4-40GB identity, BF16 support, CUDA 13.0, cuDNN 92000, and
  Triton CUDA architecture 80 passed. Qualification then failed after 32.74
  seconds because the harness requested removed Transformers attributes
  `chunk_gated_delta_rule` and `fused_recurrent_gated_delta_rule`. Model load
  and training did not begin, so Gate 0B remains unqualified. The structured
  failure is sealed by
  `8ddeff566da4a32abfb3586f90f0ca5196cacbaed299dcb52d9fec3b733b3df6`;
  the 31-object runtime backup is independently verified by seal
  `d407c689528356d007b29f08725f29f5dc7caae3334b13cbe11e9dfc7c0d83aa`.
- Passed the A100 deletion gate, deleted the GPU VM, subnet, and VPC, and
  independently proved all run-scoped instances, disks, networks, subnets, and
  routers absent. The deletion evidence is sealed by
  `f5adbff101728eaa3e559f9d047f35c7fd8535f9041d2df8d65cbd94f2a02d2b`;
  the post-delete absence backup is sealed by
  `9862d12c9a48d96253bfe06a0d39daf4bfb6ddd55b3d7224689b795fc86a1068`.
  The complete local run evidence is also archived to GCS generation
  `1787451344731424` with SHA-256
  `c761399cef0729841d9eba74b1f12ee9b95f5b8f8ce0369b24c02f957218da98`.
- Corrected the qualifier to inspect the decorated Transformers 5.15.1 kernel
  closures and require their resolved implementations to come from
  `causal_conv1d` and `fla`. This remains fail-closed and does not infer a CUDA
  pass from symbol presence. The runtime mounts the run-scoped workspace at
  `/workspace`, so the sealed image can be reused without rebuilding. The
  controller now forwards the attempt ID into the container, and both backup
  verification reads are generation-pinned. The full local suite passes with
  one intentional integration skip, and the independent second pass reports
  aligned.
- Ran the attribute-repair retry under GCS prefix
  `ganesh-mini-1.0/gate0b/20260823T030116Z`. The exact environment and three
  external CUDA kernel resolutions passed; the recurrent wrapper alone fell
  back to Transformers Torch because FLA 0.5.2 names the available fused
  implementation `fused_recurrent_gated_delta_rule`. The structured failure
  seal is
  `d7fdb89ce744524ec87ad4b10caf2cb189ef7fb61f61fb6e2e7c152a6f538e50`.
  The terminal backup seal is
  `39ed40945ded583ebbc47ebbbcf3e4d9faf899dcbbe418a741aef87a4ea86065`.
  No model load, optimizer step, or training occurred.
- Passed the retry's deletion gate, backed all run evidence to GCS, deleted
  the VM, disk, subnet, and VPC, and proved them absent. The composite deletion
  backup, deletion gate, and post-delete seals are respectively
  `a5e5c0779fe298ee0d915481e435fa22cccc017b2c17bde2d4947264c7d16204`,
  `7e1d4f9c3eb3dbbe558c4e972083dcc272e3dd1b95bb7f64bdb23d891d3bab88`,
  and `8d353de09d2e61f165f7eff0d2b6edcfcbcc43650bc202dbf6c7e5b4c1b3af07`.
  A final complete local-evidence archive is independently verified in GCS by
  manifest seal
  `f0e930840aebc876ea49f92e5ce4deabf59a3922a8ae4e72fcd2c5cd89a8316c`.
- Implemented a fail-closed pre-import compatibility alias that exposes FLA's
  fused recurrent CUDA implementation under the exact symbol Transformers
  5.15.1 requests. The existing closure inspection still requires the
  recurrent implementation to originate in `fla`; the Torch fallback remains
  disallowed. The retry path now shares one model load across inference and
  training qualification and assigns 12 vCPUs/72 GiB to the container.
  The full local suite passed at that point: 114 tests passed and one
  intentional integration test was skipped.
- Replaced the unusable all-zero Qwen assistant mask with tokenizer-owned
  prefix differencing. The exact pinned tokenizer proves response-only
  boundaries for all 1,449 seed and validation rows across the six lanes;
  prompt/scaffolding tokens are masked, terminal completion tokens are active,
  and non-prefix, empty, batched, or overlength records fail closed. The shared
  implementation is used by both CUDA qualification and seed-pilot
  preparation. After the broader controller repair, the full local suite has
  135 collected tests: 131 pass and four environment-dependent integration
  tests are intentionally skipped.
- Attempted the approved v3 card in `us-central1-a`; the provider returned
  `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` before creating a VM. The unused
  subnet and VPC were deleted and the exact v3 resources were proved absent.
- Ran the zone-only v4 retry in provider-suggested `us-central1-b`. All pinned
  inputs and the sealed CUDA image passed generation, size, and hash checks,
  but qualification exited before model load because the container entrypoint
  could not import `scripts.train.response_only`: `/workspace` was mounted but
  absent from `PYTHONPATH`. The 31-object composite backup is sealed by
  `5fb8e2dae08ff7924a55f72cc5a1bad10eb37e508a5b11560ec112d6b0d02e40`;
  the stopped-provider deletion gate is sealed by
  `df4f793d8607364ee86e1f8ba04cf162491ed8f3209f2e50d3ef44a9c7abb64d`.
  The VM, disk, subnet, and VPC were deleted and their absence is sealed by
  `8ac2896c7a397fc23649eb4ed02eaa53d5d4df112851cf0db14c4e335de79d9f`;
  the independently verified six-object post-delete backup is sealed by
  `632b86742d1191f82dad8aec3f8c68eae2c754579e61f783387ff00a3d56a78a`.
- The runner now exports `PYTHONPATH=/workspace` into the offline container,
  with a regression assertion and direct qualifier import smoke. Historical
  v3/v4 cards and hashes remain immutable; the next card must bind this changed
  runner and a new deterministic workspace archive.
- Ran the approved v5 qualification in `us-central1-b`. The repaired import
  path worked and the exact A100, BF16, CUDA/Triton/FLA kernels, package set,
  sealed image, and pinned model inventory passed. ms-swift 4.5.2 then stopped
  before model loading because automatic registry matching returned both
  `qwen3_5` and `ovis_ocr2`. The qualifier now explicitly requests
  `model_type="qwen3_5"` with downloads disabled and verifies the returned type
  and template. The VM was stopped after its 29-object terminal backup was
  verified, then deleted after a 33-object composite backup and deletion gate
  passed. VM, disk, subnet, and VPC absence and the six-object post-delete
  backup are independently sealed.
- Ran the approved v6 qualification in `us-central1-b`. Explicit ms-swift
  model selection correctly returned `model_type="qwen3_5"`; qualification
  then failed before model load because the harness incorrectly treated the
  type-level `ModelMeta.template=None` as a registry failure. The pinned
  ms-swift 4.5.2 source shows that Qwen3.5's template belongs to its model group
  and must be resolved separately. The qualifier now explicitly resolves both
  `model_type="qwen3_5"` and `template_type="qwen3_5"`, recording the nullable
  raw metadata field only as a diagnostic. The focused qualifier suite passes.
- V6's terminal backup, stopped-resource composite backup, deletion gate,
  exact absence proof, and post-delete backup are sealed by
  `5e80ce5264f434b47102706e16a9fa2dd8a494f0a166cf83e01e45b2e944a0c2`,
  `3f8e090c99829139a2cc7b4400f6e40a6e940eb05b8450ef5b2516e91d3b142a`,
  `f1a27123f1362dcfe7c9d55049d4464cf39180d0339145a52c2a3a0a3faba83a`,
  `05392d670d9617c3ffc46584db2531dec730e11c0055070da277696a5e902b0c`,
  and `6db8cc64584a9895a00822273a01a142999e3020552df843f9c9c1dae72876bd`.
  The VM, auto-deleted boot disk, subnet, and VPC are verified absent.
  The complete local run archive has SHA-256
  `dfbc2c8136b03e046245ca6fe318374bd2f54c341ef8c7ae0990ccc644639777`
  and its independent GCS verification is sealed by
  `7e14c80111eefd4f0564f1cf8a9c57081385ea008b55f33796c00e9dfe502f54`.

## Not started or incomplete

- Gate 3 v2 completion: the `3e-5` candidate, both complete 30-task canaries,
  LR selection, and the selected candidate's 180-task development evaluation
- Evidence-triggered 4,000–8,000-row expansion, if the repaired seed remains
  insufficient
- Main joint verified SFT and optional correction pass
- Candidate quantization and final laptop certification
- Ganesh v0.1 rerun on the Ganesh Mini decision surface

## Prepared after the latest audit repair

- Gate 2 is ready. All 1,449 authorized seed rows pass current-toolchain
  syntax/compile compatibility and have zero overlap with the 540 frozen
  development and decision tasks. The balanced pilot schedule contains 2,155
  sampled rows, 345,832 response tokens, and 636,093 input tokens; that exact
  input count is now the hard main-pilot ceiling.
- A Linux seed-pilot preflight now fails on exactly `gate1_ready`. Gate 0,
  Gate 2, response-only rendering, token balance, recipe identity, and the
  exact 636,093-token prepared dataset all pass. This proves a successful
  baseline admission will remove the last non-compute pilot prerequisite.
- The production evaluation runner now batches by length and language,
  verifies concurrently in network-disabled sandboxes, resumes only sealed
  model/config/task/runtime/implementation-bound evidence, persists completed
  verification between generation batches, rejects cardinality and duplicate
  task defects, and emits result-compatible evidence for the paired scorer.
  The Qwen baseline is CUDA-bound to the same external kernel contract as Gate
  0. Gate 1 reopens all 180 task seals instead of trusting aggregate
  accounting. Cross-template comparison pairs on frozen source-task identity
  while preserving model-specific rendered-prompt hashes. Gate 1 is closed
  only on the unexecuted exact Qwen development baseline. The prior
  runner-readiness seal
  `4afb29fcfbc1bda3252bd7bb4e96158ef92efb1fc1cda82b1308701b0e6cb848`
  is historical. Its replacement binds the passed native run, global
  separation, repaired workspace, retention slice, Gate 1/2 reports, and the
  full test suite. A subsequent host-orchestration hardening superseded that
  replacement; the current 171-test evidence is sealed by
  `04c3beba85fab9dcef8f5931335029a375e788040b95b6a591bef3eeacf630f0`.
  The zero-task public diagnostic is retained as a complete exclusion result
  instead of weakening admission rules.
- The SFT engine is hash-bound, response-only, cost/time/VRAM bounded,
  checkpoint-resumable, validates held-out loss diagnostically, and requires
  save/reload logit reproduction. Its Qwen-specific structural guard freezes
  the nested vision tower, disables the actual language-model cache during
  training, restores serving cache, and computes the diagnostic macro across
  five product families rather than six compiler lanes. It reserves 600
  seconds for finalization and forces a resumable terminal checkpoint at a
  bounded stop. LR selection binds
  both complete 400k-token candidate runs and their exact 180-task development
  result collections.
- Training packaging is deterministic and excludes every evaluation surface
  while including the exact prepared train and validation inputs.
- Ganesh v0.1's five released adapters are provisioned from immutable Git
  objects and match the release hashes. Its full Gemma base inventory is
  pinned. Rust is explicitly routed to the base because v0.1 did not release a
  Rust adapter. Disk cleanup increased local free space to roughly 232 GiB, so
  the 23.9 GB base is no longer blocked on local storage; provisioning remains
  deferred until the comparison gate to avoid an unnecessary early download.
- Merge, GGUF F16/Q8 construction, constrained laptop certification, clustered
  statistical adjudication, Q8 retention, and final fail-closed release
  decision tooling are present but have not been executed on a trained model.
  The release path now also has a pinned llama.cpp server backend for sealed
  F16/Q8 evaluation, a six-lane export-equivalence verifier, and a fail-closed
  Hugging Face publisher. Gate 8 requires sealed raw-result-set roots, a fresh
  Ganesh v0.1 comparison, seed/readiness/execution-card/training-run lineage,
  artifact-to-training binding, export equivalence, quantization retention,
  and both laptop profiles. These controls are locally tested; they do not
  constitute executed release evidence.
- The evaluation verifier contract has been migrated before baseline generation
  from unavailable Apple/ARM64-local images to six project-owned Linux/AMD64
  images. Every base manifest and toolchain version is pinned; TypeScript's
  package tarball is verified against its registry SHA-512 integrity value.
  The exact tag, image ID, and platform are checked before every sandbox run.
  Local readiness is 6/6 and sealed by
  `36c070d9d8554c7f2999b5e4d5bbacbc67664eb64ac2dc34196534de155737a1`.
  The 918,639,104-byte portable image archive is internally verified against
  its OCI tag/manifest/config/layer graph and sealed by manifest
  `aba48afc9f1a75d6911204fd1e49193a9908655ad7d0540ec9cd53c82396bac8`.
  The original deterministic development-only execution workspace contained
  exactly 180 tasks and excluded decision tasks, seed/training data, model
  outputs, and authoring code; it was sealed by
  `846cf0b64e3d1804cbbdaa44cb57a07da989e298c9ed7f3cd8f2c400dda625f5`.
  That workspace is historical. Its byte-reproducible replacement binds the
  repaired task seals. The baseline host audit then identified that an outer
  CUDA container using the host Docker socket could produce verifier bind
  paths invisible to the host daemon. The execution package now forces
  verifier temporary directories onto an identical host/container mount,
  keeps the model container offline, re-audits all six image identities after
  loading, preserves resumable outputs, and accepts only a complete exact-base
  180-task run. The twice-reproduced current archive has SHA-256
  `e64e3e78d3e5d1e0d97479c7e92de25babc89ce761002271e4206733bddbb209`
  and manifest seal
  `4d8e66ce89eabbcc08e6bf7520dd9b0baad5edc426ff27add07e4ab5aae5a8e9`.
  Historical ARM64 directionality results remain immutable but are explicitly
  non-current.
  A manually dispatched, read-only GitHub Actions workflow was historically
  used to load the exact private content-addressed image archive on native AMD64,
  execute all 1,080 reference and
  known-bad checks across development and decision surfaces with at most two
  concurrent tranches, rerun global decision separation, and return one sealed
  evidence archive. This is non-GCloud compute and does not expose a task to a
  model. That workflow has since been removed and GitHub Actions is disabled
  for this repository; the sealed historical results remain evidence.
  The first dispatch, GitHub Actions run `32636800789`, independently loaded
  the exact archive but stopped before task execution because the host-audit
  code used a Docker Go-template helper (`dict`) unavailable on the runner.
  No directionality result was claimed. The controller now reads portable full
  Docker JSON and seals early failures; packaging now succeeds on partial
  diagnostics. The incomplete 161,802-byte artifact from that failed run was
  deleted, while GitHub's immutable run logs remain the failure evidence.
  The retry, run `32636958446`, executed every tranche. Ten passed; development
  tranches 1 and 2 failed six Go references at the obsolete 30-second limit.
  All 15 evidence seals verify. The full 170,686-byte evidence tar is preserved
  with SHA-256
  `fadd5ab16d2ecf8d53ef6a19b4eded9d093bcf3b922b664db147a23fefb0e098`.
  Development compiled lanes now use the already established 60-second rule;
  the six development manifests and overlap reports were regenerated without
  changing prompts or behavioral artifacts.
  The final retry, run `32639381229`, passed all 12 tranches and all 1,080
  executions with zero timeouts. The preserved 171,088-byte inner archive has
  SHA-256
  `dc44846887b2570885c7d082a5bb812bac56e6144523461c73bb29e7612849e2`;
  the passed-run receipt is sealed by
  `1877bb99a1cab96d962c14301cb6b453785c9487af8692d4c3c130c08afec73f`.
  The adopted top-level native evidence is sealed by
  `aed01c430f33c4580438b824993a9302e72726e4295c82b6e867745e81130cfb`,
  and the replacement zero-overlap global report is sealed by
  `a47d733caaf6d9db735a020dd182ab01cf1ffeb140f7984a846d5ac0d89cf53f`.
  The seed manifest was regenerated through the approved importer; its 1,399
  train and 50 validation records remained byte-identical. Gate 2 remains
  ready.

- Executed the approved Standard `g2-standard-8` L4 Gate 0B run under prefix
  `20260823T145734Z`. The provider exposed 23,659,151,360 CUDA bytes. Both
  recipes passed immutable identity, dependency, external-kernel, and
  non-thinking text-inference checks. BF16 LoRA failed after 91.20 seconds
  while requesting 96 MiB with 41.12 MiB free; the correctly triggered NF4
  QLoRA fallback failed after 148.42 seconds while requesting 512 MiB with
  445.12 MiB free. Both failures occurred in the 4,096-token synthetic
  backward envelope before any training record or optimizer step. The sealed
  run-result is
  `1fffbc66e2bda232b7a5b866fcfaf3094fac1ea4c54c5d76d4e03902d7063f91`.
  All 32 terminal objects were independently double-read from their pinned GCS
  generations under backup-manifest seal
  `087d7c89b1806ddbe61772ba44ba8ce5ccbe17c8dd18fb122aa29189784d8f85`.
  The VM, auto-delete disk, subnet, and VPC were deleted and are absent under
  proof seal
  `eb8171a24a2c893a7fad2a7806fb4f187af7dbb4b86b2d630aee7882c359071d`.

- Executed the approved bounded L4 v3 retry under prefix
  `20260823T152838Z`. Vision offload passed and released 662,833,664 BF16 CUDA
  bytes and 190,087,680 NF4 CUDA bytes. BF16 LoRA still OOMed while requesting
  96 MiB with 73.12 MiB free; QLoRA still OOMed while requesting 512 MiB with
  111.12 MiB free. Both failures remained inside the 4,096-token synthetic
  backward envelope, with zero training records and optimizer steps. The run
  result is sealed by
  `78a1af009066bc2403ad1e4d9ed6e3f865bb2666288bc4f27d95a61ca6d48ee7`.
  All 32 terminal objects and the VM inventory are independently verified by
  `ed92e5f42f4a076a347685ab829fa07a6644cce7e7c19f0cb9c6985d37d97c8a`.
  GPU billing stopped after 867.951 seconds, giving a compute upper estimate of
  `$0.20580668756242`. The VM, disk, subnet, and VPC are absent under proof
  `cda4d4b4a44f52b25dddac1e2f6939390499352da57336fc49e868baef52c8af`.

- Executed the approved bounded L4 v4 retry under prefix
  `20260823T165923Z` with the measured 3,072-token envelope. Both recipes
  again passed exact identity and text inference. BF16 LoRA OOMed while
  requesting 2.84 GiB with 2.65 GiB free. The correctly triggered NF4 QLoRA
  fallback reached backward but OOMed while requesting 48 MiB with 27.12 MiB
  free, a measured shortfall of 21,894,267 bytes. Neither recipe began a
  training record or optimizer step. The fail-closed run result is sealed by
  `67a691b9de7ed34a906b174a7bc4b0d80d23c42d93bee476c0987e687258d5c9`.
  All 32 terminal objects were independently downloaded and verified twice;
  the identical manifest seal is
  `b3d643fae56aa109c0ddd0d0f86e83e5f7fdca98fb899e03b977f2ade7e430e4`
  and the local verification record is sealed by
  `19529bb46c4fb587dece6c3ebe1364e34fca6c38aba14cf5a88b1ad4a5c6ca8b`.
  Billing stopped after 853.409 seconds, for a compute upper estimate of
  `$0.2023585195776689`. The VM, auto-delete disk, subnet, and VPC are absent
  under proof `00fe3d479e2db5f84c950ad1a19372ad252d8bc7b855f1c342bd3fde88bcdd8e`.

- Executed the approved bounded L4 v5 retry under prefix
  `20260823T180807Z` with the measured 2,944-token envelope. The initial
  `us-central1-a` create failed for provider capacity before any VM or disk
  existed; the same approved run was generation-pinned and reallocated to
  `us-central1-c`. Exact identity and text inference passed for both recipes.
  BF16 LoRA OOMed while requesting 2,925,527,040 bytes with 301,072,384 bytes
  free. NF4 QLoRA reached backward but OOMed while requesting 73,400,320 bytes
  with 9,568,256 bytes free, a 63,832,064-byte terminal shortfall. PyTorch
  simultaneously reported about 95,934,218 bytes reserved but unallocated,
  which exceeds that shortfall and makes allocator-segment tuning a measured
  next hypothesis rather than speculation. No training record or optimizer
  step ran. The fail-closed run result is sealed by
  `0519d41c66f5f410e9d6a4a01ff4f7c3af8650d0a86b7b40f9a25a666dd849c9`.
  All 32 terminal objects were independently downloaded and verified twice;
  the identical manifest seal is
  `bfed538722d9d23776e6bf75c51b6d024f86f0fe2e64f9f2571e9c30ea04d2cf`
  and the local verification record is sealed by
  `7fa2fca07cdb48936a1933cb1a2dbbb63fe0e5329ac572e9261b70d8d01ac480`.
  Billing stopped after 864.951 seconds, for a compute upper estimate of
  `$0.20509533396908667`. The VM, auto-delete disk, subnet, VPC, and matching
  routers are absent under proof
  `5af5685dd4f8b42118bfd2ad4148f5296ae61948d9dce31b28d46a363620be5c`.

- Attempted the approved bounded L4 v6 allocator retry under prefix
  `20260823T223044Z`. Standard `g2-standard-8` capacity was unavailable in
  `us-central1-c`; GCP explicitly directed the request to `us-central1-a`,
  where the one allowed capacity reallocation also returned
  `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` with no further available zone.
  Neither create produced a VM or disk, qualification did not start, and
  compute cost is `$0`. All six generation-pinned inputs were independently
  downloaded and verified twice under identical manifest
  `606e36225d7901041e103f1729178d4147b73cb68b61456393bc89eb78ba7712`.
  The temporary subnet and VPC were deleted; VM, disk, subnet, and VPC absence
  is sealed by
  `6f4c5509085c6e01489cd69552e273b9acdffb8871bb92a2ebff4f16d94ec9a0`.
  This is a provider-capacity abort, not qualification evidence; the allocator
  hypothesis remains untested.

- Attempted the approved regional Standard L4 retry under prefix
  `20260824T024709Z` with a 30-minute, `$1.00` incremental ceiling. The
  preflight selected `us-east4` because the project had 16 unused Standard L4
  quota, both authorized zones supported `g2-standard-8`, and the durable GCS
  bucket is co-located in `US-EAST4`. Both `us-east4-a` and the sole authorized
  fallback `us-east4-c` returned `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`
  before creating a VM or disk. No GPU, qualification process, training record,
  optimizer step, or compute billing existed. All seven generation-pinned
  inputs were independently downloaded twice under identical manifest
  `7e6347207863fa6ce1cfab8994031ead2a9d5bcc3e4a29d3ecb37c062566a3e3`.
  The temporary subnet and VPC were deleted; VM, disk, subnet, VPC, and router
  absence is sealed by
  `fae70b66d8043df4c08c049e1cd064e7c81db4d260c4fa9304b75e1c391c23f9`.
  This is another provider-capacity abort and supplies no allocator evidence.

- Submitted the approved G2 Standard L4 Flex-start request under prefix
  `20260824T160620Z`, with a two-hour request-valid duration, 30-minute maximum
  runtime, automatic VM deletion, and `$1.00` incremental ceiling. Preflight
  passed with 16 unused preemptible L4 quota, 5,000 unused preemptible vCPUs,
  co-located `US-EAST4` storage, and a conservative `$0.95` upper bound. GCP
  accepted the instance as `FLEX_START` and exposed it as `PENDING`, but the
  insert operation returned `ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS` after
  23.649 seconds instead of retaining the request for its declared two-hour
  validity. The VM never entered `RUNNING`; qualification, training records,
  optimizer steps, GPU runtime, and compute cost are all zero. Six
  generation-pinned inputs were independently downloaded twice under identical
  manifest
  `472df5930660c5e37cbdfd79115b9538ca04394921d3875cbad1e9b71ac6b2f1`.
  The terminal request, VM, disk, subnet, VPC, and router scope are absent under
  proof
  `91953aa7e563fdb423e0508e4e06319fcb8aa3be703572b4b5f24e275d91080d`.
  The allocator hypothesis remains untested.

- Executed the approved `us-east1-b` G2 L4 Flex-start run under prefix
  `20260824T161956Z`. The 23,659,151,360-byte L4 passed exact environment,
  external-kernel, model, tokenizer/template, and text-inference checks. BF16
  LoRA OOMed on a 2.72 GiB loss allocation. NF4 with
  `expandable_segments:True` passed training structure but still OOMed during
  the 2,944-token synthetic backward envelope; no real record or optimizer
  step ran. The BF16/NF4 evidence seals are
  `ee7a07c910d059393b1ba15cc516c4bf78a02921fb85f6003140880802c82669`
  and
  `f1d43f17c03b1833635d563d83be9e0a81d1a3370dbd90aaa6743f71dc057c50`.
  All 32 terminal objects passed two immutable-generation downloads under
  inventory hash
  `04eb8aa2204555a33a1c8117c017c678c9f3448060ee968bf15c7461e7743585`.
  The run-result, backup, and teardown seals are
  `c59d09d513a7e28f882d957e6ba22fbe2899edaf68cafea1a3ad4c0a17dba036`,
  `3c289a929bde8b673b3e7a411989f6ec3ace0808052f347b4dd29c9946408843`,
  and
  `11d6011b335c5771c1adcf50a0a30825bd8ae50c7556e189df5bbf27bb53c034`.
  VM, disk, subnet, VPC, and router scope are absent. The conservative
  incremental upper bound is `$0.5686070833333333`, below `$1.00`.

- Diagnosed the dominant 2,944-token allocation as full-vocabulary training
  loss materialization: 1,462,108,160 BF16 logit bytes become
  2,924,216,320 FP32 bytes in Transformers causal cross-entropy, matching the
  observed 2.72 GiB request. The local candidate now pins Liger Kernel 0.8.2
  and enables only Qwen3.5 fused linear cross-entropy with
  `skip_logits=True`. It fails closed if training returns logits. Sequence
  length, rank, alpha, data, optimizer, and serving behavior are unchanged.
  The full local suite passes: 197 passed, one intentional integration skip.

- Rebuilt the pinned Linux AMD64 CUDA image locally after increasing Docker
  Desktop from its inadequate 4 GiB/5-vCPU allocation to 12 GiB/8 vCPUs. The
  image is
  `ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1-liger082`, ID
  `sha256:cdaf068ffcb933120181168ebf6ae1546ddf81e01b2ad006a1a18dd2e43d9860`,
  and size 8,372,032,086 bytes. A network-disabled AMD64 smoke verified the
  exact Torch, Transformers, FLA, causal-conv1d, and Liger versions plus
  Liger's Qwen3.5 multimodal fused-loss forward and `skip_logits` contract.
  Two final workspace builds produced the identical 1,773,034-byte archive
  SHA-256
  `806a5a400278bf7c13092514f5f7b4d8fa0909697ff0cf6a0f9c2b6e8d503310`.
  The local prequalification is sealed by
  `32db10f29dcf15969ccf89db18e55586c1941a758e31c3754bafada529063c0f`.
  The approved execution card is sealed by
  `de09844691ea1ede2d9ef22e152b4289699b656fbf119523795a361207f96efa`.

- Passed Gate 0B under GCS prefix `20260824T180957Z`. BF16 LoRA completed all
  16 real records and optimizer steps after the full 2,944-token envelope.
  The qualification evidence seal is
  `d5c8df044c0b49b1473a2a13e163bcd7acfc06da09b1ea9a0bea75aa1d493a6a`.
  Adapter reload had zero maximum logit difference; safe merge produced finite
  logits with `0.125` maximum absolute difference. The merged 4,426,558,864-byte
  checkpoint and all other 40 terminal objects passed two independent
  generation-pinned reads. The backup, run-result, and teardown seals are
  `d4cd0d2f31f43e081183eef4ff191c2b3aa53eeb2e11763dd4dd723ad1f25cdf`,
  `b29db7d69b7a9653b6be7b4f79390d00a62f2176228f7a995a5ff0b48f85c84d`,
  and
  `95e4ed973cdc746795f0ee1b59045adbce1ceda8bb7af4a8902be86308bcf2f0`.
  Provider auto-delete removed the VM and disk; the subnet and VPC were also
  deleted. The conservative incremental upper bound is `$0.9686175`, below
  the approved `$1.00` ceiling.

## Next action

Gate 0B, Gate 1, and Gate 2 are complete. Gate 3 v2 has one valid completed
`1e-5` training artifact but no executable canary result. The local verifier-
loading repair, v2 workspace, and campaign rehearsal are sealed. The next
cloud action, after a fresh explicit approval and clean execution card, should
reuse the generation-pinned completed `1e-5` adapter as an immutable candidate
input, run its canary, train `3e-5`, run that canary, select the LR, and execute
the selected candidate's full 180-task evaluation. It must not retrain `1e-5`
unless resume/import validation cannot prove the exact completed artifact.

Data expansion remains premature. Comparable validation loss moved in the
right direction across all five product families, but executable behavior was
never measured. Only the completed canaries and full development evaluation
can distinguish seed insufficiency from a useful conservative seed adapter.

The local cloud layer now prepares a Gate 3-only campaign on one
`g2-standard-12` L4 Flex-start VM in an explicitly approved `us-east1` G2 zone.
It allows two hours for provisioning, caps runtime at four hours, reserves the
last 30 minutes for terminal backup, and caps incremental cost at USD 5.00.
This bound is based on executed attempt `20260826T042539Z`: 400,652 training
tokens took 1,845 seconds and a full 180-task candidate evaluation took 1,710
seconds. Two 461,235-token candidates, two 30-task canaries, and one full
selected-candidate evaluation therefore retain substantial contingency without
the obsolete 18-hour envelope.

The evaluation v2 workspace seals the canonical 180-task base result and the
deterministic canary. The training v2 workspace seals the unique-row weighted
seed and contains no evaluation surface. The guest verifies the canonical Gate
1 report against the bundled base run, trains both candidates, selects on the
canary under the frozen rule, and fully evaluates only the selected already-
trained candidate. It does not regenerate the base and does not run a third SFT.

The preparation record at `measurement/gate3/gcloud/preparation.json` is a
repaired full-campaign fallback and is `prepared-not-executable`. Before asking
for another cloud approval, a continuation preparation must additionally bind
the completed `1e-5` candidate as an immutable imported input and prove that
the controller cannot retrain or replace it. Fresh price/quota preflight,
generation-pinned uploads, and a clean-commit execution card remain missing.
The public-price conservative upper is `$4.351665392`, below the proposed USD
5.00 ceiling. The launcher retains two-minute GCS checkpoints, fail-closed
backup, exact-resource teardown proof, and double immutable-generation
verification. Its maximum-runtime action is `STOP`, not `DELETE`, so the boot
disk survives until the local finalizer independently verifies the complete
terminal GCS inventory. Only then may the finalizer delete the VM, disk,
subnet, and VPC. Any terminal-integrity or deletion-gate failure preserves the
stopped resources. No GCloud action occurred while preparing this revision.

The terminal validator is now version-aware. Historical Gate 1 success still
requires its generated baseline, while Gate 3 v2 success requires both
candidate training artifacts, both canary task-evidence collections, sealed LR
selection with exact collection hashes and lane counts, the selected
candidate's complete SFT and save/reload evidence, its 180-task collection,
every promotion check, and the terminal campaign seal. The output has a
dedicated Gate 3 terminal schema. This prevents both a valid reused-baseline
run from being rejected by the obsolete Gate 1 contract and an incomplete
candidate path from being trusted through phase-ledger claims alone.

The dependency-complete `.venv` suite passes with only the intentionally
disabled Docker integration test skipped. Forcing that optional test on the
Apple-Silicon Docker host is not a current native verifier result: the
Linux/AMD64 Go compiler exhausts the emulated container's 32-process sandbox
limit. The production Linux/AMD64 archive already passed all 1,080 executions
on GitHub Actions with zero timeouts, so the emulation failure does not alter
Gate 1. It remains a local portability diagnostic and must not be reported as
fresh native directionality evidence.

## Authorization state

All work within the Ganesh Mini objective is authorized, including the Ganesh
v0.1 seed corpus, local and non-GCloud compute, downloads, long-running jobs,
training, evaluation, repository operations, and artifact publication.

GCloud usage is the only standing authorization boundary. The approved
`us-east1` fused-loss Flex-start L4 execution is complete, double-verified in
GCS, and fully torn down; no run-scoped compute or network resource remains.
Non-GCloud compute remains standing-authorized. The staged Gate 1-through-3
attempt in `us-east1-c` is complete, sealed, and fully torn down. Its
conditional `us-east1-d` fallback was not activated because `c` provisioned.
Any replacement GCloud execution requires fresh explicit approval plus current
price/quota preflight and a new executable card.

No recurring goal-alignment heartbeat or deviation-review subagent is active.

## 2026-08-25 — Staged retry reached the campaign, failed on Docker-name case, and was fully torn down

Approved attempt `20260825T061157Z` passed fresh price, quota, identity,
absence, and two-read GCS preflight; provisioned one `g2-standard-12` L4
Flex-start VM immediately in `us-east1-c`; and authenticated every immutable
input generation. The guest verified both isolated workspaces, Gate 0 and Gate
2 receipts, the exact upstream model, the qualified CUDA image, the offline
Docker bundle, and all verifier images. CUDA image import and NVIDIA Docker
configuration also completed successfully.

The campaign then failed after workspace isolation and before the first of 180
baseline tasks. The outer controller correctly requires the canonical
uppercase UTC attempt ID, but the nested baseline host reused that evidence ID
as a Docker container name and still allowed only lowercase slug characters.
Its sealed diagnostic is `staged campaign failed: invalid baseline attempt ID`.
No baseline metric, training step, decision prompt, or candidate artifact was
produced; Gate 1 remains closed.

The controller and wrapper backed the runtime and diagnostic envelope to GCS
and shut the VM down. Finalization rejected that envelope because the
checkpoint command had appended to `gcs-backup.log` inside the directory it
was simultaneously hashing and uploading. The inventory therefore recorded
the empty-file hash while GCS preserved the subsequently written 4,746-byte
log. This is a genuine integrity failure, not an admissible terminal result.

Because the normal finalizer failed closed before deletion, the exact stopped
VM, auto-delete disk, subnet, and VPC were then deleted explicitly. Four
independent exact-name provider listings are empty. Their five-object manual
teardown envelope was downloaded twice by immutable generation under backup
seal `5e210a79f37ea445a87d5b3f3c76657c618e86cdc60c12f60d6df1de75cc2747`;
the manifest itself is also stored in GCS at generation `1787639587497426`.
No run-scoped resource remains.

The permanent repair preserves the uppercase attempt ID in every evidence
contract while deriving lowercase-only names for baseline, training, and
evaluation containers. Checkpoint output now stays under `/var/log`; all
runtime writers are stopped and awaited before that fixed log is copied into
the evidence tree and the terminal inventory is written. Regression tests use
the exact production ID `20260825T061157Z` and enforce stop, capture, hash, then
backup ordering. The rebuilt non-executable preparation seal is
`ef3bc566ed3db33602d27e2d15ad52541674e6febce9cb8af92ba08a13950bf8`.
The approved one-retry GCloud scope is consumed; another cloud execution needs
fresh explicit approval.

## 2026-08-25 — Retry exposed a post-create generation overwrite and was fully torn down

Approved retry `20260825T055326Z` passed fresh price/quota/identity/absence
preflight and two-read GCS verification, then provisioned immediately in
`us-east1-c`. The fixed UTC attempt-ID contract passed. The controller stopped
before downloading any model or verifier assets because the launcher uploaded
the execution card once to bind its immutable generation, created the VM, and
then uploaded the same card path again alongside the launch receipt. With
bucket object versioning unavailable, the second upload replaced the bound
generation. The guest correctly rejected the stale generation URI and exited
`1`. No baseline task, training step, or decision prompt executed.

The VM was stopped immediately after the anomaly was confirmed. The guest had
already backed a six-object partial runtime envelope and a four-object wrapper
failure envelope. Their independent backup seals are
`6597132edc1f8444da5527544ad27316cc2f98cfeebcb1e9b8c78f67b086b7ba`
and
`29460913df428feb9c6f10bd44e52ae795987263324e897b703bdbd1b3a9e796`.
The finalizer now permits recovery from this partial state only after verifying
its original inventory and wrapper independently, requiring matching nonzero
exit codes and diagnostics, and preserving the original inventory bytes inside
the recovered terminal envelope.

The recovered terminal is correctly `sealed-failure` under seal
`797012a6f738b620cb17bdc25a54fd8f6c0bb87ff935af7654bfc73722f1b45d`.
Deletion-gate seal
`45cfc61789af7dde2b48c42976a70a481af138468601315000a465a2f843f1d7`
passed. The VM, auto-delete disk, subnet, and VPC were deleted; absence-proof
seal
`591491e56d98abe382c4bd427259887ef4e493072f35521c300c096c2ae0d35f`
proves all four identities absent. Finalization seal
`1c78b87a257672d5a417485727fe23e554867dd74a0aa6e56d57a5545592cad1`
and final 15-object post-delete backup seal
`fa1ad6dede3deeb6318b8ef3a53b5615aedca829492a8f279679793b4091c7f1`
close the attempt. Provider timestamps bound creation-to-stop to about 157
seconds; this is not an asserted invoice amount.

The launcher now uploads only the new launch receipt after VM creation and
never overwrites generation-bound bindings or the execution card. Direct tests
enforce this ordering and the partial-terminal recovery invariants. The full
suite passes with the one intentional Docker integration skip. The rebuilt
non-executable preparation seal is
`404b92eca32b6b19832abab41329a47e3e2b180fb132c874c4d67223641bdc97`.
Gate 1 remains closed and training has not started. The one-retry GCloud
approval is consumed; another execution requires fresh explicit approval.

## 2026-08-25 — Provisioned Gate 1 attempt failed before baseline and was fully torn down

Approved run `20260825T052909Z` passed fresh preflight, immutable input upload,
and executable-card binding, then provisioned one `g2-standard-12` Flex-start
VM in `us-east1-c`. The metadata wrapper authenticated and downloaded the exact
controller, but the controller rejected the launcher-generated UTC attempt ID:
the launcher emitted `20260825T052909Z` while the controller allowed only
lowercase slug characters. It exited `40` before creating the runtime evidence
directory. No model or verifier image download, baseline task, training step,
or decision-set access occurred.

The wrapper backed its exact four-object failure envelope to GCS. Because the
failure preceded runtime inventory creation, the finalizer was hardened to
recover only from an empty terminal prefix plus that independently double-read
exact wrapper envelope. Recovery binds both bootstrap hashes to the execution
card, requires a nonzero integer exit and nonempty diagnostics, then creates a
sealed terminal inventory without promoting any model result. Terminal
validation seal
`56b3d0f6d3215dfd1f8d1ef4b473f195ce0e29eb5c7c6450c3a2c12e6221e87a`
correctly records `sealed-failure`; deletion-gate seal
`9dc479102c03a838a8e2b7d248b0ea114bbfed30d817550dc61d0f168747144f`
records `passed`.

The VM, auto-delete disk, subnet, and VPC were deleted. Provider queries and
absence-proof seal
`349071ab20135cbb8e506863de0468b1118e0805e8483278ab2e52107aab154d`
prove all four exact identities absent. The finalization seal is
`35bedced6370830b8ce1406efa8ca9b712f6c4b487cabb6f0807420c2a471f32`;
the final 14-object post-delete backup seal is
`6d64a411d904c8ce540c1e84e6773ff7b4e2c28385459c207225cea01cf3139c`.
The provider timestamps bound creation-to-stop to about 132 seconds, far below
the approved runtime and cost ceilings; this is a conservative time bound, not
an asserted invoice amount.

The permanent controller contract now accepts only the launcher's exact
`YYYYMMDDTHHMMSSZ` attempt format, and focused recovery/validation tests pass.
The rebuilt non-executable preparation seal is
`4f6cda6e3a1b3003d59385ecd80685048df9c09f2a074ef0af1bd2b89b7e4a7c`.
Gate 1 remains closed, no training has started, and the conditional
`us-east1-d` fallback is no longer authorized because `us-east1-c` provisioned.

## 2026-08-25 — Staged campaign launch reached provider stockout and was fully torn down

Approved run `20260824T204540Z` passed account, project, current price, quota,
machine/image, exact-resource-absence, and GCS round-trip preflight. All sealed
evaluation, training, model, image, verifier, controller, and execution-card
inputs were uploaded with immutable generations and the preflight prefix passed
independent double reads before infrastructure creation.

The `g2-standard-12` Flex-start create in `us-east1-b` exited before a VM or
disk was provisioned. Its interactive provider stderr reported
`ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS`, but the launcher did not redirect
that stderr into the run directory; therefore the exact provider message is
not decision-grade sealed evidence and must not be reconstructed as such. The
sealed record proves create exit code `1`, an empty create JSON, and complete
absence of the exact VM, disk, subnet, and network identities. The temporary
subnet and VPC were deleted after the first verified failure backup. Cleanup
seal `63b8e20e9a1caeb2659d66f5bae4c170bd2d241a897dd868567b073c25e0efbd`
and final 68-object backup seal
`c7222bd9917be67b5fb458f704d363821704d53b234b1d94061209c7dc17ff92`
close the attempt. No VM or GPU runtime occurred; only storage/API operations
and short-lived free network objects were used.

Before another request, the launcher now captures provider-create stderr,
binds the execution card to the selected approved zone, and permits only the
official G2/L4 zones `us-east1-b`, `us-east1-c`, and `us-east1-d`. Immutable
GCS verification still performs two independent generation-pinned reads per
object, now with a bounded default of eight concurrent objects to remove the
serial cleanup bottleneck. The replacement preparation seal is
`682b9466b306dffe9c3155a5828cc46e075138edc9f7aa338472bd01b1e0c34c`.

Gate 1 remains closed and no training has started. The next GCloud action is
blocked on a fresh explicit approval. The recommended bounded fallback is one
aggregate campaign attempt sequence in `us-east1-c`, then `us-east1-d` only if
`c` fails before provisioning, with at most one running VM and the existing
18-hour runtime and USD 19 aggregate incremental ceiling.

## 2026-08-25 — Gate 1 Linux bytecode mutation failed closed and was repaired

Approved attempt `20260825T085926Z` passed fresh price, quota, resource
absence, GCS round-trip, immutable input, and double-read preflight checks. It
provisioned `g2-standard-12` VM `ganesh-mini-g1-l4-20260825t085926z` in
`us-east1-c`. All staged downloads matched their hashes. The offline Docker
installation, NVIDIA container runtime, qualified CUDA image load, exact image
ID, and GPU inspection passed.

The campaign stopped before baseline generation with controller exit `1` and
the exact diagnostic `extracted development workspace file set mismatch`.
Workspace isolation had passed immediately before the baseline helper import.
On Linux, that import created in-tree `__pycache__` files because the extracted
workspace was host-writable; the helper then correctly rejected the mutation.
The earlier Mac rehearsal did not expose this because that interpreter directs
bytecode to an external user cache.

The terminal is a strict `sealed-failure` under seal
`cbc3bb69978ad0bcd526f195b94526aa71caf03d48ccb7356b24dd240e500334`.
Deletion gate
`090f96e55c1f3ba857e9bf8cccb409cc14fc627b54be3f269fe2478a139dc257`
passed. The exact VM, auto-delete disk, subnet, and VPC were deleted; absence
proof
`ba7e3cf424d8c981a280ece41dfdfddcf186803cc2af4312d77f81e7a9e8adf7`
proves all four absent. Finalization seal
`84b11ce6b3cb2703e610bf4024dbf2c824be57a959c11f35af57c1dc675fd7f4`
and final post-delete backup seal
`308d4da01f815963808989aec625644d2df4d75d3a9aaafd51187c4a164de1bd`
close the attempt. Provider start-to-stop time was about 536 seconds; this is a
runtime bound, not an asserted invoice amount.

The startup controller now invokes the campaign with `python3 -B`, and the
campaign independently sets `sys.dont_write_bytecode`. The runtime rehearsal
forces in-tree bytecode semantics, imports the archived modules, and asserts
that the extracted file set remains identical to the 214-file manifest. The
evaluation archive is resealed at
`f5a1518ab6d24d3fce649838fb623115988478b508541a5ccb05c13842b868eb`;
the rehearsal and preparation seals are
`e9d39a0e486c192b05c62810e8ef94fbb39c665c96f2d66af5cad0b009a10902`
and
`4e52713bcf6caa2f4438a21de8e408c42724d7f34f61c16a238bb88690eca0b9`.
The complete local suite passes. Gate 1 remains closed, no training has
started, and the consumed one-attempt approval does not authorize another VM.

## 2026-08-25 — GitHub Actions removed

At the user's direction, both repository workflows were removed and GitHub
Actions was disabled at repository level. Historical native AMD64 and Gate 1
workflow run IDs remain provenance records only. Current validation is local
or part of an explicitly approved GCloud execution; no push or manual GitHub
workflow can run.

## 2026-08-25 — Read-only nested Docker mounts failed closed and were removed

Approved attempt `20260825T103213Z` provisioned one `g2-standard-12` Flex-start
L4 VM in `us-east1-c`. Fresh price/quota/resource-absence/GCS preflight passed;
all immutable downloads, hashes, Docker and NVIDIA setup, exact CUDA image,
verifier runtime readiness, bytecode immutability, and workspace isolation
passed. The base container then exited `125` before model loading because the
host model directory targeted `/workspace/models/qwen3.5-2b-15852e8`. That
target did not exist in the sealed archive, and Docker could not create it
beneath the read-only `/workspace` bind. No baseline task, inference token,
training step, or decision prompt executed.

Terminal validation is correctly `sealed-failure` under seal
`189a75945ba4619cab3a781090b588a6614dd86f835d2108a37f28551732d125`.
The deletion gate seal is
`a8f6762bb0a2c1439950beeaad8e753c0f28013bc636855b7d67421f3674189b`;
absence proof
`3f2a08d74b521eb1a139505b2d77e4c7986aa1819408043135d5e32bae27189b`
proves the exact VM, auto-delete disk, subnet, and VPC absent. Finalization seal
`ad2b702484b4a4d0fcc1b0d8569fd7fa49ac079a8e5d96a7330f900b4717f5c9`
and final 14-object post-delete backup seal
`84fb612a6b279a678635d2623d488840e31c72d60b2ce236d2af4fbcc3a03084`
close the attempt. Provider start-to-stop time was about 588 seconds; this is a
runtime bound, not an asserted invoice amount.

The repair removes the whole nested-mount failure class. External model,
training/adapter, output, and control binds use independent top-level container
paths; `/workspace` remains the only sealed read-only code/data bind. Runtime
path overrides do not mutate the frozen config or logical evidence paths. A
mount guard rejects external targets at or beneath `/workspace`, and the
archive rehearsal executes the exact archived baseline/campaign builders.
Evaluation archive seal
`497fdc835ac134d2a20a5fee96e063d60511ef6555f9e2df40db82d054ee5e2c`,
rehearsal seal
`8747337210b167a9b0099e605b98c3b7fbcf1e3b291066687b887fad3765aea0`,
and preparation seal
`7131fb8c768fad2c70bec28d36fb375a92d2e52911803265deec6559208628da`
bind the repaired bytes. The full local suite passes. Gate 1 remains closed;
the consumed approval does not authorize another GCloud VM.
## 2026-08-28 — Expansion production recovered at 1,403 rows

The first production controller failed closed after a transient Docker Desktop
bind-mount race while verifying the known-bad implementation in sealed batch
`java-0029-g0180n6-r0120n4`. Docker returned exit `127` because its translated
`/private/var/folders` source briefly did not exist inside the Docker VM. This
was verifier infrastructure failure, not candidate failure. The controller
drained already-running lanes, preserved 1,393 accepted rows, and exited.

Expansion admission now uses a stable `/private/tmp/ganesh-mini-verifier` root
on macOS and retries verifier infrastructure failures at most three times,
retaining every failed attempt in expansion evidence. Persistent
infrastructure failures are separated before the teacher-repair path. The
production controller now holds a non-blocking process lock and can recover an
exact failed/running batch only when its candidate hash and teacher selection
match the sealed evidence; recovery neither regenerates teacher output nor
advances queue offsets.

The exact Java batch was reverified from candidate SHA-256
`4b28b4d553ef0d495e902d6e3ea928036a29c5396f3d6022f6cf906a7fee3f0f`
and admitted 10/10 with zero remaining rejection. Production is paused at
1,403 rows under corpus SHA-256
`9c05e3d2efd510cf857e23e0bb1a2678877a2bef89383c983dcb4eac6ebb968f`.
A six-way, 30-execution local Docker mount smoke passed without failure, and
the complete local test suite passes with one intentional skip. The next
action is to resume exactly one five-worker local controller.
# Active recovery r3 — 2026-09-08

Gate2: actual local generation session49105, 14 approved generation parents,
8JavaScript/6TypeScript, two concurrent lanes under maximum3. Immutable plan
617a754bf9ae98a4e595077de132e15c5556db21554da5f7d98a9f88e236a712;
see HANDOFF.md and RECOVERY_R3_SELECTION_20260908.md. Remaining43 proposed
parents are queued, not approved/admitted. All recommendation notes main-read.
144 data tests pass; prior9 admission hashes verified and automatic accumulated
recovery dedup added. No r3 admissions or training progress counted. Original
holds2812, admitted recoveries9, maximum combined3082, minimum remaining918.
Training/release estimated50%/35%, not measured task percentages. Nextgeneration
checkpoint10–60min low confidence; full-delivery ETA not supportable yet.
No VM or training. Current local work authorized. Latest verified remote backup
is admission9; active r3 requires terminal evidence backup and byte verification.
# R3 terminal update — 2026-09-08

R3 admitted2 (JS0025/0394), bringing recovery admissions11; original holds2812,
maximum combined3084, minimum remaining916. No training seal. All14 generation
and42 diagnostic executions completed; main integrated allthree quality reports.
R4 generation19 (session57980) and r5 one-time test correction11 (session69865)
are active. See HANDOFF for exact assignments and immutable plan hashes.
144 data tests pass. Next checkpoint15–45min lowconfidence; training/release
estimated50%/35%, full-delivery ETA still ungrounded. No VM/training; local work
authorized. Terminal r3 backup in progress, not yet claimed verified.
# Latest running checkpoint — 2026-09-08

Terminal r3+total11 admission evidence backup VERIFIED: RECOVERY_R3_BACKUP.md.
R4 Go9 generated, serial diagnostics95197 and independent review active; Java
lane preserved as prompt-byte guard failure, requiring a new version disposition.
R5 corrected JS5 pass diagnostics and main-accepted quality, not yet admitted;
TS6 correction active69865. R6 generation11 active28510, one lane worker.
See HANDOFF for exact assignments. No overlapping sandbox verifier should start
until current serial job completes.144 data tests pass. No new admissions beyond
11, no training/VM; estimates50%training/35%release, next decision15–45min low
confidence, full delivery ETA not supportable. Later/active runs need new backup.
# Admission21 — 2026-09-08

R5 admitted10 after quality and actual execution/separation, bringing21 new
recoveries (Go2,Java2,JS9,TS7,Python1,Rust0). Max combined3094,min remaining906;
original holds2812 unchanged, no final corpus/training seal. See R5 admission
report and HANDOFF. R6 actual diagnostics19463 active; r7 correction53332,
r8Java retry49992,r9 correction22325 active. All prior review reports integrated.
144 data tests pass. Terminal evidence backup in progress, latest verified
remote checkpoint still11 until proof. No VM/training or permission blocker;
training/release estimated50%/35%, next10–30minlowconfidence, overallETAungrounded.
# Admission25 and verification queue — 2026-09-08

R6 adds4 admitted(3Python,1Rust), total25 recoveries; maximum combined3098,
minimum gap902,original holds2812 unchanged. No corpus/training seal.
R7/r8/r9 generation complete. ONEserial verifier41369 runs r9six->r8ten->r7nine;
no parallel verifier/admission until it finishes. Main accepted r7/r9 staticreviews;
r8 finalreport pending main integration. See HANDOFF.144data tests pass.
GCS checkpoint through21 verified; newer r6admission4 andr7/r8/r9 await backup.
NoVM/training; estimated50%training/35%release, next20–45minlowconfidence,
overallETAungrounded. Current localwork authorized.

# Gate 4 prelaunch boundary — 2026-09-09

Gate 2 is terminal at 3,225 rows and 2,438,853 input tokens. All Gate 4 launch
inputs were rehydrated to GCS because the historical August generations had
expired. Model, CUDA image, Docker runtime bundle, verifier archive/manifest,
training workspace, evaluation workspace, and launch scripts now have exact
generation bindings and downloaded byte-for-byte SHA-256 proof. The canonical
input-restoration receipt seal is
`9648e00f7ab3c16aac6d4052d4be3345a663bd3fc74497168695c8f1bbf7302b`.

Read-only GCloud evidence shows `us-east1` and `us-east1-c` UP,
`g2-standard-8` at 8 vCPU/32 GiB, L4 quota 16 with usage 0, and boot image
`common-cu129-ubuntu-2204-nvidia-580-v20260831` READY. This does not prove
point-in-time capacity. The exact Standard proposal uses a 200 GiB balanced
disk, an eight-hour maximum lifetime, and a `$7.50` absolute incremental
ceiling. Proposal seal:
`5bb6b25b448a509f570dd924b6d508ab057fd2f2455d06db8353054cda06aba3`.

The launch controller enforces network-disabled Docker execution, immutable
input checks, 8 CPU/30 GiB container bounds, periodic GCS checkpoints, a hard
shutdown watchdog, terminal backup, and conditional full evaluation. A failed
promotion gate is recorded as `completed-canary-not-promoted`, not as an
infrastructure failure. Fifteen focused tests pass. The full suite has the same
three pre-existing stale Gate 1 evidence failures and no new failure.

No VM or other compute resource exists. Current state is
`waiting-for-exact-execution-approval`; do not bind the provider card or create
GCloud compute until that approval is received.

### Gate 4 approved attempt active — 2026-09-09

- Navneet approved exact proposal
  `5bb6b25b448a509f570dd924b6d508ab057fd2f2455d06db8353054cda06aba3`
  with an absolute incremental ceiling of `$7.50`.
- Attempt `20260909T015118Z` is running on the single approved Standard
  `g2-standard-8` L4 instance in `us-east1-c`; instance ID is
  `8737372232357839343`. It has no external IP, a 200 GiB auto-delete balanced
  disk, restart disabled, and provider-enforced eight-hour deletion.
- The initial bootstrap failed closed before training on a 65-character
  evaluation-manifest hash copied into the proposal. The unchanged object and
  local roundtrip file have the correct 64-character SHA-256
  `cf88badcc33c78c824c24dc67c9accf9f5c3527fe3b140e4218f33f59c42a360`.
  Failure evidence is preserved in GCS.
- Only that binding was corrected. Outer card v2 generation is
  `1788919774477052`; the same VM was restarted. Guest checks passed all ten
  immutable inputs, and the campaign phase ledger reports
  `workspace-and-provider-admission=passed` with status `running`.
- Do not create another VM. Continue checkpoint monitoring, then terminal
  roundtrip verification, teardown, two absence checks and the
  no-billing-except-GCS audit.

### Gate 4 same-VM retry prepared — 2026-09-09

- The v2 campaign passed workspace/provider admission and verifier-image
  readiness, then exited before model initialization because the host passed a
  dynamic elapsed prior cost where the sealed training card requires `0.0`.
  Zero training tokens were consumed.
- Terminal evidence was exact-generation downloaded and inventory-verified.
  The distinct GCS failure archive has generation `1788920860248908` and
  SHA-256
  `e8b53c43e9d579091f5ce8ca6f99e07898b410895680b41c3566afad4d0e5bdf`.
- The VM is `TERMINATED`; disk/network/subnet remain for a same-VM retry. No
  second VM is authorized or needed.
- Controller fix and regression test pass. Workspace v5 and startup v3 are
  uploaded and exact-roundtrip verified. Next bind a fresh attempt prefix,
  update the retained VM metadata, and restart the same provider instance.

### Gate 4 retained-disk bootstrap retry correction — 2026-09-09

- Attempt `20260909T022847Z` reused the same VM and verified all ten input
  downloads, then failed before controller/model/training on an interactive
  Docker-package debconf question during retained-disk reinstall.
- The VM is again `TERMINATED`; zero training tokens were consumed. The exact
  failure archive is GCS generation `1788922020962270`, SHA-256
  `af0dd839bbe717ac9aea59f9ca78b54e45adc4fcddd2e3dd9ece9797e16249db`,
  with byte-identical generation-pinned roundtrip proof.
- Startup now forces noninteractive debconf and needrestart behavior, preserves
  installed configuration, and bounds `dpkg` calls. Focused tests and shell
  syntax pass.
- Next is startup v4 upload/roundtrip and another same-provider-ID attempt under
  a reduced remaining runtime envelope. No additional VM is authorized.

### Gate 4 training active — 2026-09-09

- Attempt `20260909T025013Z` is running on the original instance ID
  `8737372232357839343`; no second VM exists.
- Startup v4 and the fresh outer card are generation-pinned and byte-roundtrip
  verified in GCS. Provider lifetime is reduced to 27,000 seconds with restart
  disabled and termination action `DELETE`.
- The retained-disk package fix passed. Runtime checkpoints exist and the
  campaign ledger is `running` with workspace/provider admission passed.
- Current phase is model initialization/training. No permission blocker. After
  terminal backup: exact inventory verification, full teardown, then two
  resource-absence and billing checks.

### Gate 4 terminal and checkpoint diagnostic — 2026-09-09

- Training completed at 2,438,853 tokens. The final adapter scored 6/30 versus
  base 5/30 on the frozen canary, improving only Rust; the terminal decision is
  valid `do-not-promote`. Full 180-task candidate evaluation did not run.
- All Ganesh VM, disk, subnet, and network resources were deleted after a
  verified 128-object terminal backup and exact-generation archive roundtrip.
  Two absence checks passed. No Ganesh compute is active.
- The earlier claim of one stale base evidence seal was wrong. The reader
  ASCII-escaped U+00E9 while the evidence contract hashes UTF-8 JSON. A sealed
  audit validates all 180 task seals, the run seal, and all 360 generated and
  verifier bindings; no evidence was repaired. Audit seal:
  `307bff0cafd28b02278b5fdcbbd7117677269cd9707d6beaba133f22dba96c98`.
- A local evaluation-only sweep package covers the five earlier saved
  checkpoints. It has no training or promotion authority. The next hard stop
  is explicit GCloud approval to upload and generation-bind its new inputs;
  after that, VM execution requires approval of the resulting exact proposal.
  Planned VM bound is one Standard L4 for at most two hours and $2.25.
- The sealed local sweep workspace has 596 files, manifest seal
  `0b5baf8ded482fefa8b827169fc425c6881365e1a08ed814bcda226e4ffa94ae`,
  and archive SHA-256
  `8a3619ee9bbb9816359eecad4c7b46c92f202644e29090880b3d44e7b485d3d6`.
  Exact extraction verification and 26 focused tests pass.
- Pending upload-only plan seal
  `22357cac8b6da43aa56bd11eaede2f199995a90035aa76caf5c235ccb485cc4b`
  permits four named GCS objects totaling 1,163,234 bytes plus immutable-
  generation roundtrip checks. It authorizes no compute or infrastructure and
  still requires fresh explicit GCloud approval.
- The upload-only plan was explicitly approved and completed: four objects,
  1,163,234 bytes, exact-generation byte roundtrips passed, and no compute or
  infrastructure action occurred. Receipt seal:
  `36711a078822cca4ffa60da6f8c2f368ad1c1454d199c9051355f22052088e81`.
- All ten inputs are bound under seal
  `2ba45d22404120afe6b081aa67455d3604a717a349a4cfe1c20225055b036763`.
  Exact evaluation-only VM proposal seal
  `b31d95b6e9097fa1056a522628773240d0c2d80ebd925becf457163b28900db5`
  has a 7,200-second maximum, provider bound `$1.762043024`, and `$2.25`
  absolute ceiling. State is `waiting-for-exact-execution-approval`; no cloud
  compute is active.
- Project-wide GCS-only billing is not certified because unrelated unattached
  disk `laxmi-wmv2-training-01` remains; its ownership/deletion is a separate
  user decision.
# Gate 4 capacity probe awaits exact execution approval — 2026-09-09

The read-only GCloud prerequisite inspection is complete under approved plan
`50b3783cb1287bfa3a44e00772db6f24bfd2b70b8d102b1b9f537276042fd521`.
All four planned resource names are absent; zone/type/quota, VM bucket IAM and
all ten exact-generation inputs passed. Inspection report seal:
`74b3757f92d614a4f65d02bd4f8a60b15aac5134a9e1d0acd98c05a466bb4a0f`.

One bounded Standard L4 proposal is now pending explicit approval: seal
`461e968ae2fa79d3401e522d52bf91cbcc359cdded68d8fff62dff51631934f0`,
maximum 7,200 seconds, provider upper `$1.762043024`, absolute ceiling `$2.25`.
It includes two post-approval create-only card uploads, the 624-row/468,601-token
capacity probe, save/reload, and only the frozen 30-task continuation screen.
No GCloud mutation or billing action has occurred under the read-only plan.
Current state is WAITING FOR EXACT EXECUTION APPROVAL, not technically stuck.
Training estimate 74%; release estimate 52%; inception-to-delivery estimate
63%. After approval, capacity verdict ETA is approximately 2–3 hours; final
delivery remains 2–5 days only if the continuation screen passes.

# Gate 4 gradient-conflict probe awaits exact execution approval — 2026-09-13

The v4 local mechanism, cloud inputs, and approved read-only prerequisite
inspection are complete. Inspection report seal is
`d92854a13a237c44cf6a172dfa53794c4c2ce32d77cf8adf9d99ed7b85d08d14`.
The planned names are absent; zone/type/quota, VM bucket IAM, and all ten exact-
generation inputs passed. No GCloud mutation or billing action occurred.

One bounded Standard L4 execution proposal is pending exact approval: seal
`faf9ed1f062f49d6f48c0a3cfeec2beedc1dcd67aa5ab85a757ec384de4af7ff`,
maximum 7,200 seconds, provider upper `$1.762043024`, absolute ceiling `$2.25`.
It first runs a zero-step gradient-conflict audit. Training and the 30-task
canary are conditional on the frozen audit threshold; failure is a valid
mechanism verdict, not an infrastructure failure. Full development evaluation
and every later release-stage action remain out of scope. Current state is
WAITING FOR EXACT EXECUTION APPROVAL; no Ganesh compute resource is active.
Training estimate 84%; release estimate 58%; inception-to-delivery estimate
72%. Conditional probe-to-verified-teardown ETA after approval is 2–3 hours.

# Gate 4 gradient-conflict execution active — 2026-09-13

Exact proposal `faf9ed1f062f49d6f48c0a3cfeec2beedc1dcd67aa5ab85a757ec384de4af7ff`
is approved under the `$2.25` ceiling. One Standard L4 VM is active with hard
provider deletion at `2026-09-13T19:26:52Z`. Input admission passed. The audit
container has ended, but terminal evidence is not yet in GCS; its result is
therefore unknown. Current state is ACTIVE / TERMINAL-EVIDENCE PENDING, not a
model failure. No teardown until evidence is independently recovered and
verified.

# Gate 4 gradient-conflict attempt invalid and fully torn down — 2026-09-14

Attempt `20260911T020000Z` reached the bounded provider deletion time without a
terminal GCS backup. The VM and auto-delete disk are gone; GCS has only the two
input cards. The attempt has no model-result authority and its audit/training
outcome is unknown. The exact remaining subnet and network were deleted, two
absence checks passed, and the wider Ganesh resource inventory is empty. The
unrelated `laxmi-wmv2-training-01` disk remains untouched.

Local root cause is fixed: audit-stop exit code `2` is now admitted only long
enough to validate sealed audit evidence, and all background controller jobs
redirect away from FIFO loggers so orphaned descendants cannot block terminal
inventory and backup. Nine focused tests plus shell syntax pass. Training
estimate remains 84%, release estimate 58%, and inception-to-delivery estimate
72%; this was an invalid infrastructure-evidence attempt, not a model failure.
Next step is to seal and approve new immutable controller/evaluation inputs and
a fresh bounded rerun. Conditional rerun-to-verdict ETA remains 2–3 hours after
its exact GCloud approvals.

# Corrected gradient-conflict rerun package awaits upload approval — 2026-09-14

The finalization defects are fixed, the development-v8 workspace was rebuilt
deterministically, and the corrected source/artifacts are pushed through commit
`c01a99b81e9712e9be5d01d7a09595e8e2c65fee`. Eighteen focused tests pass.
Upload-only plan
`b3cc9c24470a0efa851c986f6dfe9125fe7c627f80f2463d887871542267c0ce`
binds five new immutable objects totaling 7,424,694 bytes. State is
WAITING FOR EXACT UPLOAD APPROVAL; no Ganesh compute is active. Upload approval
does not authorize cloud inspection or a rerun.

# Corrected gradient-conflict inputs uploaded — 2026-09-14

Upload-only plan
`b3cc9c24470a0efa851c986f6dfe9125fe7c627f80f2463d887871542267c0ce`
completed: five create-only objects, 7,424,694 bytes, with exact-generation
byte roundtrips. Receipt seal:
`96a76d12f8d8e5e54556514e83194e7edc4cbe9fccf7144a5c60e0d590ea9e11`.
No compute or infrastructure action occurred.

State is WAITING FOR EXACT READ-ONLY INSPECTION APPROVAL on plan
`e7b1602ca2c01b785cc5f93b9d3b8543e81affecf14c3787ce219cf2bf367c66`.
It binds fresh attempt `20260914T003000Z`; no Ganesh compute is active.

# Corrected gradient-conflict rerun awaits execution approval — 2026-09-14

Read-only inspection under plan
`e7b1602ca2c01b785cc5f93b9d3b8543e81affecf14c3787ce219cf2bf367c66`
passed all resource-absence, provider, L4 quota, IAM, immutable-input and
current-price checks without cloud mutation. Report seal:
`be5a8cebb3b07b9c15a8fff271092bb041d8f3e2c7cef6ac4c969fc5f3ed2017`.

Execution proposal
`af67925bf32f28b2708862a517af58b00f161cbbd66c2c3d00db05987f98cd88`
is pending exact approval under the USD 2.25 ceiling. No Ganesh compute is
active. Training remains 84%, release 58%, overall delivery 72%; conditional
probe verdict ETA is 2–3 hours after approval.

# Corrected gradient-conflict rerun active — 2026-09-14

Execution proposal
`af67925bf32f28b2708862a517af58b00f161cbbd66c2c3d00db05987f98cd88`
is approved and one exact Standard L4 VM is RUNNING. Provider ID is
`268054164708970511`; calculated hard deletion is `2026-09-14T05:50:01Z`.
Execution cards and inputs are generation-pinned. Current state is ACTIVE,
waiting for runtime evidence; no audit, training or quality result is yet
claimed.
