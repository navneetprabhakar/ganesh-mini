# R8 Java static recovery review — 2026-09-08

Gate 2: complete prompts, references, independent tests and known-bad implementations read for all ten derived generation candidates, against the exact approved R8 scopes carried from R4. **Six static positives; four quality holds.** No execution, generation, cloud usage, admission or central state edits. No new original-row review credit.

## Exact per-ID decisions

All suffixes identify `exp-v1-recovery-r8-java-generation-<suffix>`.

| Suffix | Disposition | Reference and actual test finding |
|---|---|---|
| 0710 | Static positive | Remaining-length-bounded endpoints and start=end avoid overflow. A header plus two rows at Integer.MAX_VALUE batch size directly distinguishes the overflow mutant with tiny inputs. Exact grammar, Turkish default-locale independence, original order and immutable independent output have coherent tests. |
| 0641 | HOLD — missing precision witness | BigInteger squared distance correctly preserves exact inclusion over the declared int coordinates and long radius. Tests cover huge radii and exact axis distances but never the near-boundary point `(Integer.MAX_VALUE,1)` with origin viewer and radius Integer.MAX_VALUE. The double mutant rounds this just-outside distance onto the boundary; existing cases do not expose that rounding. |
| 0642 | Static positive | Both supports and convert are inside the runtime-to-ParseException boundary, with cause identity retained. The test's supports marker exception directly distinguishes the mutant. Ordered custom selection, null result, wrong type, built-ins and validation are covered. text/plain is checked by content, not unpromised String identity. |
| 0647 | Static positive | Empty URL rejected in add and changeUrl; persistent snapshots and unchanged prior catalogs preserved. Tests exercise both empty-URL rejections and accept whitespace-only/nonempty opaque values exactly as expressly allowed. Getter API is frozen in the derived prompt; no private-field oracle. |
| 0617 | HOLD — missing accepted-Set witness | Reference iterates group elements rather than querying contains(null), preserving Set.of and TreeSet compatibility. Tests only use null-query-tolerant LinkedHashSet, Collections.emptySet and Collections.singleton. No Set.of or TreeSet input reaches the original failure. Full-assets validation before first match and mutable detached results are meaningfully tested, but the intended mutant survives those cases. |
| 0677 | Static positive | Explicit String.isBlank versus String.trim distinction is present. U+2003-containing blank ID test distinguishes trim-only mutant. Final immutable fields and synchronized state/read/transition/toString methods implement the concurrency contract. Bounded 24-worker start-latch races independently require exactly one beginSend, deliver and markRead success. |
| 0687 | HOLD — wrong exception-stage oracle and missing apply witness | Reference validates permission IDs during apply for every kind, as the approved scope explicitly requires. Tests demand construction alone reject REPLACE permissions containing null and DELETE permissions containing zero. Neither constructor does this, so both reference and mutant fail those assertions. No existing-group DELETE invalid-permission apply call tests the intended defect. |
| 0762 | HOLD — standalone-newline oracle conflict | Exactly-one-separator correction is implemented and tested. However, the suite expects decodeFeed("\\n") to return empty, while both implementations reject it as a blank line. The prompt allows a trailing newline and describes zero records but does not explicitly settle the standalone-newline interpretation. This expectation is not a basis to silently broaden the reference; omit the ambiguous assertion in a bounded test correction or make an expressly approved contract decision. |
| 0785 | Static positive | Blank validation uses isBlank while output normalization stays trim; tests verify U+2003 around nonblank text remains stored, and Unicode-blank heading rejection distinguishes the mutant. Equals-equal distinct listeners, identity deduplication, ordered snapshot add/remove, same exception propagation/stop and independent hubs are covered. No new concurrency guarantee. |
| 0763 | Static positive | isBlank validation precedes ID allocation; valid padded text stays unchanged. Unicode-blank rejection distinguishes mutant; failed appends do not consume IDs. Immutable snapshots, clear/reset and Long.MAX_VALUE logical ticks are checked. Eight joined workers perform 40 appends each; resulting IDs must be sequential in ledger order with 320 distinct payloads, without assuming worker scheduling. |

## Seven criteria and scope limits

1. **Prompt clarity:** all five strict reference-fix problems (0710, 0641, 0642, 0617, 0687) are exactly equal to immutable parent problem strings, including opening/final instructions. The failed R4 prompt-paraphrase issue is not present in these R8 artifacts. Two oracle rebuilds and three clarification prompts change only the approved URL/grammar/API or blankness/normalization scopes. The 0762 standalone newline remains a specific unresolved interpretation, not a general review caveat.
2. **API consistency:** required public APIs, order, schemas, immutable/mutable return semantics and exception categories are retained. 0687 tests violate the approved apply-time exception stage. No test reflects over private fields. 0617 returns the original first matching Asset as promised; its identity assertions are not an invented private layout. 0677 tests the exact raw delimiter toString format even when content contains a pipe; it does not demand escaping.
3. **Independent tests:** exact specification-only origin and output bindings pass for every row. Independence does not cure the two oracle conflicts or two missing defect witnesses.
4. **Whole-target nontriviality:** complete targets combine grammar/chunking/locale/ownership (0710), exact geometry/validation/color/matrix ownership (0641), ordered callbacks/fallback/error boundaries (0642), persistent catalog state (0647), full validation/selection/first identity/ownership (0617), synchronized lifecycle (0677), sequential transaction validation/sorted deep snapshots (0687), line grammar/opaque fields/immutable output (0762), reentrant identity subscriptions (0785), and synchronized ledger IDs/snapshots/reset (0763). No positive relies on the recovery patch's size.
5. **Idiomatic implementation:** BigInteger provides exact geometry without epsilon; iterative validation avoids hostile null queries; standard synchronized methods protect mutable Java state; copies and unmodifiable wrappers implement declared ownership. Reference fixes are substantively sound in the specified domains. No private ID exhaustion or enormous history behavior is fabricated.
6. **Dependency isolation:** references/tests use Java standard library only, requested Solution APIs and executable SolutionTest mains. Concurrent tests use start latches, thread joins and captured worker exceptions, with bounded worker counts/work. No compilation or execution performed in this review.
7. **Realistic failures:** all ten supplied mutants model the original held mechanism. Six positive suites exercise it. 0641/0617 miss it; 0687/0762 contain common failing assertions that cannot count as discrimination.

Coverage breadth is recorded separately from actual defects: 0642 does not include the suggested later-null-after-supporting-converter case; its full reference prevalidates all conversions and its actual supports exception witness is decisive. 0677 does not concurrently sample toString or independently use a Unicode-blank sender; 0763 does not interleave clear/read with writers or verify every concurrent payload-to-tick association. Their explicit synchronization/source structure and bounded existing tests support static positives, not exhaustive concurrency certification. 0785 uses a Unicode-blank heading rather than both fields, but both corrected field predicates are visible and the actual mutant is distinguished. These omissions do not justify inventing scheduling, output or normalization rules.

For held 0641 a minimal specification-derived witness excludes `(MAX_INT,1)` and includes `(MAX_INT,0)` at radius MAX_INT. For held 0617 standard Set.of empty/nonempty and TreeSet valid group inputs suffice. For 0687 enclose construction and apply in invalid-permission checks with an existing group; include null/empty/positive DELETE controls and preserve original map on failure. Do not move validation to the constructor to satisfy the current test. For 0762 retain the valid nonempty feed single-trailing-newline tests, extra-pipe rejection, interior blank and two-trailing-newline rejection; do not use the disputed standalone newline to redefine the reference. This report initiates no correction loop.

## Integrity and provenance

Paths below are relative to `datasets/cache/expansion-v1/versioned-recovery/r8/`.

- `plan.json` file SHA256: `1a579af9da9d542d6bb4f03c8fbc030fd0b9d3102a31c347cd631bfc18b873de`.
- `java-recovery-architect-evidence.json`: `9cb29348172d7aa8fb931e9489bc1e18892d2a7bdaefc229a246c4d7a998c902`.
- `java-recovery-independent-tests-evidence.json`: `f5bf9b22d238b98c6e66540bc9c99b41a41ca6f71bcba46795ad414a8587e301`.

Both evidence prompt and final-output hashes recompute correctly; both disallowed-tool lists are empty. Independent task payloads contain exactly id/problem, matching candidate prompts. All ten architect problem/reference_code/known_bad_code strings and independent test_code strings equal the installed components. All ten immutable parent canonical hashes match plan bindings. Source metadata, except the appended recovery transformation, and rights match their original parents; no original lineage is overwritten or new rights decision asserted.

| Suffix | Candidate file SHA256 | Test content SHA256 |
|---|---|---|
| 0710 | ab92529965938deabd038ef77cc65a2f1be588e14030280ec8c74f2d40fa2fc2 | 13c6bdf0870752d8d1add9b4b991590e70f250d1e9f0663877c5a6c29bc5c8e9 |
| 0641 | c9cab9f7b6d62f0e155326f04c8c42f081114b5e6f269755dd4a5954859dc225 | 3b3575f36ef1a426b4fc4b84b333543ac78aa8826dca1354a7d8eb7ec869430e |
| 0642 | fc90c5a1a42ea01b063fdd7bf25fbcec759028dc0be74ea192580c744598710b | 62f04ffdbe0e771fad631fe879b6e33bfc4ecaad1f069f9dc870898d15c85329 |
| 0647 | ed6d6a38cf2affb97b57bdbdaf93e48e185a9c34f7fb3da190cc9dda7117ae07 | d4b2a50d45512967e6b34f538a75c424b0cb5e9604eaefd81624c74ae223066a |
| 0617 | c9c5c8aa0a37fdccbab6a7c4dcd55fd9bcc42824de42271ef85c8f0faac8866a | 0e995b704f6ec1b77c5cdd662274f53c87d26c40b42b2192eed7a0745399a592 |
| 0677 | fbcfc30600bec0a2d73daaa101f51899dd73c345c89a4af273bae47a001c69bb | 0221b4f5727ff4f8a929dd16fd1d77a26419a3fb48b2de08c62ff56d9189fc83 |
| 0687 | 4b33e4f4723ff43ff7aefed485b860e5e0fb755d8456f0663edf082346fb8b9b | 07711aaf585266a0efe3fd72dd5dba98e59db47041356eb43876df539f5f618a |
| 0762 | f7af8a304d18124e7a642ee4e85b8723463042562a63058c2e669e53eca406dc | 4fd115d8623d951437c59a906a3869b55af1e7ee358e3688b681a3274e292358 |
| 0785 | 7875fddbd7a81647a3fa20e5c620918852656c94bd8c64f9471315a9bed2367a | 8502391f242ee704e479d98a50c06b7b68f697d3d865d6deb82038e9e451969a |
| 0763 | 2c035c56d630933b75ac703c07d16f7cd723d2b6eb0d15f812eccb50aeaa9df3 | c16dafff425703823073193984f8ae2f2403cd4906eafb9e72673d233d18994b |

Main owns separately evidenced sandbox qualification and admission. These static positives do not imply execution or release readiness.
