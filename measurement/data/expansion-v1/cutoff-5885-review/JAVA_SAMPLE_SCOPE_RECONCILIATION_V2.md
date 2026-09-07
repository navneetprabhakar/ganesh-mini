# Java sample positive reconciliation — 2026-09-07

Focused reread of all34 previously positive Java sample prompts/references against
v14 null-query validation, percentage intermediate overflow and page arithmetic.
This adds zero outside-sample inspections and is not an admission seal.
Original5885 SHA256:680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.
Original sample, original tasks and historical reconciliation-v1 remain unchanged.

No new null-query or percentage defect was found in these34 references. This is
manual scope reconciliation, not additional execution coverage or universal proof.
Five blank-domain inconsistencies surfaced in that reread and are held below.
The earlier repair0041/0241/0243 rationale treated known-bad source trim calls as
defining the public contract. That is too strong: the prose says blank/nonblank
without specifying String.trim semantics. Source implementation cannot silently
narrow that contract. These are reversible correctness/contract-clarity holds;
recovery must explicitly freeze whitespace semantics and independently test them.
An explicit trim-plus-nonempty contract is not changed by this decision.

| Original positive ID suffix | Focused finding |
| --- | --- |
| generation-0662 | Code-point whitespace validation and independent EnumSet; no null query or percentage/page expression. |
| generation-0137 | Validated boxed-ID lookup and copied sorted snapshots; no new expression. |
| generation-0253 | Full row/element null traversal; bounded index selection. |
| generation-0268 | Validated state transitions; bounded acquisition counts. |
| generation-0308 | anyMatch element validation before copy; identity graph traversal. |
| generation-0379 | Element prevalidation and detached sorted mirror; no null query. |
| generation-0384 | Parsed bounded quality integer is displayed, not multiplied as a percentage. |
| generation-0393 | floorMod and fixed three-slot accounting; no unsafe page end. |
| generation-0394 | Checked sums remain valid; hold: U+2003-only input throws instead of zero. |
| generation-0395 | Center expansion on concrete arrays; no new page expression. |
| generation-0406 | Checked stack addition; output limit guards before append. |
| generation-0434 | Checked simulated-time addition; no percentage or page math. |
| generation-0458 | Complete element validation; set queries receive non-null strings. |
| generation-0636 | Exactly-once panel/provider delegation; new groups not applicable. |
| generation-0680 | Validated contacts with explicit null-array allowance and detached outputs. |
| generation-0739 | Nonempty, explicitly untrimmed IDs; guarded map queries and copied lists. |
| generation-0782 | Guarded EnumSet queries; hold: Unicode-only blank resource key accepted. |
| repair-0140 | Complete array prevalidation before folded comparison; no null query. |
| repair-0030 | Explicit parseLong and ordinary wrapping sum; no percentage operation. |
| repair-0041 | Copy boundary is valid; hold: Unicode-only blank segment accepted. |
| repair-0068 | Revision equality and cache ownership; no arithmetic or null query. |
| repair-0147 | Checked maximum, code-point-to-UTF16 conversion; no unsafe page end. |
| repair-0184 | 1L shift with index0..63 validation; no new issue. |
| repair-0219 | Divisibility guarded, derived vertex count and index bounds. |
| repair-0241 | Null-safe comparisons valid; hold: Unicode-only blank name accepted. |
| repair-0243 | Constructor/getter copies valid; hold: Unicode-only blank name accepted. |
| repair-0372 | Large maxWidth/maxHeight can overflow the numerator even for small grids, but then that axis needs no downsampling and factor is clamped to1; an incorrect required sampling factor needs infeasibly large concrete dimensions. Earlier bounded decision retained, not universal arithmetic safety. |
| repair-0376 | Full element traversal, size comparison without capacity addition, FIFO eviction. |
| repair-0414 | head+size concern needs >1-GiB concrete byte capacity; outside512-MiB envelope. No reflection/virtual-array counterexample. Bounded decision retained. |
| repair-0418 | Every set/list element validated before membership query. |
| repair-0428 | Validated finite role/action policy; no new groups. |
| repair-0475 | Dependency loops validate before map query; remaining count only decreases from list size. |
| repair-0499 | Counts bounded by List size, comparator uses Integer.compare, sublist0..limit guarded. |
| repair-0512 | Entry-by-entry validation, non-null key queries and explicit addExact. |

## Executed probes

Each `java-<kind><number>-sample-blank.java` has a matching `-result.json`
binding the frozen candidate, original task, isolated test, raw output and pinned
sandbox. Network disabled;1CPU/512MiB/64pids/60s. All compile, then exit[0,1],
timed_out=false; no original tests or candidates changed.

| ID suffix | Duration ms | Observed result |
| --- | --- | --- |
| generation-0394 | 2867 | IllegalArgumentException wrapping NumberFormatException on U+2003. |
| generation-0782 | 3431 | Assertion: blank resource key accepted. |
| repair-0041 | 3104 | Assertion: blank segment accepted. |
| repair-0241 | 3193 | Assertion: blank property name accepted. |
| repair-0243 | 2408 | Assertion: blank snapshot name accepted. |

Java sample becomes29 positive/31 held; total sample165/135, corpus2028 holds
(2025 additive plus historical3), outside inspections4799 unchanged. At most3857
original rows remain unheld. Approved versioned recovery remains necessary.
Cross-lane newer-scope reconciliation and prior outside page arithmetic remain
open; this document closes only this Java sample-positive pass.
