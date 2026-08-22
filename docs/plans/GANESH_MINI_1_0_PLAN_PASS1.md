# Ganesh Mini 1.0 plan — pass 1

Status: superseded by the reviewed pass-2 plan.

## Initial proposal

1. Start from the post-trained `Qwen/Qwen3.5-2B` checkpoint.
2. Reuse the Ganesh v0.1 verifier and multilingual data where practical.
3. Establish base scores on public multilingual coding benchmarks.
4. Build a balanced five-language SFT mix of roughly 20,000–50,000 verified
   records.
5. Run one QLoRA SFT experiment, merge the adapter, and evaluate it.
6. If SFT improves the development score, run a preference or RLVR phase.
7. Export 16-bit and 8-bit GGUF artifacts for laptops.
8. Compare Qwen base, Ganesh Mini, and Ganesh v0.1.

## Initial defaults

- One product bucket for JavaScript and TypeScript.
- Row-balanced sampling across five languages.
- Public benchmark scores as the primary promotion evidence.
- QLoRA rank 32, 4k sequence length, one to two epochs.
- A single 8–16 GB laptop-runtime target.

## Why this pass was rejected

The second review found that these defaults were not strong enough:

- Ganesh v0.1 data cannot be presumed reusable after its own rights and teacher
  provenance audit found unresolved lanes.
- Combining JavaScript and TypeScript in evaluation would hide compiler-specific
  regressions.
- Row balance is misleading because record lengths vary substantially.
- Public benchmarks are too exposed to support the only promotion decision.
- Jumping from SFT to RLVR adds infrastructure and reward-hacking risk before
  a 2B model has shown a clean supervised gain.
- “Runs on 8–16 GB” is not testable without separate context, RSS, and artifact
  envelopes.
- One monolithic training run gives poor failure localization.

The canonical pass-2 plan corrects these issues.

## Subsequent user decision

On 2026-08-22, the user explicitly authorized the cleaned Ganesh v0.1 training
data for Ganesh Mini. This overrides the first review's provenance concern for
that corpus. The remaining second-pass corrections—separate JS/TS measurement,
token balancing, private decision evidence, staged training, and explicit RAM
contracts—still stand.
