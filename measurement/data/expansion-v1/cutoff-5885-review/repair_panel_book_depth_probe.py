import unittest
from solution import PanelBook


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_panel_content(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            PanelBook({'main': value})
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
