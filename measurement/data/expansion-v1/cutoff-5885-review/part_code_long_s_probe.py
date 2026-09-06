from solution import scan_part_codes

actual = list(scan_part_codes('part: ſAA-0000-U'))
print(repr(actual))
assert actual == [], 'non-ASCII long s must not be accepted as an ASCII letter'
