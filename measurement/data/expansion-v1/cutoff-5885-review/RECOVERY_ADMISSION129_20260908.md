# Recovery admission 129 — 2026-09-08

Gate 2 remains open. Two serial candidate-mode admissions accepted 20 records
with zero rejected, raising cumulative recoveries from 109 to 129. No final
corpus, balance, training or release seal is claimed.

## Admission r21-r22-three-v1

- Accepted 3: R21 JavaScript generation0090; R22 Go generation0218 and repair0180.
- Lane counts: Go2, JavaScript1. Type counts: generation2, repair1.
- Evaluation files inspected: 546. Serial record and verifier workers: 1.
- Output: `measurement/data/expansion-v1/recovery-admission/r21-r22-three-v1/admitted.jsonl`.
- Output bytes: 26288; SHA256 `6851e7385c212c0aa496ad9da7083537ef70108e307e67f7ac8629c9086ad71a`.
- Report SHA256 field: `0afc74ccf10936d39a1248fa14b31f567d71f306ef573469fb06a981f4593f25`.
- Report file SHA256: `a25b9a57a7c7b59ef0d7d18a209975f73a2ee8d64e84cb13584ac55b8cb927de`.

R22 Go0095 passed separate pinned race directionality but remains excluded for
test-oracle and atomicity holds. Other R22 Go rows remain held as recorded in
the full review. All R22 Java repair artifacts remain excluded because their
generated prompts exceeded the approved source-only edit scope; this was not
silently waived.

## Admission r23-seventeen-v1

- Accepted 17: Python4, TypeScript4, JavaScript3 and Rust6.
- All 17 passed fresh serial pinned reference/known-bad/original-parent
  directionality and main-integrated terminal static review.
- This was the sole bounded test correction; no second critic was used.
- Evaluation files inspected: 546. Serial record and verifier workers: 1.
- Output: `measurement/data/expansion-v1/recovery-admission/r23-seventeen-v1/admitted.jsonl`.
- Output SHA256: `d1cf2e55453d965099004172bd599f8df7885a88f160dd278d90b497593f9d04`.
- Report file SHA256: `d45a70cb1d48ef4799eebf422f81d73dae42c83cbf2becb899d09e862c0178bd`.

## Cumulative state

129 recoveries: Go23, Java19, JavaScript22, TypeScript22, Python21, Rust22;
generation118 and repair11. With at most 3073 retained originals, the maximum
combined corpus is 3202 and the minimum gap to the 4000-record diagnostic floor
is 798 before further exclusions and token-family balancing.

All original holds remain immutable. This admission does not promote training.
R21/R22/R23 raw generation, review, diagnostics and admission evidence must be
included in the next verified GCS backup before cleanup.
