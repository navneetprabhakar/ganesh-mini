import unittest
from solution import combine_sensors


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_sample(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            combine_sensors([{'name': 'd'}], [[{'code': 'a', 'label': ''}]], [{'a': value}])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
