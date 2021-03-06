"""
There are exactly ten ways of selecting three from five, 12345:

123, 124, 125, 134, 135, 145, 234, 235, 245, and 345

In combinatorics, we use the notation, ^(5)C_(3) = 10.

In general,
^(n)C_(r) = 	
n!
r!(n r)!
	,where r <= n, n! = n (n 1) ... 3 2 1, and 0! = 1.

It is not until n = 23, that a value exceeds one-million: ^(23)C_(10) = 1144066.

How many, not necessarily distinct, values of  ^(n)C_(r), for 1 <= n <= 100, are greater than one-million?

Permutation of 123 (n=3) for 2 digit (r=2) -> n!/(n-r)! -> 6
12
13
21
23
31
32

Combination (non repeat) must reduce duplicate. If r=2 -> remove 2.
12
13 
21 <- already
23
31 <- already
32

if r = 3, there's only 1. remove 5. 
123

so the pattern is n!/( (n-r)! * r!)

"""
import math
count = 0
for n in xrange(1,101):
    for r in xrange(1,n):
        if math.factorial(n) / (math.factorial(r)*math.factorial(n-r)) > 1000000:
            count += 1

print count