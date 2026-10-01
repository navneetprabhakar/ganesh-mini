# Gate 2 V5 source-feasibility addendum — 2026-09-16

Status: sealed pre-execution amendment

Applies to: `capability-stratified-v5-interface-replay/v1`

Base plan SHA-256:
`132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b`

## Measured feasibility result

Before any V5 model call, the cohort constructor evaluated the sealed V4 source
ontology after excluding the 3,225-row seed corpus, every V2 and V3 assignment,
and all 120 V4 queue assignments. The eligible graph contained 2,371 fresh
accepted cell/source edges. Fifty-nine repair cells retained at least one fresh
reserve source. `graph_and_tree/java/repair` retained zero.

The failed constructor emitted no cohort, source, carry, or exclusion manifest.
This is a pre-execution source-feasibility result, not a candidate outcome.

## Amendment

Replace the base plan's requirement to prebind 60 reserve sources with exactly
59 reserve sources, one for every repair cell except
`graph_and_tree/java/repair`. That cell is explicitly first-pass-only.

The two fresh TypeScript primary sources remain mandatory and distinct from all
59 reserves. The frozen 60-primary cohort, 58 immutable carries, full downstream
rerun, first-pass thresholds, visibility boundaries, and all other V5 rules are
unchanged.

If `graph_and_tree/java/repair` is rejected or unresolved in the V5 first pass,
V5 fails immediately even when the aggregate first-pass thresholds otherwise
pass. No source extension, reserve generation, candidate correction, or
post-outcome source search is permitted for that cell.

If every first-pass threshold passes and the rejected cells are all among the
59 prebound reserve cells, generate exactly one reserve for each rejected cell,
up to six. A reserve remains forbidden for any non-rejected cell.

Revised absolute budgets are:

- ordered first pass: 60 candidates, comprising 58 immutable carries and 2 new
  teacher generations;
- prebound conditional reserve sources: 59;
- generated reserves: 0–6;
- absolute terminal candidate budget: 65; and
- absolute new V5 teacher-generation budget: 7.

## Rationale and hard stop

This amendment avoids an adaptive source-classification campaign undertaken
solely to manufacture one optional reserve after the complete fresh-source
inventory was measured. It makes the limitation stricter, not looser: the
unreserved Java cell must pass its frozen primary or the qualification ends.

Stop before any V5 model call if the constructor does not bind exactly 59
unique reserve identities, either fresh TypeScript primary lacks a distinct
eligible source, any selected identity is excluded or reused, or any cell other
than `graph_and_tree/java/repair` lacks its reserve binding. This addendum
authorizes no GCloud action, training, evaluation opening, publication, or
release claim.
