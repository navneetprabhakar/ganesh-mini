from solution import create_config, parse_config

account = "first\u2028second"
text = create_config({"account": account})
actual = parse_config(text)
assert actual["account"] == account, repr(actual)
