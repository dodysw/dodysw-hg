"""
THIS FUCKING TAKES A LONG TIME!!
"""
count = 0
for n in xrange(10**18):
    if sum(map(int, str(n))) == sum(map(int, str(137*n))):
        count += 1
        print n
