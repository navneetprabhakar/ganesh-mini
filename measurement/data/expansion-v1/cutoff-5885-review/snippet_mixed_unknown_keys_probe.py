from solution import SnippetTemplate

try:
    SnippetTemplate({1: 'x', 'unknown': 'y'})
except ValueError:
    pass
except Exception as exc:
    raise AssertionError(f'unknown keys require ValueError, got {type(exc).__name__}') from exc
else:
    raise AssertionError('unknown keys accepted')
