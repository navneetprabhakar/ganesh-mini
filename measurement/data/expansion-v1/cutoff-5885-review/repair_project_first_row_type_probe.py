import unittest
from solution import project_rows


class ReviewProbe(unittest.TestCase):
    def test_first_weight_row_container_type(self):
        with self.assertRaises(TypeError):
            project_rows([], [(1,)], [0])


if __name__ == '__main__':
    unittest.main()
