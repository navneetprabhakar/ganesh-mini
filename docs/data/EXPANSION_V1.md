# Ganesh Mini expansion v1

## Decision

The 1,399-row seed established that LoRA training works, but the completed
`1e-4` pilot regressed from 20/180 to 13/180 development passes. More epochs
over the same corpus would amplify the demonstrated failure mode. Gate 3 now
requires a new 6,000-row execution-verified corpus before another pilot.

This is an SFT data correction, not a switch to RL or a larger adapter. The
next training recipe remains one bounded epoch and may change only after the
new data passes its own admission and a small pilot demonstrates positive
directionality.

## Frozen composition

| Lane | Rows | Share |
|---|---:|---:|
| Go | 1,200 | 20% |
| Java | 1,200 | 20% |
| JavaScript | 600 | 10% |
| TypeScript | 600 | 10% |
| Python | 1,200 | 20% |
| Rust | 1,200 | 20% |
| **Total** | **6,000** | **100%** |

Task-type target: 3,600 generation rows and 2,400 repair rows. The final token
objective is rebalanced after tokenization; row quotas do not replace the
existing five-family 20% token objective.

## Source findings

- The pinned NVIDIA OpenCodeInstruct source is CC-BY-4.0 and execution
  enriched, but a 1,000-row streaming sample contained 999 Python rows. It is
  admitted only as a Python drafting source. Its supplied tests do not count
  as independent admission tests.
- Pinned McEval-Instruct contains 35,943 rows under CC-BY-SA-4.0. Its target
  inventory is Go 996, Java 1,000, JavaScript 998, TypeScript 998, Python 999,
  and Rust 997. It is a useful multilingual drafting queue, but it has no
  independent per-answer behavioral tests and remains unadmitted pending a
  source-rights decision.
- Pinned MdEval-Instruct contains 16,008 repair conversations under MIT and
  often embeds tests with the buggy source. It is a promising repair drafting
  source, but target-lane yield is uneven and its source-provided tests must be
  rerun; independent tests are still required by the current admission
  contract.
- Public benchmark families—including HumanEval, MBPP, MultiPL-E, McEval
  evaluation, CodeFuseEval, LBPP, and SWE-bench—are prohibited regardless of
  license or convenience.

## Codex CLI teacher

Drafting uses authenticated Codex CLI 0.144.4 with the `gpt-5.6-sol` model
alias, medium reasoning, and priority service tier. Every invocation is
ephemeral, ignores user configuration and repository rules, uses a read-only
sandbox, runs from a new isolated directory, and is constrained by a JSON
output schema. The architect and independent-test passes are separate CLI
invocations. The test pass receives only the task ID and specification; it
never receives source tests, the reference answer, or the known-bad answer.

The provider does not expose an immutable snapshot behind the model alias.
Therefore regeneration is not the reproducibility contract. Each run seals
the exact prompt, raw JSONL event stream, final structured output, usage,
requested model alias, CLI version, stderr, and content hashes. Teacher output
remains candidate material until executable admission passes.

## Admission sequence

1. Import only pinned source records and preserve URI, revision, record ID,
   original record hash, license, rights, and every transformation.
2. Create a self-contained prompt, reference answer, behavioral harness, and
   at least one plausible known-bad implementation.
3. Generate tests in an isolated teacher pass that cannot see source tests or
   the reference implementation.
4. Run the reference and every known-bad implementation in the pinned
   network-disabled Docker verifier. The reference must pass and every
   known-bad implementation must fail without infrastructure errors.
5. Reject exact code overlap, exact normalized prompt overlap, and near-prompt
   SimHash overlap with every synthetic, diagnostic, development, and decision
   evaluation task. Reject duplicates within the expansion corpus.
6. Seal only when all 6,000 rows meet the frozen lane and task-type quotas.

`scripts/data/admit_expansion.py` implements this boundary. Candidate mode can
measure yield during construction; `--seal` fails until the exact final corpus
is complete and balanced.

## Quality sampling

Automated execution is necessary but not sufficient. Before training, inspect
a deterministic 5% sample stratified by lane, source, task type, and rejection
history. The sample must check prompt clarity, API consistency, test
independence, non-triviality, idiomatic code, dependency isolation, and whether
the known-bad implementation represents a real failure mode. Any systematic
defect reopens the affected stratum rather than being waived as noise.

## Current status

The contract, schema, source inventory, exact/fuzzy separation, execution
gate, known-bad directionality check, and unit tests are implemented. The
first naive six-lane tranche admitted only 1/6 rows. Explicit language runtime
contracts raised that to 4/6. A separate architect critic corrected the
remaining JavaScript reference; a separate test critic corrected the remaining
TypeScript harness without seeing reference or known-bad code. The final
combined qualification admitted 6/6 rows with zero tool events under report
seal `0aeedf655a23eacf67cab8d10bf8a4a40e3366c94b779f1734c8b22aa3dece36`.

The 60-row tranche generated ten rows per lane with zero CLI failures and zero
tool events. First-pass admission accepted 46/60. One targeted correction pass
changed only the fourteen rejected rows and raised the final combined result
to 52/60: Go 8, Java 7, JavaScript 10, TypeScript 8, Python 9, and Rust 10.
There were no additional cross-batch exact or fuzzy collisions. The final
admission report seal is
`4324d30331b872e9650c921b018561e16d275b36c2e729b4caf35f74a11ab547`.

The tranche consumed 395,472 input and 163,616 output tokens across generation
and targeted repair. A deterministic manual sample of one admitted row per
lane passed every quality criterion. This qualifies source-driven expansion
at an observed 86.7% yield; it does not justify forcing rejected rows through
repeated critics. The ten qualification topic stems are not a 6,000-row
diversity source. Production construction must draw from the pinned
multilingual generation and repair queues, oversample to quota, retain
rejections, and use Codex for transformation, independent tests, and bounded
correction.
