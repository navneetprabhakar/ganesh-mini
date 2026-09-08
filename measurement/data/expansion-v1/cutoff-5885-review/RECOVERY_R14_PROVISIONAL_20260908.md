# R14 provisional architecture retries — 2026-09-08

Status: proposal only, exactly two original parents; main approval required. No reservation, teacher launch, execution, admission, or new original coverage. R12 concurrency is not permission to launch this draft. These are architecture retries, not another independent-test critic round.

Full reads covered both immutable original prompts (including embedded faulty source), references and tests; both approved r11 request scopes; Python's complete rejected architect output; and Rust's complete r11 prompt/reference/tests/mutant. Existing diagnostic files were read, not rerun.

## Exact lineage and scope

| Original parent | Canonical parent SHA-256 | Required fresh output ID |
|---|---|---|
| exp-v1-python-repair-0138 | 097e1648410b0391b52875d213ea6a982c8d3418fe08bfd48153bf2c6da17c72 | exp-v1-recovery-r14-python-repair-0138 |
| exp-v1-rust-repair-0102 | 8c2b016284660327c9d77e34b6ccf76585bcaf4e147c761ef4d9bfe7d4a923f0 | exp-v1-recovery-r14-rust-repair-0102 |

Both remain `contract-clarification`, with the full approved r11 rationale copied into the provisional requests before adding only architecture retry instructions. The r11 derived artifact is evidence, never a replacement original parent. Approved scope: `measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_REPAIR_SCOPE_PY_RUST_20260908.md`, file SHA-256 `5890b2a7bd51e92b4139db8773399f7726070ef0a07b975cc8470a5048f84de4`. Approved r11 `datasets/cache/expansion-v1/versioned-recovery/r11/plan.json` file SHA-256 `2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6`.

### Python0138

The strict-ID guard correctly rejected `exp-v1-python-repair-0138` where `exp-v1-recovery-r11-python-repair-0138` was requested. There is no emitted r11 Python candidate or independently authored test artifact to rename or approve. A fresh architecture attempt must return the exact r14 ID, followed by the ordinary independent-test and quality/execution gates.

Preserve `aggregate_metrics`, iterable Mapping input, exact category/amount/accepted schema, finite Real excluding bool, and validation of rejected rows. Finite exact integers and standard Fraction values must not be converted to float for validation. Preserve native accepted-order summation from integer zero, native mixed-operation exception propagation, and no extra finite-output guarantee. Preserve first-accepted category order, fresh outputs and no mutation. The embedded/new known-bad source already fixes accepted-only filtering and isolates lossy finiteness conversion; do not restore the original filtering bug. Require accepted `10**500`, cancellation, Fraction controls, rejected huge values, later malformed rejected rows, category order/count and independent outputs. No new integer cap, Mapping restriction, global digit-limit setting or custom-number guarantee.

### Rust0102

The existing reference diagnostic records E0631: `trim_matches(char::is_ascii_whitespace)` supplies `fn(&char)` where a character predicate is required. Use `trim_matches(|c: char| c.is_ascii_whitespace())`. This adapts the exact approved predicate; it does not broaden whitespace, redefine VT, or change the domain. Existing r11 tests are not the cause of this compiler failure.

Preserve qualified_ref/project_slug/RepoPlan APIs and traits; primary/supporting/tag stable deduplication, distinct branch/tag identities, invalid-reference skipping, final slash/colon component, trailing slash removal and exactly one `.git` removal. New embedded known-bad source must retain the already-correct `strip_suffix(".git").unwrap_or(leaf)` and isolate Unicode `.trim()` as its only targeted defect. Tests must retain U+2003 prefix/suffix preservation, named ASCII padding controls, `repo.git.git` to `repo.git`, malformed references, ordering and nonmutation. The existing mutant and original parent reference both compiled then failed the U+2003 witness; this is historical evidence, not an r14 pass.

## Evidence bindings

Paths below are relative to `datasets/cache/expansion-v1/versioned-recovery/r11/` unless prefixed otherwise. File hashes are raw bytes; candidate canonical hash uses sorted compact UTF-8 JSON with ensure_ascii=false.

| Evidence | SHA-256 |
|---|---|
| python-failure.json | 12b92fbcff0d63fbdf5d4f3efa7d331a3f5f40547c02b933d2e1f5b2388b30d8 |
| python-recovery-architect-evidence.json | 5aa93c1a07d1ca937c2ca35f0f8ea84014829f3330b16f86dc5efcfb24b38d46 |
| Python raw final output, evidence final_output_sha256 (not a candidate) | 38b0de5a420c45cce3e6b9cd102ac0f4a4b4a2620ceb9146a40acb1f7c26682b |
| Python raw stdout_jsonl | ed13e8dcbf40ff41ec92d48a0575f327cd7b8ca140889245aa21a20eafcaccba |
| exp-v1-recovery-r11-rust-repair-0102.candidate.json file | 85c2c25a4d9305b3bebeb3f53805b70a34586f972d70963148119518b38113a5 |
| Rust r11 candidate canonical | f70b7ac81d2125c7e961f70a586cd9a2f35e09c85da8dc365bac48b700c939a8 |
| rust-recovery-architect-evidence.json | d32b5a0eb262beb8bb6376784b4357340c217fa0fb3b3e84f63e77b5d77f0f85 |
| rust-recovery-independent-tests-evidence.json | c8827440ce9e58e479cfbc6d3375142acfb82139db49a9fd704188c7e0be7747 |

Rust diagnostics directory: `measurement/data/expansion-v1/recovery-diagnostics/r11/`; filenames use prefix `exp-v1-recovery-r11-rust-repair-0102-`.

| Diagnostic suffix | File SHA-256 |
|---|---|
| reference.json | d8b5df8d5d2e91253288b8b147d92ac9dd981f49fddac89773e20cf6c20083e7 |
| known-bad-0.json | bfb3095748554d9a0d2aea91a4f9038b7875df48de75b453fbf2d1d97965439c |
| original-parent-reference.json | bd6332421e859a25ada26373720f631670b380273cccdf29360a3663d144e94c |
| summary.json | 758d76740ffd6fa2ea1f43c73eb7962b91721d4b2e757344fcb8f8d8d762b906 |

Rust raw compile stderr SHA-256: `1a17aa54b83dfeaf70ca0a7d52faa20098464f7c68efe301f95e0021a9c9e35f`; failing reference code SHA-256 `175291dbe4db834527336b4b9af08c114779ee6a7bcdea8276048cdae53a0b69`.

## Source/rights and approval boundary

Python: MdEval-Instruct revision `38c9197e3add996fae624eb198ebd06155b2101e`, row01990, source SHA-256 `73599e4b3e0df122a094495051835c773da202b671b7dc60365f75a9854362de`, MIT. Rust: McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, row03276, source SHA-256 `d11d77577758ac7332e12deb503c8cf60f1257cbd1c6e0fe66cc774fe35152b2`, CC-BY-SA-4.0. Preserve each original source/rights record and attribution; all five recorded rights remain true. These existing bindings do not independently establish release readiness.

Main must validate both request parent/hash bindings and the current ledger before approval/reservation. After generation, require exact-ID and embedded-source guards, independent tests from the permitted specification surface, seven-criterion review and sandbox directionality. Do not hand-edit prior outputs, silently salvage Python by renaming, reuse a failed reference as passing evidence, or launch another automated critic loop. No r14 artifacts or execution outcomes yet exist.
