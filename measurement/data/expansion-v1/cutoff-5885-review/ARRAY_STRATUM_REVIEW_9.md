# Array-validation follow-up, batch 9

2026-09-06. Array-hit positions 121–135 outside the frozen sample inspected for
prompt/reference/original-test consistency: **15 new / 144 unique outside-sample
targeted inspections**. Frozen 300 unchanged; not seven-criterion approval.
Ten diagnostic failures on nine new held records in pinned network-disabled,
resource-limited sandboxes. No timeout; JS exits `[1]`, TS `[0,0,1]`.

| ID suffix | Finding | Result file | ms |
| --- | --- | --- | ---: |
| javascript-generation-0094 | boxed MIME coerced into accepted property key | cabinet-boxed-mime-result.json | 340 |
| javascript-generation-0091 | sparse regions accepted | member-regions-sparse-result.json | 357 |
| javascript-generation-0092 | sparse labels accepted | workboard-labels-sparse-result.json | 415 |
| typescript-generation-0086 | valid required width lost in spread copy | dimensions-hidden-width-result.json | 2119 |
| javascript-generation-0097 | sparse directory accepted | directory-entries-sparse-result.json | 347 |
| javascript-generation-0098 | sparse sections accepted | dashboard-sections-sparse-result.json | 340 |
| typescript-generation-0092 | stated-valid contact rejected by stricter regex | registration-contact-domain-result.json | 2708 |
| typescript-repair-0061 | missing finite band value accepted | band-values-sparse-result.json | 2546 |
| typescript-repair-0063 | valid JSON __proto__ key lost | workspace-proto-key-result.json | 2899 |
| typescript-repair-0063 | undefined sparse slot accepted | workspace-sparse-result.json | 3079 |

Original tests omit these inputs. Registration diagnostic is a specification/
reference mismatch, not a recommendation for email validation: `a@b..c` meets
the stated single-@, non-whitespace, dot-containing domain with non-dot edges.
The frozen task does not forbid consecutive interior dots. Workspace input is
an ordinary JSON-parsed object, not prototype mutation; it must preserve the
own `__proto__` key. Totals: **116 additive / 119 holds including historical
three**.

## Scoped negative findings and unresolved boundaries

- JS generation0094 materializes bytes with Array.from before validation, so
  its byte path does not skip sparse elements. Hold is MIME type coercion only.
- TS generation0085 PreferenceStore has per-registration unsubscribe identity
  and captures active entries before notification; changes apply later. Shallow
  merge semantics commonly scope enumerable properties, so no required-field
  loss is inferred for arbitrary preference keys. Reentrant update notification
  values remain an explicit callback-policy question.
- TS generation0086 DimensionLedger similarly snapshots registrations correctly;
  its hold is validated dimension copying, not duplicate subscription identity.
- TS generation0087 AccountDirectory uses per-registration entries and snapshots
  for notification. Hidden/extra patch fields and optional active=undefined
  semantics need API review; no automatic rejection inferred from typed extras.
- JS repair0067 permissionMatrix validates with for-of before mapping a private
  dense order list. First position/last value semantics agree with original tests.
- JS generation0103 workshop menu intentionally ignores malformed records;
  missing slots are ignored by the for-of typeof guard. Field-name list is dense.
  Surrogate URI domain behavior remains unprobed.
- JS generation0106 decodeAlert checks permission before parsing, then validates
  a fixed dense field list. JSON-only input rules out constructor-array holes.
- JS generation0107 IntervalIndex maps internal push-built data and uses direct
  closed-bound comparisons. No arithmetic-overflow or sparse-input path found.
- TS repair0061 extremely large matrix sizes remain a separate infeasible-output
  domain question; diagnostic allocates only one cell.
- JS generation0091 uses a deterministic digest as required; this task's explicit
  toy credential-storage contract is not a production password-storage endorsement.

Continue at array-hit position 136. No candidate rewrite, generation restart,
revised partition, training seal or new VM. V3 scope remains nine groups / 14
strata / 3,085 review records, not automatic rejections.
