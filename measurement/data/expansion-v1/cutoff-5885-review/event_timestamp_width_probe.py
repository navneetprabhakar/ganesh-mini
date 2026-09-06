from solution import decode_event_batch

try:
    actual = decode_event_batch('id=x|at=202411T000000|cents=1|category=c', set())
except ValueError:
    pass
else:
    raise AssertionError(f'non-YYYYMMDD timestamp accepted: {actual!r}')
