from solution import parse_cards

source = "Q: First?\r\n- yes\r\n- no\r\nA: 1\r\n\r\nQ: Second?\r\n- left\r\n- right\r\nA: 2"
actual = parse_cards(source)
assert [card["answer"] for card in actual] == ["yes", "right"], repr(actual)
