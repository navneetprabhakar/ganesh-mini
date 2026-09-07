# Go focused non-triviality review — batch 43

Positions631–645, full prompt/reference read; not a full new test/mutant review.
12 criterion-positive, three non-triviality holds plus three static behavioral holds.
1400 total holds (1397 additive+3),3575 unique outside inspections. Resume646.

| Position | ID | Finding |
| --- | --- | --- |
| 631 | exp-v1-go-generation-0676 | Criterion-positive: zero-value reusable dual indexing, kind-sensitive pending deletion and copied payload ownership. |
| 632 | exp-v1-go-generation-0679 | Non-triviality hold: direct type-switch conversion and prescribed domain guards around math.Pow; numerical evaluation is delegated. |
| 633 | exp-v1-go-generation-0682 | Criterion-positive packet dispatch; static behavioral hold: null counter values decode into zero ints and are accepted despite the integer-only body contract. Struct decoding also accepts differently cased outer field names. |
| 634 | exp-v1-go-generation-0685 | Criterion-positive: synchronized validate-before-start component lifecycle, stopped-state cleanup and restartable status snapshots. |
| 635 | exp-v1-go-generation-0686 | Non-triviality hold: direct finite/range guards, explicitly supplied weighted-mean formula and fixed precision formatting. |
| 636 | exp-v1-go-generation-0687 | Criterion-positive: store call/error/log sequencing distinguishes negative affected counts from store failures and preserves wrapped error identity. |
| 637 | exp-v1-go-generation-0688 | Criterion-positive: shallow listing ownership, full textual validation and shared column width across ordered records; no invented method-call purity extension. |
| 638 | exp-v1-go-generation-0689 | Criterion-positive: synchronized epoch expiry, checked signed value and unsigned epoch changes, and expiration-preserving addition. |
| 639 | exp-v1-go-generation-0691 | Criterion-positive: validated unique-ID directory with independent nested tag storage and sorted detached views. |
| 640 | exp-v1-go-generation-0692 | Criterion-positive arena lifecycle; static behavioral hold: uncapped shared slice capacity lets an earlier allocation overwrite future regions before they are returned as supposedly zeroed bytes. |
| 641 | exp-v1-go-generation-0693 | Criterion-positive: validate exported identifiers, nested uniqueness and kind mapping before sorting copies and rendering exact declaration layout. |
| 642 | exp-v1-go-generation-0695 | Criterion-positive: lock-serialized sink calls, successful-baseline-only updates, forced checkpoints and closed-before-validation precedence. |
| 643 | exp-v1-go-generation-0697 | Criterion-positive directory updates; static behavioral hold: lowercase indexing does not implement Unicode case-insensitive uniqueness, allowing sigma/final-sigma contacts separately. |
| 644 | exp-v1-go-generation-0698 | Non-triviality hold: direct scalar getters/setters and fixed constructor defaults with variadic-count/format guards. |
| 645 | exp-v1-go-generation-0701 | Criterion-positive: ordered validation separates absent from corrupt state and performs only an existing-key atomic state change. |

Static review only; no new execution claimed. generation0682 accepts
{"kind":"counters","body":{"x":null}} as x=0; null is not an integer.
generation0692: NewScratch(2,2), Take(1), then reslice the returned value to
length2 and write its second byte; the next Take(1) returns that nonzero byte.
The returned two-index slice exposes all remaining arena capacity.
generation0697: contacts "Σ" and "ς" lowercase to different keys despite
Unicode case-insensitive equivalence; this is the same lowercase-versus-fold
class already documented in earlier Go directory reviews.
Criterion-positive is not admission or a claim of all-seven-criteria approval.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

