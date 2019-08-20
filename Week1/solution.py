import sys

digit_string = sys.argv[1]
digit = int(digit_string)
s = 0

while digit:
    s += digit % 10
    digit //= 10

print(s)
