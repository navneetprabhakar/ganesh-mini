import unittest
from solution import schedule_stages


class ReviewProbe(unittest.TestCase):
    def test_newly_ready_earlier_stage_precedes_later_ready_stage(self):
        self.assertEqual(schedule_stages({'first': ['base'], 'base': [], 'last': []}),
                         ('base', 'first', 'last'))


if __name__ == '__main__':
    unittest.main()
