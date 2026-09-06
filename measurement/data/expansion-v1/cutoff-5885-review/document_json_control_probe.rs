#[path = "solution.rs"]
mod solution;

#[test]
fn document_cache_json_must_escape_control_characters() {
    let docs = [solution::NamedDocument { name: "doc\0".into(), body: "key=value\u{8}".into() }];
    let rendered = solution::compile_documents(&docs, "").unwrap().cache_json;
    assert!(!rendered.bytes().any(|b| b < 0x20), "raw controls in {rendered:?}");
}
