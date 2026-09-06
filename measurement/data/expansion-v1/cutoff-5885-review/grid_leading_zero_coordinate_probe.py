import unittest
from solution import GridRoom


class GridLeadingZeroTests(unittest.TestCase):
    def test_valid_decimal_coordinate(self):
        room = GridRoom(2, 2)
        participant = room.join('user', {})
        self.assertEqual(room.execute(participant, 'place ' + '0' * 5000 + '1 0'), (1, 0))


if __name__ == '__main__':
    unittest.main()
