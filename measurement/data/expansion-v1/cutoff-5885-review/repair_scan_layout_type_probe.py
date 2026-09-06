import unittest
from solution import decode_scan


class Probe(unittest.TestCase):
    def test_malformed_layout(self):
        with self.assertRaises(ValueError):
            decode_scan({'rows': 0, 'columns': 0, 'channels': 0, 'layout': []}, [])


if __name__ == '__main__':
    unittest.main()
