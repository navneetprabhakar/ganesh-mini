from solution import load_transform

caught = None
try:
    load_transform({"type": []})
except Exception as error:
    caught = error
assert isinstance(caught, ValueError), f"unknown transform type raised {type(caught).__name__}"
