from solution import SignalDataset

assert SignalDataset().features([1e308, 1e308, 1e308]) == (1e308, 0.0, 0.0, 0.0)
