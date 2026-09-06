from solution import interpret_utterance

actual = interpret_utterance('hié', 10, {})
print(repr(actual))
assert actual == {'action': 'retry', 'speech': 'Please say that again.', 'target': None}, 'hi is not a complete alphanumeric token'
