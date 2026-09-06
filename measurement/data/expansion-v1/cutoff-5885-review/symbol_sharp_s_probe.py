from solution import pack_symbols

actual = pack_symbols('AßB')
print(repr(actual))
assert actual == '00|01', 'unsupported sharp s must be skipped, not expanded into two supported letters'
