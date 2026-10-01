# Gate 3 token-length hard stop — 2026-09-24

The 720 capability cohort and 180 broad replay rows passed package-level
content-free exact, normalized, and fuzzy separation against the remaining
3,045 prior training rows, package peers, and 540 frozen private evaluation
tasks. All six failure counts are zero. The immutable separation report is
`measurement/gate3/capability-scale-v1/package-separation-v1/report.json`,
seal `e1df396fd714c9b984649630d03da22efc816245841e80dbdb2e637dc0c805d8`.

The next untruncated Qwen tokenizer pass found one failure among 900 rows:
`cap-scale-binary_and_bitwise-typescript-repair-first_pass-01` renders to
3,032 tokens, exceeding the frozen 2,944-token training maximum by 88.
Response truncation is forbidden. The failed tokenization report is
`measurement/gate3/capability-scale-v1/package-tokenization-v1/report.json`,
seal `4e44bd293e5a7d5404ed44600c7534cf0fcf12bb46da60d835281e8449456927`.
The original 720 seal is construction-stage evidence, not a final 900-row
training package; no training or release may proceed from it.

The same cell has two prebound but unused queue sources,
`cap-scale-binary_and_bitwise-typescript-repair-reserve-06` and `-07`. Neither
has teacher, semantic, independent test-author, delta, or executable evidence.
The frozen reserve activation rule covered terminal first-pass construction
failure, whereas this first-pass candidate reached executable admission and
then failed the final token-length gate. The construction plan also marks a
failed final corpus gate as a hard stop. Do not silently reinterpret reserve
eligibility, modify or truncate the admitted row, count an unverified reserve,
or reuse the old failed package.

Recommended prospective resolution: approve one-cell post-admission
token-length replacement using the already prebound `reserve-06` source;
preserve this failure and the existing 720/180 artifacts, qualify the new row
through teacher, semantic, independent test-author, blind delta, executable,
separation, quality, and token-length checks, then rebuild and reseal a new
720/900 package. Use `reserve-07` only if separately justified and within the
original two-reserve-per-cell allowance. The counted teacher usage is
1,059/1,200 before any such draft. This is a proposal, not authorization to
activate the reserve under the current frozen rule. No GCloud action occurred.
The exact proposal is
`docs/plans/GATE3_TOKEN_LENGTH_ONE_CELL_REPLACEMENT_20260924.md`, SHA-256
`1844d190adcdc47496fc18fa9ec94babaeb469931985b384ac0c575726d4b13c`.
