from solution import save_member

def member(identifier, handle):
    return {'id': identifier, 'handle': handle, 'email': f'{identifier}@x', 'secret': 's', 'avatar': None, 'tags': []}

profile = {'handle': 'new', 'email': 'new@x', 'secret': 's', 'avatar': None, 'tags': []}
try:
    actual = save_member([member(1, 'same'), member(2, ' SAME ')], profile)
except (TypeError, ValueError):
    pass
else:
    raise AssertionError(f'existing normalized duplicate handles accepted: {actual!r}')
