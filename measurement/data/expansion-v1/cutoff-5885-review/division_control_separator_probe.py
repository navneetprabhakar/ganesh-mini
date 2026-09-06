from solution import divide_integer_text

text = '\x1c1'
try:
    int(text, 10)
except ValueError:
    pass
else:
    raise AssertionError('oracle expected Python int to reject separator')
actual = divide_integer_text(text, '1')
print(repr(actual))
assert actual.kind == 'invalid', 'parsing must follow Python base-10 int syntax'
