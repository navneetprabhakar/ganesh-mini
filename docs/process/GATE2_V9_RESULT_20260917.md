# Gate 2 V9 qualification result — 2026-09-17

Status: passed

Contract: `capability-stratified-v9-literal-key-guard/v1`

## Result

Gate 2 repair-corpus construction passed under V9. The final reconstructed
cohort contains exactly 60 admitted candidates, 0 rejected candidates, and 0
unresolved outcomes. The qualification report seal is
`cb0eafa84cbd76ff90c72456883c854d22356bb87da7a1ecf6a7bd4cf50ade0e`.

V9 retained the 58 exact V7 admissions, carried the exact accepted V8 Python
cross-cutting role, and generated one fresh Rust primary-discrimination role.
It ran one fresh blind delta audit for each of the two corrected candidates,
reran content-free global separation across the reconstructed 60-candidate
cohort, and executed the exact four-suite matrix for both corrected candidates.
Both passed:

| Candidate | Lane | Corrected role | Final result |
|---|---|---|---|
| `cap-v4-associative_aggregation-rust-repair-primary` | Rust | `primary_discrimination` | admitted |
| `cap-v4-binary_and_bitwise-python-repair-primary` | Python | `cross_cutting` | admitted |

The V2 generation-equivalence result remains passed for all 60 generation
cells. Together with the 60 admitted repair cells, final combined coverage is
120/120. Evaluation artifacts read outside the content-free boundary remain
zero.

This is a corpus-construction qualification result. It makes the repair corpus
eligible for the next training-entry assessment; it does not itself authorize
or execute training, open untouched evaluation, publish artifacts, or make a
release claim. No new training using this qualified corpus has run.

## Terminal V6–V9 sequence

The result preserves each prior version as terminal evidence rather than
rewriting it:

1. **V6 — readiness no-go.** The provider accepted the content-free schema and
   returned the two required role objects, but the local validator imposed an
   impossible serialized JSON member-order requirement. The candidate campaign
   never started: zero candidate test-author calls, delta calls, structural
   reauthors, executable decisions, or evaluation reads. Readiness-failure seal:
   `39a8264850aafb9c8b8db6ed9de4f8d6e0d46b4ad331329a4e2c21c6cce3f778`.
2. **V7 — 58/60 qualification no-go.** Order-insensitive exact-key handling
   passed readiness and the complete campaign admitted 58 candidates, rejected
   two authored-test roles, and left zero unresolved. Neither rejection
   demonstrated a bad reference. Qualification seal:
   `1bbdd82b8558542547f0476e8b753089a0c93e73221f4db4c6b6b9787dde3f06`.
3. **V8 — validator no-go.** Exactly two replacement role-author calls returned
   structured responses. The Python cross-cutting role passed its frozen
   checks, while an over-broad Rust metadata-access guard rejected a dynamic
   `metadata().get(&key)` use that did not assert either disputed literal key.
   V8 stopped before delta audit or candidate execution. Qualification-failure
   seal:
   `ff2de8bc59f6f0da95e53bb020470df3b2abbda5b1f76c83f03f6814f6648af5`.
4. **V9 — passed.** Readiness proved the corrected Rust guard rejects the V7
   literal-key assertion while accepting dynamic unrelated-key inspection and
   preserving the V8 Python verdict. The bounded final correction then reached
   60/60 admissions, zero unresolved, and 120/120 combined coverage.

These are construction-interface findings, not model-training failures.

## Canonical artifacts

- V9 plan:
  `docs/plans/GATE2_REPAIR_DELTA_V9_LITERAL_KEY_GUARD_PLAN_20260917.md`,
  SHA-256
  `b050cb106bbbef023f99780ce5b3d843fe0f3d247f82f67adf2375f49142e641`;
- V9 readiness:
  `measurement/gate2/capability-stratified-v9-literal-key-guard/final-v1/readiness-v9.json`,
  report seal
  `008e6a3479fd40066c648753d78d342989a72adf5359f9b54ad7cdf6f3998452`;
- V9 qualification:
  `measurement/gate2/capability-stratified-v9-literal-key-guard/final-v1/qualification-summary-v9.json`,
  report seal
  `cb0eafa84cbd76ff90c72456883c854d22356bb87da7a1ecf6a7bd4cf50ade0e`;
- complete-cohort separation report seal:
  `6939abd59610a771288f9232604f6d2c32c8ad74be1bc3398337ab22f8063647`;
- frozen separation-contract SHA-256:
  `4c480fbb7ea1177afb0f4a840efe81e6acdf62f2bd2a41d7da03032abe733a8e`;
- V2 generation qualification seal:
  `293ebd4d38e4200a9de6bd45ba1a9ba4d0f9c0707ce632ba0be8241f41195139`.

## Current boundary and next step

Gate 2 is complete. No training job or GCloud resource is active. The next
step is to freeze the exact 120-cell qualified corpus/training input lineage,
perform the explicit Gate 3/4 training-entry assessment, and start training
only under its controlling authorization and resource contract. Untouched
evaluation, publication, and release remain downstream gates.
