# R3 admission decision — 2026-09-08

Main fully read and integrated all three r3 quality reports, including final JS-B.
Their candidate hash bindings agree with selected actual artifacts. All42 serial
diagnostics are preserved; see RECOVERY_R3_INTEGRATION_20260908.md. That immutable
earlier integration's pending JS-B wording is superseded by this final decision.

JS0025 and0394 pass static all-criteria review and fresh reference/mutant/original
directionality. Preparation compared3073 retained originals and the nine previous
hash-bound admissions: no overlap. Fresh candidate admission checked546 evaluation
files and reran the references/supplied mutants serially in pinned network-disabled
resource-limited sandboxes. Accepted2/rejected0; candidate status passed.

Output: measurement/data/expansion-v1/recovery-admission/r3-two-v1/admitted.jsonl
bytes15939, SHA b178a066e1c565f5bf85e1dde44a751b4ed85e86814016af777438e41d472fec.
Admission logical seal24b9a1a3e6830674eb24b299fa1872264cfd5947065d7ee809d18f2867ba75d9.
Balance_passed=false: this is not a final corpus or training seal.

Total new recoveries admitted11: Go2,Java2,JavaScript4,TypeScript2,Python1,Rust0.
All are generation. Original holds2812 unchanged; maximum3073 originals plus11
recoveries=3084, minimum additional admissions916 before further exclusions and
family-token balance. No original-row coverage increase or original hold lifting.

R5 is one test-only correction for11 held r3 artifacts; JS0296 is excluded because
its required hidden-id data-loss reference defect also needs correction. r4 is
19 new Go/Java generations. These active runs are not yet reviewed/admitted.
