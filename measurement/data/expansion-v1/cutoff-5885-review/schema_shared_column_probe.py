import unittest

from solution import upgrade, downgrade


class SharedColumnTests(unittest.TestCase):
    def test_unrelated_column_is_preserved(self):
        for operation in (upgrade, downgrade):
            with self.subTest(operation=operation.__name__):
                shared = {"nullable": "previous"}
                schema = {"documents": {"source": shared, "other": shared}}
                result = operation(schema)
                self.assertEqual(result["documents"]["other"], {"nullable": "previous"})
                self.assertEqual(shared, {"nullable": "previous"})


if __name__ == "__main__":
    unittest.main()
