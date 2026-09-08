# R21 Python independent static review — 2026-09-08

## Result

Gate 2. Exactly four derived generation candidates reviewed: **0063, 0017, 0156 and 0781. All four are test-quality holds; zero static positives.** The references implement their approved corrections. No reference defect is established by this review.

Read complete current specifications, references, tests and supplied mutants against original parents, approved R21 plan and RECOVERY_NEXT_PYTHON_RUST_BATCH2_20260908.md. No candidate execution, further generation, admission or central mutation. Zero new original-row coverage. Other R21 lanes are out of scope.

## Integrity and seven criteria

All four problem strings are byte-identical to original parents, as required for reference-fix. Parent canonical hashes match the approved plan. Every problem/reference/mutant equals architect output, and every independent test equals test-author output after standard trailing-newline normalization. Test-author inputs contain exactly id/problem, with no reference, mutant, source tests or architect context. Stored author prompt/output hashes validate; both author processes returned0 without timeout or disallowed tool items. Independence is verified provenance, not proof of adequate tests.

All source fields other than explicit versioned transformation match approved parent source; all rights match plan and remain true for answer/model_training/prompt/redistribution/tests. Authorized McEval-Instruct revision57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0. Approved selection evidence hash matches860adcc76d6378fc5d2a47b89ee761d59b34920dd2fb8ad9a3736b6162011cb4.

Across the seven criteria, specifications/APIs remain self-contained, targets remain substantive, references are ordinary standard-library Python and supplied mutants are realistic reproductions of the held defect. The blocking criterion is independently sufficient, contract-faithful behavioral tests. Full-task substance is parser recovery/order (0063), asynchronous completion/error ordering/ownership (0017), hook lifecycle/logging identity (0156), and matrix topology/transparency/deep ownership (0781), not patch size. Test execution remains constrained to main's sandbox; no new executed metric is claimed here.

## Individual dispositions

### exp-v1-recovery-r21-python-generation-0063 — hold: missing valueless-rel witness

Reference changes rel lookup to attributes.get("rel") or "", so parser-supplied None is handled. Mutant restores get("rel", ""), which only handles an absent key, not an explicitly valueless attribute.

Tests cover absent rel, empty URL attributes, malformed trailing markup, deduplication, case-insensitive tokens and fresh results. None contains a valueless rel attribute. The corrected defect is therefore not witnessed. Required bounded test: '<img src="a"><link rel href="ignored"><img src="b">' => ["a","b"], with valueless src/href controls. Preserve valid existing tests. Do not introduce URL normalization or a new HTML grammar.

### exp-v1-recovery-r21-python-generation-0017 — hold: timing-dependent wait-all witness

Reference collects every ticket result, stores the first BaseException by submission order, and raises only after draining all tickets. Existing argument-copy, result identity and shutdown behavior is retained. The mutant stops on the first failure.

test_gather_waits_for_all_work_before_raising_first_exception uses Timer(0.15, release_second.set), starts it, then calls gather in the main test thread. The second job may finish before gather is entered or before the first error is observed under scheduling delay; then the short-circuit mutant also sees second_finished set and passes. second_started orders worker startup, but does not tie release to an active gather observer. There is also no separate reverse-completion-order pair of failing jobs: the intended first failure precedes the second release. This is a missing reliable adversarial witness, not evidence the repaired reference fails.

Use the approved observer-thread design: first error already established; second worker started and held behind an explicit Event; observer marks gather entry and records settlement/error and second_finished at observation. Keep second blocked while checking that gather has not settled; release only under controller control, then require observer completion and first submitted error after second completion. Explicit bounded waits are scheduling safety guards, not a performance contract or mathematical guarantee over a starved scheduler. Propagate observer exceptions; always release in finally and join. Independently test two failures that complete in reverse submission order. Do not rely on a timer alone.

Current cleanup is substantially resource-safe for these fixtures: gates are set in finally and timer cancellation/join is paired; executor.shutdown waits after release. The 2-second worker-start timeout could fail a starved valid runtime, but no starvation failure is asserted here. sys.maxsize max_workers constructs no actual jobs and is not a demonstrated resource exhaustion; ordinary positive-worker tests are sufficient for this repair. No cross-args/kwargs alias policy or concurrent submission semantics should be added.

### exp-v1-recovery-r21-python-generation-0156 — hold: missing falsey logger plus private-layout oracle

Reference uses explicit None fallback and preserves supplied Logger instances irrespective of truthiness. Mutant uses logger or fallback.

All supplied loggers in tests are ordinary truthy logging.Logger instances. No FalseyLogger exists. test_constructor_validation_and_default_logger additionally directly requires unit._logger and BaseUnit(logger)._logger. That private storage name is not part of the prompt and was explicitly excluded by the approved request. A valid implementation storing the same Logger elsewhere would be rejected.

Remove private _logger assertions. Use a logging.Logger subclass whose __bool__ returns False and debug records messages, verify BaseUnit stages and AuditUnit base/audit pairs through public behavior. For None fallback, attach a temporary handler to the named default logger and restore its state in finally; no private layout is required. Retain state, hook exception, read-only snapshot and no-global-logging-configuration checks. The fresh-process import check is standard-library-only and tests a promised condition; it is not itself a forbidden candidate-side I/O requirement. A subprocess timeout is advisable for bounded diagnostics, with the enclosing sandbox still mandatory.

### exp-v1-recovery-r21-python-generation-0781 — hold: missing repeated-row placement witness

Reference copies each base row independently, correcting deep-copy memo preservation of repeated row objects. Mutant deepcopies the entire base at once.

All current nonempty base rows are independently constructed. Deep cell isolation, transparency, fresh row containers and the distinct empty-row assertion do not exercise an input where the same row object occurs twice. Both implementations produce distinct output rows for the current distinct empty inputs. Required witness: row=[0]; stamp_matrix([row,row], [[1]],0,0) => [[1],[0]], unchanged row/input. Add mutable base-cell and transparent-position controls on a repeated-row input, then mutate returned cells and confirm both inputs remain untouched. Do not add a blanket promise that every output cell is mutually unaliased; placement independence and input detachment suffice.

## Exact bindings

Candidate files below are under datasets/cache/expansion-v1/versioned-recovery/r21/. SHA256 canonical values use sorted compact UTF-8 JSON.

- datasets/cache/expansion-v1/versioned-recovery/r21/plan.json: a5fe5bbb1cffe149091f626ed317a0e79c39985c10c883acd8f83df3c04582ca.
- datasets/cache/expansion-v1/versioned-recovery/r21/run-contract.json: a455daccb7e85a30c3cc86d4c328ee44be8e6fd166afef6fe685bba9c8225be4.
- python-recovery-architect-evidence.json: file 0542350b846c80ab46b26ce914138034901641ccdb83046a1868e2b637fdc26e; prompt 9cc4116706fdea1a63e998e58c2e65f8857dafdc89171ca608793a1ae68ee392; final output 4ca9c7ddca4185341cb5332a5b4496a56c41813765c9c581d89fc5eca134408d.
- python-recovery-independent-tests-evidence.json: file 4a9f8ea3a70989b5ae6b72b782d9c458cb6634428d1b52d8ba944d419966a809; prompt 6fcdfec947b851027ab9c0ff8d65f31ccd640ce061472688126709573bd9971f; final output ad1b5edf387b29431d0f60b2adf8940d6ed25bbaae3be689c9c94529972212fd.

### exp-v1-recovery-r21-python-generation-0063

- Candidate file: aab52df3d7bdd4bc462d86272d8e833c56e19167df34813c4faeb251e6790b5a.
- Candidate canonical: ad2350f7f30aa0d8e2ae1e62b7c5ae25805b71296a319a982e0f8d02613b9a96.
- Original parent canonical: b064d4aec3a7de115990eab9116edbb5f8d63ab16722a01381ea7be991ba83ff.
- Source row-08307: eee4b16d4bcac7bda70cfaa52ef1df926cab8afa15fe4bfec6997ea37fdb0372.
- Problem: d08e2c87d1765592c39b0d92d7fcccf71e0e84ab53a5f8c60760e8951f779337.
- Reference: dc5383b9ea1ca273a52c44ee27c50026f386a44d05d035559cb3dd58fb6e3a44.
- Supplied mutant: bd7e11039e02a86ac3715e3ff1e4b63b1c6ce8f42cb3ae8afa567a41f5605198.
- Independent test: 5c4bbdf9bd34138c96848d2dfacea749fbce24336870b5b106bd9e1a86b69e94.

### exp-v1-recovery-r21-python-generation-0017

- Candidate file: 398cde94c35d2c90e88d376b383702f5f8488cbe05822a005862568c9361473b.
- Candidate canonical: 70f55aefb2559ae95ee6b3e8b21a86599adcdc7861d48e5434c3b4531f128b31.
- Original parent canonical: 723dca54f596a0ba0fd3a1b0a8c6b18d3a32c03e18ed64336c26b73c5850043c.
- Source row-08337: 264fc64f9bca86a567470ab99e8af285724d0562b4deff83bf96ab2c015bd22f.
- Problem: 55a17cb9a4a7c87fad53d875234e74dd0ad3e786a378489843369482713ee5ea.
- Reference: 2c8a2aaca90d17e9f047ccd3baeefa124b9a2560349290b6aec4f03cd9a859d2.
- Supplied mutant: cb22d8d8a79cf8ddd9797cc930076b8c565d40ebb6739702b008043f4c82e3f3.
- Independent test: 67eb1e06051f46ac2cd21a2988763ee0a10157255004cbd1b225cd9cc799ad49.

### exp-v1-recovery-r21-python-generation-0156

- Candidate file: 5e29e1f4c95202d450fd542d02f9519686dc0c1c84a68083085edb403fc71d09.
- Candidate canonical: 3bb4f63ee262a44bb403d626383b28d9776e88fa062564598776a3570d38c3a0.
- Original parent canonical: 0c23e909c2ebad68f8ede1a958275f2556a147199fbef166e3dc9c443e8e64b6.
- Source row-08157: 002be561d743d0b170192022d03dfe040e83c1d56c16e7d9c87f25d8e36bffdb.
- Problem: dd53aabfb665ded9b96d502ac5ceb89e2f3a4ee44c82890b27cdfe4a9f917cba.
- Reference: e72699b581817c88c09c6180ad5326de212ed1928d9b65d5275242700fd9285a.
- Supplied mutant: 04601ba54b2a9d8c36b51dc0437bc1f85f4d2bc8591d7e6375e62d926115fa36.
- Independent test: ebf51dee75160ce3fb63fb71323e32c92a7b217ac3e0089b4e37531e795b86e2.

### exp-v1-recovery-r21-python-generation-0781

- Candidate file: d21edb3cbb5d1c2cb6085d2092e6a58a68cf4730ab16560e6c4a8c2bf9e55911.
- Candidate canonical: 0f41054b1abeeefbdd6ab057b349dbb9bb2f97e99ae5864d18eb4b4b3881d923.
- Original parent canonical: e38611dd9c5e9d79c0ae6264ad5445cab62cfbafee1f652cba9dfe8243607df3.
- Source row-08398: 2397dd65af3b9e0d7927b07b721090b7be7c3c50ab170213e14fdfac188fad3d.
- Problem: 22f0c818bc8d999d1776bd5447344bc136cb8bfc51f675aa69e5e58b308fca74.
- Reference: a603c86b534e84c129da93df2a0efd6ae8199b0bc1693f01f71c9a2c94899a18.
- Supplied mutant: cca7111f939b953fce593f5e75e830ccffa4948f15bba553f93b683cdeb589c5.
- Independent test: f3a3063c95ed4e946e6c41d5a593861eca903dfbd9acf2f81485527d21575a91.

## Handoff

Four derived test-quality holds, with immutable specification/reference/mutant content available for a separately approved bounded test correction. No automatic correction has been initiated. Main owns diagnostics, any correction decision and admission. A reference pass or occasional mutant failure alone must not erase these missing-witness/private-oracle findings.

