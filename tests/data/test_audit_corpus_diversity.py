import hashlib
import json

from scripts.data.audit_corpus_diversity import build, canonical_bytes, prompt_tags, scaffold_fingerprint


def row(identifier: str, lane: str, task_type: str, prompt: str) -> dict:
    return {
        "id": identifier,
        "lane": lane,
        "task_type": task_type,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "complete source"},
        ],
        "source": {"record_id": f"source-{identifier}"},
    }


def test_tags_are_observable_and_multi_label() -> None:
    tags = prompt_tags("Parse Unicode strings, reject malformed input, and return a sorted copy without mutation.")
    assert tags == [
        "aliasing_or_mutation",
        "errors_or_malformed",
        "ordering_or_sorting",
        "parsing_or_encoding",
        "string_or_unicode",
    ]


def test_scaffold_masks_code_and_surface_literals() -> None:
    left = "Implement `Alpha` for 12 values.\n```go\nfunc A() {}\n```"
    right = "Implement `Beta` for 99 values.\n```rust\nfn b() {}\n```"
    assert scaffold_fingerprint(left) == scaffold_fingerprint(right)


def test_build_binds_selected_ids_and_seals_report(tmp_path) -> None:
    corpus = tmp_path / "corpus.jsonl"
    selected = tmp_path / "selected.jsonl"
    rows = [
        row("a", "go", "generation", "Parse a string and reject malformed input."),
        row("b", "rust", "repair", "Repair a sorted sequence without mutating the input."),
    ]
    corpus.write_text("".join(json.dumps(value) + "\n" for value in rows))
    selected.write_text(json.dumps({"id": "prepared-a", "source_id": "a"}) + "\n")
    report = build(corpus, selected)
    claimed = report.pop("report_sha256")
    assert claimed == hashlib.sha256(canonical_bytes(report)).hexdigest()
    assert report["scope"]["evaluation_surfaces_read"] == 0
    assert report["corpus"]["records"] == 2
    assert report["selected_probe"]["records"] == 1


def test_missing_selected_id_fails_closed(tmp_path) -> None:
    corpus = tmp_path / "corpus.jsonl"
    selected = tmp_path / "selected.jsonl"
    corpus.write_text(json.dumps(row("a", "go", "generation", "Parse input.")) + "\n")
    selected.write_text(json.dumps({"source_id": "missing"}) + "\n")
    try:
        build(corpus, selected)
    except ValueError as exc:
        assert "missing from corpus" in str(exc)
    else:
        raise AssertionError("missing selected ID must fail closed")
