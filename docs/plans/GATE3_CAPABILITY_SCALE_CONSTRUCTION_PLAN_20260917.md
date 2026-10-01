# Gate 3 capability-scale construction plan — 2026-09-17

Status: local construction contract; source queue not yet sealed

## Objective

Build the training-only 900-row capability-data pilot corpus unlocked by the
passing training-entry assessment. The target is exactly 720 capability rows,
six in every one of the 120 cells, plus 180 broad replay rows, fifteen in every
lane/task-type pair. This plan authorizes local non-GCloud source selection,
candidate construction, review, sandboxed admission, and evidence sealing. It
does not authorize training, evaluation opening, or GCloud usage.

## Starting inventory

The controlling input is
`measurement/gate3/training-entry-v1/manifest.json`, seal
`fbf45982984c2c669e03abf1c773d768019651184547104271de12c42f79318c`.
Retain all 174 qualified rows: 114 generation and 60 repair. The exact deficit
to six per cell is 546 admissions: 246 generation and 300 repair.

## Draft budget

Use conservative model-call accounting against the original 1,200-draft cap:

- V2 qualification and bounded replacements: 247 drafts;
- V3 repair teacher: 60 drafts;
- V4 repair teacher versions 1, 2, and 3: 180 drafts, counting every returned
  teacher output even when a later version superseded it; and
- V5 fresh teacher replacements: 2 drafts.

Historical usage is therefore 489 drafts. At most 711 additional drafts remain.
Freeze 546 first-pass requests, exactly matching the current per-cell deficits,
and prebind at most 165 source-unique replacements. A replacement is eligible
only for a failed first-pass request in the same cell and only after the failure
is terminally sealed. If 165 replacements cannot reach six admissions in every
cell, stop; do not exceed the 1,200-draft ceiling.

The original qualification plan's ten-drafts-per-cell field cannot be applied
across all superseded V2–V5 contract attempts: a repair cell has one retained
admission, at least six conservatively counted historical drafts, and still
needs five new admissions. This scale contract therefore supersedes that
incompatible per-cell field prospectively while preserving the stricter global
1,200-draft ceiling. In the scale phase, each cell may receive only its exact
first-pass deficit plus at most two replacement drafts. The 165 replacements
are allocated as one slot for every cell plus a second slot for the first 45
cells in deterministic seeded order.

## Source selection

Select from the sealed training-source queue only. Exclude:

1. every source represented in the prior 3,225-row corpus;
2. every source used by any V2–V5 teacher draft, including rejected,
   unresolved, superseded, and replacement outputs;
3. every source in the 174-row qualified inventory; and
4. every source already assigned elsewhere in the new first-pass or reserve
   queue.

Within each cell, order eligible same-lane/task-type sources by seeded SHA-256
over the plan seal, cell ID, source queue ID, and full source identity. Assign
the first `cell_top_up` sources to first pass. Allocate the 165 replacement
slots deterministically across cells by seeded round-robin: one per cell, then
a second for the first 45 cells in the same seeded order.

## Construction and admission

Use the V9 canonical test-author and executable contract prospectively:

- teacher visibility is limited to one training stimulus, the assigned primary
  capability, scheduled cross-cutting dimension, and pinned lane runtime;
- test authors see only the specification and controller-owned runtime/path
  bindings;
- semantic reviewers see the specification and assigned ontology labels;
- blind delta audit and exact canonical executable matrices remain required;
- reference primary/cross must pass, known-bad primary must fail, and known-bad
  cross must pass;
- every candidate passes exact, normalized, and fuzzy global separation; and
- no evaluator prompt, reference, output, task ID, or private archetype is
  exposed to construction.

Every admitted row binds source identity, prompt and response hashes, candidate
hash, teacher evidence, independent tests, semantic verdict, delta verdict,
runtime/image identity, staged files, verifier outcomes, correction count, and
separation evidence. At most one candidate correction is allowed.

## Broad replay

After capability construction reaches 720 admitted rows, deterministically
select 180 rows from the sealed prior training corpus: fifteen per
lane/task-type pair. Replay rows must have complete rights and lineage, remain
source-disjoint from all 720 capability rows, pass current integrity checks,
and be resealed under the new package. Replay selection may not inspect an
evaluation surface.

## Final corpus gates

The 900-row corpus must have:

- exactly six capability rows per cell;
- exactly fifteen replay rows per lane/task-type pair;
- 900 unique record IDs and 900 unique source identities;
- no normalized scaffold cluster above 2%;
- two blind manual reviews per primary capability;
- complete exact/normalized/fuzzy separation and lineage evidence;
- zero evaluation records or evaluation-derived construction inputs; and
- a byte-stable canonical training JSONL plus sealed balance and quality
  manifests.

## Hard stops

Stop on upstream hash drift, historical draft-accounting mismatch, insufficient
unused sources, source reuse, an unsealed candidate outcome, evaluation
exposure, more than 165 replacement needs, any cell below six admissions, or a
failed final corpus gate. Training, untouched evaluation, promotion, merge,
quantization, publication, and every GCloud action remain downstream.
