# Gate 3 selected-pilot development failure: bounded local analysis

Status: diagnostic only; no revised training recipe or GCloud execution card.

## Sealed evidence

- Selected `1e-5` adapter: full unique 900-row, 651,639-input-token epoch,
  113 optimizer steps, and save/reload passed. Its training evidence is
  `measurement/gate3/capability-scale-v1/full-pilot-gcloud/20260930T205829Z/terminal-roundtrip/output/training/run-evidence.json`.
- The frozen 180-task development run completed with evaluation exit 0,
  independently verified terminal backup, and exact resource teardown.
  Its adjudication is
  `measurement/gate3/capability-scale-v1/full-pilot-eval/gcloud/20261001T020646Z/development-adjudication.json`,
  report SHA-256 `4177c8e5782481877d0de5e20b861e46886a3c93138bf2d3a8037e4cfe088cd3`.
- Upstream passed 20/180; the selected adapter passed 19/180. Paired
  transitions: 3 wins, 4 losses, 173 ties. Five-family macro pass@1 moved
  from 0.1000 to 0.0967. Only Python improved, while the requirement is at
  least four of five families; Java and TypeScript each lost one lane pass.
  Go remained 0/30. These are the executed frozen results, not an estimate.
- The 50-row *training-validation diagnostic* five-family record-mean loss
  moved from 0.370317 on the upstream to 0.367116 on the adapter. That loss
  reduction does **not** establish executable capability improvement, and
  the validation set is Python-heavy (30 of 50 records).
- The 30-task canary tied upstream at 5/30 for both learning rates. This was
  a selection tie, not a positive Gate 3 signal.

## Narrow defect observations

The four paired regressions are a TypeScript compile error involving an
unavailable `stream` module and implicit `any`; a Java compile error from
missing collection imports; and two Python verifier assertion failures.
Those are failure *classes* only. Do not copy private task prompts, tests,
solutions, or model outputs into training or candidate-generation inputs.
The three paired wins were Python tasks. A seven-discordance sample is too
small to infer a single root cause. The cluster-aware 95% interval for the
paired delta includes zero, so the observed one-task decline is not a
population-effect estimate; the frozen gate still fails deterministically.

## Prospective correction boundary

1. Keep both completed candidates, the admitted baseline, and the failed
   adjudication immutable. Do not try the unselected `3e-5` adapter on all
   180 tasks post hoc, relabel a quality failure as a runtime retry, or open
   the 360 private decision tasks.
2. Audit the **training-source** corpus locally for language balance,
   instruction-to-code completeness, executable success, truncation,
   duplicate identities, and task-type coverage. Use only independent
   authorized non-evaluation sources for any correction candidates.
3. Separately audit adapter update magnitudes, per-lane training/validation
   diagnostics, and whether the frozen attention-only rank-8 mechanism is
   demonstrably under-capacity. A lower validation loss alone does not
   justify changing rank, learning rate, epochs, or the serving contract.
4. Before another paid run, write and seal a prospective data-or-mechanism
   change with a disjoint candidate source, unchanged private evaluation
   boundaries, a stop rule, expected budget, and an explicit new execution
   scope. The prior $15 ceiling is absolute, not a fresh allowance.

Until such a correction passes a new bounded pilot under the frozen quality
criteria, Gate 3, Gate 4, the decision set, and Hugging Face model release
remain blocked. The separate Gate 0B raw-report recovery gap also remains.
