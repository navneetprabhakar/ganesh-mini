import unittest
from solution import run_transform_chain


class Probe(unittest.TestCase):
    def test_malformed_operation_value_error(self):
        with self.assertRaises(ValueError):
            run_transform_chain(1, [{'op': [], 'amount': 1}])

    def test_finite_integer_no_stages(self):
        self.assertEqual(run_transform_chain(10**400, []), 10**400)


if __name__ == '__main__':
    unittest.main()
