import unittest
from solution import encode_register_write

class Probe(unittest.TestCase):
    def test_bytes_like_memoryview_rejected(self):
        with self.assertRaises(ValueError):
            encode_register_write(0, memoryview(b'a'))

if __name__ == '__main__':
    unittest.main()
