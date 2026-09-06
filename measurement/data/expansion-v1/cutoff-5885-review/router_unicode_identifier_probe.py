from solution import CommandRouter

name = "é"
assert name.isidentifier()
router = CommandRouter()
router.register("/{" + name + "}", "target")
assert router.resolve("/value") == ("target", {name: "value"})
