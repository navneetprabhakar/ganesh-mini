import base64
import hashlib
import hmac
from solution import read_credential

def encode(value):
    return base64.urlsafe_b64encode(value).rstrip(b'=').decode('ascii')

payload = encode(b'{"exp":100,"sub":"a","sub":"b"}')
signature = encode(hmac.new(b'secret', payload.encode('ascii'), hashlib.sha256).digest())
try:
    actual = read_credential(payload + '.' + signature, 0, 'secret')
except ValueError as exc:
    assert str(exc) == 'invalid credential'
else:
    raise AssertionError(f'noncanonical duplicate-claim credential accepted: {actual!r}')
