import unittest
from solution import partition_by_state


class Probe(unittest.TestCase):
    def test_finite_item(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            partition_by_state([value], 0)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
