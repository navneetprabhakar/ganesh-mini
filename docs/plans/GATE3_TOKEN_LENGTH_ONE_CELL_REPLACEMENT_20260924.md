# Gate 3 one-cell token-length replacement proposal — 2026-09-24

Status: proposed; not authorized for execution under the frozen final-corpus
hard stop.

## Trigger and immutable evidence

The 900-row package separation passed under seal
`e1df396fd714c9b984649630d03da22efc816245841e80dbdb2e637dc0c805d8`.
The package tokenizer then failed exactly one row,
`cap-scale-binary_and_bitwise-typescript-repair-first_pass-01`: 3,032 tokens
against the 2,944-token maximum. The failed report is sealed at
`4e44bd293e5a7d5404ed44600c7534cf0fcf12bb46da60d835281e8449456927`.
Do not edit, truncate, relabel, or count this row toward final training entry.
Preserve the old 720 admission and failed 900 tokenization as historical
construction evidence, not a final training package.

## Prospective exception requested

Permit one post-executable token-length replacement in the single
`binary_and_bitwise/typescript/repair` cell. Use only its already prebound and
unused `cap-scale-binary_and_bitwise-typescript-repair-reserve-06` source:
`Multilingual-Multimodal-NLP/McEval-Instruct` revision
`57bd46727e49ac3e2890218a146d35c2454a8496`, record `row-33299`,
source hash `ccb28e294fc38b7e156cf48c4cb97f9a7402e48c0ac05064f046c92d74862ac5`.
This source occurs only in the frozen source queue among current Gate 3
artifacts. It is the first of two prebound same-cell reserve slots. The second
slot is not activated by this proposal.

This exception changes only reserve eligibility for a terminal final-package
length failure. It does not change the 1,200 global teacher-draft cap, the
2,944-token maximum, six-per-cell/900-row targets, evaluation separation,
independent test-author contract, or release gates. Counted teacher usage is
1,059 before this proposal; at most one new teacher draft is permitted here,
bringing usage to at most 1,060. No GCloud action is authorized.

## Execution and stop conditions

1. Bind the exact existing reserve source and original failed row in a new
   immutable activation manifest; never mutate the original queue or reports.
2. Generate at most one teacher draft for that source. Run the pinned tokenizer
   on its full untruncated training messages before admitting it. If above
   2,944 tokens, stop and preserve the failure; do not silently activate
   `reserve-07` or shorten the answer.
3. If within length, run blind semantic review, independent V9 test-author,
   fresh blind delta, and the exact resource-limited, network-disabled
   executable matrix. Respect the existing one-correction limit. A failure
   stops this proposal; any additional candidate needs a separate decision.
4. Rebuild a new 546/720 cohort by replacing only the overlength row. Verify
   six per cell and global record/source uniqueness. Re-run complete content-
   free exact, normalized, and fuzzy separation against training and frozen
   private evaluation, including all 900 package rows. Repeat two blind
   content-level reviews for the affected primary capability using the new
   row; label AI reviewers as AI, never as humans.
5. Reselect or rebind 180 broad replay rows deterministically against the new
   sealed 720 cohort. Tokenize all 900 without truncation, recompute frozen
   20/20/10/10/20/20 lane objective weights, and run the final package
   validator. Only its passing seal may unlock the bounded Gate 3 pilot.

If any upstream hash drifts, a source is reused, an evaluation surface leaks
into construction, the teacher count exceeds 1,200, or a final package gate
fails, stop and preserve evidence. No training, publication, or GCloud usage
follows automatically from approval of this local data-repair proposal.
