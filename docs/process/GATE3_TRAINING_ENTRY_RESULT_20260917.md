# Gate 3/4 training-entry assessment result — 2026-09-17

Status: passed for corpus construction; training not started

## Result

The unified qualified inventory is sealed at 174 records: 114 V2 generation
admissions covering all 60 generation cells and 60 V9 repair admissions
covering all 60 repair cells. All 174 record IDs and all 174 source identities
are unique. Every row carries complete prompt, answer, test, redistribution,
and model-training rights.

The lineage marks exactly one deterministic anchor in each of the 120 cells.
The anchor matrix contains ten records per lane/task-type pair, twelve per
primary capability, and twenty-four per scheduled cross-cutting dimension.
No evaluation artifact was read and no training or GCloud action ran.

Canonical artifacts:

- assessment plan: `docs/plans/GATE3_TRAINING_ENTRY_ASSESSMENT_PLAN_20260917.md`,
  SHA-256 `a1606049ce585ced662692ec8f31e29b35fc69a88df5c44339f8af64ac6849d0`;
- qualified lineage:
  `measurement/gate3/training-entry-v1/qualified-lineage.jsonl`, SHA-256
  `f9daacdd55183ac220f926d8135124e4ffba97ea42acd8bb114326b64e19f73c`;
- training-entry manifest:
  `measurement/gate3/training-entry-v1/manifest.json`, manifest seal
  `fbf45982984c2c669e03abf1c773d768019651184547104271de12c42f79318c`
  and file SHA-256
  `41dfcfe11e9ddf25cfe4a0505069818fd8b4e8ca8e1afdfb7ea5871aac618e71`.

## Construction accounting

The 174 qualified records count toward the planned six records per cell. The
remaining capability deficit is exactly 546 admissions: 246 generation and
300 repair. Reaching those deficits produces 720 capability records. Adding
180 broad replay records, fifteen per lane/task-type pair, produces the
intended 900-row bounded-pilot corpus.

## Decision

Proceed with local source-queue sealing and corpus construction under the
existing non-GCloud data authority. Do not train yet. Training requires the
final 900-row corpus integrity, balance, quality, separation, tokenization,
objective-weighting, retention, runtime, and bounded-pilot contracts.

Reuse only the proven SFT execution, checkpoint/recovery, evidence, retention,
and finalization infrastructure after re-versioning. Prior adapters and the
capacity-only, lane-scheduling-only, earlier-checkpoint, and PCGrad mechanisms
remain terminal `do-not-promote` evidence and are not eligible as the new
quality hypothesis. The prospective hypothesis is the materially different
capability-stratified data distribution.

Any GCloud inspection, upload, execution, resource mutation, teardown, or
billing still requires a fresh exact approval.
