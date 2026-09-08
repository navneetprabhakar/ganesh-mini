from types import MappingProxyType
from solution import stage_module
assert stage_module('', 'https://example.test/', MappingProxyType({}), {}) == dict(url=None, filename=None, source=None, downloaded=False, cache={})
