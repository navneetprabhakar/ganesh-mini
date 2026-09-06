# Python repair review, batch 25

Positions 361–375 of 426: full prompts, known-bad/corrected source and original
tests read. Eight new holds, 900 additive plus historical three = 903;
2,292 unique outside-sample inspections. Pending dispositions, not final
rejections, seven-criterion approvals or new known-bad certifications.

| Position | Repair ID | Scoped finding |
| --- | --- | --- |
| 361 | 0422 | Alphabet zero digit repairs encoding. Exact divmod, integer and alphabet validation agree; no new hold. |
| 362 | 0423 | Modulo checksum repairs overflow. Bytes conversion precedes byte-length validation; boundaries agree. No new hold. |
| 363 | 0425 | Full range repairs final chunk. Hold: nested mutable element shared across chunks; copy-depth wording requires disposition. |
| 364 | 0426 | UTF-8 before XOR repairs Unicode. Empty/type/key rules agree; test reference mirrors implementation, independence pending. No new hold. |
| 365 | 0428 | Outdegree repairs transition weights. Hold: huge invalid damping raises OverflowError. Test reference mirrors implementation; independence pending. |
| 366 | 0429 | Owner-index lookup repairs assignment. Full owner validation, item order and unknown lookup agree; no new hold. |
| 367 | 0430 | Big endian repairs length decoding. Exact length, type and empty frame agree; bytes identity wording pending. No new hold. |
| 368 | 0431 | Returning text repairs bytes output. Single-codepoint validation and iterable consumption agree; no new hold. |
| 369 | 0433 | Deepcopy repairs usual nested alias. Hold: accepted standard MappingProxyType cannot be copied. |
| 370 | 0434 | Final decoding error repairs premature failure. Hold: recognized non-text codec escapes as LookupError; encoding-domain disposition pending. |
| 371 | 0435 | Strict capacity comparison repairs equality. Hold: malformed unhashable operation changes validation exception type; prose scope pending. |
| 372 | 0436 | Sets repair duplicate programs. Field validation and sorted all-user output agree; no new hold. |
| 373 | 0437 | Strict half-turn comparison repairs positive boundary. Hold: finite large angle cannot progress by subtracting a small turn. |
| 374 | 0438 | Strict UTF-8 repairs replacement decoding. Hold: valid large field hits CSV runtime limit. Newline handling and BOM agree. |
| 375 | 0439 | Correct bisection half repairs update. Hold: underflow sign test accepts nonzero constant without a bracket. |

Eight pinned Python 3.11.15 network-disabled/resource-limited probes exited 1
without outer sandbox timeout; eight failing/error tests. The angle probe used
an internal two-second deadline, caught TimeoutError, and failed its assertion.
The chunk probe reached the cross-chunk alias assertion; its later input-alias
assertion was not reached. Original tests read, not rerun by isolated probes.
Candidate/test/sample/partition unchanged; candidate SHA:
`680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.

| ID | Probe/result stem | ms | Observed |
| --- | --- | ---: | --- |
| 0425 | repair_chunk_copy_nested_alias / repair-chunk-copy-nested-alias | 724 | nested cross-chunk alias |
| 0428 | repair_rank_nodes_damping / repair-rank-nodes-damping | 695 | OverflowError |
| 0433 | repair_visible_profile_mapping / repair-visible-profile-mapping | 488 | TypeError |
| 0434 | repair_decode_nonblank_codec / repair-decode-nonblank-codec | 516 | LookupError |
| 0435 | repair_memory_timeline_operation / repair-memory-timeline-operation | 417 | TypeError |
| 0437 | repair_continuous_turns_stall / repair-continuous-turns-stall | 2600 | internal probe deadline |
| 0438 | repair_decode_rows_field_limit / repair-decode-rows-field-limit | 618 | csv.Error |
| 0439 | repair_bracketed_zero_underflow / repair-bracketed-zero-underflow | 486 | missing ValueError |

Probe filenames append `_probe.py`; results append `-result.json`.
Batch awaits backup. GCS verified through repair345 / 891 holds / 2,262
outside-sample inspections: QUALITY_STRATUM_891_BACKUP.md. Continue position376.
