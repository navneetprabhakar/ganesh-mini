from solution import partition_enrollment

actual = partition_enrollment('given,family,contact,tier,optional\nA,B,a@x,starter\n')
print(repr(actual))
assert actual == {'starter': [], 'experienced': [], 'warnings': ['row 2: malformed']}, 'missing column must make data row malformed'
