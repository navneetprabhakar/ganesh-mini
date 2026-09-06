from solution import render_waypoints

try:
    actual = render_waypoints('0\n   \n')
except ValueError:
    pass
else:
    raise AssertionError(f'blank title accepted: {actual!r}')
