from solution import Artifact, clone_exhibit

root = Artifact("0")
node = root
for index in range(1, 1200):
    child = Artifact(str(index))
    node.children.append(child)
    node = child
try:
    copied = clone_exhibit(root)
except RecursionError:
    raise AssertionError("1200-node acyclic Artifact graph exceeded reference recursion depth") from None
node = copied
for index in range(1200):
    assert node.name == str(index)
    if index < 1199:
        node = node.children[0]
assert copied is not root
