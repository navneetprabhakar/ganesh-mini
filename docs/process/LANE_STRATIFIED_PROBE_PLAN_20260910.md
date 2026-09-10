# Gate 4 lane-stratified probe plan — 2026-09-10

## Decision boundary

The rank-16 capacity probe is terminal `do-not-promote`. Its 624-row prefix
balanced five product families, while promotion independently protected six
language lanes. TypeScript received 7.1739% of realized objective mass and lost
both of its base passes. This does not prove underweighting caused the losses,
but it makes the v2 schedule an invalid mechanism for testing lane-safe
transfer. More v2 tokens or rank are not justified.

The next experiment changes the batching mechanism while retaining the v2
adapter capacity, learning rate, sequence length, and approximately the same
token exposure. It has continuation-screen authority only.

## Frozen intervention

- Source: the already sealed 3,225-row Gate 2 prepared corpus, SHA-256
  `0e7111f51c8ec6e7dcf23ee96ea4873b03ae944ce51aaab4aed6782493133224`.
- Training: 640 unique rows and 466,614 input tokens, versus 624 rows and
  468,601 input tokens in v2. Token exposure differs by 0.4240%.
- Optimizer grouping: micro-batch 1 and gradient accumulation 10. Every one of
  64 optimizer groups contains Go 2, Java 2, JavaScript 1, TypeScript 1,
  Python 2, and Rust 2 records.
- Objective mass: each optimizer group independently realizes Go 20%, Java
  20%, JavaScript 10%, TypeScript 10%, Python 20%, and Rust 20%. Per-record
  weights reconstruct each lane's supervised-token mean inside the group.
- Capacity: rank-16 LoRA across all language-model attention projections plus
  gate/up/down MLP projections in layers 16–23, identical to v2.
- Optimization: learning rate `1e-5`, bf16 base and compute, cosine schedule,
  and the existing optimizer-group anomaly guard.
- Retention: 60 unique authorized training-corpus rows, 10 per lane, selected
  by a separate seeded-hash stream and provably disjoint from training. This
  is a loss diagnostic, not an evaluation or promotion surface.

Dataset manifest seal:
`4258e58a4f1d6a46124e413512d7ba436d47eb780582410ecd96cd9a8d0b7404`.
Prepared training SHA-256:
`08f60dd76c1658a5ac91153b36b4e389cc5e69c2a915287009aaa1cb77881091`.
Retention SHA-256:
`c88d8a888ee0ccef4311f221df4edc573d8fedcdd89f991d6613a21994132bdf`.

## Frozen continuation checks

Training is terminal only if it reaches 466,614 tokens, stays within the VRAM,
wall, and cost bounds, preserves sealed identities, and passes adapter
save/reload. Before executable canary adjudication, the non-evaluation
retention guard requires:

- no lane's supervised-token-mean loss to increase by more than 5% from the
  same run's base-model diagnostic; and
- no increase in the five-family macro supervised-token-mean loss.

The unchanged 30-task executable canary then requires at least two improved
product families, net pass gain at least +2, zero pass regression in every
language lane, no increase in non-code outputs, no increase in truncations,
and save/reload success. Passing permits planning the next bounded step only.
It does not permit the 180-task development run, decision tasks, main
training, merge, quantization, publication, or a release claim.

## Local readiness and cloud boundary

The local execution card passes every preflight check and remains deliberately
`prepared-not-executable`. Card seal:
`2ff26cb52a1c630e324891717aae6e8d4ec61615a7d7cf681cbe6704ef0da82d`.

The deterministic training workspace contains 52 files and is sealed at
manifest `f3a6af93be4892fae8d7471fca2685c722bfb6b968b00f2eff6e672427537aa6`;
archive SHA-256 is
`5bfb4616b467690e298fc41c15657ff55cc48631a498860ecd395717af477e15`.
The development-only evaluation workspace contains 587 files/180 tasks and is
sealed at manifest
`e4804cffd18a6fb40027d3b7215b026ceb39bede4251adc26a6a9649c334a331`;
archive SHA-256 is
`9e74b86085033c2ab008242cf505c6837c5a9e9b6ac4260b2d93cea395c75346`.
Both archives were rebuilt byte-identically and independently verified against
every manifest entry.

No GCloud read, upload, mutation, resource creation, or billing action is
authorized by this local preparation. Source commit
`7711fa636cb4b08043518ec1bc97d76aadca889b` binds the four local workspace
objects. Their upload-only plan totals 7,399,962 bytes and is sealed at
`9c92677248903be640ad6b4905cbba268126659540ac70ac2ee082e9da97fc61`.
That plan completed with four create-only uploads and exact-generation
roundtrip verification. Receipt seal is
`f3e127d0db29b4623fef251e76852ac1c3428fbb67d74ab79eaa1d4b00cf8e4f`.
Provider inspection remains separately gated by plan
`32804a7e859b7567910f62bc4b403fa3781a6d26b826a033775c7174d9526be4`;
VM execution is not yet proposed or authorized.
