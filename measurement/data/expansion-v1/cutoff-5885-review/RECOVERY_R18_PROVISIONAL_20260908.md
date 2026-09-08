# R18 provisional test-only correction — 2026-09-08

Gate 2. Draft only: **two requests, Python repair0138 and Rust repair0102**, from the completed R14 run. No plan reservation, generation, execution, admission or original-row coverage credit. R13 Rust0361 is excluded because its review is positive; main handles qualification.

Read correct_recovery_tests.py and reconciled the completed R13/R14 review. Both selections are oracle-rebuild for the correction pipeline, not fresh architecture requests. Exact original-parent hashes are in recovery-requests-r18-PROVISIONAL.json; exact previous R14 derived canonical hashes are in recovery-test-feedback-r18-PROVISIONAL.json. These are different hash roles. Main must read and approve these drafts before creating any plan; tentative r18 in the request does not reserve it.

Python removes only the unsupported ExplodingFloat pre-aggregation error-priority oracle and adds ordinary integer cancellation/rejected huge-value coverage. Existing exact huge integer/Fraction, native operation errors and ordinary late malformed rejected-event validation remain. No special custom-number behavior is invented.

Rust corrects VT classification to the explicitly named Rust char::is_ascii_whitespace predicate, retaining FF and the U+2003 preservation witness. Do not broaden the reference predicate. An FF-padding slug control covers the same explicit rule without new semantics.

All R14 specification/reference/mutant bytes must remain unchanged. The critic sees specification, prior tests and specification-derived feedback; the repair specification itself includes broken input, so this is not blindness to embedded source. No separately corrected reference is passed. Source/rights must remain bound to original parents through the existing planner/correction path. Normal fresh independent review, sandbox directionality, separation and admission gates remain required; no repeated correction loop is proposed.

Review evidence: measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R13_R14_REVIEW_20260908.md, SHA-256 f4e7d9a8b06f5690334b76a81275f03fbb67761a0c8bcf6202b12b4b553ee409.

## Exact previous bindings

Canonical uses sorted compact UTF-8 JSON; file/content hashes cover exact bytes.

### exp-v1-recovery-r14-python-repair-0138

- file: `datasets/cache/expansion-v1/versioned-recovery/r14/exp-v1-recovery-r14-python-repair-0138.candidate.json`
- file_sha: `df73ba067c0cd39243867b525c75cd84ca0510b802d767a706fa6bb7f2f61dda`
- canonical: `d510f25bd5b259f24dcb32ad719a010f970fc8af350827526df2407b5fc926a9`
- parent: `097e1648410b0391b52875d213ea6a982c8d3418fe08bfd48153bf2c6da17c72`
- prompt: `3e9530f8fdd09d0ac73827fa5fa1987318f9efc6674002ebfa0934b0c1c16200`
- reference: `a343644ad08e3f93bd8f4a1e0f3f6af06a69ce2e46eedb388e4d474fa520a197`
- mutant: `73863c0d4a7512b23d97468999075f0f08ec352f543d9d5d24f5790d94919779`
- test: `0613b34b8f02ae09bfda5c362d6c55b7ab6fbfe7a8166cddef722a1ab8cbcb3c`

### exp-v1-recovery-r14-rust-repair-0102

- file: `datasets/cache/expansion-v1/versioned-recovery/r14/exp-v1-recovery-r14-rust-repair-0102.candidate.json`
- file_sha: `d2e12a454017a0a5fcf3dc40254828c49270ac6e87a17e48376cc710980a86c6`
- canonical: `4d58a05badc57e8b8cc24efec7263633d26e7eed2c88814c063455cb783a93ef`
- parent: `8c2b016284660327c9d77e34b6ccf76585bcaf4e147c761ef4d9bfe7d4a923f0`
- prompt: `43d8a017a339391d2af9944a758a6b8aee68964c2c4b7a6f6bcbc3e4fa32fce4`
- reference: `29be4e94463fd7b8c1aa670cb7c750e6db3d93cd71aaaab0412d6ccd61bf54b2`
- mutant: `6b2ec40b5b9a4653c04112c1490efe0704952f24c0bede3e1b95de727ea94637`
- test: `9475e5f31c7434341a514db945ccfcf5405e8c3ba0e86f3d8ba8a4d6cd9f54ae`

