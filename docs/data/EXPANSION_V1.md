# Ganesh Mini expansion v1

## Current cutoff — 2026-09-05

Navneet approved ending construction at 5,885 admitted rows: Go 1,085
(627 generation, 458 repair), Java/Python/Rust 1,200 each, and
JavaScript/TypeScript 600 each. Total mix: 3,507 generation and 2,378 repair.
This supersedes the historical 6,000-row targets below. The original config
and production state remain historical; final admission uses the separate
`datasets/cache/expansion-v1/cutoff-5885/cutoff.config.json`.

`python -m scripts.data.prepare_expansion_cutoff --output-dir <new-directory>`
validates the approved corpus hash and counts, resolves exact original
executable candidates, and creates a manifest and 300-row review sample.
Quality review and full serial execution remain pending; the family token
objective and all other quality requirements remain in force.

## Decision

The 1,399-row seed established that LoRA training works, but the completed
`1e-4` pilot regressed from 20/180 to 13/180 development passes. More epochs
over the same corpus would amplify the demonstrated failure mode. The 5,885-row
construction cutoff was subsequently reviewed in full; quality holds leave
3,073 retained originals, supplemented by separately admitted recoveries.

On 2026-09-09 the fully reviewed 3,225-row terminal corpus was measured at
2,438,853 input tokens, 5.288x the completed seed pilot volume, with zero rows
outside the qualified 2,944-token envelope. This is sufficient for one bounded
executable pilot. Its immutable source corpus is sealed at SHA256
`4254b6f82323421edbbece17fe1a0eb43a622c697059921afbf34aca600b949d`.
The former 4,000-row floor
is retired for pilot entry. Further expansion now depends on executable learning
directionality, not quota completion. Quality, separation, family-token balance,
lineage and release gates are unchanged.

This is an SFT data correction, not a switch to RL or a larger adapter. The
next training recipe remains one bounded epoch and may change only after the
new data passes its own admission and a small pilot demonstrates positive
directionality.

## Historical construction targets

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
6. Seal the exact fully reviewed retained-plus-recovery corpus only after its
   terminal count, hashes, separation and five-family token objective pass.

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

## Source-driven pilot and production reserve

The deterministic source-driven pilot used the exact pinned McEval-Instruct
and MdEval-Instruct snapshots. Eight ten-row batches were generated: one per
lane plus a second TypeScript and Rust batch. After at most one targeted
correction per rejected row, 71/80 rows passed executable admission (88.75%):
41 generation and 30 repair. TypeScript finished 17/20 and Rust 16/20, so the
initial ten-row weakness was partly sampling variance. No cross-batch exact or
fuzzy collision was found. A deterministic one-per-lane manual review passed
all seven quality criteria. The summary seal is
`a69cbdd35f2de099eb009a6e82eee53efc33c9951863b2d58f14a1b26d888a77`.

During that pilot, the rejection-correction path was found to replace pinned
source lineage with the Codex identity on changed rows. Those rows were not
accepted as production evidence. The implementation now carries the original
source object through correction; a deterministic restoration bound the old
teacher outputs to their original sources, and all corrected-lineage inputs
were re-admitted from scratch. The reproduced results, not the pre-restoration
reports, control the pilot decision.

The adaptive production reserve contains 8,480 drafting stimuli under SHA-256
`a020b6f66a40688547b71052d5123252102eb91d51f69196bef9a70d7dc9ac78`.
Its extra capacity is concentrated in Go repair and Rust generation based on
measured yield. Cross-language McEval stimuli are allowed only after the same
transformation into a new target-language task; source identity and record
hashes remain intact. The controller does not generate the full reserve
unconditionally. It stops each lane/task type when the frozen final quota is
met, applies no more than one correction, and rejects the remainder.

Production later exposed a host-capacity defect when Go admission was raised to
four concurrent records and eight AMD64 verifier containers. Starting with Go
batch 98, reference executions repeatedly reached the 60-second task deadline;
the missing timeout classification incorrectly sent them through the
behavioral correction path. A two-container retry of batch 111 also exhausted
the deadline, so production defaults to one record and one verifier container
on this host. Timeout alone remains contextual: serial batch 111 exposed a
malformed candidate test file, which is a behavioral failure eligible for the
single correction pass. The earlier parallel reports remain preserved and are
not teacher-quality evidence.

`scripts/data/build_expansion_quality_sample.py` implements the historical
6,000-row construction sample. The cutoff has since received complete original
review plus per-recovery review, which supersedes sample-only coverage. The
final combined-corpus seal must bind those review dispositions and rerun exact
sampling/separation checks against its own terminal hash.
