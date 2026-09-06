from solution import prepare_measurements

record = {'x': 2}
actual = prepare_measurements([record, record], ['x'])
print(repr(actual))
assert actual['rows'] == [{'x': 0.0}, {'x': 0.0}], 'repeated input reference must not normalize the same row twice'
assert record == {'x': 2}
