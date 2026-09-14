# Training-corpus diversity audit — 2026-09-14

## Scope

This audit reads only the authorized 3,225-row training corpus and the 640-row
v3 probe selection. It reads zero evaluation tasks, prompts, references,
outputs, or verifier records. Its observable tags are deterministic lexical
descriptors, not claims that a task deeply exercises the named capability.

Report seal:
`714fe87491fb798c6248f53e40dd80c9d305125f39dd631db8d7c47114b8f793`.

## Findings

The 640-row probe is not suffering from an obvious selection-specific topic
dropout. It is 19.84% of the full corpus. Across thirteen observable contract
tags, representation ranges from 17.69% to 23.87%. Examples include parsing or
encoding at 20.11%, callbacks or events at 20.18%, deduplication or grouping at
20.56%, and sequence transformation at 19.67%. The selected set has all six
lanes, both task types, 594 unique source records, and no duplicate normalized
prompt scaffolds under this audit.

The full corpus has 2,812 unique source records for 3,225 admitted rows and no
duplicate normalized prompt scaffolds. It is nevertheless highly concentrated
in observable contract wording: string or Unicode appears in 2,322 rows,
errors or malformed-input handling in 2,286, ordering or sorting in 2,116, and
aliasing or mutation in 2,075. Concurrency or atomicity appears in 112 rows,
callbacks or events in 218, graph or tree operations in 243, and parsing or
encoding in 358.

Those frequencies cannot be interpreted as semantic coverage because the
teacher contract itself repeatedly asks for empty, malformed, boundary,
ordering, aliasing, and mutation behavior. The audit therefore rejects both
of these unsupported conclusions:

1. that the 640-row hash selection accidentally discarded the full corpus's
   useful capability mix; and
2. that 3,225 unique-looking prompts prove sufficient capability diversity.

The full 3,225-row run already failed broad executable transfer, and three
subsequent changes to capacity, exact lane scheduling, checkpoint choice, and
gradient-conflict control did not repair it. The remaining evidence points
back to the supervision distribution and task construction, not another
optimizer-only adjustment.

## Decision consequence

The 2026-09-09 Gate 2 corpus-sufficiency decision was explicitly valid for one
bounded pilot. That allowance is exhausted. Reopen Gate 2 before another Gate
4 training proposal and build a new capability-stratified corpus contract from
training-only sources. Do not use private development archetypes or prompts as
training templates. Do not generate more rows through the unchanged teacher
contract, and do not use this lexical audit alone to select records.

The next local artifact must define a training-only capability ontology,
minimum cross-lane coverage, source-stimulus diversity, semantic review, and
executable admission. Only after that contract is frozen should construction
cost and a new bounded pilot be proposed.
