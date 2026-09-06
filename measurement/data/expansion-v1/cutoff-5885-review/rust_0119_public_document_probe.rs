#[path = "solution.rs"]
mod solution;
use solution::{Archive, Document};

#[test]
fn publicly_constructed_document_must_respect_required_id() {
    let mut archive = Archive::new();
    assert!(archive.add(Document { id: 0, title: "Title".into(), pages: 1 }).is_err());
    assert!(archive.documents().is_empty());
}
