"""
1, 3, 5, 7, 9 -> 2   3x3
13, 17, 21, 25 -> 4  5x5
31, 37... -> 6
"""
total = 1
n = 3
for i in xrange(3, 1002, 2):
    o = i - 1
    diagonals = [n, n + o, n + 2*o, n + 3*o]
    print diagonals
    total += sum(diagonals)
    n = n + 3*o + i + 1
    
print total