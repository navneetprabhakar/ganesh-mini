import unittest
from solution import make_grid, set_cell


class Probe(unittest.TestCase):
    def test_only_selected_cell_changes(self):
        row = [0]
        grid = [row, row]
        self.assertIs(set_cell(grid, 0, 0, 1), grid)
        self.assertEqual(grid, [[1], [0]])

    def test_finite_fill(self):
        value = {}
        for _ in range(600):
            value = {'x': value}
        error = None
        try:
            make_grid(1, 1, value)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
