from solution import MemoryCatalog

catalog = MemoryCatalog({'rows': [{}, {'v': None}]})
actual = catalog.select('rows', {'v': None})
print(repr(actual))
assert actual == [{'v': None}], 'a missing field is not a value equal to None'
