import unittest
from solution import decode_envelope


class Probe(unittest.TestCase):
    def test_valid_long_integer(self):
        text = '{"token":"x","values":[' + '1' * 5000 + ']}'
        error = None
        try:
            result = decode_envelope(text)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result['values'][0] % 10, 1)


if __name__ == '__main__':
    unittest.main()
