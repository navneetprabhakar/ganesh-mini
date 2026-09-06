from solution import scan_part_codes

actual = list(scan_part_codes('part: KAA-0000-M'))
print(repr(actual))
assert actual == [], 'non-ASCII Kelvin sign must not be accepted as an ASCII letter'
