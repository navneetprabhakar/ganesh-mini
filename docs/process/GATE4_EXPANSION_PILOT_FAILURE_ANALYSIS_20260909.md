# Gate 4 expansion-pilot failure analysis — 2026-09-09

## Result

The 3,225-row BF16 LoRA run is a valid completed training experiment and an
invalid release candidate. The frozen canary result is `do-not-promote`:

- exact base: 5/30;
- final adapter: 6/30;
- net gain: +1;
- improved product families: 1/5, below the required 4/5;
- per-lane regression: 0;
- non-code/truncation increase: 0;
- save/reload: passed.

The only pass-status improvement is Rust `collapse-runs`. Ten candidate source
files are byte-identical to the base output. The other twenty outputs changed,
but nineteen retained the same pass/fail result. Final diagnostic validation
loss improved from 0.370317 to 0.353869 on the five-family record macro, which
did not translate into broad executable correctness.

## Interpretation

The observed update is too weak or too poorly aligned with the frozen
development failures to justify scale-up. This result does not support a full
180-task candidate run, additional epochs, a Gate 5 correction continuation,
merge, quantization, or publication. Lower loss alone is not promotion
evidence.

The saved quarter-epoch checkpoints contain complete adapter snapshots at
406,491; 814,098; 1,224,637; 1,629,235; 2,036,559; and 2,438,853 seen tokens.
Before paying for another training run, evaluate the first five checkpoints on
the same 30-task development canary. The final checkpoint is already measured.
This is a diagnostic sweep, not permission to choose or publish a checkpoint.
It answers whether executable quality peaked earlier or whether the whole
trajectory is flat.

## Recommended bounded next experiment

Run one evaluation-only L4 job using the existing exact base model, verifier
images, evaluation workspace, and checkpoint artifacts. Evaluate five
unmeasured checkpoints serially, retain raw generations and verifier evidence,
compare every checkpoint against the same exact 30 base task records, back up
all evidence, and tear down.

Planning envelope, subject to a new sealed execution proposal and explicit
GCloud approval:

- one Standard `g2-standard-8` with one L4 in `us-east1-c`;
- no external IP, restart disabled, auto-delete disk;
- two-hour provider maximum;
- estimated active evaluation about 25–40 minutes plus restore and backup;
- using the already bound public rates, compute upper bound $1.707249 and
  200 GiB balanced-disk upper bound $0.054795;
- proposed absolute incremental ceiling: $2.25.

If no checkpoint improves at least four families, retire this attention-only
rank-8/1e-5 trajectory and change the training mechanism. The next plausible
mechanism test is broader LoRA capacity (all layers and selected MLP
projections) at a separately bounded token budget, not more examples forced
through the same weak update. If an earlier checkpoint does improve four
families, evaluate that one checkpoint on the complete 180-task development
surface before any further training decision.

## Separate evidence defects and billing boundary

One unselected tranche-2 base task file has an invalid outer evidence seal.
It does not affect the 30 selected canary tasks, but it must be repaired through
a versioned evidence action before full-baseline or release use. The original
file remains unchanged.

All Ganesh compute and network resources are absent. Project-wide GCS-only
billing cannot be certified because unrelated unattached 200 GiB balanced disk
`laxmi-wmv2-training-01` remains in `us-central1-a`. Its deletion requires an
explicit ownership decision separate from Ganesh.
