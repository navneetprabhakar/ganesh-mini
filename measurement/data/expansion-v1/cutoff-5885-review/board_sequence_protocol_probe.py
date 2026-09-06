from solution import RecordBoard

class Records:
    def __getitem__(self, index):
        if index == 0:
            return {"label": "one"}
        raise IndexError(index)

assert list(Records()) == [{"label": "one"}]
actual = RecordBoard(Records()).rows()
assert actual == [{"label": "one", "icon": None, "marked": False}], repr(actual)
