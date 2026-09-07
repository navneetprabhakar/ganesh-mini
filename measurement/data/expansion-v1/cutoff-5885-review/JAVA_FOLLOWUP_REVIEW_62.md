# Java combined quality follow-up — batch 62

Positions916–930 of v14 Java queue1112, full prompt/reference read.
Eight new holds: four non-triviality and four static findings.
1932 total holds (1929 additive+3),4617 unique outside inspections. Resume931.
Approved versioned recovery remains pending; original corpus unchanged.

| Position | ID | Finding |
| --- | --- | --- |
| 916 | exp-v1-java-generation-0658 | Static hold: int loop counter wraps after Integer.MAX_VALUE in the explicitly full-domain factorial contract; theoretical boundary not executed. Elementary factorial reduction also needs non-triviality reconsideration. |
| 917 | exp-v1-java-generation-0659 | Criterion-positive canonical positive-long parsing rejects signs, leading zeros and overflow before immutable model translation; explicit String.trim semantics do not require Unicode blank rejection. |
| 918 | exp-v1-java-generation-0660 | Criterion-positive cursor-based UTF-16 length framing checks canonical counts and subtraction-based bounds before slicing, then consumes a canonical nonnegative long revision. |
| 919 | exp-v1-java-repair-0437 | Non-triviality hold: direct removal of index-minus-one in the supplied list insertion; all nested copying and validation are already supplied. |
| 920 | exp-v1-java-repair-0438 | Static hold: start + maximumSize and subsequent int increment can overflow for sufficiently large valid lists; correction only fixes end exclusion. Large-list boundary not executed. |
| 921 | exp-v1-java-repair-0439 | Criterion-positive type-directed literal dispatch replaces an unsafe narrowing cast and rejects unsupported implementations while preserving raw text versus numeric rendering. |
| 922 | exp-v1-java-repair-0440 | Criterion-positive payload type discrimination restores both supported representations and the specified IllegalArgumentException boundary instead of ClassCastException. |
| 923 | exp-v1-java-generation-0656 | Static hold: U+2003-only book title passes required blank rejection. Not executed. |
| 924 | exp-v1-java-generation-0663 | Static hold: U+2003-only ID passes constructor nonblank check. Numeric recovery must also address overflowed distances: target -Double.MAX_VALUE and values Double.MAX_VALUE then Double.MAX_VALUE/2 compare as equal infinities, retaining the farther first reading. Not executed. |
| 925 | exp-v1-java-generation-0664 | Criterion-positive grid movement validates before mutation, removes collected parcels and freezes a terminal won/lost state while returning detached row snapshots. |
| 926 | exp-v1-java-generation-0665 | Criterion-positive in-place doubly-linked reversal saves old next before rewiring both links and swaps endpoints, retaining append correctness and detached snapshots. |
| 927 | exp-v1-java-repair-0441 | Non-triviality hold: directly substitutes the prescribed exclusive scalar lower-bound comparator in a supplied linear count. |
| 928 | exp-v1-java-repair-0442 | Non-triviality hold: single null-to-empty fallback around the supplied String.replace wrapper. |
| 929 | exp-v1-java-repair-0443 | Criterion-positive expiry transition forbids renewal exactly at deadline and preserves no-mutation behavior on checked addition failure. |
| 930 | exp-v1-java-repair-0444 | Non-triviality hold: prescribed null-label ternary and literal string concatenation replacing trim. |

No new execution. Static findings are not executed results. Focused positives are not full seven-criterion approval or admission.
Frozen SHA680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec.

