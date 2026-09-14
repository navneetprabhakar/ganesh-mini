# Gate 2 capability-stratified corpus plan — 2026-09-14

Status: local contract sealed; qualification implementation next

Plan seal:
`0181751bdd912b8d04ccf954c358cb22681d6fc4aa5b3896a986e7a1ce73af01`.

## Purpose

Measure whether a new training-only construction contract can produce
substantive, executable coverage across capabilities, languages, and task
types. This is not a training or release authorization. It reads no evaluation
surface and forbids deriving training tasks from private development or
decision tasks.

## Matrix

The contract has ten primary capabilities:

1. associative aggregation;
2. binary and bitwise transformation;
3. callbacks and events;
4. graph and tree operations;
5. numeric reasoning;
6. ordering and selection;
7. parsing and encoding;
8. sequence algorithms;
9. stateful workflows; and
10. string and Unicode handling.

Every capability crosses six language lanes and both generation and repair,
creating 120 cells. Each cell receives exactly one scheduled cross-cutting
dimension from duplicate handling, immutability/aliasing, malformed input,
stable ordering, or state isolation. A task may add at most one more only when
intrinsically necessary. Generic edge-case boilerplate cannot count as its
primary capability.

## Qualification before scale

The first phase drafts 240 candidates: two distinct training-source stimuli
per cell. It must admit at least 120 records and at least one record in every
cell. Each empty cell gets at most one bounded replacement; any remaining gap
stops construction. This qualification is authorized under the standing
non-GCloud dataset scope and requires no new cloud permission.

If qualification passes, the intended pilot corpus is 720 new records—six per
cell—plus 180 broad replay records, fifteen per lane/task-type pair. New
construction is capped at 1,200 drafts. The intended 900-row corpus is still
not training authority; its integrity, balance, quality, separation, token
budget, and runtime plan must be sealed first.

## Isolation and admission

- Classifiers see training-source stimuli and the ontology only.
- The teacher sees a training stimulus, one primary capability, one scheduled
  cross-cutting dimension, and the language runtime contract.
- Independent test authors see only the candidate specification.
- Semantic reviewers see the specification and assigned ontology labels.
- No constructor or reviewer sees evaluation prompts, references, outputs,
  verifier records, or private archetype names.
- References must pass; every known-bad implementation must fail inside the
  pinned resource-limited, network-disabled verifier.
- Exact, normalized, and fuzzy separation must pass against all training and
  evaluation surfaces.
- Source lineage, teacher evidence, record IDs, prompt hashes, tests, and
  verifier evidence remain sealed.

The final corpus requires all 120 cells, unique source stimuli, no normalized
scaffold cluster over 2%, two blind manual reviews per primary capability, and
at most one correction pass per candidate.

## Hard stops

Stop if qualification admits fewer than 120 records, any cell remains empty,
evaluation data enters construction, semantic or executable admission fails,
the pilot needs more than 1,200 drafts, or global separation/lineage evidence
is incomplete. Do not compensate by weakening a cell, adding generic edge-
case prose, or repeatedly repairing rejected candidates.

No GCloud read, upload, mutation, or billing action is authorized. No model
training, evaluation, promotion, merge, quantization, or publication is
authorized by this plan.
