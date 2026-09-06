from solution import CentroidBinaryClassifier

model = CentroidBinaryClassifier([{"label": 0, "x": 0.0}, {"label": 1, "x": 1e200}]).fit()
assert model.predict([[0.0]]) == [0]
