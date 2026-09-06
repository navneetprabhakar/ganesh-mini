#[path = "solution.rs"]
mod solution;

#[test]
fn sixteen_byte_nonhex_payload_is_bad_hex() {
    assert!(matches!(solution::decode_key("KEY:00000000000000é"), Err(solution::KeyDecodeError::BadHex)));
}

#[test]
fn leading_plus_is_not_hexadecimal() {
    assert!(matches!(solution::decode_key("KEY:+000000000000000"), Err(solution::KeyDecodeError::BadHex)));
}
