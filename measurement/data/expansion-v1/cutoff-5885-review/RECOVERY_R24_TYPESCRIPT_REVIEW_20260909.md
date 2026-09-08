# R24 TypeScript independent static quality review — 2026-09-09

Gate 2; static review only. Exactly nine R24 TypeScript candidates were reviewed against the complete plan/run contract, exact original parents and hold evidence, the batch-3 selection boundary, raw architect and independent-test evidence, and every derived prompt, reference, mutant and test. No generated code was executed, no candidate was changed, no admission was made, and no cloud resource was used.

## Decision

**Zero unconditional positives; nine holds.** Three byte-preserved generation prompts have inadequate tests. Generation-0382 has an invalid oracle, misses its defining mutant witness, and changes behavioral prompt prose despite the selection saying its behavioral specification remains unchanged. All five repair candidates have an approved prompt-scope/binding hold: their surrounding behavioral prose changed despite the explicit oracle-rebuild rule to preserve it and replace only the embedded source, apart from necessary stale nonbehavioral diagnosis.

| Candidate | Reference quality | Test quality | Approved prompt scope | Overall |
| --- | --- | --- | --- | --- |
| generation-0294 | Positive | Hold: both defining defects are untested | Preserved exactly | Hold |
| generation-0366 | Positive | Hold: duplicate-registration identity is not distinguished | Preserved exactly | Hold |
| generation-0368 | Positive | Hold: early-year witness absent; static readonly-array type error | Preserved exactly | Hold |
| generation-0382 | Positive | Hold: wrong callback count and defining child-unsubscribe witness absent | Hold: behavioral clarification added | Hold |
| repair-0030 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |
| repair-0063 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |
| repair-0158 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |
| repair-0190 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |
| repair-0211 | Positive conditional on scope | Positive conditional on scope | Hold: behavioral prose added | Hold |

These are exact-artifact holds, not final claims that the parent targets are unrecoverable. None is an admission.

## Prompt-scope discrepancies

The controlling batch-3 report requires repair oracle rebuilds to preserve all behavioral prose/API/domain/error/ownership rules, replace **only** the embedded complete source, and update stale nonbehavioral diagnosis only if needed. It separately says generation-0382 uses oracle-rebuild to remove the old oracle accommodation while its behavioral specification remains unchanged. Removing the embedded source from original and derived repair prompts leaves unequal prose for all five repairs; generation-0382 is also not byte-preserved.

- **generation-0382:** adds read-only getter wording, explicit independent-registration lifetimes, removal snapshot behavior, exception policy, controller insertion/snapshot semantics and non-exposure. These may clarify the intended target, but they are behavioral additions rather than an unchanged specification.
- **repair-0030:** adds array-valued lookup semantics for absent built-in names and explicitly accepts own or inherited array-valued entries.
- **repair-0063:** adds fresh-get, dense-array, exact prototype, sparse-slot, proto-key, failed-replacement atomicity and repeated-reference rules.
- **repair-0158:** adds complete validation timing, exact runtime string requirements, inherited-string acceptance, non-string fallback and empty-string translation behavior.
- **repair-0190:** changes “plain records” to “records” while adding proto-key/prototype/inherited-result semantics and explicit cyclic/non-record exclusions; it also restructures the formerly unfenced embedded source.
- **repair-0211:** adds Set duplicate-registration semantics and explicit per-lifetime stale-unsubscribe behavior.

The additions largely agree with the selection rationales; that does not authorize a different training prompt. As with the recorded R22 fail-closed decision, main must either authorize a new contract-clarification version or generate a source-only version under the original prose. Test-only correction cannot repair this binding.

## Per-candidate review

### generation-0294 — missing both held-defect witnesses

The reference uses indexed tag validation and registration objects, correctly preserving tag normalization/ownership, replacement atomicity, snapshot delivery, per-listener copies and idempotent per-registration unsubscription. The mutant restores only callback-identity removal.

The suite never constructs sparse constructor or replacement tags, so it does not exercise the separately bound sparse-tag hold. It also never performs the required `A,B,A`, unsubscribe-last-`A`, then-notify sequence: its initial listeners are two different anonymous callbacks, and later subscriptions do not test duplicate callback identity. Add both approved witnesses, including no notification and unchanged state on malformed replacement. No reference change is indicated.

### generation-0366 — duplicate-registration witness absent

The reference stores distinct registration objects per event bucket and removes by registration identity. Event names, unchanged title, insertion order, snapshot behavior, idempotence and immediate exception propagation are coherent.

The suite registers the same `shared` callback twice, but removes one while both snapshot callbacks still run and observes identical output strings. It never uses distinguishable `A,B,A` ordering with the last `A` unsubscribed before emission, so callback-index removal is not separated from registration-identity removal. It also does not repeat the witness on another event bucket as requested. The narrow mutant is therefore expected to survive. Add the two-event identity witness; preserve the reference.

### generation-0368 — early-year and compile holds

The reference avoids `Date.UTC`'s 0–99 year remapping by setting the full UTC year explicitly. It otherwise retains ordered validation, exact date syntax, calendar checks, email rule, normalization, nonmutation and online venue behavior. The mutant narrowly restores `Date.UTC`.

The suite has no valid `0099-01-01` or `0096-02-29` success case; its only early-year value is `0000-01-01`, which is paired with a modern earliest date and fails by ordering regardless of the remapping bug. Thus it does not distinguish the mutant. It also declares `errorsOf(...): string[]` but returns `result.errors`, whose declared type is `readonly string[]`; under the strict TypeScript contract this is a static mutable/readonly incompatibility. Change the helper return type to `readonly string[]` and add the approved early-year positive plus 1900/2000 controls. Do not open a year-zero policy or invent exact error messages.

### generation-0382 — bad oracle, missing witness and scope hold

The reference gives every subscription a distinct object and an idempotent closure, with snapshot emission. Its state/controller behavior is coherent under the derived prompt.

The drawer test's second emission has active registrations `first`, the remaining original `shared`, and one child `shared` created during the first emission. The `first` callback creates another child only after the second snapshot is taken. The correct second observation is therefore `first` plus **two** `shared` calls, but the suite expects three. The reference is statically expected to fail that assertion.

Neither drawer nor dismiss tests create two child registrations during one notification and then unsubscribe only one child before a later emission. Consequently the owner-group sibling-deletion mutant is not directly exercised. Correct the count and add the exact two-child/unsubscribe-one witness independently for service and controller. The separate unauthorized prompt expansion still blocks this exact artifact.

### repair-0030 — substantive positive conditional on scope

The reference treats only array-valued graph lookups as dependency lists, so absent built-in properties become leaves while valid inherited arrays remain usable. Tests cover absent `constructor`, own and inherited array entries, non-array inherited values, DFS order, cycles, roots, duplicates, empty names and nonmutation. The mutant realistically restores unguarded lookup. No additional reference/test defect was found; prompt scope remains blocking.

### repair-0063 — substantive positive conditional on scope

The reference validates dense arrays, finite primitives, exact plain-object prototypes and cycles, safely defines proto keys, clones repeated acyclic references independently and commits only after a complete clone. Tests cover ownership, kind isolation, trimmed IDs, replacement order/atomicity, invalid domains, sparse arrays, cycles, repeated references and own `__proto__`. The mutant narrowly restores unsafe proto assignment. No additional reference/test defect was found; prompt scope remains blocking.

### repair-0158 — substantive positive conditional on scope

The reference uses a translation only when ordinary lookup yields a string. Tests cover inherited valid strings, inherited and own non-strings, empty string, missing keys, selection/fallback, complete validation, duplicates, fresh output and nonmutation. The inherited non-string fixture distinguishes the mutant even without the optional built-in `toString` example. No additional reference/test defect was found; prompt scope remains blocking.

### repair-0190 — substantive positive conditional on scope

The reference uses `Reflect.ownKeys`, enumerable descriptors, own-existing checks, recursive copying and safe own-property definition. Tests cover recursive merge, array-within-array ownership, undefined override, symbol/non-enumerable/inherited keys, `__proto__`, constructor collision and bidirectional isolation. The narrow unsafe-write mutant is meaningfully distinguished. No additional reference/test defect was found; prompt scope remains blocking.

### repair-0211 — substantive positive conditional on scope

The reference adds an active guard to each Set-based subscription closure. The suite proves initial duplicate Set behavior, required answers, state transitions, exact errors, defensive snapshots/listener copies, reset retention, no-op transitions and the decisive old-unsubscribe/resubscribe sequence. The mutant removes only the active guard and is meaningfully distinguished. No additional reference/test defect was found; prompt scope remains blocking.

## Seven-criterion assessment

1. **Prompt clarity:** the three reference-fix generation prompts are byte-preserved and clear. Generation-0382 and all five repair prompts are understandable but exceed their approved edit class.
2. **API consistency:** exported types/classes/functions, synchronous delivery and return/error behavior are coherent. The generation-0382 callback-count oracle contradicts its own snapshot semantics; generation-0368's helper return type contradicts the exported readonly error type.
3. **Independent tests:** the independent author returned zero, did not time out, reported no tool events or parse error, and every emitted test equals the candidate test exactly. The author received IDs and full derived specifications only. Repair specifications contain their embedded broken source, so this is specification-origin independence rather than implementation blindness.
4. **Non-triviality:** all targets combine meaningful state, validation, ordering, ownership, traversal, calendar or property-key behavior; no decision is based on patch size.
5. **Idiomatic reference:** registration tokens, indexed validation, UTC full-year setting, array-aware graph lookup, safe property definition and defensive cloning are suitable TypeScript/JavaScript mechanisms. The holds arise from scope/test quality, not stylistic preference.
6. **Dependency isolation:** every task is standard-library TypeScript under the pinned local runtime, without external packages, network, filesystem or service dependency. No candidate was executed here.
7. **Realistic known-bad:** all mutants are narrow and semantic. Generation-0294/0366/0368 lack decisive witnesses; generation-0382 both lacks the defining sibling-unsubscribe witness and carries a bad assertion. The five repair mutants are meaningfully tested conditional on scope resolution.

## Immutability, lineage and shared evidence

All nine plan parent hashes equal canonical JSON hashes of exact originals in `datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl`. Candidate rights equal parent/plan rights with all five booleans true. Candidate source fields equal their exact parents except the explicit recovery transformation. Candidate messages match prompt/reference; rendered prompts match prompts. Architect output exactly supplies all derived problems/references/mutants and independent output exactly supplies all tests.

Shared bindings:

- Parent corpus SHA256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
- Hold ledger SHA256: `9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee`.
- R24 plan raw SHA256: `1f89608807b00559e993952c6d0a1936baccae882322c3315ae7efe3dd37d9fb`; declared logical SHA256: `d2816d2eaf52f5c8427808ec807f04439218bb6a502eb95f4bcee5df970d71bc`; request SHA256: `2e881ce718f8509655f0a894daddc305c869bc787deb6672a9b68d6e0d416451`.
- Run contract raw SHA256: `a455daccb7e85a30c3cc86d4c328ee44be8e6fd166afef6fe685bba9c8225be4`.
- TypeScript architect evidence raw SHA256: `bd8d57fc8e6a4dcb54fd4b4c64124263b35680dfc87e0bc69f910ffcd8a557c6`.
- TypeScript independent-test evidence raw SHA256: `c40d10a46488a704df94d075eedce2940c57a55134568b6788ca19331f4c0df3`.
- Batch-3 selection report raw SHA256: `f5e59348f4d1a986c144629f43153e39d08492380d7066fa2d3a9fe8d0bab139`.

### Candidate content bindings

Hashes are raw candidate file bytes or canonical JSON as labeled; prompt/reference/test/mutant hashes are raw UTF-8 content.

| Candidate | File | Canonical JSON | Prompt | Reference | Test | Mutant |
| --- | --- | --- | --- | --- | --- | --- |
| generation-0294 | `4d8f7a0b66f7ca63b8c35354bd84bc06e7b37056090870678b6e1e0c71e2a2f3` | `c9e8d748162d0dead05c139804106126ff84f31fe4790fac367c35da13cc97f3` | `cd5ca15648adb86896b25b15026017f2e97dedaf223e7138853ad2d5112e02ea` | `2cc6f4fab53f9f87f31a4c9ad8436cfb1434eec35f24c760451bca959024b328` | `8724f73a7b445e575ed04781abc9150ade75e5770716e327908bf87ce7fa0d56` | `a07ec64c670cfa92ba83d55fe38b4ebe3a5ca59f22ae223d49b86118f9ded863` |
| generation-0366 | `204f26c67d53fbc0fe8dbd7588493d9c127383ddc303986c62acb00b10d35ffb` | `6591a155453e236af96711c0bb08c45db3621d395dd1ad16453cfd7aee6b4c83` | `cbccd01987d29e94683586f1f6cec54cc7836c0b4086ac311a58283af641a4f9` | `007b2ae8593535fdc4c435a83504c82d2059194c33f79656bb6b2536756f19cb` | `98b86fae0a9e5608c3ffa581ff4ad8d49c8c386cb35b3b6b8e32cd50063c5616` | `0d56f1c639b53168b8c23d5e5470446af9d08484d22f7791a2ea92587981b3a2` |
| generation-0368 | `0f8215e66f980e34f1d290b28398468a36f14d9666f0bace188a6af407e2086e` | `eb740f69cec46cb470f23f3bfefc922d8bc3657528549768b1785e6bcba4a867` | `23910463ceac6581da65a37806a63b1120762f6429793c3384a83cd6c003c4c3` | `adcdaf2e12e71c8cfe821f607c05679e5edb562258e2e1cd7c8f140e4116078a` | `219c666e2b49953b51b2a9dc7cf2a9292c8736c976add76928f67a94d1cbe4ed` | `2163414e32cce1677952064fe35c40474f02364920e82a3253ca5ad63baf23dc` |
| generation-0382 | `3b45d8b685ae31853c19589be3e8f19c3b13e9ec1c0d5cd1f04752fbad668702` | `49c383e547bdb8563c00dc6d7ad632d2afd02e96b0448341432b6d3036b64636` | `424b030efc8d73386d45a676be5017200f069bdb3e41b7398831e93d5c2d525e` | `c9861b26722cd9589e3fe0f84efd641ffa1ffec8c6646d6743864f64d615d9ab` | `f78f2675e427eee108532b00a7c7c642ca35e3930bb38414ceded41c7be2047b` | `e1162b66da13fd16166153ddd0d23d0f773cf1b6e457ba929044362c3d3f0ecf` |
| repair-0030 | `fc5e6601555128b51aea8889844d4060335f344f11ab4fc459c5e9aa4d2e0359` | `6ee518ebfd46d498c89848c8ddc7cc83b2cc1e6c62f230127cb58b0f670748c0` | `0ee71db4109fbd03eddffc1eb4ed435960cda7acd2963289d1b30e0a4a7dcd61` | `0d505a55ada68d9aea8d7f9ceac3774839599c95bc47a731080448b3564a0cfd` | `e22b4fe9168893c105c621deaa2765769944efb96fb2012e7813ecceb63f7bbc` | `38b8ed2a49467d8d3b8673e0112ffc2878be6f7e884876a40ee577f7837d1df8` |
| repair-0063 | `1032dabdee475b947d80d32916412bc24a3252a7434639313fded495449c8511` | `b0c675a78343130c227564156071db092db205a81bfeb659675d36a34c784388` | `1d0cd32d9d5ca41588b60337b4c4351d51496b1efb2a871bb3a729b172a21b9a` | `49f28a66f980357fa5f0c7d4f27c5a6db83e12aba21205fd4fd127802ccbab00` | `bcdb33f64f09955f5d7d42177ba0968524d2ff6b885086e08957885ac2bd36bc` | `be9cad4a1b8d5ccaffee241185e0b1b91267bd378e4adc016f75ec633ffab9af` |
| repair-0158 | `8342e7e23950abf20e535d18fc8fbe5d292fabd1c56bd9064e1aa0820ca92531` | `a49afe95167ccc93415dc6a5bb1e1c2157f99c00e83bec6415bafc5bb8293654` | `1660dc9bfac5c39552381147001a2a1b5522bc1a12d94a1ab1da770946590c51` | `ec86e602e9f5dbe44894b0f7fc1a4929b7ba0d7c9bccb942d5e69bfa8904521b` | `07a389d1b827785e7d2dd1f7f5bb96525eae270004c27abc3d6f2e75d9eb2db6` | `9e0bceeeaa02db1f9f7385c22c4dc997d9061db4dd89d5061b0cc05ccfff9b3d` |
| repair-0190 | `f1d0fa3a09a29be8c2730db2f4552d69e6e35db281114b490b7f7f0c6a447e4b` | `0c23747ec52ccf9393b64fd4d96fe0f67a3b94deb71b28500ece987ce584df79` | `b98b1dba0c164fae15c96593bbfa1da9e3bb747c1236635d6d6a3b1da1ed7be8` | `dd7cd434eb4a9397bbc3242159b421c29f88d0d2ce256991aceefdbd68a3978b` | `45304233cf137e11bc99eeb3f47e9445c9f4097952f0da1902ffdf40e8b3fe92` | `f5720666d917e46f0e931bc442bc0e40611f8ef2746adf2e053bbaf38741e83b` |
| repair-0211 | `0e04abb1e0adbae016c794a046e9413cbed5356204af0b850c2c97ab72d7a5bd` | `202df5529a399c7299e9c3c291259055f7f2f2b23463c3ac02c790d8ac45491f` | `06f60ca13965fc2bf0abfbd3e482cc3c82adac0120beafe22e438c889e249883` | `13cfad6ec73378f7e286bd82fa11053c15d836e3548017c25424cd26c6c16bf8` | `65ca154d9a9d048b34f42ef3a9fb0d641e2a3954293776cbd2b3cac2fa71fd66` | `8f8c487159adf6ac45237063b0a5687ef458813cd13004996c484b9a6737a6ce` |

### Parent and hold bindings

| Candidate | Parent canonical JSON | Hold evidence | Source record |
| --- | --- | --- | --- |
| generation-0294 | `5b3f759e01ed5df9ac801d7dc639963f09568820de828828051e5a461072fb4f` | document-duplicate-result.json `c6d94e6538dbe6cde768340ec39b090e9f2b1b99a20b04be9ff16cc522e7ecb4`; document-sparse-result.json `d50e53603e0c9950fd7e937ea590d513bbdbd6f5fa387be52a8ed5a24b490a61` | row-32734 `91c45d3dda6eef386f52513c5b4891329f5311810d4555c71a6d7495a098f89d` |
| generation-0366 | `f7c2a72a9d9031d3ffad9c48d1b3a6f82219afb4677bfe3515cba44ef42efa64` | header_0366_registration_probe-result.json `54e8ef3280eeaeb8f988f82e3a314972d2c20ce2b0bb428898d2d1bf1d032ff6` | row-33158 `f2abb47eda2e3a2d3a2062d239d15f84ab6f0b01d6bb32155210d9f9b7c9f383` |
| generation-0368 | `43e7ee667f90b4114ca95e22c9285b47ef45665412de87fd76c7f23fc762b9a0` | workshop-early-year-result.json `6e0517b692c7351625612ef7730320d99e824c5f7a73a79cb30480972ca2be3c` | row-33254 `8cc7bc1f483937bc4a3c629ab2a27146064eff63ce575e798cf399a4f1b63751` |
| generation-0382 | `27f80e5b3c491d542f41cebaf0d3b8c72fed443b8ee3f753e153c8cde4fae8e1` | drawer-subscription-result.json `e35c96eb8202b225202bd2790e3b9a331fc49f70bf679711c5af31e609e99b4f` | row-33391 `17bdb274dfe14eb642def96744e12dbcb7971e849cedabe3ce2cf52a04914c16` |
| repair-0030 | `1507fddcff8bd1ddd40dc51bc5b592e1b455a42bc179b2567a7750c642429920` | residual-dependencies-0030-result.json `109873e8f59fb08da308c16d45a13dbed75cfc203c46964636a2ceee39532970` | row-02537 `bc2dc0700653b32df5fa9cd629ee07350e648b10dac5335e471c3a0ed419e502` |
| repair-0063 | `0c8ed1c572c9f30b9d708b9d0aff4765d86a6c778f691e09eb2d13d528fa89c5` | workspace-proto-key-result.json `d1eed3932d75d0e277df91a2baad0681216e8525060f6bcc27811ddb07abd938`; workspace-sparse-result.json `658beaae404f90fea261e5fd7f36713f9f1fa93f43cfae4ba7d0e1a622228d3b` | row-32777 `98ccd131f49c74bc70ae6088bb5396b50cb0d71ef59b6dcb69ebe4690f7466c5` |
| repair-0158 | `9b773881d015a560ed807faf980b227bd0cefa2b3c62c8a3bfc99a6220bb51cb` | panel-inherited-translation-result.json `9e552652ee51af660d2d54776016e0ced7cd83e98cc8400f5bda4324fbbdb93a` | row-32837 `394aa58aecdb3da5e23cb6421f5db58c3edec8edb2914e2f382619e5b09712d3` |
| repair-0190 | `3af1da2539951774d0e5a64a8b0d1499b765b6b823c0bc3c59a7f2bd8c8e9179` | merged-preferences-proto-key-result.json `7c5baf71ea824c882d1ac31c0f49fdc21bc6ab101e896857db549aef0f2afabe` | row-33467 `eb627c743dc8089df585abb47bea11abde5cb3819513d9edd2377ce2590b7e26` |
| repair-0211 | `a0f31f22a8d704c068cf3b5ce3673fd2fc5c977c83534fd3b208f98ca18db16c` | survey_0211_unsubscribe_probe-result.json `24874d89366cb5c6f8056c77f9f2387fa22543c31f9926c890d8265083b56d06` | row-32788 `714834166c1c38cf7b0b9d5103f7d216c7b65eee56163dd9b5c7e16ad144fed3` |

Generation and all repairs except repair-0030 retain McEval-Instruct CC-BY-SA-4.0 revision `57bd46727e49ac3e2890218a146d35c2454a8496`; repair-0030 retains MdEval-Instruct MIT revision `38c9197e3add996fae624eb198ebd06155b2101e`. This verifies lineage, not a new rights determination.

Main should preserve every exact artifact and hold, reconcile the prompt-scope failures centrally, and not count any of these nine as a seven-criterion positive or admission.
