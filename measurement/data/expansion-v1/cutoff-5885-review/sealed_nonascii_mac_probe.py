from solution import SealedText

valid = SealedText('x', b's', 0).token
malformed = valid.rsplit('|', 1)[0] + '|\u2603'
try:
    SealedText.from_token(malformed, b's')
except ValueError:
    pass
except Exception as exc:
    raise AssertionError(f'malformed string token requires ValueError, got {type(exc).__name__}') from exc
else:
    raise AssertionError('malformed MAC accepted')
