from time import time
from math import log10
st = time()

limit = 100

#http://en.wikipedia.org/wiki/Methods_of_computing_square_roots
#digit by digit calculation (long division)
def sqrt1(n, size=100):
    #Let p be the part of the root found so far, ignoring any decimal point. (For the first step, p = 0).
    p = r = i = 0
    #preparation
    q = n
    pairs = []
    while q > 0:
        q,t = divmod(q, 100)
        pairs.append(t)
    decimal_pos = 0
    for i in xrange(size):
        #Starting on the left, bring down the most significant (leftmost) pair of digits not yet used
        a = 0
        if pairs:
            a = pairs.pop()
        elif decimal_pos == 0:
            decimal_pos = i

        c = r*100 + a
        #Determine the greatest digit x such that y = (20*p + x)*x does not exceed c
        x = 0
        while (20*p + x+1) * (x+1) <= c:
            x += 1
        y = (20*p + x) * x
        #Place the digit x as the next digit of the root
        p = p*10 + x
        if not pairs and c == 0:
            break
        
        #Subtract y from c to form a new remainder.
        r = c - y
        i += 1

    return p, decimal_pos

#by drea   (Python)
def buildLongSqrt(aNum):
    startNum = 1
    count = 0
    bigNum = 0
    numLeft = aNum
    for i in range(100):
        while numLeft >= startNum:
            numLeft -= startNum
            startNum += 2
            count += 1
        bigNum = (bigNum * 10) + count
        numLeft *= 100
        startNum = (bigNum * 20) + 1
        count = 0
    return bigNum

total = 0
for n in xrange(2,101):
    s = sqrt1(n,100)
    decimals = str(s[0])
    if len(decimals) < 100:
        continue
    sum_digits = sum(map(int, decimals))
    total += sum_digits
        
print "ans:", total
print time() - st