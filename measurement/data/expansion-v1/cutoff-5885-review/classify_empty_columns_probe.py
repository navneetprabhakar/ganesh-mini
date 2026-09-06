from solution import classify_rows

actual = classify_rows({"a": [], "b": ()})
assert actual == {"Decision": []}, repr(actual)
