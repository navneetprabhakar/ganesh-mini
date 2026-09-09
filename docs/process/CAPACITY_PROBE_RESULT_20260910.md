# Gate 4 capacity-probe result — 2026-09-10

## Outcome

The execution authorized by proposal
`461e968ae2fa79d3401e522d52bf91cbcc359cdded68d8fff62dff51631934f0`
completed as attempt `20260909T173721Z`. The 624-row, 468,601-token rank-16
capacity probe trained successfully, sealed all six checkpoints, and passed all
eight terminal checks, including save/reload, adapter identity, VRAM bound, and
cost bound. Training took 949.957 seconds; the bounded campaign completed in
1,123.698 seconds. The terminal training report seal is
`8a7c424d8abb96e5a951f5b16abf4641ba1e494a311dd444c0e786bc97f8802a`.

The frozen 30-task continuation screen completed 30/30 with 6 candidate passes
versus 5 base passes. The candidate improved three product families, but its
net gain was only +1 rather than the required +2, and TypeScript regressed from
2 passes to 0. Non-code and truncation counts did not increase. The frozen
decision is therefore `do-not-promote`; adjudication seal is
`d907065abf4ffee4237bef92a040b27b5bf83916bb287588ac3695a40869094b`.

| Lane | Base | Candidate | Delta |
| --- | ---: | ---: | ---: |
| Go | 0 | 1 | +1 |
| Java | 1 | 2 | +1 |
| JavaScript | 1 | 1 | 0 |
| Python | 1 | 1 | 0 |
| Rust | 0 | 1 | +1 |
| TypeScript | 2 | 0 | -2 |
| Total | 5 | 6 | +1 |

This is a valid mechanism result, not an infrastructure failure. The result
terminates the exact capacity-probe-v2 mechanism. It grants no authority for
the 180-task development surface, decision-set opening, main training, merge,
quantization, publication, or release.

## Evidence and cost

The terminal GCS tree contains 129 manifest-bound files. An independent local
recovery verified every SHA-256 entry with zero mismatches. The terminal
manifest SHA-256 is
`124703d11260839d0a458c5d59b3255ca4c22583782c79ed80343bc3fd47fd12`.
The provider/control evidence archive SHA-256 is
`73f9a34f847e4c53152aabf7ceca1be638fcb713718cc22f5db25d80f0811b09`;
it was uploaded create-only at generation `1788981472815348` and downloaded by
that exact generation for byte comparison. The final teardown receipt is GCS
generation `1788981697224407`, with receipt seal
`a41d86031b325ccb4f98a8ac14a3990afe7d01cc60c933223128744c4df18b5f`.

Projected compute cost is `$0.2664489284483141747466666667`, below the
`$2.25` absolute incremental ceiling.

## Teardown and billing boundary

Only the named capacity-probe VM, auto-delete disk, subnet, and network were
deleted. Two provider absence checks, 94 seconds apart, found all four absent.
Project-wide inventory has zero instances, addresses, forwarding rules,
routers, reservations, snapshots, and machine images. The unrelated unattached
200 GiB disk `laxmi-wmv2-training-01` remains in `us-central1-a`, may continue
to bill, and was explicitly outside this approval. It is accurate to claim no
active Ganesh capacity-probe compute billing; it is not accurate to claim that
the entire project is GCS-only.

## Next decision

Do not scale this recipe or try to rescue it with a longer run: the earlier
checkpoint sweep already rejected premature stopping, while this probe shows
that roughly 10x adapter capacity still trades TypeScript competence for gains
elsewhere. The next local step is a task-level error and training-mixture audit,
focused on the two lost TypeScript passes and whether the three gained passes
represent a coherent learnable mechanism. Any new cloud experiment requires a
new sealed hypothesis, bounded recipe, price envelope, and explicit approval.
