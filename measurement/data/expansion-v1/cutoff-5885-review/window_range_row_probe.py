from solution import WindowBatcher

data = [range(2), range(2, 4)]
actual = WindowBatcher(1, 1, 0, data, [], []).train_examples
assert actual == ((((0, 1),), ((2, 3),)),), repr(actual)
