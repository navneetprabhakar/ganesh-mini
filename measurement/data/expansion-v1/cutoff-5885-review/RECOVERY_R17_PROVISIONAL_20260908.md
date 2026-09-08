# Provisional R17 JS/TS test-only correction — 2026-09-08

Gate 2: exactly 13 selected original parents, seven JavaScript and six TypeScript. Positive TypeScript0267 is explicitly excluded. This proposal does not reserve r17 or launch generation, execution or a critic. Main must validate and approve before launch. All originals remain held; zero original-coverage credit.

Read correct_recovery_tests.py and the r13/r10 request-feedback conventions. Request entries bind original parent canonical hashes; feedback keys are the proposed r17 derived IDs and bind the previous r12 canonical candidate hashes. All 13 previous candidate hashes were freshly recomputed, not copied from file hashes. R12 has no correction_attempt, preserving eligibility for one bounded correction only; a failed correction does not authorize another loop.

## Correction boundary

Every r12 problem, reference and supplied mutant must remain byte-for-byte unchanged. Feedback contains specification-derived witnesses and oracle repairs only, no reference or mutant source. Preserve independent correction origin and raw outputs. Source/rights remain governed by existing parent bindings; no ownership decision reopened.

JavaScript0001/0003/0009/0012/0173/0233 gain actual sparse-array witnesses; matching valid prefixes are important where a later lookup could otherwise throw incidentally. Recipe tests also cover raw blank-but-nonempty keys/ingredients and remove unsupported Error-subclass exclusions. JavaScript0391 removes its leading reflection check while retaining direct returned-Promise/no-synchronous-throw/zero-side-effect validation and sequential/error identity behavior.

TypeScript0036 removes the unsupported safe-integer language cap and adds valid-address/invalid-metadata Promise rejection. TS0078 tests hidden required fields while accepting hidden extras; TS0148 combines duplicate email and invalid accessLevel ordering; TS0228 uses actual own __proto__ data and hidden own values without a returned-prototype or descriptor-flag oracle; TS0300 tests year0099, sparse records and non-enumerable required id without settling year0000; TS0345 tests blank amend and drop with one actual U+0009 TAB.

The TAB witness is specified by Unicode code point in prose so a critic cannot confuse JSON escaping with a literal two-character backslash-t input. No VT, year-zero, new metadata domain, new error subtype, private layout or global resource policy is added. Existing valid tests stay unless an exact unsupported assertion is explicitly removed.

## Immutable aggregate bindings

- Original corpus SHA256: 680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
- Hold ledger SHA256: 9dce318a6736c8dddd9f21722a13a59094ec98219354cc697feb5807439c5eee.
- RECOVERY_R12_JS_TS_REVIEW_20260908.md SHA256: 835852a52c537556c37389b692902bb8a48e2552a80d6d01e6baad2a7ae2cefa.

## Per-candidate immutable r12 bindings

All previous candidate files are under datasets/cache/expansion-v1/versioned-recovery/r12. Canonical hashes use sorted compact UTF-8 JSON; file hashes use original bytes.

### exp-v1-javascript-generation-0001

- Proposed ID: exp-v1-recovery-r17-javascript-generation-0001.
- Original parent canonical: e2cb4a2b43b8771f3913856f4bd0b83e4999e0bef3a35f3b87a131c253fce467.
- Previous exp-v1-recovery-r12-javascript-generation-0001.candidate.json file: ae33f6ddb4aa73a344fdcb79799b8580f4aa16c32328db1df587bb552769913d.
- Previous candidate canonical: 370cb0f02e5f977a509b3381f9f52445a4db114fc4d126560e44f47e65feccb8.
- Frozen problem: 6d2da714ba09359b00eb6581c8cc4f338a78e6ca91224518002cc3468a91a1d1.
- Frozen reference: 24bed6d7e511c9f0e441e2960dfa791ab9aa6e9e1023289d5c13f77915d8011e.
- Frozen mutant: c2ad039e7031edf592bb811f43af1941b051b583878414b514dc918a86d34bd2.
- Previous tests: 218efef3fc80fc5acb48b8b73c5cf76ec1b507ba6230b3af85544d69510716b7.

### exp-v1-javascript-generation-0003

- Proposed ID: exp-v1-recovery-r17-javascript-generation-0003.
- Original parent canonical: 9f132a9b64779cc059a7128ee5b06c41397250ec70a7ad464bb008ef48189b88.
- Previous exp-v1-recovery-r12-javascript-generation-0003.candidate.json file: 92814a8d44a82ad520f365708a5c96061e4b38c3e60cecc69adb1192766541c2.
- Previous candidate canonical: 7902eb11212325caec22c59ac2b59bbfc575ed25a64eb425d466065fd38d7eb9.
- Frozen problem: 35e76a5e44ed84232591fd362cc017348747e039442b00895a5d44e1fe2b3695.
- Frozen reference: 90a187b0fb3bffea1e6662e6b4fe5548f8404deb25b1348aac798887e220a44d.
- Frozen mutant: 09ca038102412cc2fbbb4aef2a8994aa392275a5a364804dc09cf32c8d8d6064.
- Previous tests: 5334dea4e903ecce56f2a21c1f8ea50e3225aebcee856910645a7c1de95fc27c.

### exp-v1-javascript-generation-0009

- Proposed ID: exp-v1-recovery-r17-javascript-generation-0009.
- Original parent canonical: 5ef90228f5f124928ab2ea698baf3d7e52e35061eb8218d4afb950ece4943e45.
- Previous exp-v1-recovery-r12-javascript-generation-0009.candidate.json file: e18966b38f65a33ace365e9a578f42e74c969665bc730b3e89c574825ea08449.
- Previous candidate canonical: 12f41300e930c3389c2e11a9bd0403a340ea24f6e4caa7aabde5804503c7aa99.
- Frozen problem: 7cfed1be26a163c8466fb3e0fcf46d54314bf47d1b16ce3afd7c59fe69534bca.
- Frozen reference: fbef0e7453a59d0dff00160d892c5bae74d3c05d47b3c9c4d3097255af8f815a.
- Frozen mutant: 75686a31f31be7ac4228123a87524f61a92d87f9230df480e6f0fe35eedfb09d.
- Previous tests: a1d3fcb3d761e4b59ea6845c83f7cc66e0723a370795c1c816cead4a8259ce73.

### exp-v1-javascript-generation-0012

- Proposed ID: exp-v1-recovery-r17-javascript-generation-0012.
- Original parent canonical: 87af48b766e695e5938172d490a3fff70a679f58367d9682c07cc10fe932122e.
- Previous exp-v1-recovery-r12-javascript-generation-0012.candidate.json file: b186e8c6fab49d8639238831c3bb41fb96b5bc79c74e18a4abbea4ac434f7163.
- Previous candidate canonical: ffb9119eb445e220248197dcf68a432328e880d59033f0d2e708f38549af23fd.
- Frozen problem: ae49b861e7cafe94b9c4e4901e5b48b2c58a91127e8138b6fc5f12300820cece.
- Frozen reference: 156faaea49704bce06188ecef5f9c59b1e439c16f74cfc88105bb8df12f4b593.
- Frozen mutant: 55b7766a9e68c5951e8a7e474be6d78dcd85379c68d3f5604e1773e74090d345.
- Previous tests: 9e2da08f780485aa05c1da44014d351fe78265de347abce4648e12fef30a095c.

### exp-v1-javascript-generation-0173

- Proposed ID: exp-v1-recovery-r17-javascript-generation-0173.
- Original parent canonical: 7fb4868925a359f15a939f71b88ca3648d79798540f7689c3d510c4bc939dcfd.
- Previous exp-v1-recovery-r12-javascript-generation-0173.candidate.json file: 520a981829bf47a8a2c04077e2bcbfbff14a6592f6c57bcca147d0d7dcfa8948.
- Previous candidate canonical: 7f9119da73f9e927c1d50d50a4ea4757b8340793503d7928b45d0aff995e4cda.
- Frozen problem: 0e4c82d29ce9cdf46b645856797777d6b96549366a9c80934991862a61f418f0.
- Frozen reference: 4961edf7ef37d536a100d6bf47a1428376bf7d2a294fb7009b4cdffeacd388e7.
- Frozen mutant: 2319bd51ffca7a0733b9958cd14f8af79d78c1d466a0e216ca00233dcb5d3ed7.
- Previous tests: f0397495280b494c65caf7343ab18b0935a564b3a379dcb73fa869a0198410eb.

### exp-v1-javascript-generation-0233

- Proposed ID: exp-v1-recovery-r17-javascript-generation-0233.
- Original parent canonical: 46c375e9acebc09156cc8e8a9359b71f02030059fb2e7d3cd200fe0a9795f030.
- Previous exp-v1-recovery-r12-javascript-generation-0233.candidate.json file: 0c638a6a261e7116c86afef383091eb110c06f109034a9253238b4aa6ffb4299.
- Previous candidate canonical: 5df0e23ec790f695d8d2e681225cb2720cbe5458f7aa8261a1f0a4464df20f33.
- Frozen problem: 0c98a23bb40c41f3ab03e557b9d47bd96c9d93c23579e2ccf15206a153a51bdf.
- Frozen reference: b4d60cee510d38525f867ff2e6b8953d20dd34ffc6bab08a6078feb226f1a4e5.
- Frozen mutant: c487592f1fa9483638f9dc57c9b8b3a52c11df2bada4ef4730c8c567fe3a3c44.
- Previous tests: 39a49c74b39b3d84b2a92755d9e131c91e7104db4f90798a6b836e2cf40f71be.

### exp-v1-javascript-generation-0391

- Proposed ID: exp-v1-recovery-r17-javascript-generation-0391.
- Original parent canonical: 23c4d632efca57c66090f4ce698f3ac113fe0a74860beee4c499f88b84205a9c.
- Previous exp-v1-recovery-r12-javascript-generation-0391.candidate.json file: 43bce2288e450ce69cd53b085afcd50ff6ad20546685a4e9fbb5b0d609d9d6fd.
- Previous candidate canonical: d9b0b658b7f7e16cddae3c0d93cbe1730c72fceaaf150f80dd4abc40b5c95791.
- Frozen problem: 7769d9757381c93b4737170f67565461e5bb2eede804f20c03886c7922450528.
- Frozen reference: a399714f082607295d57c240a587fd875c4ae3f9d24bad8de71676dff3393b2c.
- Frozen mutant: a1edec9dca0cae78db783e2032c6ffd76cfd715029083dabe583fd53b2dac493.
- Previous tests: 63a851e6ad154346e887f7381e29fb6f6a63b4a40fd58b9a83e47b9420eb59e0.

### exp-v1-typescript-generation-0036

- Proposed ID: exp-v1-recovery-r17-typescript-generation-0036.
- Original parent canonical: 8972e476c5337d9d93eea39c6398d1678e1563b23fc3db4c6696fcc2867ae185.
- Previous exp-v1-recovery-r12-typescript-generation-0036.candidate.json file: f58dd0ddf5b548f0832a0a104c070a2f80a19c8f201832791d464ea4ad035020.
- Previous candidate canonical: 1e5b726e348eaf8e03e6a94d40bccd462cd437fed21bad801afaf82d6963c081.
- Frozen problem: 585548abc47e31309c840476ff91e73b438bf26c5fc5f0f056df63f45250cca1.
- Frozen reference: b88e54a7821c4eb976c59de1fd4a0dfff0ecbea08e0bf2c4660dd0ab0bc63e4e.
- Frozen mutant: d3e839802541d9bf12fbe98ceadaf422753c5f963183442e4d89d7321ff252b2.
- Previous tests: b2733a0aef0f64cf9f69fecb74b1e52891608fe7fa60a1aa1db0151bddb71035.

### exp-v1-typescript-generation-0078

- Proposed ID: exp-v1-recovery-r17-typescript-generation-0078.
- Original parent canonical: bc13b1006c2e4895e294d759248d64dedf1b02618c6aa5228fa1cda2efe34843.
- Previous exp-v1-recovery-r12-typescript-generation-0078.candidate.json file: 3f66b096b97c7046bb3f95fc635c980f1e14580f7074962ffc1dfec0657bb690.
- Previous candidate canonical: 4a51c3ffc5a78dc90ed56b95c9bbcc692142f7e8c38f39826c382d54d8a5ba11.
- Frozen problem: e3bc968f548a031e362185edf570d63a7f440a9f09c7d94d644fc411029f0406.
- Frozen reference: 361f8a99debb2696133ccca0c7636dd3864a6c90b20b40ba04c75cdb570cd9cb.
- Frozen mutant: a1fb1ac7325854469d6f4350af649949e5874edf5bff8b97b7792dd2f122deb8.
- Previous tests: 66dabb73a070a6a887bb19a08412773ca380ff57a960b916eb4764984faceb12.

### exp-v1-typescript-generation-0148

- Proposed ID: exp-v1-recovery-r17-typescript-generation-0148.
- Original parent canonical: c98c452f81d3b7cf707118e7ae6fca5dc56bf18f91d2d3d817358d678dc53c4e.
- Previous exp-v1-recovery-r12-typescript-generation-0148.candidate.json file: b80f8ce07b0900bac81ab2d28de3ce1ac59244a275de04fa3ad936cedb7f086f.
- Previous candidate canonical: c16a29e263fdd74eddff40899c7d4840a9087b2af32e53563c969c45433ecf19.
- Frozen problem: 29bb13be4a80ce2740873569511d61a836f5c957210ff179dabfe1d3e2321308.
- Frozen reference: 9e2b8422c37e474b6215930c33819797c407900a97654a6100bedb70c7bc4e11.
- Frozen mutant: 97c48cbda4736d192e366eec734a838f94cf9bb20c4e728ea97ae1016c718133.
- Previous tests: a5da80352de34028678df9685dc7c34baeaff3aa759be811b8d0baab56b41487.

### exp-v1-typescript-generation-0228

- Proposed ID: exp-v1-recovery-r17-typescript-generation-0228.
- Original parent canonical: c823a5ec5608671e167047a4b6d9cd8c85c8f5a8c8506f3cd242e34c03e9736c.
- Previous exp-v1-recovery-r12-typescript-generation-0228.candidate.json file: 1a36c4554c49c3723afedbe34c6b645c757953150c042dc8eee240036cea2989.
- Previous candidate canonical: 5cb90b8be179de7906a5fe1d9ab5f15d5268be8c2e8dfec604a0b0b353ac7f51.
- Frozen problem: 8c9b8d6ddbb4bd99d12d71d05147fa07cb79ce6277fabfcb3db6c7440af1d959.
- Frozen reference: b2d8763043f63b15e62e1a273406bdfae05c52049a0f5ef2efea937205da3849.
- Frozen mutant: 4dcd87ff8abdec447442ffa6b424db5d370fb39e615bf6c0bdf94a9f1aaa095c.
- Previous tests: 5a4f21aa5cdeade3b35d80aa9f779f8cc5a58bda381330e3ae4705dea81a72ca.

### exp-v1-typescript-generation-0300

- Proposed ID: exp-v1-recovery-r17-typescript-generation-0300.
- Original parent canonical: f3cfdd59bbe0196a94c80a91a34f282f891a78519ffae45c448f154d35b60f37.
- Previous exp-v1-recovery-r12-typescript-generation-0300.candidate.json file: 71507479c611e74ecf279adb83f0e58aadba04236281db77694e0c1b58a13134.
- Previous candidate canonical: fe47313e0a75fcb670be5727bbfce5e3bd8acd4b6671f680da48dda8e5af5083.
- Frozen problem: b299fbea0dd30181fb9546e50144b724a0906ff50172ba42602b76d67752d004.
- Frozen reference: 70ef35f99d1820eb951a7b681bd4ed9c7d6f0a1f1f00bfd4fd4ddb4750d84165.
- Frozen mutant: 61eadef8a88b9e8022f5e83f11b0682006789ebefa17c8dcffbdfa6a6f1197c6.
- Previous tests: 721349ede8dfb6114ffdb8580524007ed7037498ec5ebc585a19e811db020961.

### exp-v1-typescript-generation-0345

- Proposed ID: exp-v1-recovery-r17-typescript-generation-0345.
- Original parent canonical: 9b7562bc82f90801804afde0d3952e1768dcffcba1458746d4622798fa62d77a.
- Previous exp-v1-recovery-r12-typescript-generation-0345.candidate.json file: cb6bfb8d51c9dd32ddb6beaf0228440003ca37f49f5233f378ada8e35a3b9754.
- Previous candidate canonical: c4324b3e8808bd6abe72039396b84b3306cfe08c1617658fcc943a37d0a0d97f.
- Frozen problem: 5eff049a5bfe40f537c3b57455d44dfedb927481e94f68e235aa888ebb34a558.
- Frozen reference: f69c423b08b88c778e2bdbb754065bf25eb068239d2ff3a139c2caac72400335.
- Frozen mutant: 02b843f569f7d0df8720464c28f614be7286f1b0e4b015184e891a67609dbbc4.
- Previous tests: 0807836f7457fa6235475d65cb92299bee1bc2f25edda86336ff5fd58be02fbb.

Only this isolated note and recovery-requests-r17-PROVISIONAL.json/recovery-test-feedback-r17-PROVISIONAL.json were written. No diagnostics, candidates, reservations, central ledger or state changed. Main owns subsequent one-time correction, static review, serial sandbox and admission.

