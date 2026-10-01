import pytest

from scripts.benchmarks.reassemble_public_rust import apply_rust_stop


def test_rust_published_stop_prevents_duplicate_closing_brace() -> None:
    raw = "fn answer() -> i32 {\n    1\n}\nfn extra() {}"
    assert apply_rust_stop(raw, ["\n}"], "}\nfn main() {}") == (
        "fn answer() -> i32 {\n    1\n"
    )


def test_rust_reassembly_fails_on_changed_contract() -> None:
    with pytest.raises(ValueError):
        apply_rust_stop("fn answer() {}", [], "}\nfn main() {}")
