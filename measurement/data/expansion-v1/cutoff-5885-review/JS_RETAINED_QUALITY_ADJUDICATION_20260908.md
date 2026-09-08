# JavaScript retained quality adjudication — 2026-09-08

## Boundary and method

Gate 2. Exactly three retained elementary/idiom questions from FINAL_DELTA_JAVASCRIPT_1_20260908.md: exp-v1-javascript-generation-0004, exp-v1-javascript-generation-0027, exp-v1-javascript-generation-0191. Fresh complete prompt, reference and every supplied test read for all three. This is zero new unique-row coverage and no execution evidence. No central files, holds, cloud resources or corpus changed; only this report was written.

Calibration read: SEVEN_CRITERIA_GO.md (criterion and patch-size policy), SEVEN_CRITERIA_JAVASCRIPT.md (frozen lane sample), and the relevant frozen TypeScript elementary examples. Nontriviality assesses the complete target and interactions, not line count, test volume, naming or the size of a hypothetical repair. This qualitative admission criterion is not a measured claim about model learning.

Candidate final.candidates.jsonl SHA-256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

## Definite scoped dispositions

| Candidate ID | Nontriviality | Idiomatic code | Full-contract basis |
|---|---|---|---|
| exp-v1-javascript-generation-0004 | HOLD | Scoped positive | Two string type guards, one ko-versus-other branch, and literal interpolation of two supplied strings into completely specified messages. There is no parser, localization lookup, escaping, fallback negotiation, mutable state or interacting transformation. Whitespace/empty preservation and unsupported-locale fallback are direct branches, not sufficient additional substance. The exact output tests are consistent, but cannot make this fixed-format wrapper nontrivial. Comparable to held Go generation0137/0416, not to the JavaScript sample's stateful callback or bounded-arithmetic targets. Template literals and validation are idiomatic; correctness is not the hold basis. |
| exp-v1-javascript-generation-0027 | Scoped positive | Scoped positive, minor redundancy | The full target combines synchronously thrown validation with a Promise-returning successful API, one asynchronous settlement per bounded task, stable input-index output order, and fresh arrays. A top-level async function would violate the synchronous-error boundary; collecting completion-order reports could violate ordering. Promise.all preserves input order while queueMicrotask implements the expressly required per-task asynchronous settlement. These interacting asynchronous/API constraints are substantive beyond the ready/held string formula. The final sort is redundant because Promise.all already preserves order, but is bounded at 1000, local and semantically harmless; this isolated unnecessary sort does not warrant an idiom hold. Constructing promises around queueMicrotask is not wrapping an already existing promise. |
| exp-v1-javascript-generation-0191 | HOLD | Scoped positive | One ASCII prefix guard and concatenation select the only dynamic value; all five field definitions and all four booleans/type values are supplied verbatim. The complete solution instantiates fixed literals and freezes a known two-level structure. Freshness and Object.freeze calls are direct library operations, not a general recursive freezer, graph traversal, schema derivation or interacting state constraint. Closely matches frozen held TypeScript generation0260, a constant palette with frozen copied fields. The field helper is idiomatic; exact schema/order/freeze tests are valid but do not establish nontriviality. |

Three rows: **2 proposed nontriviality holds, 1 scoped positive; 3 scoped idiom positives; 0 undecided questions.** No new prompt/API defect is alleged. Their earlier C/J positives remain criterion-scoped and cannot override an elementary-target hold. These findings do not change or reopen frozen sample decisions.

## Necessary systematic membership delta

Two repeated elementary generation targets occur in the same exact stratum:

```json
{
  "lane": "javascript",
  "source": "Multilingual-Multimodal-NLP/McEval-Instruct",
  "task_type": "generation",
  "rejection_history": "first_pass",
  "population": 273
}
```

The existing javascript_elementary_training_targets group in frozen stratum-followup-inventory-v14.json includes only javascript / m-a-p/MdEval-Instruct / repair / first_pass, population 211. Therefore propose adding **one criterion-to-stratum membership**, with evidence IDs exp-v1-javascript-generation-0004 and exp-v1-javascript-generation-0191:

| Accounting | Existing | Addition | Proposed |
|---|---:|---:|---:|
| JS elementary group population | 211 | 273 | 484 |
| Group stratum count | 1 | 1 | 2 |
| Newly added membership, frozen sample | — | 14 | — |
| Newly added membership, outside sample | — | 259 | — |
| New globally reopened unique rows | — | 0 | — |
| Global reopened union / distinct strata | 5500 / 21 | 0 / 0 | 5500 / 21 |

The 273 IDs are exactly **all** JavaScript records in final-systematic-delta-queue-v1.json, not just its prior-unheld subset. The frozen queue contains that first-pass generation stratum and no other JavaScript stratum; its exact IDs and candidate hashes already exist there. Queue SHA-256: `d7dfae1a9e37ad8f26ed1c828165c2378a0ee68eed65b6c13747d44ea9c07e64`. FINAL_SYSTEMATIC_SCOPE_DELTA_20260908.md also lists every exact member and its prior inspection source. Do not re-sort or replace the frozen corpus to express this extension.

All 273 were already globally reopened and previously inspected under other criteria. Their C/J reconciliation does not automatically adjudicate elementary quality. Conversely, membership in this group is not an automatic rejection or a demand for 273 new full reads.

## Narrow reconciliation implications

Pinned additional-holds.json contains 2745 additive IDs (2748 including the unrelated historical three), SHA-256 `19e0c0705e31461c7b9e77142f3a336a3eaaf60363372e075665462107e20fd2`. In the added stratum, 128 are already held and 145 survive at that snapshot. Both proposed hold IDs and the new positive are among those 145; finaldelta recommendations not yet integrated into that pinned ledger must be deduplicated by main.

- Preserve the 128 current exclusions; no repeated elementary check is needed simply to keep them excluded.
- This report resolves three surviving IDs: 0004/0191 adversely and 0027 positively.
- The five surviving frozen samples 0006, 0124, 0196, 0230 and 0374 already have explicit nontriviality decisions in SEVEN_CRITERIA_JAVASCRIPT.md. Preserve their substantive stateful, identity, arithmetic and grammar-based reasons; do not turn a sample flag alone into coverage.
- That leaves at most 137 other surviving IDs to **join to existing elementary evidence** at this snapshot, before accounting for later accepted holds or existing non-sample elementary findings. This is not a claim that 137 fresh full reviews are necessary, and this bounded report does not adjudicate them.
- Carry adequate prior complete-target reasoning; freshly reread only an actual gap. Neither boilerplate “not seven-criterion approval” nor the new membership itself establishes an unresolved defect.

Main should append the new group stratum/evidence in a successor scope version, preserving v14 (SHA-256 `4c0e0f9e0d32057f0738a1d57a16146619f6f355b0d686d04e0df0ffd1f44bce`) and recording parent hashes. No systematic membership or ledger update is performed here. No training or release closure follows from this bounded adjudication.

