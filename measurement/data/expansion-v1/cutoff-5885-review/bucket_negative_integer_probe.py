import unittest
from solution import bucketize_vectors

class BucketNegativeProbe(unittest.TestCase):
    def test_large_negative_integer_is_value_error(self):
        with self.assertRaises(ValueError):
            bucketize_vectors([[-10 ** 400]], 1)

if __name__ == '__main__':
    unittest.main()
