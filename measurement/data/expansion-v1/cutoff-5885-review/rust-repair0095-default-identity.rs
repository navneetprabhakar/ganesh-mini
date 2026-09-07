#[path = "solution.rs"]
mod solution;

#[test]
fn public_default_starts_ids_at_one() {
    let mut book = solution::IdentityBook::default();
    assert_eq!(book.add("a".into(), "secret".into(), solution::Permission::Reader), Ok(1));
}
