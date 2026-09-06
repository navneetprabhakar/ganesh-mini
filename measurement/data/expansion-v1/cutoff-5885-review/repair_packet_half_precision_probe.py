import unittest
from solution import PacketTimeline


class ReviewProbe(unittest.TestCase):
    def test_integer_distance_strictly_above_odd_half(self):
        modulus = 2 ** 54 + 3
        last = modulus - 1
        raw = last - (modulus // 2 + 1)
        timeline = PacketTimeline(modulus)
        timeline.push(last)
        self.assertEqual(timeline.push(raw), modulus + raw)


if __name__ == '__main__':
    unittest.main()
