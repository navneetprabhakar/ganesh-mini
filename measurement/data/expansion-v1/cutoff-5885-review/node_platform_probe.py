import unittest
from solution import create_node


class ReviewProbe(unittest.TestCase):
    def test_unhashable_platform(self):
        with self.assertRaises(ValueError):
            create_node('node', '127.0.0.1', platform=[])


if __name__ == '__main__':
    unittest.main()
