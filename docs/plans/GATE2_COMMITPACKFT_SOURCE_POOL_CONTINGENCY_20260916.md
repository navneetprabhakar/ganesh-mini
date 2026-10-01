# Gate 2 CommitPackFT source-pool contingency — 2026-09-16

Status: frozen preparatory addendum; inactive unless the v8 source-affinity
evidence proves that the existing approved source pool cannot satisfy the
Gate 2 v3 global 120-source match.

Parent contract: `capability-stratified-v3-repair-delta/v1`

Parent plan SHA-256:
`4023a896300112f9f93f2a16698d549f203e3e75b4e71ae054f3a98463e2f0f0`

## Decision

Conditionally approve `bigcode/commitpackft` as a third training-only repair
stimulus dataset for the native JavaScript and TypeScript lanes. This is a
source-pool extension before queue sealing, not a candidate retry, a relaxed
quality gate, or permission to train. It may be activated only after the
current v8 campaign reaches terminal evidence and the unchanged global matcher
cannot construct the 60 primary plus 60 cell-bound reserve assignments.

The parent plan already requires at least two approved datasets and limits any
one dataset to at most 50% of either 60-source cohort. It does not require
exactly two datasets. The implementation may therefore generalize the current
30/30 implementation detail to the plan-native rule: at least two represented
datasets per cohort and no more than 30 assignments from any dataset in either
cohort. The 60-candidate first pass, 66-candidate absolute generation budget,
all source-affinity requirements, and every downstream gate remain unchanged.

## Pinned source

- dataset: `bigcode/commitpackft`
- URI: `https://huggingface.co/datasets/bigcode/commitpackft`
- revision: `fc56fe33c030c6daa414c2b112c932b8eed085e6`
- JavaScript file: `data/javascript/data.jsonl`
  - bytes: `128001108`
  - SHA-256: `968688a1163c2dbbced0d0f9cf1dd52bc0b626c2ad9b02ff23f5700b2e277f25`
- TypeScript file: `data/typescript/data.jsonl`
  - bytes: `14620423`
  - SHA-256: `43d32596844c62aa23b0e5a8811648f6f20fa07d9ab80499d66507136b844a76`

Only records whose per-record license is exactly one of MIT, Apache-2.0,
BSD-2-Clause, BSD-3-Clause, ISC, CC0-1.0, or Unlicense are eligible. Missing,
unknown, copyleft, or unrecognized license values fail closed. The dataset
field is evidence supplied by CommitPackFT, not independently verified
file-level legal advice. Preserve it exactly in the lineage and do not publish
raw source stimuli without a separate release-rights review.

## Deterministic source construction

Construct exactly the first 1,000 eligible JavaScript and first 1,000 eligible
TypeScript roots when each lane has at least that many eligible records.
Eligibility
is decided before ordering: required lineage fields must be present,
`old_contents` must be non-empty, the record license must be allowlisted, the
record must not contain a prohibited benchmark marker, and its lineage must be
absent from the prior corpus, v2 artifacts, the current source queue, and cited
repair evidence.

Order eligible records only by:

`SHA256(seed || NUL || dataset || NUL || revision || NUL || source file || NUL || physical record ID)`

No capability keyword, evaluation result, classifier result, `new_contents`,
or later candidate outcome may influence this ordering. The complete source
record and raw physical JSONL line are hashed for provenance. The manifest
also binds the count and ordered-identity hash of the complete eligible
inventory before the fixed 1,000-record slice; later capability outcomes may
not expand, shrink, or reorder that slice.

The visible stimulus contains bounded `subject`, bounded `message`, and bounded
`old_contents` only. `new_contents` is quarantined: it is never serialized into
the extension queue, stimulus, ordering key, source-affinity prompt, teacher
prompt, or public evidence. It may be read only while hashing the complete
pinned record and while applying the fail-closed prohibited-marker safety
filter. Native JavaScript remains JavaScript and native TypeScript remains
TypeScript; no cross-language projection is authorized by this addendum.

## Unchanged gates

Before classification, the extension queue must pass the existing content-free
exact, normalized, and fuzzy comparison against every frozen evaluation
surface. The classifier receives only the resulting content-free attestation.
Every accepted root must independently satisfy all five frozen affinity
booleans, including self-contained standard-library-only feasibility and the
absence of frameworks, services, filesystem, network, clock, randomness,
installation, or external dependencies. A package or framework import is not
silently removed to manufacture eligibility.

The complete extension, policy, input hashes, rejection counts, ordering
contract, lineage, separation attestation, classifier evidence, final queue,
and manifests must be sealed. Classifier execution is prohibited before the
activation condition is recorded as satisfied. After activation, the standing
local qualification scope authorizes source classification, but not teacher
generation, training, GCloud, publication, or any change to the frozen Gate 2
pass thresholds.

## Legal and provenance limitation

CommitPackFT rows may list multiple repositories or forks and do not provide a
locally verified file-level license or NOTICE bundle. Preserve the raw
repository field, its ordered parsed values, commit hash, old/new paths,
per-record license, physical record ID, complete-record hash, raw-line hash,
and pinned snapshot hash. Do not infer a canonical repository when the source
does not identify one. Apache NOTICE, attribution, personal-data, and public
redistribution review remains mandatory before any CommitPack-derived content
is released.
