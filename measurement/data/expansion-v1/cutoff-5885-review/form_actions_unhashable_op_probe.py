import unittest

from solution import apply_form_actions


class MalformedOperationTests(unittest.TestCase):
    def test_unhashable_operation_raises_value_error(self):
        for operation in ([], {}):
            with self.subTest(operation=operation):
                with self.assertRaises(ValueError):
                    apply_form_actions({}, [{"op": operation}])


if __name__ == "__main__":
    unittest.main()
