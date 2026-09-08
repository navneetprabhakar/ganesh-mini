# R11 Rust repair independent static quality review — 2026-09-08

## Boundary and result

Gate 2, exactly five derived repairs: exp-v1-recovery-r11-rust-repair-0343, -0361, -0113, -0102 and -0095 (each suffix expands to that complete prefix). **Three static positives (0343/0113/0095), two derived quality holds (0361 test discrimination, 0102 reference compilation).** This review executes no candidate, claims no sandbox result or admission, and adds zero original-row coverage. Originals remain held. Python is outside scope.

Read complete original and derived specifications, embedded faulty source, references and tests; reconciled original evidence and approved repair scope. Contract-clarification explicitly permits replacing embedded faulty source and repair description while preserving corrected objectives/APIs. This is not a reference-fix byte-equality exemption invented after generation.

## Provenance and integrity

All five canonical parents match plan bindings; original source objects and rights equal their approved plan objects. Derived source preserves every original source field except the explicit versioned transformation; all five rights flags remain true. Source is authorized McEval-Instruct revision 57bd46727e49ac3e2890218a146d35c2454a8496, CC-BY-SA-4.0. No rights decision reopened.

For all five, architect output problem/reference/mutant exactly equals candidate problem/reference/mutant; embedded fenced Rust is byte-identical to the supplied mutant. Independent author output equals the test file. Author task objects contain only id/problem, with the derived problem including its complete repair mutant. Architect and independent-author calls are separate; return codes 0, not timed out, no disallowed tool items, and stored prompt/final-output hashes recompute correctly.

Important provenance correction: the independent-author prompt's generic boilerplate says it has not seen a known-bad implementation. That sentence is literally inaccurate for repair tasks because the problem embeds it. Actual payload supports independence from the reference and original tests, not blindness to the embedded repair source. This visibility is explicitly permitted by the approved repair scope; it is not evidence of reference leakage.

File SHA256 bindings:

- Original corpus: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
- R11 plan.json: 2adb55c09e9ca50683d9703be52a73b2b9b22c2d131873efe99347e44d4d4fc6 (internal plan_sha256 9ea52821b748c6e429216a477e3484a08fb7a56f6713c2a1382df40ccf0cd15b).
- rust-recovery-architect-evidence.json: d32b5a0eb262beb8bb6376784b4357340c217fa0fb3b3e84f63e77b5d77f0f85.
- rust-recovery-independent-tests-evidence.json: c8827440ce9e58e479cfbc6d3375142acfb82139db49a9fd704188c7e0be7747.
- RECOVERY_REPAIR_SCOPE_PY_RUST_20260908.md: 5890b2a7bd51e92b4139db8773399f7726070ef0a07b975cc8470a5048f84de4.

The first three named JSON files are under datasets/cache/expansion-v1/versioned-recovery/r11; the scope note is under measurement/data/expansion-v1/cutoff-5885-review.

## Seven-criterion decisions

### 0343 — static positive

Clear exact grammar, empty matching value, case-sensitive first match and whole-input validation. Public borrowed-input API is consistent; standard-library slicing uses ASCII delimiter boundaries and retains permitted UTF-8. The full target combines parsing, validation and selection rather than elementary padding. Reference rejects forbidden ] in both extracted fields without early-returning a match. Independent tests include a matching bad]value and a bad]kind after an earlier valid match, which distinguish the actual omitted-validation mutant; malformed suffix, empties, Unicode/newline, ordering and borrowed-input controls support the corrected objective. No unsupported oracle or dependency found. Realistic targeted defect is preserved with the original selection correction already present.

### 0361 — derived hold: bounded defect-witness gap; reference statically positive

The clarified 64-bit contract, exact mathematical time quotient/remainder and bulk per-step-equivalent clamping are coherent. u128 intermediate arithmetic preserves the carry, and the quotient fits usize under the stated runtime; opposing directions and independent clamping are retained. This is a nontrivial state-transition target, standard-library-only and idiomatic. Tests are independently authored and their expected arithmetic is correct.

However the overflow test uses step=10 and elapsed=u64::MAX after accumulating 9; the other maximum-count test uses step=1 and elapsed=u64::MAX. The supplied mutant still performs one loop per step. These require astronomical mutant work before the intended arithmetic assertion can be observed; a timeout is not a bounded semantic witness of the saturation defect. Even a version fixing saturation while retaining the old per-step loop would time out. This is not a claim that these valid bulk-work oracles contradict the derived contract.

The approved tiny witness is absent: a 1x1 grid with step=u64::MAX and elapsed sequence MAX-1, MAX, 1 must return 0,1,1; the saturation mutant returns 0,1,0 after at most one step per call. Require that bounded specification-grounded witness before calling the intended defect independently distinguished. Test-only correction is sufficient; no new numeric domain, implementation change, allocation probe or coordinate injection is needed. Main owns diagnostics/correction decisions. Ordinary validation/exact interval/remainder/clamping tests do not replace this witness.

### 0113 — static positive

Logical maximum ring length and overflow-free wrapping are explicit, with existing traits/API only. Reference previous uses zero-to-last or decrement, while next remains safe because maintained index is at most len-1 (thus at most usize::MAX-1). Empty handling, resize clamp/reset and page/overlay/focus isolation remain correct. Full target coordinates ring and UI invariants, not merely a one-line arithmetic exercise. Independent maximum-length next-then-previous is a tiny real overflow witness; subsequent previous/next checks wrap. Empty, ordinary wrap, resize and UI controls are valid and dependency-free. The requested singleton regression is not explicitly present, but static code and existing zero/ordinary/wrap coverage do not expose a concrete new failure; do not turn every omitted redundant control into a hold.

### 0102 — derived hold: reference predicate signature

The contract correctly names Rust char::is_ascii_whitespace, retains exactly-one .git removal and stable branch/tag ordering, and preserves Unicode text. The supplied reference passes char::is_ascii_whitespace directly to trim_matches. That method item accepts &char, while the string pattern predicate expects char, so the implementation is statically type-incompatible. This is a reference compilation/API issue, not an unsupported test oracle. Main sandbox should independently confirm; no execution is claimed here.

The independent U+2003 boundary slug test directly distinguishes the overbroad Unicode trim mutant. ASCII padding, suffix case/exactly-one removal, empties, ref validation, category identity/order and stored-string equality are specification-grounded using only existing traits. FF is not explicitly exercised, but the principal defect has a real witness. Whole-target parsing/normalization/ordered deduplication remains substantive; standard-library-only. A predicate adapter respecting the exact named ASCII predicate would address the narrow reference issue, without changing contract, broadening to Unicode trim, or imposing new VT policy. No automatic correction launched.

### 0095 — static positive

Explicit coherent new/default initialization, failure order, success-only IDs and exact same-entry authentication resolve the original discrepancy without a private-layout oracle. Reference delegates Default to new, retains AND authentication and ordered validation; lifetime ID exhaustion is explicitly out of scope. Independently authored tests directly compare first IDs from both constructors, plus failed/duplicate additions not consuming IDs, independent books, case-sensitive credentials/permissions, observers and nonempty blank credentials. These follow the prompt rather than adding trimming or trait requirements. Full target combines insertion atomicity, identity/authentication, initialization and observations; idiomatic standard-library implementation and realistic derived-default mutant. No concrete remaining static defect.

## Exact per-candidate bindings

Canonical hashes use sorted-key compact UTF-8 JSON; file hashes refer to original candidate JSON bytes. Candidate files are in datasets/cache/expansion-v1/versioned-recovery/r11.

### exp-v1-recovery-r11-rust-repair-0095

- Candidate file (exp-v1-recovery-r11-rust-repair-0095.candidate.json): 04af32e4998528b026cbd126d8225b4af7016f43cfa3d9915bdca69ab993bb4c.
- Candidate canonical: c73de157b4544c808a2c70fe5b016843b2db4736b7abf54d4310d6085312979f.
- Parent canonical: 1f0349892f99919906a6a1150d189fdeb1404b3d04dc11a6db486c2478f36ad7.
- Source row-23720: d8d862ca93eac78348575794a692db1cab7dfeca2f6ee7eba370ca9c88656da8.
- Parent hold evidence: measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_6.md; SHA256 2e5a33cf86973a29052f686083002293dc924375abc0a129ffa7d02f570c296f.
- Problem: 6ad0cd4d70369837c82af3005581267d32c8ccfbae241909fe8a6f1e4acf0192.
- Reference: 2d07025a2822e3dff34e72f04fb9f7e604a19a557fba26dbcf1ed84ad6b49f6a.
- Embedded/supplied mutant: 3b82c08fcf9e4bb271f792464fc0b8debd82afc43a6164b50efa79ad54400853.
- Independent solution_test.rs: 07c8c24033fc09047a84c3c7cee97d462c4b43f2869c0689555e2cd59761ba06.

### exp-v1-recovery-r11-rust-repair-0102

- Candidate file (exp-v1-recovery-r11-rust-repair-0102.candidate.json): 85c2c25a4d9305b3bebeb3f53805b70a34586f972d70963148119518b38113a5.
- Candidate canonical: f70b7ac81d2125c7e961f70a586cd9a2f35e09c85da8dc365bac48b700c939a8.
- Parent canonical: 8c2b016284660327c9d77e34b6ccf76585bcaf4e147c761ef4d9bfe7d4a923f0.
- Source row-03276: d11d77577758ac7332e12deb503c8cf60f1257cbd1c6e0fe66cc774fe35152b2.
- Parent hold evidence: measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_7.md; SHA256 f59c4574805967e005972ce8dfb22631d84d718b697fac03246865e592422e60.
- Problem: 9db62fc4f00f8c96ebb0d28c91c5c658772105f2f67205ad8315d6aacad57089.
- Reference: 175291dbe4db834527336b4b9af08c114779ee6a7bcdea8276048cdae53a0b69.
- Embedded/supplied mutant: 6b2ec40b5b9a4653c04112c1490efe0704952f24c0bede3e1b95de727ea94637.
- Independent solution_test.rs: 500efea0380cda6cd9e45f034c186ca1f13111d220f08ac6a76dc5102b830f40.

### exp-v1-recovery-r11-rust-repair-0113

- Candidate file (exp-v1-recovery-r11-rust-repair-0113.candidate.json): 1763859eb37606309cb67b929b191936b40c4591918afa6307deb09742e36e29.
- Candidate canonical: 228b2014f2bfa79313ea73ee6bb4bba7427efd20a5859822c8329cc609c9bc98.
- Parent canonical: 942bc20053c7f88bad642fef157e0cc411dd89b5b27ad9f5479166fe70e921f7.
- Source row-06274: 8fcbdea35247717fcc566870d4b776765c99c868dff6533147fe2d90cf04f6fb.
- Parent hold evidence: measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_7.md; SHA256 f59c4574805967e005972ce8dfb22631d84d718b697fac03246865e592422e60.
- Problem: baf4d1bb698229f05837b7ad8b6de7afd6586e820a91bd293f159b5e5ea8e246.
- Reference: a0a07c0aa0cb17d1b2ae7bedabef91cbb0d08162bd2619f56cbed16f8c095ca4.
- Embedded/supplied mutant: f853812d47850d680a7677b8b30802e1f52a71d62178e44157420b166d49d919.
- Independent solution_test.rs: e10de110224e38a5a330c18c47a729349cda36999844976cff700948d386ba4d.

### exp-v1-recovery-r11-rust-repair-0343

- Candidate file (exp-v1-recovery-r11-rust-repair-0343.candidate.json): 4832622424bc3ccd0fc4f3c4d9d102d9977c9848e3c0a810c2b1eb78d1f5c53c.
- Candidate canonical: f5fcf7933e4152b085089469519156b61f170e91322c06423fe2933c3ef32f76.
- Parent canonical: c9dd3f8da96f17de8beb02fa7caa4db8b37bcc8ac5310049ba80d78352dc61dc.
- Source row-23662: 69f046905718618b53c19cc17341846b06ede647a6a851c5dbf0d7922941a78a.
- Parent hold evidence: measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_21.md; SHA256 079207144cccdb572f633febe23b60ed2a9c26bb42e395fb6cd124da2a1d038d.
- Problem: 531906e80b4a79d49ab341b69def44d5793a57e164cef1732e04f14b4f625ff5.
- Reference: d484fe245f55a2f4bf3b6fe242ae6ecb480aeefef5b40d8cd7a535b71bbb417c.
- Embedded/supplied mutant: d41eed62c476eefb56b881ce9487aff9b1e561112fa555918da8835df2d8dd54.
- Independent solution_test.rs: 5fc006438e8e0229b4f0e399b22021dff5fd5b61410d65a43a92b7fd17e2bd8f.

### exp-v1-recovery-r11-rust-repair-0361

- Candidate file (exp-v1-recovery-r11-rust-repair-0361.candidate.json): 438935de5c604591aa9170dd436f57aa13e8c6015b44b277d5d5b6e67527e6e4.
- Candidate canonical: dcaa7a451cdd18cae01a70720e033f3fb00752cdbbe54ba27b6bd37e5ff9d0bd.
- Parent canonical: 7f4a1f8b5996c876c97df3b662c4198b0e58ea0420b219abf391399d3a6aa015.
- Source row-23923: 69e904572e01dba6a53d62c34aff15a6a7af7dbbc934bdf50c1b14464c7a80db.
- Parent hold evidence: measurement/data/expansion-v1/cutoff-5885-review/RUST_ELEMENTARY_REVIEW_22.md; SHA256 556d8b77f2081976d98289781c3be970575497703a7b708d57d782761d3ee8ad.
- Problem: d34bfd43761720379a766fb3ee60f19bf3e4a3d2b147143d993024af3d1f28c0.
- Reference: ed316859966eeb6b8bffebea10cd9607a14bb387ca3ae3177a5ea2046e274e40.
- Embedded/supplied mutant: 3b87f6a3c1e515e6cf3e568016625dd897a0f497cdbca8ad311b08e7afaf6d78.
- Independent solution_test.rs: 97f9ee7e173587ce87da2f259fcc9c1d1dacaf0cd12bba762a23d02151b15d52.

No central files, candidates, plans, ledgers or original evidence changed. Main retains serial resource-limited, network-disabled verification and admission responsibility. No further critic loop or generation initiated by this review.

