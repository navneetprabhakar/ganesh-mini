from solution import register_entries

try:
    actual = register_entries({'items': [1], 'next_id': 1}, [])
except ValueError:
    pass
else:
    raise AssertionError(f'non-dictionary existing item accepted: {actual!r}')
