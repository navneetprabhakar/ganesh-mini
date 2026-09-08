# Python numeric-pending follow-up 1

2026-09-08. Scope is exactly the ten pending entries in
`python-criteria-reconciliation-through300.json`: eight unheld and two already
elementary-held. This is an integration recommendation, not a central-state
update. ZERO new unique inspections; no candidate execution or capacity test.
Original review notes remain unchanged.

Corpus SHA256: `680b4b52a567da668bbc235095bf723acf9ba6b01401de813d203ac196df66ec`.
The original prompt/reference/tests for all ten were read in this reviewer's
current or preceding bounded assignments. The last five full rereads were
generation0027/0054/0162/0285 and repair0110. Main independently reread the
eight unheld candidates as stated in the assignment.

## Recommended dispositions

Close six numeric questions, propose three numeric-domain/clarity holds, and
retain one narrowly defined resource-probe question. No elementary disposition
is reversed. Scoped closure is not seven-criterion admission.

| Candidate ID | Already elementary-held | Numeric recommendation | Substantive basis and remaining boundary |
| --- | --- | --- | --- |
| exp-v1-python-generation-0019 | No | CLOSE — scoped positive | Cartesian expansion preserves order and width-zero identity; empty alphabet with positive width is mathematically empty. Python integer iteration does not narrow width. Iterating pointlessly after result becomes empty is an avoidable-work/idiomatic-quality concern, not a demonstrated numeric defect or violation of a stated time bound. Preserve that concern separately; no capacity guarantee inferred. |
| exp-v1-python-generation-0027 | No | CLOSE — scoped positive | Proper divisors occur in factor/partner pairs, with perfect-square partner deduplication and exact integer sum/comparison. Inclusive upper+1 and ignoring values below1 use arbitrary-precision arithmetic. Trial division can be slow, but no runtime complexity or capacity limit was promised. No numeric hold based solely on huge intervals. |
| exp-v1-python-generation-0054 | No | CLOSE — scoped positive | Two arrays of width min(slot_count,action_count+1) meet the explicitly required proportional-memory bound. Every transition uses integer arithmetic and modular reduction. Linear iteration over action_count is not forbidden; do not invent a logarithmic-time requirement or a constant-time one-slot special case. Absolute allocation/time feasibility remains uncertified, not numeric failure. |
| exp-v1-python-generation-0075 | No | HOLD — numeric-domain/clarity | The prompt requires JSON-serializable input values and valid JSON array output. Python's default json.dumps serializes float NaN/infinities as nonstandard tokens; the reference does not set allow_nan=False. On the broad Python-serializable reading, a one-record NaN input can produce [NaN], violating valid-JSON output. On the strict-JSON-value reading, nonfinite input is excluded, but that narrower domain is not stated. Select that domain or specify rejection; do not silently clear the contradiction. |
| exp-v1-python-generation-0076 | No | HOLD — numeric-domain/clarity | classify_scalar returns a category, not a float. The syntactically ordinary decimal '1e400' denotes a finite decimal number, yet float conversion produces infinity and reference classifies it as text. The prompt does not say finite in binary64 or give exponent/magnitude bounds. Specify decimal-finite semantics or float-representable semantics. This is not a claim that the task must return a representable float. CRLF framing remains a separate unresolved criterion. |
| exp-v1-python-generation-0084 | Yes | CLOSE — scoped positive | Positive multiples strictly below horizon follow Python's exact range semantics. Producing the explicitly materialized list necessarily costs space proportional to its length. No global allocation guarantee or maximum list length was promised; do not turn unavoidable huge output into a numeric defect. Existing elementary hold remains. |
| exp-v1-python-repair-0059 | No | PENDING — bounded resource probe recommended | For ordinary finite allocations, (value & ((1<<width)-1)) >> bits correctly implements unsigned low-width shifting, including negative values. But positive tiny values with gigantic width demand a gigantic mask despite a tiny exact output. This distinguishes an avoidable intermediate from unavoidable output allocation. No capacity result exists; the proposed probe below is not yet evidence and does not itself justify a hold. |
| exp-v1-python-generation-0162 | No | HOLD — numeric-domain/clarity | Payload may be any valid JSON value, but default json.loads maps the valid finite-number lexeme 1e400 to infinity; parse_constant rejects literal NaN/Infinity only and cannot intercept exponent overflow. The prompt gives no numeric representation/range policy for arbitrary JSON numbers. Integer digit limits are an additional runtime-dependent restriction, not needed to establish this missing policy. Clarify whether payload numbers use default Python JSON conversion, bounded finite floats, or another representation before admission. |
| exp-v1-python-repair-0110 | Yes | CLOSE — scoped positive, output/runtime caveat retained | pages controls an explicitly materialized list of pages separate footer strings. Counters/range arithmetic are exact. Astronomical pages necessarily requires astronomical output, independently of decimal formatting limits; no universal allocation guarantee was promised. Retain extreme formatter/runtime caveat as unexecuted, but it is not by itself an additional numeric gate. Existing elementary hold remains. |
| exp-v1-python-generation-0285 | No | CLOSE — scoped positive | Prompt explicitly delegates invalid CLI values to normal argparse behavior. Standard int conversion and argparse's conversion-error path are consistent with that delegated parser contract; port is explicitly bounded and workers/threads checked positive. Do not impose an undocumented arbitrary-length decimal lexer or disable runtime integer safeguards. This closure does not certify any actual service capacity. |

Proposed new hold IDs: `exp-v1-python-generation-0075`,
`exp-v1-python-generation-0076`, `exp-v1-python-generation-0162`.
These are static contract/domain findings, not executed numeric failures.
If main chooses to leave any as pending instead of a clarity hold, record the
same precise missing domain choice; do not label it a positive.

## Why the JSON cases are different

0075 constructs output text required to be valid JSON; merely being accepted by
Python's permissive serializer does not establish that property. A useful
contract choice is either strict JSON-value inputs, excluding NaN/infinities,
or explicit rejection via the serializer. Existing permission to propagate
serialization exceptions does not authorize returning invalid JSON text.

0162 consumes JSON text containing a valid finite-number lexeme. Its issue is
not Python-only nonstandard input constants: rejecting NaN does not reject or
preserve the numeric meaning of 1e400. The required Python representation is
underspecified. Do not demand exact arbitrary decimal arithmetic generally
without a contract change, but do not assume silent infinity is intended.

0076 similarly needs no float output: a classifier can recognize finite decimal
syntax without imposing the representability restriction introduced by float().

Lone-surrogate behavior, general custom-object copying, recursive depth, and
other historical questions stay separate. No global JSON or alias criterion
is cleared by these numeric recommendations.

## Recommended repair0059 probe — NOT EXECUTED

Purpose: distinguish an avoidable width-sized intermediate from a genuinely
large required answer. Expected results can be stated without another giant
mask or reconstruction of verifier metrics:

- Control: logical_right_shift(0,0,32) == 0.
- Control: logical_right_shift(1,0,32) == 1.
- Large-width target: logical_right_shift(0,0,2**32) == 0.
- Large-width target: logical_right_shift(1,0,2**32) == 1.
- Fast-path control: logical_right_shift(-1,2**32,2**32) == 0.

The width value itself is a small Python integer. A 2**32-bit mask needs at
least512 MiB of mathematical bit storage, before interpreter representation
and temporaries. Returned target results need only a few bits. No decimal
conversion-limit behavior is involved.

Run each case in a separate approved network-disabled resource-limited sandbox
using the pinned Python toolchain and unchanged candidate artifact. Suggested
bounded envelope, only if supported by the existing approved runner:256 MiB
hard process/container memory,2 CPU seconds,5 wall seconds,16 processes and
4 KiB output. Otherwise adapt width to the frozen hard memory cap M bytes so
width=16*M bits demands at least2*M bytes for the mask; preserve the actual
limits in evidence. Do not raise production limits or run this on the host.

Record candidate/test hashes, Python identity, configured limits, per-case
exit/signal, timeout, elapsed time and raw output. Stop each process at its
limit. MemoryError, kill or timeout would characterize failure under that
specific envelope, not prove universal correctness failure or invent a
runtime promise. Main must adjudicate whether it supports the existing
idiomatic/resource admission criterion. A passing run must not be generalized
to arbitrary widths. No probe has been dispatched here.
