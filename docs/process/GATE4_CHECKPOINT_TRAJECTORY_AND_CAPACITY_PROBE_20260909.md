# Gate 4 checkpoint trajectory and capacity probe — 2026-09-09

## Executed evidence

The frozen 30-task development canary has valid results for the exact base,
four intermediate Gate 4 checkpoints, and the final adapter. The fifth
intermediate checkpoint produced no task or run evidence and is excluded. It
is a controller/runtime timeout, not a model failure.

| Seen tokens | Passes | Go | Java | JavaScript | TypeScript | Python | Rust |
|---:|---:|---:|---:|---:|---:|---:|---:|
| Base | 5 | 0 | 1 | 1 | 2 | 1 | 0 |
| 406,491 | 6 | 0 | 1 | 2 | 2 | 1 | 0 |
| 814,098 | 4 | 0 | 1 | 1 | 1 | 1 | 0 |
| 1,224,637 | 5 | 0 | 1 | 1 | 1 | 1 | 1 |
| 1,629,235 | 5 | 0 | 1 | 1 | 1 | 1 | 1 |
| 2,438,853 | 6 | 0 | 1 | 1 | 2 | 1 | 1 |

Across those six measured points, 23 tasks fail everywhere, four pass
everywhere, and only three ever change pass status. Only seven of the 30 tasks
pass at any point. The earliest checkpoint improves only the combined
JavaScript/TypeScript family; the later and final checkpoints shift the lone
gain to Rust. No measured point approaches the frozen four-of-five-family
promotion threshold.

The sealed machine-readable report is
`measurement/gate4/checkpoint-sweep-20260909/trajectory-analysis.json`, report
seal
`ccafed3584dee7adb835e11bd6e47c180e53e9b87480f698dcfb769419898e4b`.
The missing 2,036,559-token checkpoint is explicitly excluded and no score is
reconstructed.

## Decision

Earlier stopping is rejected as a repair. The evidence is consistent with an
adapter update that is too weak or too narrowly targeted to create broad
executable transfer. It does not prove that capacity alone is causal, but it
makes another rank-8, final-eight-layer, attention-only run unjustified.

One capacity probe is locally specified in
`configs/train/expansion_capacity_probe_v2.json`, file SHA-256
`3e201e80560052a503ab4b56b71684a4c50430750bb6de9cc8419dbd30bb5aa5`.
Its local preflight card seal is
`15ec9533a547c0cc45a1fa0dcfb5267440d4118e2c8f4c0a255f502c391afafd`.
The card is `prepared-not-executable`: it contains no provider price or cloud
approval binding.

The 46-file training workspace is sealed locally. Its 5,575,271-byte archive
has SHA-256
`0550d2f39bda880077b03b5f0cc57e2eff0e08db0ba130339abb17f715797945`;
the manifest seal is
`fbb4b4cf30e6664fe583c9a8ff5a2042b7ab282663174fd21f534b7e51350bcd`.
The 587-file development-only evaluation workspace is also sealed locally.
Its 1,012,468-byte archive SHA-256 is
`6bca993d7ba0a744724aef324b303e1caf95a7be7943ba18a874e02fe0758db3`;
manifest seal is
`752eb6a124dd2949226164fbe237e1f31c7a264c9fe5a0b69534c517c8f39b02`.

The intervention keeps the learning rate, data order, optimizer, batch size,
sequence length, seed, precision and loss controls fixed, but changes the
adapter from rank 8 to rank 16 and expands targeting to:

- the selected q/v or fused input/output attention projections in all 24
  language-model layers; and
- gate/up/down MLP projections only in layers 16–23.

The exact shape-derived LoRA parameter estimate is 7,520,256 versus 729,088 in
the prior recipe, a 10.3x increase. BF16 adapter weights plus estimated FP32
gradients and AdamW states add about 0.10 GiB. The prior run peaked at about
5.26 GB on a 24 GB L4, so memory capacity is not the expected constraint;
actual peak VRAM remains a hard measured gate.

## Bounded continuation screen

The probe stops after the existing prepared corpus's first 624 records and
468,601 input tokens. This is 19.2% of the previous run. The weighted objective
shares are Go 20.27%, Java 20.31%, JavaScript/TypeScript 18.32%, Python 21.95%,
and Rust 19.14%. The earlier 536-row shortcut was rejected because its
JavaScript/TypeScript objective share was only 16.3%.

After save/reload, the same frozen 30-task canary may authorize preparation of
a full-token continuation only if all of these pass:

- at least two of five product families improve over the exact base;
- net executable gain is at least two passes;
- no lane loses a pass;
- non-code and truncated outputs do not increase; and
- save/reload reproduces.

Passing this screen is not checkpoint promotion. It does not authorize the
180-task development run, decision-set opening, Gate 5, merge, quantization or
publication. Failure ends this mechanism without spending the remaining
80.8% of training tokens. Because rank and target scope change together, a
pass would establish the combined mechanism, not attribute causality to either
change separately.

No GCloud inspection, upload, resource creation or execution is authorized by
this document. Provider pricing, exact inputs, a cost ceiling, teardown, GCS
backup and explicit approval must be sealed separately.

Thirty-eight focused tests pass. The Python 3.12 full suite retains only the
three already documented stale Gate 1 workspace/readiness failures; the probe
introduces no new full-suite failure.
