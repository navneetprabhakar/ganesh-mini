from scripts.benchmarks.run_public_multipl_e import postprocess_program


def test_postprocess_applies_published_stop_token_after_exact_prefix() -> None:
    prefix = "package example\nfunc answer() int {\n"
    raw = prefix + "return 1\n}\nfunc TestExtra() {}<|im_end|>"
    program, matched = postprocess_program(raw, prefix, ["\nfunc"])
    assert matched is True
    assert program == prefix + "return 1\n}\n"


def test_postprocess_does_not_rewrite_nonmatching_prefix() -> None:
    program, matched = postprocess_program("different\nfunc Extra() {}", "original", ["\nfunc"])
    assert matched is False
    assert program == "different\nfunc Extra() {}"


def test_rust_full_program_applies_published_stop_without_exact_doc_prefix() -> None:
    prefix = "/// task documentation\nfn answer() -> i32 {\n"
    raw = "fn answer() -> i32 {\n    1\n}\nfn extra() {}"
    program, matched = postprocess_program(
        raw, prefix, ["\n}"], stop_nonmatching_full_program=True,
    )
    assert matched is False
    assert program == "fn answer() -> i32 {\n    1\n"
