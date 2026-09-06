import unittest
from datetime import date
from solution import prepare_expedition


class ExpeditionExplicitFinishTests(unittest.TestCase):
    def test_present_finish_must_be_date(self):
        data = dict(name='Trip', brief='Map', division='Science', leader='Asha',
                    start=date(2028, 3, 4), finish=None)
        with self.assertRaises(ValueError):
            prepare_expedition(data, ['Science'], ['Asha'])


if __name__ == '__main__':
    unittest.main()
