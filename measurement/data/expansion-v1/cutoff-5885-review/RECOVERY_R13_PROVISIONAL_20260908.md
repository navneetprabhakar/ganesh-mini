# Provisional R13 single Rust test correction — 2026-09-08

Gate 2. Exactly one original parent, exp-v1-rust-repair-0361, using emitted r11 candidate exp-v1-recovery-r11-rust-repair-0361 as the unchanged specification/reference/mutant source. Proposed derived ID: exp-v1-recovery-r13-rust-repair-0361. This is an oracle-rebuild request, not a reservation, generation, admission or candidate execution. Existing diagnostics are untouched. Original remains held; zero new original review credit.

Read correct_recovery_tests.py and r10 request/feedback examples. The request selects the original parent canonical hash; feedback is keyed by proposed derived ID and binds the previous r11 candidate canonical hash. R11 run-contract has no correction_attempt. Main must approve and validate before any launch; a failed correction is not permission for a second critic.

## Narrow correction

The arithmetic reference is statically sound and existing bulk-work oracles are valid. Add the tiny 1x1, step=u64::MAX sequence elapsed(MAX-1, MAX, 1) => (0,1,1), checking coordinates and optional subsequent zero elapsed. This distinguishes lost carry using at most one logical step per call rather than astronomical work.

Ordering is essential: a separate test or lexicographically early test name cannot stop Rust's other tests from running a huge loop after an assertion failure. The feedback therefore requires the bounded witness at the beginning of every test function/path containing an astronomical logical-step call, using an independent fresh grid or helper. The original bulk assertions then retain their original state/setup and full valid domain. No concurrency setting change or timeout oracle is requested. No implementation code is included in feedback; repair prompts themselves inherently expose the embedded faulty source under the approved provenance rule.

The correction must preserve the r11 problem, reference and supplied mutant byte-for-byte. Existing exact/partial/zero elapsed, validation order, opposing directions, independent axes, clamping and borrowed-input controls remain required. Do not invent public-coordinate corruption, physical allocation, numeric caps or a different arithmetic policy.

## Exact SHA256 bindings

- Original corpus: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
- Hold ledger: 9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee.
- Original parent canonical: 7f4a1f8b5996c876c97df3b662c4198b0e58ea0420b219abf391399d3a6aa015.
- Previous r11 candidate canonical: dcaa7a451cdd18cae01a70720e033f3fb00752cdbbe54ba27b6bd37e5ff9d0bd.
- Previous r11 candidate file bytes: 438935de5c604591aa9170dd436f57aa13e8c6015b44b277d5d5b6e67527e6e4.
- R11 review evidence: cee2cbda138862dae339b9d80aa483dd3fadadc1dee1f73005b2ea29fe19f507.
- Frozen problem: d34bfd43761720379a766fb3ee60f19bf3e4a3d2b147143d993024af3d1f28c0.
- Frozen reference: ed316859966eeb6b8bffebea10cd9607a14bb387ca3ae3177a5ea2046e274e40.
- Frozen embedded/supplied mutant: 3b87f6a3c1e515e6cf3e568016625dd897a0f497cdbca8ad311b08e7afaf6d78.
- Previous independent tests: 97f9ee7e173587ce87da2f259fcc9c1d1dacaf0cd12bba762a23d02151b15d52.

Candidate source is datasets/cache/expansion-v1/versioned-recovery/r11/exp-v1-recovery-r11-rust-repair-0361.candidate.json. Review evidence is measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_R11_RUST_REVIEW_20260908.md. Original authorized source/rights bindings are preserved by the normal planner/correction path; this proposal neither changes nor reopens them.

Only recovery-requests-r13-PROVISIONAL.json, recovery-test-feedback-r13-PROVISIONAL.json and this isolated note were written. No central state, candidate, plan reservation or diagnostic process changed.

