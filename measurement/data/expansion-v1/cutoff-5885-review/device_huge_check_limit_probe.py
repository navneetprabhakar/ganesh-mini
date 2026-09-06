from solution import DeviceCatalog

caught = None
try:
    DeviceCatalog([]).await_tag("missing", [], 10 ** 30)
except Exception as error:
    caught = error
assert isinstance(caught, TimeoutError), f"valid check limit raised {type(caught).__name__}: {caught}"
