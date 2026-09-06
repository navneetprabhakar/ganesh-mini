import unittest
from solution import update_library


class ReviewProbe(unittest.TestCase):
    def test_unhashable_operation(self):
        with self.assertRaises(ValueError):
            update_library({}, {}, [{'op': [], 'id': 1}])


if __name__ == '__main__':
    unittest.main()
