# Gate 4 gradient-conflict probe result — 2026-09-14

## Verdict

Attempt `20260914T003000Z` is a valid terminal diagnostic. The frozen
eight-group, zero-optimizer-step audit found no qualifying negative cross-lane
gradient conflict, so stage 2 was correctly blocked. No PCGrad training,
retention evaluation, or 30-task continuation screen ran.

This is not an infrastructure failure and it is not a failed trained model.
It rejects the specific hypothesis that the observed v3 task oscillation is
explained by pairwise negative LoRA-gradient directions at the declared
threshold and sampled optimizer groups. Conditional PCGrad is therefore not
eligible under the frozen plan.

## Executed measurement

- Eight optimizer groups were measured: `0, 9, 18, 27, 36, 45, 54, 63`.
- Each group measured all 15 pairwise cosines across Go, Java, JavaScript,
  TypeScript, Python, and Rust: 120 measurements total.
- Minimum observed cosine: `0.035201297582185986`.
- Maximum observed cosine: `0.4617275900415903`.
- Mean observed cosine: `0.16382851837594095`.
- Negative cosines: `0`.
- Cosines below the frozen `-0.05` threshold: `0`.
- Groups with a qualifying negative pair: `0/8`; required: `4/8`.
- Groups with JavaScript or TypeScript negative participation: `0/8`;
  required: `4/8`.
- Optimizer steps: `0`; seen training tokens: `0`.
- Campaign status: `completed-gradient-audit-no-conflict`.
- Projected compute cost: `$0.08009125052911889715777777778`.

The audit, run, phase ledger, and campaign canonical seals all verify:

- audit: `411885c12f8db68ce22986244c6d67822abcae16aa9f9c23d7a755a740eea69e`
- run: `af3ea3cf1545f3711f9ca4fdd5a9dca88941a34f820f7403c8245c0d6c9cbfad`
- phase ledger: `a32b193e407719fbff07cbcab2fcb50f00c02850ba36e1a59ca77f2b45db3bc7`
- campaign: `d31915796be69a2f9f0c6e20f0ea387b435d98a9507221f881ced3d842d7785f`

## Preservation and teardown

All 25 entries in the VM terminal manifest independently passed SHA-256
verification after exact-generation recovery. The recovered directory has 26
files and 30,231,021 bytes; terminal manifest SHA-256 is
`5fef6e6135a9a4adafcb89d0fa69e66aac956e9fe8e217e372e7cecdf57e0a5f`.

The compact control archive and recovery record were uploaded create-only and
round-tripped by exact generation:

- control archive generation `1789358988755320`, SHA-256
  `da1b5e8d82a402a66329f20a255c98ba0b209351c2ce4a409db9b35ac56e8b04`
- recovery record generation `1789358992992417`, SHA-256
  `b5531e42fd46258142ff149910e0cb3280996a3c10c7a2dce292b09d32090056`
- pre-teardown receipt generation `1789359051863633`
- teardown receipt generation `1789359329656748`, canonical receipt seal
  `d73e72e35542428ba5a96a6706e2e036cd26b6c79f789b26a135b54b889dafd9`
- post-teardown audit archive generation `1789359494557821`, SHA-256
  `84403c72248cd6a70612bb77ff3a0497e351ff4e16de43653e3877a2d70673ac`
- teardown-audit preservation record generation `1789359520965327`, SHA-256
  `ff171139a038782a6b64e63522b648e3d2304d94a4b47d89ddea1978cc2f872c`

The exact VM, boot disk, subnet, and network were deleted. Two absence checks
52 seconds apart found every exact resource absent and no Ganesh-named Compute
surface. The unrelated detached 200 GiB disk `laxmi-wmv2-training-01` remains
untouched and may bill; project-wide GCS-only billing is therefore false.

## Consequence

Do not train the conditional PCGrad recipe, weaken the conflict threshold, or
open the 30-task canary. Gate 4 remains blocked on producing a model with
defensible multilingual executable transfer. The next local work must return
to task/corpus diversity and the persistent `collapse-runs` failure cluster,
then freeze a genuinely different bounded mechanism before any new GCloud
proposal.
