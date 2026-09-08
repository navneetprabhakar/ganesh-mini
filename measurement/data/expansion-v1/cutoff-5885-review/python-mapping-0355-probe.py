from solution import compile_catalog
assert compile_catalog({1: [('x', b'a')]}, ['sample2']) == {1: {'sample2': {'x': (97,)}}}
