import math

def triagen():
    n = i = 1
    while 1:
        yield i
        n += 1
        i += n
        
def divisor_count(n):
    divcount = 0
    tmax = math.sqrt(n)
    for t in xrange(1, tmax+1):
        if n % t == 0:
            divcount += 2
    if n == tmax:
        divcount -= 1
    return divcount
        
for i in triagen():
    divnum = divisor_count(i)
    if divnum > 150:
        print i, divnum
    if  divnum > 500:
        print i
        break