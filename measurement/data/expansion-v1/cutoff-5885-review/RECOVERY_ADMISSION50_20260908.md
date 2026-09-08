# Recovery admission50 checkpoint — 2026-09-08

Batch r7-r10-selected25-v1 completed:25 accepted,0 rejected, candidate mode,
status passed, balance_passed=false. This is not a final corpus/training seal.
Main accepted the full r7Go/r8Java/r9Python/Rust/r10Java quality reports and
verified selected file hashes against them. All25 have fresh reference-pass,
known-bad behavioral-fail and original-parent behavioral-fail diagnostics.
R7 Go0439/0522 additionally passed actual pinned go test -race directionality;
their summary/reference bindings are included in the exact selection JSON.

Preparation compared3073 retained originals and all25 previously admitted
recoveries; no overlaps. Admission inspected546 evaluation files and executed
references/controls serially under the unchanged pinned, network-disabled,
resource-limited sandbox. Review omissions and historical failures are preserved;
race qualification is bounded evidence, not exhaustive scheduling proof.

New batch: Go9,Java10,Python4,Rust2. Cumulative50: Go11,Java12,JS9,TS7,Python8,
Rust3, allgeneration. Original holds2812 unchanged, original corpus unchanged.
Maximum retained originals+recoveries3123; minimum additional877 admissions to
4000 before further exclusions and family-token balancing. No training started.

Directory measurement/data/expansion-v1/recovery-admission/r7-r10-selected25-v1:
admitted.jsonl bytes192860,
SHA256 9cb7240b48c01afc1f600b409b3acec13bda04ebd20021995691d6cbfa87b674.
Admission logical report seal:
95a207a08bf4359c388d839d125bbd8a29dbd6591043e812b3b9cc2e88c42d43.
Selection: cutoff-5885-review/recovery-admission-r7-r10-selected25.json.

R11's12 generated candidates are not included. Its completed static reports
are main-read:10 positives (Go1/Rust3/JS2/TS4), Rust0102 reference signature hold
and Rust0361 bounded arithmetic-witness hold. Serial actual diagnostics are
running separately; Python0138 raw ID failure preserved. Repair authors saw
embedded broken input, not corrected reference; generic blindness boilerplate
must not be repeated as an evidence claim.
