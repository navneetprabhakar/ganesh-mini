from solution import ParcelCrate

sentinel = TypeError("copy sentinel")

class CopyFailure:
    def __deepcopy__(self, memo):
        raise sentinel

caught = None
try:
    ParcelCrate("owner", [CopyFailure()])
except Exception as error:
    caught = error
assert caught is sentinel, f"copy exception was replaced: {type(caught).__name__}: {caught}"
