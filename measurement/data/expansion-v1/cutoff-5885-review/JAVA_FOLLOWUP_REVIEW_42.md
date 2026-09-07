# Java combined quality follow-up — batch 42

Positions616–630 of v14 Java queue1112, full prompt/reference read.
Four new holds: two non-triviality and two static behavioral/contract findings.
1770 total holds (1767 additive+3),4317 unique outside inspections. Resume631.

| Position | ID | Finding |
| --- | --- | --- |
| 616 | exp-v1-java-generation-0433 | Criterion-positive validated immutable records and registry presence semantics preserve existing data on duplicate insertion and distinguish missing-ID errors. |
| 617 | exp-v1-java-generation-0439 | Criterion-positive canonical-NaN/signed-zero bit matching and detached ragged-row mapping preserve source state on mapper exceptions. |
| 618 | exp-v1-java-generation-0440 | Criterion-positive quotient/remainder token allocation replaces per-transfer iteration and preserves holder/count consistency up to long transfer limits with copied arrays. |
| 619 | exp-v1-java-generation-0443 | Criterion-positive code-point boundary masking widens visible-count addition and preserves surrogate/code-point boundaries without normalization. |
| 620 | exp-v1-java-generation-0444 | Criterion-positive immutable path extension/renaming and value equality include ordered segments and optional display name without mutable exposure. |
| 621 | exp-v1-java-repair-0293 | Criterion-positive unsigned frame length and subtraction-based truncation repair maintain cursor boundaries and detached payloads for high-bit length bytes. |
| 622 | exp-v1-java-repair-0294 | Criterion-positive transposed allocation repair restores rectangular shape invariants and preserves raw copied doubles including zero-column matrices. |
| 623 | exp-v1-java-repair-0295 | Non-triviality hold: adds the explicitly prescribed byte-range guard before a supplied narrowing cast. |
| 624 | exp-v1-java-generation-0441 | Static hold: SKU edge-whitespace prohibition is checked with trim equality, allowing U+2003-prefixed/suffixed SKUs. Ordered exact changes and remove/recreate semantics are otherwise substantive. |
| 625 | exp-v1-java-generation-0445 | Static contract hold: Parcel constructor imposes unrequested nonnegative-ID and nonnull-recipient restrictions on a paging task whose record fields have no such domain constraints. |
| 626 | exp-v1-java-generation-0446 | Criterion-positive three independently implemented insertion strategies preserve ownership, duplicate ordering and binary insertion boundaries without library sorting. |
| 627 | exp-v1-java-generation-0447 | Criterion-positive complete existing ID/handle uniqueness validation precedes duplicate-candidate no-op or immutable append. Explicit trim/nonempty validation is not broadened to nonblank. |
| 628 | exp-v1-java-generation-0448 | Criterion-positive global unique-ID validation, optional filtering and selected-key/ID ordering produce independent immutable snapshots. |
| 629 | exp-v1-java-generation-0450 | Criterion-positive explicit radix conversion uses bounded reverse digit emission rather than delegating conversion and handles zero through MAX_VALUE. |
| 630 | exp-v1-java-repair-0297 | Non-triviality hold: substitutes the directly specified height variable for width in the supplied centerY expression. |

No new execution. Static findings are not executed results. Focused positives
are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
