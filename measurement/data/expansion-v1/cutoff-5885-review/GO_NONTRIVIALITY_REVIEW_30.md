# Go focused non-triviality review — batch 30

Positions436–450, full prompt/reference read; not a full new test/mutant review.
Ten criterion-positive, five non-triviality holds plus one static behavioral hold.
1336 total holds (1333 additive+3),3380 unique outside inspections. Resume451.

| Position | ID | Finding |
| --- | --- | --- |
| 436 | exp-v1-go-repair-0248 | Criterion-positive: grouping must preserve first-key order without cross-group shared backing-array state. Extra per-append copying is unnecessary but not a correctness failure. |
| 437 | exp-v1-go-generation-0373 | Criterion-positive: concurrent remaining-lifetime accounting, permanent-zero distinction and inclusive expiry without absolute-clock overflow. |
| 438 | exp-v1-go-generation-0375 | Non-triviality hold: direct count guard and alternating string concatenation. |
| 439 | exp-v1-go-generation-0376 | Criterion-positive: authoritative revision caching, load-before-cache use, invalidation, error preservation and detached bytes. Callback reentrancy is not required. |
| 440 | exp-v1-go-generation-0378 | Criterion-positive: strict single-value decoding, UseNumber, container-first traversal and ordered escaped JSON Pointer paths. |
| 441 | exp-v1-go-repair-0249 | Criterion-positive: convert byte-based rotation to rune-count/modular indexing without splitting UTF-8 characters. |
| 442 | exp-v1-go-repair-0250 | Non-triviality hold: direct removal of extra minus-one from supplied mean denominator. IEEE propagation is expressly allowed; no new numeric probe. |
| 443 | exp-v1-go-repair-0251 | Criterion-positive: merged sort must allocate independently before append can reuse caller capacity. |
| 444 | exp-v1-go-repair-0252 | Non-triviality hold: direct fixed-width hexadecimal format-string correction. |
| 445 | exp-v1-go-generation-0379 | Criterion-positive: insertion-ordered capability identity, duplicate constructor rejection versus Add no-op, and independent copies. |
| 446 | exp-v1-go-generation-0381 | Criterion-positive: ordered output-to-input callback chain, trace retention and failure at reached nil stage without suppressing prior effects. |
| 447 | exp-v1-go-generation-0382 | Criterion-positive authentication task; static behavioral hold: raw-base64 signature decoding accepts appended CR/LF without canonical encoding check. Canonical JSON comparison does not validate encoded signature spelling. |
| 448 | exp-v1-go-generation-0383 | Criterion-positive: zero-value profile store, replacement identity check and nil-aware role ownership across every read/write. |
| 449 | exp-v1-go-repair-0253 | Non-triviality hold: direct absolute-value guard; safe widening before subtraction already supplied. |
| 450 | exp-v1-go-repair-0254 | Non-triviality hold: direct exclusive exponent-loop boundary correction. |

No new execution in this batch. generation0382 uses the same permissive
RawURLEncoding.DecodeString signature path demonstrated in prior executed
0276 probe; its own code was read, but no separate execution is claimed.
Append a newline to a minted token: decoded signature and decoded payload
remain unchanged, so the subsequent HMAC/JSON checks do not reject it.
Frozen candidate SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

