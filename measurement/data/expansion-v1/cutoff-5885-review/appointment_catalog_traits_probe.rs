#[path = "solution.rs"]
mod solution;

use solution::AppointmentCatalog;

fn require_eq<T: Eq>() {}

#[test]
fn catalog_implements_the_required_public_type_equality_trait() {
    require_eq::<AppointmentCatalog>();
}
