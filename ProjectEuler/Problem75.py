"""
a*a + b*b = c*c
sqrt(a*a + b*b) = c
L = a + b + c
 = a + b + c
"""

def countIntTriangleIsOne(L):
    #FAIL/SLOW
    total = 0
    for i in xrange(1,L):
        for j in xrange(i+1, L):
#             print L, "Try", i, j
            if (i + j) > L:
                break
            longside = (i*i+j*j)**0.5
#             print "long:", longside, "Total:", i+j+longside
            if longside > (L - i - j):
                if j == i+1:
                    return total
                else:
                    break
            found = (longside == (L - i - j) and longside % 1 == 0)
            if found:
                total += 1
                break
            if total > 1:
                return 0
    return total
    
def try2(L):
    #FAIL/SLOW
    """
    a*a + b*b = c*c, meaning c must be integer, thus c*c must have integer square root.
    e.g. 4, 9, 16, 25, ...
    to increase search speed, let's create a list of squares
    """
    limit = 10000000
    is_square = [False] * limit
    is_square[1] = True
    for i in xrange(2,int(limit**0.5)):
        if not is_square[i]:
            j = i*i
            while j < limit:
                is_square[j] = True
                j *= j
    squares = [i for i in xrange(1,limit) if is_square[i]]
    
    # then based on reduced set above, let's find a possible combination
    for i in xrange(0,len(squares)/2):
        for j in xrange(i+1, len(squares)/2):
            csq = squares[i]+squares[j]
            if is_square[csq]:
                triangle = squares[i]**0.5,squares[j]**0.5,csq**0.5
                print "possible triangle:", triangle, "L:", sum(triangle)
                if triangle[0]**2+triangle[1]**2 == triangle[2]**2:
                    print "TRIANGLE!"

    print squares
    
def try3():
    #FAIL/SLOW
    limit = 7500
    squares = [i*i for i in xrange(limit)]
    L = [0] * 15000
    for i in xrange(limit):
        for j in xrange(i+1, limit):
            c = (squares[i]+squares[j])**0.5
            el = int(i+j+c)
            if el < 15000 and c % 1 == 0:
                L[el] += 1
                
    print L
    print "Ans:", sum([1 for i in L if i == 1])

def try4():
    """
    Based on euclidian formulae at
    http://en.wikipedia.org/wiki/Pythagorean_triple
    """
    #for L to reach 1.5M, a+b+c must be <= 1.5M,
    #m^2 - n^2 + 2mn + m^2 + n^2 = 2m^2 + 2mn = 2m(m + n) <= 1.5M
    # m(m + n) <= 750K, m^m + mn <= 750K, mn <= 750k - m^m
    # n <= (750K - m^m)/m, or solving for m
    # m < 500*3**0.5
    # or it's easier to use wolfram: http://www.wolframalpha.com/input/?i=m*m+-+n*n+%2B+2*m*n+%2B+m*m+%2B+n*n+%3C%3D+1500000%2C+m+%3E+0%2C+n+%3E+0%2C+m+%3E+n
    limit_m2 =int(500*3**0.5)
    limit_m1 = int(250*6**0.5)
    Ls = [dict()] * (1500000+1)
    #"given an arbitrary pair of positive integers m and n with m > n"
    for m in xrange(2,limit_m2+1):
        limit_n = ((750000 - m*m)/m) + 1 if m > limit_m1 else m
        for n in xrange(1, limit_n):
            #k*2*m*(m+n) <= 1500000 or k <= 7500000/(m*(m+n))
            limit_k = (750000/(m*(m+n))) + 1
            for k in xrange(1, limit_k):
                #k*(m*m - n*n) + k*2*m*n + k*(m*m + n*n)  -> k*2*m*(m+n)
                L = k*2*m*(m+n)
                # a and b sometimes exchanges, c is stable (by experiment) thus appropriate for identification
                c = k*(m*m + n*n)
                if not Ls[L]:
                    Ls[L] = set([c])
                else:
                    Ls[L] |= set([c])
    return map(len, Ls).count(1)
    
from time import time

st = time()
print "ans:", try4()
print time()-st