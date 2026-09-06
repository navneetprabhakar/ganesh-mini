from solution import SignalGuidance

class Model:
    dropout_probability = float('nan')
    mode = 'caption'
    def __call__(self, signal, metadata):
        return []

try:
    SignalGuidance(Model())
except ValueError:
    pass
else:
    raise AssertionError('NaN does not satisfy dropout_probability > 0')
