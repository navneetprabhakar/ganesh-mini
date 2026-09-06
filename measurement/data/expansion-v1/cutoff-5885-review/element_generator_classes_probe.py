from solution import Element

classes = (name for name in ["primary", "wide"])
actual = Element("div", class_=classes).render()
assert actual == '<div class="primary wide"></div>', repr(actual)
