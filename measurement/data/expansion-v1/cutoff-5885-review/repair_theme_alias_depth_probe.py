import unittest
from solution import combine_theme


class Key:
    pass


class Probe(unittest.TestCase):
    def test_override_key_not_aliased(self):
        key = Key()
        result = combine_theme({}, {key: 1})
        self.assertIsNot(next(iter(result)), key)

    def test_finite_payload(self):
        value = {}
        for _ in range(600):
            value = {'x': value}
        error = None
        try:
            combine_theme({'x': value}, {})
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
