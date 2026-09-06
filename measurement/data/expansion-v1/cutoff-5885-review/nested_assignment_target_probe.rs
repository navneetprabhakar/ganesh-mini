#[path = "solution.rs"]
mod solution;
use solution::{eval, EvalError, Expr, Scope};

#[test]
fn failed_outer_assignment_preserves_target_despite_nested_write() {
    let mut scope = Scope::new();
    scope.insert("target".into(), 9);
    let expr = Expr::Assign("target".into(), Box::new(Expr::Add(
        Box::new(Expr::Assign("target".into(), Box::new(Expr::Number(12)))),
        Box::new(Expr::Name("missing".into())),
    )));
    assert_eq!(eval(&expr, &mut scope), Err(EvalError::UnknownName("missing".into())));
    assert_eq!(scope.get("target"), Some(&9));
}
