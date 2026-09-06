import unittest

from solution import StrokeBuffer


class FiniteCoordinateTests(unittest.TestCase):
    def test_finite_large_integer_point(self):
        buffer = StrokeBuffer()
        buffer.start("black")
        buffer.add(10 ** 400, 0)
        self.assertEqual(buffer.stop()["points"], [(10 ** 400, 0)])


if __name__ == "__main__":
    unittest.main()
