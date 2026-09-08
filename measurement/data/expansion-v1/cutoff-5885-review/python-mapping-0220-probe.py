from types import MappingProxyType
from solution import DocumentActivator
x = DocumentActivator(MappingProxyType({'doc': {'sections': ['x']}}))
assert x.activate('doc').value == {'sections': ['x']}
