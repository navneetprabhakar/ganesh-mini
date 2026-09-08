# R21 Java architecture failure and provisional R22 retry — 2026-09-08

## Main-approved extension: terminal Go lane, combined R22 scope14

This section supersedes the Java-only retry count in the original analysis below. Main confirmed Go failure and requested the combined draft. Main's prior classification mistake was accepting reference-fix for repairs that require replacing their embedded broken source to isolate a new mutant. The selection rationale also contributed to that incompatible combination. This is not teacher failure alone; the exact guard prevented inconsistent training examples.

Go terminal go-failure.json reports the same ValueError. First failing Go row is repair0048; all three repairs0048/0180/0233 fail embedding. Generation rows have no embedding requirement. Generation0218 legitimately differs from its original prompt under approved contract-clarification; all other Go problems preserve original bytes. No Go independent-test evidence or Go candidate files exist. Combined retry is exactly Go8 + Java6 =14 incomplete original parents, with8 repair classes changed to oracle-rebuild,5 generation reference-fix and1 generation contract-clarification. Other lanes and any completed artifacts are out of scope and preserved.

Go mismatches:0048 embedded <= tie replacement differs from returned < signed-width mutant;0180 original divide-first source differs from quotient/remainder overflowing multiplication mutant;0233 wrong sum denominator differs from float-before-subtraction mutant. All are substantive source differences.

All behavioral prose/API/domain/error/ownership rules remain frozen for repairs. Only embedded broken source is replaced; stale nonbehavioral diagnosis must not contradict it (notably Java0460 floating-point sentence and Go0180 operation-order diagnosis). Main should approve neutralizing those diagnostic statements, or choose a compatible mutant; this is not permission to alter behavior or relax guards. Fresh exact R22 IDs must come from the teacher, not renaming archived R21 items.

- datasets/cache/expansion-v1/versioned-recovery/r21/go-failure.json: 95716d1092c62e418247d0ae89ca7fb2c3009ad2fa50ec403f601a1d560ecfc2
- datasets/cache/expansion-v1/versioned-recovery/r21/go-recovery-architect-evidence.json: f58ab127e93460b35a799068271d4d0c9cf44021e8d7760efc50d5e928dbd752
- Go architect prompt SHA256: 61a8d60dc30613b8e327703e768439378eec47574d0293ddb18fb090fd6ee7d4; final_output SHA256: 5e16f8bdc8a047cea7945469ebcbe8f8c0ac8f10675594c8a567ad556279b24a; returncode 0; timed_out false. These are author statuses, not code verification.

### exp-v1-recovery-r21-go-generation-0027

- Parent exp-v1-go-generation-0027; canonical 3fca5e99057f8713a19a8bbe37827effe22c5ff22c04366cf98a656cb31dc0ac.
- Raw architect item canonical cbf5fb2f4f561a361a46d7ddcc1695e51fe9ee0c63900945431f8d9d2bca752a (not candidate hash).
- Problem 96baab03bcc8a98fb487b72346b5bd9403d39830360085dedf711aa2273691d6; reference e0998a6f6e31fa6fb9009d361fac221e0354b2ed8c52a8ff5b5bd33c3972530a; mutant 28f492a8bab7648a3127dfa2c529b0e0a999b815ddc1ea6bd75d282eecba0af0.
- Original-problem equality true; embedding not applicable; completed candidate false.
- Source {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-16164","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"1a9ed05364034dc652c7173ba9e7edc1cae10da0379ad88a4e890126c67ecea2","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Prior approved evidence measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.

### exp-v1-recovery-r21-go-repair-0048

- Parent exp-v1-go-repair-0048; canonical 750c4daa922b861fd2013145a76364da01755ac8c61c1fa092e4c0cb950392b5.
- Raw architect item canonical d9ebfc062af0669bab56ab1f1ef6c9569e5abadbd6ad27bf2b0ca7eaf7f28f48 (not candidate hash).
- Problem 9e74c345b7189df709173547e1520dc4d19f541fb8d69e29534a7636585ed71f; reference 384727b7c8fa361983f81700ab8a4388c014e59399a750843c8cd796de6eedd8; mutant 3ce1f3020a7f2827e65ce864fbd79c0226aeae322db0012c769af26785e9d364.
- Original-problem equality true; embedding false; completed candidate false.
- Source {"dataset":"m-a-p/MdEval-Instruct","license":"MIT","license_uri":"https://opensource.org/license/mit/","record_id":"row-00314","revision":"38c9197e3add996fae624eb198ebd06155b2101e","source_record_sha256":"a359818cd6f9e35da3cb1d15ca4da60ed09578855a0c542c8606bb39c11ff9cd","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/m-a-p/MdEval-Instruct"}
- Rights {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Prior approved evidence measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.

### exp-v1-recovery-r21-go-generation-0095

- Parent exp-v1-go-generation-0095; canonical 179863828385f6d0259eb99b885c38820d13b3d8c6844f45620e3dc9cb03e573.
- Raw architect item canonical 0dfe1a32d3d70ff05fa417f9c40073341b237a861edaaf68b15cbee5021f8545 (not candidate hash).
- Problem 2f7bf5287781a5534abc28810d82ad1a362684773c16c930bdd183720612fcce; reference 7e415a2ad06ce3e05a585e172e04a3c04f8bfb693d86e7c8c566f35877fb6385; mutant 2a90c42f289d23776b99bc269be123dbc93c957f0707c06f92e6ae06b8a4f55e.
- Original-problem equality true; embedding not applicable; completed candidate false.
- Source {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-27736","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"f5aa52ee5881c9450065352f784eac6d229abb418c6c0376d1071e089df5bdf2","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Prior approved evidence measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.

### exp-v1-recovery-r21-go-generation-0121

- Parent exp-v1-go-generation-0121; canonical 748e3d3563c5167ffd6fcbec801b9191aa48a4b28d852a5dcd78b1c5ff6e721d.
- Raw architect item canonical ad82e1a19e7a1ed162b5bdddc27d8d12334624750c506c369bff293fc9ee8cf8 (not candidate hash).
- Problem e289568f43c8807df18d1cb48eff6990c09fc769933c5aa58d1b4ee8b80fdd42; reference 5aaa3bbae6c0bfae235ca43a78c291507e2438d4934eb6081f9c6382c807af97; mutant 10c11a44d5e7c61744d31abb58010b7771558543fb4ee074407073144014fecb.
- Original-problem equality true; embedding not applicable; completed candidate false.
- Source {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-27755","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"7c070187bd90893cde5d662efe2f622ce5aff653ff3ebd40a2f4267fbacc8a6f","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Prior approved evidence measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.

### exp-v1-recovery-r21-go-generation-0218

- Parent exp-v1-go-generation-0218; canonical 9e86e83b0e915ce72b597e18fa741ba566dc55109e2b1b951245c55ca4dfcfc7.
- Raw architect item canonical 8d3786388d81ba8e75791e7440b33b695a95db94e4a53c24d16bbd9235daa906 (not candidate hash).
- Problem 72b1e10f1de81978d9bf8ffe2f9fbfee79bf762c026ab0ab6de80f80660cb491; reference aba83100a5b4bfc8edb6657fd7fc10b70dd2e3b3b9bb12d71adbc3ed027345d4; mutant 9bf53b08de206935c55faf56b824f67c0575a713e35391d32227be5392e35203.
- Original-problem equality false; embedding not applicable; completed candidate false.
- Source {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-16417","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"2bdf1e2757b3bb800b3caf52479e9585f8993d1fb6810215b1ee9c574b6ec4fb","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Prior approved evidence measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.

### exp-v1-recovery-r21-go-repair-0180

- Parent exp-v1-go-repair-0180; canonical 7b5faf2fe549940745ff9bab52fa3bc710b837ce12d956656ff511a5648e6112.
- Raw architect item canonical 291cb0343c88a7f1eec9d35ce125b9934445302ae2edcb07cf05bbd13d0af3dd (not candidate hash).
- Problem 1a91ee508c0b25058de5ae7b883cf7434ae3fb52a60a2d475fcba32a01d3a9b3; reference 852b46082e5cd3f931f7ba1a72424133243783b23e428e72b34927f76afd2a77; mutant cf4fdbd2ea95fa927b5ae62d5b8ee7dc444ea509017e15c925f94fe67bb8cf69.
- Original-problem equality true; embedding false; completed candidate false.
- Source {"dataset":"m-a-p/MdEval-Instruct","license":"MIT","license_uri":"https://opensource.org/license/mit/","record_id":"row-11216","revision":"38c9197e3add996fae624eb198ebd06155b2101e","source_record_sha256":"ade965862f69231d186a52f7fe4929c39946818a77eee9b7e5718f779440ac86","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/m-a-p/MdEval-Instruct"}
- Rights {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Prior approved evidence measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.

### exp-v1-recovery-r21-go-generation-0280

- Parent exp-v1-go-generation-0280; canonical a3e286b919262fbae3b53571ec92273fb0df3a94d347c153277c09f0fff9d39a.
- Raw architect item canonical 04e483d3133aafb40f7ce9f2c4ccea10910262a72bd070b244818f799fc73ab2 (not candidate hash).
- Problem 4c13666bb4ca43e61f0ee911475426a911b30eb600029165d0467852bae067c0; reference e05fdae5feda2c1908058b182b141eb6a28e4d18d84c7384e01ed78735a7ae3a; mutant daf0854bbc80ad5e57ba9be7155e2617cf1dc63eca2c87d96f36c5135d681297.
- Original-problem equality true; embedding not applicable; completed candidate false.
- Source {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-28009","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"bcab7a773879d76851c2be5e4d8092c6a9a4b84a70f04f92246616faf3d3bec7","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Prior approved evidence measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.

### exp-v1-recovery-r21-go-repair-0233

- Parent exp-v1-go-repair-0233; canonical 353fc94add0a23ae2f54cdee93f18fc3d68ca42b298cbb0e7239d595237cdf6f.
- Raw architect item canonical b373c3cc2a174ef893355fb49e6cd51703615fccc8cee33c2c407ef5707162f2 (not candidate hash).
- Problem 2d41b1902e19fbb06df8a612b49ce7ed5de88408c4c666eadd354d04b0f98b67; reference cd85134ad44933b3a730476009a344a47b64a77d015f77265a54d748dab2ad18; mutant 835f04dc3397ef829b5fa314e161e72086f2750be222f29ec5c15efe0ea0ac91.
- Original-problem equality true; embedding false; completed candidate false.
- Source {"dataset":"m-a-p/MdEval-Instruct","license":"MIT","license_uri":"https://opensource.org/license/mit/","record_id":"row-00779","revision":"38c9197e3add996fae624eb198ebd06155b2101e","source_record_sha256":"b676eda5236fc21bceb7add437cb7f764b8a901279e1ef35caf5c6897b1fe096","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/m-a-p/MdEval-Instruct"}
- Rights {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Prior approved evidence measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.



## Finding

Java lane has zero completed candidate files and no independent-test evidence. All six planned IDs are incomplete and eligible for a proposed fresh architecture retry; none is salvaged, renamed or admitted. Archived architect returned0/timed_out=false, but that is generation output, not a valid candidate or execution success.

The guard first fails at exp-v1-recovery-r21-java-repair-0065. All five repair items fail the same exact source-embedding condition. Generation0026 has no embedding requirement and passes the frozen-problem comparison. All six returned problems equal their original parent problem byte-for-byte.

Root cause: reference-fix freezes the original complete prompt including its original known-bad source, while the approved rationale requests a new isolated held-defect mutant. Architect returned that new mutant without replacing the old embedded source. These are substantively different sources, not merely trailing-newline normalization. The guard correctly rejects the mismatch; retain it unchanged. The loop validates every architecture item before any Java test author call or candidate persistence, so even the unaffected generation item did not complete.

| Repair suffix | Original embedded source | Returned known_bad_code mismatch |
| --- | --- | --- |
|0065|integer scale division|double scale/floating floor instead|
|0075|unmodifiable wrapper over caller list|ArrayList snapshot added, leaving contains(null) defect; imports/spacing also differ|
|0401|missing collision rejection|collision guard added, leaving full-key validation absent; formatting also differs|
|0460|Double.parseDouble conversion|Long.parseLong conversion, leaving -0 acceptance; spacing differs|
|0464|startsWith opener|equals opener, leaving character-length separator bug; braces/spacing differ|

## Provisional fresh retry route

Propose recovery-requests-r22-PROVISIONAL.json for exactly these six original parents. Generation0026 remains reference-fix with original problem byte-identical. Five repairs explicitly change class to oracle-rebuild so a newly versioned repair problem may embed its exact new known_bad_code while preserving the original behavioral contract and approved correction scope. This is an architecture retry, not correct_recovery_tests, and not an attempt to bypass frozen-problem checking under reference-fix. Main must approve this explicit class/scope update before launching.

For each repair, retain all API/domain/error/ownership rules; replace only the embedded source and adjust any stale diagnosis that no longer describes that source. In0460 specifically, prose saying the decoder currently uses floating point must be updated when the new mutant uses exact Long parsing but accepts negative zero. No runtime behavior is thereby changed. The new complete known_bad_code must occur verbatim inside problem (as checked by known_bad_code.strip() in problem). No independently reconstructed or manually patched R21 candidate is proposed.

Preserve all approved tiny witnesses in the R21 plan. New independent test authors see the new problem only, not architecture answers. Generation0026's archived mutant uses Integer.parseInt without retaining lexical checks for sign/non-ASCII digits; this is additionally broader than the intended isolated int-bound mutant. A fresh mutant should retain the correct ASCII canonical grammar and slot closure, reintroducing only the unnecessary machine-int bound. This observation does not create a completed artifact or change its original held scope.

No reservation, generation, sandbox execution, source repair, raw mutation, guard relaxation, central changes or new coverage occurred. Before main launch recheck that no candidate unexpectedly appeared and exclude any actually completed record. This Java terminal failure does not invalidate intact other lanes.

## Exact evidence and lineage bindings

- datasets/cache/expansion-v1/versioned-recovery/r21/plan.json: a5fe5bbb1cffe149091f626ed317a0e79c39985c10c883acd8f83df3c04582ca
- datasets/cache/expansion-v1/versioned-recovery/r21/run-contract.json: a455daccb7e85a30c3cc86d4c328ee44be8e6fd166afef6fe685bba9c8225be4
- datasets/cache/expansion-v1/versioned-recovery/r21/java-failure.json: 930dde697bbe7e0e0656b45ec2d8cb49e7328a9d99ee4a5fd12e2b614bff849c
- datasets/cache/expansion-v1/versioned-recovery/r21/java-recovery-architect-evidence.json: c4404d032be0c222f6bb744973b91dc037287c1ba87c5dc355a3162718ebb73f
- scripts/data/generate_versioned_recovery.py: b4f5e87c34bd2a736680778ee7724f8c9e3b2a19a80af44b7fb6f74005fd725e
- Architect prompt SHA256: b55b395af229331d0a51fe0fcef363465b44fe64804ad616df0e71b362251794
- Architect final_output SHA256: 0737a19237f17f8441f269f1d53efbdbd534667aa93b184f2d4ed8a0fc5d28cf
- Original corpus SHA256: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec
- Frozen hold ledger SHA256: 9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee

Original parent canonical hashes were recomputed and match plan. The item canonical hashes below bind raw architect objects, NOT candidate hashes (no Java candidates exist). Source and recorded rights remain those of the approved plan, not new legal conclusions.

### exp-v1-recovery-r21-java-generation-0026

- Original parent: exp-v1-java-generation-0026; canonical SHA256 0534a85b6da9497118cb55f2e8f05bbfba9aa4e4f0eb626cf714ea0e4c4d8884.
- Raw architect item canonical SHA256: d686a06dc0ae2b84c468d0ce2bdd9bd402d3fd00c5b6e621b91c85dccb6bfa61.
- Problem SHA256: 82a167b3147c36c0e7be0654e88ec6f2c9da27a85f62b7c689eb626fd1603bb9; reference SHA256: a9c763653afd7cd106dc310b9d7f6c9a23fbab104067cb35a9bc1a239604afa4; known-bad SHA256: 951437e2a7dd6da0223adcdb9d84c28ebbe5d7f20c0363f0c780f0b5c42caa96.
- Original-problem equality: true; repair embedding: not applicable; completed candidate: false.
- Source: {"dataset":"Multilingual-Multimodal-NLP/McEval-Instruct","license":"CC-BY-SA-4.0","license_uri":"https://creativecommons.org/licenses/by-sa/4.0/","record_id":"row-28204","revision":"57bd46727e49ac3e2890218a146d35c2454a8496","source_record_sha256":"ca9c0668735ab216ff80d8c898379935316b6e9941594001b78d3d846ce98ed0","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification; reference corrected against independent tests","uri":"https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Approved scope evidence: measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.
- Original hold evidence: measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_4.md; reason Static hold: canonical numeric node tokens have no int bound in the prompt, but validToken rejects 2147483648; the valid tree 2147483648,*,* is rejected.

### exp-v1-recovery-r21-java-repair-0065

- Original parent: exp-v1-java-repair-0065; canonical SHA256 c34d1c5d2b3f003ffea1c853e8dc04f86613d318364859a05b61f9b63688f065.
- Raw architect item canonical SHA256: da4f86c5dfea7119c65a489a2d346b1071d825fad3b46ff40bc27940a5282f94.
- Problem SHA256: 38ce365fd27849c957bec9fd8f1694a814f6f0f0a2b3f16b5b7a65a72f6825b0; reference SHA256: 4bae81d5a85dd5808209974f131542012068609dbc201f8b08235dc7c98b4420; known-bad SHA256: 7f23bd6cfac60a7749e16d684a0064e2056882887bc88d558608a09b97b4a922.
- Original-problem equality: true; repair embedding: false; completed candidate: false.
- Source: {"dataset":"m-a-p/MdEval-Instruct","license":"MIT","license_uri":"https://opensource.org/license/mit/","record_id":"row-10884","revision":"38c9197e3add996fae624eb198ebd06155b2101e","source_record_sha256":"a2ffe7305badc421b558e313f5945f22cf347d8d9e6181900d8b05b4a223277a","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/m-a-p/MdEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Approved scope evidence: measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.
- Original hold evidence: measurement/data/expansion-v1/cutoff-5885-review/java_repair_0065_exact_floor_probe-result.json; reason Executed hold: fitSize(100,100,29,29) returns [28,28], not the exact-floor [29,29]; binary floating rounding changes the required integer result.

### exp-v1-recovery-r21-java-repair-0075

- Original parent: exp-v1-java-repair-0075; canonical SHA256 7f843f49c9d9925480529ce3eac1047552fca5e2f28293d9e4403c3e3f617556.
- Raw architect item canonical SHA256: f88494c4a5c5c7e61b71833d2efdc28bff3fe9323e7c96789a9a9d70a00c4c5d.
- Problem SHA256: ce3949843d26efa4e066a9761c4940ec71439386b514bac373af6b3289e6f302; reference SHA256: 5c8f5789a5b3f5dc3e757c9fe5eb09168ccf754687a04b64ed62e7c3af91fc46; known-bad SHA256: cb900a08061c487afb49b27349e53b24450d540e297405f064d464f9fd51eefe.
- Original-problem equality: true; repair embedding: false; completed candidate: false.
- Source: {"dataset":"m-a-p/MdEval-Instruct","license":"MIT","license_uri":"https://opensource.org/license/mit/","record_id":"row-09982","revision":"38c9197e3add996fae624eb198ebd06155b2101e","source_record_sha256":"49a965fee739dffecbfccbfab49ef5a95cc5402a7bbeaa0db2200b47ae1ecb95","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/m-a-p/MdEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Approved scope evidence: measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.
- Original hold evidence: measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_11.md; reason Criterion-positive nested-list snapshot repair; static hold: source Map.of("x",List.of(1)) throws from contains(null), rejecting valid immutable list input.

### exp-v1-recovery-r21-java-repair-0401

- Original parent: exp-v1-java-repair-0401; canonical SHA256 c4d8ddefa4859653bc409279ab5db7cc83cdb24d68f788d33b1ec930831dbf9f.
- Raw architect item canonical SHA256: f17473ec76efd6036d82954be11fc2fe58b0a01669161981c484fcb93444f400.
- Problem SHA256: 227dec471d003144c6edc873631f595cd9f404ae5d4a355f00dc5400f84850b7; reference SHA256: 6794278c35458a74d3076245024a41cee018227e2d5241ab7c3426a1a7bcd909; known-bad SHA256: 6022bfdf60519bfebc06857bdf6bd53ceac1ee8cac2380d483408e7503a0d604.
- Original-problem equality: true; repair embedding: false; completed candidate: false.
- Source: {"dataset":"m-a-p/MdEval-Instruct","license":"MIT","license_uri":"https://opensource.org/license/mit/","record_id":"row-12432","revision":"38c9197e3add996fae624eb198ebd06155b2101e","source_record_sha256":"450b4f119dd3fc8460d37ff6b217a516794ce24008c366c8f52b4a0f3dc8780a","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/m-a-p/MdEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Approved scope evidence: measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.
- Original hold evidence: measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_57.md; reason Static hold: required validation of null/empty existing row keys is absent, including no-op/absent-source fast paths; actual rename can dereference a null key.

### exp-v1-recovery-r21-java-repair-0460

- Original parent: exp-v1-java-repair-0460; canonical SHA256 1b7dccfae15207310d49be2af3b5916aff29f6c55ac89b64eeb614660ac41182.
- Raw architect item canonical SHA256: 7a6844309bf85f7c65b74c1077f7884ab10d16ac68350bf34cff83de9da324d9.
- Problem SHA256: baf1dda0231a74b6d349e406d460485c2f0c7b507559c2a58b735b999c8f804f; reference SHA256: 1f4c3a9af90b4003e5be0657a16759e148914f2207533c6a8ca76011f15b7728; known-bad SHA256: 7e1ffbe4059894687d44d5832ddea7744714563ef45673cad023c020f8658697.
- Original-problem equality: true; repair embedding: false; completed candidate: false.
- Source: {"dataset":"m-a-p/MdEval-Instruct","license":"MIT","license_uri":"https://opensource.org/license/mit/","record_id":"row-11843","revision":"38c9197e3add996fae624eb198ebd06155b2101e","source_record_sha256":"85fd71077decc1963d8b90e139f7aa5cc72987c0412f850ed0b2ad00a741a7ce","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/m-a-p/MdEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Approved scope evidence: measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.
- Original hold evidence: measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_65.md; reason Static hold: canonical predicate still accepts explicitly forbidden -0, which Long.parseLong decodes as zero. Not executed.

### exp-v1-recovery-r21-java-repair-0464

- Original parent: exp-v1-java-repair-0464; canonical SHA256 fa8d34215fe2836c1f6e49d6fd40bdb900ed86ec10fd685f9ea760c1bada280c.
- Raw architect item canonical SHA256: 339db5bd7e43aa2f14731e842ca1e61d77be554ecb15241e536cdb85a000d2cf.
- Problem SHA256: 0f014ce2059b52ee96ebb5b13115f108e22de864a137aca321952b4f8fc9f68d; reference SHA256: 063570f583a9f610b989930623467a5c15e3b7db60d0a40f3befbf0be3823580; known-bad SHA256: a95f9a5290e07417751f84bc130c1eef0716ebf0f02698d4be7de75130e323ec.
- Original-problem equality: true; repair embedding: false; completed candidate: false.
- Source: {"dataset":"m-a-p/MdEval-Instruct","license":"MIT","license_uri":"https://opensource.org/license/mit/","record_id":"row-08055","revision":"38c9197e3add996fae624eb198ebd06155b2101e","source_record_sha256":"dfac8640df86d1e6e84375ad183965c1906bb26b51980cd1025a9e96d85f1b46","transformation":"Codex teacher creates a new self-contained task inspired by this drafting stimulus; source answers/tests are not trusted and independent tests see only the transformed specification","uri":"https://huggingface.co/datasets/m-a-p/MdEval-Instruct"}
- Rights: {"answer":true,"model_training":true,"prompt":true,"redistribution":true,"tests":true}
- Approved scope evidence: measurement/data/expansion-v1/cutoff-5885-review/RECOVERY_NEXT_GO_JAVA_BATCH2_20260908.md; SHA256 7bfe39355de78bf5b35741043cb341e38b9b86c49e0ea3df278c021837f336c6.
- Original hold evidence: measurement/data/expansion-v1/cutoff-5885-review/JAVA_FOLLOWUP_REVIEW_65.md; reason Static hold: newline joining uses character length as an interior-line counter, losing initial empty lines; opener, empty string, x, terminator yields x instead of newline+x. Not executed.
