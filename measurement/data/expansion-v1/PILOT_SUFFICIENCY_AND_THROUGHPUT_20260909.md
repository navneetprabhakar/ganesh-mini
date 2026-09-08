# Expansion pilot sufficiency and throughput

Date: 2026-09-09

Status: pilot-sufficient-corpus-sealed

## Decision

The fully reviewed retained expansion plus admitted recoveries is sufficient to
enter one bounded executable pilot. The former 4,000-row diagnostic floor is
retired as a pilot-entry requirement; it is not a correctness, evaluation-
separation, quality, main-training, or release waiver.

This is an adaptive measurement decision. Further expansion is justified only
by the bounded pilot's executable learning result, not by an arbitrary row
count. R26 admission, immutable combined-corpus construction, exact/fuzzy
evaluation separation, and final source-corpus hashes are now terminal.
Response-only tokenization and five-family objective weighting remain Gate 4
training-package work before any compute execution.

## Exact current corpus measurement

The reproducible JSON report is
`measurement/data/expansion-v1/PILOT_SUFFICIENCY_AND_THROUGHPUT_20260909.json`.
It binds the frozen 5,885-candidate corpus, the 2,812-parent hold partition, all
152 admitted recovery outputs, the pinned Qwen tokenizer, and the executed L4
training evidence.

- Retained originals: 3,073.
- Admitted recoveries: 152.
- Terminal combined corpus: 3,225 records.
- Input tokens: 2,438,853.
- Supervised response tokens: 1,324,262.
- Input-token volume relative to the completed 461,235-token seed pilot: 5.288x.
- Task mix: 2,105 generation / 1,120 repair (65.3% / 34.7%).
- Lane rows: Go848, Java579, JavaScript228, TypeScript293, Python537, Rust740.
- Records exceeding the qualified 2,944-token envelope: zero.
- Longest record: 2,659 tokens (`exp-v1-go-repair-0504`).
- Sealed corpus: `datasets/cache/expansion-v1/pilot-sealed-3225/train.jsonl`.
- Sealed corpus SHA-256: `4254b6f82323421edbbece17fe1a0eb43a622c697059921afbf34aca600b949d`.
- Sealed corpus bytes: 44,998,793.

Unequal raw lane volume does not become an unequal optimization objective. The
training package must attach the already-qualified per-row coefficients that
produce Go20%, Java20%, JavaScript10%, TypeScript10%, Python20%, and Rust20% of
the supervised-token objective.

## Executed throughput basis

The repaired Qwen3.5-2B BF16 LoRA run processed 461,235 input tokens in
1,560.648 seconds: 295.541 input tokens/second. Its enclosing training phase
took 1.06035x the trainer wall time. Applying that measured factor to the
terminal 2,438,853-token corpus gives:

- expected training phase: 8,750.2 seconds (2h25m50s);
- conservative training phase at 75% of measured rate: 11,666.9 seconds
  (3h14m27s);
- 30-task canary from executed evaluation throughput: 285 seconds;
- 180-task development evaluation: 1,710 seconds;
- recommended hard runtime ceiling: six hours, including a reserved final
  30 minutes for evidence backup.

This resolves pilot throughput for execution-card planning. It does not quote a
current cloud price or authorize a VM. Fresh GCloud price/quota/IAM preflight,
an exact cost ceiling, and explicit GCloud approval remain mandatory before
resource creation.

## Promotion rule

The pilot must use the qualified response-only, attention-only rank-8 BF16 LoRA
mechanism for one unique epoch. It proceeds beyond the canary only under the
frozen executable directionality rule; final promotion still requires at least
four of five product families to improve, no material lane regression, no
increase in formatting/truncation failures, and reproducible save/reload.
