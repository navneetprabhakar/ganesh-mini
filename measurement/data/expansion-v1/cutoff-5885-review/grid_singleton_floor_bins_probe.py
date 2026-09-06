from solution import GridReducer

# floor(i / 2): first bin empty, second bin contains the singleton.
actual = GridReducer("maximum", [(1, 2)]).reduce([[[7]]])
assert actual == [[0.0, 7]], f"floor-defined singleton bins: {actual!r}"
