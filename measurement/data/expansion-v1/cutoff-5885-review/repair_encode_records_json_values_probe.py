import unittest
from solution import encode_records


class Probe(unittest.TestCase):
    def test_non_json_values_rejected(self):
        for value in ((1, 2), {1: 'x'}):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    encode_records([{'x': value}])


if __name__ == '__main__':
    unittest.main()
