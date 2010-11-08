def pentagonals(l, startsfrom=1):
    for n in xrange(startsfrom,l+1):
        yield int(n*(3*n-1)*0.5)

def veryslow():
    pentcount = 10000
    pent = list(pentagonals(pentcount))
    minimum_D = 9999999999
    diffc = 0
    sumc = 0
    for j in xrange(pentcount-1):
        for k in xrange(j+1, pentcount):
            pdiff = pent[k]-pent[j]
            psum = pent[j]+pent[k]
            if pdiff in pent and psum in pent:
                minimum_D = min(minimum_D, pdiff)
    print minimum_D

import math
def is_pentagonal(y):
    """
    y = x(3x-1)/2.
    y is the input, we need to find x, and whether it's an positive integer. Using quadratic equation, we convert to the following:
    
    x = (-b +- sqrt(b^2-4ac))/2a
    since y = x(3x-1)/2 is 1.5*x^2 - 0.5*x - y = 0, then a = 1.5, b = 0.5, c = -y
    x = (0.5 +- sqrt(0.25+6y)/3. Since x must be positive integer, then -1.5 must be added with positive number. so:
    x = (0.5 + sqrt(0.25+6y)/3

    """
    x = (0.5 + math.sqrt(0.25+6*y))/3
    return x % int(x) == 0

def faster():
    j = 1
    k = 2
    while 1:
        #print "Pos k at",k
        while j < k:
            jval = j*(3*j-1)*0.5
            kval = k*(3*k-1)*0.5
            if is_pentagonal(jval+kval) and is_pentagonal(kval-jval):
                print "Found", kval-jval, "at", j,k
            j += 1
        k += 1
        j = 1

#veryslow() #took overnight
faster()