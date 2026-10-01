# Gate 3 L4 usable-memory retry — prospective clarification

Status: Navneet authorized another retry by saying “ok try again”; the hardware
floor clarification below is not yet explicitly accepted. No new VM started.

## Why unchanged retry is not useful

The last attempt passed the canonical 13-file upstream model materialization,
then exited before model load at the combined BF16 / 24,000,000,000-byte CUDA
guard. Neither guard operand was recorded. Historical L4 observations report
23,659,151,360 CUDA-visible bytes, below that literal floor, with BF16 supported.
Do not report those historical bytes as a current-device measurement.

The current nominal 24-GB L4 provisioning choice and literal CUDA-byte guard
are not mutually consistent with those observations. The current capability
training runner uses the same literal guard and also needs consistent handling.
Repeating the old workspace unchanged is not a remediation.

## Proposed interpretation requiring Navneet's direction

For the same NVIDIA L4 24-GB hardware class, use an explicit minimum of
22 GiB (23,622,320,128 bytes) CUDA-visible VRAM, with exactly one CUDA device
and actual BF16 support. This matches the historical qualification checker
floor; it is a prospective contract clarification, not a claim that the
current 900-row training capacity has passed. Other GPU classes retain the
literal 24,000,000,000-byte floor. No smaller GPU, quantization fallback,
sequence reduction, truncation, teacher generation or quality-gate waiver.

Before any model load, write and seal GPU name, CUDA-visible bytes, BF16 result,
device count, selected hardware-floor rule and required bytes, including on
failure. Apply the same rule to the qualification and actual-host SFT checks.
Retain strict upstream inventory checks, canonical materialization, pinned CUDA
image, BF16 attention-only rank-8 LoRA, 2,944-token envelope, objective weights,
and frozen peak-VRAM ceiling. Probe only 16 longest unique rows / two optimizer
steps, with no retained adapter or evaluation access. Qualify measured capacity;
never treat the historical mechanism result as current model-quality evidence.

## Evidence availability limitation

The locally retained admitted Gate 0B summary `20260824T180957Z/run-result.json`
records a passed L4 fused-loss mechanism and binds raw qualification SHA
`ac9d809739def7fb67838c77221681b1db5cb8a32f655e82ddfd95647ce94c1b`.
Its original generation-pinned GCS report cannot currently be downloaded.
Current-object lookup, historical-prefix listing and all-version lookup also
returned no match. Related archive-root checks did not locate a replacement.
This is a recovery gap, not proof that every possible copy is lost. Preserve
historical summaries and backup manifests; do not reconstruct missing raw
outputs or claim they were recovered. Resolve this evidence gap before release.

## Same-budget execution boundary after explicit floor acceptance

One further allocated start only; no automatic paid retry after failure.
Keep the SAME cumulative $5 ceiling, accounting for all three prior starts:

- $2.50 conservative prior-use reserve, not a billing invoice;
- $1.762043024 maximum next two-hour VM plus disk;
- $0.50 transfer reserve;
- $0.237956976 remaining backup/operations/cleanup headroom.

Before allocation, bind actual prior timestamps, finalization and independent
backup evidence for all three attempts, test the revised guard and negative
cases, and seal a new evaluation-free workspace rather than changing v3.
Use exact pinned inputs, provider two-hour STOP, bounded offline probe,
complete verified terminal backup before deletion, and double resource absence.
Zero-runtime capacity refusals may change bounded US zone only after verified
backup and cleanup. No full quality pilot, Gate 3 pass, release, or new $5
budget is authorized by this retry proposal.
