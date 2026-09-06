import unittest
from solution import collect_values


class Reader:
    def __init__(self, value):
        self.value = value
        self.closes = 0

    def read(self, key):
        return self.value

    def close(self):
        self.closes += 1


class Session:
    def __init__(self, reader):
        self.reader = reader

    def open(self):
        return self.reader


class Probe(unittest.TestCase):
    def test_finite_reader_value(self):
        value = []
        for _ in range(600):
            value = [value]
        reader = Reader(value)
        error = None
        try:
            collect_values(Session(reader), ['x'])
        except Exception as exc:
            error = type(exc).__name__
        self.assertEqual(reader.closes, 1)
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
