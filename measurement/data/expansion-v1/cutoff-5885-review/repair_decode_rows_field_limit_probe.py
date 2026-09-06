import unittest
from solution import decode_rows


class Probe(unittest.TestCase):
    def test_valid_long_field(self):
        self.assertEqual(decode_rows(b'x'*140000), [['x'*140000]])


if __name__ == '__main__':
    unittest.main()
