#[path = "solution.rs"]
mod solution;
use solution::{decode_profile, ProfileError};

#[test]
fn quiet_is_a_zero_or_one_literal_not_a_general_u16() {
    assert_eq!(decode_profile("force=1;heat=2;rate=3;quiet=+1"),
               Err(ProfileError::MalformedField));
}

#[test]
fn whitespace_anywhere_includes_unicode_whitespace() {
    assert_eq!(decode_profile("force\u{2003}=1;heat=2;rate=3;quiet=0"),
               Err(ProfileError::MalformedField));
}
