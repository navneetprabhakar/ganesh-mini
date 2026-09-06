from solution import compose_command_catalog

fallback = {"namespace": "fallback", "commands": [], "metadata": {}}
section = {"namespace": " ", "commands": ["run"], "metadata": {}}
actual = compose_command_catalog([section], fallback)
assert actual[1]["namespace"] == " "
