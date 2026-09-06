#[path = "solution.rs"]
mod solution;
use solution::TagRegistry;

#[test]
fn sorts_complete_qualified_tag_strings() {
    let mut registry = TagRegistry::new();
    for scope in ["a", "a0"] {
        registry.register_scope(scope).unwrap();
        registry.register_tag(scope, "x").unwrap();
    }
    assert_eq!(registry.tags(), vec!["a0::x", "a::x"]);
}
