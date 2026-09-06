from solution import process_inbox

raw = {'id': 'x', 'items': []}
def parse(value):
    value['items'].append('parsed')
    return value

process_inbox([('x.packet', raw)], parse, lambda value: True)
assert raw == {'id': 'x', 'items': []}, 'parser mutated caller-owned raw input'
