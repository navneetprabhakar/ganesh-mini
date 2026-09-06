import unittest
from solution import score_gesture_plan


class GestureAdditivityTests(unittest.TestCase):
    def test_complete_mapping_is_sum_of_individual_rounds(self):
        rows = [(g, t) for g in ("stone", "sheet", "shears") for t in ("low", "mid", "high")]
        individual = [score_gesture_plan([row]) for row in rows]
        self.assertEqual(tuple(map(sum, zip(*individual))), (57, 57))
        self.assertEqual(score_gesture_plan(rows), (57, 57))


if __name__ == "__main__":
    unittest.main()
