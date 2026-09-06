from solution import parse_cents

assert parse_cents('0' * 5000 + '1') == (True, 100)
