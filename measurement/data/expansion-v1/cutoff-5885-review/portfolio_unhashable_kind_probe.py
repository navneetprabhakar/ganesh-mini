from solution import Portfolio

try:
    Portfolio().frozen_ids([])
except ValueError:
    pass
except Exception as exc:
    raise AssertionError(f'unsupported kind requires ValueError, got {type(exc).__name__}') from exc
else:
    raise AssertionError('unsupported kind accepted')
