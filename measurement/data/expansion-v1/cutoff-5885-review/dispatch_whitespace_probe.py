import unittest
from solution import RepeatModule, Connection, Assistant


class DispatchWhitespaceTests(unittest.TestCase):
    def test_tab_delimits_command_token(self):
        connection = Connection()
        module = RepeatModule(connection, Assistant("bot"))
        self.assertTrue(module.dispatch("user", "!repeat\thello"))
        self.assertEqual(connection.sent, [("user", "hello")])


if __name__ == "__main__":
    unittest.main()
