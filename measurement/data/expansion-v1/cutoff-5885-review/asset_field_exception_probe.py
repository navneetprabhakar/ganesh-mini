from solution import AssetDraft

try:
    AssetDraft('a', 1, 'IN', {})
except ValueError:
    pass
except Exception as exc:
    raise AssertionError(f'invalid label field requires ValueError, got {type(exc).__name__}') from exc
else:
    raise AssertionError('invalid label accepted')
