import unittest
from solution import run_task_command


class TaskNumberTests(unittest.TestCase):
    def test_valid_decimal_one_with_leading_zeroes(self):
        records = [{"text": "task", "done": False}]
        result, output = run_task_command(records, ["finish", "0" * 5000 + "1"])
        self.assertEqual(output, "Finished 1")
        self.assertTrue(result[0]["done"])


if __name__ == "__main__":
    unittest.main()
