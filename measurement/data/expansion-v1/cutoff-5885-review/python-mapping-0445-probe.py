from types import MappingProxyType
from solution import find_notices
x = dict(id='1', district='d', locality='l', department='p', arrangement='a', published=True)
assert find_notices([MappingProxyType(x)], {'authenticated': True}, district='d', locality='l') == [x]
