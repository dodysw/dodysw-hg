import math

total = 0

for x in xrange(10,9999999):
    if x == sum([math.factorial(int(c)) for c in str(x)]):
        print x
        total += x
    
print "Total", total
    