import sys

n = int(sys.argv[1])
for i in range(n - 1, -1, -1):
    print(' ' * i + '#' * (n - i))
