import unittest
from solution import build_rail_plan

class RailWidthProbe(unittest.TestCase):
    def test_finite_centered_tracks_when_total_width_overflows(self):
        plan = build_rail_plan({'plan_id': 'p', 'name': 'n', 'segments': [{
            'id': 's', 'start': [0.0, 0.0], 'length': 1.0, 'heading': 0.0,
            'tracks': [{'id': 'a', 'width': 1e308}, {'id': 'b', 'width': 1e308}],
        }]})
        tracks = plan.segments[0].tracks
        self.assertEqual(tracks[0].start, (0.0, -5e307))
        self.assertEqual(tracks[1].start, (0.0, 5e307))

if __name__ == '__main__':
    unittest.main()
