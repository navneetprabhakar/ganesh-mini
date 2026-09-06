#[path = "solution.rs"]
mod solution;
use solution::parse_packet;
#[test]
fn accepted_attribute_values_must_not_silently_lose_carriage_returns() {
    // LF is the delimiter. If CRLF is instead considered malformed, rejection
    // is also acceptable here; accepting it while altering the value is not.
    if let Ok(packet) = parse_packet(b"READ /\nkey:value\r\nnext:kept\n\nbody") {
        assert_eq!(packet.attributes[0].1, "value\r");
    }
}
