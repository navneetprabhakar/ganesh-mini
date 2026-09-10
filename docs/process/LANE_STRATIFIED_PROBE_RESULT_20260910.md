# Gate 4 lane-stratified probe result — 2026-09-10

## Decision

`do-not-promote`. The bounded probe completed successfully but failed the
frozen continuation rule. This is a valid model-quality result, not a training
or infrastructure failure.

## Execution

- Proposal: `8184f4694efdfab2da3b895393caec4c753d6b782f8c810067824f5d957926fa`
- Attempt: `20260910T043000Z`
- Compute: Standard `g2-standard-8`, one NVIDIA L4, 200 GiB balanced disk
- Training: 640 unique rows, 466,614 tokens, 64/64 optimizer steps
- Training wall time: 811.168 seconds
- Campaign wall time: 1,152.715 seconds
- Projected compute cost: `$0.2733293085082184083644444444`
- Startup/controller exit codes: 0/0

All six verifier images matched their frozen OCI identities. Training produced
six resumable checkpoints and a final rank-16 adapter. Save/unload/reload
passed with maximum absolute logit difference `0.0`. No loss-anomaly trigger
fired. Peak VRAM was 5,070,913,536 bytes.

## Retention guard

The 60 held-out authorized-corpus rows were disjoint from training. All six
lanes improved, so both the per-lane maximum 5% loss-increase rule and the
no-macro-increase rule passed.

| Lane | Base record mean | Candidate record mean | Relative change |
|---|---:|---:|---:|
| Go | 0.193280 | 0.173094 | -10.44% |
| Java | 0.290206 | 0.247834 | -14.60% |
| JavaScript | 0.233192 | 0.206011 | -11.66% |
| TypeScript | 0.178510 | 0.152182 | -14.75% |
| Python | 0.336762 | 0.290376 | -13.77% |
| Rust | 0.196305 | 0.168711 | -14.06% |
| Five-family macro | 0.244481 | 0.211822 | -13.36% |

## Frozen continuation screen

| Lane/family | Upstream passes | Candidate passes | Delta |
|---|---:|---:|---:|
| Go | 0 | 0 | 0 |
| Java | 1 | 2 | +1 |
| JavaScript | 1 | 1 | 0 |
| TypeScript | 2 | 1 | -1 |
| Python | 1 | 1 | 0 |
| Rust | 0 | 1 | +1 |
| Total | 5 | 6 | +1 |

Two product families improved and non-code/truncation counts did not increase.
The candidate nevertheless failed two frozen checks: minimum net pass gain was
`+2` but observed gain was `+1`; maximum lane regression was zero but
TypeScript regressed by one. Full development was therefore not opened.

## Preservation and teardown

The terminal prefix contains 130 objects: 129 manifest entries plus the
manifest. Every entry independently passed SHA-256 verification after local
recovery. Important identities:

- terminal manifest: `b437b8aece9ae8afef8bc0703efd02e9ef6d3802bc426bc3815af1d61f231551`
- training evidence: `1393f0fab569e46d71d64273afeac69a91841f9f3c26f39d6248644b73dc4087`
- canary adjudication: `3dfd584c608243f4a6867f5c28dacfb75e855eb01a488c0ac0b2a642012cbd5f`
- campaign result: `2f87bda315f8aade6da866c998f3ea6b927022bb46cffeebacae4a39f990b429`
- final adapter file: `8bf926578f0e6efe31152fba3f74756b4e93203cf69c57182a9accd5628d60c8`

The compact control archive and recovery receipt were uploaded create-only and
roundtrip-verified at generations `1789016588012192` and
`1789016586942988`. The teardown receipt seal is
`ccb72c357494d6b5fa6d897dd7f3c9b256444667a20644330f2530d478125df2`,
generation `1789016873044612`.

The exact VM, auto-delete disk, subnet, and network were deleted. Two checks
43 seconds apart found all four absent. No project instances, addresses,
forwarding rules, routers, reservations, snapshots, machine images, or custom
images remain. The unrelated 200 GiB disk `laxmi-wmv2-training-01` remains and
may bill; it was not touched. Thus this Ganesh attempt is GCS-only, while the
whole project is not.

## Next step

Do not scale this recipe. First compare all 30 candidate task transitions with
upstream and the rejected v2 probe, especially the TypeScript loss and the
absence of a Go gain despite balanced objective mass. Use that local audit to
decide whether a narrowly targeted data/optimization correction is justified
or whether the mechanism class should be retired.
