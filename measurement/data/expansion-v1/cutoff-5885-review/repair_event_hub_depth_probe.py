import unittest
from solution import EventHub


class Probe(unittest.TestCase):
    def test_finite_payload(self):
        value = []
        for _ in range(600):
            value = [value]
        hub = EventHub()
        hub.subscribe('[event]', lambda payload: 'called')
        error = None
        try:
            result = hub.emit('[event]', value)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, ['called'])


if __name__ == '__main__':
    unittest.main()
