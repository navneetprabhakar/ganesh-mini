from solution import encode_grid, FormatError

caught = None
try:
    encode_grid([], ["name"], [])
except Exception as error:
    caught = error
assert isinstance(caught, FormatError), f"invalid style raised {type(caught).__name__}"
