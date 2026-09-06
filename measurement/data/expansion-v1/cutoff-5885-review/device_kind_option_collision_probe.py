from solution import expand_device_profiles

actual = expand_device_profiles([{"kind": "phone", "device_kind": ["option"]}])
assert actual[0]["device_kind"] == "phone", f"option overwrote required kind: {actual!r}"
