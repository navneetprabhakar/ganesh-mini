# Array-validation follow-up, batch 10

2026-09-06. Positions 136–150 inspected against prompt, reference and original
tests: 15 new / 159 unique outside-sample targeted inspections. Frozen 300
unchanged; this is not seven-criterion approval. Ten newly held records bring
the ledger to 126 additive / 129 including historical three.

All ten diagnostics reproduced assertion failures in pinned, network-disabled,
resource-limited sandboxes; no timeouts. TypeScript compiled before failing.

| ID suffix | Finding | Evidence result |
| --- | --- | --- |
| typescript-repair-0064 | Sparse chrome entries bypass string validation. | document-chrome-sparse-result.json |
| javascript-repair-0076 | Sparse cursor input bypasses element validation. | cursor-sparse-result.json |
| typescript-generation-0101 | Valid existing required book ID is lost during copying. | book-existing-hidden-id-result.json |
| typescript-repair-0068 | Validated required score is lost during review copying. | review-hidden-score-result.json |
| typescript-generation-0099 | Whitespace-only password accepted despite blank-password prohibition. | session-blank-password-result.json |
| typescript-repair-0066 | Valid required email is lost during member copying. | select-member-hidden-email-result.json |
| javascript-generation-0115 | Sparse samples bypass finite-number validation. | meter-sparse-result.json |
| javascript-generation-0119 | Sparse initial ingredients bypass string validation. | recipe-initial-sparse-result.json |
| javascript-generation-0120 | Sparse candidates bypass object validation. | candidates-sparse-result.json |
| javascript-repair-0077 | Sparse accounts bypass credential validation. | console-accounts-sparse-result.json |

Original tests omit these counterexamples. Required-field probes use valid
typed objects with a required own property marked non-enumerable, not missing
fields or arbitrary extra properties. The access-session prompt forbids blank
passwords; unlike username/token the reference checks only empty password.

Scoped negative findings: JS repair0073 validates workspace entries with for-of;
explicit shallow-copy semantics do not independently warrant a hidden-key hold.
JS repair0075 validates rule/step arrays before mapped copies. JS repair0079
maps only internal dense jobs; running-state transition and finally protect
callback reentry/error behavior. JS generation0126 explicitly checks dense own
indices even with zero limit, and its original tests include sparse rejection.
JS generation0118 uses dense own-key lists; whether non-enumerable parent nodes
belong to its mapping is a contract-clarity issue, not a new executed defect.
ReviewLedger constructor normalization and session duplicate-token authorization
semantics remain open API questions. Nontriviality remains unadjudicated.

The pre-existing recipe-sparse result concerns a different candidate. It was
preserved; this batch uses separately named recipe-initial-sparse evidence.
Continue at position 151. No candidate rewrite, revised partition, training
seal, generation restart or new VM. Systematic scope v3 remains 9 groups /
14 strata / 3,085 review records, not automatic rejections.
