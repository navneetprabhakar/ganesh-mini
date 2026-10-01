# Gate 3 canonical model materialization rescue

Status: prospective, not approved or executed on GCP.

## Finding and scope

Two allocated starts stopped before any model training. The first inherited
the preserved image's old entrypoint (exit 2); the second reached the intended
script but rejected noncanonical archive files (exit 1). Both terminal backups
passed independent immutable-generation recovery, exact teardown, and double
absence checks. Project VM, disk and reserved-address inventories are empty.

The cached model archive matches the exact pinned GCS source SHA-256
`846221797a5b57db5d7184680df4e74641a61504f687f86b81d85a471bb8c930`.
Full CPU verification proved all 13 canonical upstream files byte-correct.
The archive also contains 47 AppleDouble sidecars and 29 Hugging Face download
cache files. These are packaging metadata, not additional upstream model files.
Canonical-only materialization was executed locally and passed the unchanged
strict model checker again. No model loading, optimizer step or throughput
measurement occurred. Forty-five focused tests pass.

CPU archive verification seal:
`c06347a0a96667ea63a30ad49e7f1b0d83c614caf1db8eb44bb33e09a7d65db3`.
Actual canonical materialization seal:
`fe540d05ffa45b1392b87d83885dda21d9598a6dc6b7f2b19a126b088bd98402`.
Unchanged checker recheck seal:
`12ef547d30aac92d4303b30a2ae56295480a2dfaf2cd64905598702b1add1026`.
Prior runtime/cost-reserve evidence seal:
`d796e5160cedb4c8c40547b90b6047828544f7b7e1857c47c078b2557434d55e`.

## Proposed bounded exception

Authorize one further allocated qualification start, not chained paid retries,
as an explicit exception to the current one-rescue execution boundary. Zero-
runtime capacity refusals may be retried in the previously bounded US regions
only after their backup and cleanup verification. Do not duplicate a live job.

Keep the existing cumulative $5 ceiling; this is not another $5 budget:

- $2 conservative reserve for the two prior starts and preceding staging;
- $1.762043024 maximum for the next VM plus 200-GB disk for two hours;
- $0.50 inter-region input-transfer reserve;
- $0.737956976 remaining backup, operations, tax and cleanup headroom.

The two prior RUNNING intervals were 571.334 and 566.191 seconds, each under
15 minutes. The reserves above are conservative budget controls, not invoices.

Wire the tested `scripts/train/inspect_model_archive.py` into the startup as a
generation-pinned, SHA-verified input. Use its canonical materialization mode
to copy only the 13 byte-verified upstream files into an empty model directory.
Retain the original archive and excluded metadata hashes; never relax the
inventory checker. Keep the corrected explicit `--entrypoint python3`.

Keep the exact Qwen revision `15852e8c16360a2fea060d615a32b45270f8a8fc`,
preserved CUDA image, BF16 rank-8 attention LoRA, 2,944-token envelope, frozen
weights, 16 longest source-unique rows and two optimizer steps. No adapter is
retained, no evaluation is opened, and no teacher draft is generated.
The 900-row data package and 1,060/1,200 draft count stay unchanged.

One L4, network-disabled resource-limited container, two-hour provider STOP,
30-minute probe bound, complete terminal backup before deletion and double
resource absence remain mandatory. A failure stops this exception. No full
quality pilot, NF4 fallback, Gate 3 pass, Gate 8 decision or HF release is
authorized by this proposal. Report actual measurement only if it completes.
