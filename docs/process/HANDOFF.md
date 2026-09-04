# Ganesh Mini 1.0 handoff

Last verified snapshot: 2026-09-04 14:38 IST

This document is an operational handoff, not a replacement for the canonical
plan or evidence. Live state can advance after the timestamp above. Re-read the
files in the "Start here" section before acting.

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
