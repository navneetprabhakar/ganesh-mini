from solution import nearest_bundle

# Root is a normalized absolute directory in the virtual entry set.
assert nearest_bundle('/a/doc', 'ember', {'/', '/a', '/a/ember.lock'}) == '/a'
