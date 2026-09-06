import logging
import unittest
from solution import BaseUnit


class FalseyLogger(logging.Logger):
    def __init__(self):
        super().__init__("probe")
        self.messages = []

    def __bool__(self):
        return False

    def debug(self, message, *args, **kwargs):
        self.messages.append(message)


class SuppliedLoggerTests(unittest.TestCase):
    def test_falsey_logger_instance_is_used(self):
        logger = FalseyLogger()
        BaseUnit(logger).initialize()
        self.assertEqual(logger.messages, ["base:initialization"])


if __name__ == "__main__":
    unittest.main()
