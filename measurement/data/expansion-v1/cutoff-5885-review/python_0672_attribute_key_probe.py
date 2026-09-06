from solution import EntryOptions, build_entry

try:
    build_entry("book", EntryOptions(title="Title", attributes={1: "value"}))
except TypeError:
    pass
else:
    raise AssertionError("dict[str, object] attributes accepted an integer key")
