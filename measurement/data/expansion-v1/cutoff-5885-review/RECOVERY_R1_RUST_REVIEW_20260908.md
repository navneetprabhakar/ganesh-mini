# Recovery r1 Rust independent review — 2026-09-08

## Dispositions

- Rust0359: arithmetic correction and distinguishing oracle are statically sound; execution remains main's responsibility. Exact historical MAX-1 regression is absent, though another valid test distinguishes widening. The derived prompt adds unrelated trait requirements despite the request's no-unrelated-specification-change instruction; reconcile that scope delta before approval.
- Rust0396: reservation-headroom correction is statically sound, but the candidate is blocked by a test compilation requirement absent from its API and a record-return-value oracle/specification mismatch. A compile failure of its known-bad is not meaningful behavioral rejection.

Full derived prompts, references, independent tests and known-bad programs were read; immutable parent prompts/references/tests and exact request/plan semantics were reconciled. Calibration: SEVEN_CRITERIA_RUST.md and its seven-criterion policy. No candidate execution, teacher/cloud calls, candidate/plan/ledger changes, new unique-row credit or admission claim. Only this isolated report is written.

## Exact bindings

Canonical hashes use the admission planner's sorted compact UTF-8 JSON representation. File hashes are actual pretty-printed candidate file bytes. Paths share `datasets/cache/expansion-v1/versioned-recovery/r1/`, with full derived ID plus `.candidate.json`.

### exp-v1-recovery-r1-rust-generation-0359

- Parent canonical SHA256: `cbd06d15f78b5b9e6a8b072ea30dcf7072ab0160259bda440c9b58bd704a93be`
- Derived file SHA256: `908f58f6058ef651a0acce039457b23b741cb3938d6c4820ce06efa6bd4c2a5e`
- Derived canonical SHA256: `fdf3d8d61377de04a4a33847450769525413883ed0b5ce3210f5caa340544067`
- Prompt/rendered-prompt SHA256: `72ae0973243ee96e999cf93b015d33ed1268a6a9d2c37936f352c7089071ed0c`
- Reference SHA256: `78619130aebb935bdb579a33e77bdc9e28d3d6b0f6df614ab9b4960c9020eb00`
- Independent solution_test.rs SHA256: `1ae233950c417406d8b8b6fafdf41954b92430c704023b2c162b618072a1074c`
- Known-bad SHA256: `32461bf2cbfe334fb1928feab06efdc04276122e266b183d8e1f56bddc53ad0e`
- Original source record: `row-06157`; source_record_sha256: `ec1f4d3745ff5cc34baada0378c3581fa6e26cc2117d4d86a46d0017e1a35f8e`

### exp-v1-recovery-r1-rust-generation-0396

- Parent canonical SHA256: `e41829396ee52614f965b12d66de50255affc3c8b06af066d79d5d8f6e89404e`
- Derived file SHA256: `a349c6801a89366521b713e9d1aee9e8811a5d3f33132ab1de3e68c6db3339b1`
- Derived canonical SHA256: `92bb09e209e3afa5b123e0fa8bc0e8dfeb92e370018d640ac93b0c9c0020f3c9`
- Prompt/rendered-prompt SHA256: `f06e835be52f069657301f7e2258173bb697a62e8e89dd1bdd28188a6fbe6041`
- Reference SHA256: `e133a76d91e442c2085627ab1f120a111fe3b7e3bd3a80ba147b1ae68157caf1`
- Independent solution_test.rs SHA256: `c6d3ddeb123b27acb2ac8c05af848f054625172bddfd35f4f1b608e79287ef94`
- Known-bad SHA256: `f9063a9c0c37f7dbd49861f3cab795b8ca42fe9018d0c1d18212719f3d0ac67c`
- Original source record: `row-23861`; source_record_sha256: `d4c241abd182747b0c2414a8b2e60d1c3203a6cb81a55476eee3630d434bc1b4`


Both parents retain McEval-Instruct revision `57bd46727e49ac3e2890218a146d35c2454a8496`, CC-BY-SA-4.0 license/attribution and original source transformation lineage. Frozen parent corpus SHA256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

Read-only integrity checks verified parent canonical hashes against request and plan, message/reference equality, every file/prompt/rendered/reference/known-bad declared content hash, and byte equality of each known-bad with its original parent reference. No historical output was rewritten.

| Evidence/binding path | File SHA256 |
| --- | --- |
| measurement/data/expansion-v1/cutoff-5885-review/recovery-requests-r1.json | `c7fed0810f7fa42b2b0e5c56ccf9e0afe2c0b239db8aa529c5c0744f58e6b37d` |
| datasets/cache/expansion-v1/versioned-recovery/r1/plan.json | `a955b22d518994f9b2470cd6aaf89134a709bd7ba33dbe7d06797dc5b06ef9f1` |
| datasets/cache/expansion-v1/versioned-recovery/r1/rust-recovery-architect-evidence.json | `576ddec8680bda6b1f122bd755db4ad26dcfb6a819e91be63ee8a755d50601f7` |
| datasets/cache/expansion-v1/versioned-recovery/r1/rust-recovery-independent-tests-evidence.json | `01b6e059bd404e7f09d738d52150b9f3a80e193b9479bb39eee665b7252bd7dd` |

## Rust0359 — arithmetic and oracle

The requested operation order is implemented exactly: bonus_damage.saturating_mul(elapsed) in u32, divide by nonzero max_charge_ms, then base_damage.saturating_add(bonus). No intermediate widening remains. Charging uses affordability to bound the energy product; zero rate costs zero, and elapsed charging cannot exceed max_charge_ms. Later phase accumulation saturates and transitions discard excess time on distinct calls. Release, insufficient energy, one strike, zero-duration later transitions and interruption remain coherent.

The independent test `damage_uses_saturating_u32_multiplication_before_division` uses max charge4, accumulated charge2, bonusMAX, base10. Saturated product is4294967295; division by4 is1073741823; adding10 gives **1073741833**, exactly its expected value. The original widening control yields2147483657 instead. Thus this test statically distinguishes the actual original defect with a tiny public input; compilation/runtime confirmation is not claimed.

The historical oracle-conflict case remains important: max chargeMAX, chargeMAX, bonusMAX and baseMAX-2 must give **MAX-1**, because saturated productMAX divided byMAX is one. The new reference computes that value. The new tests do not contain that exact case. Their `final_damage_addition_saturates` case instead uses max charge1, charge1, bonus10 and baseMAX-2 and correctly expects MAX; it must not be mistaken for a corrected copy of the historical case. Recommend retaining the exact MAX-1 regression in a separately versioned test extension, while preserving the original wrong assertion as historical evidence.

### Request-to-prompt scope delta

Request classification is oracle-rebuild and explicitly says no unrelated specification changes. The derived prompt newly mandates Debug/Clone/Copy/PartialEq/Eq on value types and Debug/Clone on ChargedAction. Original reference happens to derive these, but original prompt did not require them; an alternative compliant original implementation need not expose Clone, and the new `required_traits_are_available` and `cloned_actions_progress_independently` tests make those additions binding. This is a real narrowing of accepted implementations, not necessary to correct saturating multiplication.

The derived prompt also spells out saturating elapsed accumulation and Advance::Finished after completion, matching the original reference's existing behavior. These are ancillary clarifications, not the arithmetic hold itself. Main should either authorize/document these exact changes under a revised request binding or remove unrelated requirements in a new derived version; do not silently call the current prompt an exact original-contract oracle rebuild. No reference correctness defect is inferred merely from these explicit derived requirements.

## Rust0396 — correct headroom, invalid test package

### Reservation invariant

The new prompt explicitly reserves balance + pending amount within u64. Reference record checks checked_add(reserved) followed by checked_add(charge) before any mutation. Beginning a withdrawal transfers amount from unreserved balance to pending, preserving their sum. Successful finish removes pending, reducing the sum; failed finish restores pending to balance and clears pending, preserving the sum. Consequently the failure-path checked restoration cannot overflow in a reachable valid state. Authorization and matching-ID checks precede mutation, and next-ID arithmetic is checked before reserving funds. This implements the requested semantic change; it does not merely allow restoration failure.

The targeted test starts with balanceMAX, withdraws one, then attempts a charge of one. Since (MAX-1)+1+1 exceeds MAX, it correctly expects Overflow with unchanged balanceMAX-1 and a subsequent successful failure-restoration toMAX. The original control accepts that charge because it ignores reserved headroom. The witness is valid and would discriminate the defect once the test package's unrelated blockers are resolved.

### Static compilation blocker

`empty_owner_is_invalid` calls:
`ServiceLedger::new(...).unwrap_err()`.

Result::unwrap_err requires its Ok type to implement Debug. ServiceLedger has no Debug implementation in either supplied reference or original known-bad, and the derived prompt does not require ServiceLedger: Debug (only named value types have traits). Therefore this test package statically fails compilation for both. This is a test/API mismatch, not a behavior-based mutant kill. Minimal test correction is pattern matching the Err or checking the error through an API that does not impose Debug on ServiceLedger; do not add an unrelated public trait merely to placate the test.

### Record return-value mismatch

The prompt specifies Result<u64, LedgerError> but never says whether Ok contains the selected charge or resulting balance. Original reference and original tests use cumulative balance; the recovery reference deliberately preserves Ok(updated). Several new independent tests instead assert selected-charge values:

- default charges3/5: second record expects Ok(5), reference returns Ok(8);
- subsequent override7/11 and original-user3: tests expect7/11/3, reference returns15/26/29;
- changed-default/override test: second operation expects Ok(10), reference returns Ok(13).

These are not headroom failures. Do not change reference to selected-charge returns simply to pass these tests: that would change the existing parent behavior outside the requested reservation fix. Explicitly freeze **Ok(new unreserved balance)** in a new derived contract, consistent with parent and recovery reference, and independently repair those expected values. A failing test here cannot certify rejection of the reserve defect because even the corrected reference disagrees.

Additional scoped clarifications in the derived prompt enumerate error variants, value traits, authorization-first ordering and checked ID advancement matching existing reference behavior. They should remain visible in the semantic diff rather than being attributed solely to headroom. No private ID-exhaustion execution is requested. The successful-finish headroom-release and exact remaining-headroom acceptance cases would strengthen coverage but are not new demonstrated implementation defects.

## Seven criteria

| Criterion | Rust0359 | Rust0396 |
| --- | --- | --- |
| Prompt clarity | Derived formula unambiguous; request scope delta needs reconciliation. | HOLD: record Ok(u64) meaning left unstated and oracle selects a conflicting meaning. |
| API consistency | Reference satisfies derived API/traits, but newly required traits exceed the specified correction. | HOLD: unwrap_err requires unpromised ServiceLedger: Debug; return expectations disagree with reference/parent. |
| Independent test origin | Supported specification-only author lineage; independence does not establish scope approval. | Supported same lineage; independent authorship does not excuse invalid tests. |
| Non-triviality | Positive: interacting charge/energy/phase/event lifecycle, not padded arithmetic. | Positive: authorization, overrides, reservation commit/rollback and atomic accounting. |
| Idiomatic code | Positive statically: integer bounds, enum state and native saturation. | Positive statically: owned state, HashMap overrides and checked pre-mutation invariant. |
| Dependency isolation | Standard library only; pinned sandbox result pending main. | Standard library only; pinned sandbox result pending main. |
| Realistic known-bad failure | Original widened reference is realistic and a valid test distinguishes it statically; actual execution pending. | Original reserve-ignoring reference is realistic and targeted witness valid, but compilation/oracle blockers prevent valid behavioral qualification. |

Independent-author prompt contains only the finalized derived IDs/specifications and generic instructions, not references/known-bad/source tests/architect context. Archived audit reports returncode0, no timeout, no disallowed tool items and no parse error. Prompt SHA256 `bc0844936acd54635f7d77ad060c5c7d5a9a6bec830969f8d6340d3d8f2f0280`; final-output SHA256 `8f0cab42a615f7d17080e580870255e50908ae7a71cd41cbef60e774c4b7244d`. This records origin, not executed correctness.

## Handoff

Preserve current r1 candidates and all raw evidence unchanged. Record sandbox diagnostics separately. Resolve Rust0359 scope binding explicitly; preserve a corrected MAX-1 regression alongside the existing valid distinguishing case. For Rust0396, create a new hash-bound version with explicit cumulative return semantics and independently corrected compile-safe assertions, then rerun reference and original-defect control. Never count shared compile failure or a wrong oracle as successful mutation rejection. Neither this static review nor an isolated passing run authorizes admission.

