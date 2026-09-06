import unittest
from solution import compose_node_config


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_dictionary(self):
        common = {}
        cursor = common
        for _ in range(600):
            cursor['child'] = {}
            cursor = cursor['child']
        error = None
        try:
            result = compose_node_config(common, {}, 'unknown')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        for _ in range(600):
            result = result['child']
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
