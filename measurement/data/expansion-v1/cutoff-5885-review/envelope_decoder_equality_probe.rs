#[path = "solution.rs"]
mod solution;
use solution::EnvelopeDecoder;

fn require_equality<T: PartialEq + Eq>() {}

#[test]
fn all_public_types_include_decoder_equality_traits() {
    require_equality::<EnvelopeDecoder>();
}
