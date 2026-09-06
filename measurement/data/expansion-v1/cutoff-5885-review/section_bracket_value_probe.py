import unittest
from solution import parse_sections


class AssignmentBracketTests(unittest.TestCase):
    def test_assignment_value_may_end_with_bracket(self):
        self.assertEqual(parse_sections(["[main]", "value=items[0]"]), [{"name": "main", "values": {"value": "items[0]"}}])


if __name__ == "__main__":
    unittest.main()
