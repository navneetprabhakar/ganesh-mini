# R21 Rust six-candidate review — 2026-09-08

Static full review of complete derived specification/reference/tests and mutant differences against complete references, approved R21 plan and bound selection evidence. Existing diagnostic artifacts were read, not executed by this reviewer. No generation, admission, retry draft/version, central edits or new original coverage.

## Dispositions

All six references are statically consistent with the approved scoped corrections. **Six test-quality holds, zero terminal quality positives.** This does not equate failed test expectations with defective references or passing diagnostics with admission.

| Suffix | Archived reference / mutant / original-reference outcomes | Disposition |
| --- | --- | --- |
|0012|pass / pass / pass|HOLD: missing parenthesized extra-token witness|
|0064|behavioral failure / behavioral failure / behavioral failure|HOLD: unsupported specific invalid-Named error oracle; ordering witness exists|
|0071|pass / pass / pass|HOLD: CR test at final header line misses defect; unpromised Debug bound|
|0111|pass / behavioral failure / behavioral failure|HOLD: unpromised Debug bound and incomplete approved proposed-state coverage|
|0342|pass / behavioral failure / behavioral failure|HOLD: approved non-ASCII key-domain witnesses missing|
|0414|behavioral failure / behavioral failure / behavioral failure|HOLD: raw-tab rejection contradicts approved trim-before-control interpretation|

All diagnostics compiled; reference failures0064/0414 are runtime assertions, not compilation failures. Evidence uses pinned rust-1.85.0 image ganesh-mini-rust-verify@sha256:f7a845c048ec8b96df961b9b1b754dcfcf5e2f824401e59cca0a1c42d64c2192, sandbox contract b64089f9f047e0b6b0a475e6c2f19ea9451d2480109ad08abb1b2561f7070e6e. No timeouts reported in inspected reference diagnostics.

## Per-ID review and minimal specification-only correction feedback

### 0012

Recursive-descent precedence, unary chaining, checked literal/add/subtract/multiply/divide/negation and byte offsets are substantive and idiomatic. The reference distinguishes a present unexpected token from EOF after parsing a parenthesized expression. Existing tests cover extra tokens only outside parentheses; therefore the realistic mutant and original reference pass.

Test-only feedback: retain valid existing cases; add evaluate("(1 2)") -> UnexpectedToken(3), nested "((1 2))" -> UnexpectedToken(4), and "(1 a)" -> UnexpectedToken(3). Keep "(" and "(1 + 2" MissingClosingParen, empty parentheses, missing operands, byte offsets and checked i64 boundaries. Do not invent cross-error priorities or allow out-of-range positive literals just because unary minus precedes them. No new depth policy.

### 0064

Precollecting names without early errors, then validating each model and properties in order, fixes the actual hold and allows forward references. Exact formatting/recursive types/outer Option are preserved. Tests already contain earlier bad-name property versus later duplicate model, a decisive ordering witness.

The reference diagnostic fails only because Named("Not.Valid") yields UnknownModel while test demands InvalidIdentifier. The contract requires validation of Named references but does not explicitly assign lexical-invalid absent references to InvalidIdentifier instead of UnknownModel; requiring one category here adds an error-precedence interpretation beyond the approved scope. Reference correctly rejects it. Do not claim the runtime assertion proves a reference defect.

Test-only feedback: remove this exact category overconstraint; require rejection for malformed absent Named text without fixing its unspecified category, and independently test syntactically valid absent Named("Missing") -> UnknownModel. Retain invalid declared model/property identifiers -> InvalidIdentifier. Add earlier nested unknown reference versus later invalid/duplicate model, and earlier bad-name property versus later2Later, alongside forward-reference controls. Keep lexical grammar authoritative: keywords and "_" are accepted text-generator identifiers; generated text need not compile. No extra traits beyond those declared.

### 0071

LF-only split and explicit CR-as-value preservation implement the approved contract clarification. Binary payload is owned without UTF-8 restriction; text parsing additionally validates body UTF-8. Names/values, duplicate order, first separator and exact two-space-separated fields are coherent.

Current CR witness is the LAST attribute before LF LF. Header slicing removes the separator's first LF, leaving a terminal CR, which str::lines does not strip. Thus the mutant passes. Also success .unwrap() on Result requires ParseError:Debug, unpromised by specification and explicitly excluded in approved scope.

Test-only feedback: use trait-neutral success matches with a fixed panic message, not unwrap/expect or Debug formatting of errors. For BOTH parsers use READ / followed by LF, key:value CR LF, next:kept LF LF body; assert both attributes including literal trailing CR and exact body. Keep duplicate/empty/colon-containing values, first-separator behavior, binary invalid UTF-8 acceptance and text rejection, independent ownership after caller input mutation. No CRLF alternate framing or general control ban.

### 0111

Reference clones a proposed rule, applies tri-state patches, validates all resulting fields and commits only on success. Public invalid id/channels/prefix are checked and a cleared invalid optional field can become valid. Stable borrowed ordering is correct; no constructor-only invariant assumption. Existing direct invalid-id case rejects the mutant and original reference.

Tests still use create/update Result.unwrap requiring unpromised RuleError:Debug. Public-field pointer assertions on failure are not independently held here: the prompt explicitly says byte-for-byte unchanged. However approved feedback requested public-value snapshots, not incidental trait requirements. Missing planned empty-channel/blank-prefix and clear-invalid-optional controls leave targeted coverage incomplete.

Test-only feedback: trait-neutral matches for success; explicit RulePatch fields (no Default), no NoticeRule Clone/Eq assumption. Create then independently mutate public id=0, clear channels, or make prefix whitespace-only; apply otherwise-valid expiry change and require corresponding error with complete public-field snapshot unchanged. Separately set invalid existing expiry/tags and clear through Some(None), requiring success because proposed state is validated. Preserve full valid tri-state behavior, empty tags, exact text and stable returned reference identity. Avoid priority assertions when multiple fields are invalid.

### 0342

Named char::is_ascii_whitespace closure is correct on key/value paths; duplicate tracking and exact-one-equals handling remain intact. NBSP literal summary test already rejects Unicode-trimming mutant, so this is not missing ALL defect coverage. Required output ownership and grammar controls are substantive.

Approved scope additionally requires non-ASCII-prefixed key identity: missing. A solution fixing values but still Unicode-trimming keys would pass current tests.

Test-only feedback: add U+2003-wrapped label preserving both characters; U+2003-prefixed code without actual code must fail missing required code. With actual code present, the prefixed key is a unique ignored unknown and must succeed; repeating that identical unknown key must fail. Retain ASCII tab/form-feed padding, no specified error-string demands, and do not add a Unicode-only blank-line policy or treat VT as char::is_ascii_whitespace.

### 0414

Reference validates all trimmed entry keys before resolving conflicts, preserving EmptyKey priority and first malformed index. Existing conflict followed by DEL-containing key decisively rejects the early-conflict mutant. Owned output and ASCII matching are correct.

Two reference assertions fail because tests demand leading/trailing TAB be rejected before trimming. Approved scope expressly preserves trimming before interior-control checking. Thus tab-prefixed valid key at index1 is valid and empty key at index2 is first malformed; trailing-tab "key" is valid.

Test-only feedback: change expected first malformed index to2 in the existing leading-tab case, or replace index1 with a genuinely interior control for an index1 witness. Trailing-tab key must return trimmed matching value. Retain interior TAB/LF/NUL/DEL rejection, complete validation after conflict, multiple malformed suffixes choosing first, valid-only conflicts, equal values, no match, detached output and ASCII-only comparison. Do not reopen raw-padding policy or add allocation restrictions.

## Seven-criterion accounting

Prompt clarity/API consistency are scoped positives for references;0064 category ambiguity and0414 oracle interpretation are explicitly handled without adding behavior. Independent test origin is positive: exact separate author items bind tests, while architect items bind problem/reference/mutant; no implementation leakage inferred. Nontriviality is positive for grammar/checked diagnostics0012, recursive forward-reference rendering0064, framing/ownership0071, transactional tri-state updates0111, key/value grammar0342 and validation/conflict precedence0414. References use idiomatic standard-library code with no external dependency. All mutants model the actual held semantic family;0012/0071 lack a rejecting witness,0064/0414 have unrelated false oracles, and0111/0342 pass directionality but retain the identified test obligations. All six remain test-only holds, not architecture failures.

## Exact artifact bindings

Candidate/evidence base: datasets/cache/expansion-v1/versioned-recovery/r21. Diagnostic base: artifacts/verification/cutoff-5885-vm/recovery-diagnostics/r21-ts-rust-js. Candidate canonical JSON hashes use sorted keys, compact separators, UTF-8 ensure_ascii=False. Each complete candidate filename is ID.candidate.json. Source metadata is distinct from generated answer/test evidence.

Approved evidence: measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_PYTHON_RUST_BATCH2_20260908.md SHA256860adcc76d6378fc5d2a47b89ee761d59b34920dd2fb8ad9a3736b6162011cb4. R21 plan file SHA256a5fe5bbb1cffe149091f626ed317a0e79c39985c10c883acd8f83df3c04582ca. Original source/rights decisions are preserved, not reopened.

### exp-v1-recovery-r21-rust-generation-0012

- Original parent canonical: 45578ce324c41c8bee44f0b9bd48f5184c0022494f0ab67265cdac2053b02886
- Candidate file: 2777fbe8c5694f623827d8fe6cbe9e135cf88a332e3d061ec290f27dc7c48ed0; canonical: bf531b354b2d7e9c35d34792fa145056770daef4e30bfa39f5feee876e100ff7
- Prompt: e7c6e0f5675d424679743bc779608c1fedb756484877786d65bb9a5ccc2d8c7e; answer/reference: 825ab51d467e944d9a926ec136f417bf0604b38ce11fa5f512d458dc1440973c
- solution_test.rs: f435298ff4de3f690876a1935934956840ae4f7b3e4548b087def93ecb2d8ba6; known-bad: 5209df71dd4f4395536d3608c63cc1731e2a69ada15d5ccc05ae9aaa2376cdee
- Source: {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-23670","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"74e0892178c4208a92529ad7ff121ff460e9234a8652f3b295de27d18e13a0cd","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests; versioned recovery exp-v1-recovery-r21-rust-generation-0012 from exp-v1-rust-generation-0012 sha256=45578ce324c41c8bee44f0b9bd48f5184c0022494f0ab67265cdac2053b02886","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Diagnostic reference.json file SHA256: af264af2820b58aed2fb9a4d568de7b516373238a64eea43d39ee16b26ac9611; exit codes [0,0]
- Diagnostic known-bad-0.json file SHA256: 68b8f0e633487945eac180223a01209bd304ed8aa727c56f877279f6d4ca1ac8; exit codes [0,0]
- Diagnostic original-parent-reference.json file SHA256: a6d2dae354071f1f71234e82bc13e3ab9701babcc6052c4645e93951f94b97e4; exit codes [0,0]
- Diagnostic summary.json file SHA256: 76fb5fe27836360c5e5347d1d4d437b138ca37ade851bc914917d166a8e3991d

### exp-v1-recovery-r21-rust-generation-0064

- Original parent canonical: 3b3050e4e3e301fdadaaf3fd2d92ce3ce57b0e8e0067cb32112ed88a58adb9dc
- Candidate file: cbc6e0c9bd7b2edc828c32b8041120e33a7f8d510b29f2401de58d4ae17b91da; canonical: a15cc83ff8dadf1061389ff4dffa8d882605d8ab110b0ac9abfdfd59a45cce7e
- Prompt: 77072b4f93d931a0ea22ed6b5bb574ebb5ac1c0a859f0418b3f929610f026d13; answer/reference: 4350c496ca5b7d2339837cdbb164d50593aba86b472d8468da94160f624dad1f
- solution_test.rs: 3de685ddfaad559c0f9ffec6a5c58fda5875ec4de62d4081ff707c3189d6d98a; known-bad: ab4afb2c071d0c87293586117951727fbba81ceaba47005de23f74c8159bc0f9
- Source: {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-23794","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"87494f452d3efe2333a2407b843683deaf960d7ad7a38585c5244925f2e26c17","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r21-rust-generation-0064 from exp-v1-rust-generation-0064 sha256=3b3050e4e3e301fdadaaf3fd2d92ce3ce57b0e8e0067cb32112ed88a58adb9dc","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Diagnostic reference.json file SHA256: a040fd65ae3c448242be1c055a67e7d4d191ea440733d5ee2cdf89275854802f; exit codes [0,101]
- Diagnostic known-bad-0.json file SHA256: d9fe3a4b30555231ec2a68de8b15563ea4efd38e69868fa08467251e8d99bfae; exit codes [0,101]
- Diagnostic original-parent-reference.json file SHA256: a9c09fa10e69b57945a449105db2a806b0df13b5dace08c8cb01043f7e12391a; exit codes [0,101]
- Diagnostic summary.json file SHA256: 847afa1771540eae110a5f085e132cf2533a6514d40a0761d5db6f63b06d2bd0

### exp-v1-recovery-r21-rust-generation-0071

- Original parent canonical: e2ceb1e16802116fff5a7b828b4a01b13ac7c996d841f293fdca978b0186610d
- Candidate file: b012dc09376f48f523d072ff73a6d8adc5ca9c53a36c64a7800576bbf3229fd8; canonical: 0dd61fcc0a99305c1099c38d9018b46bd473c4b81ef7bb85ff89740d8c264528
- Prompt: 05eafc417f3fb179645df8c7d9d0a392da3960b35d150ebb725972c93036369f; answer/reference: ab92319cc02461717e1bbd067cc0d5223de949a2aa19d141bccd688b022922b2
- solution_test.rs: 9179d07c12b2cb211b773dec8278ae18b6770a9aff973ebf22a1a3f5a1f571d3; known-bad: 796201a2fa2a8e706ceb32add9d0c607149d7c2b860cf1cd5a875c331d4c64e0
- Source: {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-05827","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"70cd4c936746caf3958edcd46ad96d982d28dcb01f575a5b63799969bdef7680","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r21-rust-generation-0071 from exp-v1-rust-generation-0071 sha256=e2ceb1e16802116fff5a7b828b4a01b13ac7c996d841f293fdca978b0186610d","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Diagnostic reference.json file SHA256: 2c1f5504c6c7ac795aef8e241cab5267937d9abd654f16038c95158e25f19807; exit codes [0,0]
- Diagnostic known-bad-0.json file SHA256: cec1e54d832cbaf9222c108cdd22b1f51489a7f19d75a780bca5385f59ba4ca7; exit codes [0,0]
- Diagnostic original-parent-reference.json file SHA256: ec8855531dc75d958d4f38774c36e3c84327f620adb20636221a1fbdc7558880; exit codes [0,0]
- Diagnostic summary.json file SHA256: 87a23866c7cd61cde4cbbf397fe5fd7157af813b8499d3330f32c8163394c574

### exp-v1-recovery-r21-rust-generation-0111

- Original parent canonical: 42d67460786da429421d42ac674375082c1cedd18823e1e323eb0b9a903eaed2
- Candidate file: e87c9dff9163a6bd41d08423e6f5c8bb92efd0089340918a9bdba0350df3cdae; canonical: 6c3941bee54dc25b3f559d856309d6341a8204f6199a467ef4e4768fe943c67d
- Prompt: 1060062f0cd123e7e9ffc62f6fa76fb5893539e1aacb621da2fd3a0859f8b502; answer/reference: 3c5f21f3a690b2ee300ef2064b223cd3210ee98aaac485276af90a26b165b32a
- solution_test.rs: 6de83f003c6b05bab900ec6bc69eb6489ba1aa4887515231cca2285ddaaad231; known-bad: 720420c227e306f3c319b1d00daa9e23657b6a07e5ae10596c48682134e1a448
- Source: {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-05889","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"9634d380340030a875384b7bb095738072a6fb2940c7d961b227f25e00f67e4d","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r21-rust-generation-0111 from exp-v1-rust-generation-0111 sha256=42d67460786da429421d42ac674375082c1cedd18823e1e323eb0b9a903eaed2","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Diagnostic reference.json file SHA256: 27eafdfe896e5f5cb6ab55f03317910a8a094484dca1c4b8440604661e54a2cd; exit codes [0,0]
- Diagnostic known-bad-0.json file SHA256: 2ebf5b4b855180703da68fd7b226a2ad0051315cf821ddd971e620e6ef3f0b1d; exit codes [0,101]
- Diagnostic original-parent-reference.json file SHA256: 7190c71788819a32bd787665f37294580d7ec738e99c6ff2c237b4e9c0a26d47; exit codes [0,101]
- Diagnostic summary.json file SHA256: fd267b3c9891f0b871bef7a832bf71921f38005a8b7ef0da62be1944d95f3914

### exp-v1-recovery-r21-rust-generation-0342

- Original parent canonical: 9130d034eb347f9d19e8bc8c67f68b7c018b6f6e6d4ee2a3cdc22b4997652634
- Candidate file: 1315ce39eeb2e4c0ca7c67a4169c6ee42c3401ebb16ace023409c76e86cc0f4c; canonical: 23aef207a98b3291deafda2ec465dd4e2b8c7e45dfdaa880390d4bbd600aeffc
- Prompt: cfc34b2f401dcb7dcac891b908e006ebf8d55ba67e56f6ce4985f7f7a9f9e716; answer/reference: 59e3282678fefdd3753f8890ea09fb37dcb3ca08927c8b3b865079a3f5170015
- solution_test.rs: 02d7afad7c9410bce18f57af12637e204d89cf3b60592fc8df6ee14d24841ec7; known-bad: 5d53db9ba1640224a23c2804951892debb2a8439130c2845d5db0b2f01a745a3
- Source: {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-23810","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"bd320d0d81e852d74fc42a3f595ccf4779d6532d470f21a9a9ae0a46daa3c4ac","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r21-rust-generation-0342 from exp-v1-rust-generation-0342 sha256=9130d034eb347f9d19e8bc8c67f68b7c018b6f6e6d4ee2a3cdc22b4997652634","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Diagnostic reference.json file SHA256: 27ca771c8ce4ae4eb3fd5bb334430755977d9816870f98e8f0af7292f6669690; exit codes [0,0]
- Diagnostic known-bad-0.json file SHA256: 4c9b994aa2d9f5ee8c491cf5dcf0891672498a7de8b6d076fda5cccf5bf00dc0; exit codes [0,101]
- Diagnostic original-parent-reference.json file SHA256: ae205e61f39e196735cb97570ca4d5cb9795a35d5afaa40ee2c244347190f4b2; exit codes [0,101]
- Diagnostic summary.json file SHA256: efc69c379858f11b941aa1ef02d9149938c6f3638e467200c89ca810c4831d8c

### exp-v1-recovery-r21-rust-generation-0414

- Original parent canonical: 967630134b4366dd6f569a3c43333edca71f3912974b87248f183a157041d60b
- Candidate file: 492e2c0fd22b9b83575724ee4ccbbe4c650c8b0adef6b6a70728d55f46e561a1; canonical: 492c4ad2c31b9d5e55d864a005d810d4607e6c833bccb7ec778c715c824a4d88
- Prompt: ff7e586ef0f78c6ffe5ea1a6ef4073cce4a295ceeb4baecf7b9e8ce371fd5124; answer/reference: 3adc4edc1ef15018c39712948b7a8a27b9db9521e2322a24879df827cc7620b1
- solution_test.rs: 6a0e5f47a7d83e25a17e8f14bb51b15efc61d95d547579bf2afad7db4838b3b9; known-bad: fbc9d845901b84dccb0b79fc08537a565005edba6b996ca96e72ee3f2a5bb21d
- Source: {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-23808","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"a3bd7801d03dd4ee5860d6223ca12f96388eb694a2b821f77e6e44493fb29417","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; versioned recovery exp-v1-recovery-r21-rust-generation-0414 from exp-v1-rust-generation-0414 sha256=967630134b4366dd6f569a3c43333edca71f3912974b87248f183a157041d60b","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Diagnostic reference.json file SHA256: b449a6cc1be5f617787c9b7462630a3ea21d9d78ff2db8c026260d5b63aad325; exit codes [0,101]
- Diagnostic known-bad-0.json file SHA256: 0a11d22b3414db27b68bdc440885eb0ff0f4b13c3625a3bf1bddf3142151ebb2; exit codes [0,101]
- Diagnostic original-parent-reference.json file SHA256: 970c5730666c5eb527a9c946f21063893ecf30b88d6d0194ff4b5f5df678c3cf; exit codes [0,101]
- Diagnostic summary.json file SHA256: 4df170fd5e1e05022bad9305bbf3e22794a89fcb69d5b7f274849c4798e731a4

## Author provenance

Exact six IDs and all architect problem/reference/mutant contents match candidate fields; independent test final items match complete candidate tests. These checks parsed and hashed data only. No tests were run by this reviewer.

- rust-recovery-architect-evidence.json file 06b454955a944f018513fb15514a65fb9ddf91ebe2f55cee0e21ecbcc03c305c; prompt a25f2941d7fea4b66d199d8f8815a9a980a9300c63e0afca780289313c4d8ee8; final_output 35ed23a13abe7879545b11a415a13fb2f2a63eefba27619f50c929024f70e9ae
- rust-recovery-independent-tests-evidence.json file 6665cc7e8d0a8fdb3d3fc1f8c06e008af6bd4a5c48f10c056893a572823b1581; prompt 96846d9e168529a8cff986c0cdf57dd68ebf86df3fc4cc60f7948aff5c8a151e; final_output 3c383400a82c573c94ff43bc95ef5bd3af01dbb0290fcbde54d78a40029de798

